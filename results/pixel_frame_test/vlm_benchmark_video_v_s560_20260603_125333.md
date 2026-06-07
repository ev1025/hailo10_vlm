# 엣지 VLM 해석 평가 (v_s560)

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
| Qwen3-VL-2B-Instruct | ✅ 7.71s | 83% | 72% | 11% | 2.74s | 31.2 | 4511 MB |

## Qwen3-VL-2B-Instruct — `Qwen/Qwen3-VL-2B-Instruct`

**위험 유형별 인식 (카테고리별 정답률)**

| 카테고리 | 정답유형 | N | 위험판정 | 판정정답률 | 유형정답률 | 미상 |
|---|---|---|---|---|---|---|
| 화재 | 화재 | 8 | 8 | 100% | 88% | 0 |
| 연기 | 화재 | 9 | 8 | 89% | 89% | 0 |
| 사람 쓰러짐/낙상 | 낙상 | 5 | 3 | 60% | 60% | 0 |
| 기계·장비 전도 | 전도 | 5 | 3 | 60% | 0% | 0 |
| 정상 주차장(오탐 테스트) | 없음 | 5 | 0 | 100% | 100% | 0 |
| 정상 작업장(오탐 테스트) | 없음 | 4 | 1 | 75% | 75% | 0 |

**항목별 결과**

