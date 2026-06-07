# 엣지 VLM 해석 평가 (v_f4)

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
| Qwen3-VL-2B-Instruct | ✅ 8.21s | 75% | 67% | 11% | 2.51s | 32.1 | 4242 MB |

## Qwen3-VL-2B-Instruct — `Qwen/Qwen3-VL-2B-Instruct`

**위험 유형별 인식 (카테고리별 정답률)**

| 카테고리 | 정답유형 | N | 위험판정 | 판정정답률 | 유형정답률 | 미상 |
|---|---|---|---|---|---|---|
| 화재 | 화재 | 8 | 7 | 88% | 88% | 0 |
| 연기 | 화재 | 9 | 9 | 100% | 89% | 0 |
| 사람 쓰러짐/낙상 | 낙상 | 5 | 1 | 20% | 20% | 0 |
| 기계·장비 전도 | 전도 | 5 | 2 | 40% | 0% | 0 |
| 정상 주차장(오탐 테스트) | 없음 | 5 | 0 | 100% | 100% | 0 |
| 정상 작업장(오탐 테스트) | 없음 | 4 | 1 | 75% | 75% | 0 |

**항목별 결과**

| 유형 | 정답 | 판정 | 정오 | 시간 | 해석(앞부분) |
|---|---|---|---|---|---|
| 화재 | 위험 | 위험 | ✅ | 3.1s | 화재가 발생한 것으로 보이며, 연기와 불꽃이 뚜렷하게 보이고, 인근에는 소방관이 대응하고 있습니다.… |
| 화재 | 위험 | 위험 | ✅ | 3.4s | 화재 발생 현상이 보이며, 주변에는 불꽃과 연기가 존재하고, 카메라가 촬영한 장면에서 빛이 흐르는 … |
| 없음 | 위험 | 정상 | ❌ | 1.9s | 실내 환경에서 높은 밝기와 자연광이 잘 들어오며, 안전한 상태로 보이며, 아무런 위험 요소가 보이지… |
| 화재 | 위험 | 위험 | ✅ | 1.6s | 화재가 발생한 집 앞에서 소방관들이 대응하고 있으며, 불꽃과 연기로 인해 위험한 상황이 발생하고 있… |
| 화재 | 위험 | 위험 | ✅ | 2.3s | 방 안에서 큰 불꽃이 발생하여 주변 물건들이 연기와 함께 떨어지고 있으며, 화재 위험은 매우 높음.… |
| 화재 | 위험 | 위험 | ✅ | 2.0s | 화재 발생 시 인원들이 물을 사용하여 대응하고 있으며, 연기와 함께 큰 폭발이 발생한 것으로 보이며… |
| 화재 | 위험 | 위험 | ✅ | 2.5s | 화재 감지 시스템이 활성화되어 있으며, 작업자와 주변 장비가 위험한 상태로 인식되고 있습니다. 이는… |
| 화재 | 위험 | 위험 | ✅ | 2.3s | 화재가 발생한 것으로 보이며, 빛이 떨어지는 상태로 인해 위험한 상황이 발생하고 있습니다. 즉, 현… |
| 낙상 | 위험 | 위험 | ✅ | 2.9s | 장면에서 forklift가 트럭 옆에 위치하고 있으며, 그 뒤로 트럭이 움직이기 시작하는 순간, f… |
| 없음 | 위험 | 정상 | ❌ | 2.3s | 장면은 물류센터 내부에서 운반 중인 대형 트럭과 포장된 녹색 봉투가 있는 자동차를 보여주며, 작업자… |
| 낙상 | 위험 | 위험 | ✅ | 2.5s | 터널 안에서 작업 중인 인물이 무게를 견딜 수 없는 상태로 떨어져서 위험한 상황이 발생하고 있으며,… |
| 없음 | 위험 | 정상 | ❌ | 2.9s | 장소는 공장 내부이며, 인물은 이동하고 있으며, 주변에는 물건과 기계가 보입니다. 그러나 현재 장면… |
| 없음 | 위험 | 정상 | ❌ | 2.3s | 화면에는 포장된 상자들이 정돈되어 있으며, 작업 중인 기계는 안정적인 상태로 작동하고 있습니다. 주… |
| 없음 | 정상 | 정상 | ✅ | 2.6s | 차량이 주차된 공간 내에서 이동하고 있는 것으로 보이며, 주변에는 다른 차량이 정지되어 있으며, 불… |
| 없음 | 정상 | 정상 | ✅ | 2.3s | 현재 장면은 밤에 촬영된 것으로, 주변에는 차량들이 정지되어 있으며, 주변 환경은 안정적입니다. C… |
| 없음 | 정상 | 정상 | ✅ | 2.5s | 현재 장면은 비가 내리는 날씨에서 촬영되었으며, 건물과 주차장, 그리고 녹색 지대 등이 보입니다. … |
| 없음 | 정상 | 정상 | ✅ | 2.7s | 눈이 내리는 날의 공공장소에서 차량과 인사가 있는 장면이며, 주변에는 정상적인 운행과 안전 상태를 … |
| 없음 | 정상 | 정상 | ✅ | 1.7s | 차량들이 정비된 상태이며, 주차장 내부는 안전한 상태로 보이며, 특별한 위험 요소나 불안정한 구조물… |
| 없음 | 정상 | 정상 | ✅ | 1.8s | 작업 중인 직원들은 안전한 자세를 취하고 있으며, 주변에는 물건이 잘 정돈되어 있고, 전기 및 화재… |
| 없음 | 정상 | 정상 | ✅ | 1.5s | 장면은 공장 내부의 작업 공간으로 보이며, 물리적 위험 요소는 없으며, 모든 객체는 정상적인 상태로… |
| 없음 | 정상 | 정상 | ✅ | 3.4s | 재난 현장의 엣지 카메라로 캡처된 장면은 공장 내 저장실 내부를 보여주며, 여러 개의 높은 선반과 … |
| 낙상 | 정상 | 위험 | ❌ | 2.8s | 화면에서 높은 위치에 있는 창고의 상단에 녹색 잔디와 나무가 떨어져 있는 것을 볼 수 있으며, 이는… |
| 없음 | 위험 | 정상 | ❌ | 2.9s | CCTV 영상에서 보이는 장면은 상점 내부의 일반적인 상황을 보여주며, 고객과 직원이 상품을 확인하… |
| 없음 | 위험 | 정상 | ❌ | 3.0s | 카메라에서 촬영된 장면은 공장 내부의 작업 공간으로 보이며, 작업자들이 안전한 상태에서 작업하고 있… |
| 없음 | 위험 | 정상 | ❌ | 2.0s | 화면에는 사람과 가구가 보이며, 주변 환경은 평화롭고 정상적인 상태입니다. 다만, 카메라가 캡처한 … |
| 낙상 | 위험 | 위험 | ✅ | 3.0s | 엣지 카메라에서 촬영된 장면에서 여성 한 명이 승강기에서 떨어져 내려가고 있으며, 그녀는 안전한 위… |
| 없음 | 위험 | 정상 | ❌ | 2.8s | 엣지 카메라로 캡처된 장면은 지하철역 내에서 사람들이 엘리베이터와 계단을 이용해 이동하는 모습을 보… |
| 낙상 | 위험 | 위험 | ✅ | 3.3s | CCTV 영상에서 빛이 떨어지는 듯한 불규칙한 빛이 나타나며, 이는 빛이 떨어진 상태로 보이며, 주… |
| 화재 | 위험 | 위험 | ✅ | 2.4s | 화재 감지 알림이 표시되어 있으며, 인물이 무릎을 꿇고 있는 상태로, 주변 환경이 불안정해 보이며,… |
| 화재 | 위험 | 위험 | ✅ | 2.6s | 화면에 보이는 녹색 숲의 일부가 연기로 가득 차 있으며, 이는 화재 발생의 징후로 보입니다. 연기는… |
| 화재 | 위험 | 위험 | ✅ | 2.3s | 화면에서 검은 연기와 함께 건물이 파괴되고 있으며, 이는 화재 발생의 시각적 증거입니다. 현재의 상… |
| 화재 | 위험 | 위험 | ✅ | 2.1s | 공장 내에서 연기와 불꽃이 발생하고 있으며, 여러 탱크와 시스템이 불안정한 상태로 보임. 이는 화재… |
| 화재 | 위험 | 위험 | ✅ | 2.1s | 화재 발생 현상이 나타나고 있으며, 폭발적인 소리와 연기, 그리고 불꽃이 관찰됩니다. 이는 매우 심… |
| 화재 | 위험 | 위험 | ✅ | 3.2s | CCTV 영상에서 연기와 불꽃이 발생하고 있으며, 화재가 확산되고 있는 상태임을 알 수 있음. 화재… |
| 화재 | 위험 | 위험 | ✅ | 2.7s | 화재 발생 현장에서 연기와 불꽃이 뚜렷하게 보이며, 주변 환경이 매우 위험한 상태로 보임. 즉, 현… |
| 화재 | 위험 | 위험 | ✅ | 2.8s | 화면 중앙에서 빨간색 불꽃이 발생하며, 주변의 건물과 테이블이 빛나고 있으며, 이는 화재의 신호를 … |

