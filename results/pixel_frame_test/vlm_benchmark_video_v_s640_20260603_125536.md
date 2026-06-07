# 엣지 VLM 해석 평가 (v_s640)

## 데이터셋 구성 (위험 3종 + 정상)

| 카테고리 | 정답 | 위험유형 | 영상 |
|---|---|---|---|
| 화재 (`fire`) | 위험 | 화재 | 8 |
| 연기 (`smoke`) | 위험 | 화재 | 9 |
| 사람 쓰러짐/낙상 (`person_fall`) | 위험 | 낙상 | 5 |
| 기계·장비 전도 (`machine_tipover`) | 위험 | 전도 | 5 |
| 정상 주차장(오탐 테스트) (`normal_parking`) | 정상 | 없음 | 5 |
| 정상 작업장(오탐 테스트) (`normal_worker`) | 정상 | 없음 | 4 |

## 모델 종합 비교

| 모델 | 로드 | 상황인식 정확도 | 유형 정확도 | 과잉해석(오탐) | 평균 지연 | tok/s | peak VRAM |
|---|---|---|---|---|---|---|---|
| Qwen3-VL-2B-Instruct | ✅ 7.72s | 86% | 72% | 11% | 2.99s | 29.3 | 4570 MB |

## Qwen3-VL-2B-Instruct — `Qwen/Qwen3-VL-2B-Instruct`

**위험 유형별 인식 (카테고리별 정답률)**

| 카테고리 | 정답유형 | N | 위험판정 | 판정정답률 | 유형정답률 | 미상 |
|---|---|---|---|---|---|---|
| 화재 | 화재 | 8 | 8 | 100% | 88% | 0 |
| 연기 | 화재 | 9 | 9 | 100% | 89% | 0 |
| 사람 쓰러짐/낙상 | 낙상 | 5 | 3 | 60% | 60% | 0 |
| 기계·장비 전도 | 전도 | 5 | 3 | 60% | 0% | 0 |
| 정상 주차장(오탐 테스트) | 없음 | 5 | 0 | 100% | 100% | 0 |
| 정상 작업장(오탐 테스트) | 없음 | 4 | 1 | 75% | 75% | 0 |

**항목별 결과**

