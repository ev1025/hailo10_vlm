# 엣지 VLM 해석 평가 (v_f16s560)

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
| Qwen3-VL-2B-Instruct | ✅ 7.8s | 89% | 75% | 11% | 3.47s | 23.2 | 5176 MB |

## Qwen3-VL-2B-Instruct — `Qwen/Qwen3-VL-2B-Instruct`

**위험 유형별 인식 (카테고리별 정답률)**

| 카테고리 | 정답유형 | N | 위험판정 | 판정정답률 | 유형정답률 | 미상 |
|---|---|---|---|---|---|---|
| 화재 | 화재 | 8 | 8 | 100% | 100% | 0 |
| 연기 | 화재 | 9 | 8 | 89% | 89% | 0 |
| 사람 쓰러짐/낙상 | 낙상 | 5 | 3 | 60% | 60% | 0 |
| 기계·장비 전도 | 전도 | 5 | 5 | 100% | 0% | 0 |
| 정상 주차장(오탐 테스트) | 없음 | 5 | 0 | 100% | 100% | 0 |
| 정상 작업장(오탐 테스트) | 없음 | 4 | 1 | 75% | 75% | 0 |

**항목별 결과**

| 유형 | 정답 | 판정 | 정오 | 시간 | 해석(앞부분) |
|---|---|---|---|---|---|
| 화재 | 위험 | 위험 | ✅ | 4.6s | 화재가 발생한 것으로 보이며, 소방관이 화재를 진압하는 과정에서 빛이 흐르는 상태로, 주변은 매우 … |
| 화재 | 위험 | 위험 | ✅ | 3.6s | 카메라에서 촬영된 장면은 밤에 촬영되었으며, 차량 주변에 불꽃과 빛이 나는 것을 볼 수 있습니다. … |
| 화재 | 위험 | 위험 | ✅ | 2.9s | 화재는 카페트 위에 떨어진 불꽃이 발생하여 주변이 붉게 빛나고 있으며, 이는 매우 심각한 위험을 나… |
| 화재 | 위험 | 위험 | ✅ | 3.8s | 화재가 발생한 건물에서 불꽃과 연기가 뚜렷하게 보이며, 소방관들이 대응하고 있습니다. 화재는 매우 … |
| 화재 | 위험 | 위험 | ✅ | 2.7s | 방 안에서 불이 발생하고 있으며, 화재가 확대되고 있다. 이는 위험한 상황이며, 즉시 구조적 대응이… |
| 화재 | 위험 | 위험 | ✅ | 3.2s | 화재가 발생한 장소에서 빠르게 소화되는 과정이 보이며, 인원들이 물을 사용하여 대응하고 있습니다. … |
| 화재 | 위험 | 위험 | ✅ | 3.2s | 화재 감지 시스템이 활성화되어 있으며, 여러 개의 화재 경고 표시가 이미지에 나타나고 있다. 이는 … |
| 화재 | 위험 | 위험 | ✅ | 2.9s | 화재 감지 시스템이 작동하여 빠르게 인지하고, 직원들이 즉각적인 대응을 수행하며, 화재가 확산되고 … |
| 낙상 | 위험 | 위험 | ✅ | 6.0s | 장면은 공장 내에서 포크 레이저가 트럭에 올려진 물품을 운반하던 중, 무단으로 움직였으며, 그 결과… |
| 낙상 | 위험 | 위험 | ✅ | 4.5s | 장면에서 높은 위치에 있는 포크레인을 사용한 작업자가 운반 중인 트럭을 향해 움직이며, 그 후 트럭… |
| 낙상 | 위험 | 위험 | ✅ | 3.3s | 장면에서 높은 위치에 있는 물체가 무게를 견딜 수 없는 상태로 떨어져 사람을 던지는 사고가 발생하고… |
| 낙상 | 위험 | 위험 | ✅ | 2.9s | 화면에서 녹색 포크스틱이 높은 위치에서 떨어져 내려오는 모습이 보이며, 이는 낙상 위험을 나타냅니다… |
| 낙상 | 위험 | 위험 | ✅ | 4.4s | 화재나 낙상의 위험이 있는 상황이지만, 현재 화재나 낙상의 직접적인 증거는 없으며, 장면에서의 움직… |
| 없음 | 정상 | 정상 | ✅ | 3.5s | 캡처된 장면은 지하 주차장 내부이며, 차량들이 정비되어 있고, 안전한 상태로 보입니다. 주차장 내부… |
| 없음 | 정상 | 정상 | ✅ | 2.5s | 화면에는 차량들이 주차된 것으로 보이며, 주변에는 녹색 식물과 조명이 설치되어 있는 것으로 보아 안… |
| 없음 | 정상 | 정상 | ✅ | 2.4s | 화면에는 물이 흘러 있는 지대와 건물, 차량 등이 보이며, 아무런 위험한 현상이나 이상적인 상태가 … |
| 없음 | 정상 | 정상 | ✅ | 4.0s | 눈이 내리는 날, 주차장에서 차량이 정지하고, 한 사람이 토양 분해기로 눈을 제거하는 작업을 하고 … |
| 없음 | 정상 | 정상 | ✅ | 3.9s | 화면에는 차량이 여러 대 parked되어 있으며, 주차장 내부는 정돈되어 있고, 아무런 위험한 현상… |
| 없음 | 정상 | 정상 | ✅ | 3.7s | 화면에는 작업 중인 직원들과 다양한 물품이 보이며, 작업 공간은 정돈되어 있고, 안전 장비가 사용되… |
| 없음 | 정상 | 정상 | ✅ | 3.8s | 장면은 공장 내부의 작업 공간으로 보이며, 작업자와 물품이 정상적인 상태로 배치되어 있습니다. 주변… |
| 없음 | 정상 | 정상 | ✅ | 2.6s | 장소는 공장 내부이며, 작업 중인 장비와 인원은 안전한 상태로 보이며, 주변에는 위험 요소가 보이지… |
| 낙상 | 정상 | 위험 | ❌ | 3.2s | 화면에서 높은 위치에 있는 선반들이 무너져 내리는 모습이 보이며, 이는 물리적 위험을 의미합니다. … |
| 없음 | 위험 | 정상 | ❌ | 3.8s | CCTV 영상에서 고객이 상점 내부에서 상품을 구매하고, 직원이 결제를 처리하는 장면이 보이며, 주… |
| 낙상 | 위험 | 위험 | ✅ | 3.9s | CCTV 카메라에서 촬영된 장면은 높은 위험성을 가진 장소로 보이며, 한 사람이 작업 중에 무게를 … |
| 없음 | 위험 | 정상 | ❌ | 3.3s | 화면에는 사람과 자연환경이 보이며, 주변에는 건물과 녹지가 보입니다. 그러나 이 장면은 재난 현장에… |
| 낙상 | 위험 | 위험 | ✅ | 2.6s | 엘리베이터에서 한 사람이 넘어지며 다른 사람에게 도움을 요청하고 있으며, 이는 낙상의 위험을 나타냅… |
| 낙상 | 위험 | 위험 | ✅ | 4.1s | 엘리베이터가 끝까지 내려가면서 사람이 떨어졌으며, 경찰관이 그 사람을 구조하기 위해 도움을 요청하고… |
| 화재 | 위험 | 위험 | ✅ | 3.1s | CCTV 영상에서 화재가 발생한 것으로 보이며, 빛이 나는 불꽃과 연기가 관찰됩니다. 이는 매우 심… |
| 화재 | 위험 | 위험 | ✅ | 2.7s | 화재 감지 알림이 표시되어 있으며, 작업 중인 인원이 화재 발생 현장을 확인하고 빠르게 이동하고 있… |
| 없음 | 위험 | 정상 | ❌ | 3.7s | 화면에는 공기 중에 있는 연기와 함께 녹색 식물이 있는 지역이 보이며, 이는 자연적인 상태로 보입니… |
| 화재 | 위험 | 위험 | ✅ | 4.1s | 화면에는 검은 연기와 함께 건물들이 보이며, 이는 화재 발생의 시각적 증거입니다. 연기는 건물의 빛… |
| 화재 | 위험 | 위험 | ✅ | 3.0s | 공장의 여러 탱크와 연기 발생 현상이 관찰되며, 일부 구조물에서 불꽃이 떨어지는 모습이 보이며, 이… |
| 화재 | 위험 | 위험 | ✅ | 3.2s | 화재 발생 후 연기와 불꽃이 확산되고 있으며, 인원들이 급히 떨어져 있는 상황. 화재는 큰 규모로 … |
| 화재 | 위험 | 위험 | ✅ | 3.7s | 화재가 발생한 것으로 보이며, 방화기와 같은 소방 장비가 작동하고 있다. 화재는 빠르게 확산되고 있… |
| 화재 | 위험 | 위험 | ✅ | 3.1s | 화재가 발생하여 큰 불꽃과 연기가 나오고 있으며, 주변에는 소방관들이 대응하고 있습니다. 현재의 상… |
| 화재 | 위험 | 위험 | ✅ | 2.9s | 화재가 발생한 것으로 보이며, 불꽃과 연기가 공중에서 확산되고 있어 위험한 상황입니다. 이는 즉각적… |

