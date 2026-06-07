"""
입력 해상도/프레임 파라미터 스윕 — VIDEO_NUM_FRAMES / VIDEO_FRAME_MAX_SIDE /
IMAGE_MAX_PIXELS / IMAGE_MIN_PIXELS 를 바꿔가며 '판정 정확도'·'유형 정확도' 변화를 측정한다.

run_benchmark.py 를 조합별로 subprocess 실행(매 실행 새 프로세스 → VRAM 깨끗이 해제)하며,
결과는 모두 results/pixel_frame_test/ 에 <tag> 를 붙여 저장한다. 프롬프트는 단일(config.PROMPT) 고정.

축 분리 — 영상 파라미터(프레임 수/프레임 변)는 영상 결과에만, 이미지 픽셀 상한은 이미지 결과에만 영향.
  → 영상축 조합은 --media video 로, 이미지축 조합은 --media image 로만 돌려 시간 절약.

사용:
  venv\\Scripts\\python.exe vlm\\tools\\param_sweep.py --dry-run        # 실행 명령만 출력(검증)
  venv\\Scripts\\python.exe vlm\\tools\\param_sweep.py                  # 전체 스윕 실행
  venv\\Scripts\\python.exe vlm\\tools\\param_sweep.py --only f16,i1600 # 일부만
  venv\\Scripts\\python.exe vlm\\tools\\param_sweep.py --limit 6        # 미디어별 6개로 빠른 점검
  venv\\Scripts\\python.exe vlm\\tools\\param_sweep.py --summary-only   # 추론 없이 기존 결과 요약표만
실행 후: report_to_pdf.py 로 pixel_frame_test/ 의 md → pdf 변환(재귀 탐색).
"""

from __future__ import annotations

import argparse
import glob
import json
import re
import subprocess
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

VLM_DIR = Path(__file__).resolve().parent.parent
RUN_BENCHMARK = VLM_DIR / "run_benchmark.py"
OUT_SUBDIR = "pixel_frame_test"
RESULTS_DIR = VLM_DIR / "results"
SWEEP_DIR = RESULTS_DIR / OUT_SUBDIR

_PATCH = 28 * 28   # Qwen-VL 비주얼 토큰 1개 = 28×28 px. 픽셀 상한을 토큰 배수로 표기.

# 기준값(config.py 기본) — 조합표에서 'base' 로 표기, 한 축씩만 바꿔 비교(ablation).
BASE = {"frames": 8, "side": 448, "imax": 1280, "imin": 256}

# 스윕 조합 — media: 이 조합이 영향을 주는 축만 평가(video=프레임축, image=픽셀축).
#   imax/imin 은 28² 의 '배수'(토큰 수)로 적는다 → 실제 픽셀 = 배수 * 28 * 28.
SWEEP = [
    # ── 영상 축: 프레임 수 / 프레임 변(px) ── (낙상·전도 영상 약점 개선 가설 검증)
    {"tag": "v_base",  "media": "video", "frames": 8,  "side": 448, "imax": 1280, "imin": 256},
    {"tag": "v_f16",   "media": "video", "frames": 16, "side": 448, "imax": 1280, "imin": 256},
    {"tag": "v_f4",    "media": "video", "frames": 4,  "side": 448, "imax": 1280, "imin": 256},
    {"tag": "v_s560",  "media": "video", "frames": 8,  "side": 560, "imax": 1280, "imin": 256},
    {"tag": "v_s640",  "media": "video", "frames": 8,  "side": 640, "imax": 1280, "imin": 256},
    {"tag": "v_f16s560", "media": "video", "frames": 16, "side": 560, "imax": 1280, "imin": 256},
    # ── 이미지 축: 픽셀 상/하한 ──
    {"tag": "i_base",  "media": "image", "frames": 8,  "side": 448, "imax": 1280, "imin": 256},
    {"tag": "i_768",   "media": "image", "frames": 8,  "side": 448, "imax": 768,  "imin": 256},
    {"tag": "i_1600",  "media": "image", "frames": 8,  "side": 448, "imax": 1600, "imin": 256},
    {"tag": "i_2048",  "media": "image", "frames": 8,  "side": 448, "imax": 2048, "imin": 256},
    {"tag": "i_min128","media": "image", "frames": 8,  "side": 448, "imax": 1280, "imin": 128},
]


def build_cmd(cfg: dict, limit: int) -> list[str]:
    cmd = [
        sys.executable, str(RUN_BENCHMARK),
        "--media", cfg["media"],
        "--out-subdir", OUT_SUBDIR,
        "--tag", cfg["tag"],
        "--video-num-frames", str(cfg["frames"]),
        "--video-frame-max-side", str(cfg["side"]),
        "--image-max-pixels", str(cfg["imax"] * _PATCH),
        "--image-min-pixels", str(cfg["imin"] * _PATCH),
    ]
    if limit:
        cmd += ["--limit", str(limit)]
    return cmd


def _is_base(cfg: dict) -> bool:
    return (cfg["frames"], cfg["side"], cfg["imax"], cfg["imin"]) == \
           (BASE["frames"], BASE["side"], BASE["imax"], BASE["imin"])