| 유형 | 정답 | 판정 | 정오 | 시간 | 해석(앞부분) |
|---|---|---|---|---|---|
| 화재 | 위험 | 위험 | ✅ | 2.9s | 화재가 발생한 터널 내부에서 연기가 뚜렷하게 보이며, 인근에는 소방관들이 활동하고 있습니다. 이는 … |
| 낙상 | 위험 | 위험 | ✅ | 3.6s | 카메라가 촬영된 장면에서 차량이 빠르게 움직이며, 그 후에 빛이 강하게 밝아지는 것을 볼 수 있습니… |
| 화재 | 위험 | 위험 | ✅ | 2.9s | 화면 중앙의 테이블 위에 불꽃이 발생하고 있으며, 이는 화재의 징후로 보입니다. 현재의 상태에서 불… |
| 화재 | 위험 | 위험 | ✅ | 1.9s | 화재가 발생한 건물 앞에서 소방관들이 활동하고 있으며, 불꽃과 연기로 인해 위험한 상황이 발생하고 … |
| 화재 | 위험 | 위험 | ✅ | 2.9s | 방 안에서 불이 발생하고 있으며, 주변에는 가구와 전기 장비가 높게 놓여 있어 위험한 상태입니다. … |
| 화재 | 위험 | 위험 | ✅ | 2.2s | 화재가 발생한 장소에서 연기가 떠오르며, 인원이 대응하고 있으며, 화재는 매우 심각하게 진행되고 있… |
| 화재 | 위험 | 위험 | ✅ | 2.6s | 화재 감지 시스템이 활성화되어 있으며, 화재 발생 위치에서 빛나는 불꽃이 관찰됩니다. 이는 즉각적인… |
| 화재 | 위험 | 위험 | ✅ | 3.4s | 화재 감지 시스템이 활성화되어 화재가 발생한 것을 확인하며, 빛나는 불꽃과 함께 폭발적인 소리와 함… |
| 낙상 | 위험 | 위험 | ✅ | 10.2s | 장면에서 forklift가 트럭 앞에 위치하고 있으며, 운전자가 트럭을 타고 있는 것을 볼 수 있습… |
| 낙상 | 위험 | 위험 | ✅ | 3.7s | 포크세터가 트럭에 붙어 있는 상태에서 빠르게 움직이며 트럭의 뒷부분을 향해 달리며, 그 후 트럭이 … |
| 낙상 | 위험 | 위험 | ✅ | 3.1s | 이 영상은 재난 현장의 엣지 카메라로 캡처된 장면이며, 기계가 무게를 초과하여 떨어지는 순간이 보입… |
| 없음 | 위험 | 정상 | ❌ | 2.8s | 장소는 공장 내부이며, 작업자와 장비가 보이며, 이는 일반적인 작업 환경으로 보입니다. 그러나 장면… |
| 없음 | 위험 | 정상 | ❌ | 2.5s | 화면에는 포장된 상자들이 정돈되어 있으며, 포크세터가 작업 중인 상태이며, 주변에는 안전한 공간이 … |
| 없음 | 정상 | 정상 | ✅ | 3.0s | 캡처된 장면은 지하 주차장 내부이며, 차량들이 정비된 상태로 주차되어 있고, 아무런 위험한 현상이나… |
| 없음 | 정상 | 정상 | ✅ | 2.7s | 화면에는 차량들이 주차된 것으로 보이며, 주변에는 녹색 식물과 조명이 설치되어 있는 것으로 보아 안… |
| 없음 | 정상 | 정상 | ✅ | 2.8s | 화면에는 물이 흐르는 지대와 건물, 차량이 보이며, 주변 환경은 정상적인 상태입니다. 다만, 바닥에… |
| 없음 | 정상 | 정상 | ✅ | 2.7s | 눈이 내리는 날, 주차장에서 운반 차량과 차량 사이에 있는 사람, 그리고 토양을 깨끗하게 하는 장비… |
| 없음 | 정상 | 정상 | ✅ | 2.2s | 화면에는 차량이 주차되고 있으며, 인공위치와 기계적 장비는 보이지 않으며, 주변에는 특별한 위험 요… |
| 없음 | 정상 | 정상 | ✅ | 3.1s | 화면에는 작업 중인 직원들과 다양한 포장된 상품들이 보이며, 작업 공간은 정돈되어 있고, 안전 장비… |
| 없음 | 정상 | 정상 | ✅ | 2.2s | 화면에는 작업 중인 인물과 물품이 보이며, 주변에는 일반적인 재료와 장비가 배치되어 있습니다. 이는… |
| 없음 | 정상 | 정상 | ✅ | 1.7s | 공장 내부는 정돈되어 있으며, 작업 중인 장비와 인원은 안전한 상태로 보이며, 위험 요소가 없습니다… |
| 낙상 | 정상 | 위험 | ❌ | 2.8s | 화면에서 높은 위치에 있는 선반들이 무너져 내리며, 바닥에 깨진 패allet과 물건들이 흩어져 있음… |
| 없음 | 위험 | 정상 | ❌ | 3.1s | CCTV 영상에서 캡처된 장면은 상점 내부의 일반적인 상황을 보여주며, 고객과 직원 간의 상호작용이… |
| 낙상 | 위험 | 위험 | ✅ | 3.4s | 카메라에서 촬영된 장면은 식당의 주방 내부이며, 한 남성이 검은색 의자에 앉아 있는 것을 보고 있다… |
| 없음 | 위험 | 정상 | ❌ | 2.2s | 화면에는 사람과 자동차가 보이며, 주변 환경은 평화롭고 정상적인 상태입니다. 아무런 위험 요소가 보… |
| 낙상 | 위험 | 위험 | ✅ | 3.2s | 엣지 카메라에서 촬영된 장면에서 사람들이 승강기에서 떨어지는 모습이 보이며, 이는 낙상 위험을 나타… |
| 낙상 | 위험 | 위험 | ✅ | 3.8s | 엘리베이터가 운행 중인 시점에서 한 사람이 엘리베이터를 타고 내려가면서 무단히 떨어져서 바닥에 넘어… |
| 화재 | 위험 | 위험 | ✅ | 4.0s | CCTV 영상에서 화재 발생 후 빠른 소방대의 대응이 보이며, 건물 내부가 불에 휘둘리고 있다. 화… |
| 화재 | 위험 | 위험 | ✅ | 2.3s | 화재 감지 알림이 표시되어 있으며, 작업자들이 물을 흘리는 상태로 보이며, 화재 발생 가능성이 높음… |
| 낙상 | 위험 | 위험 | ✅ | 2.0s | 하늘에서 흐르는 연기와 함께 공기 중에 떠 있는 물질이 관찰되며, 이는 낙상 위험이 있는 것으로 보… |
| 화재 | 위험 | 위험 | ✅ | 2.3s | 건물들이 연기와 함께 불을 띠고 있으며, 이는 화재 발생의 징후입니다. 현재의 상황에서 건물이 파괴… |
| 화재 | 위험 | 위험 | ✅ | 2.4s | 공장 내부에서 연기가 나는 것으로 보이며, 일부 건물에는 불꽃이 떨어지는 모습이 관찰된다. 이는 화… |
| 화재 | 위험 | 위험 | ✅ | 3.1s | 화재 발생 현상이 관찰되며, 연기와 불꽃이 빠르게 확산되고 있으며, 인원들이 긴급히 이동하고 있는 … |
| 화재 | 위험 | 위험 | ✅ | 2.7s | 화재가 발생한 것으로 보이며, 연기와 불꽃이 관찰되며, 화재가 확산되고 있는 상황임을 알 수 있음.… |
| 화재 | 위험 | 위험 | ✅ | 2.7s | 화재가 발생하여 큰 연기와 불꽃이 나오고 있으며, 건물이 파손되고 있다. 이는 매우 심각한 위험 상… |
| 화재 | 위험 | 위험 | ✅ | 2.6s | 화면 중앙에서 빛나는 불꽃이 발생하고 있으며, 주변은 흐릿하게 보이며, 이는 화재의 신호를 나타냅니… |

