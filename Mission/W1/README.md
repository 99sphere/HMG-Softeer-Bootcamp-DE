# Week 1 (Pandas, Matplotlib, SQL)
## Environment Setting (venv with Jupyter)
### venv 가상환경 생성, activate, deactivate
#### create virtual env 

```
python3 -m venv {virtual env name}
```

#### activate & deactivate
```
source {virtual env name}/bin/activate
```

```
deactivate
```

### Jupyter Lab에 kernel 추가
```
python3 -m ipykernel install --user --name [virtual env name] --display-name [jupyter kernel name]
```

### Jupyter Lab에서 kernel 제거
```
jupyter kernelspec list (존재하는 kernel 확인)
jupyter kernelspec uninstall {jupyter kernel name}
```

## Intro to Pandas and Matplotlib
### Data Processing (with pandas)
#### Analysis
- df.info: column name, dtype 등 확인
- df.columns: 존재하는 column들의 이름 확인
- df.describe: statistical한 정보 확인 (mean, std, ..., etc)
- df.corr: column별 correlation을 확인
- 기타 column 별 연산 모두 가능

#### Manipulate
- column 삽입 -> df['key'] = values 
- df.rename: column 이름 변경
- idx로 indexing 할 때는 iloc, condition으로 indexing 할 때는 loc
- stack, unstack으로 multi-index 생성 및 해제 가능
    ```
    df.loc[df.Region=="Asia"].iloc[:5]
    ```

### Visualize (with matplotlib)
- df.plot() -> line, bar, hist, scatter 등 matplotlib으로 그릴 수 있는 건 대부분 가능
- df.hist() -> 여러 개의 column에 대한 histogram을 아래 처럼 한번에 생성
![image](https://github.com/99sphere/2024-Spring-System-Programming/assets/59161083/e097f655-9366-4adb-8740-b5dec66b93cf)
- option들이 matplot과 거의 동일함.

## Intro to SQL
- [SQL Tutorial](https://www.w3schools.com/sql/default.asp)
- DB Browser, Data Grip 같은 tool들로 생성한 DB에 저장된 정보들 쉽게 확인 가능
- [간단한 명령어 참고](https://github.com/99sphere/HMG_DataEngineering/blob/main/Mission/W1/mission2.ipynb)
- 더 복잡한 상황 연습을 위해 프로그래머스 연습 문제 푸는 중

## Concepts
### ETL
#### Extract
기존의 DB, 웹사이트, SaaS 등에서 raw data를 수집하는 과정.

#### Transform
수집한 raw data를 목적에 맞게 가공하는 과정. (ex. 비정형 데이터를 정형 데이터로 가공, 모든 feature 중 유의미한 feature만 추출, 의도에 맞게 정렬, 중복 데이터 제거 등)

#### Load
목적에 맞게 가공된 데이터를 데이터 저장소에 저장.

## Team Discussion
- (mtcars) 데이터셋 분석을 통해 얻을 수 있는 경제적 가치
  - 목적에 맞는 차량 spec 결정이 용이해진다.
    - 연비가 낮은 차량을 만드는 것이 목적이라면, 무게는 가볍게, 마력을 작게 할수록 연비가 높아진다는 점을 이용할 수 있다. 

- (mtcars) 상관관계가 높은 조합에서 얻을 수 있는 결론
  - 양의 상관관계가 가장 큰 조합: cylinder 수와 배기량
  - 음의 상관관계가 가장 큰 조합: 연비와 무게
  - 큰 상관관계를 가지는 특징들은 너무 당연한 것들이라 유의미한 분석을 하기 어려울 수 있다.

- (world economy) wikipedia 대신, 직접 데이터를 얻으려면?
  - 공식적으로 제공하는 API가 있는 지 확인, 없으면 똑같은 방식으로 crawling.

- (world economy) 데이터가 갱신된다면, 과거의 데이터는?
  - 데이터베이스에 저장할 때 갱신하는 날짜를 같이 저장해서 구분할 수 있도록 한다.