| 유형 | 정답 | 판정 | 정오 | 시간 | 해석(앞부분) |
|---|---|---|---|---|---|
| 화재 | 위험 | 위험 | ✅ | 3.0s | 화재가 발생한 것으로 보이며, 연기와 불꽃이 시야에 나타나고 있으며, 인물은 화재를 진압하는 데 직… |
| 낙상 | 위험 | 위험 | ✅ | 3.7s | 카메라가 촬영된 장면에서 차량이 빠르게 움직이며, 그 후에 빛이 강하게 밝아지는 것을 볼 수 있습니… |
| 화재 | 위험 | 위험 | ✅ | 2.2s | 실내에서 불꽃이 발생하여 주변이 붉게 빛나고 있으며, 이는 화재의 신호를 나타냅니다. 현재의 상황은… |
| 화재 | 위험 | 위험 | ✅ | 1.8s | 화재가 발생한 건물 앞에서 소방관들이 활동하고 있으며, 불꽃과 연기로 인해 위험한 상황이 발생하고 … |
| 화재 | 위험 | 위험 | ✅ | 2.7s | 방 안에서 불이 발생하고 있으며, 주변에는 가구와 전자기기 등이 높은 위험을 초래할 수 있는 물체들… |
| 화재 | 위험 | 위험 | ✅ | 3.4s | 화재가 발생한 장소에서 빠르게 소화되는 방식으로 인해 주변이 흐릿하게 보이며, 인원이 즉각적인 대응… |
| 화재 | 위험 | 위험 | ✅ | 1.9s | 화재 감지 시스템이 활성화되어 있으며, 화재 발생 위치가 여러 곳에서 확인됨. 이는 빠른 대응이 필… |
| 화재 | 위험 | 위험 | ✅ | 2.2s | 화재 감지 시스템이 활성화되어 있으며, 실내에서 불꽃과 연기가 발생하고 있습니다. 이는 빠른 대응이… |
| 낙상 | 위험 | 위험 | ✅ | 9.9s | 장면에서 forklift가 트럭 앞에 위치하고 있으며, 운전자가 트럭을 타고 있는 것을 볼 수 있습… |
| 낙상 | 위험 | 위험 | ✅ | 2.6s | 장면에서 높은 위치에 있는 트럭이 떨어져서 바닥에 떨어졌으며, 이는 낙상의 위험을 나타냅니다. 이는… |
| 낙상 | 위험 | 위험 | ✅ | 2.7s | 이 영상은 재난 현장의 엣지 카메라로 캡처된 장면이며, 기계가 무게를 초과하여 떨어지는 순간이 보입… |
| 없음 | 위험 | 정상 | ❌ | 2.9s | 장소는 공장 내부이며, 작업자들이 안전한 거리에서 움직이고 있으며, 장비는 정상적으로 작동하고 있습… |
| 없음 | 위험 | 정상 | ❌ | 2.6s | 화면에는 포장된 상자들이 정돈되어 있으며, 포크세터가 작업 중인 상태이며, 주변에는 안전한 공간이 … |
| 없음 | 정상 | 정상 | ✅ | 2.7s | 차량이 주차된 공간 내에서 이동하고 있는 것으로 보이며, 주변에는 다른 차량들이 정지되어 있으며, … |
| 없음 | 정상 | 정상 | ✅ | 2.5s | 화면에는 차량들이 주차된 것으로 보이며, 주변에는 녹색 식물과 조명이 설치되어 있는 것으로 보아 안… |
| 없음 | 정상 | 정상 | ✅ | 2.3s | 화면에는 물이 흐르는 지대와 건물, 차량이 보이며, 주변 환경은 정상적인 상태입니다. 다만, 바닥에… |
| 없음 | 정상 | 정상 | ✅ | 2.4s | 눈이 내리는 날, 주차장에서 운반 차량이 정지하고, 사람들은 눈으로 덮인 자동차와 주변을 걷고 있습… |
| 없음 | 정상 | 정상 | ✅ | 2.6s | 화면에는 차량이 주차되고 있으며, 주차장 내부는 정돈되어 있고, 아무런 위험한 현상이나 불안정한 상… |
| 없음 | 정상 | 정상 | ✅ | 2.0s | 화면에는 작업 중인 직원들과 다양한 물품이 보이며, 안전한 작업 환경이 유지되고 있습니다. 주변에는… |
| 없음 | 정상 | 정상 | ✅ | 2.0s | 장소는 창고로 보이며, 다양한 물품과 기계가 배치되어 있고, 사람들은 작업을 하고 있는 것으로 보이… |
| 없음 | 정상 | 정상 | ✅ | 1.7s | 공장 내부는 정돈되어 있으며, 물리적 위험 요소가 없으며, 작업 중인 인물들은 안전한 거리에서 활동… |
| 낙상 | 정상 | 위험 | ❌ | 2.5s | 화면에서 높은 위치에 있는 선반들이 무너져 내리며, 바닥에 깎아진 물체와 함께 많은 파손된 선반과 … |
| 없음 | 위험 | 정상 | ❌ | 2.3s | CCTV 영상에서 상점 내부의 고객과 직원이 상호작용하고 있으며, 주변에는 일반적인 상점 장비와 제… |
| 낙상 | 위험 | 위험 | ✅ | 2.5s | CCTV 영상에서 한 남성이 바닥에 떨어진 검은색 물건을 들고 있는 모습이 보이며, 그 물건이 바닥… |
| 없음 | 위험 | 정상 | ❌ | 3.1s | 화면에는 사람과 가정용 건물이 보이며, 주변 환경은 평화롭고 안정적인 상태입니다. 다만, 빛이 강하… |
| 낙상 | 위험 | 위험 | ✅ | 3.2s | 엘리베이터가 빠르게 움직이며 사람들을 이동시키는 동안, 한 사람이 엘리베이터 안에서 무언가를 잡고 … |
| 낙상 | 위험 | 위험 | ✅ | 3.3s | 엘리베이터가 운행 중인 시점에서 한 사람이 엘리베이터를 타고 내려가면서 무단히 떨어져서 바닥에 넘어… |
| 화재 | 위험 | 위험 | ✅ | 2.1s | 화재가 발생한 것으로 보이며, 연기와 불꽃이 관찰되며, 소방대원들이 현장을 진입하고 있다. 이는 매… |
| 화재 | 위험 | 위험 | ✅ | 2.3s | 화재 감지 알림이 표시되어 있으며, 작업자들이 화재 발생 장소에서 빠르게 떨어져 나가고 있다. 이는… |
| 없음 | 위험 | 정상 | ❌ | 2.2s | 화면에는 공기 중에 있는 연기와 함께 흐르는 바람이 보이며, 이는 자연적인 현상으로 보이며, 위험 … |
| 화재 | 위험 | 위험 | ✅ | 2.4s | 건물 사이에서 검은 연기와 불꽃이 떠오르며, 이는 화재 발생의 징후로 보이며, 주변 환경이 위험한 … |
| 화재 | 위험 | 위험 | ✅ | 2.8s | 공장의 여러 탱크와 연기 방출 시스템에서 연기가 발생하고 있으며, 이는 화재의 가능성을 시사합니다.… |
| 화재 | 위험 | 위험 | ✅ | 2.4s | 화재 발생 현상이 나타나며, 연기와 불꽃이 뚜렷하게 보이며, 주변의 물체가 파손되고 있다. 이는 매… |
| 화재 | 위험 | 위험 | ✅ | 2.5s | 화재가 발생한 것으로 보이며, 연기와 불꽃이 관찰되며, 이는 위험한 상황을 나타냅니다. 화재가 발생… |
| 화재 | 위험 | 위험 | ✅ | 3.1s | 화재가 발생하여 건물이 �il리고 있으며, 연기와 불꽃이 뚜렷하게 보이며, 이는 매우 심각한 위험을… |
| 화재 | 위험 | 위험 | ✅ | 2.2s | 화면 오른쪽에서 불꽃이 떨어져 있으며, 주변은 흐릿한 상태로 인해 위험한 상황이 발생하고 있다. |

