# 엣지 VLM 해석 평가 (naksubj)

## 데이터셋 구성 (위험 3종 + 정상)

| 카테고리 | 정답 | 위험유형 | 이미지 |
|---|---|---|---|
| 화재 (`fire`) | 위험 | 화재 | 6 |
| 연기 (`smoke`) | 위험 | 화재 | 7 |
| 사람 쓰러짐/낙상 (`person_fall`) | 위험 | 낙상 | 5 |
| 기계·장비 전도 (`machine_tipover`) | 위험 | 전도 | 6 |
| 정상 주차장(오탐 테스트) (`normal_parking`) | 정상 | 없음 | 5 |
| 정상 작업장(오탐 테스트) (`normal_worker`) | 정상 | 없음 | 5 |

## 모델 종합 비교

| 모델 | 로드 | 상황인식 정확도 | 유형 정확도 | 과잉해석(오탐) | 평균 지연 | tok/s | peak VRAM |
|---|---|---|---|---|---|---|---|
| Qwen3-VL-2B-Instruct | ✅ 7.68s | 91% | 74% | 10% | 2.73s | 30.3 | 5193 MB |

## Qwen3-VL-2B-Instruct — `Qwen/Qwen3-VL-2B-Instruct`

**위험 유형별 인식 (카테고리별 정답률)**

| 카테고리 | 정답유형 | N | 위험판정 | 판정정답률 | 유형정답률 | 미상 |
|---|---|---|---|---|---|---|
| 화재 | 화재 | 6 | 6 | 100% | 83% | 0 |
| 연기 | 화재 | 7 | 5 | 71% | 29% | 0 |
| 사람 쓰러짐/낙상 | 낙상 | 5 | 5 | 100% | 100% | 0 |
| 기계·장비 전도 | 전도 | 6 | 6 | 100% | 100% | 0 |
| 정상 주차장(오탐 테스트) | 없음 | 5 | 0 | 100% | 80% | 0 |
| 정상 작업장(오탐 테스트) | 없음 | 5 | 1 | 80% | 60% | 0 |

**항목별 결과**