## 상세 내역 

### Qwen3-VL-2B-Instruct

<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire1.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire1.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 터널 내부에서 연기가 뚜렷하게 보이며, 인근에는 소방관들이 활동하고 있습니다. 이는 매우 위험한 상황이며, 즉시 구조 작업이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire2.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire2.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 카메라가 촬영된 장면에서 차량이 빠르게 움직이며, 그 후에 빛이 강하게 밝아지는 것을 볼 수 있습니다. 이는 차량이 빠르게 움직이고, 빛이 강하게 밝아지는 것으로, 낙상의 위험이 존재합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire3.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire3.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화면 중앙의 테이블 위에 불꽃이 발생하고 있으며, 이는 화재의 징후로 보입니다. 현재의 상태에서 불꽃이 계속해서 유지되고 있음을 확인할 수 있습니다. 즉, 위험한 상황이 발생하고 있으며, 즉각적인 조치가 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire4.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire4.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 건물 앞에서 소방관들이 활동하고 있으며, 불꽃과 연기로 인해 위험한 상황이 발생하고 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire5.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire5.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 방 안에서 불이 발생하고 있으며, 주변에는 가구와 전기 장비가 높게 놓여 있어 위험한 상태입니다. 화재는 빠르게 확산되고 있으며, 이는 빠른 구조적 대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire6.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire6.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 장소에서 연기가 떠오르며, 인원이 대응하고 있으며, 화재는 매우 심각하게 진행되고 있다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire7.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire7.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 감지 시스템이 활성화되어 있으며, 화재 발생 위치에서 빛나는 불꽃이 관찰됩니다. 이는 즉각적인 위험을 나타내며, 즉시 대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire8.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire8.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 감지 시스템이 활성화되어 화재가 발생한 것을 확인하며, 빛나는 불꽃과 함께 폭발적인 소리와 함께 연기, 파편이 발생하고 있으며, 이는 매우 심각한 위험을 나타냅니다. 즉, 현재 상황은 화재 발생 상태이며, 즉시 구조 및 안전 조치가 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover1.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover1.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 장면에서 forklift가 트럭 앞에 위치하고 있으며, 운전자가 트럭을 타고 있는 것을 볼 수 있습니다. 이는 작업 중 발생할 수 있는 위험한 상황을 나타냅니다. 특히, 트럭이 운전자가 타고 있는 상태에서 forklift가 트럭을 빠르게 움직일 경우, 운전자가 트럭을 타고 있는 상태에서 forklift가 트럭을 빠르게 움직일 경우, 운전자가 트럭을 타고 있는 상태에서 forklift가 트럭을 빠르게 움직일 경우, 운전자가 트럭을 타고 있는 상태에서 forklift가 트럭을 빠르게 움직일 경우, 운전자가 트럭을 타고 있는 상태에서 forklift가 트럭을 빠르게 움직일 경우, 운전자가 트럭을 타고 있는 상태에서 forklift가 트럭을 빠르게 움직일 경우, 운전자가 트럭을 타고 있는 상태에서 forklift가 트럭을 빠르게 움직일 경우, 운전자가 트럭을 타고 있는 상태에서 forklift가 트럭을 빠르게 �</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover2.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover2.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 포크세터가 트럭에 붙어 있는 상태에서 빠르게 움직이며 트럭의 뒷부분을 향해 달리며, 그 후 트럭이 뒤로 떨어져서 바닥에 떨어지는 모습이 보입니다. 이는 매우 위험한 상황이며, 운전자가 사고를 피할 수 없으며, 즉시 조치가 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover3.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover3.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 이 영상은 재난 현장의 엣지 카메라로 캡처된 장면이며, 기계가 무게를 초과하여 떨어지는 순간이 보입니다. 이는 작업 중 발생한 사고로, 작업자에게 위험한 상황을 초래할 수 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover4.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover4.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 장소는 공장 내부이며, 작업자와 장비가 보이며, 이는 일반적인 작업 환경으로 보입니다. 그러나 장면에서의 움직임이나 이상한 행동은 보이지 않으며, 위험 요소는 없습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover5.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover5.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 포장된 상자들이 정돈되어 있으며, 포크세터가 작업 중인 상태이며, 주변에는 안전한 공간이 보입니다. 이는 위험 요소가 없는 정상적인 작업 환경을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking1.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking1.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 캡처된 장면은 지하 주차장 내부이며, 차량들이 정비된 상태로 주차되어 있고, 아무런 위험한 현상이나 불안정한 상태가 보이지 않습니다. 주변에는 빛이 잘 비추어져 있으며, 차량들의 위치와 운행 상태는 안정적입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking2.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking2.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 차량들이 주차된 것으로 보이며, 주변에는 녹색 식물과 조명이 설치되어 있는 것으로 보아 안전한 상태입니다. 다만, CCTV 영상의 품질상 일부 불분명한 부분이 있지만, 현재 상황은 위험 요소가 없습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking3.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking3.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 물이 흐르는 지대와 건물, 차량이 보이며, 주변 환경은 정상적인 상태입니다. 다만, 바닥에 물이 묻어 있는 것은 정상적인 상태로 간주됩니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking4.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking4.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 눈이 내리는 날, 주차장에서 운반 차량과 차량 사이에 있는 사람, 그리고 토양을 깨끗하게 하는 장비가 보이며, 모든 객체는 안정적인 상태로 보이며, 위험 요소는 없습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking5.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking5.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 차량이 주차되고 있으며, 인공위치와 기계적 장비는 보이지 않으며, 주변에는 특별한 위험 요소나 불안정한 상태가 나타나지 않습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker1.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker1.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 작업 중인 직원들과 다양한 포장된 상품들이 보이며, 작업 공간은 정돈되어 있고, 안전 장비를 착용한 상태입니다. 주변에는 물리적 위험 요소가 없으며, 전기나 화학물질 등의 위험 요소도 보이지 않습니다. 따라서 이 장면은 정상적인 상태입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker2.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker2.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 작업 중인 인물과 물품이 보이며, 주변에는 일반적인 재료와 장비가 배치되어 있습니다. 이는 안전한 상태로 보이며, 위험 요소는 없습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker3.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker3.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 공장 내부는 정돈되어 있으며, 작업 중인 장비와 인원은 안전한 상태로 보이며, 위험 요소가 없습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker_4.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker_4.mp4 · 정답 정상 · 판정 위험(낙상) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 화면에서 높은 위치에 있는 선반들이 무너져 내리며, 바닥에 깨진 패allet과 물건들이 흩어져 있음을 확인할 수 있습니다. 이는 낙상의 위험이 매우 높은 상태이며, 즉시 조치가 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall1.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall1.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> CCTV 영상에서 캡처된 장면은 상점 내부의 일반적인 상황을 보여주며, 고객과 직원 간의 상호작용이 이루어지고 있으며, 주변에는 보안 장비와 안전 기기들이 설치되어 있습니다. 상점 내부는 정돈되어 있고, 제품이 잘 진열되어 있어 위험 요소가 없습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall2.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall2.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 카메라에서 촬영된 장면은 식당의 주방 내부이며, 한 남성이 검은색 의자에 앉아 있는 것을 보고 있다. 이 남성은 무언가를 들고 있으며, 그의 몸이 의자에 기대어 있는 상태로 보인다. 이는 낙상의 위험을 나타내며, 이는 위험한 상황을 의미한다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall3.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall3.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 사람과 자동차가 보이며, 주변 환경은 평화롭고 정상적인 상태입니다. 아무런 위험 요소가 보이지 않으며, 장면은 안전한 상태입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall4.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall4.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 엣지 카메라에서 촬영된 장면에서 사람들이 승강기에서 떨어지는 모습이 보이며, 이는 낙상 위험을 나타냅니다. 승강기에서 떨어지는 사람의 움직임은 즉각적인 위험을 초래할 수 있으며, 이는 급격한 위험 상황을 의미합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall5.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall5.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 엘리베이터가 운행 중인 시점에서 한 사람이 엘리베이터를 타고 내려가면서 무단히 떨어져서 바닥에 넘어지는 사고가 발생한 것으로 보이며, 이는 매우 심각한 위험을 초래할 수 있다. 이는 엘리베이터 안내 및 안전 조치가 부족한 상황에서 발생한 사고로, 즉시 인근의 안전 조치가 필요하다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke1.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke1.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> CCTV 영상에서 화재 발생 후 빠른 소방대의 대응이 보이며, 건물 내부가 불에 휘둘리고 있다. 화재는 큰 피해를 유발했으며, 60명의 소방관이 출동한 것으로 보인다. 이는 매우 심각한 위험 상황을 나타내며, 즉시 대응이 필요하다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke2.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke2.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 감지 알림이 표시되어 있으며, 작업자들이 물을 흘리는 상태로 보이며, 화재 발생 가능성이 높음.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke3.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke3.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 하늘에서 흐르는 연기와 함께 공기 중에 떠 있는 물질이 관찰되며, 이는 낙상 위험이 있는 것으로 보입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke4.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke4.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 건물들이 연기와 함께 불을 띠고 있으며, 이는 화재 발생의 징후입니다. 현재의 상황에서 건물이 파괴되고 있는 것으로 보이며, 위험한 상태입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke5.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke5.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 공장 내부에서 연기가 나는 것으로 보이며, 일부 건물에는 불꽃이 떨어지는 모습이 관찰된다. 이는 화재 발생의 가능성을 시사하며, 즉시 대응이 필요하다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire1.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire1.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 발생 현상이 관찰되며, 연기와 불꽃이 빠르게 확산되고 있으며, 인원들이 긴급히 이동하고 있는 상황이다. 이는 매우 심각한 위험을 나타내고 있으며, 즉각적인 대응이 필요하다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire2.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire2.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 것으로 보이며, 연기와 불꽃이 관찰되며, 화재가 확산되고 있는 상황임을 알 수 있음. 이는 위험한 상황이며, 즉시 대응이 필요함.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire3.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire3.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생하여 큰 연기와 불꽃이 나오고 있으며, 건물이 파손되고 있다. 이는 매우 심각한 위험 상황이다. 즉, 현재의 상황에서 위험한 상태이며, 즉, 화재가 진행되고 있는 것으로 판단된다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire4.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire4.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화면 중앙에서 빛나는 불꽃이 발생하고 있으며, 주변은 흐릿하게 보이며, 이는 화재의 신호를 나타냅니다. 현재의 상황은 매우 위험하며, 즉각적인 대응이 필요합니다.</div></div></div>