## 상세 내역 

### Qwen3-VL-2B-Instruct

<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire1.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire1.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 것으로 보이며, 연기와 불꽃이 시야에 나타나고 있으며, 인물은 화재를 진압하는 데 직면해 있습니다. 이는 매우 심각한 상황으로, 즉시 대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire2.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire2.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 카메라가 촬영된 장면에서 차량이 빠르게 움직이며, 그 후에 빛이 강하게 밝아지는 것을 볼 수 있습니다. 이는 차량이 빠르게 움직이고, 주변 환경이 불안정한 것으로 보이며, 이는 낙상의 위험을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire3.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire3.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 실내에서 불꽃이 발생하여 주변이 붉게 빛나고 있으며, 이는 화재의 신호를 나타냅니다. 현재의 상황은 매우 위험하며, 즉시 구조대가 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire4.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire4.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 건물 앞에서 소방관들이 활동하고 있으며, 불꽃과 연기로 인해 위험한 상황이 발생하고 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire5.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire5.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 방 안에서 불이 발생하고 있으며, 주변에는 가구와 전자기기 등이 높은 위험을 초래할 수 있는 물체들이 배치되어 있습니다. 이는 화재 발생의 위험을 높이고, 즉시 구조적 대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire6.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire6.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 장소에서 빠르게 소화되는 방식으로 인해 주변이 흐릿하게 보이며, 인원이 즉각적인 대응을 하기 위해 빠르게 움직이고 있다. 이는 매우 심각한 상황을 나타내며, 즉각적인 대응이 필요하다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire7.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire7.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 감지 시스템이 활성화되어 있으며, 화재 발생 위치가 여러 곳에서 확인됨. 이는 빠른 대응이 필요함.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire8.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire8.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 감지 시스템이 활성화되어 있으며, 실내에서 불꽃과 연기가 발생하고 있습니다. 이는 빠른 대응이 필요하며, 즉각적인 안전 조치가 취해져야 합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover1.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover1.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 장면에서 forklift가 트럭 앞에 위치하고 있으며, 운전자가 트럭을 타고 있는 것을 볼 수 있습니다. 이는 작업 중 발생할 수 있는 위험한 상황을 나타냅니다. 특히, 트럭이 운전자가 타고 있는 상태에서 forklift가 트럭을 빠르게 움직일 경우, 운전자가 트럭을 타고 있는 상태에서 forklift가 트럭을 빠르게 움직일 경우, 운전자가 트럭을 타고 있는 상태에서 forklift가 트럭을 빠르게 움직일 경우, 운전자가 트럭을 타고 있는 상태에서 forklift가 트럭을 빠르게 움직일 경우, 운전자가 트럭을 타고 있는 상태에서 forklift가 트럭을 빠르게 움직일 경우, 운전자가 트럭을 타고 있는 상태에서 forklift가 트럭을 빠르게 움직일 경우, 운전자가 트럭을 타고 있는 상태에서 forklift가 트럭을 빠르게 움직일 경우, 운전자가 트럭을 타고 있는 상태에서 forklift가 트럭을 빠르게 �</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover2.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover2.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 장면에서 높은 위치에 있는 트럭이 떨어져서 바닥에 떨어졌으며, 이는 낙상의 위험을 나타냅니다. 이는 작업자에게 위험한 상황을 초래할 수 있으며, 즉시 조치가 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover3.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover3.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 이 영상은 재난 현장의 엣지 카메라로 캡처된 장면이며, 기계가 무게를 초과하여 떨어지는 순간이 보입니다. 이는 작업 중 발생한 사고로, 작업자에게 위험한 상황을 초래할 수 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover4.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover4.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 장소는 공장 내부이며, 작업자들이 안전한 거리에서 움직이고 있으며, 장비는 정상적으로 작동하고 있습니다. 화재나 낙상 등의 위험 요소가 보이지 않으며, 장비와 인원 모두 안전하게 운영되고 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover5.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover5.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 포장된 상자들이 정돈되어 있으며, 포크세터가 작업 중인 상태이며, 주변에는 안전한 공간이 보입니다. 이는 위험 요소가 없는 정상적인 작업 환경을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking1.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking1.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 차량이 주차된 공간 내에서 이동하고 있는 것으로 보이며, 주변에는 다른 차량들이 정지되어 있으며, 안전한 상태로 보입니다. 다만, CCTV 영상의 품질상 일부 흐릿함이 있을 수 있으나, 위험 요소는 없습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking2.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking2.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 차량들이 주차된 것으로 보이며, 주변에는 녹색 식물과 조명이 설치되어 있는 것으로 보아 안전한 상태입니다. 다만, CCTV 영상의 품질상 일부 불분명한 부분이 있지만, 현재 상황은 위험 요소가 없습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking3.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking3.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 물이 흐르는 지대와 건물, 차량이 보이며, 주변 환경은 정상적인 상태입니다. 다만, 바닥에 물이 묻어 있는 것은 정상적인 상태로 간주됩니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking4.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking4.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 눈이 내리는 날, 주차장에서 운반 차량이 정지하고, 사람들은 눈으로 덮인 자동차와 주변을 걷고 있습니다. 주변에는 다른 차량들이 보이며, 모든 객체는 안전하게 유지되고 있는 것으로 보입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking5.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking5.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 차량이 주차되고 있으며, 주차장 내부는 정돈되어 있고, 아무런 위험한 현상이나 불안정한 상태가 보이지 않습니다. 주변에는 안전 기기나 특별한 위험 요소가 없으며, 모든 차량은 안정적으로 주차되어 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker1.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker1.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 작업 중인 직원들과 다양한 물품이 보이며, 안전한 작업 환경이 유지되고 있습니다. 주변에는 휘발성 물질이 없는 것으로 보이며, 위험 요소는 없습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker2.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker2.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 장소는 창고로 보이며, 다양한 물품과 기계가 배치되어 있고, 사람들은 작업을 하고 있는 것으로 보이지만, 현재에는 위험한 상황이나 이상적인 행동이 나타나지 않았습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker3.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker3.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 공장 내부는 정돈되어 있으며, 물리적 위험 요소가 없으며, 작업 중인 인물들은 안전한 거리에서 활동하고 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker_4.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker_4.mp4 · 정답 정상 · 판정 위험(낙상) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 화면에서 높은 위치에 있는 선반들이 무너져 내리며, 바닥에 깎아진 물체와 함께 많은 파손된 선반과 포장재가 흩어져 있습니다. 이는 낙상의 위험이 매우 높음을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall1.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall1.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> CCTV 영상에서 상점 내부의 고객과 직원이 상호작용하고 있으며, 주변에는 일반적인 상점 장비와 제품이 보입니다. 영상은 정상적인 상점 운영 환경을 나타내며, 위험 요소는 보이지 않습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall2.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall2.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> CCTV 영상에서 한 남성이 바닥에 떨어진 검은색 물건을 들고 있는 모습이 보이며, 그 물건이 바닥에 떨어져 있는 것으로 보아 위험한 상황이 발생하고 있다. 이는 낙상 위험이 존재하는 것으로 판단된다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall3.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall3.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 사람과 가정용 건물이 보이며, 주변 환경은 평화롭고 안정적인 상태입니다. 다만, 빛이 강하게 빛나는 부분이 있어 일부 흐림이 발생했지만, 이는 자연광의 영향일 뿐입니다. 아무런 위험 요소가 보이지 않으며, 현재 상황은 정상입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall4.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall4.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 엘리베이터가 빠르게 움직이며 사람들을 이동시키는 동안, 한 사람이 엘리베이터 안에서 무언가를 잡고 있는 것으로 보이며, 그 후에 엘리베이터가 떨어지는 듯한 모습이 나타남. 이는 낙상 위험이 존재함을 시사하며, 현재 상황은 매우 위험하다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall5.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall5.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 엘리베이터가 운행 중인 시점에서 한 사람이 엘리베이터를 타고 내려가면서 무단히 떨어져서 바닥에 넘어지는 사고가 발생한 것으로 보이며, 이는 매우 심각한 위험을 초래할 수 있습니다. 이는 엘리베이터 안내자와 같은 인력이 즉각적인 조치를 취해야 할 상황입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke1.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke1.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 것으로 보이며, 연기와 불꽃이 관찰되며, 소방대원들이 현장을 진입하고 있다. 이는 매우 심각한 상황으로, 즉시 대응이 필요하다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke2.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke2.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 감지 알림이 표시되어 있으며, 작업자들이 화재 발생 장소에서 빠르게 떨어져 나가고 있다. 이는 화재 발생의 신호이며, 즉 위험한 상황이다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke3.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke3.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 공기 중에 있는 연기와 함께 흐르는 바람이 보이며, 이는 자연적인 현상으로 보이며, 위험 요소가 없습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke4.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke4.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 건물 사이에서 검은 연기와 불꽃이 떠오르며, 이는 화재 발생의 징후로 보이며, 주변 환경이 위험한 상태에 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke5.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke5.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 공장의 여러 탱크와 연기 방출 시스템에서 연기가 발생하고 있으며, 이는 화재의 가능성을 시사합니다. 특히, 탱크가 불안정한 상태일 수 있으므로, 즉각적인 안전 조치가 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire1.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire1.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 발생 현상이 나타나며, 연기와 불꽃이 뚜렷하게 보이며, 주변의 물체가 파손되고 있다. 이는 매우 심각한 위험을 의미하며, 즉시 구조 및 안전 조치가 필요하다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire2.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire2.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 것으로 보이며, 연기와 불꽃이 관찰되며, 이는 위험한 상황을 나타냅니다. 화재가 발생한 지역에서 스프링클러 시스템이 작동하여 불을 진압하는 것을 확인할 수 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire3.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire3.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생하여 건물이 �il리고 있으며, 연기와 불꽃이 뚜렷하게 보이며, 이는 매우 심각한 위험을 나타냅니다. 즉, 현재 상황은 화재가 진행되고 있으며, 즉각적인 대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire4.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire4.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화면 오른쪽에서 불꽃이 떨어져 있으며, 주변은 흐릿한 상태로 인해 위험한 상황이 발생하고 있다.</div></div></div>