| 유형 | 정답 | 판정 | 정오 | 시간 | 해석(앞부분) |
|---|---|---|---|---|---|
| 전도 | 위험 | 위험 | ✅ | 5.1s | 캡처된 이미지에는 여러 개의 종류의 박스가 높게 쌓여 있으며, 그 뒤쪽에는 연기가 피어오르고 있는 … |
| 화재 | 위험 | 위험 | ✅ | 3.8s | 화재가 발생한 것으로 보이며, 소방관이 화재 현장을 진입하고 있는 상황이다. 화재는 매우 심각하며,… |
| 화재 | 위험 | 위험 | ✅ | 1.8s | 화재 현장에서 소방관이 대응하고 있으며, 빛이 강하게 떨어지는 상태로 인해 위험한 상황이 발생하고 … |
| 화재 | 위험 | 위험 | ✅ | 3.0s | 화면 왼쪽에서 강한 불꽃과 빛이 나오며, 주변은 붉은색으로 변해 있어 화재가 발생한 것으로 보입니다… |
| 화재 | 위험 | 위험 | ✅ | 2.3s | 자동차가 불꽃으로 끼워져 있으며, 주변에는 사람들이 모여 있는 것으로 보아 위험한 상황이 발생하고 … |
| 화재 | 위험 | 위험 | ✅ | 2.9s | 차량의 앞쪽 바퀴 주변에서 빛나는 불과 흐르는 연기가 보이며, 이는 화재 발생 상황을 나타냅니다. … |
| 전도 | 위험 | 위험 | ✅ | 2.0s | 기계가 떨어진 상태로, 작업자들이 그 주변에서 안전하게 대응하고 있으며, 이는 위험한 상황을 나타냅… |
| 전도 | 위험 | 위험 | ✅ | 2.2s | 트럭이 완전히 바닥에 떨어져 있으며, 기계가 위험한 상태로 보입니다. 이는 사고 발생 후의 장애 상… |
| 전도 | 위험 | 위험 | ✅ | 1.8s | 녹색 토목 기계가 사람을 위협하는 상태로 떨어지고 있으며, 기계가 사람에게 위협적인 상태로 작동하고… |
| 전도 | 위험 | 위험 | ✅ | 2.0s | 기계가 떨어져 흔들리는 상태이며, 주변에는 사람들이 있는 것으로 보아 위험한 상황이 발생하고 있다. |
| 전도 | 위험 | 위험 | ✅ | 2.1s | 기계가 무게를 견딜 수 없는 상태로, 물리적 충격으로 인해 떨어질 가능성이 있음. |
| 전도 | 위험 | 위험 | ✅ | 2.2s | 기계가 바닥에 떨어져 있는 상태이며, 주변에는 물건들이 떨어진 것으로 보이며, 이는 위험한 상황을 … |
| 낙상 | 정상 | 정상 | ✅ | 2.4s | 화면 왼쪽 하단에서 한 사람이 걷고 있으며, 그는 주변의 차량과 비교해도 이상한 행동을 보이지 않는… |
| 없음 | 정상 | 정상 | ✅ | 1.8s | 이미지에는 차량이 정지해 있는 것으로 보이며, 인물이나 기계적 위험 요소는 보이지 않으며, 전반적인… |
| 없음 | 정상 | 정상 | ✅ | 2.3s | 화면에는 차량들이 정지된 상태이며, 인물이나 기계가 위험한 상황을 나타내는 것은 없습니다. 주변 환… |
| 없음 | 정상 | 정상 | ✅ | 1.6s | 화면에는 차량이 운행하고 있으며, 주차장과 도로가 보이며, 현재는 아무런 위험 요소가 없음을 확인할… |
| 없음 | 정상 | 정상 | ✅ | 2.0s | 화면에는 차량들이 정지된 상태로 주차되어 있으며, 인공지능 기반의 CCTV 시스템에서 촬영된 것으로… |
| 없음 | 정상 | 정상 | ✅ | 1.7s | 화면에는 작업 중인 직원들과 물품, 기계 등이 보이며, 모든 사람이 안전한 상태로 작업하고 있으며,… |
| 낙상 | 정상 | 정상 | ✅ | 2.7s | 화면에 보이는 객체는 작업 중인 사람과 기계, 물품 등이 포함되어 있으며, 이들은 모두 정상적인 상… |
| 낙상 | 정상 | 위험 | ❌ | 2.4s | 상단에서 사람의 발이 바닥을 벗어나는 듯한 움직임이 보이며, 그 사람이 높은 위치에서 위험한 상태로… |
| 없음 | 정상 | 정상 | ✅ | 1.7s | 작업 중인 직원들이 안전한 상태이며, 기계와 인력 모두 이상이 없으며, 화재나 낙상 등의 위험 요소… |
| 없음 | 정상 | 정상 | ✅ | 3.4s | 화면에는 두 사람이 바구니에 올려진 상자들을 운반하는 장면이 보이며, 이는 일반적인 물류 작업의 일… |
| 낙상 | 위험 | 위험 | ✅ | 2.0s | 작업자 한 명이 기계 앞에 넘어져 있는 상태이며, 이는 작업 중 발생한 사고로 보이며, 즉시 구조적… |
| 낙상 | 위험 | 위험 | ✅ | 2.2s | 작업 중인 인물이 무릎을 꿇고 넘어진 상태이며, 다른 인물이 그를 지원하고 있다. 이는 높은 위험을… |
| 낙상 | 위험 | 위험 | ✅ | 2.0s | 이미지에서 한 사람이 바닥에 넘어져 있는 상태이며, 이는 명확한 위험을 의미합니다. 이는 빠른 조치… |
| 낙상 | 위험 | 위험 | ✅ | 2.9s | 화면에 보이는 인물이 바닥에 떨어져 있는 상태이며, 이는 낙상(사람)을 의미합니다. 이는 즉각적인 … |
| 낙상 | 위험 | 위험 | ✅ | 3.1s | 화면 중앙에서 남자가 바닥에 떨어져 있는 상태이며, 그의 몸이 바닥에 닿아 있는 것으로 보아 낙상 … |
| 낙상 | 위험 | 위험 | ✅ | 3.2s | 화면 중앙에서 흐르는 연기와 함께 한 사람이 무릎을 꿇고 있는 모습이 보이며, 그 주변에는 박스가 … |
| 낙상 | 위험 | 위험 | ✅ | 2.9s | 화면 중앙에서 한 사람이 큰 파편이나 물질을 떨어뜨린 것으로 보이며, 그 주변에는 흐릿한 연기와 함… |
| 화재 | 위험 | 위험 | ✅ | 3.3s | 차량의 앞부분에서 밀집된 연기와 함께 빛이 흐르는 상태로, 차량이 불이 나는 것으로 보이며, 이는 … |
| 없음 | 위험 | 정상 | ❌ | 3.4s | 화면에는 작업장 내부의 저장 공간이 보이며, 빛이 들어오는 창문과 함께 여러 개의 박스가 정돈되어 … |
| 없음 | 위험 | 정상 | ❌ | 2.3s | 이미지에는 기체가 있는 항공기와 그 주변에 위치한 작업 장비가 보이며, 화재나 낙상 관련 오류나 위… |
| 화재 | 위험 | 위험 | ✅ | 10.0s | 화재가 발생한 것으로 보이며, 빛이 흐르는 상태로 인해 위험한 상황이 발생하고 있다. 즉, 화재가 … |
| 낙상 | 위험 | 위험 | ✅ | 2.2s | 화면 중앙에 사람이 바닥에 누워 있으며, 주변에는 높은 수준의 박스와 선반들이 존재하고, 그 사이에… |

