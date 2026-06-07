# 엣지 VLM 해석 평가 (v_base)

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
| Qwen3-VL-2B-Instruct | ✅ 7.83s | 83% | 72% | 11% | 2.51s | 30.8 | 4403 MB |

## Qwen3-VL-2B-Instruct — `Qwen/Qwen3-VL-2B-Instruct`

**위험 유형별 인식 (카테고리별 정답률)**

| 카테고리 | 정답유형 | N | 위험판정 | 판정정답률 | 유형정답률 | 미상 |
|---|---|---|---|---|---|---|
| 화재 | 화재 | 8 | 8 | 100% | 100% | 0 |
| 연기 | 화재 | 9 | 8 | 89% | 78% | 0 |
| 사람 쓰러짐/낙상 | 낙상 | 5 | 3 | 60% | 60% | 0 |
| 기계·장비 전도 | 전도 | 5 | 3 | 60% | 0% | 0 |
| 정상 주차장(오탐 테스트) | 없음 | 5 | 0 | 100% | 100% | 0 |
| 정상 작업장(오탐 테스트) | 없음 | 4 | 1 | 75% | 75% | 0 |

**항목별 결과**

| 유형 | 정답 | 판정 | 정오 | 시간 | 해석(앞부분) |
|---|---|---|---|---|---|
| 화재 | 위험 | 위험 | ✅ | 2.3s | 화재가 발생한 것으로 보이며, 연기와 불꽃이 시야에 나타나고 있으며, 인근에는 소방관이 있는 것으로… |
| 화재 | 위험 | 위험 | ✅ | 2.6s | 카메라가 촬영된 장면은 밤에 촬영되었으며, 차량이 주차된 도로에서 불꽃이 떨어지는 모습이 보입니다.… |
| 화재 | 위험 | 위험 | ✅ | 2.2s | 실내에서 불꽃이 발생하여 주변이 붉게 빛나고 있으며, 이는 화재의 신호를 나타냅니다. 현재의 상황은… |
| 화재 | 위험 | 위험 | ✅ | 1.8s | 화재가 발생한 건물에서 불꽃과 연기가 뚜렷하게 보이며, 소방관들이 활동하고 있어 위험한 상황이 발생… |
| 화재 | 위험 | 위험 | ✅ | 1.9s | 방 안에서 불이 발생하고 있으며, 여러 물건이 연기와 함께 떨어지고 있다. 이는 매우 위험한 상황이… |
| 화재 | 위험 | 위험 | ✅ | 2.2s | 화재가 발생한 장소에서 연기가 떠오르고 있으며, 인원이 빠져나가는 모습이 보이며, 이는 매우 심각한… |
| 화재 | 위험 | 위험 | ✅ | 2.6s | 화재 감지 시스템이 활성화되어 있으며, 화재 발생 위치에서 빛나는 불꽃과 함께 빨간색 표시가 나타나… |
| 화재 | 위험 | 위험 | ✅ | 3.0s | 화재 감지 시스템이 활성화되어 있으며, 실내에서 불꽃과 연기가 발생하고 있습니다. 이는 즉각적인 위… |
| 낙상 | 위험 | 위험 | ✅ | 4.3s | 장면에서 forklift가 트럭의 앞부분에 위치하고 있으며, 트럭이 운행 중인 상태에서 forkli… |
| 낙상 | 위험 | 위험 | ✅ | 1.8s | 장면에서 포크로 운반 중인 트럭이 바닥에 떨어져 있는 것을 볼 수 있으며, 이는 낙상의 위험을 나타… |
| 낙상 | 위험 | 위험 | ✅ | 2.7s | 장면에서 fork lift가 무게를 견딜 수 없는 상태로 운행하고 있으며, 작업자들이 그 앞에 서 … |
| 없음 | 위험 | 정상 | ❌ | 2.6s | 장소는 공장 내부이며, 작업자들이 안전한 거리에서 움직이고 있으며, 장비와 물건들은 정돈되어 있습니… |
| 없음 | 위험 | 정상 | ❌ | 1.8s | 장면은 창고 내부에서 작업 중인 것으로 보이며, 인물과 장비가 안전하게 움직이고 있으며, 위험 요소… |
| 없음 | 정상 | 정상 | ✅ | 1.9s | 차량들이 정비된 상태이며, 주변에는 특별한 위험 요소가 보이지 않으며, CCTV 영상에서의 움직임은… |
| 없음 | 정상 | 정상 | ✅ | 2.5s | 화면에는 차량들이 주차된 것으로 보이며, 주변에는 녹색 식물과 조명이 설치되어 있는 것으로 보아 안… |
| 없음 | 정상 | 정상 | ✅ | 2.0s | 화면에는 물이 흘러 있는 지대와 건물, 차량 등이 보이며, 아무런 위험한 현상이나 불안정한 상태가 … |
| 없음 | 정상 | 정상 | ✅ | 2.1s | 눈이 내리는 날, 차량과 인물이 안전하게 움직이고 있으며, 주변에는 다른 차량들이 정지되어 있는 것… |
| 없음 | 정상 | 정상 | ✅ | 2.1s | 차량들이 정지 상태로 주차되어 있으며, 주변에는 특별한 위험 요소나 불안정한 상태가 보이지 않으며,… |
| 없음 | 정상 | 정상 | ✅ | 2.3s | 화면에는 작업 중인 직원들과 물품이 보이며, 안전 장비를 착용하고 있는 것으로 보아 작업 중인 상태… |
| 없음 | 정상 | 정상 | ✅ | 2.9s | 장면은 공장 내부의 작업 공간으로 보이며, 작업자와 물품이 정상적인 상태로 배치되어 있습니다. 주변… |
| 없음 | 정상 | 정상 | ✅ | 2.2s | 공장 내부는 정돈되어 있으며, 작업 중인 장비와 인원이 안전하게 운영되고 있습니다. 주변에는 물리적… |
| 낙상 | 정상 | 위험 | ❌ | 2.2s | 화면에서 빠르게 움직이는 장면으로 인해, 바닥에 무너진 물건들과 함께 파손된 선반들이 보이며, 이는… |
| 없음 | 위험 | 정상 | ❌ | 2.5s | CCTV 영상에서 상점 내부의 고객과 직원이 상호작용하고 있으며, 주변에는 일반적인 상점 장비와 제… |
| 낙상 | 위험 | 위험 | ✅ | 2.9s | CCTV 영상에서 한 남성이 작업 중에 무언가를 떨어뜨리거나 넘어져 있는 모습이 보이며, 그의 움직… |
| 없음 | 위험 | 정상 | ❌ | 3.1s | 화면에는 사람과 가정용 건물이 보이며, 주변 환경은 평화롭고 안정적인 상태입니다. 아무런 위험 요소… |
| 낙상 | 위험 | 위험 | ✅ | 3.6s | 엘리베이터 안에서 두 사람이 함께 타고 있으며, 그 중 한 명이 엘리베이터를 내려가려는 동작을 취하… |
| 낙상 | 위험 | 위험 | ✅ | 3.4s | 엘리베이터가 운행 중인 시점에서 한 사람이 엘리베이터 안으로 빠져나가며, 그 후 다른 사람들이 엘리… |
| 화재 | 위험 | 위험 | ✅ | 2.5s | 화재가 발생한 것으로 보이며, 연기와 불꽃이 관찰되며, 소방대원들이 현장을 점검하고 있다. 이는 매… |
| 화재 | 위험 | 위험 | ✅ | 2.1s | 화재 감지 알림이 표시되어 있으며, 작업자들이 화재 발생 장소에 접근하고 있는 것으로 보아 위험한 … |
| 없음 | 위험 | 정상 | ❌ | 3.3s | 화면에는 공기 중에 있는 연기와 함께 녹색 나무들이 보이며, 주변에는 건물과 공공 시설이 있습니다.… |
| 화재 | 위험 | 위험 | ✅ | 1.8s | 건물 사이에서 검은 연기와 함께 폭발이 발생하여 위험한 상황이 발생하고 있으며, 이는 화재의 가능성… |
| 낙상 | 위험 | 위험 | ✅ | 2.4s | 공장의 여러 탱크와 연기 배출 시스템이 보이며, 연기의 방향과 높이에서 낙하 위험이 존재함. 이는 … |
| 화재 | 위험 | 위험 | ✅ | 2.5s | 화재 발생 현상이 보이며, 연기와 불꽃이 뚜렷하게 나타나고 있으며, 주변의 물체가 파손되고 있다. … |
| 화재 | 위험 | 위험 | ✅ | 2.9s | CCTV 영상에서 화재가 발생한 후, 스프링클러 시스템이 작동하여 불을 진압하는 모습이 보이며, 화… |
| 화재 | 위험 | 위험 | ✅ | 2.7s | 화재가 발생한 것으로 보이며, 건물이 �il이되고 있으며, 연기와 불꽃이 뚜렷하게 보입니다. 이는 … |
| 화재 | 위험 | 위험 | ✅ | 2.6s | 화면 중앙에서 빛나는 불꽃이 발생하고 있으며, 주변의 건물과 인프라가 피해를 입고 있는 것으로 보임… |

