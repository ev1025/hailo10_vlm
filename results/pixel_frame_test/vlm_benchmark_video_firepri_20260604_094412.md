# 엣지 VLM 해석 평가 (firepri)

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
| Qwen3-VL-2B-Instruct | ✅ 7.92s | 89% | 94% | 11% | 3.57s | 22.6 | 5224 MB |

## Qwen3-VL-2B-Instruct — `Qwen/Qwen3-VL-2B-Instruct`

**위험 유형별 인식 (카테고리별 정답률)**

| 카테고리 | 정답유형 | N | 위험판정 | 판정정답률 | 유형정답률 | 미상 |
|---|---|---|---|---|---|---|
| 화재 | 화재 | 8 | 8 | 100% | 100% | 0 |
| 연기 | 화재 | 9 | 9 | 100% | 100% | 0 |
| 사람 쓰러짐/낙상 | 낙상 | 5 | 3 | 60% | 100% | 0 |
| 기계·장비 전도 | 전도 | 5 | 4 | 80% | 100% | 0 |
| 정상 주차장(오탐 테스트) | 없음 | 5 | 0 | 100% | 80% | 0 |
| 정상 작업장(오탐 테스트) | 없음 | 4 | 1 | 75% | 75% | 0 |

**항목별 결과**

| 유형 | 정답 | 판정 | 정오 | 시간 | 해석(앞부분) |
|---|---|---|---|---|---|
| 화재 | 위험 | 위험 | ✅ | 2.5s | 화재 현장에서 소방관이 불꽃과 연기를 보며 작업하고 있으며, 화재가 매우 심각한 상태로 보입니다. |
| 화재 | 위험 | 위험 | ✅ | 4.6s | 카메라에서 보이는 장면은 밤에 촬영되었으며, 왼쪽에 불꽃과 연기가 나는 것을 볼 수 있습니다. 이는… |
| 화재 | 위험 | 위험 | ✅ | 3.0s | 실내에서 불꽃이 발생한 것으로 보이며, 주변 환경이 불안정해 보입니다. 이는 빠르게 진행되는 위험 … |
| 화재 | 위험 | 위험 | ✅ | 3.2s | 화재가 발생한 건물에서 불꽃과 연기가 뚜렷하게 보이며, 소방관들이 현장에 도착하여 대응하고 있습니다… |
| 화재 | 위험 | 위험 | ✅ | 3.0s | 방 안에서 불이 났으며, 연기가 피어오르고 있다. 화재는 벽에 있는 표지판과 같은 안전 정보를 제공… |
| 화재 | 위험 | 위험 | ✅ | 3.3s | 화재가 발생한 장소에서 불꽃과 연기가 뚫려 있으며, 인원들이 대응하고 있는 상황이다. 이는 매우 심… |
| 화재 | 위험 | 위험 | ✅ | 4.8s | 화재 감지 시스템이 활성화되어 있으며, 화재가 발생한 장소에서 불꽃과 연기가 보이며, 인원이 해당 … |
| 화재 | 위험 | 위험 | ✅ | 2.5s | 화재 감지 시스템이 활성화되어 있으며, 실내에서 불꽃과 연기가 발생하고 있다. 이는 빠른 대응이 필… |
| 전도 | 위험 | 위험 | ✅ | 3.1s | 장면은 공장 내에서 기계가 무단으로 움직이며 사고를 일으킨 것으로 보이며, 이는 기계의 안전 조치를… |
| 전도 | 위험 | 위험 | ✅ | 3.6s | 기계가 무게를 견딜 수 없는 상태에서 떨어졌으며, 운전자가 사망한 것으로 보입니다. 이는 매우 심각… |
| 전도 | 위험 | 위험 | ✅ | 3.5s | 장면에서 기계가 무게를 견딜 수 없는 상태로 떨어져 사람을 던지는 사고가 발생하고 있으며, 이는 기… |
| 전도 | 위험 | 정상 | ❌ | 5.3s | 장면은 공장 내부에서 작업 중인 기계가 떨어지는 듯한 움직임을 보이고 있으며, 이는 낙상(기계)의 … |
| 전도 | 위험 | 위험 | ✅ | 3.0s | 화재나 불꽃이 보이지 않지만, 기계가 위험한 상태로 운행하고 있으며, 이는 작업 중 발생할 수 있는… |
| 없음 | 정상 | 정상 | ✅ | 4.1s | 장면은 지하 주차장 내부이며, 차량들이 정지 상태로 보이며, 아무런 위험한 현상이나 불안정한 상태가… |
| 없음 | 정상 | 정상 | ✅ | 2.8s | CCTV 영상은 밤에 촬영된 것으로, 주변에는 차량들이 정차하고 있으며, 아무런 위험한 현상이나 불… |
| 없음 | 정상 | 정상 | ✅ | 3.3s | 장면은 비가 내리는 날의 야외 공간으로 보이며, 건물, 주차장, 그리고 녹색 지대가 보입니다. 이곳… |
| 전도 | 정상 | 정상 | ✅ | 4.2s | 눈이 내리는 날, 주차장에서 운반용 트럭이 정지하고 있으며, 사람들은 눈을 제거하기 위해 휘두르는 … |
| 없음 | 정상 | 정상 | ✅ | 3.5s | 장면은 주차장을 보여주며, 차량들이 정지해 있고, 사람이나 기계가 위험한 상황을 일으키는 것은 보이… |
| 없음 | 정상 | 정상 | ✅ | 4.7s | 재난 현장의 엣지 카메라로 캡처된 장면은 창고 내부에서 작업 중인 직원들이 박스를 처리하고 있는 모… |
| 없음 | 정상 | 정상 | ✅ | 3.4s | 장면은 공장 내부의 작업 공간으로 보이며, 사람과 기계가 활동하고 있는 상태입니다. 그러나 화재나 … |
| 없음 | 정상 | 정상 | ✅ | 3.2s | 장소는 공장 내부이며, 기계와 인물이 보이지만, 불꽃이나 연기, 화재 등 위험 요소가 나타나 있지 … |
| 전도 | 정상 | 위험 | ❌ | 2.8s | 기계가 무단으로 떨어져 물건들이 바닥에 흩어졌으며, 이는 위험한 상황을 초래할 수 있습니다. |
| 낙상 | 위험 | 정상 | ❌ | 3.9s | CCTV 영상에서 여성 고객이 보조를 받으며 카운터 앞에 서 있는 모습이며, 이는 일반적인 상점 내… |
| 낙상 | 위험 | 위험 | ✅ | 3.6s | CCTV 카메라에서 촬영된 장면은 농업용 기계가 바닥에 떨어져 있는 것을 보여주며, 이는 사람의 위… |
| 낙상 | 위험 | 정상 | ❌ | 3.5s | 화면에서 두 명의 사람이 집 앞 porch에 서 있으며, 한 명이 다른 사람을 향해 움직이고 있다.… |
| 낙상 | 위험 | 위험 | ✅ | 5.4s | 엣지 카메라에서 촬영된 장면에서는 사람들이 엘리베이터를 이용해 내려가고 있으며, 한 명이 엘리베이터… |
| 낙상 | 위험 | 위험 | ✅ | 4.0s | 승강장에서 내려가는 사람의 뒤로 낙상한 사람이 나타나며, 이는 위험한 상황을 초래할 수 있습니다. … |
| 화재 | 위험 | 위험 | ✅ | 3.1s | 화재가 발생한 것으로 보이며, 불꽃과 연기가 보이고, 인근에는 소방대원들이 대응하고 있습니다. 이는… |
| 화재 | 위험 | 위험 | ✅ | 3.1s | 화재 감지 알림이 표시되어 있으며, 작업 중인 인원이 불꽃이나 연기를 보이고 있다. 이는 화재 발생… |
| 화재 | 위험 | 위험 | ✅ | 2.9s | 연기와 불꽃이 보이며, 이는 화재 발생의 징후로, 즉 시스템 내에서 위험한 상황을 나타냅니다. |
| 화재 | 위험 | 위험 | ✅ | 3.4s | 화면에는 검은 연기가 하늘로 퍼져 있으며, 건물들이 불에 떨어지고 있는 것으로 보입니다. 이는 화재… |
| 화재 | 위험 | 위험 | ✅ | 4.0s | 공장의 여러 탱크와 청소구조물에서 연기가 흐르고 있으며, 일부 구조물에서 불꽃이 떨어지고 있다. 이… |
| 화재 | 위험 | 위험 | ✅ | 3.5s | 화재 발생 시 연기와 불꽃이 발생하며, 인원들이 빠르게 피난하고 있는 상황. 화재는 매우 심각한 위… |
| 화재 | 위험 | 위험 | ✅ | 3.8s | 화재가 발생한 것으로 보이며, 연기와 불꽃이 관찰되며, 이는 위험한 상황을 나타냅니다. 화재가 발생… |
| 화재 | 위험 | 위험 | ✅ | 3.1s | 화재가 발생하여 큰 연기가 떠오르고 있으며, 불꽃과 함께 건물이 파손되고 있습니다. 이는 매우 심각… |
| 화재 | 위험 | 위험 | ✅ | 3.7s | 화재가 발생한 것으로 보이며, 불꽃과 연기가 공중에서 퍼져 있는 상태로, 사람들은 긴급히 떠나고 있… |

