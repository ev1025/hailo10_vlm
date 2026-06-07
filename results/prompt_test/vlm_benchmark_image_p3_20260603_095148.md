# 엣지 VLM 해석 평가 (P3)

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
| Qwen3-VL-2B-Instruct | ✅ 7.86s | 76% | 74% | 10% | 3.39s | 31.8 | 4546 MB |

## Qwen3-VL-2B-Instruct — `Qwen/Qwen3-VL-2B-Instruct`

**위험 유형별 인식 (카테고리별 정답률)**

| 카테고리 | 정답유형 | N | 위험판정 | 판정정답률 | 유형정답률 | 미상 |
|---|---|---|---|---|---|---|
| 화재 | 화재 | 6 | 6 | 100% | 100% | 0 |
| 연기 | 화재 | 7 | 4 | 57% | 71% | 2 |
| 사람 쓰러짐/낙상 | 낙상 | 5 | 4 | 80% | 100% | 0 |
| 기계·장비 전도 | 전도 | 6 | 3 | 50% | 0% | 3 |
| 정상 주차장(오탐 테스트) | 없음 | 5 | 0 | 100% | 100% | 0 |
| 정상 작업장(오탐 테스트) | 없음 | 5 | 1 | 80% | 80% | 0 |

**항목별 결과**

