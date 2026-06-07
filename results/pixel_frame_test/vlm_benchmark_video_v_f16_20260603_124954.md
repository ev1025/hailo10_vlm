# 엣지 VLM 해석 평가 (v_f16)

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
| Qwen3-VL-2B-Instruct | ✅ 9.44s | 86% | 72% | 11% | 2.84s | 27.6 | 4855 MB |

## Qwen3-VL-2B-Instruct — `Qwen/Qwen3-VL-2B-Instruct`

**위험 유형별 인식 (카테고리별 정답률)**

| 카테고리 | 정답유형 | N | 위험판정 | 판정정답률 | 유형정답률 | 미상 |
|---|---|---|---|---|---|---|
| 화재 | 화재 | 8 | 8 | 100% | 100% | 0 |
| 연기 | 화재 | 9 | 8 | 89% | 78% | 0 |
| 사람 쓰러짐/낙상 | 낙상 | 5 | 3 | 60% | 60% | 0 |
| 기계·장비 전도 | 전도 | 5 | 4 | 80% | 0% | 0 |
| 정상 주차장(오탐 테스트) | 없음 | 5 | 0 | 100% | 100% | 0 |
| 정상 작업장(오탐 테스트) | 없음 | 4 | 1 | 75% | 75% | 0 |

**항목별 결과**

