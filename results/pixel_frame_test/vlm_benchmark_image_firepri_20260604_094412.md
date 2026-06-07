# 엣지 VLM 해석 평가 (firepri)

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
| Qwen3-VL-2B-Instruct | ✅ 7.92s | 94% | 82% | 10% | 2.56s | 30.9 | 5224 MB |

## Qwen3-VL-2B-Instruct — `Qwen/Qwen3-VL-2B-Instruct`

**위험 유형별 인식 (카테고리별 정답률)**

| 카테고리 | 정답유형 | N | 위험판정 | 판정정답률 | 유형정답률 | 미상 |
|---|---|---|---|---|---|---|
| 화재 | 화재 | 6 | 6 | 100% | 100% | 0 |
| 연기 | 화재 | 7 | 6 | 86% | 57% | 0 |
| 사람 쓰러짐/낙상 | 낙상 | 5 | 5 | 100% | 100% | 0 |
| 기계·장비 전도 | 전도 | 6 | 6 | 100% | 100% | 0 |
| 정상 주차장(오탐 테스트) | 없음 | 5 | 0 | 100% | 80% | 0 |
| 정상 작업장(오탐 테스트) | 없음 | 5 | 1 | 80% | 60% | 0 |

**항목별 결과**

| 유형 | 정답 | 판정 | 정오 | 시간 | 해석(앞부분) |
|---|---|---|---|---|---|
| 화재 | 위험 | 위험 | ✅ | 1.7s | 화재 발생 시점에서 연기와 불빛이 보이며, 이는 위험한 상황을 나타냅니다. |
| 화재 | 위험 | 위험 | ✅ | 1.9s | 화재 현장에서 소방관이 불길을 막기 위해 접근하고 있으며, 불꽃과 연기가 뚜렷하게 보이며 위험한 상… |
| 화재 | 위험 | 위험 | ✅ | 1.8s | 화재 현장에서 불꽃과 연기가 매우 강하게 떨어지고 있으며, 한 명의 인물이 화재에 맞서 있는 것으로… |
| 화재 | 위험 | 위험 | ✅ | 2.2s | 화면 왼쪽에서 불꽃과 연기가 뚜렷하게 보이며, 이는 화재 발생의 징후입니다. 현재의 상황에서 위험성… |
| 화재 | 위험 | 위험 | ✅ | 3.0s | 자동차가 불을 뿜고 있으며, 연기와 화염이 확대되고 있다. 이는 매우 심각한 화재 상황이며, 주변 … |
| 화재 | 위험 | 위험 | ✅ | 3.2s | 차량의 앞쪽에서 불꽃과 연기가 발생하고 있으며, 이는 화재의 신호입니다. 차량은 주행 중인 것으로 … |
| 전도 | 위험 | 위험 | ✅ | 1.6s | 기계가 떨어진 상태로 위험한 상황이며, 인근에는 구조대원들이 대응하고 있습니다. |
| 전도 | 위험 | 위험 | ✅ | 2.1s | 트럭이 완전히 바닥에 떨어져 있으며, 기계가 위험한 상태로 보입니다. 이는 사고 발생 후의 장애 상… |
| 전도 | 위험 | 위험 | ✅ | 2.1s | 녹색 토목 기계가 사람을 떨어뜨리고 있는 상황이며, 기계가 사람을 잡고 있는 상태로, 이는 매우 위… |
| 전도 | 위험 | 위험 | ✅ | 2.0s | 기계가 떨어져 있는 상태로, 먼지와 파편이 공중에 떠오르고 있으며, 이는 위험한 상황을 나타냅니다. |
| 전도 | 위험 | 위험 | ✅ | 1.9s | 기계가 무게를 견딜 수 없는 상태로 떨어져 있는 것으로 보이며, 이는 위험한 상황을 초래할 수 있다… |
| 전도 | 위험 | 위험 | ✅ | 1.9s | 기계가 바닥에 떨어져 있는 상태이며, 주변에는 물건들이 떨어진 것으로 보이므로 위험한 상황입니다. |
| 낙상 | 정상 | 정상 | ✅ | 2.1s | 화면 왼쪽에는 한 명의 사람이 있는 것으로 보이며, 그는 주차장에서 걷고 있는 것으로 보입니다. 이… |
| 없음 | 정상 | 정상 | ✅ | 2.4s | 장면은 실내 주차장으로 보이며, 차량들이 정렬되어 있고, 인물이나 기계적 위험 요소는 보이지 않습니… |
| 없음 | 정상 | 정상 | ✅ | 1.9s | 이미지에는 불꽃이나 연기, 화재 관련 특징이 보이지 않으며, 주변에는 차량과 인물이 보이며, 이는 … |
| 없음 | 정상 | 정상 | ✅ | 1.8s | 화면에는 차량이 운행하고 있으며, 주변에는 건물과 녹지가 보이며, 아무런 위험한 현상이나 불안정한 … |
| 없음 | 정상 | 정상 | ✅ | 3.1s | 화면에는 차량들이 주차된 실내 공간이 보이며, 불안정한 상태나 위험한 상황이 나타나는 것이 없습니다… |
| 없음 | 정상 | 정상 | ✅ | 1.9s | 화재나 낙상(사람) 등 위험 요소가 보이지 않으며, 작업 중인 인원들은 안전한 상태로 보이며, 기계… |
| 낙상 | 정상 | 정상 | ✅ | 2.1s | 화재나 낙상(기계) 등의 위험이 보이지 않으며, 인물은 안전한 상태에서 작업하고 있습니다. 다만, … |
| 낙상 | 정상 | 위험 | ❌ | 2.1s | 상단에서 사람의 하체가 보이며, 그 사람은 높은 위치에 서 있는 것으로 보아 위험한 상태입니다. 이… |
| 없음 | 정상 | 정상 | ✅ | 2.3s | 공장 내부의 작업장에서 여러 명의 직원들이 전동 기계를 사용하며 일하고 있으며, 화재나 불꽃, 연기… |
| 없음 | 정상 | 정상 | ✅ | 2.3s | 장면은 재난 현장의 엣지 카메라로 캡처된 것으로, 두 사람이 밀폐된 공간에서 상자들을 운반하는 모습… |
| 낙상 | 위험 | 위험 | ✅ | 2.8s | 작업 중인 기계가 사람에게 위협을 주는 상황이며, 인체가 기계에 부딪혀 넘어진 상태로, 즉 낙상(사… |
| 낙상 | 위험 | 위험 | ✅ | 2.8s | 작업 중인 인원이 무너진 구조물의 빌딩에서 떨어져 넘어졌으며, 다른 인원이 그를 구조하고 있다. 이… |
| 낙상 | 위험 | 위험 | ✅ | 2.9s | 이미지에서 두 명의 인물이 높은 위치에 서 있으며, 한 명은 바닥에 무릎을 꿇고 있는 상태로, 이는… |
| 낙상 | 위험 | 위험 | ✅ | 2.4s | 화면에 보이는 인물이 바닥에 떨어져 있는 상태이며, 이는 낙상(사람)을 의미합니다. 이는 위험한 상… |
| 낙상 | 위험 | 위험 | ✅ | 3.5s | 방 안에 누군가 무릎을 꿇고 바닥에 떨어져 있는 상태이며, 이는 낙상(사람)의 위험을 나타냅니다. … |
| 화재 | 위험 | 위험 | ✅ | 3.2s | 화면에는 연기가 퍼져 있으며, 한 사람이 무릎을 꿇고 있는 상태로, 그 주변에는 박스와 상자들이 놓… |
| 화재 | 위험 | 위험 | ✅ | 1.7s | 화재 발생 시 연기와 불꽃이 보이며, 인원이 빠르게 이동하고 있는 상황으로, 위험한 상태입니다. |
| 화재 | 위험 | 위험 | ✅ | 2.6s | 차량의 앞부분에서 연기가 발생하고 있으며, 이는 화재의 징후로 보입니다. 차량은 주행 중인 상태이며… |
| 없음 | 위험 | 정상 | ❌ | 2.9s | 이미지에는 연기나 불꽃, 화염 등 위험 요소가 보이지 않으며, 장소는 기업 내 저장 공간으로 보이며… |
| 전도 | 위험 | 위험 | ✅ | 2.9s | 이미지에는 항공기와 그 주변에 있는 기계가 보이며, 기계가 연기와 함께 작동하고 있는 것으로 보입니… |
| 화재 | 위험 | 위험 | ✅ | 2.8s | 화재가 발생한 것으로 보이며, 불꽃과 연기가 뚜렷하게 보이고, 인근에는 작업 중인 기계와 사람의 위… |
| 낙상 | 위험 | 위험 | ✅ | 9.0s | 화재가 발생한 것으로 보이며, 인공지능이 판단한 결과는 위험 상태입니다. 이는 화재가 발생한 것으로… |

## 상세 내역 

### Qwen3-VL-2B-Instruct

<div class="capture"><div class="cap-img"><img src="../../dataset/images/fire1.jpg"></div><div class="cap-body"><div class="cap-head">[image] fire1.jpg · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 발생 시점에서 연기와 불빛이 보이며, 이는 위험한 상황을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/fire2.jpg"></div><div class="cap-body"><div class="cap-head">[image] fire2.jpg · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 현장에서 소방관이 불길을 막기 위해 접근하고 있으며, 불꽃과 연기가 뚜렷하게 보이며 위험한 상황임을 알 수 있음.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/fire3.jpg"></div><div class="cap-body"><div class="cap-head">[image] fire3.jpg · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 현장에서 불꽃과 연기가 매우 강하게 떨어지고 있으며, 한 명의 인물이 화재에 맞서 있는 것으로 보여 위험한 상황입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/fire4.jpg"></div><div class="cap-body"><div class="cap-head">[image] fire4.jpg · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화면 왼쪽에서 불꽃과 연기가 뚜렷하게 보이며, 이는 화재 발생의 징후입니다. 현재의 상황에서 위험성이 매우 높습니다. 즉, 화재가 발생한 것으로 판단됩니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/fire5.jpg"></div><div class="cap-body"><div class="cap-head">[image] fire5.jpg · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 자동차가 불을 뿜고 있으며, 연기와 화염이 확대되고 있다. 이는 매우 심각한 화재 상황이며, 주변 사람들은 이를 지켜보고 있는 것으로 보인다. 즉, 화재가 발생하고 있으며, 위험한 상황이다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/fire6.jpg"></div><div class="cap-body"><div class="cap-head">[image] fire6.jpg · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 차량의 앞쪽에서 불꽃과 연기가 발생하고 있으며, 이는 화재의 신호입니다. 차량은 주행 중인 것으로 보이며, 인근에는 사람의 실체가 보이지 않지만, 화재의 위험성이 매우 높습니다. 즉, 이 장면은 화재 상황을 나타내며, 즉시 구조 및 소방 서비스 요청이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/machine_tipover1.webp"></div><div class="cap-body"><div class="cap-head">[image] machine_tipover1.webp · 정답 위험 · 판정 위험(전도) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(기계)  <br><span class="cap-label">설명</span> 기계가 떨어진 상태로 위험한 상황이며, 인근에는 구조대원들이 대응하고 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/machine_tipover2.jpg"></div><div class="cap-body"><div class="cap-head">[image] machine_tipover2.jpg · 정답 위험 · 판정 위험(전도) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(기계)  <br><span class="cap-label">설명</span> 트럭이 완전히 바닥에 떨어져 있으며, 기계가 위험한 상태로 보입니다. 이는 사고 발생 후의 장애 상태이며, 즉시 구조 작업이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/machine_tipover3.jpg"></div><div class="cap-body"><div class="cap-head">[image] machine_tipover3.jpg · 정답 위험 · 판정 위험(전도) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(기계)  <br><span class="cap-label">설명</span> 녹색 토목 기계가 사람을 떨어뜨리고 있는 상황이며, 기계가 사람을 잡고 있는 상태로, 이는 매우 위험한 상황입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/machine_tipover4.jpg"></div><div class="cap-body"><div class="cap-head">[image] machine_tipover4.jpg · 정답 위험 · 판정 위험(전도) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(기계)  <br><span class="cap-label">설명</span> 기계가 떨어져 있는 상태로, 먼지와 파편이 공중에 떠오르고 있으며, 이는 위험한 상황을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/machine_tipover5.jpg"></div><div class="cap-body"><div class="cap-head">[image] machine_tipover5.jpg · 정답 위험 · 판정 위험(전도) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(기계)  <br><span class="cap-label">설명</span> 기계가 무게를 견딜 수 없는 상태로 떨어져 있는 것으로 보이며, 이는 위험한 상황을 초래할 수 있다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/machine_tipover6.jpg"></div><div class="cap-body"><div class="cap-head">[image] machine_tipover6.jpg · 정답 위험 · 판정 위험(전도) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(기계)  <br><span class="cap-label">설명</span> 기계가 바닥에 떨어져 있는 상태이며, 주변에는 물건들이 떨어진 것으로 보이므로 위험한 상황입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_parking1.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_parking1.jpg · 정답 정상 · 판정 정상(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> 화면 왼쪽에는 한 명의 사람이 있는 것으로 보이며, 그는 주차장에서 걷고 있는 것으로 보입니다. 이는 일반적인 상황이며, 위험 요소가 없습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_parking2.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_parking2.jpg · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 장면은 실내 주차장으로 보이며, 차량들이 정렬되어 있고, 인물이나 기계적 위험 요소는 보이지 않습니다. 조명은 전반적으로 안정적이며, 불안정한 상태나 위험한 동작이 나타나는 것이 없습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_parking3.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_parking3.jpg · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 이미지에는 불꽃이나 연기, 화재 관련 특징이 보이지 않으며, 주변에는 차량과 인물이 보이며, 이는 일반적인 정상적인 장면을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_parking4.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_parking4.jpg · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 차량이 운행하고 있으며, 주변에는 건물과 녹지가 보이며, 아무런 위험한 현상이나 불안정한 상태가 보이지 않습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_parking5.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_parking5.jpg · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 차량들이 주차된 실내 공간이 보이며, 불안정한 상태나 위험한 상황이 나타나는 것이 없습니다. 주변에는 연기, 불꽃, 화염 등이 보이지 않으며, 사람이나 기계가 위험한 상황을 일으키고 있는 것도 확인되지 않습니다. 따라서 이 장면은 정상적인 상태입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_worker1.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_worker1.jpg · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화재나 낙상(사람) 등 위험 요소가 보이지 않으며, 작업 중인 인원들은 안전한 상태로 보이며, 기계는 정상 작동하고 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_worker2.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_worker2.jpg · 정답 정상 · 판정 정상(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> 화재나 낙상(기계) 등의 위험이 보이지 않으며, 인물은 안전한 상태에서 작업하고 있습니다. 다만, 작업 중인 사람의 위치는 주의가 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_worker3.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_worker3.jpg · 정답 정상 · 판정 위험(낙상) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> 상단에서 사람의 하체가 보이며, 그 사람은 높은 위치에 서 있는 것으로 보아 위험한 상태입니다. 이는 낙상(사람)의 위험을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_worker4.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_worker4.jpg · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 공장 내부의 작업장에서 여러 명의 직원들이 전동 기계를 사용하며 일하고 있으며, 화재나 불꽃, 연기 등 위험한 상황이 보이지 않습니다. 장비와 인원 모두 안전하게 작동하고 있는 것으로 보입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_worker5.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_worker5.jpg · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 장면은 재난 현장의 엣지 카메라로 캡처된 것으로, 두 사람이 밀폐된 공간에서 상자들을 운반하는 모습이 보입니다. 이는 일반적인 작업 환경이며, 위험 요소가 없습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/person_fall1.jpg"></div><div class="cap-body"><div class="cap-head">[image] person_fall1.jpg · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> 작업 중인 기계가 사람에게 위협을 주는 상황이며, 인체가 기계에 부딪혀 넘어진 상태로, 즉 낙상(사람)의 위험이 존재합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/person_fall2.webp"></div><div class="cap-body"><div class="cap-head">[image] person_fall2.webp · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> 작업 중인 인원이 무너진 구조물의 빌딩에서 떨어져 넘어졌으며, 다른 인원이 그를 구조하고 있다. 이는 매우 심각한 위험 상황이며, 즉, 사람의 생명이 위험에 처해 있다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/person_fall3.jpg"></div><div class="cap-body"><div class="cap-head">[image] person_fall3.jpg · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> 이미지에서 두 명의 인물이 높은 위치에 서 있으며, 한 명은 바닥에 무릎을 꿇고 있는 상태로, 이는 낙상(사람)의 상황을 나타냅니다. 이는 즉각적인 위험을 초래할 수 있으므로 위험을 판단합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/person_fall4.jpg"></div><div class="cap-body"><div class="cap-head">[image] person_fall4.jpg · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> 화면에 보이는 인물이 바닥에 떨어져 있는 상태이며, 이는 낙상(사람)을 의미합니다. 이는 위험한 상황으로 판단됩니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/person_fall5.jpg"></div><div class="cap-body"><div class="cap-head">[image] person_fall5.jpg · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> 방 안에 누군가 무릎을 꿇고 바닥에 떨어져 있는 상태이며, 이는 낙상(사람)의 위험을 나타냅니다. 이는 즉각적인 위험을 초래할 수 있으며, 즉각적인 조치가 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/smoke1.jpg"></div><div class="cap-body"><div class="cap-head">[image] smoke1.jpg · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화면에는 연기가 퍼져 있으며, 한 사람이 무릎을 꿇고 있는 상태로, 그 주변에는 박스와 상자들이 놓여 있다. 이는 화재 발생 후의 상황을 나타내며, 위험한 상황임을 알 수 있다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/smoke2.jpg"></div><div class="cap-body"><div class="cap-head">[image] smoke2.jpg · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 발생 시 연기와 불꽃이 보이며, 인원이 빠르게 이동하고 있는 상황으로, 위험한 상태입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/smoke3.jpg"></div><div class="cap-body"><div class="cap-head">[image] smoke3.jpg · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 차량의 앞부분에서 연기가 발생하고 있으며, 이는 화재의 징후로 보입니다. 차량은 주행 중인 상태이며, 주변에는 병원 차량 등이 보이지만, 현재는 인명피해가 발생하지 않아 위험은 존재합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/smoke4.jpg"></div><div class="cap-body"><div class="cap-head">[image] smoke4.jpg · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 이미지에는 연기나 불꽃, 화염 등 위험 요소가 보이지 않으며, 장소는 기업 내 저장 공간으로 보이며, 인물이나 기계의 이상한 동작도 관찰되지 않습니다. 따라서 위험은 없습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/smoke5.jpg"></div><div class="cap-body"><div class="cap-head">[image] smoke5.jpg · 정답 위험 · 판정 위험(전도) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(기계)  <br><span class="cap-label">설명</span> 이미지에는 항공기와 그 주변에 있는 기계가 보이며, 기계가 연기와 함께 작동하고 있는 것으로 보입니다. 이는 낙상(기계)의 위험을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/smoke_fire1.jpg"></div><div class="cap-body"><div class="cap-head">[image] smoke_fire1.jpg · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 것으로 보이며, 불꽃과 연기가 뚜렷하게 보이고, 인근에는 작업 중인 기계와 사람의 위치가 확인된다. 이는 매우 심각한 위험을 초래할 수 있으므로 즉각적인 대응이 필요하다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/smoke_fire2.jpg"></div><div class="cap-body"><div class="cap-head">[image] smoke_fire2.jpg · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> 화재가 발생한 것으로 보이며, 인공지능이 판단한 결과는 위험 상태입니다. 이는 화재가 발생한 것으로 보이며, 인공지능이 판단한 결과는 위험 상태입니다. 이는 화재가 발생한 것으로 보이며, 인공지능이 판단한 결과는 위험 상태입니다. 이는 화재가 발생한 것으로 보이며, 인공지능이 판단한 결과는 위험 상태입니다. 이는 화재가 발생한 것으로 보이며, 인공지능이 판단한 결과는 위험 상태입니다. 이는 화재가 발생한 것으로 보이며, 인공지능이 판단한 결과는 위험 상태입니다. 이는 화재가 발생한 것으로 보이며, 인공지능이 판단한 결과는 위험 상태입니다. 이는 화재가 발생한 것으로 보이며, 인공지능이 판단한 결과는 위험 상태입니다. 이는 화재가 발생한 것으로 보이며, 인공지능이 판단한 결과는 위험 상태입니다. 이는 화재가 발생한 것으로 보이며, 인공지능이 판단한 결과는 위험 상태입니다. 이는 화재가 발생한 것으로 보이며, 인공지능이 판단한 결과는 위험 상태입니다. 이는 화재가 발생한 것으로 보이며, 인공지능</div></div></div>