def summarize() -> str:
    """pixel_frame_test/ 의 결과 json 을 모아 조합별 판정/유형 정확도 비교표(md) 생성."""
    rows = []
    for jp in sorted(glob.glob(str(SWEEP_DIR / "vlm_benchmark_*.json"))):
        d = json.loads(Path(jp).read_text(encoding="utf-8"))
        a = d.get("args", {})
        media = d.get("media", "?")
        st = (d.get("model_stats") or [{}])[0]
        cm = st.get("cm_all", {})
        # 파일명에서 태그 추출: vlm_benchmark_<media>_<tag>_<ts>
        m = re.search(rf"vlm_benchmark_{media}_(.+)_\d{{8}}_\d{{6}}", Path(jp).name)
        tag = m.group(1) if m else "?"
        imax_mult = (a.get("image_max_pixels") or 0) // _PATCH
        imin_mult = (a.get("image_min_pixels") or 0) // _PATCH
        rows.append({
            "tag": tag, "media": media,
            "frames": a.get("video_num_frames"), "side": a.get("video_frame_max_side"),
            "imax": imax_mult, "imin": imin_mult,
            "acc": cm.get("accuracy"), "type_acc": st.get("type_acc"),
            "fa": cm.get("false_alarm"), "vram": st.get("peak_mb"), "t": st.get("avg_time"),
        })

    def pct(x):
        return "-" if x is None else f"{x*100:.0f}%"

    out = ["# 입력 파라미터 스윕 요약 (판정 vs 유형 정확도)\n",
           "프롬프트 단일(config.PROMPT) 고정. 한 축씩만 변경(ablation). 기준=`base` 와 비교.\n"]

    for media, axis_cols, axis_hdr in (
        ("video", ("frames", "side"), "프레임 | 프레임변"),
        ("image", ("imax", "imin"), "imax(×28²) | imin(×28²)"),
    ):
        mr = [r for r in rows if r["media"] == media]
        if not mr:
            continue
        out.append(f"## {'영상' if media == 'video' else '이미지'} 축\n")
        out.append(f"| 조합 | {axis_hdr} | 판정 정확도 | 유형 정확도 | 오탐 | 평균 지연 | peak VRAM |")
        out.append("|---|---|---|---|---|---|---|")
        for r in sorted(mr, key=lambda x: x["tag"]):
            axis = " | ".join(str(r[c]) for c in axis_cols)
            t = f"{r['t']:.2f}s" if r["t"] is not None else "-"
            out.append(f"| `{r['tag']}` | {axis} | {pct(r['acc'])} | {pct(r['type_acc'])} | "
                       f"{pct(r['fa'])} | {t} | {r['vram']} MB |")
        out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="입력 픽셀/프레임 파라미터 스윕")
    ap.add_argument("--only", default="", help="실행할 태그 콤마목록(기본 전체)")
    ap.add_argument("--limit", type=int, default=0, help="미디어별 최대 N개(빠른 점검)")
    ap.add_argument("--dry-run", action="store_true", help="실행 명령만 출력(추론 안 함)")
    ap.add_argument("--summary-only", action="store_true", help="추론 없이 기존 결과 요약표만 생성")
    args = ap.parse_args()

    if not args.summary_only:
        only = {t.strip() for t in args.only.split(",") if t.strip()}
        plan = [c for c in SWEEP if not only or c["tag"] in only]
        if not plan:
            print(f"[중단] --only 일치 조합 없음: {args.only}")
            sys.exit(1)
        SWEEP_DIR.mkdir(parents=True, exist_ok=True)
        print(f"스윕 {len(plan)}개 조합 → {SWEEP_DIR}\n")
        for i, cfg in enumerate(plan, 1):
            cmd = build_cmd(cfg, args.limit)
            base_mark = " (=base)" if _is_base(cfg) else ""
            print(f"[{i}/{len(plan)}] {cfg['tag']}{base_mark} · media={cfg['media']} · "
                  f"frames={cfg['frames']} side={cfg['side']} imax={cfg['imax']} imin={cfg['imin']}")
            print("     " + " ".join(f'"{c}"' if " " in c else c for c in cmd))
            if args.dry_run:
                continue
            r = subprocess.run(cmd)
            if r.returncode != 0:
                print(f"  [경고] {cfg['tag']} 실행 실패(returncode={r.returncode}) — 계속 진행")
        if args.dry_run:
            print("\n[dry-run] 실제 추론은 하지 않았습니다.")
            return

    # 요약표 생성/저장
    summary = summarize()
    sp = SWEEP_DIR / "SWEEP_SUMMARY.md"
    SWEEP_DIR.mkdir(parents=True, exist_ok=True)
    sp.write_text(summary, encoding="utf-8")
    print("\n" + summary)
    print(f"\n요약 저장 → {sp}")
    print(r"PDF: venv\Scripts\python.exe vlm\tools\report_to_pdf.py")


if __name__ == "__main__":
    main()
