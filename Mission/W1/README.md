# Week 1 (Pandas, Matplotlib, SQL)
## 1. Environment Setting (venv with Jupyter)
### 1.1. venv 가상환경 생성, activate, deactivate
#### 1.1.1. create virtual env
```
python3 -m venv {virtual env name}
```
#### 1.1.2. activate
```
source {virtual env name}/bin/activate
```
#### 1.1.3. deactivate
```
deactivate
```
### 1.2. Jupyter Lab에 kernel 추가
```
python3 -m ipykernel install --user --name [virtual env name] --display-name [jupyter kernel name]
```
### 1.3. Jupyter Lab에서 kernel 제거
```
jupyter kernelspec list (존재하는 kernel 확인)
jupyter kernelspec uninstall {jupyter kernel name}
```
## 2. Intro to Pandas and Matplotlib
### 2.1. Data Processing (with pandas)
#### 2.1.1. Analysis
- df.info: column name, dtype 등 확인
- df.columns: 존재하는 column들의 이름 확인
- df.describe: statistical한 정보 확인 (mean, std, ..., etc)
- df.corr: column별 correlation을 확인
- 기타 column 별 연산 모두 가능
#### 2.1.2. Manipulate
- column 삽입 -> df['key'] = values
- df.rename: column 이름 변경
- idx로 indexing 할 때는 iloc, condition으로 indexing 할 때는 loc
- stack, unstack으로 multi-index 생성 및 해제 가능
    ```
    df.loc[df.Region=="Asia"].iloc[:5]
    ```