## 상세 내역 

### Qwen3-VL-2B-Instruct

<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire1.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire1.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 현장에서 소방관이 불꽃과 연기를 보며 작업하고 있으며, 화재가 매우 심각한 상태로 보입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire2.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire2.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 카메라에서 보이는 장면은 밤에 촬영되었으며, 왼쪽에 불꽃과 연기가 나는 것을 볼 수 있습니다. 이는 화재 발생의 징후로 보이며, 주변 환경이 매우 위험한 상태로 보입니다. 즉, 화재가 발생했음을 알 수 있으며, 이는 매우 심각한 상황입니다. 따라서 조치를 취해야 합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire3.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire3.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 실내에서 불꽃이 발생한 것으로 보이며, 주변 환경이 불안정해 보입니다. 이는 빠르게 진행되는 위험 상황으로, 즉시 대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire4.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire4.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 건물에서 불꽃과 연기가 뚜렷하게 보이며, 소방관들이 현장에 도착하여 대응하고 있습니다. 화재는 매우 심각하며, 주변에는 사람들이 보입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire5.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire5.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 방 안에서 불이 났으며, 연기가 피어오르고 있다. 화재는 벽에 있는 표지판과 같은 안전 정보를 제공하고 있으며, 이는 위험한 상황을 나타낸다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire6.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire6.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 장소에서 불꽃과 연기가 뚫려 있으며, 인원들이 대응하고 있는 상황이다. 이는 매우 심각한 위험을 나타내며, 즉시 구조 및 소방대응이 필요하다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire7.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire7.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 감지 시스템이 활성화되어 있으며, 화재가 발생한 장소에서 불꽃과 연기가 보이며, 인원이 해당 장소에 존재하고 있습니다. 이는 매우 심각한 위험을 나타냅니다. 즉, 화재가 발생했으며, 인원이 그 장소에 있음을 확인할 수 있습니다. 따라서, 즉시 안전 대책을 취해야 합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire8.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire8.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 감지 시스템이 활성화되어 있으며, 실내에서 불꽃과 연기가 발생하고 있다. 이는 빠른 대응이 필요하다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover1.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover1.mp4 · 정답 위험 · 판정 위험(전도) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(기계)  <br><span class="cap-label">설명</span> 장면은 공장 내에서 기계가 무단으로 움직이며 사고를 일으킨 것으로 보이며, 이는 기계의 안전 조치를 무시한 상태에서 발생한 사고입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover2.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover2.mp4 · 정답 위험 · 판정 위험(전도) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(기계)  <br><span class="cap-label">설명</span> 기계가 무게를 견딜 수 없는 상태에서 떨어졌으며, 운전자가 사망한 것으로 보입니다. 이는 매우 심각한 사고로, 즉시 구조대와 병원으로 이송해야 합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover3.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover3.mp4 · 정답 위험 · 판정 위험(전도) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(기계)  <br><span class="cap-label">설명</span> 장면에서 기계가 무게를 견딜 수 없는 상태로 떨어져 사람을 던지는 사고가 발생하고 있으며, 이는 기계의 불안정한 상태와 관련된 위험을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover4.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover4.mp4 · 정답 위험 · 판정 정상(전도) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 낙상(기계)  <br><span class="cap-label">설명</span> 장면은 공장 내부에서 작업 중인 기계가 떨어지는 듯한 움직임을 보이고 있으며, 이는 낙상(기계)의 가능성을 의미합니다. 그러나 현재의 장면에서 화재나 불꽃 등 위험 요소는 보이지 않으며, 기계의 움직임은 일반적인 작업 중 발생할 수 있는 사고를 나타냅니다. 따라서 이는 &#x27;낙상(기계)&#x27;의 유형으로 판단됩니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover5.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover5.mp4 · 정답 위험 · 판정 위험(전도) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(기계)  <br><span class="cap-label">설명</span> 화재나 불꽃이 보이지 않지만, 기계가 위험한 상태로 운행하고 있으며, 이는 작업 중 발생할 수 있는 위험을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking1.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking1.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 장면은 지하 주차장 내부이며, 차량들이 정지 상태로 보이며, 아무런 위험한 현상이나 불안정한 상태가 보이지 않습니다. 주변에는 연기나 불꽃, 화염 등이 나타나 있지 않으며, 사람이나 기계의 낙상 위험이 존재하지 않습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking2.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking2.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> CCTV 영상은 밤에 촬영된 것으로, 주변에는 차량들이 정차하고 있으며, 아무런 위험한 현상이나 불꽃, 연기 등이 보이지 않습니다. 화재나 낙상(사람) 등의 위험이 존재하지 않으며, 현재 상황은 정상적인 상태입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking3.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking3.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 장면은 비가 내리는 날의 야외 공간으로 보이며, 건물, 주차장, 그리고 녹색 지대가 보입니다. 이곳에는 사람이나 기계가 보이지 않으며, 불꽃이나 연기가 등장하지 않습니다. 따라서 위험 요소는 없습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking4.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking4.mp4 · 정답 정상 · 판정 정상(전도) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 낙상(기계)  <br><span class="cap-label">설명</span> 눈이 내리는 날, 주차장에서 운반용 트럭이 정지하고 있으며, 사람들은 눈을 제거하기 위해 휘두르는 장비를 사용하고 있습니다. 이 장비는 운반용 트럭과 관련된 작업을 수행하는 것으로 보이며, 현재는 위험한 상황이 아닙니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking5.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking5.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 장면은 주차장을 보여주며, 차량들이 정지해 있고, 사람이나 기계가 위험한 상황을 일으키는 것은 보이지 않습니다. 주변에는 안전 조치가 이루어진 상태이며, 불꽃이나 연기 등 위험 요소는 없습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker1.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker1.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 재난 현장의 엣지 카메라로 캡처된 장면은 창고 내부에서 작업 중인 직원들이 박스를 처리하고 있는 모습입니다. 작업 공간은 안전하게 유지되고 있으며, 인력과 기계는 정상적인 상태입니다. 아무런 위험한 현상이나 불안정한 상태가 보이지 않으며, 작업 중인 직원들은 안전한 자세를 취하고 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker2.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker2.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 장면은 공장 내부의 작업 공간으로 보이며, 사람과 기계가 활동하고 있는 상태입니다. 그러나 화재나 불꽃, 연기 등 위험 요소는 보이지 않으며, 모든 객체는 정상적인 상태로 보입니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker3.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker3.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 없음  <br><span class="cap-label">설명</span> 장소는 공장 내부이며, 기계와 인물이 보이지만, 불꽃이나 연기, 화재 등 위험 요소가 나타나 있지 않으며, 작업 중인 기계는 안전하게 작동하고 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker_4.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker_4.mp4 · 정답 정상 · 판정 위험(전도) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(기계)  <br><span class="cap-label">설명</span> 기계가 무단으로 떨어져 물건들이 바닥에 흩어졌으며, 이는 위험한 상황을 초래할 수 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall1.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall1.mp4 · 정답 위험 · 판정 정상(낙상) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> CCTV 영상에서 여성 고객이 보조를 받으며 카운터 앞에 서 있는 모습이며, 이는 일반적인 상점 내부의 일상적인 상황으로 보입니다. 주변에는 다른 고객들이 보이며, 상점 내부의 안전 조치가 유지되고 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall2.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall2.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> CCTV 카메라에서 촬영된 장면은 농업용 기계가 바닥에 떨어져 있는 것을 보여주며, 이는 사람의 위험한 행동으로 인해 발생한 사고임을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall3.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall3.mp4 · 정답 위험 · 판정 정상(낙상) ❌</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-safe">정상</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> 화면에서 두 명의 사람이 집 앞 porch에 서 있으며, 한 명이 다른 사람을 향해 움직이고 있다. 이는 일반적인 상황이며, 낙상(사람)의 위험이 존재하지 않음을 의미한다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall4.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall4.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> 엣지 카메라에서 촬영된 장면에서는 사람들이 엘리베이터를 이용해 내려가고 있으며, 한 명이 엘리베이터를 타고 내려가는 과정에서 다른 사람에게 도움을 주는 것으로 보이지만, 그 중 한 명이 엘리베이터를 잘못 사용하여 넘어지는 모습이 나타나고 있다. 이는 위험한 상황이며, 즉시 조치가 필요하다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall5.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall5.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 낙상(사람)  <br><span class="cap-label">설명</span> 승강장에서 내려가는 사람의 뒤로 낙상한 사람이 나타나며, 이는 위험한 상황을 초래할 수 있습니다. 승강장에서 낙상한 사람의 위치가 안전하지 않으며, 다른 사람들의 안전을 위협하고 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke1.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke1.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 것으로 보이며, 불꽃과 연기가 보이고, 인근에는 소방대원들이 대응하고 있습니다. 이는 매우 심각한 상황으로, 즉시 대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke2.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke2.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 감지 알림이 표시되어 있으며, 작업 중인 인원이 불꽃이나 연기를 보이고 있다. 이는 화재 발생의 신호이며, 즉시 대응이 필요하다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke3.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke3.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 연기와 불꽃이 보이며, 이는 화재 발생의 징후로, 즉 시스템 내에서 위험한 상황을 나타냅니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke4.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke4.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화면에는 검은 연기가 하늘로 퍼져 있으며, 건물들이 불에 떨어지고 있는 것으로 보입니다. 이는 화재 발생의 징후이며, 주변 환경이 위험한 상태에 있습니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke5.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke5.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 공장의 여러 탱크와 청소구조물에서 연기가 흐르고 있으며, 일부 구조물에서 불꽃이 떨어지고 있다. 이는 화재 발생의 징후로, 즉 시스템 내부에서의 불안정한 상태를 나타내며, 즉 위험한 상황이다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire1.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire1.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재 발생 시 연기와 불꽃이 발생하며, 인원들이 빠르게 피난하고 있는 상황. 화재는 매우 심각한 위험을 초래할 수 있으며, 즉각적인 대응이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire2.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire2.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 것으로 보이며, 연기와 불꽃이 관찰되며, 이는 위험한 상황을 나타냅니다. 화재가 발생한 장소에서 소방관이 즉시 대응할 필요가 있으며, 이는 위험한 상황을 의미합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire3.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire3.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생하여 큰 연기가 떠오르고 있으며, 불꽃과 함께 건물이 파손되고 있습니다. 이는 매우 심각한 상황이며, 즉시 구조대의 개입이 필요합니다.</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire4.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire4.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text"><span class="cap-label">판정</span> <span class="v-danger">위험</span>  <br><span class="cap-label">유형</span> 화재  <br><span class="cap-label">설명</span> 화재가 발생한 것으로 보이며, 불꽃과 연기가 공중에서 퍼져 있는 상태로, 사람들은 긴급히 떠나고 있습니다. 이는 매우 심각한 상황이며, 즉시 구조대와 소방대의 개입이 필요합니다.</div></div></div>
