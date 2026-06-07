"""
캐시된 결과 JSON(vlm_benchmark_*.json)으로 마크다운 리포트를 재생성 — GPU 추론 없이.
파서/상세도/리포트 레이아웃을 바꾼 뒤 모델 재실행 없이 md 만 다시 뽑을 때 사용.
평가된 미디어별(이미지/영상)로 vlm_benchmark_<media>_<ts>.md 를 분리 생성한다.

사용: venv\\Scripts\\python.exe tools\\rebuild_report.py [json경로]  (생략 시 모든 json 재생성)
"""

from __future__ import annotations

import argparse
import glob
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  #  를 import 경로에

import config as C          # noqa: E402
import run_benchmark as R   # noqa: E402
import vlm_engine as E      # noqa: E402


def rebuild_one(jpath: Path) -> None:
    d = json.loads(jpath.read_text(encoding="utf-8"))
    env = d["env"]
    ts_m = re.search(r"(\d{8}_\d{6})", jpath.name)
    ts = ts_m.group(1) if ts_m else "rebuilt"

    # records 재구성 + 최신 파서/상세도로 재산정
    recs = []
    for r in d["records"]:
        r = dict(r)
        txt = r.get("text") or ""
        r["preview_path"] = Path(r["preview_path"]) if r.get("preview_path") else None
        # 영상인데 썸네일 없으면 원본 영상에서 대표(중간) 프레임 생성
        if r.get("media") == "video" and not r.get("preview_path"):
            vp = C.VIDEO_DIR / r["name"]
            if vp.exists():
                r["preview_path"] = E.video_thumbnail(vp)
        if not r.get("error"):
            r["pred"] = R.parse_verdict(txt)
            r["pred_type"] = R.parse_danger_type(txt)
            r["reason"] = R.description_of(txt)
            r["chars"] = len(txt)
            r["detail"] = R.detail_score(txt, r["pred"], r["pred_type"])
        recs.append(r)

    loaded_info = {m["hf_id"]: {"loaded": m.get("loaded"), "load_sec": m.get("load_sec"),
                                "peak_mb": m.get("peak_mb"), "error": m.get("error")}
                   for m in d.get("model_stats", [])}
    model_infos = [{"name": m["name"], "hf_id": m["hf_id"]} for m in d.get("model_stats", [])]
    a = d.get("args") or {}
    # 구버전 json 은 prompt(번호)만 있음 → 제목 라벨용 태그로 환산(P1..P5)
    tag = a.get("tag") or (f"P{a['prompt']}" if a.get("prompt") else None)
    args = argparse.Namespace(
        temperature=a.get("temperature", 0.0),
        tag=tag,
        video_num_frames=a.get("video_num_frames"),
        video_frame_max_side=a.get("video_frame_max_side"),
        image_max_pixels=a.get("image_max_pixels"),
        image_min_pixels=a.get("image_min_pixels"),
    )
    R.REPORT_DIR = jpath.parent   # 캡처 이미지 상대경로 기준 = json/md 가 놓인 폴더

    # items 재구성(고유 미디어 파일) — dataset 디렉토리 스캔 아님
    seen, items = set(), []
    for r in recs:
        key = (r["media"], r["name"])
        if key in seen:
            continue
        seen.add(key)
        items.append({
            "path": r.get("preview_path") or (C.IMAGE_DIR / r["name"] if r["media"] == "image" else C.VIDEO_DIR / r["name"]),
            "name": r["name"], "stem": r["stem"], "media": r["media"],
            "category": r["category"], "expected": r["expected"], "danger": r["danger"],
        })
    m_stats = R.model_stats_for(model_infos, recs, loaded_info)
    md = R.build_report(recs, items, m_stats, env, args)
    out = jpath.with_suffix(".md")   # json 과 같은 basename (프롬프트 태그 보존)
    out.write_text(md, encoding="utf-8")
    cm = m_stats[0].get("cm_all", {}) if m_stats else {}
    print(f"재생성 → {out.name}" + (f"  (정확도 {cm.get('accuracy')} · 오탐 {cm.get('false_alarm')})" if cm else ""))


def main():
    if len(sys.argv) > 1:
        targets = [Path(sys.argv[1])]
    else:   # results/ 와 그 하위(prompt_test, pixel_frame_test) 모두 재귀 탐색
        targets = [Path(p) for p in sorted(
            glob.glob(str(C.RESULTS_DIR / "**" / "vlm_benchmark_*.json"), recursive=True))]
    if not targets:
        print("[중단] 재생성할 JSON 이 없습니다.")
        sys.exit(1)
    for jp in targets:
        if jp.exists():
            rebuild_one(jp)


if __name__ == "__main__":
    main()