### 2.2. Visualize (with matplotlib)
- df.plot() -> line, bar, hist, scatter 등 matplotlib으로 그릴 수 있는 건 대부분 가능
- df.hist() -> 여러 개의 column에 대한 histogram을 아래 처럼 한번에 생성
![image](https://github.com/99sphere/2024-Spring-System-Programming/assets/59161083/e097f655-9366-4adb-8740-b5dec66b93cf)
- option들이 matplot과 거의 동일함.

## 3. Intro to SQL
- [SQL Tutorial](https://www.w3schools.com/sql/default.asp)
- DB Browser, Data Grip 같은 tool들로 생성한 DB에 저장된 정보들 쉽게 확인 가능
- [간단한 명령어 참고](https://github.com/99sphere/HMG_DataEngineering/blob/main/Mission/W1/mission2.ipynb)
- 더 복잡한 상황 연습을 위해 프로그래머스 연습 문제 푸는 중
- column 명은 숫자로 대체 가능

### 3.1. 데이터 조회
#### 3.1.1. SELECT
- Table에서 column을 선택할 때 사용
```
SELECT {COLUMN NAME, ...} FROM {DB NAME}.{TABLE NAME}
```
```
SELECT * FROM {TABLE NAME} -> 모든 column 선택
```
- SUM, COUNT, AVG 등의 aggregation function을 함께 사용할 수 있다.
```
SELECT AVG(PRICE) FROM {PAYMENTS} -> 평균 price 선택
```
- "AS"를 활용하여, column 이름을 변경하여 조회할 수 있다.
```
SELECT COUNT(PRODUCT_CODE) AS N_PRODUCT FROM {PAYMENTS} -> PRODUCT_CODE를 counting 한 값의 column name을 N_PRODUCT로 변경
```
- "DISTINCT"를 활용하여, 중복을 제외한 데이터를 조회할 수 있다. 
```
SELECT DISTINCT ORDERNUMBER FROM ORDER_DETAILS
```
#### 3.1.2. WHERE
- 테이블에서 특정 조건에 맞는 데이터를 찾을 수 있다.  
- BETWEEN A AND B (A, B 포함)
```
SELECT PRODUCT_NUMBER FROM PRODUCT WHERE PRODUCT_NUMBER BETWEEN 10 AND 12
```
-  \>, <, =, <> (!=)
```
SELECT PRODUCT_NUMBER FROM PRODUCT WHERE COUNTRY="U.S.A"
```
```
SELECT PRODUCT_NUMBER FROM PRODUCT WHERE PRODUCT_NUMBER <> 13
```
- IN, NOT IN
```
SELECT PRODUCT_NUMBER FROM PRODUCT WHERE PRODUCT_NUMBER IN (10, 11, 12)
```
```
SELECT PRODUCT_NUMBER FROM PRODUCT WHERE PRODUCT_NUMBER NOT IN (9, 12)
```
-  IS NULL, IS NOT NULL
```
SELECT PRODUCT_NUMBER FROM PRODUCT WHERE PRICE IS NOT NULL
```
```
SELECT PRODUCT_NUMBER FROM PRODUCT WHERE PRODUCT_NUMBER IS NOT NULL
```

-  LIKE "%TEXT%" 등과 함께 사용한다.
  - LIKE에서 사용하는 %, _는 모든 문자를 의미한다. (wildcard) %는 0글자 이상을, _는 1글자를 허용한다. 
```
SELECT PRODUCT_NUMBER FROM PRODUCT WHERE ADDRESS LIKE "%ST%"
```

#### 3.1.3. GROUP BY
- "GROUP BY"를 활용하여, column 값들을 group화해 각 값들의 평균 값, 갯수 등을 구할 수 있다.
- 두 개 이상의 column으로도 그룹화 할 수 있다.
```
SELECT COUNTRY, AVG(PRICE) FROM CARS GROUP BY COUNTRY
```
```
SELECT COUNTRY, CITY, AVG(PRICE) FROM CARS GROUP BY COUNTRY, CITY
```

#### 3.1.4. JOIN
- 데이터는 하나의 Table에 적재되지 않는다. JOIN 명령어를 통해 다양한 Table의 데이터를 한번에 조회할 수 있다.
- LEFT JOIN, RIGHT JOIN, INNER JOIN, FULL JOIN등의 명령어를 사용할 수 있다.
```
SELECT * FROM ORDER FULL JOIN CUSTOMERS ON ORDER.CUSTOMER_ID = CUSTOMERS.CUSTOMER_ID
```

#### 3.1.5. CASE WHEN
- 조건에 따라 다른 값을 출력하고 싶을 때 사용한다.
```
SELECT 
CASE 
WHEN AGE BETWEEN 20 AND 29 THEN "20's"
WHEN AGE BETWEEN 30 AND 39 THEN "30's"
WHEN AGE BETWEEN 40 AND 49 THEN "40's"
END
FROM CUSTOMERS
```
- ELSE도 사용 가능하다.
```
SELECT COUNTRY,
CASE 
WHEN COUNTRY IN ('USA', 'Canada') THEN 'North America'
ELSE
'OTHERS'
END AS REGION
FROM CUSTOMERS
```
- GROUP BY에도 사용 가능하다.
```
SELECT CASE 
WHEN COUNTRY IN ('USA', 'Canada') THEN 'North America' 
ELSE 'OTHERS"
END AS REGION,
COUNT(CUSTOMER_NUMBER) N_CUSTOMERS
FROM CUSTOMERS
GROUP BY CASE
WHEN COUNTRY IN ('USA', 'Canada') THEN 'North America'
ELSE 'OTHERS'
END
```

#### 3.1.6. RANK, DENSE_RANK, ROW_NUMBER
- 데이터의 순위를 매기기 위해 사용하는 함수이다.
  - RANK: 같은 등수가 있는 경우, 이를 고려하여 순위를 매김. (2개가 공동 1위인 경우, 그 다음은 3위)
  - DENSE_RANK: 같은 등수가 있는 경우, 이를 고려하지 않고 순위를 매김.  (2개가 공동 1위인 경우, 그 다음은 2위)
  - ROW_NUMBER: 같은 등수가 있는 경우에도, 다르게 순위를 매긴다.
```
SELECT RANK() OVER(ORDER BY PRICE) FROM ORDERS
```
```
SELECT DENSE_RANK() OVER(ORDER BY PRICE) FROM ORDERS
```
```
SELECT ROW_NUMBER() OVER(ORDER BY PRICE) FROM ORDERS
```

#### 3.1.7. SUBQUERY
- Query안의 query여서 subquery라고 부른다.
- 다양한 위치에 사용할 수 있다.
```
SELECT ORDER_NUMBER FROM ORDERS 
WHERE CUSTOMER_NUMBER IN (SELECT CUSTOMER_NUMBER FROM CUSTOMERS WHERE CITY='NYC')
```
```
SELECT CUSTOMER_NUMBER FROM (SELECT CUSTOMER_NUMBER FROM CUSTOMERS WHERE CITY='NYC')
```

### 3.2. 데이터 추가, 삭제, 갱신, 정합성
#### 3.2.1. INSERT
- Table에 행을 추가한다.
```
INSERT INTO {table name(column 1, column 2, ...)} VALUES (value 1, value 2, ...)
```

#### 3.2.2. DELETE
- Table에서 행을 삭제한다.
```
DELETE FROM {table name} WHERE {column name}={specific value}
```

#### 3.2.3. UPDATE
- Table에 있는 데이터의 정보를 수정한다.
```
UPDATE {table name} SET {column_name}={new value} WHERE {condition}
```

#### 3.2.4. PROCEDURE
- 매크로처럼 반복되는 내용을 하나의 단위로 생성하는 것.
```
DELIMITER //
CREATE PROCEDURE SALES_MINUS()
BEGIN
UPDATE PRODUCT SET PRICE=(-1)*PRICE
WHERE CANCELED='T' AND SALES_DATE=CURDATE()-1;
END //
DELIMITER;
```

#### 3.2.5. VIEW
- 보안상의 이슈로 직접 데이터를 조회할 수 있는 권한을 줄 수 없을 때 사용한다.
- 생성된 View는 테이블과 동일하게 사용 가능하다.
```
CREATE VIEW {view name} AS SELECT ORDER_ID FROM SALES WHERE CANCELED='Y';
```

#### 3.2.6. MECE
- Mutually Exclusive Collectively Exhaustive의 줄인 말로, 중복/누락 데이터가 발생하지 않도록 분석해야 한다는 것을 의미한다.
- 각 항목들은 상호배타적이며, 이들을 하나로 모았을 때는 완전한 데이터를 구성해야 한다.
- 이에 대한 확인 없이 분석을 진행하는 경우 더 큰 비용이 발생하므로, 항상 정합성을 확인해야 한다.

## 4. Concepts & Feedback(from Lecture)
### 4.1 Concepts
### 4.1.1. ETL
#### 4.1.1.1. Extract
기존의 DB, 웹사이트, SaaS 등에서 raw data를 수집하는 과정.
#### 4.1.1.2. Transform
수집한 raw data를 목적에 맞게 가공하는 과정. (ex. 비정형 데이터를 정형 데이터로 가공, 모든 feature 중 유의미한 feature만 추출, 의도에 맞게 정렬, 중복 데이터 제거 등)
#### 4.1.1.3. Load
목적에 맞게 가공된 데이터를 데이터 저장소에 저장.

### 4.2 Feedback
#### 4.2.1. mission 1 관련

- 주어진 데이터 내에서만 뭔가를 찾아내려고 하는 것 자체가 위험한 생각일 수 있다.
- 실제로 mtcars 데이터에서 얻을 수 있는 정보 중 의미있는 것을 찾기는 어렵다.
- 판매량, 금액, 옵션 등의 정보를 추가로 구해서 사용하면, 유의미한 정보를 만들어 낼 수 있을 것이다.

#### 4.2.2. mission 2 관련
- sqlite에서 지원 안하는 명령어
    - procedure, any, all, etc
    - 다른 명령어로 비슷한 기능을 수행할 수 있다. → 필요할 때 찾아보기

#### 4.2.3. mission3 관련
- ETL 단계를 나누는 이유 → 추상화. 각 단계는 동기적으로 수행될 필요가 없고, 분업도 용이하다.
- IMF에서 GDP 정보를 update 하면, 어떻게 알 수 있을까?
    - hash
    - 직접 값 비교
- 과거 정보가 필요하다면?
    - 날짜 정보에 대한 column을 추가 (데이터 양이 충분히 많을 때, 아래 방식보다 성능이 더 좋다.)
    - 날짜별 table을 추가
- etc
    - 데이터 양이 많아지면 caching(?)도 고려해 볼 수 있다.
- communication
    - 인구 수, 1인당 GDP, 1인당 구매 가능 자본?, GDP 성장률 같은 정보들을 추가로 제공할 수 있고, 더 필요할 것 같은 정보가 있는지 추가적인 정보가 필요한 지에 대한 communication을 통한 develope이 필수.
    - Ford 사례 → 사람들은 답을 모른다. 말 타고 다니는 사람들은 자동차를 떠올리는게 쉽지 않음.

#### 4.2.4 코드 관련
    - Region 정보에 대한 processing은 extract, loading과 상관 없다. Extract 할 때, region 정보를 같이 받아오는 게 아님. 이건 다른 script에서 실행하고, mission3을 실행할 때는 이미 그 정보가 있다고 가정하고 짜야 함.
    - code와 data를 분리해라. (ex. Region info)

## 5. (Selected) Team Discussion
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
  - 데이터베이스에 저장할 때 갱신하는 날짜를 새로운 column에 저장해서 구분할 수 있도록 한다.