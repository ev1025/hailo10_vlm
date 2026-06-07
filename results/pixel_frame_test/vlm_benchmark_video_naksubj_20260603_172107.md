# 엣지 VLM 해석 평가 (naksubj)

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
| Qwen3-VL-2B-Instruct | ✅ 7.68s | 86% | 89% | 11% | 3.62s | 21.9 | 5193 MB |

## Qwen3-VL-2B-Instruct — `Qwen/Qwen3-VL-2B-Instruct`

**위험 유형별 인식 (카테고리별 정답률)**

| 카테고리 | 정답유형 | N | 위험판정 | 판정정답률 | 유형정답률 | 미상 |
|---|---|---|---|---|---|---|
| 화재 | 화재 | 8 | 8 | 100% | 100% | 0 |
| 연기 | 화재 | 9 | 8 | 89% | 89% | 0 |
| 사람 쓰러짐/낙상 | 낙상 | 5 | 3 | 60% | 100% | 0 |
| 기계·장비 전도 | 전도 | 5 | 4 | 80% | 80% | 0 |
| 정상 주차장(오탐 테스트) | 없음 | 5 | 0 | 100% | 80% | 0 |
| 정상 작업장(오탐 테스트) | 없음 | 4 | 1 | 75% | 75% | 0 |

**항목별 결과**

