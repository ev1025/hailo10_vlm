"""
VLM 벤치마크 공통 설정 — 모델/카테고리/경로/프롬프트/프레임 파라미터.

이 폴더의 스크립트는 패키지가 아니라 평범한 스크립트로 실행한다.
  venv\\Scripts\\python.exe run_benchmark.py     # 추론 + md 리포트
실행 시 스크립트 폴더가 sys.path[0] 이 되어 `import config` 가 동작한다.
"""

from __future__ import annotations

from pathlib import Path

VLM_DIR = Path(__file__).resolve().parent
DATASET_DIR = VLM_DIR / "dataset"
VIDEO_DIR = DATASET_DIR / "videos"
IMAGE_DIR = DATASET_DIR / "images"
VIDEO_THUMB_DIR = DATASET_DIR / "video_thumbs"   # 영상 대표(중간) 프레임 — 리포트 카드용
RESULTS_DIR = VLM_DIR / "results"

# ── 테스트 대상 VLM (fp16) ──────────────────────────────────────
#   Qwen2-VL-2B 는 한국어 지시를 무시(이미지 이해 거부)해 제외 — 프롬프트_튜닝_기록.md '모델 선정' 참고.
#   → 한국어를 네이티브로 처리하는 Qwen3-VL-2B 단독 사용.
VLM_MODELS = [
    {"name": "Qwen3-VL-2B-Instruct", "hf_id": "Qwen/Qwen3-VL-2B-Instruct"},
]

# ── 데이터셋 카테고리 ───────────────────────────────────────────
#   분류 대상 위험 3종: ① 화재·연기 ② 사람 쓰러짐/낙상 ③ 기계·장비 전도(넘어짐)
#   + 오탐 통제용 정상 2종(주차장·작업장).
#   count: 수집 영상 수 · label: 정답(위험/정상) · danger: 위험유형(화재/낙상/전도/없음) · query: 유튜브 검색어
#   합계 영상 30개 → 각 영상의 중간 프레임 1장씩 = 이미지 30개. 모델당 60개, 2모델 120건.
#   카테고리 키 = dataset/images·videos 파일 접두사.
#   smoke 는 프롬프트상 '화재·연기' 묶음이라 정답유형 화재로 둠('smoke_fire*' 도 'smoke' 접두사로 매칭).
CATEGORIES = {
    "fire":            {"count": 6, "label": "위험", "danger": "화재", "query": "warehouse fire cctv footage",      "desc": "화재"},
    "smoke":           {"count": 7, "label": "위험", "danger": "화재", "query": "factory smoke cctv",              "desc": "연기"},
    "person_fall":     {"count": 5, "label": "위험", "danger": "낙상", "query": "worker collapse fall cctv",        "desc": "사람 쓰러짐/낙상"},
    "machine_tipover": {"count": 6, "label": "위험", "danger": "전도", "query": "forklift tip over accident cctv",  "desc": "기계·장비 전도"},
    "normal_parking":  {"count": 5, "label": "정상", "danger": "없음", "query": "empty parking lot cctv",           "desc": "정상 주차장(오탐 테스트)"},
    "normal_worker":   {"count": 5, "label": "정상", "danger": "없음", "query": "factory worker working cctv",      "desc": "정상 작업장(오탐 테스트)"},
}

VIDEO_EXTS = {".mp4", ".mkv", ".webm", ".mov", ".avi"}
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

# ── 영상 수집(yt-dlp) ───────────────────────────────────────────
MAX_DURATION_SEC = 30      # 30초 이하 영상만
MIN_DURATION_SEC = 3
VIDEO_MAX_HEIGHT = 480      # 단일 progressive 스트림 유도(ffmpeg 머지 불필요) + 용량 절감
SEARCH_POOL_MULT = 6        # 필터로 일부 탈락 → count*MULT 만큼 검색해 count개 확보