## 상세 내역 

### Qwen3-VL-2B-Instruct

<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire1.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire1.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 것으로 보이며, 소방관이 화재를 진압하는 과정에서 빛이 흐르는 상태로, 주변은 매우 붉은색으로 변하고 있으며, 불꽃이 매우 강하게 떨어지고 있다. 이는 매우 위험한 상황이며, 즉시 구조 및 안전 조치가 필요하다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire2.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire2.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 카메라에서 촬영된 장면은 밤에 촬영되었으며, 차량 주변에 불꽃과 빛이 나는 것을 볼 수 있습니다. 이는 화재 발생의 징후로 보이며, 즉시 대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire3.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire3.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재는 카페트 위에 떨어진 불꽃이 발생하여 주변이 붉게 빛나고 있으며, 이는 매우 심각한 위험을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire4.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire4.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 건물에서 불꽃과 연기가 뚜렷하게 보이며, 소방관들이 대응하고 있습니다. 화재는 매우 심각하며, 건물의 구조가 위험해 보입니다. 이 상황에서는 즉각적인 구조적 대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire5.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire5.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 방 안에서 불이 발생하고 있으며, 화재가 확대되고 있다. 이는 위험한 상황이며, 즉시 구조적 대응이 필요하다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire6.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire6.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 장소에서 빠르게 소화되는 과정이 보이며, 인원들이 물을 사용하여 대응하고 있습니다. 이는 매우 심각한 상황이며, 즉시 대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire7.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire7.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 감지 시스템이 활성화되어 있으며, 여러 개의 화재 경고 표시가 이미지에 나타나고 있다. 이는 화재 발생의 신호를 제공하며, 즉시 대응이 필요하다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire8.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire8.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 감지 시스템이 작동하여 빠르게 인지하고, 직원들이 즉각적인 대응을 수행하며, 화재가 확산되고 있는 상황이 나타나고 있다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover1.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover1.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 장면은 공장 내에서 포크 레이저가 트럭에 올려진 물품을 운반하던 중, 무단으로 움직였으며, 그 결과 트럭이 넘어져 사고가 발생한 것으로 보입니다. 이는 포크 레이저의 안전 조작이 부족하고, 운전자가 주의를 기울지 않아 발생한 사고로, 매우 심각한 위험을 초래할 수 있습니다. 사고 후에는 즉시 조치를 취해야 하며, 작업자와 운전자의 교육 및 점검이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover2.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover2.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 장면에서 높은 위치에 있는 포크레인을 사용한 작업자가 운반 중인 트럭을 향해 움직이며, 그 후 트럭이 빠르게 회전하면서 포크레인의 일부가 트럭에 닿아 넘어져서 무너지는 모습이 보입니다. 이는 매우 위험한 상황이며, 작업자에게 큰 피해를 줄 수 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover3.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover3.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 장면에서 높은 위치에 있는 물체가 무게를 견딜 수 없는 상태로 떨어져 사람을 던지는 사고가 발생하고 있으며, 이는 작업 중인 인원에게 위험한 상황을 초래할 수 있다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover4.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover4.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 화면에서 녹색 포크스틱이 높은 위치에서 떨어져 내려오는 모습이 보이며, 이는 낙상 위험을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover5.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover5.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 화재나 낙상의 위험이 있는 상황이지만, 현재 화재나 낙상의 직접적인 증거는 없으며, 장면에서의 움직임은 위험 요소를 나타내는 것으로 보입니다. 그러나 이 장면에서는 빠른 움직임과 함께 인물이 사고 위험을 겪고 있는 것으로 보이며, 이는 위험한 상황을 의미합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking1.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking1.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 캡처된 장면은 지하 주차장 내부이며, 차량들이 정비되어 있고, 안전한 상태로 보입니다. 주차장 내부에는 특별한 위험 요소가 없으며, 조명과 안전 시스템이 작동 중입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking2.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking2.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 차량들이 주차된 것으로 보이며, 주변에는 녹색 식물과 조명이 설치되어 있는 것으로 보아 안전한 상태입니다. 다만, CCTV 영상의 품질상 일부 불분명한 부분이 있지만, 현재 상황은 위험 요소가 없습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking3.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking3.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 물이 흘러 있는 지대와 건물, 차량 등이 보이며, 아무런 위험한 현상이나 이상적인 상태가 나타나지 않았습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking4.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking4.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 눈이 내리는 날, 주차장에서 차량이 정지하고, 한 사람이 토양 분해기로 눈을 제거하는 작업을 하고 있습니다. 주변에는 다른 차량들이 있으며, 모든 장비와 사람들은 안전하게 움직이고 있습니다. 이는 일반적인 날씨 조건에서의 정상적인 작업을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking5.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking5.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 차량이 여러 대 parked되어 있으며, 주차장 내부는 정돈되어 있고, 아무런 위험한 현상이나 불안정한 상태가 보이지 않습니다. 또한, 인공위치나 특별한 안전 장비가 설치되어 있지 않으며, 주변 환경은 평온하고 안정적인 상태입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker1.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker1.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 작업 중인 직원들과 다양한 물품이 보이며, 작업 공간은 정돈되어 있고, 안전 장비가 사용되고 있습니다. 주변에는 휘발성 가스나 연기 등 위험 요소가 없는 것으로 보이며, 모든 장비와 인력은 안전하게 작동하고 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker2.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker2.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 장면은 공장 내부의 작업 공간으로 보이며, 작업자와 물품이 정상적인 상태로 배치되어 있습니다. 주변에는 택배용 트럭과 수납용 가방 등이 보이며, 작업자들은 안전한 거리에서 작업하고 있습니다. 이는 위험 요소가 없는 것으로 판단됩니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker3.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker3.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 장소는 공장 내부이며, 작업 중인 장비와 인원은 안전한 상태로 보이며, 주변에는 위험 요소가 보이지 않습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker_4.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker_4.mp4 · 정답 정상 · 판정 위험(낙상) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 화면에서 높은 위치에 있는 선반들이 무너져 내리는 모습이 보이며, 이는 물리적 위험을 의미합니다. 이는 사고 발생의 가능성을 높이고, 즉시 대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall1.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall1.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> CCTV 영상에서 고객이 상점 내부에서 상품을 구매하고, 직원이 결제를 처리하는 장면이 보이며, 주변에는 일반적인 상점 내 장비와 가구들이 보입니다. 영상은 정상적인 상점 운영 환경을 나타내며, 위험 요소는 보이지 않습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall2.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall2.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> CCTV 카메라에서 촬영된 장면은 높은 위험성을 가진 장소로 보이며, 한 사람이 작업 중에 무게를 견딜 수 없는 상태로 바닥에 넘어져 있는 모습이 보입니다. 이는 낙상 위험이 매우 높은 상황을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall3.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall3.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 사람과 자연환경이 보이며, 주변에는 건물과 녹지가 보입니다. 그러나 이 장면은 재난 현장에서의 위험 요소가 포함되어 있지 않으며, 현재의 상태는 정상적인 것으로 판단됩니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall4.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall4.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 엘리베이터에서 한 사람이 넘어지며 다른 사람에게 도움을 요청하고 있으며, 이는 낙상의 위험을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall5.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall5.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 엘리베이터가 끝까지 내려가면서 사람이 떨어졌으며, 경찰관이 그 사람을 구조하기 위해 도움을 요청하고 있다. 이는 낙상의 위험을 나타내며, 즉, 엘리베이터가 끝까지 내려가면서 사람의 안전이 위협받는 상황이다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke1.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke1.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> CCTV 영상에서 화재가 발생한 것으로 보이며, 빛이 나는 불꽃과 연기가 관찰됩니다. 이는 매우 심각한 위험을 나타내며, 즉시 대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke2.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke2.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 감지 알림이 표시되어 있으며, 작업 중인 인원이 화재 발생 현장을 확인하고 빠르게 이동하고 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke3.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke3.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 공기 중에 있는 연기와 함께 녹색 식물이 있는 지역이 보이며, 이는 자연적인 상태로 보입니다. 주변에는 건물과 산업시설이 있으며, 현재의 장면에서 위험 요소가 나타나지 않습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke4.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke4.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화면에는 검은 연기와 함께 건물들이 보이며, 이는 화재 발생의 시각적 증거입니다. 연기는 건물의 빛을 흐리게 하며, 주변 환경이 불안정해 보입니다. 이는 매우 심각한 위험을 나타내며, 즉시 구조대가 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke5.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke5.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 공장의 여러 탱크와 연기 발생 현상이 관찰되며, 일부 구조물에서 불꽃이 떨어지는 모습이 보이며, 이는 화재의 가능성을 시사합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire1.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire1.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 발생 후 연기와 불꽃이 확산되고 있으며, 인원들이 급히 떨어져 있는 상황. 화재는 큰 규모로 진행되고 있어, 즉각적인 대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire2.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire2.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 것으로 보이며, 방화기와 같은 소방 장비가 작동하고 있다. 화재는 빠르게 확산되고 있으며, 소방관들이 도착하기 전에 방화기로 불을 막는 것으로 보인다. 이는 매우 위험한 상황이다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire3.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire3.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생하여 큰 불꽃과 연기가 나오고 있으며, 주변에는 소방관들이 대응하고 있습니다. 현재의 상황은 매우 위험하며, 즉각적인 구조 및 소방대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire4.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire4.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 것으로 보이며, 불꽃과 연기가 공중에서 확산되고 있어 위험한 상황입니다. 이는 즉각적인 안전 조치가 필요합니다.</div></div></div>