| 유형 | 정답 | 판정 | 정오 | 시간 | 해석(앞부분) |
|---|---|---|---|---|---|
| 화재 | 위험 | 위험 | ✅ | 3.0s | 화재는 화재가 발생하고 있는 것으로 보이며, 주변의 물체들이 불에 빠지고 있는 것을 확인할 수 있습… |
| 화재 | 위험 | 위험 | ✅ | 2.9s | 화재가 발생한 것으로 보이며, 화재는 방 안에서 빛을 내고 있으며, 한 명의 인물이 화재를 감지하고… |
| 화재 | 위험 | 위험 | ✅ | 2.9s | 화재 현장에서 소방관이 화재를 진압하고 있으며, 빛나는 불꽃과 연기로 인해 매우 위험한 상황을 보이… |
| 화재 | 위험 | 위험 | ✅ | 3.0s | 화면 왼쪽 상단에는 강력한 불꽃이 떠오르고 있으며, 주변 환경이 붉은색으로 변해 있어 매우 위험한 … |
| 화재 | 위험 | 위험 | ✅ | 4.3s | 화재는 차량의 후방에 발생하고 있으며, 빛나는 불과 검은 연기로 인해 매우 위험한 상황을 나타냅니다… |
| 화재 | 위험 | 위험 | ✅ | 3.7s | 흰색 Mini Cooper 차량의 왼쪽 앞부분에서 빛나는 불과 검은 연기로 인해 화재가 발생하고 있… |
| 낙상 | 위험 | 위험 | ✅ | 3.2s | 화면에 보이는 장비는 Volvo 브랜드의 건설용 기계로, 지형이 어려운 산악 지역에서 무단으로 떨어… |
| 낙상 | 위험 | 위험 | ✅ | 2.4s | 트럭이 완전히 뒤집혀 있으며, 지하철이나 건물 등에 닿는 것을 방지하기 위해 조치가 필요합니다." … |
| 낙상 | 위험 | 불명 | ∅ | 4.1s | 화면에 보이는 장비는 포크세터로, 그 위에 있는 무게가 큰 물체를 들고 있는 상태이며, 이 물체가 … |
| 낙상 | 위험 | 불명 | ∅ | 4.2s | 화면에 보이는 장비는 트럭과 농업 장비가 있는 장소에서 발생한 사고로 보이며, 이는 장비가 무단으로… |
| 낙상 | 위험 | 위험 | ✅ | 2.7s | 화면에 보이는 인물은 무게가 큰 물건을 운반하는 자동차를 사용하고 있으며, 그 물건이 떨어질 위험이… |
| 낙상 | 위험 | 불명 | ∅ | 4.1s | 화면에 보이는 장비는 바닥에 뒤집혀 있으며, 이는 낙상 상태를 나타냅니다. 장비는 무단으로 바닥에 … |
| 없음 | 정상 | 정상 | ✅ | 2.9s | 화면에는 차량이 주차된 공원 형태의 주차장이 보이며, 사람들은 주차장 안에서 일정한 행동을 하고 있… |
| 없음 | 정상 | 정상 | ✅ | 2.7s | 영상은 주차장 내부의 실내 환경을 보여주며, 차량들이 정해진 위치에 주차되어 있으며, 인물이나 불꽃… |
| 없음 | 정상 | 정상 | ✅ | 2.1s | 화면에는 차량들이 주차된 것으로 보이며, 인근에는 사람이나 특별한 활동이 없으며, 화재나 낙상, 전… |
| 없음 | 정상 | 정상 | ✅ | 2.4s | 화면에는 차량이 주차된 것으로 보이며, 주변 환경은 안전하다. 다만, 일부 스크린 오류가 발생했을 … |
| 없음 | 정상 | 정상 | ✅ | 2.5s | 화면에는 주차된 차량들이 있으며, 주차 공간 내부에 CCTV 카메라가 설치되어 있습니다. 현재는 아… |
| 없음 | 정상 | 정상 | ✅ | 3.5s | 화면에는 공장 내부의 물류 작업 장면이 보이며, 직원들이 상자와 패키지를 처리하고 있습니다. 주변에… |
| 없음 | 정상 | 정상 | ✅ | 3.1s | 화면에는 재난 현장의 엣지 카메라 영상이 제공되며, 작업 공간 내부의 물건과 인물들이 보입니다. 그… |
| 낙상 | 정상 | 위험 | ❌ | 3.1s | 화면 상단에서 한 사람이 높은 곳에 서 있으며, 그 아래쪽에는 작업대가 있는 공간이 보입니다. 이 … |
| 없음 | 정상 | 정상 | ✅ | 2.7s | 화면은 공장 내부의 직장 환경을 보여주며, 작업 중인 직원들이 생산 작업을 하고 있으며, 안전 장비… |
| 없음 | 정상 | 정상 | ✅ | 2.6s | 화면은 재난 현장의 엣지 카메라 영상이 아님. 두 사람이 밀폐된 공간에서 상자들을 운반하고 있으며,… |
| 낙상 | 위험 | 위험 | ✅ | 4.2s | 화재, 낙상, 전도, 없음 중 택 1\n화면에 보이는 객체는 노동자와 장비입니다.\n위험 판단의 근… |
| 낙상 | 위험 | 정상 | ❌ | 3.8s | 재난 현장에서 작업 중인 인물이 쓰레기와 돌로 뒤덮인 지대에 넘어져 있으며, 다른 인물이 그를 구조… |
| 낙상 | 위험 | 위험 | ✅ | 3.1s | 화면 하단에는 작업복을 입고 있는 인물이 바닥에 무릎을 꿇고 있으며, 이는 'person_fall'… |
| 낙상 | 위험 | 위험 | ✅ | 2.2s | 영상에서 한 사람이 바닥에 넘어져 있는 상태로, 'Person_Fall' 클래스로 인식되어 있으며,… |
| 낙상 | 위험 | 위험 | ✅ | 3.7s | 사람이 바닥에 떨어져 있는 상태로, 그는 베이스 오브 스타일의 소파를 기반으로 하며, 바닥에 떨어진… |
| 화재 | 위험 | 불명 | ∅ | 4.8s | 화재가 발생한 것으로 보이며, 화재의 증거로는 연기와 함께 인물들이 무릎을 꿇고 있는 상황이 있습니… |
| 화재 | 위험 | 불명 | ∅ | 4.7s | 화재는 화재 발생 시, 화재가 발생한 장소에서 빠르게 발생하는 연기와 불꽃이 관찰됩니다. 이는 화재… |
| 화재 | 위험 | 위험 | ✅ | 5.3s | 화재는 차량의 앞부분에서 발생하고 있으며, 차량의 앞부분에 연기와 함께 불꽃이 떠오르고 있습니다. … |
| 없음 | 위험 | 정상 | ❌ | 5.0s | 화면에는 재난 현장의 엣지 카메라 영상이 아닌, 산업용 저장고 내부의 장면이 담겨 있습니다. 이곳은… |
| 화재 | 위험 | 위험 | ✅ | 2.6s | 비행기 앞쪽 바닥에 있는 장비가 연기가 나는 상태이며, 이는 화재 발생의 징후로 보입니다. 장비는 … |
| 화재 | 위험 | 위험 | ✅ | 3.3s | 화재가 발생한 것으로 보이며, 화재는 상단의 선반 위에 있는 물건들에서 발생하고 있으며, 빛을 내고… |
| 낙상 | 위험 | 위험 | ✅ | 4.3s | 화재는 나타나지 않으며, 전도도 없으며, 화재와 관련된 특징은 없습니다. 그러나 인물이 바닥에 누워… |

