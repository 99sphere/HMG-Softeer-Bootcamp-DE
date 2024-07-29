## 주제
- New York 지역에서, WAV 차량의 호출량 예측하기
- 사용 데이터셋
    - TLC 데이터셋
    - 날씨 관련 정보
    - 지역 축제 관련 정보
    
    ![IMG_7537322C5932-1.jpeg](https://prod-files-secure.s3.us-west-2.amazonaws.com/d5fbc738-7e70-4fc4-8ccb-71d1fde36e4c/a0d12122-e314-443b-b775-961dcf1c4420/IMG_7537322C5932-1.jpeg)
    

## Intro
- 미국에서는 매년 7월을 ‘장애인을 위한 달’ / ‘장애인 인식 개선을 위한 달’로써 행사를 많이 진행한다.
- 해당 사이드 프로젝트의 최종 목표인 ‘WAV 차량 수요 분석 및 예측’을 위해서는 ML/DL 기반의 예측 모델이 필요하다. 학습에 필요한 컬럼을 선별하는 과정에서 어떤 파생변수를 추가할 수 있을지에 대하여 목표를 두고 시각화를 진행하였음.

## 평일 / 주말별 수요 예측 시각화 (groupBy Day)
![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/d5fbc738-7e70-4fc4-8ccb-71d1fde36e4c/c4f4c817-aca9-45d3-b72d-1e1429582174/Untitled.png)

![스크린샷 2024-07-29 오후 5.11.15.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/d5fbc738-7e70-4fc4-8ccb-71d1fde36e4c/ffa9b943-b29c-41f1-baf2-5a82e4bd1b34/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA_2024-07-29_%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE_5.11.15.png)

- 평일은 주황색, 주말은 하늘색으로 막대그래프의 색상을 변경하여 시각화에 활용하였음.
- 평일 / 주말 별로 WAV 차량 수요 예측 결과를 시각화하기 위해 연속적인 3달 (6, 7, 8)을 추출하여 경향성을 파악해보았으며, 모든 달에서 평일이 주말보다 더 많은 사용자가 있다는 사실을 인지함
- 이에 따라, 특정 일시 (ex - 20240701)에 수요 예측을 진행하고 싶다면 평일 / 주말 여부가 중요한 역할을 한다고 판단했으며, 해당 파생변수를 활용할 수 있을 것이라 예상함.

## 계절(여름/겨울)별  수요 예측 시각화 (groupBy Hour)
![스크린샷 2024-07-29 오후 6.09.27.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/d5fbc738-7e70-4fc4-8ccb-71d1fde36e4c/4909acc9-b15c-4c38-91ec-2f5668557ab4/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA_2024-07-29_%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE_6.09.27.png)

![스크린샷 2024-07-29 오후 6.10.53.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/d5fbc738-7e70-4fc4-8ccb-71d1fde36e4c/67444107-9cae-4f52-bc69-5d81fd7a0be6/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA_2024-07-29_%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE_6.10.53.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/d5fbc738-7e70-4fc4-8ccb-71d1fde36e4c/4f17faf2-dd4b-47f0-a641-999d79b77402/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/d5fbc738-7e70-4fc4-8ccb-71d1fde36e4c/e77db03b-f04c-4c99-996d-87685f1b2d83/Untitled.png)

- 위 - 여름 (2023년 7월) / 아래 - 겨울 (2023년 1월)
- 좌 - 평일 / 우 - 주말
- 여름과 겨울 모두 평일보다 주말에, 늦은 시간대의 이용 횟수가 높다.
- 여름, 겨울 모두 주말/평일에 시간대별 수요가 눈에 띄게 달라지므로, 시간대별 수요 예측을 진행한다면 평일/주말 여부도 예측을 위한 feature로 사용해야 할 것이다.

## 날씨 관련 (TO DO)