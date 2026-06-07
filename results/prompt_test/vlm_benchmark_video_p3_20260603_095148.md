# 엣지 VLM 해석 평가 (P3)

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
| Qwen3-VL-2B-Instruct | ✅ 7.86s | 69% | 72% | 11% | 3.07s | 31.5 | 4546 MB |

## Qwen3-VL-2B-Instruct — `Qwen/Qwen3-VL-2B-Instruct`

**위험 유형별 인식 (카테고리별 정답률)**

| 카테고리 | 정답유형 | N | 위험판정 | 판정정답률 | 유형정답률 | 미상 |
|---|---|---|---|---|---|---|
| 화재 | 화재 | 8 | 8 | 100% | 100% | 0 |
| 연기 | 화재 | 9 | 6 | 67% | 89% | 1 |
| 사람 쓰러짐/낙상 | 낙상 | 5 | 2 | 40% | 40% | 0 |
| 기계·장비 전도 | 전도 | 5 | 1 | 20% | 0% | 0 |
| 정상 주차장(오탐 테스트) | 없음 | 5 | 0 | 100% | 100% | 0 |
| 정상 작업장(오탐 테스트) | 없음 | 4 | 1 | 75% | 75% | 0 |

**항목별 결과**

| 유형 | 정답 | 판정 | 정오 | 시간 | 해석(앞부분) |
|---|---|---|---|---|---|
| 화재 | 위험 | 위험 | ✅ | 2.7s | 화재가 발생한 것으로 보이며, 화재가 있는 공간에서 인물이 빠져나가는 모습이 보입니다. 화재는 매우… |
| 화재 | 위험 | 위험 | ✅ | 3.0s | 영상에서 밤에 주차된 차량 옆에 불꽃이 떠오르고 있으며, 화재가 발생하고 있는 것으로 보입니다. 불… |
| 화재 | 위험 | 위험 | ✅ | 2.5s | 화재는 화염이 발생하고 있으며, 주변에는 빛이 나는 불꽃이 보입니다. 이는 매우 심각한 위험을 나타… |
| 화재 | 위험 | 위험 | ✅ | 3.2s | 화재가 발생한 건물에서 불꽃과 연기로 인해 위험한 상황이 발생하고 있으며, 소방관들이 대응하고 있습… |
| 화재 | 위험 | 위험 | ✅ | 3.3s | 화재가 발생하고 있으며, 방 안의 여러 물건들이 불에 끼어 있다. 화재는 벽에 닿는 물건을 포함하고… |
| 화재 | 위험 | 위험 | ✅ | 3.7s | 화재가 발생한 장소는 공장 내부이며, 화재는 빠르게 번져나가고 있으며, 주변에는 많은 사람들이 있는… |
| 화재 | 위험 | 위험 | ✅ | 2.8s | 화재가 발생한 것으로 보이며, 화재 경고 알림이 표시되어 있습니다. 화재는 빨간색 빛을 발하며, 주… |
| 화재 | 위험 | 위험 | ✅ | 3.1s | 화재 감지 시스템이 활성화되어 있으며, 화재가 발생한 장소는 작업 공간 내에서 빠르게 발화하고 있다… |
| 없음 | 위험 | 정상 | ❌ | 2.8s | 화면은 재난 현장의 엣지 카메라 영상으로, 주로 작업 장비와 인원의 움직임을 보여주고 있습니다. 이… |
| 낙상 | 위험 | 위험 | ✅ | 2.9s | 화면에서 볼 수 있는 장비는 높은 위치에 있는 트럭을 기반으로 하며, 이 트럭이 바닥에 떨어져 있음… |
| 없음 | 위험 | 정상 | ❌ | 2.9s | 영상은 재난 현장의 엣지 카메라 영상으로, 작업 중인 기계와 인물의 움직임을 보여주고 있으며, 위험… |
| 없음 | 위험 | 정상 | ❌ | 3.1s | 영상은 재난 현장의 엣지 카메라 영상으로, 인물과 장비가 있는 공장 내부를 보여주고 있으며, 화재나… |
| 없음 | 위험 | 정상 | ❌ | 2.7s | 재난 현장의 엣지 카메라 영상에서, 작업자와 장비가 안전하게 움직이고 있으며, 화재나 낙상 등의 위… |
| 없음 | 정상 | 정상 | ✅ | 2.3s | 영상은 지하 주차장 내부의 장면을 보여주며, 차량들이 정지된 상태로 주차되어 있으며, 아무런 위험 … |
| 없음 | 정상 | 정상 | ✅ | 3.5s | 영상은 밤에 촬영된 것으로, 주변에는 차량들이 정지해 있으며, 주변 환경은 안전하다. CCTV 카메… |
| 없음 | 정상 | 정상 | ✅ | 3.5s | 화면은 비가 내리는 날의 재난 현장의 엣지 카메라 영상으로, 바닥이 물에 빠져 있고, 주변에는 차량… |
| 없음 | 정상 | 정상 | ✅ | 2.2s | 화면은 눈이 내리는 날의 공원이나 주차장을 보여주고 있으며, 사람과 차량이 있는 것으로 보이며, 위… |
| 없음 | 정상 | 정상 | ✅ | 2.7s | 화면에는 주차된 자동차들과 건물이 보이며, 아무런 위험 요소가 나타나고 있지 않습니다. CCTV 영… |
| 없음 | 정상 | 정상 | ✅ | 3.0s | 재난 현장의 엣지 카메라 영상에서 보이는 장면은 안전한 작업 환경을 나타내며, 작업자들이 안전한 위… |
| 없음 | 정상 | 정상 | ✅ | 3.0s | 영상은 재난 현장의 엣지 카메라 영상으로, 작업 중인 인물과 장비가 보이며, 화재나 낙상, 전도 등… |
| 없음 | 정상 | 정상 | ✅ | 3.0s | 재난 현장의 엣지 카메라 영상은 공장 내부의 저장 공간을 보여주고 있으며, 작업 중인 장비와 인원이… |
| 낙상 | 정상 | 위험 | ❌ | 3.4s | 영상에서 재난 현장의 한 장면으로 보이는 화면은 무너진 구조물과 함께 파손된 물건들이 떨어져 있는 … |
| 없음 | 위험 | 정상 | ❌ | 2.7s | 영상은 상점 내부에서 고객과 직원이 상점 결제 장소에서 상품을 거래하는 장면을 보여줍니다. 이는 일… |
| 낙상 | 위험 | 위험 | ✅ | 3.1s | 카메라 영상에서 남성 한 명이 무릎을 꿇고 바닥에 떨어진 상태로 보이며, 그의 몸이 바닥에 닿아 있… |
| 없음 | 위험 | 정상 | ❌ | 2.2s | 화면에는 사람과 자연 환경이 보이며, 아무런 위험 요소가 나타나고 있지 않습니다. 주변 환경은 평온… |
| 없음 | 위험 | 정상 | ❌ | 3.0s | 영상은 엣지 카메라로 촬영된 것으로, 사람들이 엘리베이터를 이용하고 있는 장면을 보여줍니다. 이는 … |
| 낙상 | 위험 | 위험 | ✅ | 3.9s | 영상에서 승강기 안에 사람이 떨어져 내려오는 상황이 발생하고 있으며, 이는 매우 위험한 상황을 나타… |
| 화재 | 위험 | 불명 | ∅ | 2.5s | 화재가 발생한 것으로 보이며, 빛이 나는 불꽃과 연기, 그리고 화재 대응 팀의 활동이 확인됩니다. … |
| 화재 | 위험 | 위험 | ✅ | 2.9s | 화재/소각 감지 알림이 표시되어 있으며, 작업 중인 인원이 화재 발생 시 즉각적인 대응을 요구합니다… |
| 화재 | 위험 | 위험 | ✅ | 3.9s | 영상에서 녹색 숲의 일부가 연기로 가득 차 있으며, 이는 화재 발생의 징후입니다. 연기는 공기 중에… |
| 화재 | 위험 | 위험 | ✅ | 3.2s | 화면에는 건물들이 있으며, 그 중 일부는 검은 연기로 뒤덮여 있습니다. 이는 화재 발생의 징후로 보… |
| 없음 | 위험 | 정상 | ❌ | 3.0s | 화면에는 산업 복합체가 보이며, 연기와 배출구가 있는 것으로 보아 화재나 낙상 등의 위험이 존재하지… |
| 화재 | 위험 | 위험 | ✅ | 3.1s | 화재가 발생한 것으로 보이며, 화재는 큰 규모의 연기와 불꽃을 내고 있습니다. 화재가 발생한 장소는… |
| 화재 | 위험 | 정상 | ❌ | 5.9s | 화재가 발생한 장소는 대형 백화점의 저장실로 보이며, 화재는 빛을 내고 있으며, 주변에는 수많은 상… |
| 화재 | 위험 | 위험 | ✅ | 2.6s | 화재가 발생한 것으로 보이며, 건물의 외벽에서 연기가 떠오르고, 불꽃이 번쩍이는 모습이 확인된다. … |
| 화재 | 위험 | 위험 | ✅ | 3.4s | 화재는 화염이 발생하고 있으며, 빛을 내는 불꽃이 보입니다. 이는 매우 심각한 위험을 나타냅니다. … |