## 상세 내역 

### Qwen3-VL-2B-Instruct

<div class="capture"><div class="cap-img"><img src="../../dataset/images/fire1.jpg"></div><div class="cap-body"><div class="cap-head">[image] fire1.jpg · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;화재&quot;,<br>  &quot;설명&quot;: &quot;화재는 화재가 발생하고 있는 것으로 보이며, 주변의 물체들이 불에 빠지고 있는 것을 확인할 수 있습니다. 화재의 빛과 연기로 인해 주변 환경이 매우 위험하게 보입니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/fire2.jpg"></div><div class="cap-body"><div class="cap-head">[image] fire2.jpg · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;화재&quot;,<br>  &quot;설명&quot;: &quot;화재가 발생한 것으로 보이며, 화재는 방 안에서 빛을 내고 있으며, 한 명의 인물이 화재를 감지하고 있는 상황입니다. 이는 매우 위험한 상황이며, 즉시 구조 및 소방 서비스의 개입이 필요합니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/fire3.jpg"></div><div class="cap-body"><div class="cap-head">[image] fire3.jpg · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;화재&quot;,<br>  &quot;설명&quot;: &quot;화재 현장에서 소방관이 화재를 진압하고 있으며, 빛나는 불꽃과 연기로 인해 매우 위험한 상황을 보이고 있습니다. 화재의 심각성은 매우 높으며, 소방관은 즉각적인 대응이 필요합니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/fire4.jpg"></div><div class="cap-body"><div class="cap-head">[image] fire4.jpg · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;화재&quot;,<br>  &quot;설명&quot;: &quot;화면 왼쪽 상단에는 강력한 불꽃이 떠오르고 있으며, 주변 환경이 붉은색으로 변해 있어 매우 위험한 상황을 나타냅니다. 이는 화재가 발생한 것으로, 즉시 구조대와 소방대의 개입이 필요합니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/fire5.jpg"></div><div class="cap-body"><div class="cap-head">[image] fire5.jpg · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;화재&quot;,<br>  &quot;설명&quot;: &quot;화재는 차량의 후방에 발생하고 있으며, 빛나는 불과 검은 연기로 인해 매우 위험한 상황을 나타냅니다. 차량은 완전히 타오르고 있으며, 주변에는 사람들이 모여 있는 것으로 보아 경찰이나 구조대가 대응할 필요가 있습니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/fire6.jpg"></div><div class="cap-body"><div class="cap-head">[image] fire6.jpg · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;화재&quot;,<br>  &quot;설명&quot;: &quot;흰색 Mini Cooper 차량의 왼쪽 앞부분에서 빛나는 불과 검은 연기로 인해 화재가 발생하고 있으며, 차량은 주차된 도로 위에 위치하고 있습니다. 불과 연기는 차량의 앞부분에 집중되어 있어, 즉시 대응이 필요합니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/machine_tipover1.webp"></div><div class="cap-body"><div class="cap-head">[image] machine_tipover1.webp · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;낙상&quot;,<br>  &quot;설명&quot;: &quot;화면에 보이는 장비는 Volvo 브랜드의 건설용 기계로, 지형이 어려운 산악 지역에서 무단으로 떨어졌습니다. 작업자들은 이 장비를 안전하게 지키기 위해 대응하고 있으며, 이는 매우 위험한 상황을 나타냅니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/machine_tipover2.jpg"></div><div class="cap-body"><div class="cap-head">[image] machine_tipover2.jpg · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;낙상&quot;,<br>  &quot;설명&quot;: &quot;트럭이 완전히 뒤집혀 있으며, 지하철이나 건물 등에 닿는 것을 방지하기 위해 조치가 필요합니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/machine_tipover3.jpg"></div><div class="cap-body"><div class="cap-head">[image] machine_tipover3.jpg · 정답 위험 · 판정 불명(낙상) ∅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험과 정상 중 택 1&quot;,<br>  &quot;유형&quot;: &quot;낙상&quot;,<br>  &quot;설명&quot;: &quot;화면에 보이는 장비는 포크세터로, 그 위에 있는 무게가 큰 물체를 들고 있는 상태이며, 이 물체가 떨어질 가능성이 매우 높습니다. 이는 위험한 상황을 의미하며, 즉시 조치가 필요합니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/machine_tipover4.jpg"></div><div class="cap-body"><div class="cap-head">[image] machine_tipover4.jpg · 정답 위험 · 판정 불명(낙상) ∅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험과 정상 중 택 1&quot;,<br>  &quot;유형&quot;: &quot;낙상&quot;,<br>  &quot;설명&quot;: &quot;화면에 보이는 장비는 트럭과 농업 장비가 있는 장소에서 발생한 사고로 보이며, 이는 장비가 무단으로 떨어졌거나, 운행 중에 부딪혔을 가능성이 있습니다. 이는 위험한 상황으로 판단됩니다. 사고의 원인은 명확하지 않지만, 장비의 안전성 문제와 관련된 것으로 보입니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/machine_tipover5.jpg"></div><div class="cap-body"><div class="cap-head">[image] machine_tipover5.jpg · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;낙상&quot;,<br>  &quot;설명&quot;: &quot;화면에 보이는 인물은 무게가 큰 물건을 운반하는 자동차를 사용하고 있으며, 그 물건이 떨어질 위험이 있습니다. 이는 재난 현장에서의 위험 요소로 간주됩니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/machine_tipover6.jpg"></div><div class="cap-body"><div class="cap-head">[image] machine_tipover6.jpg · 정답 위험 · 판정 불명(낙상) ∅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험과 정상 중 택 1&quot;,<br>  &quot;유형&quot;: &quot;낙상&quot;,<br>  &quot;설명&quot;: &quot;화면에 보이는 장비는 바닥에 뒤집혀 있으며, 이는 낙상 상태를 나타냅니다. 장비는 무단으로 바닥에 떨어졌으며, 주변에는 물건들이 놓여 있습니다. 이는 매우 심각한 위험을 초래할 수 있는 상황입니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_parking1.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_parking1.jpg · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;정상&quot;,<br>  &quot;유형&quot;: &quot;없음&quot;,<br>  &quot;설명&quot;: &quot;화면에는 차량이 주차된 공원 형태의 주차장이 보이며, 사람들은 주차장 안에서 일정한 행동을 하고 있습니다. 주차장 내부는 정돈되어 있으며, 차량 사이에 문제가 발생하지 않아 위험 요소가 없습니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_parking2.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_parking2.jpg · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;정상&quot;,<br>  &quot;유형&quot;: &quot;없음&quot;,<br>  &quot;설명&quot;: &quot;영상은 주차장 내부의 실내 환경을 보여주며, 차량들이 정해진 위치에 주차되어 있으며, 인물이나 불꽃, 화재 등 위험 요소가 존재하지 않습니다. 전체적인 상태는 안전하고 정상적입니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_parking3.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_parking3.jpg · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;정상&quot;,<br>  &quot;유형&quot;: &quot;없음&quot;,<br>  &quot;설명&quot;: &quot;화면에는 차량들이 주차된 것으로 보이며, 인근에는 사람이나 특별한 활동이 없으며, 화재나 낙상, 전도 등의 위험이 존재하지 않습니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_parking4.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_parking4.jpg · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;정상&quot;,<br>  &quot;유형&quot;: &quot;없음&quot;,<br>  &quot;설명&quot;: &quot;화면에는 차량이 주차된 것으로 보이며, 주변 환경은 안전하다. 다만, 일부 스크린 오류가 발생했을 수 있으나, 현재는 위험 요소가 없습니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_parking5.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_parking5.jpg · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;정상&quot;,<br>  &quot;유형&quot;: &quot;없음&quot;,<br>  &quot;설명&quot;: &quot;화면에는 주차된 차량들이 있으며, 주차 공간 내부에 CCTV 카메라가 설치되어 있습니다. 현재는 아무런 위험 요소나 이상 현상이 관찰되지 않으며, 주차 공간은 안전하게 유지되고 있습니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_worker1.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_worker1.jpg · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;정상&quot;,<br>  &quot;유형&quot;: &quot;없음&quot;,<br>  &quot;설명&quot;: &quot;화면에는 공장 내부의 물류 작업 장면이 보이며, 직원들이 상자와 패키지를 처리하고 있습니다. 주변에는 수많은 상자와 포장된 제품이 쌓여 있으며, 작업 중인 직원들은 안전한 상태로 보입니다. 이는 일반적인 재고 관리나 포장 작업의 일상적인 활동으로, 위험 요소가 없습니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_worker2.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_worker2.jpg · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;정상&quot;,<br>  &quot;유형&quot;: &quot;없음&quot;,<br>  &quot;설명&quot;: &quot;화면에는 재난 현장의 엣지 카메라 영상이 제공되며, 작업 공간 내부의 물건과 인물들이 보입니다. 그러나 화재, 낙상, 전도 등의 위험 요소가 관찰되지 않으며, 장비와 사람들은 안전하게 움직이고 있습니다. 따라서 &#x27;없음&#x27;을 판단합니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_worker3.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_worker3.jpg · 정답 정상 · 판정 위험(낙상) ❌</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;낙상&quot;,<br>  &quot;설명&quot;: &quot;화면 상단에서 한 사람이 높은 곳에 서 있으며, 그 아래쪽에는 작업대가 있는 공간이 보입니다. 이 사람은 높은 위치에서 떨어질 수 있는 위험이 있습니다. 또한, 작업대 위에는 여러 가지 장비와 물건들이 놓여 있어, 위험한 상태로 보입니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_worker4.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_worker4.jpg · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;정상&quot;,<br>  &quot;유형&quot;: &quot;없음&quot;,<br>  &quot;설명&quot;: &quot;화면은 공장 내부의 직장 환경을 보여주며, 작업 중인 직원들이 생산 작업을 하고 있으며, 안전 장비나 위험 요소는 보이지 않습니다. 따라서 이는 재난 현장의 엣지 카메라 영상으로 판단됩니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/normal_worker5.jpg"></div><div class="cap-body"><div class="cap-head">[image] normal_worker5.jpg · 정답 정상 · 판정 정상(없음) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;정상&quot;,<br>  &quot;유형&quot;: &quot;없음&quot;,<br>  &quot;설명&quot;: &quot;화면은 재난 현장의 엣지 카메라 영상이 아님. 두 사람이 밀폐된 공간에서 상자들을 운반하고 있으며, 이는 일반적인 물류 작업의 일환으로 보이며, 위험 요소가 존재하지 않음.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/person_fall1.jpg"></div><div class="cap-body"><div class="cap-head">[image] person_fall1.jpg · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;낙상&quot;,<br>  &quot;설명&quot;: &quot;화재, 낙상, 전도, 없음 중 택 1\n화면에 보이는 객체는 노동자와 장비입니다.\n위험 판단의 근거는 노동자가 화물차 옆에 무릎을 꿇고 넘어져 있는 상황입니다.\n심각도는 매우 높습니다.\n필요한 조치는 즉각적인 구조적 안전 조치와 함께, 인력의 복귀를 위한 안전 점검을 수행해야 합니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/person_fall2.webp"></div><div class="cap-body"><div class="cap-head">[image] person_fall2.webp · 정답 위험 · 판정 정상(낙상) ❌</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;정상&quot;,<br>  &quot;유형&quot;: &quot;낙상&quot;,<br>  &quot;설명&quot;: &quot;재난 현장에서 작업 중인 인물이 쓰레기와 돌로 뒤덮인 지대에 넘어져 있으며, 다른 인물이 그를 구조적 지원을 제공하고 있다. 이는 작업 중 발생한 부상 상황을 나타내며, 위험은 존재하지만 현재는 안전한 상태로 보인다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/person_fall3.jpg"></div><div class="cap-body"><div class="cap-head">[image] person_fall3.jpg · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;낙상&quot;,<br>  &quot;설명&quot;: &quot;화면 하단에는 작업복을 입고 있는 인물이 바닥에 무릎을 꿇고 있으며, 이는 &#x27;person_fall&#x27;이라고 명시된 위험 상황을 나타냅니다. 이는 직원의 안전에 대한 위험을 의미하며, 즉시 조치가 필요합니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/person_fall4.jpg"></div><div class="cap-body"><div class="cap-head">[image] person_fall4.jpg · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;낙상&quot;,<br>  &quot;설명&quot;: &quot;영상에서 한 사람이 바닥에 넘어져 있는 상태로, &#x27;Person_Fall&#x27; 클래스로 인식되어 있으며, 이는 높은 위험을 나타냅니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/person_fall5.jpg"></div><div class="cap-body"><div class="cap-head">[image] person_fall5.jpg · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;낙상&quot;,<br>  &quot;설명&quot;: &quot;사람이 바닥에 떨어져 있는 상태로, 그는 베이스 오브 스타일의 소파를 기반으로 하며, 바닥에 떨어진 상태로 보입니다. 이는 위험한 상황이며, 즉, 사람의 안전을 위협하는 상태입니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/smoke1.jpg"></div><div class="cap-body"><div class="cap-head">[image] smoke1.jpg · 정답 위험 · 판정 불명(화재) ∅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험과 정상 중 택 1&quot;,<br>  &quot;유형&quot;: &quot;화재&quot;,<br>  &quot;설명&quot;: &quot;화재가 발생한 것으로 보이며, 화재의 증거로는 연기와 함께 인물들이 무릎을 꿇고 있는 상황이 있습니다. 이는 화재가 발생한 후의 상태를 나타냅니다. 화재의 심각도는 매우 높으며, 즉시 구조 및 안전 조치가 필요합니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/smoke2.jpg"></div><div class="cap-body"><div class="cap-head">[image] smoke2.jpg · 정답 위험 · 판정 불명(화재) ∅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험과 정상 중 택 1&quot;,<br>  &quot;유형&quot;: &quot;화재&quot;,<br>  &quot;설명&quot;: &quot;화재는 화재 발생 시, 화재가 발생한 장소에서 빠르게 발생하는 연기와 불꽃이 관찰됩니다. 이는 화재가 발생한 장소에서 빠르게 발생하는 연기와 불꽃이 관찰됩니다. 이는 화재가 발생한 장소에서 빠르게 발생하는 연기와 불꽃이 관찰됩니다. 이는 화재가 발생한 장소에서 빠르게 발생하는 연기와 불꽃이 관찰됩니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/smoke3.jpg"></div><div class="cap-body"><div class="cap-head">[image] smoke3.jpg · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;화재&quot;,<br>  &quot;설명&quot;: &quot;화재는 차량의 앞부분에서 발생하고 있으며, 차량의 앞부분에 연기와 함께 불꽃이 떠오르고 있습니다. 이는 차량의 전기 시스템이나 내부 부품이 파손되었거나, 외부 환경에 의해 발생한 것으로 보입니다. 차량은 주차 상태이며, 주변에는 병원 차량이 보입니다. 이는 매우 심각한 상황이며, 즉시 구조 및 안전 조치가 필요합니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/smoke4.jpg"></div><div class="cap-body"><div class="cap-head">[image] smoke4.jpg · 정답 위험 · 판정 정상(없음) ❌</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;정상&quot;,<br>  &quot;유형&quot;: &quot;없음&quot;,<br>  &quot;설명&quot;: &quot;화면에는 재난 현장의 엣지 카메라 영상이 아닌, 산업용 저장고 내부의 장면이 담겨 있습니다. 이곳은 기름과 가스 공장의 저장 공간으로 보이며, 빛이 들어오는 창문에서 흐르는 연기와 함께 여러 층의 박스들이 정렬되어 있습니다. 이는 일반적인 산업 환경의 일상적 장면이며, 화재나 낙상 등의 위험 요소가 나타나지 않습니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/smoke5.jpg"></div><div class="cap-body"><div class="cap-head">[image] smoke5.jpg · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;화재&quot;,<br>  &quot;설명&quot;: &quot;비행기 앞쪽 바닥에 있는 장비가 연기가 나는 상태이며, 이는 화재 발생의 징후로 보입니다. 장비는 전기 기기로 보이며, 연기는 안전 상황에서의 위험을 나타냅니다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/smoke_fire1.jpg"></div><div class="cap-body"><div class="cap-head">[image] smoke_fire1.jpg · 정답 위험 · 판정 위험(화재) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;화재&quot;,<br>  &quot;설명&quot;: &quot;화재가 발생한 것으로 보이며, 화재는 상단의 선반 위에 있는 물건들에서 발생하고 있으며, 빛을 내고 있다. 화재는 매우 심각하며, 주변의 선반과 기계가 위험에 처해 있다.&quot;<br>}<br>```</div></div></div>
<div class="capture"><div class="cap-img"><img src="../../dataset/images/smoke_fire2.jpg"></div><div class="cap-body"><div class="cap-head">[image] smoke_fire2.jpg · 정답 위험 · 판정 위험(낙상) ✅</div><div class="cap-text">```json<br>{<br>  &quot;판정&quot;: &quot;위험&quot;,<br>  &quot;유형&quot;: &quot;낙상&quot;,<br>  &quot;설명&quot;: &quot;화재는 나타나지 않으며, 전도도 없으며, 화재와 관련된 특징은 없습니다. 그러나 인물이 바닥에 누워 있는 상태로, 이는 낙상의 가능성을 의미합니다. 이는 위험한 상황이며, 즉, 인물이 위험한 위치에서 떨어졌거나, 무단으로 떨어져 있음을 의미합니다.&quot;<br>}<br>```</div></div></div>