| 유형 | 정답 | 판정 | 정오 | 시간 | 해석(앞부분) |
|---|---|---|---|---|---|
| 화재 | 위험 | 위험 | ✅ | 2.7s | 화재가 발생한 것으로 보이며, 연기와 불꽃이 뚜렷하게 보이고, 인공적인 화재 장비를 사용하는 것으로… |
| 화재 | 위험 | 위험 | ✅ | 3.0s | 카메라에서 촬영된 장면은 밤에 촬영되었으며, 차량 주변에 불꽃과 연기가 발생하고 있는 것을 볼 수 … |
| 화재 | 위험 | 위험 | ✅ | 3.0s | 화재는 바닥에 있는 흰색 물체가 불을 띠고 있으며, 이는 화재 발생의 신호입니다. 이는 매우 심각한… |
| 화재 | 위험 | 위험 | ✅ | 2.5s | 화재가 발생한 건물에서 불꽃과 연기가 뚜렷하게 보이며, 소방관들이 대응하고 있습니다. 이는 매우 심… |
| 화재 | 위험 | 위험 | ✅ | 2.8s | 방 안에서 큰 불꽃이 발생하고 있으며, 주변의 물건들이 떨어질 수 있는 위험성이 존재합니다. 특히,… |
| 화재 | 위험 | 위험 | ✅ | 2.8s | 화재가 발생한 장소에서 연기가 퍼지고 있으며, 인원들이 물을 사용하여 대응하고 있습니다. 이는 매우… |
| 화재 | 위험 | 위험 | ✅ | 2.8s | 화재 감지 시스템이 활성화되어 있으며, 여러 개의 화재 경고 표시가 이미지에 나타나고 있다. 이는 … |
| 화재 | 위험 | 위험 | ✅ | 2.8s | 화재 감지 시스템이 작동하며, 화재가 발생한 장소에서 빛나는 불꽃과 연기가 관찰된다. 이는 즉각적인… |
| 낙상 | 위험 | 위험 | ✅ | 3.8s | 장면은 공장 내에서 포크리프트가 트럭에 올려진 물품을 운반하던 중, 무단으로 이동하여 높은 위치에서… |
| 낙상 | 위험 | 위험 | ✅ | 3.1s | 장면에서 높은 위치에 있는 포크스터가 트럭의 앞부분에 위치한 허공에 떨어져서 넘어지는 모습이 보입니… |
| 낙상 | 위험 | 위험 | ✅ | 2.5s | 장면에서 fork lift가 무게를 견딜 수 없는 상태로 운행하고 있으며, 작업자들이 그 앞에 있는… |
| 없음 | 위험 | 정상 | ❌ | 2.7s | 장소는 공장 내부이며, 작업자들이 안전한 거리에서 움직이고 있으며, 장비와 물건들은 정돈되어 있습니… |
| 낙상 | 위험 | 위험 | ✅ | 2.8s | 화면 왼쪽에서 빨간색 토스터가 운반 중인 상자에 대해 주의가 필요합니다. 이는 위험한 상황이며, 운… |
| 없음 | 정상 | 정상 | ✅ | 2.6s | 캡처된 장면은 지하 주차장 내부이며, 여러 차량이 정지 상태로 보이며, 아무런 위험한 현상이나 불안… |
| 없음 | 정상 | 정상 | ✅ | 2.6s | 화면에는 차량들이 주차된 것으로 보이며, 주변에는 녹색 식물과 조명이 설치되어 있는 것으로 보아 안… |
| 없음 | 정상 | 정상 | ✅ | 2.6s | 화면에는 물이 흐르는 도로와 건물, 차량이 보이며, 아무런 위험한 현상이나 불안정한 상태가 나타나지… |
| 없음 | 정상 | 정상 | ✅ | 2.2s | 눈이 내리는 날, 차량과 인물이 운행 중이며, 주변에는 다른 차량들이 보이고, 모든 객체는 안정적인… |
| 없음 | 정상 | 정상 | ✅ | 1.6s | 화면에는 차량이 주차되고 있으며, 안전한 상태로 보이며, 위험 요소는 없음. |
| 없음 | 정상 | 정상 | ✅ | 3.0s | 화면에는 작업 중인 직원들과 물품이 보이며, 안전 장비와 안전 조치가 이루어지고 있습니다. 주변에는… |
| 없음 | 정상 | 정상 | ✅ | 3.0s | 장면은 공장 내부의 작업 공간으로 보이며, 작업자와 물품이 정상적인 상태로 배치되어 있습니다. 주변… |
| 없음 | 정상 | 정상 | ✅ | 1.9s | 장소는 공장 내부이며, 작업 중인 장비와 인원은 안전하게 운영되고 있으며, 주변에는 위험 요소가 보… |
| 낙상 | 정상 | 위험 | ❌ | 2.6s | 화면에서 높은 위치에 있는 선반들이 무너져 내리는 모습이 보이며, 이는 낙상의 위험을 나타냅니다. … |
| 없음 | 위험 | 정상 | ❌ | 3.3s | CCTV 영상은 상점 내부에서 고객과 직원이 상호작용하는 장면을 보여주며, 주변 환경은 정돈되어 있… |
| 낙상 | 위험 | 위험 | ✅ | 3.4s | 카메라에서 촬영된 장면은 공장 내부의 작업 공간으로 보이며, 한 사람이 작업대 앞에서 무게를 가진 … |
| 없음 | 위험 | 정상 | ❌ | 2.7s | 화면에는 사람과 가정용 건물이 보이며, 주변 환경은 평화롭고 안정적인 상태입니다. 아무런 위험 요소… |
| 낙상 | 위험 | 위험 | ✅ | 3.2s | 사람들이 엘리베이터를 이용하던 중, 한 사람이 엘리베이터에서 떨어져 내려가며 위험한 상황이 발생했습… |
| 낙상 | 위험 | 위험 | ✅ | 3.8s | 엘리베이터가 운행 중인 시점에서 한 사람이 엘리베이터 안으로 빠져나가며, 그 후 다른 사람들은 엘리… |
| 화재 | 위험 | 위험 | ✅ | 3.2s | CCTV 카메라에서 촬영된 장면은 밤에 화재가 발생한 장면을 보여주며, 불꽃과 연기로 인해 주변이 … |
| 화재 | 위험 | 위험 | ✅ | 3.4s | 화재 감지 알림이 표시되어 있으며, 작업자들이 화재 발생 시 즉각적인 대응을 하고 있는 것으로 보임… |
| 없음 | 위험 | 정상 | ❌ | 3.4s | 화면에는 공기 중에 있는 연기와 함께 녹색 나무들이 보이며, 주변에는 건물과 공공장소가 있습니다. … |
| 화재 | 위험 | 위험 | ✅ | 2.6s | 화면에는 검은 연기와 함께 건물들이 보이며, 이는 화재 발생의 시각적 증거입니다. 연기는 건물의 상… |
| 낙상 | 위험 | 위험 | ✅ | 3.3s | 공장의 여러 고층 건물과 탑이 있는 구조물들이 위험한 상태로 보이며, 그 중 일부는 높은 위치에서 … |
| 화재 | 위험 | 위험 | ✅ | 2.4s | 화재 발생 후 연기와 불꽃이 확산되고 있으며, 인원들이 긴급히 떨어져 있는 상황. 화재는 큰 규모로… |
| 화재 | 위험 | 위험 | ✅ | 2.4s | 화재가 발생한 것으로 보이며, 소화기 시스템이 작동하고 있다. 화재는 빠르게 확산되고 있으며, 이는… |
| 화재 | 위험 | 위험 | ✅ | 2.8s | 화재가 발생하여 큰 연기와 불꽃이 나오고 있으며, 주변에는 소방관들이 도착하여 대응하고 있습니다. … |
| 화재 | 위험 | 위험 | ✅ | 2.7s | 화면 오른쪽에서 불꽃이 떨어지고 있으며, 주변의 건물들이 흐릿하게 보이고 있다. 이는 화재 발생의 … |

## 상세 내역 

### Qwen3-VL-2B-Instruct