## 상세 내역 

### Qwen3-VL-2B-Instruct

<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire1.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire1.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;화재&quot;,<br>  &quot;설명&quot;: &quot;화재가 발생한 것으로 보이며, 화재가 있는 공간에서 인물이 빠져나가는 모습이 보입니다. 화재는 매우 강하게 불어오고 있으며, 주변 환경이 매우 위험해 보입니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire2.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire2.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;화재&quot;,<br>  &quot;설명&quot;: &quot;영상에서 밤에 주차된 차량 옆에 불꽃이 떠오르고 있으며, 화재가 발생하고 있는 것으로 보입니다. 불꽃은 차량 주변에 위치하고 있으며, 주변 환경은 안전하지 않음을 시사합니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire3.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire3.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;화재&quot;,<br>  &quot;설명&quot;: &quot;화재는 화염이 발생하고 있으며, 주변에는 빛이 나는 불꽃이 보입니다. 이는 매우 심각한 위험을 나타냅니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire4.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire4.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;화재&quot;,<br>  &quot;설명&quot;: &quot;화재가 발생한 건물에서 불꽃과 연기로 인해 위험한 상황이 발생하고 있으며, 소방관들이 대응하고 있습니다. 화재는 매우 심각하며, 건물의 구조가 위험할 수 있습니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire5.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire5.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;화재&quot;,<br>  &quot;설명&quot;: &quot;화재가 발생하고 있으며, 방 안의 여러 물건들이 불에 끼어 있다. 화재는 벽에 닿는 물건을 포함하고 있으며, 방 안의 안전 조치가 필요하다. 화재의 심각도는 매우 높으며, 즉시 구조 및 소방 서비스에 연락해야 한다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire6.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire6.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;화재&quot;,<br>  &quot;설명&quot;: &quot;화재가 발생한 장소는 공장 내부이며, 화재는 빠르게 번져나가고 있으며, 주변에는 많은 사람들이 있는 것으로 보입니다. 화재는 빠르게 확산되며, 주변의 물체들이 떨어지는 것을 보여줍니다. 이는 매우 심각한 상황을 나타냅니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire7.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire7.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;화재&quot;,<br>  &quot;설명&quot;: &quot;화재가 발생한 것으로 보이며, 화재 경고 알림이 표시되어 있습니다. 화재는 빨간색 빛을 발하며, 주변에는 인원이 존재하고, 이는 위험 상황을 나타냅니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/fire8.jpg"></div><div class="cap-body"><div class="cap-head">[video] fire8.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;화재&quot;,<br>  &quot;설명&quot;: &quot;화재 감지 시스템이 활성화되어 있으며, 화재가 발생한 장소는 작업 공간 내에서 빠르게 발화하고 있다. 화재는 빠르게 확산하며, 주변에는 사람들이 모여 있는 것으로 보이며, 즉시 대응이 필요하다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover1.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover1.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;정상&quot;,<br>  &quot;유형&quot;: &quot;없음&quot;,<br>  &quot;설명&quot;: &quot;화면은 재난 현장의 엣지 카메라 영상으로, 주로 작업 장비와 인원의 움직임을 보여주고 있습니다. 이는 안전 상황을 나타내며, 위험 요소가 포함되어 있지 않습니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover2.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover2.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;낙상&quot;,<br>  &quot;설명&quot;: &quot;화면에서 볼 수 있는 장비는 높은 위치에 있는 트럭을 기반으로 하며, 이 트럭이 바닥에 떨어져 있음을 확인할 수 있습니다. 이는 위험한 상황을 나타냅니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover3.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover3.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;정상&quot;,<br>  &quot;유형&quot;: &quot;없음&quot;,<br>  &quot;설명&quot;: &quot;영상은 재난 현장의 엣지 카메라 영상으로, 작업 중인 기계와 인물의 움직임을 보여주고 있으며, 위험 요소는 포함되어 있지 않습니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover4.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover4.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;정상&quot;,<br>  &quot;유형&quot;: &quot;없음&quot;,<br>  &quot;설명&quot;: &quot;영상은 재난 현장의 엣지 카메라 영상으로, 인물과 장비가 있는 공장 내부를 보여주고 있으며, 화재나 낙상, 전도 등의 위험 요소가 나타나지 않습니다. 전체적인 상황은 안전하고 정상적인 상태입니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/machine_tipover5.jpg"></div><div class="cap-body"><div class="cap-head">[video] machine_tipover5.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;정상&quot;,<br>  &quot;유형&quot;: &quot;없음&quot;,<br>  &quot;설명&quot;: &quot;재난 현장의 엣지 카메라 영상에서, 작업자와 장비가 안전하게 움직이고 있으며, 화재나 낙상 등의 위험 요소는 관찰되지 않습니다. 전체적인 상황은 안정적입니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking1.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking1.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;정상&quot;,<br>  &quot;유형&quot;: &quot;없음&quot;,<br>  &quot;설명&quot;: &quot;영상은 지하 주차장 내부의 장면을 보여주며, 차량들이 정지된 상태로 주차되어 있으며, 아무런 위험 요소가 관찰되지 않습니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking2.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking2.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;정상&quot;,<br>  &quot;유형&quot;: &quot;없음&quot;,<br>  &quot;설명&quot;: &quot;영상은 밤에 촬영된 것으로, 주변에는 차량들이 정지해 있으며, 주변 환경은 안전하다. CCTV 카메라에서 보이는 모든 요소는 이상하지 않으며, 화재나 낙상, 전도 등의 위험 요소가 존재하지 않는다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking3.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking3.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;정상&quot;,<br>  &quot;유형&quot;: &quot;없음&quot;,<br>  &quot;설명&quot;: &quot;화면은 비가 내리는 날의 재난 현장의 엣지 카메라 영상으로, 바닥이 물에 빠져 있고, 주변에는 차량들이 보입니다. 하지만 화재나 낙상, 전도 등의 위험 요소는 나타나지 않습니다. 전체적인 상황은 안전하고 정상적인 상태입니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking4.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking4.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;정상&quot;,<br>  &quot;유형&quot;: &quot;없음&quot;,<br>  &quot;설명&quot;: &quot;화면은 눈이 내리는 날의 공원이나 주차장을 보여주고 있으며, 사람과 차량이 있는 것으로 보이며, 위험 요소는 없습니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_parking5.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_parking5.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;정상&quot;,<br>  &quot;유형&quot;: &quot;없음&quot;,<br>  &quot;설명&quot;: &quot;화면에는 주차된 자동차들과 건물이 보이며, 아무런 위험 요소가 나타나고 있지 않습니다. CCTV 영상은 재난 상황을 반영하지 않으며, 정상적인 주차장 환경을 보여줍니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker1.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker1.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;정상&quot;,<br>  &quot;유형&quot;: &quot;없음&quot;,<br>  &quot;설명&quot;: &quot;재난 현장의 엣지 카메라 영상에서 보이는 장면은 안전한 작업 환경을 나타내며, 작업자들이 안전한 위치에 있으며, 주변에는 물건이 정돈되어 있는 것으로 보입니다. 이는 위험 요소가 없는 상태로 판단됩니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker2.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker2.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;정상&quot;,<br>  &quot;유형&quot;: &quot;없음&quot;,<br>  &quot;설명&quot;: &quot;영상은 재난 현장의 엣지 카메라 영상으로, 작업 중인 인물과 장비가 보이며, 화재나 낙상, 전도 등의 위험 요소는 나타나 있지 않습니다. 장비와 인물의 움직임은 정상적인 작업 상태로 보입니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker3.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker3.mp4 · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;정상&quot;,<br>  &quot;유형&quot;: &quot;없음&quot;,<br>  &quot;설명&quot;: &quot;재난 현장의 엣지 카메라 영상은 공장 내부의 저장 공간을 보여주고 있으며, 작업 중인 장비와 인원이 보입니다. 화재, 낙상, 전도 등의 위험 요소는 나타나지 않으며, 현재 상황은 안전한 상태입니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/normal_worker_4.jpg"></div><div class="cap-body"><div class="cap-head">[video] normal_worker_4.mp4 · 정답 정상 · 판정 위험(낙상) ❌</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;낙상&quot;,<br>  &quot;설명&quot;: &quot;영상에서 재난 현장의 한 장면으로 보이는 화면은 무너진 구조물과 함께 파손된 물건들이 떨어져 있는 것을 보여줍니다. 이는 재난 발생 후의 상태로, 구조물의 붕괴와 함께 많은 물건이 무너졌음을 의미합니다. 이는 매우 심각한 위험을 나타냅니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall1.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall1.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;정상&quot;,<br>  &quot;유형&quot;: &quot;없음&quot;,<br>  &quot;설명&quot;: &quot;영상은 상점 내부에서 고객과 직원이 상점 결제 장소에서 상품을 거래하는 장면을 보여줍니다. 이는 일반적인 상점 운영 상황이며, 재난 현장에서 발생하는 위험 요소가 포함되어 있지 않습니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall2.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall2.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;낙상&quot;,<br>  &quot;설명&quot;: &quot;카메라 영상에서 남성 한 명이 무릎을 꿇고 바닥에 떨어진 상태로 보이며, 그의 몸이 바닥에 닿아 있는 것으로 보아 낙상의 위험이 있습니다. 이는 재난 현장에서의 위험 요소로 간주됩니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall3.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall3.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;정상&quot;,<br>  &quot;유형&quot;: &quot;없음&quot;,<br>  &quot;설명&quot;: &quot;화면에는 사람과 자연 환경이 보이며, 아무런 위험 요소가 나타나고 있지 않습니다. 주변 환경은 평온하고 안전한 상태입니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall4.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall4.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;정상&quot;,<br>  &quot;유형&quot;: &quot;없음&quot;,<br>  &quot;설명&quot;: &quot;영상은 엣지 카메라로 촬영된 것으로, 사람들이 엘리베이터를 이용하고 있는 장면을 보여줍니다. 이는 일반적인 상황이며, 재난 현장에서 발생할 수 있는 위험 요소가 아닙니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/person_fall5.jpg"></div><div class="cap-body"><div class="cap-head">[video] person_fall5.mp4 · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;낙상&quot;,<br>  &quot;설명&quot;: &quot;영상에서 승강기 안에 사람이 떨어져 내려오는 상황이 발생하고 있으며, 이는 매우 위험한 상황을 나타냅니다. 사람들은 승강기 안에서 떨어질 수 있는 위험을 인식하지 못하고, 이는 재난 상황의 일환입니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke1.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke1.mp4 · 정답 위험 · 판정 불명(화재) ∅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;화재&quot;,<br>  &quot;유형&quot;: &quot;화재&quot;,<br>  &quot;설명&quot;: &quot;화재가 발생한 것으로 보이며, 빛이 나는 불꽃과 연기, 그리고 화재 대응 팀의 활동이 확인됩니다. 이는 재난 현장에서 발생한 것으로 보입니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke2.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke2.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;화재&quot;,<br>  &quot;설명&quot;: &quot;화재/소각 감지 알림이 표시되어 있으며, 작업 중인 인원이 화재 발생 시 즉각적인 대응을 요구합니다. 화재가 발생했음을 알리는 시스템이 작동하고, 이는 위험 상황을 나타냅니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke3.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke3.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;화재&quot;,<br>  &quot;설명&quot;: &quot;영상에서 녹색 숲의 일부가 연기로 가득 차 있으며, 이는 화재 발생의 징후입니다. 연기는 공기 중에 확산되어 있어 주변 환경에 위험을 초래할 수 있습니다. 이는 매우 심각한 상황이며, 즉시 대응이 필요합니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke4.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke4.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;화재&quot;,<br>  &quot;설명&quot;: &quot;화면에는 건물들이 있으며, 그 중 일부는 검은 연기로 뒤덮여 있습니다. 이는 화재 발생의 징후로 보이며, 주변 환경은 위험한 상태입니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke5.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke5.mp4 · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;정상&quot;,<br>  &quot;유형&quot;: &quot;없음&quot;,<br>  &quot;설명&quot;: &quot;화면에는 산업 복합체가 보이며, 연기와 배출구가 있는 것으로 보아 화재나 낙상 등의 위험이 존재하지 않습니다. 전체적인 상태는 안전하고 정상적인 모습을 보이고 있습니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire1.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire1.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;화재&quot;,<br>  &quot;설명&quot;: &quot;화재가 발생한 것으로 보이며, 화재는 큰 규모의 연기와 불꽃을 내고 있습니다. 화재가 발생한 장소는 박스와 같은 물건들이 쌓여 있는 공간으로 보이며, 이는 재난 상황을 악화시키고 있습니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire2.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire2.mp4 · 정답 위험 · 판정 정상(화재) ❌</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;정상&quot;,<br>  &quot;유형&quot;: &quot;화재&quot;,<br>  &quot;설명&quot;: &quot;화재가 발생한 장소는 대형 백화점의 저장실로 보이며, 화재는 빛을 내고 있으며, 주변에는 수많은 상자들이 쌓여 있습니다. 화재가 발생한 후, 스프링클러 시스템이 작동하여 화재를 진압했습니다. 화재는 10분 안에 진압되었으며, 화재의 심각도는 매우 높습니다. 이는 화재가 발생한 장소에서 스프링클러 시스템이 작동하는 것을 확인할 수 있습니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire3.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire3.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;화재&quot;,<br>  &quot;설명&quot;: &quot;화재가 발생한 것으로 보이며, 건물의 외벽에서 연기가 떠오르고, 불꽃이 번쩍이는 모습이 확인된다. 이는 매우 심각한 화재로, 즉시 대응이 필요하다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/video_thumbs/smoke_fire4.jpg"></div><div class="cap-body"><div class="cap-head">[video] smoke_fire4.mp4 · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;화재&quot;,<br>  &quot;설명&quot;: &quot;화재는 화염이 발생하고 있으며, 빛을 내는 불꽃이 보입니다. 이는 매우 심각한 위험을 나타냅니다. 화재가 발생한 장소는 대규모의 전시회장 내부이며, 사람들이 빠르게 이동하고 있는 상황입니다. 이는 즉각적인 안전 조치가 필요합니다.&quot;<br>}<br>```</div></div></div>