## 상세 내역 

### Qwen3-VL-2B-Instruct

<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire1.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire1.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 것으로 보이며, 연기와 불꽃이 뚜렷하게 보이고, 인근에는 소방관이 대응하고 있습니다. 이는 매우 심각한 상황이며, 즉시 구조 및 진화 조치가 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire2.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire2.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 발생 현상이 보이며, 주변에는 불꽃과 연기가 존재하고, 카메라가 촬영한 장면에서 빛이 흐르는 상태로 보임. 이는 매우 심각한 위험을 나타내며, 즉시 구조대와 소방대의 개입이 필요함.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire3.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire3.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 실내 환경에서 높은 밝기와 자연광이 잘 들어오며, 안전한 상태로 보이며, 아무런 위험 요소가 보이지 않습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire4.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire4.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 집 앞에서 소방관들이 대응하고 있으며, 불꽃과 연기로 인해 위험한 상황이 발생하고 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire5.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire5.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 방 안에서 큰 불꽃이 발생하여 주변 물건들이 연기와 함께 떨어지고 있으며, 화재 위험은 매우 높음. 즉, 현재 상황은 매우 위험하며, 즉시 구조 및 소화 작업이 필요함.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire6.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire6.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 발생 시 인원들이 물을 사용하여 대응하고 있으며, 연기와 함께 큰 폭발이 발생한 것으로 보이며, 위험한 상황이 발생하고 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire7.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire7.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 감지 시스템이 활성화되어 있으며, 작업자와 주변 장비가 위험한 상태로 인식되고 있습니다. 이는 화재 발생의 신호를 나타내며, 즉시 대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire8.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire8.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 것으로 보이며, 빛이 떨어지는 상태로 인해 위험한 상황이 발생하고 있습니다. 즉, 현재의 상황에서 위험한 상태입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover1.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover1.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 장면에서 forklift가 트럭 옆에 위치하고 있으며, 그 뒤로 트럭이 움직이기 시작하는 순간, forklift가 트럭의 앞부분에 부딪히는 사고가 발생합니다. 이는 작업 중의 안전 위험을 나타내며, 즉시 조치가 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover2.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover2.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 장면은 물류센터 내부에서 운반 중인 대형 트럭과 포장된 녹색 봉투가 있는 자동차를 보여주며, 작업자들이 안전하게 운반하고 있는 것으로 보이며, 위험 요소는 없습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover3.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover3.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 터널 안에서 작업 중인 인물이 무게를 견딜 수 없는 상태로 떨어져서 위험한 상황이 발생하고 있으며, 이는 작업자의 안전을 위협하는 사고임을 나타냄.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover4.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover4.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 장소는 공장 내부이며, 인물은 이동하고 있으며, 주변에는 물건과 기계가 보입니다. 그러나 현재 장면에서 위험 요소는 보이지 않으며, 화재나 낙상 등의 위험도 없으며, 전도도 확인되지 않습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover5.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover5.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 포장된 상자들이 정돈되어 있으며, 작업 중인 기계는 안정적인 상태로 작동하고 있습니다. 주변에는 인력이 없는 상태이며, 위험 요소가 보이지 않습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking1.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking1.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 차량이 주차된 공간 내에서 이동하고 있는 것으로 보이며, 주변에는 다른 차량이 정지되어 있으며, 불안정한 상태나 이상적인 사고가 발생하지 않았습니다. 주변 환경은 안정적이고, 조명 및 구조물은 모두 정상적으로 유지되고 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking2.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking2.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 현재 장면은 밤에 촬영된 것으로, 주변에는 차량들이 정지되어 있으며, 주변 환경은 안정적입니다. CCTV 카메라가 촬영된 영상에서 오류나 이상한 현상이 나타나지 않았습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking3.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking3.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 현재 장면은 비가 내리는 날씨에서 촬영되었으며, 건물과 주차장, 그리고 녹색 지대 등이 보입니다. 다만, 화재나 낙상, 전도 등의 위험 요소는 보이지 않으며, 장면은 일반적인 정상 상태입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking4.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking4.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 눈이 내리는 날의 공공장소에서 차량과 인사가 있는 장면이며, 주변에는 정상적인 운행과 안전 상태를 유지하고 있는 것으로 보입니다. 다만, 눈이 내리는 상황에서 차량이 정지하고 있는 것은 있지만, 이는 일반적인 정상적인 상황으로 간주됩니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking5.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking5.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 차량들이 정비된 상태이며, 주차장 내부는 안전한 상태로 보이며, 특별한 위험 요소나 불안정한 구조물은 보이지 않습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker1.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker1.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 작업 중인 직원들은 안전한 자세를 취하고 있으며, 주변에는 물건이 잘 정돈되어 있고, 전기 및 화재 관련 위험 요소는 보이지 않습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker2.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker2.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 장면은 공장 내부의 작업 공간으로 보이며, 물리적 위험 요소는 없으며, 모든 객체는 정상적인 상태로 보입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker3.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker3.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 재난 현장의 엣지 카메라로 캡처된 장면은 공장 내 저장실 내부를 보여주며, 여러 개의 높은 선반과 기계가 설치되어 있으며, 작업 중인 인원과 장비가 보입니다. 그러나 현재의 장면에서 화재, 낙상, 전도 등의 위험 요소는 보이지 않으며, 장비와 인원의 위치는 안전한 상태로 보입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker_4.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker_4.mp4 · 정답 정상 · 판정 위험(낙상) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 화면에서 높은 위치에 있는 창고의 상단에 녹색 잔디와 나무가 떨어져 있는 것을 볼 수 있으며, 이는 낙상의 위험을 나타냅니다. 이는 재난 상황에서 즉각적인 위험을 발생할 수 있는 상태이며, 즉각적인 조치가 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall1.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall1.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> CCTV 영상에서 보이는 장면은 상점 내부의 일반적인 상황을 보여주며, 고객과 직원이 상품을 확인하고 결제하는 과정이 진행되고 있습니다. 주변에는 물건들이 진열되어 있으며, 안전 장비나 위험 요소는 보이지 않습니다. 이는 정상적인 상점 운영 상황을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall2.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall2.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 카메라에서 촬영된 장면은 공장 내부의 작업 공간으로 보이며, 작업자들이 안전한 상태에서 작업하고 있는 것으로 보입니다. 주변에는 물건이나 장비가 정돈되어 있으며, 불안정한 상태나 위험한 물리적 요소는 보이지 않습니다. 따라서 이 장면은 위험 요소가 없는 정상적인 상태입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall3.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall3.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 사람과 가구가 보이며, 주변 환경은 평화롭고 정상적인 상태입니다. 다만, 카메라가 캡처한 장면에서 특정 위험 요소는 보이지 않습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall4.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall4.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> 엣지 카메라에서 촬영된 장면에서 여성 한 명이 승강기에서 떨어져 내려가고 있으며, 그녀는 안전한 위치에 도달하지 못하고 있음을 확인할 수 있습니다. 이는 매우 심각한 위험 상황을 나타냅니다. 즉, 이는 낙상의 위험을 의미합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall5.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall5.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 엣지 카메라로 캡처된 장면은 지하철역 내에서 사람들이 엘리베이터와 계단을 이용해 이동하는 모습을 보여주고 있으며, 모든 사람들은 안전하게 이동하고 있는 것으로 보이며, 화재나 낙상 등의 위험 요소가 존재하지 않습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke1.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke1.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상  <br><span class="cap-label">설명</span> CCTV 영상에서 빛이 떨어지는 듯한 불규칙한 빛이 나타나며, 이는 빛이 떨어진 상태로 보이며, 주변 환경이 불안정해 보입니다. 또한, 빛이 떨어지는 방향으로 물체가 움직이고 있는 것으로 보여, 낙상의 위험이 존재합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke2.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke2.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 감지 알림이 표시되어 있으며, 인물이 무릎을 꿇고 있는 상태로, 주변 환경이 불안정해 보이며, 이는 화재 발생의 신호를 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke3.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke3.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화면에 보이는 녹색 숲의 일부가 연기로 가득 차 있으며, 이는 화재 발생의 징후로 보입니다. 연기는 공기 중에 확산되고 있어, 즉시 대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke4.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke4.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화면에서 검은 연기와 함께 건물이 파괴되고 있으며, 이는 화재 발생의 시각적 증거입니다. 현재의 상황은 매우 위험하며, 즉각적인 구조적 대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke5.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke5.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 공장 내에서 연기와 불꽃이 발생하고 있으며, 여러 탱크와 시스템이 불안정한 상태로 보임. 이는 화재의 위험을 나타내며, 즉시 대응이 필요함.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire1.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire1.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 발생 현상이 나타나고 있으며, 폭발적인 소리와 연기, 그리고 불꽃이 관찰됩니다. 이는 매우 심각한 위험을 의미하며, 즉각적인 대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire2.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire2.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> CCTV 영상에서 연기와 불꽃이 발생하고 있으며, 화재가 확산되고 있는 상태임을 알 수 있음. 화재가 지속될 경우 인명 피해 및 재산 손실의 위험성이 존재함. 즉, 화재가 현재 진행 중이며, 즉시 소화 및 안전 조치가 필요함.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire3.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire3.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 발생 현장에서 연기와 불꽃이 뚜렷하게 보이며, 주변 환경이 매우 위험한 상태로 보임. 즉, 현재 상황은 매우 위험하며, 즉시 구조 및 소방대응이 필요함.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire4.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire4.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화면 중앙에서 빨간색 불꽃이 발생하며, 주변의 건물과 테이블이 빛나고 있으며, 이는 화재의 신호를 나타냅니다. 현재의 상황은 매우 위험하며, 즉시 구조대와 소방대의 개입이 필요합니다.</div></div></div>