<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire1.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire1.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 것으로 보이며, 연기와 불꽃이 뚜렷하게 보이고, 인공적인 화재 장비를 사용하는 것으로 보여서 위험한 상황입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire2.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire2.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 카메라에서 촬영된 장면은 밤에 촬영되었으며, 차량 주변에 불꽃과 연기가 발생하고 있는 것을 볼 수 있습니다. 이는 화재의 신호이며, 즉시 대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire3.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire3.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재는 바닥에 있는 흰색 물체가 불을 띠고 있으며, 이는 화재 발생의 신호입니다. 이는 매우 심각한 위험을 초래할 수 있습니다. 즉, 이 장면은 화재 발생의 위험을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire4.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire4.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 건물에서 불꽃과 연기가 뚜렷하게 보이며, 소방관들이 대응하고 있습니다. 이는 매우 심각한 상황이며, 즉시 구조 및 진화 작업이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire5.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire5.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 방 안에서 큰 불꽃이 발생하고 있으며, 주변의 물건들이 떨어질 수 있는 위험성이 존재합니다. 특히, 화재가 확대되고 있음을 확인할 수 있습니다. 이는 즉각적인 구조적 대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire6.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire6.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 장소에서 연기가 퍼지고 있으며, 인원들이 물을 사용하여 대응하고 있습니다. 이는 매우 심각한 상황이며, 즉시 구조 및 안전 조치가 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire7.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire7.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 감지 시스템이 활성화되어 있으며, 여러 개의 화재 경고 표시가 이미지에 나타나고 있다. 이는 작업 중 발생할 수 있는 위험을 나타내며, 즉시 대응이 필요하다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire8.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire8.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 감지 시스템이 작동하며, 화재가 발생한 장소에서 빛나는 불꽃과 연기가 관찰된다. 이는 즉각적인 위험을 나타내며, 인근 사람들의 안전을 위해 즉각적인 대응이 필요하다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover1.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover1.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 장면은 공장 내에서 포크리프트가 트럭에 올려진 물품을 운반하던 중, 무단으로 이동하여 높은 위치에서 떨어졌음을 보여줍니다. 이는 사고 발생의 직접적인 원인으로, 작업자와 주변 환경에 대한 주의가 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover2.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover2.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 장면에서 높은 위치에 있는 포크스터가 트럭의 앞부분에 위치한 허공에 떨어져서 넘어지는 모습이 보입니다. 이는 매우 위험한 상황이며, 사고 발생 가능성이 높습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover3.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover3.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 장면에서 fork lift가 무게를 견딜 수 없는 상태로 운행하고 있으며, 작업자들이 그 앞에 있는 것으로 보아 위험한 상황이 발생하고 있다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover4.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover4.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 장소는 공장 내부이며, 작업자들이 안전한 거리에서 움직이고 있으며, 장비와 물건들은 정돈되어 있습니다. 화재나 낙상 등의 위험 요소가 보이지 않으며, 장비의 작동 상태도 이상이 없습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover5.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover5.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 화면 왼쪽에서 빨간색 토스터가 운반 중인 상자에 대해 주의가 필요합니다. 이는 위험한 상황이며, 운반 중에 떨어질 수 있는 위험이 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking1.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking1.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 캡처된 장면은 지하 주차장 내부이며, 여러 차량이 정지 상태로 보이며, 아무런 위험한 현상이나 불안정한 상태가 관찰되지 않습니다. 주차장 내부는 안정적이고 정상적인 상태입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking2.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking2.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 차량들이 주차된 것으로 보이며, 주변에는 녹색 식물과 조명이 설치되어 있는 것으로 보아 안전한 상태입니다. 다만, CCTV 영상의 품질상 일부 불분명한 부분이 있지만, 현재 상황은 위험 요소가 없습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking3.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking3.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 물이 흐르는 도로와 건물, 차량이 보이며, 아무런 위험한 현상이나 불안정한 상태가 나타나지 않음.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking4.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking4.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 눈이 내리는 날, 차량과 인물이 운행 중이며, 주변에는 다른 차량들이 보이고, 모든 객체는 안정적인 상태로 보이며, 위험 요소가 없습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking5.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking5.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 차량이 주차되고 있으며, 안전한 상태로 보이며, 위험 요소는 없음.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker1.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker1.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 작업 중인 직원들과 물품이 보이며, 안전 장비와 안전 조치가 이루어지고 있습니다. 주변에는 휘발성 가스나 연기 등 위험 요소가 보이지 않으며, 작업 공간은 정돈되어 있고, 모든 직원들은 안전한 상태에서 작업하고 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker2.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker2.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 장면은 공장 내부의 작업 공간으로 보이며, 작업자와 물품이 정상적인 상태로 배치되어 있습니다. 주변에는 택배용 트럭과 수납용 선반 등이 보이며, 작업자들은 안전한 거리에서 작업하고 있습니다. 이는 위험 요소가 없는 것으로 판단됩니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker3.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker3.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 장소는 공장 내부이며, 작업 중인 장비와 인원은 안전하게 운영되고 있으며, 주변에는 위험 요소가 보이지 않습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker_4.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker_4.mp4 · 정답 정상 · 판정 위험(낙상) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 화면에서 높은 위치에 있는 선반들이 무너져 내리는 모습이 보이며, 이는 낙상의 위험을 나타냅니다. 이는 재난 상황으로 간주되어야 하며, 즉시 대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall1.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall1.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> CCTV 영상은 상점 내부에서 고객과 직원이 상호작용하는 장면을 보여주며, 주변 환경은 정돈되어 있으며, 안전한 상태로 보입니다. 다만, 영상의 품질이 낮아 일부 세부 사항이 명확하지 않지만, 전체적으로 위험 요소는 없습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall2.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall2.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 카메라에서 촬영된 장면은 공장 내부의 작업 공간으로 보이며, 한 사람이 작업대 앞에서 무게를 가진 물건을 떨어뜨리고 있는 모습이 보입니다. 이는 낙상의 위험을 나타내며, 작업자의 안전에 대한 우려를 유발합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall3.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall3.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 사람과 가정용 건물이 보이며, 주변 환경은 평화롭고 안정적인 상태입니다. 아무런 위험 요소가 보이지 않으며, 장면은 일반적인 주거 지역의 일상적인 모습을 보여줍니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall4.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall4.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 사람들이 엘리베이터를 이용하던 중, 한 사람이 엘리베이터에서 떨어져 내려가며 위험한 상황이 발생했습니다. 이는 엘리베이터의 안전 기능이 작동하지 않거나, 사용자들이 안전을 무시하고 있는 것으로 보입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall5.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall5.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 엘리베이터가 운행 중인 시점에서 한 사람이 엘리베이터 안으로 빠져나가며, 그 후 다른 사람들은 엘리베이터를 이용하여 내려가고 있다. 이는 엘리베이터 안에서의 안전 문제를 나타내며, 위험한 상황이 발생하고 있다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke1.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke1.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> CCTV 카메라에서 촬영된 장면은 밤에 화재가 발생한 장면을 보여주며, 불꽃과 연기로 인해 주변이 흐릿하게 보입니다. 이는 화재의 심각성을 나타내며, 즉시 대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke2.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke2.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 감지 알림이 표시되어 있으며, 작업자들이 화재 발생 시 즉각적인 대응을 하고 있는 것으로 보임. 그러나 화재가 발생한 상황에서 작업자들이 빠르게 이동하고 있음에도 불구하고, 화재가 발생했음을 확인할 수 있는 정보가 명확하게 제공되지 않음. 따라서 위험은 존재함.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke3.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke3.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 공기 중에 있는 연기와 함께 녹색 나무들이 보이며, 주변에는 건물과 공공장소가 있습니다. 그러나 이 장면에서 화재나 낙상 등의 위험 요소는 보이지 않으며, 현재의 상태는 정상적인 것으로 판단됩니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke4.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke4.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화면에는 검은 연기와 함께 건물들이 보이며, 이는 화재 발생의 시각적 증거입니다. 연기는 건물의 상태를 나타내며, 위험한 상황을 시사합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke5.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke5.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 공장의 여러 고층 건물과 탑이 있는 구조물들이 위험한 상태로 보이며, 그 중 일부는 높은 위치에서 떨어질 수 있는 위험을 나타냅니다. 이는 낙상의 위험을 의미하며, 즉 시청자에게 위험한 상황을 알리는 것이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire1.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire1.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 발생 후 연기와 불꽃이 확산되고 있으며, 인원들이 긴급히 떨어져 있는 상황. 화재는 큰 규모로 진행되고 있어, 즉각적인 대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire2.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire2.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 것으로 보이며, 소화기 시스템이 작동하고 있다. 화재는 빠르게 확산되고 있으며, 이는 위험한 상황이다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire3.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire3.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생하여 큰 연기와 불꽃이 나오고 있으며, 주변에는 소방관들이 도착하여 대응하고 있습니다. 현재의 상황은 매우 위험하며, 즉각적인 구조 및 소방대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire4.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire4.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화면 오른쪽에서 불꽃이 떨어지고 있으며, 주변의 건물들이 흐릿하게 보이고 있다. 이는 화재 발생의 신호이며, 즉시 대응이 필요하다.</div></div></div>