## 상세 내역 

### Qwen3-VL-2B-Instruct

<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire1.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire1.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 것으로 보이며, 연기와 불꽃이 시야에 나타나고 있으며, 인근에는 소방관이 있는 것으로 보아 즉각적인 대응이 필요하다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire2.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire2.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 카메라가 촬영된 장면은 밤에 촬영되었으며, 차량이 주차된 도로에서 불꽃이 떨어지는 모습이 보입니다. 이는 화재 발생의 가능성을 시사하며, 즉시 대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire3.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire3.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 실내에서 불꽃이 발생하여 주변이 붉게 빛나고 있으며, 이는 화재의 신호를 나타냅니다. 현재의 상황은 매우 위험하며, 즉시 구조대가 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire4.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire4.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 건물에서 불꽃과 연기가 뚜렷하게 보이며, 소방관들이 활동하고 있어 위험한 상황이 발생하고 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire5.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire5.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 방 안에서 불이 발생하고 있으며, 여러 물건이 연기와 함께 떨어지고 있다. 이는 매우 위험한 상황이며, 즉시 구조적 대응이 필요하다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire6.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire6.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 장소에서 연기가 떠오르고 있으며, 인원이 빠져나가는 모습이 보이며, 이는 매우 심각한 위험 상황을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire7.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire7.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 감지 시스템이 활성화되어 있으며, 화재 발생 위치에서 빛나는 불꽃과 함께 빨간색 표시가 나타나고 있다. 이는 즉각적인 안전 대응이 필요하다는 것을 의미한다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire8.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire8.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 감지 시스템이 활성화되어 있으며, 실내에서 불꽃과 연기가 발생하고 있습니다. 이는 즉각적인 위험을 나타내며, 주변에 있는 사람들의 안전을 위협하고 있습니다. 즉시 구조대와 소방서의 개입이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover1.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover1.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 장면에서 forklift가 트럭의 앞부분에 위치하고 있으며, 트럭이 운행 중인 상태에서 forklift가 트럭의 앞부분에 위치하고 있는 것으로 보아, 운전자가 forklift를 사용하여 트럭을 운반하는 과정에서 위험한 상황이 발생할 수 있습니다. 이는 forklift가 트럭의 앞부분에 위치하고 있는 것이므로, 운전자가 forklift를 사용하여 트럭을 운반하는 과정에서 위험한 상황이 발생할 수 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover2.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover2.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 장면에서 포크로 운반 중인 트럭이 바닥에 떨어져 있는 것을 볼 수 있으며, 이는 낙상의 위험을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover3.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover3.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 장면에서 fork lift가 무게를 견딜 수 없는 상태로 운행하고 있으며, 작업자들이 그 앞에 서 있는 것으로 보아, 작업자가 fork lift의 위험한 상태에서 떨어질 가능성이 있습니다. 이는 낙상 위험을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover4.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover4.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 장소는 공장 내부이며, 작업자들이 안전한 거리에서 움직이고 있으며, 장비와 물건들은 정돈되어 있습니다. 화재나 낙상 등의 위험 요소가 보이지 않으며, 현재 상황은 안전하게 유지되고 있는 것으로 보입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover5.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover5.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 장면은 창고 내부에서 작업 중인 것으로 보이며, 인물과 장비가 안전하게 움직이고 있으며, 위험 요소는 보이지 않습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking1.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking1.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 차량들이 정비된 상태이며, 주변에는 특별한 위험 요소가 보이지 않으며, CCTV 영상에서의 움직임은 정상적인 운행을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking2.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking2.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 차량들이 주차된 것으로 보이며, 주변에는 녹색 식물과 조명이 설치되어 있는 것으로 보아 안전한 상태입니다. 다만, CCTV 영상의 품질상 일부 불분명한 부분이 있지만, 현재 상황은 위험 요소가 없습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking3.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking3.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 물이 흘러 있는 지대와 건물, 차량 등이 보이며, 아무런 위험한 현상이나 불안정한 상태가 나타나지 않았습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking4.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking4.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 눈이 내리는 날, 차량과 인물이 안전하게 움직이고 있으며, 주변에는 다른 차량들이 정지되어 있는 것으로 보이며, 현재는 위험한 상황이 아님을 알 수 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking5.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking5.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 차량들이 정지 상태로 주차되어 있으며, 주변에는 특별한 위험 요소나 불안정한 상태가 보이지 않으며, CCTV 영상에서의 움직임은 정상적인 운행을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker1.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker1.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 작업 중인 직원들과 물품이 보이며, 안전 장비를 착용하고 있는 것으로 보아 작업 중인 상태입니다. 주변에는 휘발성 가스나 연기 등 위험 요소가 없는 것으로 보입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker2.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker2.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 장면은 공장 내부의 작업 공간으로 보이며, 작업자와 물품이 정상적인 상태로 배치되어 있습니다. 주변에는 휘발성 가스나 연기 등 위험 요소가 보이지 않으며, 안전 장비나 경보 시스템도 작동 중 보이지 않습니다. 따라서 위험 요소는 없습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker3.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker3.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 공장 내부는 정돈되어 있으며, 작업 중인 장비와 인원이 안전하게 운영되고 있습니다. 주변에는 물리적 위험 요소가 보이지 않으며, 전기 및 화재 관련 위험도 없어 보입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker_4.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker_4.mp4 · 정답 정상 · 판정 위험(낙상) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 화면에서 빠르게 움직이는 장면으로 인해, 바닥에 무너진 물건들과 함께 파손된 선반들이 보이며, 이는 낙상의 위험을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall1.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall1.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> CCTV 영상에서 상점 내부의 고객과 직원이 상호작용하고 있으며, 주변에는 일반적인 상점 장비와 제품이 보입니다. 영상은 정상적인 상점 운영 환경을 나타내며, 위험 요소는 보이지 않습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall2.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall2.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> CCTV 영상에서 한 남성이 작업 중에 무언가를 떨어뜨리거나 넘어져 있는 모습이 보이며, 그의 움직임이 안정적이지 않아 위험한 상황을 나타냅니다. 이는 낙상의 위험을 의미하며, 즉시 조치가 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall3.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall3.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 사람과 가정용 건물이 보이며, 주변 환경은 평화롭고 안정적인 상태입니다. 아무런 위험 요소가 보이지 않으며, 장면은 일반적인 주거 지역의 일상적인 모습을 보여줍니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall4.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall4.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 엘리베이터 안에서 두 사람이 함께 타고 있으며, 그 중 한 명이 엘리베이터를 내려가려는 동작을 취하고 있다. 이는 낙상의 위험을 나타내며, 엘리베이터의 안정성과 사용자들의 안전을 고려해야 할 상황이다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall5.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall5.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 엘리베이터가 운행 중인 시점에서 한 사람이 엘리베이터 안으로 빠져나가며, 그 후 다른 사람들이 엘리베이터를 이용하는 동안, 엘리베이터가 떨어지는 것을 보여줍니다. 이는 낙상의 위험이 존재하며, 즉시 조치가 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke1.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke1.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 것으로 보이며, 연기와 불꽃이 관찰되며, 소방대원들이 현장을 점검하고 있다. 이는 매우 심각한 상황으로, 즉시 대응이 필요하다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke2.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke2.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 감지 알림이 표시되어 있으며, 작업자들이 화재 발생 장소에 접근하고 있는 것으로 보아 위험한 상황이 발생하고 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke3.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke3.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 공기 중에 있는 연기와 함께 녹색 나무들이 보이며, 주변에는 건물과 공공 시설이 있습니다. 이는 자연적인 환경 변화나 기후 변화의 영향을 받은 것으로 보이며, 현재의 상태에서 위험 요소가 존재하지 않습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke4.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke4.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 건물 사이에서 검은 연기와 함께 폭발이 발생하여 위험한 상황이 발생하고 있으며, 이는 화재의 가능성을 시사합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke5.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke5.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 공장의 여러 탱크와 연기 배출 시스템이 보이며, 연기의 방향과 높이에서 낙하 위험이 존재함. 이는 화재 발생 가능성과 관련된 위험 요소로 판단됨.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire1.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire1.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 발생 현상이 보이며, 연기와 불꽃이 뚜렷하게 나타나고 있으며, 주변의 물체가 파손되고 있다. 이는 매우 심각한 위험을 나타내며, 즉시 대응이 필요하다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire2.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire2.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> CCTV 영상에서 화재가 발생한 후, 스프링클러 시스템이 작동하여 불을 진압하는 모습이 보이며, 화재가 지속되고 있는 것으로 보임. 화재는 빠르게 확산되고 있으며, 방화벽이나 다른 안전 장비가 필요하지 않음.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire3.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire3.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 것으로 보이며, 건물이 �il이되고 있으며, 연기와 불꽃이 뚜렷하게 보입니다. 이는 매우 심각한 위험을 나타내며, 즉시 구조대의 개입이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire4.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire4.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화면 중앙에서 빛나는 불꽃이 발생하고 있으며, 주변의 건물과 인프라가 피해를 입고 있는 것으로 보임. 이는 매우 심각한 화재 상황을 나타내며, 즉시 구조대와 소방대의 개입이 필요함.</div></div></div>