| 유형 | 정답 | 판정 | 정오 | 시간 | 해석(앞부분) |
|---|---|---|---|---|---|
| 화재 | 위험 | 위험 | ✅ | 4.3s | 화재가 발생한 것으로 보이며, 소방관이 화재를 진압하는 모습이 보입니다. 화재는 매우 강하게 빛나고… |
| 화재 | 위험 | 위험 | ✅ | 3.8s | 카메라가 촬영된 장면에서 밤에 주차된 차량 옆에서 불꽃과 연기가 떠오르며, 이는 화재 발생의 징후로… |
| 화재 | 위험 | 위험 | ✅ | 2.8s | 화재는 카페트 위에서 발생한 것으로 보이며, 주변에는 빛이 흐르고 있다. 이는 화재가 발생했음을 시… |
| 화재 | 위험 | 위험 | ✅ | 2.7s | 화재가 발생한 건물에서 소방관들이 활동하고 있으며, 불꽃과 연기가 뚜렷하게 보이며, 위험한 상황이 … |
| 화재 | 위험 | 위험 | ✅ | 3.1s | 방 안에서 불이 발생하고 있으며, 화재는 벽에 있는 빨간색 표지판과 함께 진행되고 있습니다. 이는 … |
| 화재 | 위험 | 위험 | ✅ | 3.1s | 화재가 발생한 장소에서 빠르게 소화되는 모습이 보이며, 인원들이 물을 사용하여 대응하고 있다. 이는… |
| 화재 | 위험 | 위험 | ✅ | 3.1s | 화재 감지 시스템이 활성화되어 있으며, 화재 발생 위치가 여러 곳에 나타나고 있다. 이는 빠른 대응… |
| 화재 | 위험 | 위험 | ✅ | 2.8s | 화재 감지 시스템이 작동하여 화재가 발생한 것을 확인하고, 인원들이 즉시 대응하여 화재를 진압하고 … |
| 전도 | 위험 | 위험 | ✅ | 5.4s | 장면은 공장 내에서 기계가 무단으로 움직이며 사고를 일으킨 것으로 보이며, 이는 기계의 안전 조치를… |
| 전도 | 위험 | 위험 | ✅ | 3.2s | 기계가 무게를 견딜 수 없는 상태에서 떨어졌으며, 운전자가 사망한 것으로 보임. 이는 매우 심각한 … |
| 전도 | 위험 | 위험 | ✅ | 3.1s | 기계가 무게를 견딜 수 없는 상태에서 운행하고 있으며, 작업자들이 그 기계의 위험한 상태에 노출되어… |
| 없음 | 위험 | 정상 | ❌ | 3.8s | 장면은 공장 내부의 작업 공간으로 보이며, 인물과 기계가 정상적인 움직임을 보이고 있습니다. 아무런… |
| 전도 | 위험 | 위험 | ✅ | 3.3s | 화재나 낙상(사람) 등이 아닌 기계적 위험이 존재합니다. 이는 높은 위험을 나타내며, 작업 중에 발… |
| 없음 | 정상 | 정상 | ✅ | 4.0s | 캡처된 장면은 지하 주차장 내부이며, 여러 차량이 정지 상태로 보이며, 아무런 위험한 행동이나 이상… |
| 없음 | 정상 | 정상 | ✅ | 2.9s | 화면에는 차량들이 주차된 것으로 보이며, 주변에는 녹색 식물과 조명이 설치되어 있는 것으로 보아 안… |
| 없음 | 정상 | 정상 | ✅ | 2.4s | 화면에는 물이 흘러 있는 지대와 건물, 차량이 보이며, 아무런 위험한 상황이나 이상적인 행동이 나타… |
| 전도 | 정상 | 정상 | ✅ | 3.3s | 눈이 내리는 날, 주차장에서 운반용 트럭이 정지하고 있으며, 사람들은 눈을 제거하는 작업을 하고 있… |
| 없음 | 정상 | 정상 | ✅ | 2.8s | 화면에는 차량이 주차되고 있으며, 인공지능 기반의 시스템이 작동하고 있는 것으로 보이며, 위험 요소… |
| 없음 | 정상 | 정상 | ✅ | 3.8s | 화면에는 작업 중인 직원들과 물품이 보이며, 작업 공간은 정돈되어 있고, 기계와 인력 모두 안전하게… |
| 없음 | 정상 | 정상 | ✅ | 3.1s | 화면에는 작업 중인 인물과 물품이 보이며, 주변에는 일반적인 기계와 택배용 트럭 등이 보입니다. 이… |
| 없음 | 정상 | 정상 | ✅ | 2.8s | 장면은 공장 내부의 저장 공간으로 보이며, 기계와 인력이 작업 중인 것으로 보입니다. 하지만 현재 … |
| 전도 | 정상 | 위험 | ❌ | 2.8s | 기계가 무단으로 떨어져 물건들이 흩어졌으며, 이는 위험한 상황을 초래할 수 있습니다. |
| 낙상 | 위험 | 정상 | ❌ | 5.5s | CCTV 영상에서 여성 고객이 보조를 받으며 카운터 앞에 서 있는 것으로 보이며, 주변에는 다른 고… |
| 낙상 | 위험 | 위험 | ✅ | 4.0s | CCTV 카메라에서 촬영된 장면에서, 한 남성이 작업대 앞에 서서 무언가를 들고 있는 동안, 다른 … |
| 낙상 | 위험 | 정상 | ❌ | 3.8s | 화면에서 두 사람이 높은 곳에서 떨어지는 것을 보여주며, 이는 위험한 상황을 나타냅니다. 그러나 이… |
| 낙상 | 위험 | 위험 | ✅ | 5.7s | 엣지 카메라에서 촬영된 장면에서, 사람들이 엘리베이터를 이용해 내려가고 있으며, 한 사람이 엘리베이… |
| 낙상 | 위험 | 위험 | ✅ | 4.1s | 엘리베이터가 운행 중인 시점에서 한 사람이 엘리베이터를 타고 내려가면서 무단히 떨어져서 지나간다. … |
| 화재 | 위험 | 위험 | ✅ | 3.5s | CCTV 영상에서 화재가 발생한 장면이 보이며, 빛이 나는 불꽃과 연기가 나오는 모습이 확인된다. … |
| 화재 | 위험 | 위험 | ✅ | 3.5s | 화재 감지 알림이 표시되어 있으며, 작업 중인 인원이 화재 발생 현장을 확인하고 빠르게 떨어져 나가… |
| 없음 | 위험 | 정상 | ❌ | 7.3s | 화면에는 공기 중의 연기와 함께 녹색 식물이 있는 지역이 보이며, 이는 자연적인 상태로 보입니다. … |
| 화재 | 위험 | 위험 | ✅ | 4.2s | 화면에는 검은 연기와 함께 건물들이 보이며, 이는 화재 발생의 시각적 증거입니다. 연기는 건물의 빛… |
| 화재 | 위험 | 위험 | ✅ | 3.5s | 공장의 여러 탱크와 연소 장비가 있는 지역에서 연기가 떠오르고 있으며, 일부 구조물에서 불꽃이 떨어… |
| 화재 | 위험 | 위험 | ✅ | 3.1s | 화재 발생 후 연기가 빠르게 확산되고 있으며, 인원들이 급히 피난하고 있는 상황. 화재는 큰 규모로… |
| 화재 | 위험 | 위험 | ✅ | 2.6s | 화재가 발생한 것으로 보이며, 방화 시스템이 작동하여 불을 막는 것으로 보여, 위험한 상황이 발생하… |
| 화재 | 위험 | 위험 | ✅ | 3.2s | 화재가 발생하여 큰 연기와 불꽃이 나오고 있으며, 주변에는 소방관들이 대응하고 있습니다. 현재의 상… |
| 화재 | 위험 | 위험 | ✅ | 4.1s | 화재가 발생한 것으로 보이며, 불꽃과 연기가 공중에서 퍼져나가고 있다. 이는 매우 심각한 위험을 초… |

