"""
파라미터 스윕 심층 분석 — pixel_frame_test/ 의 결과 json 을 읽어 '카테고리 × 조합' 의
판정/유형 정답률 표를 만든다. 집계(SWEEP_SUMMARY)만으로 안 보이는 카테고리별 영향
(특히 영상의 낙상/전도가 프레임 수에 따라 어떻게 변하는지)을 드러낸다.

사용: venv\\Scripts\\python.exe tools\\analyze_sweep.py   (결과를 stdout + pixel_frame_test/SWEEP_DETAIL.md)
"""
from __future__ import annotations

import glob
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

import config as C          # noqa: E402
import run_benchmark as R   # noqa: E402

SWEEP_DIR = C.RESULTS_DIR / "pixel_frame_test"
# 카테고리 표시 순서/라벨(정답유형 병기)
CAT_ORDER = [
    ("fire", "화재"), ("smoke", "연기"), ("person_fall", "낙상"),
    ("machine_tipover", "전도"), ("normal_parking", "정상주차"), ("normal_worker", "정상작업"),
]


def load_runs(media: str):
    """media('video'|'image') 의 조합별 records → {tag: records}."""
    runs = {}
    for jp in sorted(glob.glob(str(SWEEP_DIR / f"vlm_benchmark_{media}_*.json"))):
        d = json.loads(Path(jp).read_text(encoding="utf-8"))
        m = re.search(rf"vlm_benchmark_{media}_(.+)_\d{{8}}_\d{{6}}", Path(jp).name)
        tag = m.group(1) if m else Path(jp).stem
        runs[tag] = d["records"]
    return runs


def cat_type_rate(records, cat):
    """카테고리 cat 의 유형 정답률(pred_type==danger)·판정 정답률·N."""
    rs = [r for r in records if r.get("category") == cat and not r.get("error")]
    n = len(rs)
    if not n:
        return None
    tcorrect = sum(1 for r in rs if r.get("pred_type") == r.get("danger"))
    vcorrect = sum(1 for r in rs if r.get("pred") == r.get("expected"))
    return {"n": n, "type": tcorrect / n, "verdict": vcorrect / n}


def pct(x):
    return "-" if x is None else f"{x*100:.0f}%"


def build_table(media: str, tag_order: list[str], metric: str) -> list[str]:
    runs = load_runs(media)
    tags = [t for t in tag_order if t in runs] or sorted(runs)
    out = [f"| 카테고리(정답유형) | " + " | ".join(f"`{t}`" for t in tags) + " |",
           "|---|" + "---|" * len(tags)]
    for cat, label in CAT_ORDER:
        cells = []
        any_n = False
        for t in tags:
            d = cat_type_rate(runs[t], cat)
            if d is None:
                cells.append("-")
            else:
                any_n = True
                cells.append(pct(d[metric]))
        if any_n:
            n = next((cat_type_rate(runs[t], cat)["n"] for t in tags if cat_type_rate(runs[t], cat)), 0)
            out.append(f"| {label} ({cat}, N={n}) | " + " | ".join(cells) + " |")
    return out


def main():
    md = ["# 파라미터 스윕 심층 분석 — 카테고리 × 조합\n",
          "집계표(SWEEP_SUMMARY)가 가린 카테고리별 영향. 셀 = 해당 카테고리 정답률.\n"]

    v_order = ["v_f4", "v_base", "v_s560", "v_s640", "v_f16", "v_f16s560"]  # 프레임/해상도 오름차순
    md.append("## 영상 — 유형 정답률 (프레임/해상도 ↑ 순)\n")
    md += build_table("video", v_order, "type")
    md.append("\n## 영상 — 판정 정답률\n")
    md += build_table("video", v_order, "verdict")

    i_order = ["i_768", "i_base", "i_1600", "i_2048", "i_min128"]
    md.append("\n## 이미지 — 유형 정답률\n")
    md += build_table("image", i_order, "type")
    md.append("\n## 이미지 — 판정 정답률\n")
    md += build_table("image", i_order, "verdict")

    text = "\n".join(md)
    print(text)
    sp = SWEEP_DIR / "SWEEP_DETAIL.md"
    sp.write_text(text, encoding="utf-8")
    print(f"\n저장 → {sp}")


if __name__ == "__main__":
    main()