# ── 영상 추론 프레임 샘플링(OpenCV) ─────────────────────────────
#   파라미터 스윕 결과 16f+560px 채택 — 판정 83→89%(전도 판정 60→100%), VRAM 5.2GB(8GB 내).
#   기록: 프롬프트_튜닝_기록.md §3 · results/pixel_frame_test/SWEEP_SUMMARY.md
VIDEO_NUM_FRAMES = 16       # 균일 샘플 프레임 수(짝수: temporal_patch_size=2 정합). '동작' 위험은 프레임 수가 핵심
VIDEO_FRAME_MAX_SIDE = 560  # 프레임 최대 변(px) — 8GB VRAM 보호

# ── 이미지 픽셀 상한(Qwen-VL 프로세서) ──────────────────────────
IMAGE_MAX_PIXELS = 1280 * 28 * 28   # ≈ 100만 화소
IMAGE_MIN_PIXELS = 256 * 28 * 28

# ── 생성 ────────────────────────────────────────────────────────
MAX_NEW_TOKENS = 320        # 상세 해석을 담기 위한 여유(엣지 지연도 이 길이 기준으로 측정)
TEMPERATURE = 0.0           # 0이면 greedy(재현성)
FORCE_KOREAN = True         # 중국어/한자(CJK Han) 토큰을 생성 단계에서 차단 — 한국어만 강제
REPETITION_PENALTY = 1.05   # 약한 반복 억제. 반복은 프롬프트(P5 간결화)로 이미 해결(firepri 70건 반복 0)
NO_REPEAT_NGRAM_SIZE = 0    # off — 1.3/ngram3 실험상 고칠 반복은 없는데 출력만 길어지고 형식 깨짐(REPEAT_TEST.md)

# ── 프롬프트 (P5 + 유형 '낙상(사람)/낙상(기계)' + 연기→화재 우선. 기록: 프롬프트_튜닝_기록.md) ──
#   구조화(판정/유형/설명) + 설명 간결 + 정상 장면은 결론만. 한자 차단은 FORCE_KOREAN 이 담당.
#   '전도(顚倒)'는 동음이의가 많아 2B 모델이 기계 넘어짐을 전부 '낙상'으로 오인(유형 0%) → 단어를 바꿔도 무효.
#   해결①: 모델이 즐겨 쓰는 '낙상'을 주체로만 쪼갬 → '낙상(기계)' = 전도(채점기가 '기계' 키워드로 전도 매핑).
#   부작용: 옵션에 '낙상' 2회 → 사람 포함 연기 장면이 낙상으로 끌림(연기유형 71→62%).
#   해결②: "연기·불꽃 보이면 화재 우선" 규칙 추가 → 연기 62→81% 회복, 전도 91→100%·낙상 100% 유지.
#   (results/pixel_frame_test/TERM_TEST.md · SMOKE_FIX.md)
PROMPT = (
    "당신은 재난 현장의 엣지 카메라로 캡처된 장면을 해석하는 분석 AI입니다.\n"
    "이 캡처(이미지/영상)를 보고 상황을 한국어로 분석하세요.\n\n"
    "반드시 아래 형식으로 답하되, '판정'은 위험·정상 중 하나만, '유형'은 화재·낙상(사람)·낙상(기계)·없음 중 하나만 적으세요:\n"
    "판정: 위험 / 정상\n"
    "유형: 화재 / 낙상(사람) / 낙상(기계) / 없음\n"
    "설명: 화면에 보이는 객체, 위험 판단의 근거, 심각도, 그리고 필요한 조치를 구체적으로 서술\n"
    "단, 위험이 없으면(정상) 보이지 않는 위험 요소를 하나씩 나열하지 말고, 보이는 것과 '정상'이라는 결론만 1~2문장으로 쓰세요.\n"
    "특히, 연기·불꽃·화염이 보이면 사람이 함께 있어도 유형은 반드시 '화재'로 정하세요."
)

def category_of(stem: str) -> str | None:
    """파일 stem(예: car_fire_cctv_03) → 카테고리 키."""
    for cat in CATEGORIES:
        if stem.startswith(cat):
            return cat
    return None