## 상세 내역 

### Qwen3-VL-2B-Instruct

<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire1.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire1.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 것으로 보이며, 소방관이 화재를 진압하는 모습이 보입니다. 화재는 매우 강하게 빛나고 있으며, 주변은 붉은색으로 물들어 있어 위험한 상황을 나타냅니다. 이는 즉각적인 대응이 필요하며, 소방관의 안전을 위한 조치가 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire2.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire2.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 카메라가 촬영된 장면에서 밤에 주차된 차량 옆에서 불꽃과 연기가 떠오르며, 이는 화재 발생의 징후로 보입니다. 이는 매우 심각한 위험을 나타내며, 즉시 대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire3.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire3.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재는 카페트 위에서 발생한 것으로 보이며, 주변에는 빛이 흐르고 있다. 이는 화재가 발생했음을 시사한다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire4.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire4.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 건물에서 소방관들이 활동하고 있으며, 불꽃과 연기가 뚜렷하게 보이며, 위험한 상황이 진행되고 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire5.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire5.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 방 안에서 불이 발생하고 있으며, 화재는 벽에 있는 빨간색 표지판과 함께 진행되고 있습니다. 이는 위험한 상황이며, 즉시 구조적 대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire6.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire6.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 장소에서 빠르게 소화되는 모습이 보이며, 인원들이 물을 사용하여 대응하고 있다. 이는 매우 심각한 상황이며, 즉시 대응이 필요하다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire7.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire7.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 감지 시스템이 활성화되어 있으며, 화재 발생 위치가 여러 곳에 나타나고 있다. 이는 빠른 대응이 필요하다는 점에서 위험한 상황이다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire8.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire8.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 감지 시스템이 작동하여 화재가 발생한 것을 확인하고, 인원들이 즉시 대응하여 화재를 진압하고 있으며, 화재가 지속되고 있는 것으로 보입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover1.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover1.mp4 · 정답 위험 · 판정 위험(전도) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(기계)  <br><span class="cap-label">설명</span> 장면은 공장 내에서 기계가 무단으로 움직이며 사고를 일으킨 것으로 보이며, 이는 기계의 안전 조치를 무시한 상태에서 발생한 사고입니다. 사고의 원인은 기계의 운행 조건과 관련된 오류로 보이며, 이는 매우 심각한 위험을 초래할 수 있습니다. 사고 후에는 기계의 안전 조치를 다시 확인하고, 작업자에게 안전 교육을 실시해야 합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover2.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover2.mp4 · 정답 위험 · 판정 위험(전도) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(기계)  <br><span class="cap-label">설명</span> 기계가 무게를 견딜 수 없는 상태에서 떨어졌으며, 운전자가 사망한 것으로 보임. 이는 매우 심각한 위험을 나타냄.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover3.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover3.mp4 · 정답 위험 · 판정 위험(전도) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(기계)  <br><span class="cap-label">설명</span> 기계가 무게를 견딜 수 없는 상태에서 운행하고 있으며, 작업자들이 그 기계의 위험한 상태에 노출되어 있다. 이는 작업자의 안전을 위협하는 상황이다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover4.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover4.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 장면은 공장 내부의 작업 공간으로 보이며, 인물과 기계가 정상적인 움직임을 보이고 있습니다. 아무런 위험한 상황이나 불안정한 상태가 보이지 않으며, 조명과 배경은 일반적인 산업 환경을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover5.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover5.mp4 · 정답 위험 · 판정 위험(전도) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(기계)  <br><span class="cap-label">설명</span> 화재나 낙상(사람) 등이 아닌 기계적 위험이 존재합니다. 이는 높은 위험을 나타내며, 작업 중에 발생할 수 있는 사고의 가능성을 의미합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking1.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking1.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 캡처된 장면은 지하 주차장 내부이며, 여러 차량이 정지 상태로 보이며, 아무런 위험한 행동이나 이상한 현상이 관찰되지 않습니다. 주차장 내부는 안전하게 유지되고 있으며, 조명과 안전 시스템 등이 작동 중 보입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking2.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking2.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 차량들이 주차된 것으로 보이며, 주변에는 녹색 식물과 조명이 설치되어 있는 것으로 보아 안전한 상태입니다. 다만, CCTV 영상의 품질상 일부 불분명한 부분이 있지만, 현재 상황은 위험 요소가 없습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking3.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking3.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 물이 흘러 있는 지대와 건물, 차량이 보이며, 아무런 위험한 상황이나 이상적인 행동이 나타나지 않았습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking4.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking4.mp4 · 정답 정상 · 판정 정상(전도) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 낙상(기계)  <br><span class="cap-label">설명</span> 눈이 내리는 날, 주차장에서 운반용 트럭이 정지하고 있으며, 사람들은 눈을 제거하는 작업을 하고 있습니다. 이는 기계적 오류나 위험한 상태가 아닙니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking5.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking5.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 차량이 주차되고 있으며, 인공지능 기반의 시스템이 작동하고 있는 것으로 보이며, 위험 요소는 없습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker1.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker1.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 작업 중인 직원들과 물품이 보이며, 작업 공간은 정돈되어 있고, 기계와 인력 모두 안전하게 작동하고 있습니다. 주변에는 무리한 움직임이나 이상한 행동이 나타나지 않으며, 위험 요소는 없습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker2.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker2.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 작업 중인 인물과 물품이 보이며, 주변에는 일반적인 기계와 택배용 트럭 등이 보입니다. 이는 정상적인 작업 환경을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker3.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker3.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 장면은 공장 내부의 저장 공간으로 보이며, 기계와 인력이 작업 중인 것으로 보입니다. 하지만 현재 보이는 장면에는 위험 요소가 없습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker_4.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker_4.mp4 · 정답 정상 · 판정 위험(전도) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(기계)  <br><span class="cap-label">설명</span> 기계가 무단으로 떨어져 물건들이 흩어졌으며, 이는 위험한 상황을 초래할 수 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall1.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall1.mp4 · 정답 위험 · 판정 정상(낙상) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> CCTV 영상에서 여성 고객이 보조를 받으며 카운터 앞에 서 있는 것으로 보이며, 주변에는 다른 고객들이 있다. 하지만 이 영상은 실시간으로 촬영된 것이므로, 실제 위험 요소는 존재하지 않음. 다만, 고객이 카운터에 서 있는 상태가 보이며, 이는 일반적인 상황임을 의미함.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall2.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall2.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> CCTV 카메라에서 촬영된 장면에서, 한 남성이 작업대 앞에 서서 무언가를 들고 있는 동안, 다른 남성이 그 앞에 서서 그를 놓는다. 이는 작업 중 발생한 사고의 가능성을 의미하며, 위험한 상황이 발생할 수 있다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall3.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall3.mp4 · 정답 위험 · 판정 정상(낙상) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> 화면에서 두 사람이 높은 곳에서 떨어지는 것을 보여주며, 이는 위험한 상황을 나타냅니다. 그러나 이는 이미지의 일부로 인해 실제 위험은 존재하지 않으며, 이는 정상적인 상황을 의미합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall4.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall4.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> 엣지 카메라에서 촬영된 장면에서, 사람들이 엘리베이터를 이용해 내려가고 있으며, 한 사람이 엘리베이터를 타고 내려가는 과정에서 다른 사람에게 도움을 주는 것으로 보이지만, 그 후에 엘리베이터가 떨어지는 것을 보여주고 있다. 이는 위험한 상황이며, 엘리베이터가 떨어질 수 있는 위험을 나타내고 있다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall5.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall5.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> 엘리베이터가 운행 중인 시점에서 한 사람이 엘리베이터를 타고 내려가면서 무단히 떨어져서 지나간다. 이는 엘리베이터 안에 있는 사람들의 안전을 위협하는 사고이며, 즉 위험한 상황이다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke1.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke1.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> CCTV 영상에서 화재가 발생한 장면이 보이며, 빛이 나는 불꽃과 연기가 나오는 모습이 확인된다. 이는 매우 심각한 위험 상황을 나타내며, 화재가 발생한 것으로 보인다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke2.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke2.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 감지 알림이 표시되어 있으며, 작업 중인 인원이 화재 발생 현장을 확인하고 빠르게 떨어져 나가고 있다. 이는 위험한 상황이며, 즉시 대응이 필요하다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke3.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke3.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 화면에는 공기 중의 연기와 함께 녹색 식물이 있는 지역이 보이며, 이는 자연적인 상태로 보입니다. 주변에는 건물과 산업시설이 있으며, 현재의 장면에서 위험 요소가 나타나지 않습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke4.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke4.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화면에는 검은 연기와 함께 건물들이 보이며, 이는 화재 발생의 시각적 증거입니다. 연기는 건물의 빛을 흐리게 하여 위험한 상황을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke5.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke5.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 공장의 여러 탱크와 연소 장비가 있는 지역에서 연기가 떠오르고 있으며, 일부 구조물에서 불꽃이 떨어지고 있다. 이는 화재 발생의 징후로 보이며, 즉각적인 대응이 필요하다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire1.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire1.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 발생 후 연기가 빠르게 확산되고 있으며, 인원들이 급히 피난하고 있는 상황. 화재는 큰 규모로 진행되고 있어, 즉각적인 대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire2.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire2.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 것으로 보이며, 방화 시스템이 작동하여 불을 막는 것으로 보여, 위험한 상황이 발생하고 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire3.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire3.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생하여 큰 연기와 불꽃이 나오고 있으며, 주변에는 소방관들이 대응하고 있습니다. 현재의 상황은 매우 위험하며, 즉각적인 구조 및 소방대의 개입이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire4.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire4.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 것으로 보이며, 불꽃과 연기가 공중에서 퍼져나가고 있다. 이는 매우 심각한 위험을 초래할 수 있으며, 즉각적인 구조적 대응이 필요하다.</div></div></div>