## 상세 내역 

### Qwen3-VL-2B-Instruct

<div class="capture"><div class="cap-img"><img src="../../dataset/images/fire1.jpg"></div><div class="cap-body"><div class="cap-head">[image] fire1.jpg · 정답 위험 · 판정 위험(전도) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(기계)  <br><span class="cap-label">설명</span> 캡처된 이미지에는 여러 개의 종류의 박스가 높게 쌓여 있으며, 그 뒤쪽에는 연기가 피어오르고 있는 것으로 보이며, 이는 폭발이나 화재의 가능성을 의미합니다. 이는 기계적 낙상의 위험을 나타내며, 즉, 박스들이 무너질 수 있는 상태로 보입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/fire2.jpg"></div><div class="cap-body"><div class="cap-head">[image] fire2.jpg · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 것으로 보이며, 소방관이 화재 현장을 진입하고 있는 상황이다. 화재는 매우 심각하며, 주변은 붉은 빛으로 가득 차 있고, 소방관은 안전을 위해 방향을 확인하고 있다. 이는 매우 위험한 상황이며, 즉시 구조 및 소방 작전이 필요하다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/fire3.jpg"></div><div class="cap-body"><div class="cap-head">[image] fire3.jpg · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 현장에서 소방관이 대응하고 있으며, 빛이 강하게 떨어지는 상태로 인해 위험한 상황이 발생하고 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/fire4.jpg"></div><div class="cap-body"><div class="cap-head">[image] fire4.jpg · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화면 왼쪽에서 강한 불꽃과 빛이 나오며, 주변은 붉은색으로 변해 있어 화재가 발생한 것으로 보입니다. 이는 매우 심각한 위험을 나타냅니다. 즉, 화재가 발생하고 있으며, 즉각적인 대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/fire5.jpg"></div><div class="cap-body"><div class="cap-head">[image] fire5.jpg · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 자동차가 불꽃으로 끼워져 있으며, 주변에는 사람들이 모여 있는 것으로 보아 위험한 상황이 발생하고 있다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/fire6.jpg"></div><div class="cap-body"><div class="cap-head">[image] fire6.jpg · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 차량의 앞쪽 바퀴 주변에서 빛나는 불과 흐르는 연기가 보이며, 이는 화재 발생 상황을 나타냅니다. 차량은 안전한 상태가 아님을 알 수 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/machine_tipover1.webp"></div><div class="cap-body"><div class="cap-head">[image] machine_tipover1.webp · 정답 위험 · 판정 위험(전도) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(기계)  <br><span class="cap-label">설명</span> 기계가 떨어진 상태로, 작업자들이 그 주변에서 안전하게 대응하고 있으며, 이는 위험한 상황을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/machine_tipover2.jpg"></div><div class="cap-body"><div class="cap-head">[image] machine_tipover2.jpg · 정답 위험 · 판정 위험(전도) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(기계)  <br><span class="cap-label">설명</span> 트럭이 완전히 바닥에 떨어져 있으며, 기계가 위험한 상태로 보입니다. 이는 사고 발생 후의 장애 상태이며, 즉시 구조 작업이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/machine_tipover3.jpg"></div><div class="cap-body"><div class="cap-head">[image] machine_tipover3.jpg · 정답 위험 · 판정 위험(전도) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(기계)  <br><span class="cap-label">설명</span> 녹색 토목 기계가 사람을 위협하는 상태로 떨어지고 있으며, 기계가 사람에게 위협적인 상태로 작동하고 있다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/machine_tipover4.jpg"></div><div class="cap-body"><div class="cap-head">[image] machine_tipover4.jpg · 정답 위험 · 판정 위험(전도) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(기계)  <br><span class="cap-label">설명</span> 기계가 떨어져 흔들리는 상태이며, 주변에는 사람들이 있는 것으로 보아 위험한 상황이 발생하고 있다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/machine_tipover5.jpg"></div><div class="cap-body"><div class="cap-head">[image] machine_tipover5.jpg · 정답 위험 · 판정 위험(전도) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(기계)  <br><span class="cap-label">설명</span> 기계가 무게를 견딜 수 없는 상태로, 물리적 충격으로 인해 떨어질 가능성이 있음.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/machine_tipover6.jpg"></div><div class="cap-body"><div class="cap-head">[image] machine_tipover6.jpg · 정답 위험 · 판정 위험(전도) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(기계)  <br><span class="cap-label">설명</span> 기계가 바닥에 떨어져 있는 상태이며, 주변에는 물건들이 떨어진 것으로 보이며, 이는 위험한 상황을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_parking1.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_parking1.jpg · 정답 정상 · 판정 정상(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> 화면 왼쪽 하단에서 한 사람이 걷고 있으며, 그는 주변의 차량과 비교해도 이상한 행동을 보이지 않는다. 이는 일반적인 정상적인 상황이며, 위험 요소는 존재하지 않음.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_parking2.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_parking2.jpg · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 이미지에는 차량이 정지해 있는 것으로 보이며, 인물이나 기계적 위험 요소는 보이지 않으며, 전반적인 상태가 정상적인 것으로 보입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_parking3.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_parking3.jpg · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 차량들이 정지된 상태이며, 인물이나 기계가 위험한 상황을 나타내는 것은 없습니다. 주변 환경은 안전하게 유지되고 있으며, 조명과 배경은 일반적인 밤 시간의 모습을 보여줍니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_parking4.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_parking4.jpg · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 차량이 운행하고 있으며, 주차장과 도로가 보이며, 현재는 아무런 위험 요소가 없음을 확인할 수 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_parking5.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_parking5.jpg · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 차량들이 정지된 상태로 주차되어 있으며, 인공지능 기반의 CCTV 시스템에서 촬영된 것으로 보이며, 현재는 아무런 위험 요소가 나타나 있지 않습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_worker1.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_worker1.jpg · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 작업 중인 직원들과 물품, 기계 등이 보이며, 모든 사람이 안전한 상태로 작업하고 있으며, 위험 요소는 보이지 않습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_worker2.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_worker2.jpg · 정답 정상 · 판정 정상(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> 화면에 보이는 객체는 작업 중인 사람과 기계, 물품 등이 포함되어 있으며, 이들은 모두 정상적인 상태를 유지하고 있습니다. 다만, 작업 중인 사람의 위치가 특정한 위험 요소를 포함하지 않으며, 현재의 상황에서 위험 요소는 존재하지 않습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_worker3.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_worker3.jpg · 정답 정상 · 판정 위험(낙상) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> 상단에서 사람의 발이 바닥을 벗어나는 듯한 움직임이 보이며, 그 사람이 높은 위치에서 위험한 상태로 보입니다. 이는 낙상(사람)의 위험을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_worker4.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_worker4.jpg · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 작업 중인 직원들이 안전한 상태이며, 기계와 인력 모두 이상이 없으며, 화재나 낙상 등의 위험 요소가 보이지 않음.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_worker5.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_worker5.jpg · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 두 사람이 바구니에 올려진 상자들을 운반하는 장면이 보이며, 이는 일반적인 물류 작업의 일환으로 보입니다. 주변에는 다른 상자와 바구니들이 배치되어 있으며, 사람들은 안전한 거리에서 움직이고 있습니다. 이는 위험 요소가 없는 정상적인 작업 환경을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/person_fall1.jpg"></div><div class="cap-body"><div class="cap-head">[image] person_fall1.jpg · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> 작업자 한 명이 기계 앞에 넘어져 있는 상태이며, 이는 작업 중 발생한 사고로 보이며, 즉시 구조적 조치가 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/person_fall2.webp"></div><div class="cap-body"><div class="cap-head">[image] person_fall2.webp · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> 작업 중인 인물이 무릎을 꿇고 넘어진 상태이며, 다른 인물이 그를 지원하고 있다. 이는 높은 위험을 의미하며, 즉시 구조적 안전 조치가 필요하다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/person_fall3.jpg"></div><div class="cap-body"><div class="cap-head">[image] person_fall3.jpg · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> 이미지에서 한 사람이 바닥에 넘어져 있는 상태이며, 이는 명확한 위험을 의미합니다. 이는 빠른 조치가 필요하며, 즉시 안전을 확보해야 합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/person_fall4.jpg"></div><div class="cap-body"><div class="cap-head">[image] person_fall4.jpg · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> 화면에 보이는 인물이 바닥에 떨어져 있는 상태이며, 이는 낙상(사람)을 의미합니다. 이는 즉각적인 위험을 초래할 수 있으며, 즉각적인 조치가 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/person_fall5.jpg"></div><div class="cap-body"><div class="cap-head">[image] person_fall5.jpg · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> 화면 중앙에서 남자가 바닥에 떨어져 있는 상태이며, 그의 몸이 바닥에 닿아 있는 것으로 보아 낙상 상태임을 알 수 있음. 이는 위험한 상황으로 판단됨.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/smoke1.jpg"></div><div class="cap-body"><div class="cap-head">[image] smoke1.jpg · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> 화면 중앙에서 흐르는 연기와 함께 한 사람이 무릎을 꿇고 있는 모습이 보이며, 그 주변에는 박스가 높게 쌓여 있다. 이는 인공위험의 가능성을 나타내며, 현재의 상황에서 위험한 상태임을 알 수 있다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/smoke2.jpg"></div><div class="cap-body"><div class="cap-head">[image] smoke2.jpg · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> 화면 중앙에서 한 사람이 큰 파편이나 물질을 떨어뜨린 것으로 보이며, 그 주변에는 흐릿한 연기와 함께 큰 파편이 떨어져 있는 모습이 보입니다. 이는 매우 위험한 상황이며, 즉시 구조대가 대응해야 할 상황입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/smoke3.jpg"></div><div class="cap-body"><div class="cap-head">[image] smoke3.jpg · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 차량의 앞부분에서 밀집된 연기와 함께 빛이 흐르는 상태로, 차량이 불이 나는 것으로 보이며, 이는 매우 심각한 위험을 나타냅니다. 즉, 차량이 화재 상태에 있으며, 즉시 구조대가 대응해야 합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/smoke4.jpg"></div><div class="cap-body"><div class="cap-head">[image] smoke4.jpg · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 작업장 내부의 저장 공간이 보이며, 빛이 들어오는 창문과 함께 여러 개의 박스가 정돈되어 있습니다. 이는 일반적인 물류 또는 저장 공간의 모습이며, 화재나 사람의 낙상 등 위험 요소가 나타나 있지 않습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/smoke5.jpg"></div><div class="cap-body"><div class="cap-head">[image] smoke5.jpg · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 이미지에는 기체가 있는 항공기와 그 주변에 위치한 작업 장비가 보이며, 화재나 낙상 관련 오류나 위험 요소는 보이지 않습니다. 전체적인 상태는 정상적입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/smoke_fire1.jpg"></div><div class="cap-body"><div class="cap-head">[image] smoke_fire1.jpg · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 것으로 보이며, 빛이 흐르는 상태로 인해 위험한 상황이 발생하고 있다. 즉, 화재가 발생한 것으로 보이며, 빛이 흐르는 상태로 인해 위험한 상황이 발생하고 있다. 즉, 화재가 발생한 것으로 보이며, 빛이 흐르는 상태로 인해 위험한 상황이 발생하고 있다. 즉, 화재가 발생한 것으로 보이며, 빛이 흐르는 상태로 인해 위험한 상황이 발생하고 있다. 즉, 화재가 발생한 것으로 보이며, 빛이 흐르는 상태로 인해 위험한 상황이 발생하고 있다. 즉, 화재가 발생한 것으로 보이며, 빛이 흐르는 상태로 인해 위험한 상황이 발생하고 있다. 즉, 화재가 발생한 것으로 보이며, 빛이 흐르는 상태로 인해 위험한 상황이 발생하고 있다. 즉, 화재가 발생한 것으로 보이며, 빛이 흐르는 상태로 인해 위험한 상황이 발생하고 있다. 즉, 화재가 발생한 것으로 보이며, 빛이 흐르는 상태로 인해 위</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/smoke_fire2.jpg"></div><div class="cap-body"><div class="cap-head">[image] smoke_fire2.jpg · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> 화면 중앙에 사람이 바닥에 누워 있으며, 주변에는 높은 수준의 박스와 선반들이 존재하고, 그 사이에서 불꽃이 발생한 것으로 보이며, 이는 위험한 상황을 나타냅니다.</div></div></div>
