# README
## 📑 프로젝트 소개
경희대학교 생협 카페의 데이터를 통해 재고관리의 문제점을 찾고, 이에 대한 해결방안을 제시한다.
날씨별 음료를 추천하면 고객들이 기존의 다양한 음료보다, 추천된 음료를 소비할 것을 기대할 수 있다.


## 👏 팀 소개 
|권정혁|최용빈|도유정|최보경|
|:--:|:--:|:--:|:--:|
|[개인 리포지토리](https://github.com/khuda-3rd)|[개인 리포지토리](https://github.com/khuda-3rd)|[개인 리포지토리](https://github.com/khuda-3rd)|[개인 리포지토리](https://github.com/B0gyeong)|
|Modeling|Modeling, Serving|Modeling|Modeling|


## 🔎 핵심 기능 구현
### 1. 데이터 전처리

- 계절에 상관없이 압도적으로 높은 판매량을 자랑하는 아메리카노를 데이터에서 제거함
- 각 음료별 특성 데이터 수집에서 재료가 함유되어있으면 1, 아니면 0으로 나타낼 수 있는 feature들만 남기고 나머지는 제외
- 기온 (0,1,2,3), 운량 (0,1), 강수 여부 (0,1)을 기준으로 날씨를 16개의 범주로 그룹화

  <img width="148" alt="image" src="https://github.com/B0gyeong/khuda/assets/115474637/7792a772-b1cc-486e-9d15-dbd71bf86584">

### 2. 모델링

- 매출 데이터가 존재하는 날짜의 기온, 운량, 강수여부 데이터 수집 후 그룹별로 분류
- 각 메뉴의 판매량을 날씨 그룹별 메뉴 판매량 총합으로 나눈 뒤 각 메뉴의 가중치를 곱함
- 곱한 값을 날씨 그룹의 특성별로 다 더함 -> 인기있던 특성일수록 1에 수렴

  <img width="538" alt="image" src="https://github.com/B0gyeong/khuda/assets/115474637/a31e1a92-0bcd-4898-82e5-8d51884e015f">

### 3. 유사도 측정

(1) Cosine Similarity
- 코사인 유사도는 두 벡터가 가르키는 방향이 얼마나 유사한지에 따라 유사도를 측정
- 코사인 유사도는 -1에서 1 사이의 값을 가지며 1에 가까울수록 유사도가 높다고 할 수 있음

  <img width="211" alt="image" src="https://github.com/B0gyeong/khuda/assets/115474637/5fb3c1e6-388d-4cf3-98c8-a5e511f02489">

(2) Euclidean Distance
- 거리 기반 유사도는 좌표를 기준으로 봤을 때, 비슷한 좌표에 있는 점들이 유사도가 높다고 측정
- 유클리디안 거리는 N차원 공간에서 두 점 사이의 최단 거리를 구하기 위한 가장 기초적인 알고리즘임

  <img width="210" alt="image" src="https://github.com/B0gyeong/khuda/assets/115474637/f5458b28-1473-4b8a-8960-3f1497495d61">

(3) 상위 6개의 음료를 추천해주기로 결정
- 두가지의 방법을 다 사용한 후 더 적합하다고 생각하는 거리 기반 유사도를 사용하기로 결정
- 각 날씨별 유사도가 높은 메뉴 추출 -> 평소보다 특정 날씨에 많이 팔린 음료 알 수 없음
- 날씨별 상대적으로 인기있던 특성 이용 -> 전체 평균을 기준으로 데이터 표준화
- 원래의 데이터에서 추천된 상위 3개의 음료와 표준화된 데이터에서 추천된 상위 3개의 음료를 합쳐 총 6개의 음료를 추천하기로 결정

  <img width="488" alt="image" src="https://github.com/B0gyeong/khuda/assets/115474637/68f9034b-3632-4595-a447-899709d7f0cc">


### 4. 웹 구현

- Streamlit을 이용
- 기상청 단기예보 API를 활용하여 실시간 날씨를 받아온 후 날씨에 따른 추천 메뉴 받아옴

  <img width="327" alt="image" src="https://github.com/B0gyeong/khuda/assets/115474637/55f387b1-5297-43e0-acdf-bde9a7aabaec">

  <img width="324" alt="image" src="https://github.com/B0gyeong/khuda/assets/115474637/e64b317e-ffd4-47e8-ad70-27609d4f652b">

