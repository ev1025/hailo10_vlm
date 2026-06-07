"""
VLM 프롬프트·생성 파라미터 검증 실험 모음 — 한 번의 모델 로드로 개별/일괄 실행.
각 실험은 결과를 results/pixel_frame_test/<NAME>.md 로 저장한다. (배경·결과 해석: 프롬프트_튜닝_기록.md)

  term    전도 유형어 A/B (전도→낙상 오인 → '낙상(사람)/낙상(기계)' 분기로 해결)   → TERM_TEST.md
  smoke   연기 회귀 보정 ('연기→화재 우선' 규칙)                                → SMOKE_FIX.md
  repeat  반복 억제 파라미터(repetition_penalty / no_repeat_ngram_size) 튜닝   → REPEAT_TEST.md
  korean  한자 차단(FORCE_KOREAN) on/off 인과 검증                            → FORCE_KOREAN_TEST.md

사용:
  venv\\Scripts\\python.exe -u vlm\\tools\\experiments.py term [--limit N]
  venv\\Scripts\\python.exe -u vlm\\tools\\experiments.py all              # 4개 전부(모델 1회 로드 공유)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

import torch  # noqa: E402

import config as C          # noqa: E402
import run_benchmark as R   # noqa: E402
import vlm_engine as E      # noqa: E402

OUT_DIR = C.RESULTS_DIR / "pixel_frame_test"


# ── 공통 헬퍼 ────────────────────────────────────────────────────
def infer(processor, model, it, prompt: str):
    fn = E.infer_image if it["media"] == "image" else E.infer_video
    return fn(processor, model, it["path"], prompt, C.MAX_NEW_TOKENS, 0.0)


def pick(*, cats=None, stems=None, limit=None):
    """build_dataset 를 카테고리(cats) 또는 stem(stems) 으로 필터."""
    items = R.build_dataset({"image", "video"}, limit)
    if cats is not None:
        items = [it for it in items if it["category"] in cats]
    if stems is not None:
        items = [it for it in items if it["stem"] in stems]
    return items


def save(name: str, md_lines):
    text = "\n".join(md_lines)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    sp = OUT_DIR / name
    sp.write_text(text, encoding="utf-8")
    print(text)
    print(f"\n저장 → {sp}")


# ── 1) term: 전도 유형어 A/B ─────────────────────────────────────
#   nak_subj = '전도'(동음이의 많음)를 버리고, 모델이 즐겨 쓰는 '낙상'을 주체로만 구분(사람/기계).
#             채점기가 '낙상(기계)'의 '기계' 키워드를 전도로 매핑하므로 그대로 집계됨.
_TERM_BASE_INSTR, _TERM_BASE_FMT = "화재·낙상·전도·없음", "화재 / 낙상 / 전도 / 없음"
_TERM_CATS = ["machine_tipover", "person_fall"]
_TERM_VARIANTS = [
    ("base",      "화재·낙상·전도·없음",            "화재 / 낙상 / 전도 / 없음"),
    ("jeonbok",   "화재·낙상·전복·없음",            "화재 / 낙상 / 전복 / 없음"),
    ("disamb",    "화재·낙상·전도·없음",            "화재 / 낙상(사람이 넘어짐) / 전도(기계·차량이 넘어짐) / 없음"),
    ("disamb_jb", "화재·낙상·전복·없음",            "화재 / 낙상(사람이 넘어짐) / 전복(기계·차량이 넘어짐) / 없음"),
    ("nak_subj",  "화재·낙상(사람)·낙상(기계)·없음", "화재 / 낙상(사람) / 낙상(기계) / 없음"),
]


def exp_term(processor, model, limit=None):
    items = pick(cats=_TERM_CATS, limit=limit)
    print(f"[term] 대상 {len(items)}건: "
          + ", ".join(f"{c}={sum(1 for it in items if it['category']==c)}" for c in _TERM_CATS))
    res = {}
    for vname, instr, fmt in _TERM_VARIANTS:
        prompt = C.PROMPT.replace(_TERM_BASE_INSTR, instr).replace(_TERM_BASE_FMT, fmt)
        print(f"=== 변형 '{vname}' : {fmt} ===")
        res[vname] = {c: {"ok": 0, "n": 0} for c in _TERM_CATS}
        for it in items:
            pt = R.parse_danger_type(infer(processor, model, it, prompt)["text"])
            ok = (pt == it["danger"])
            d = res[vname][it["category"]]; d["n"] += 1; d["ok"] += int(ok)
            print(f"  [{it['media'][:3]}] {it['name'][:26]:26s} 정답 {it['danger']} → 유형 {pt} {'✅' if ok else '❌'}")
        print()
    md = ["# '전도' 유형어 A/B 테스트\n",
          "유형 '단어'만 치환(나머지 프롬프트 동일). 셀 = 유형 정답률(pred_type==정답유형). 채점기는 전복→전도로 매핑.\n",
          "| 변형 | 유형줄 | 전도(machine_tipover) | 낙상(person_fall) |",
          "|---|---|---|---|"]
    for vname, _i, fmt in _TERM_VARIANTS:
        cells = [f"{res[vname][c]['ok']}/{res[vname][c]['n']} ({res[vname][c]['ok']/res[vname][c]['n']*100:.0f}%)"
                 if res[vname][c]["n"] else "-" for c in _TERM_CATS]
        md.append(f"| `{vname}` | {fmt} | {cells[0]} | {cells[1]} |")
    save("TERM_TEST.md", md)


# ── 2) smoke: 연기 회귀 보정 ─────────────────────────────────────
_SMOKE_CATS = ["fire", "smoke", "person_fall", "machine_tipover"]
_FIRE_RULE = "\n특히, 연기·불꽃·화염이 보이면 사람이 함께 있어도 유형은 반드시 '화재'로 정하세요."
_FALL_RULE = "\n사람이 서 있거나 걷거나 작업 중이면 '낙상(사람)'이 아닙니다(낙상은 사람이 바닥에 쓰러진 경우만)."
_SMOKE_VARIANTS = {"naksubj": "", "fire_pri": _FIRE_RULE, "fire_pri_fallcond": _FIRE_RULE + _FALL_RULE}


def exp_smoke(processor, model, limit=None):
    items = pick(cats=_SMOKE_CATS, limit=limit)
    print("[smoke] 대상 " + ", ".join(f"{c}={sum(1 for it in items if it['category']==c)}" for c in _SMOKE_CATS)
          + f" (총 {len(items)})")
    res = {v: {c: {"ok": 0, "n": 0} for c in _SMOKE_CATS} for v in _SMOKE_VARIANTS}
    for vname, extra in _SMOKE_VARIANTS.items():
        prompt = C.PROMPT + extra
        print(f"=== {vname} ===")
        for it in items:
            try:
                pt = R.parse_danger_type(infer(processor, model, it, prompt)["text"])
            except Exception as e:
                print(f"  [ERR] {it['name']}: {str(e)[:120]}", flush=True); continue
            ok = (pt == it["danger"])
            d = res[vname][it["category"]]; d["n"] += 1; d["ok"] += int(ok)
            if it["category"] == "smoke":   # 부작용 카테고리는 개별 출력
                print(f"  [{it['media'][:3]}] {it['name'][:24]:24s} 정답 {it['danger']} → {pt} {'✅' if ok else '❌'}", flush=True)
        print("  → " + " · ".join(f"{c[:4]} {res[vname][c]['ok']}/{res[vname][c]['n']}" for c in _SMOKE_CATS) + "\n")

    def rate(v, c):
        d = res[v][c]; return f"{d['ok']}/{d['n']}={d['ok']/d['n']*100:.0f}%" if d["n"] else "-"
    md = ["# 연기 오인 보정 실험 (유형 정답률)\n",
          "현행(naksubj=낙상(사람)/낙상(기계)) 대비 규칙 추가 효과. 셀=유형 정답률.\n",
          "| 변형 | 화재 | 연기 | 낙상(사람) | 전도(기계) |",
          "|---|---|---|---|---|"]
    for v in _SMOKE_VARIANTS:
        md.append(f"| `{v}` | " + " | ".join(rate(v, c) for c in _SMOKE_CATS) + " |")
    save("SMOKE_FIX.md", md)


# ── 3) repeat: 반복 억제 파라미터 ───────────────────────────────
#   _generate 가 호출 시점에 C.REPETITION_PENALTY / C.NO_REPEAT_NGRAM_SIZE 를 읽으므로 C 값을 덮어써 비교.
_REP_LOOPY = {"fire7", "machine_tipover3"}
_REP_CONTROL = {"fire1", "person_fall1", "normal_parking1", "smoke1"}
_REP_SETTINGS = [("base(1.05/off)", 1.05, 0), ("1.15/3", 1.15, 3), ("1.3/3", 1.3, 3)]


def _rep_score(t: str) -> int:
    """가장 많이 반복된 10~40자 구의 등장 횟수(3회 연속 반복 기준). 1 이면 사실상 반복 없음."""
    best = 1
    for m in re.finditer(r'(.{10,40}?)\1\1', t or ''):
        best = max(best, len(re.findall(re.escape(m.group(1)), t)))
    return best


def exp_repeat(processor, model, limit=None):
    items = pick(stems=_REP_LOOPY | _REP_CONTROL)
    items.sort(key=lambda it: (it["stem"] not in _REP_LOOPY, it["stem"], it["media"]))   # loopy 먼저
    print("[repeat] 대상:", ", ".join(f"{it['stem']}({it['media'][:3]})" for it in items))
    saved = (C.REPETITION_PENALTY, C.NO_REPEAT_NGRAM_SIZE)   # 끝나고 복원(all 모드 오염 방지)
    res = {}
    try:
        for label, rp, nrns in _REP_SETTINGS:
            C.REPETITION_PENALTY, C.NO_REPEAT_NGRAM_SIZE = rp, nrns
            print(f"=== {label} (rep={rp}, ngram={nrns}) ===")
            for it in items:
                t = infer(processor, model, it, C.PROMPT)["text"]
                pred, pt, rs = R.parse_verdict(t), R.parse_danger_type(t), _rep_score(t)
                res.setdefault((it["stem"], it["media"]), {})[label] = (len(t), rs, pred, pt)
                print(f"  {it['stem'][:18]:18s}{it['media'][:3]} {len(t):4d}자 반복x{rs}{'🔁' if rs >= 2 else ''} {pred}/{pt}")
            print()
    finally:
        C.REPETITION_PENALTY, C.NO_REPEAT_NGRAM_SIZE = saved
    md = ["# 반복 억제 파라미터 실험\n",
          "loopy=반복 심한 항목, control=정상 대조군. 셀=글자수(반복횟수). 반복 1=없음.\n",
          "| 항목 | " + " | ".join(s[0] for s in _REP_SETTINGS) + " | 판정/유형(최종설정) |",
          "|---|" + "---|" * (len(_REP_SETTINGS) + 1)]
    for (stem, media), d in sorted(res.items(), key=lambda x: (x[0][0] not in _REP_LOOPY, x[0])):
        kind = "🔁loopy" if stem in _REP_LOOPY else "control"
        cells = " | ".join(f"{d[s[0]][0]}자(x{d[s[0]][1]})" for s in _REP_SETTINGS)
        last = d[_REP_SETTINGS[-1][0]]
        md.append(f"| {stem}({media[:3]}) {kind} | {cells} | {last[2]}/{last[3]} |")
    save("REPEAT_TEST.md", md)


# ── 4) korean: FORCE_KOREAN on/off ──────────────────────────────
_KOR_SAMPLE = {"smoke5", "smoke3", "smoke_fire2", "fire7", "fire1", "machine_tipover3",
               "machine_tipover1", "person_fall2", "person_fall5", "normal_worker3",
               "normal_parking4", "normal_parking1"}


def exp_korean(processor, model, limit=None):
    items = sorted(pick(stems=_KOR_SAMPLE), key=lambda it: (it["stem"], it["media"]))
    print(f"[korean] 대상 {len(items)}건:", ", ".join(f"{it['stem']}({it['media'][:3]})" for it in items))
    saved = C.FORCE_KOREAN
    res = {}
    try:
        for force_on in (False, True):                 # 끈 상태 먼저
            C.FORCE_KOREAN = force_on
            print(f"=== FORCE_KOREAN {'ON' if force_on else 'OFF'} ===")
            for it in items:
                hc = E._HAN_RE.findall(infer(processor, model, it, C.PROMPT)["text"] or "")
                res.setdefault((it["stem"], it["media"]), {})[force_on] = (len(hc), "".join(sorted(set(hc))))
                print(f"  {it['stem'][:18]:18s}{it['media'][:3]} "
                      + (f"❌한자 {len(hc)}({''.join(sorted(set(hc)))[:12]})" if hc else "✅한자0"))
            print()
    finally:
        C.FORCE_KOREAN = saved
    off_t = sum(v[False][0] for v in res.values()); on_t = sum(v[True][0] for v in res.values())
    off_n = sum(1 for v in res.values() if v[False][0] > 0); on_n = sum(1 for v in res.values() if v[True][0] > 0)
    md = ["# FORCE_KOREAN 인과 검증 (한자 차단 on/off)\n",
          f"대상 {len(res)}건. 셀=출력 내 한자 개수.\n",
          f"- **OFF**: {off_n}/{len(res)}건에서 한자 출현, 총 **{off_t}자**",
          f"- **ON**: {on_n}/{len(res)}건에서 한자 출현, 총 **{on_t}자**\n",
          "| 항목 | OFF 한자 | ON 한자 |",
          "|---|---|---|"]
    for (stem, media), v in sorted(res.items()):
        off_s = f"{v[False][0]} ({v[False][1][:14]})" if v[False][0] else "0"
        on_s = f"{v[True][0]} ({v[True][1][:14]})" if v[True][0] else "0"
        mark = " ⬅" if v[False][0] and not v[True][0] else ""
        md.append(f"| {stem}({media[:3]}) | {off_s} | {on_s}{mark} |")
    save("FORCE_KOREAN_TEST.md", md)


# ── 메인 ────────────────────────────────────────────────────────
EXPERIMENTS = {"term": exp_term, "smoke": exp_smoke, "repeat": exp_repeat, "korean": exp_korean}


def main():
    ap = argparse.ArgumentParser(description="VLM 프롬프트·생성 파라미터 검증 실험 모음")
    ap.add_argument("experiment", choices=list(EXPERIMENTS) + ["all"], help="실행할 실험")
    ap.add_argument("--limit", type=int, default=0, help="카테고리·미디어별 최대 N개 (term/smoke 에만 적용)")
    args = ap.parse_args()
    if not torch.cuda.is_available():
        print("[중단] GPU 필요"); sys.exit(1)

    names = list(EXPERIMENTS) if args.experiment == "all" else [args.experiment]
    processor, model, load_sec = E.load_vlm(C.VLM_MODELS[0]["hf_id"])
    print(f"[로드] {load_sec}s · 실험 {len(names)}개: {', '.join(names)}")
    for n in names:
        print(f"\n{'#'*60}\n# 실험: {n}\n{'#'*60}")
        EXPERIMENTS[n](processor, model, limit=args.limit or None)


if __name__ == "__main__":
    main()
