"""
엣지 캡처 이미지 VLM 해석 평가 (YOLO → VLM) — Qwen3-VL-2B / Qwen2-VL-2B × (이미지 30 + 영상 30) = 120건.

엣지 디바이스의 YOLO 가 캡처한 장면을 VLM 이 '얼마나 자세히' 해석하는지 평가한다.
1차 지표: 해석 상세도(0~5)·출력 길이. 2차: 위험유형(화재/낙상/전도) 인식 정확도·과잉해석(오탐)·지연(엣지 운용).
한 번에 모델 1개만 GPU 상주(fp16) — 모델 교체 시 이전 모델 해제.

사용: venv\\Scripts\\python.exe run_benchmark.py [--models qwen3,qwen2] [--limit N] [--media image,video]
전제: 통합 DATA 에 이미지·영상 준비 완료 (config.IMAGE_DIR · VIDEO_DIR → LLM/DATA).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")  # 전시회/.env (HF_TOKEN)
except ImportError:
    pass

import torch  # noqa: E402

import config as C  # noqa: E402
import vlm_engine as E  # noqa: E402


# ── 데이터셋 수집 ────────────────────────────────────────────────
def build_dataset(media_filter: set[str], limit: Optional[int]) -> List[Dict]:
    """dataset/ 의 이미지/영상을 항목 리스트로. category 미상/짝없음은 건너뜀."""
    items: List[Dict] = []
    if "image" in media_filter and C.IMAGE_DIR.exists():
        for p in sorted(C.IMAGE_DIR.iterdir()):
            if p.suffix.lower() in C.IMAGE_EXTS:
                items.append(_make_item(p, "image"))
    if "video" in media_filter and C.VIDEO_DIR.exists():
        for p in sorted(C.VIDEO_DIR.iterdir()):
            if p.suffix.lower() in C.VIDEO_EXTS:
                items.append(_make_item(p, "video"))
    items = [it for it in items if it["category"]]   # 카테고리 식별된 것만
    items.sort(key=lambda it: (it["media"], it["name"]))
    if limit:
        # media 별로 limit 개씩
        out, seen = [], {"image": 0, "video": 0}
        for it in items:
            if seen[it["media"]] < limit:
                out.append(it)
                seen[it["media"]] += 1
        items = out
    return items


def _make_item(path: Path, media: str) -> Dict:
    cat = C.category_of(path.stem)
    meta = C.CATEGORIES.get(cat, {})
    return {
        "path": path, "name": path.name, "stem": path.stem, "media": media,
        "category": cat, "expected": meta.get("label"), "danger": meta.get("danger"),
    }


# ── 판정 파싱 / 지표 ─────────────────────────────────────────────
# 위험 3종 어휘 — 단독 '불'(불투명·불빛 등 오매칭)을 '불길/불꽃/불이 나' 등으로 한정
_DANGER_WORDS = re.compile(
    r"위험|화재|불길|불꽃|불이\s*(?:나|붙)|화염|연기|"          # 화재·연기
    r"쓰러|낙상|실신|기절|넘어(?:져|짐|진|졌|가)|"             # 사람 쓰러짐/넘어짐
    r"전도|전복|기울어|쓰러진|"                                 # 기계·장비 전도
    r"응급|위급|사고"
)
# 위험 유형 파싱용 키워드 (프롬프트가 유형을 '화재/낙상/전도/없음' 중 하나로 강제)
_TYPE_PATTERNS = [
    ("화재", re.compile(r"화재|연기|화염|불")),
    ("전도", re.compile(r"전도|전복|기울|기계|장비|지게차|크레인")),
    ("낙상", re.compile(r"낙상|쓰러|넘어|실신|기절")),
]
# 정상 결론 신호(본문) — '정상 상태'·'위험 없음'·'위험요소 부재'(나열 후 부재 포함). '안전하지 않'·'비정상'은 제외
_SAFE_WORDS = re.compile(
    r"(?<!비)정상\s*(?:상태|적|이며|입니다|으로|인|이고|이라)|평범한|"
    r"안전(?!\s*(?:하지\s*)?않)\s*(?:상태|하며|합니다|한|하게)|"
    r"이상\s*없|특이\s*사항.{0,8}없|문제\s*없|"
    r"위험.{0,15}(?:없|존재하지\s*않|관찰되지\s*않|보이지\s*않|발견되지\s*않)|"
    r"(?:화재|연기|사고|위험\s*요소).{0,15}(?:없|존재하지\s*않|보이지\s*않)"
)
# 위험 단어의 '부재'(예: '화재 없음')를 부정 문맥으로 보고 비활성화 — 위험 매칭 직후 윈도우에서만 탐지
_NEG = re.compile(r"없|아니|않|전혀|보이지|관찰되지|발견되지|감지되지|미\s*발생")
_NEG_WINDOW = 20


def _danger_active(text: str) -> bool:
    """위험 단어가 '부정 문맥이 아닌' 위치에서 매칭되면 True (예: '화재 없음'은 비활성)."""
    for mm in _DANGER_WORDS.finditer(text):
        if not _NEG.search(text[mm.end(): mm.end() + _NEG_WINDOW]):
            return True
    return False


def parse_verdict(text: str) -> str:
    """모델 출력 → '위험' | '정상' | '불명'.
    '판정:' 라인에 위험·정상 중 '하나만' 있으면 그것, 둘 다('위험 / 정상' 에코)거나 라인이 없으면
    '불명'(= 모델이 하나로 결정하지 못함 = 오답). 본문으로 추론하지 않는다."""
    if not text:
        return "불명"
    head = re.search(r"(?:VERDICT|\"?판정\"?)\s*[:：]\s*\*{0,2}\s*([^\n]+)", text, re.I)
    if not head:
        return "불명"
    seg = head.group(1)
    has_d = bool(re.search(r"위험|이상(?!\s*없)|danger", seg, re.I))
    has_s = bool(re.search(r"정상|안전|normal", seg, re.I))
    if has_d and not has_s:
        return "위험"
    if has_s and not has_d:
        return "정상"
    return "불명"   # 둘 다(에코) 또는 둘 다 아님 → 결정 실패 = 오답


def description_of(text: str) -> str:
    """상세 해석 본문 추출 — JSON '설명' 값 우선, 그다음 '설명:'/'근거:', 없으면 헤더 제외 나머지."""
    text = text or ""
    mj = re.search(r'"\s*설명\s*"\s*[:：]\s*"(.*?)"\s*[},]?\s*$', text, re.S)   # JSON 형식
    if mj:
        return mj.group(1).strip()
    for key in ("설명", "근거"):
        m = re.search(rf"\"?{key}\"?\s*[:：]\s*(.+)", text, re.S)
        if m:
            return m.group(1).strip().strip('"{}').strip()
    body = "\n".join(
        ln for ln in text.splitlines()
        if not re.match(r'\s*[\"{]?\s*(?:판정|유형)', ln)
    )
    return body.strip()


# 해석 상세도(0~5) 채점용 — 캡처 해석이 얼마나 풍부한지 근사 (Qwen3-VL 한국어 서술 어휘 반영)
_ASPECT_OBJECT = re.compile(
    r"차량|자동차|트럭|버스|오토바이|사람|인물|작업자|직원|환자|보행자|군중|"
    r"지게차|크레인|기계|장비|로봇|컨베이어|화물|적재물|컨테이너|박스|카트|"
    r"연기|불|화염|불길|불꽃|소화|들것|침대|헬멧|소방관|구급")
_ASPECT_CONTEXT = re.compile(
    r"주차장|창고|공장|작업장|현장|실내|실외|야외|야간|바닥|지면|근처|주변|배경|"
    r"도로|거리|골목|입구|출입구|선반|통로|복도|광장|매장|상점|건물|벽")
_ASPECT_SEVERITY = re.compile(
    r"심각|위급|위험|즉시|긴급|신속|대피|신고|조치|대응|확산|번질|부상|"
    r"119|소방|구조|구급|후송|이송|점검|확인\s*필요|주의|경보")


def detail_score(text: str, pred: str, pred_type: str) -> int:
    """해석 상세도 0~5: 객체식별 + 판정제시 + 유형식별 + 공간·맥락묘사 + 심각도·조치언급."""
    t = text or ""
    s = 0
    if _ASPECT_OBJECT.search(t):
        s += 1
    if pred in ("위험", "정상"):
        s += 1
    if pred_type != "-":          # 화재/낙상/전도/없음 중 하나를 제시
        s += 1
    if _ASPECT_CONTEXT.search(t):
        s += 1
    if _ASPECT_SEVERITY.search(t):
        s += 1
    return s


def parse_danger_type(text: str) -> str:
    """위험 유형 → '화재'|'낙상'|'전도'|'없음'|'-'. '유형:' 라인 우선, 없으면 본문 키워드."""
    if not text:
        return "-"
    m = re.search(r"\"?유형\"?\s*[:：]\s*\*{0,2}\s*([^\n]+)", text)
    seg = (m.group(1) if m else text)[:40]
    if re.search(r"없|해당\s*없|정상", seg) and not re.search(r"화재|연기|쓰러|전도|넘어", seg):
        return "없음"
    for name, pat in _TYPE_PATTERNS:
        if pat.search(seg):
            return name
    return "-"


def confusion(records: List[Dict]) -> Dict:
    """위험=positive 기준 지표. '불명'(모델이 위험/정상 하나로 결정 못함, 예: '위험 / 정상' 에코)은
    오답으로 보고 분모에 포함한다(정확도를 깎음)."""
    tp = tn = fp = fn = un_pos = un_neg = 0
    for r in records:
        if r.get("error") or not r.get("expected"):
            continue
        exp, pred = r["expected"], r.get("pred")
        if pred == "위험":
            if exp == "위험":
                tp += 1
            else:
                fp += 1   # 오탐(정상을 위험이라 함)
        elif pred == "정상":
            if exp == "정상":
                tn += 1
            else:
                fn += 1   # 미탐(위험을 정상이라 함)
        else:  # 불명 = 오답
            if exp == "위험":
                un_pos += 1
            else:
                un_neg += 1
    unparsed = un_pos + un_neg
    n = tp + tn + fp + fn + unparsed   # 불명도 분모(오답)
    pos = tp + fn + un_pos             # 실제 위험 수
    neg = tn + fp + un_neg             # 실제 정상 수
    return {
        "tp": tp, "tn": tn, "fp": fp, "fn": fn, "unparsed": unparsed, "n": n,
        "accuracy": round((tp + tn) / n, 3) if n else None,   # 불명은 오답이라 정확도 깎임
        "false_alarm": round(fp / neg, 3) if neg else None,   # 오탐율(정상→위험)
        "miss": round((fn + un_pos) / pos, 3) if pos else None,  # 미탐율(위험 못 잡음: 정상판정+불명)
    }


def category_breakdown(records: List[Dict]) -> Dict[str, Dict]:
    """카테고리별 — 판정(위험/정상) 정답 + 유형(화재/낙상/전도/없음) 정답 카운트."""
    out: Dict[str, Dict] = {}
    for r in records:
        if r.get("error"):
            continue
        cat = r.get("category")
        if not cat:
            continue
        d = out.setdefault(cat, {"total": 0, "pred_danger": 0, "correct": 0, "type_correct": 0, "unparsed": 0})
        d["total"] += 1
        if r.get("pred_type") == r.get("danger"):   # 유형 일치(판정과 별개로 채점)
            d["type_correct"] += 1
        pred = r.get("pred")
        if pred not in ("위험", "정상"):
            d["unparsed"] += 1
            continue
        if pred == "위험":
            d["pred_danger"] += 1
        if pred == r.get("expected"):
            d["correct"] += 1
    return out


def type_accuracy(records: List[Dict], danger_only: bool = False) -> Optional[float]:
    """유형 정확도 = pred_type == danger(정답 유형). danger_only 면 위험 카테고리(화재/낙상/전도)만."""
    ok = tot = 0
    for r in records:
        if r.get("error") or not r.get("danger"):
            continue
        if danger_only and r["danger"] == "없음":
            continue
        tot += 1
        if r.get("pred_type") == r.get("danger"):
            ok += 1
    return round(ok / tot, 3) if tot else None


# ── 리포트 헬퍼 ──────────────────────────────────────────────────
def trunc(s: str, n: int) -> str:
    s = (s or "").replace("\n", " ").replace("|", "/").strip()
    return s[:n] + ("…" if len(s) > n else "")


def pct(x) -> str:
    return "-" if x is None else f"{x*100:.0f}%"


def mark(r: Dict) -> str:
    if r.get("error"):
        return "⚠️"
    if not r.get("expected"):
        return "?"
    if r.get("pred") not in ("위험", "정상"):   # 불명/미파싱 — 혼동행렬에서도 제외됨
        return "∅"
    return "✅" if r["pred"] == r["expected"] else "❌"


# 리포트(.md)가 놓이는 디렉토리 — 캡처 이미지 상대경로의 기준. 서브디렉토리(prompt_test/pixel_frame_test)
# 출력 시 main()/rebuild 에서 실제 출력 폴더로 교체한다.
REPORT_DIR = C.RESULTS_DIR


def rel_for_md(path: Path) -> str:
    import os
    try:
        return os.path.relpath(path, start=REPORT_DIR).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def model_stats_for(model_infos: List[Dict], recs: List[Dict], loaded_info: Dict[str, Dict]) -> List[Dict]:
    """주어진 records(미디어 subset)에 대한 모델별 통계 리스트.
    loaded_info[hf_id] = {loaded, load_sec, peak_mb, error}."""
    out: List[Dict] = []
    for info in model_infos:
        hf = info["hf_id"]
        li = loaded_info.get(hf, {})
        mr = [r for r in recs if r["hf_id"] == hf]
        if not li.get("loaded"):
            out.append({"name": info["name"], "hf_id": hf, "loaded": False, "error": li.get("error")})
            continue
        ok = [r for r in mr if not r.get("error")]
        times = [r["time_sec"] for r in ok]
        tps = [r["tok_per_sec"] for r in ok]
        det = [r.get("detail", 0) for r in ok]
        ch = [r.get("chars", 0) for r in ok]
        out.append({
            "name": info["name"], "hf_id": hf, "loaded": True,
            "load_sec": li.get("load_sec"), "peak_mb": li.get("peak_mb"),
            "avg_time": round(sum(times) / len(times), 3) if times else 0.0,
            "avg_tps": round(sum(tps) / len(tps), 1) if tps else 0.0,
            "avg_detail": round(sum(det) / len(det), 2) if det else 0.0,
            "avg_chars": round(sum(ch) / len(ch)) if ch else 0,
            "cm_image": confusion([r for r in mr if r["media"] == "image"]),
            "cm_video": confusion([r for r in mr if r["media"] == "video"]),
            "cm_all": confusion(mr),
            "cb": category_breakdown(mr),
            "type_acc": type_accuracy(mr),               # 유형 전체 정확도
            "type_acc_danger": type_accuracy(mr, danger_only=True),  # 위험유형(화재/낙상/전도)만
        })
    return out


def _capture_html(text: str) -> str:
    """캡처 해석 본문 → 판정/유형/설명 라벨을 칩으로 강조 + 위험(빨강)/정상(초록) 색상 HTML."""
    import html as _h
    lines = (text or "(빈 출력)").splitlines() or ["(빈 출력)"]
    out = []
    for line in lines:
        m = re.match(r"\s*(판정|유형|설명|VERDICT|TYPE|DESC)\s*[:：]\s*(.*)$", line)
        if m:
            label, val = m.group(1), _h.escape(m.group(2))
            if label in ("판정", "VERDICT"):
                val = re.sub(r"(위험|danger|이상)", r'<span class="v-danger">\1</span>', val, flags=re.I)
                val = re.sub(r"(정상|normal|안전)", r'<span class="v-safe">\1</span>', val, flags=re.I)
            out.append(f'<span class="cap-label">{_h.escape(label)}</span> {val}')
        else:
            out.append(_h.escape(line))
    return "<br>".join(out)


# ── 마크다운 리포트 ──────────────────────────────────────────────
def build_report(records: List[Dict], items: List[Dict], model_stats: List[Dict],
                 env: Dict, args) -> str:
    md: List[str] = []
    has_img = any(it["media"] == "image" for it in items)
    has_vid = any(it["media"] == "video" for it in items)
    media_cols = [m for m, on in (("image", has_img), ("video", has_vid)) if on]
    col_name = {"image": "이미지", "video": "영상"}

    _tag = getattr(args, "tag", None)
    md.append("# 엣지 VLM 해석 평가" + (f" ({_tag})" if _tag else "") + "\n")

    # 데이터셋 구성 — 평가된 미디어 열만 표시(이미지 리포트=이미지열, 영상 리포트=영상열)
    md.append("## 데이터셋 구성 (위험 3종 + 정상)\n")
    md.append("| 카테고리 | 정답 | 위험유형 |" + "".join(f" {col_name[m]} |" for m in media_cols))
    md.append("|---|---|---|" + "".join("---|" for _ in media_cols))
    for cat, meta in C.CATEGORIES.items():
        cells = "".join(
            f" {sum(1 for it in items if it['category'] == cat and it['media'] == m)} |"
            for m in media_cols
        )
        md.append(f"| {meta['desc']} (`{cat}`) | {meta['label']} | {meta['danger']} |" + cells)
    md.append("")

    # 모델 종합 비교 (헤드라인 — 해석 상세도가 1차)
    md.append("## 모델 종합 비교\n")
    md.append("| 모델 | 로드 | 상황인식 정확도 | 유형 정확도 | 과잉해석(오탐) | 평균 지연 | tok/s | peak VRAM |")
    md.append("|---|---|---|---|---|---|---|---|")
    for st in model_stats:
        if not st["loaded"]:
            md.append(f"| {st['name']} | ❌ | - | - | - | - | - | - |")
            continue
        cm = st["cm_all"]
        md.append(f"| {st['name']} | ✅ {st['load_sec']}s | "
                  f"{pct(cm['accuracy'])} | {pct(st.get('type_acc'))} | {pct(cm['false_alarm'])} | {st['avg_time']:.2f}s | "
                  f"{st['avg_tps']} | {st['peak_mb']} MB |")
    md.append("")

    # 모델별 상세
    for st in model_stats:
        md.append(f"## {st['name']} — `{st['hf_id']}`\n")
        if not st["loaded"]:
            md.append(f"❌ **로드 실패** — {trunc(st.get('error', ''), 200)}\n")
            continue
        # 위험 유형별 인식 (화재/낙상/전도 탐지율 + 정상 카테고리 정확분류)
        md.append("**위험 유형별 인식 (카테고리별 정답률)**\n")
        md.append("| 카테고리 | 정답유형 | N | 위험판정 | 판정정답률 | 유형정답률 | 미상 |")
        md.append("|---|---|---|---|---|---|---|")
        cb = st.get("cb", {})
        for cat, meta in C.CATEGORIES.items():
            d = cb.get(cat)
            if not d or d["total"] == 0:
                continue
            rate = f"{d['correct'] / d['total'] * 100:.0f}%" if d['total'] else "-"
            trate = f"{d.get('type_correct', 0) / d['total'] * 100:.0f}%" if d['total'] else "-"
            md.append(f"| {meta['desc']} | {meta['danger']} | {d['total']} | {d['pred_danger']} | {rate} | {trate} | {d['unparsed']} |")
        md.append("")
        # 항목별 결과표 (예측유형·시간)
        recs = [r for r in records if r["hf_id"] == st["hf_id"]]
        md.append("**항목별 결과**\n")
        md.append("| 유형 | 정답 | 판정 | 정오 | 시간 | 해석(앞부분) |")
        md.append("|---|---|---|---|---|---|")
        for r in recs:
            if r.get("error"):
                md.append(f"| - | {r.get('expected','?')} | - | ⚠️ | - | (에러: {trunc(r['error'],40)}) |")
            else:
                md.append(f"| {r.get('pred_type','-')} | {r.get('expected','?')} | {r['pred']} | "
                          f"{mark(r)} | {r['time_sec']:.1f}s | {trunc(r['reason'],55)} |")
        md.append("")

    # 이미지 vs 영상 (동일 클립) — 영상이 판정을 바꾸는가? (이미지·영상이 모두 있을 때만 표시)
    if any(r.get("media") == "image" for r in records) and any(r.get("media") == "video" for r in records):
        md.append("## 이미지 vs 영상 (동일 클립 판정 변화)\n")
        md.append("동일 영상의 '중간프레임 1장' vs '영상 8프레임' 판정 비교. 영상 정보가 단일프레임 오판을 교정/악화하는지 확인.\n")
        for st in model_stats:
            if not st["loaded"]:
                continue
            by_stem = {}
            for r in records:
                if r["hf_id"] != st["hf_id"] or r.get("error"):
                    continue
                by_stem.setdefault(r["stem"], {})[r["media"]] = r
            flips = [(s, d) for s, d in by_stem.items() if "image" in d and "video" in d and d["image"]["pred"] != d["video"]["pred"]]
            md.append(f"### {st['name']}\n")
            if not flips:
                md.append("- 판정이 바뀐 클립 없음 (이미지=영상 판정 일치)\n")
                continue
            md.append(f"- 판정이 달라진 클립 {len(flips)}개:\n")
            md.append("| 클립 | 정답 | 이미지 판정 | 영상 판정 | 영상 효과 |")
            md.append("|---|---|---|---|---|")
            for s, d in flips:
                exp = d["image"].get("expected")
                ip, vp = d["image"]["pred"], d["video"]["pred"]
                effect = "교정✅" if (exp and vp == exp and ip != exp) else ("악화❌" if (exp and ip == exp and vp != exp) else "변화")
                md.append(f"| `{trunc(s,28)}` | {exp} | {ip} | {vp} | {effect} |")
            md.append("")

    # 캡처별 전체 해석 — 본 평가의 핵심
    import html as _html
    md.append("## 상세 내역 \n")
    for st in model_stats:
        if not st["loaded"]:
            continue
        md.append(f"### {st['name']}\n")
        for r in [r for r in records if r["hf_id"] == st["hf_id"]]:
            meta = (f"[{r['media']}] {r['name']} · 정답 {r.get('expected','?')} · "
                    f"판정 {r.get('pred','-')}({r.get('pred_type','-')}) {mark(r)}")
            body = (r.get("error") and f"(에러) {r['error']}") or r.get("text", "") or "(빈 출력)"
            img_html = (f'<img src="{rel_for_md(r["preview_path"])}">'
                        if r.get("preview_path") else '<div class="noimg">(이미지 없음)</div>')
            # 한 줄 HTML 카드(이미지 좌 + 해석 우). 줄바꿈은 <br> 로(HTML 블록 1줄 유지)
            md.append(
                '<div class="capture">'
                f'<div class="cap-img">{img_html}</div>'
                '<div class="cap-body">'
                f'<div class="cap-head">{_html.escape(meta)}</div>'
                f'<div class="cap-text">{_capture_html(body)}</div>'
                '</div></div>'
            )
        md.append("")
    return "\n".join(md)


# ── 메인 ────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="엣지 캡처 이미지 VLM 해석 평가 → md")
    ap.add_argument("--models", default="", help="hf_id/name 부분문자열 콤마목록 (기본 전체)")
    ap.add_argument("--media", default="image,video", help="image,video 중 선택")
    ap.add_argument("--limit", type=int, default=0, help="미디어별 최대 N개(빠른 점검용)")
    ap.add_argument("--max-new-tokens", type=int, default=C.MAX_NEW_TOKENS)
    ap.add_argument("--temperature", type=float, default=C.TEMPERATURE)
    # 입력 해상도/프레임 스윕 — 기본은 config 값. 지정 시 config 를 런타임 오버라이드.
    ap.add_argument("--video-num-frames", type=int, default=C.VIDEO_NUM_FRAMES)
    ap.add_argument("--video-frame-max-side", type=int, default=C.VIDEO_FRAME_MAX_SIDE)
    ap.add_argument("--image-max-pixels", type=int, default=C.IMAGE_MAX_PIXELS)
    ap.add_argument("--image-min-pixels", type=int, default=C.IMAGE_MIN_PIXELS)
    # 결과 분리: results/<out-subdir>/ 에 저장 + 파일명에 <tag> 삽입
    ap.add_argument("--out-subdir", default="", help="results 하위 출력 폴더(예: prompt_test, pixel_frame_test)")
    ap.add_argument("--tag", default="", help="파일명/리포트 제목에 넣을 태그(예: f8_s448)")
    args = ap.parse_args()

    # config 런타임 오버라이드 — load_vlm(이미지 픽셀)·infer_video(프레임) 가 호출 시점에 C.* 를 읽음
    C.VIDEO_NUM_FRAMES = args.video_num_frames
    C.VIDEO_FRAME_MAX_SIDE = args.video_frame_max_side
    C.IMAGE_MAX_PIXELS = args.image_max_pixels
    C.IMAGE_MIN_PIXELS = args.image_min_pixels

    if not torch.cuda.is_available():
        print("[중단] VLM 은 GPU 전용입니다 (CUDA 필요).")
        sys.exit(1)

    media_filter = {m.strip() for m in args.media.split(",") if m.strip()}
    items = build_dataset(media_filter, args.limit or None)
    if not items:
        print(f"[중단] 데이터셋이 비어있습니다. 파일을 넣으세요 → {C.IMAGE_DIR} · {C.VIDEO_DIR}")
        sys.exit(1)

    models = C.VLM_MODELS
    if args.models.strip():
        keys = [k.strip().lower() for k in args.models.split(",") if k.strip()]
        models = [m for m in C.VLM_MODELS if any(k in m["hf_id"].lower() or k in m["name"].lower() for k in keys)]
        if not models:
            print(f"[중단] --models 일치 모델 없음: {args.models}")
            sys.exit(1)

    # 단일 프롬프트 (config.PROMPT — P5 채택)
    prompt = getattr(C, "PROMPT", None)
    if prompt is None:
        print("[중단] config 에 PROMPT 가 없습니다.")
        sys.exit(1)
    print("프롬프트: config.PROMPT (단일)")

    # 출력 디렉토리(results 또는 그 하위) + 리포트 이미지 상대경로 기준 설정
    out_dir = C.RESULTS_DIR / args.out_subdir if args.out_subdir else C.RESULTS_DIR
    global REPORT_DIR
    REPORT_DIR = out_dir

    free, total = torch.cuda.mem_get_info()
    env = {
        "gpu_name": torch.cuda.get_device_name(0),
        "gpu_total_mb": round(total / 1024 / 1024),
        "torch": torch.__version__,
        "transformers": __import__("transformers").__version__,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"데이터셋 {len(items)}건(이미지/영상) · 모델 {len(models)}개 · GPU {env['gpu_name']} · 출력 → {out_dir}")

    records: List[Dict] = []
    loaded_info: Dict[str, Dict] = {}   # hf_id → {loaded, load_sec, peak_mb, error}
    overall = time.time()

    for mi, info in enumerate(models, 1):
        hf_id, name = info["hf_id"], info["name"]
        print(f"\n{'#'*60}\n# [{mi}/{len(models)}] {name} ({hf_id})\n{'#'*60}")
        torch.cuda.reset_peak_memory_stats()
        st = {"name": name, "hf_id": hf_id, "loaded": False, "load_sec": None, "peak_mb": None}
        try:
            processor, model, load_sec = E.load_vlm(hf_id)
            st["loaded"], st["load_sec"] = True, load_sec
            print(f"  [로드 완료] {load_sec}s")
        except Exception as e:
            loaded_info[hf_id] = {"loaded": False, "error": str(e)}
            print(f"  [로드 실패] {e}")
            traceback.print_exc()
            continue

        m_recs: List[Dict] = []
        times, tps, details, chars = [], [], [], []
        for ii, it in enumerate(items, 1):
            rec = {"hf_id": hf_id, "model_name": name, "media": it["media"],
                   "name": it["name"], "stem": it["stem"], "category": it["category"],
                   "expected": it["expected"], "danger": it["danger"],
                   "preview_path": it["path"] if it["media"] == "image" else E.video_thumbnail(it["path"])}
            try:
                if it["media"] == "image":
                    out = E.infer_image(processor, model, it["path"], prompt, args.max_new_tokens, args.temperature)
                else:
                    out = E.infer_video(processor, model, it["path"], prompt, args.max_new_tokens, args.temperature)
                rec.update(out)
                rec["pred"] = parse_verdict(out["text"])
                rec["pred_type"] = parse_danger_type(out["text"])
                rec["reason"] = description_of(out["text"])
                rec["chars"] = len(out["text"] or "")
                rec["detail"] = detail_score(out["text"], rec["pred"], rec["pred_type"])
                times.append(out["time_sec"])
                tps.append(out["tok_per_sec"])
                details.append(rec["detail"])
                chars.append(rec["chars"])
                ok = mark(rec)
                print(f"  [{ii}/{len(items)}] {it['media']:5s} {it['name'][:28]:28s} "
                      f"{it['expected']}/{rec['pred']}({rec['pred_type']}) {ok} "
                      f"상세{rec['detail']}/5 {rec['chars']}자 {out['time_sec']:.1f}s")
            except Exception as e:
                rec["error"] = str(e)
                print(f"  [{ii}/{len(items)}] {it['name']} 실패: {str(e)[:120]}")
                traceback.print_exc()
            records.append(rec)
            m_recs.append(rec)

        peak = round(torch.cuda.max_memory_allocated() / 1024 / 1024)
        loaded_info[hf_id] = {"loaded": True, "load_sec": st["load_sec"], "peak_mb": peak}
        cm = confusion(m_recs)
        print(f"  → 상세도 {round(sum(details)/len(details),2) if details else 0}/5 · "
              f"평균 {round(sum(chars)/len(chars)) if chars else 0}자 · 상황인식 {pct(cm['accuracy'])} · "
              f"유형 {pct(type_accuracy(m_recs))} · "
              f"오탐 {pct(cm['false_alarm'])} · 미상 {cm.get('unparsed', 0)} · "
              f"{round(sum(tps)/len(tps),1) if tps else 0} tok/s · peak {peak}MB")

        # 다음 모델 로드 전 VRAM 해제
        model = None
        processor = None
        E.free_vram()

    # 저장 — 평가된 미디어별로 리포트·원자료 분리 (이미지용 / 영상용)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    tagpart = f"_{args.tag}" if args.tag else ""
    written = []
    for media in ("image", "video"):
        m_recs = [r for r in records if r["media"] == media]
        if not m_recs:
            continue
        m_items = [it for it in items if it["media"] == media]
        m_stats = model_stats_for(models, m_recs, loaded_info)
        report = build_report(m_recs, m_items, m_stats, env, args)
        rp = out_dir / f"vlm_benchmark_{media}{tagpart}_{ts}.md"
        rp.write_text(report, encoding="utf-8")
        raw = {
            "generated_at": ts, "media": media, "env": env,
            "args": {"media": [media], "limit": args.limit, "tag": args.tag,
                     "max_new_tokens": args.max_new_tokens, "temperature": args.temperature,
                     "video_num_frames": args.video_num_frames,
                     "video_frame_max_side": args.video_frame_max_side,
                     "image_max_pixels": args.image_max_pixels,
                     "image_min_pixels": args.image_min_pixels},
            "prompt_text": prompt,
            "model_stats": m_stats,
            "records": [{k: (str(v) if isinstance(v, Path) else v) for k, v in r.items()} for r in m_recs],
        }
        jp = out_dir / f"vlm_benchmark_{media}{tagpart}_{ts}.json"
        jp.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
        written.append((media, rp))

    print(f"\n{'='*60}")
    print(f"완료: {len(records)}건 / {time.time()-overall:.1f}초")
    for media, rp in written:
        print(f"[{media}] 리포트 → {rp}")
    print(r"PDF 생성: venv\Scripts\python.exe tools\report_to_pdf.py")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
