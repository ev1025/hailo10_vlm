# hailo_vlm — 엣지 캡처 VLM 화재·재난 해석 평가

엣지 디바이스(YOLO)가 캡처한 화재·재난 현장 장면을 **Qwen3-VL-2B-Instruct**(비전언어모델)가 한국어로 얼마나 정확·상세히 해석하는지 평가하고 프롬프트·입력 파라미터를 튜닝한 프로젝트. 국방·재난 유지보수 현장 운용 가정.

**핵심 성과: 위험 유형(화재/낙상/전도/없음) 종합 분류 정확도 71% → 89%.**

> 처음 읽는다면 **[README.md](README.md)** (산출물·구조 요약) → **[프롬프트_튜닝_기록.md](프롬프트_튜닝_기록.md)** (튜닝 전 과정·근거) 순서로 보면 전체가 잡힌다.

## 저장소
- GitHub: `https://github.com/ev1025/hailo10_vlm` · branch `main`
- git author: `ev1025 <eg2874@naver.com>`
- **푸시 정책**: GitHub push 는 **사용자가 명시 요청할 때만**. 사내 GitLab(172.30.1.30) push 절대 금지.

## 구조
| 경로 | 설명 |
|---|---|
| `config.py` | 모델·카테고리·프롬프트·생성/프레임 파라미터 (채택 설정의 단일 출처) |
| `vlm_engine.py` | 모델 로드·추론(이미지·영상) + 한자 차단(FORCE_KOREAN) |
| `run_benchmark.py` | 추론 → 판정/유형 정확도·지연 집계 → `results/*.md` + `*.json` |
| `tools/` | 보조: `rebuild_report.py`(json→md), `report_to_pdf.py`(md→PDF), `param_sweep.py`·`analyze_sweep.py`(파라미터 스윕), `experiments.py`(검증 실험 term/smoke/repeat/korean/all) |
| `dataset/` | `images/`(커밋됨) · `videos/`·`video_thumbs/`(대용량, .gitignore) |
| `results/` | `pixel_frame_test/`(최종 평가 firepri + 스윕 + 실험검증 md/json/pdf), `prompt_test/`(P1~P5) |
| `프롬프트_튜닝_기록.md` | 메인 기록 — 모델선정~최종결과 전 과정 |

## 채택된 최종 설정 (`config.py`)
- **모델**: Qwen3-VL-2B-Instruct (fp16). Qwen2-VL-2B 는 한국어 거부로 제외.
- **프롬프트**: P5(간결) + 유형 어휘 `낙상(사람)`/`낙상(기계)` 분기 + **"연기·불꽃 보이면 화재 우선"** 규칙.
- **영상 입력**: 16프레임 · 560px(`VIDEO_NUM_FRAMES=16`, `VIDEO_FRAME_MAX_SIDE=560`). 이미지 ≈100만 화소.
- **FORCE_KOREAN=True**: 한자 포함 토큰 logits 를 −∞ 로 눌러 중국어 혼입 차단(디코딩 후처리, LogitsProcessor). 프롬프트로는 못 막힘.
- `REPETITION_PENALTY=1.05`, `NO_REPEAT_NGRAM_SIZE=0` — 반복은 프롬프트로 이미 해결돼 파라미터 상향은 미채택(역효과).

## 데이터 라벨 (파일 접두사로 정답 식별)
`fire`·`smoke`→화재 · `person_fall`→낙상 · `machine_tipover`→전도 · `normal_parking`·`normal_worker`→없음(정상).
이미지 34 + 영상 36. **영상은 .gitignore 라 clone 후 없음** → 평가하려면 같은 접두사로 `dataset/videos/` 에 넣어야 함.

## 실행
```powershell
# 셋업 (venv 없음 — 최초 1회). GPU: RTX 4060 8GB 기준
python -m venv venv
venv\Scripts\pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cu121
venv\Scripts\pip install -r requirements.txt   # transformers 5.9.0 등

# 추론 평가 (GPU)
venv\Scripts\python.exe run_benchmark.py --media image,video

# 결과 md → 이미지 임베드 PDF (MS Edge/Chrome 헤드리스 사용)
venv\Scripts\python.exe tools\report_to_pdf.py
```

## 작업 규칙 (중요)
- **VLM 출력은 정규식 후처리로 다듬지 말 것** — 모델 원문 그대로 노출(프롬프트로 튜닝). 채점기는 판정/유형 파싱에만 사용.
- **지표·표는 이미지·영상을 항상 둘 다** 표기(한쪽만 X).
- **GPU 사용 전 점유 여부 확인**(`nvidia-smi`), 다른 작업/사용자 있으면 대기. 본인 process 만 kill.
- **README 는 산출물 기준**(무엇이 만들어졌고 어디 있나를 앞에). 경로는 레포 루트 기준(`results/...`, `프롬프트_튜닝_기록.md`).
- 리포트 포맷을 바꾸면 GPU 재추론 없이 `tools/rebuild_report.py`(json→md) → `tools/report_to_pdf.py`(md→pdf) 로 재생성.

## 현재 상태
- 튜닝 완료(종합 유형 71→89%), 최종 설정 채택·푸시됨. README·튜닝기록 정리 완료.
- **남은 약점/후속 과제**:
  - 이미지 연기 일부(사람 포함 장면·옅은 연기) — 2B 모델 지각 한계.
  - 영상 낙상/전도 판정 일부 미탐 — few-shot / 파인튜닝 영역.
