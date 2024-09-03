# Week 7
## Monitoring and Optimizing Spark Job
### 1. Cayalyst Optimizer
- Rule-based engine.
- DataFrame API에 대해 작성한 logical plan을 optimized physical plan으로 다시 작성한다.
- Physical plan은 query가 실행되기 전에 develop된다.

### 2. Benefits of Catalyst Optimizer
- Java, Scala, Python, R 등으로 DataFrame또는 Dataset API를 이용하여 코드를 작성할 때, 이는 declarative API로 우리가 무엇을 하려고 하는지를 알려줄 뿐, 실제로 어떻게 동작할지에는 관여하지 않는다. (Spark SQL도 마찬가지)

- Optimize Query Plans
    - SQL Query의 logical execution plan을 분석 및 변환하여 효율적으로 실행할 수 있는 optimized physical plan을 생성한다.

- Enable Advanced Features
    - 다양한 advanced feature (ex. predicate pushdown, join reordering, constant folding 등) 지원 

- Code Generation
    - Catalyst는 Spark execution engine인 Tungsten과 함께, 이러한 plan의 최적화된 code를 생성한다.

![image](https://github.com/user-attachments/assets/8490ea7a-ff3a-4ea7-ba63-ca02dcbf004b)

### 3. How Catalyst Optimizer Works Internally
- 3.1. Parsing
    - SQL 쿼리나 DataFrame 작업은 abstract syntax tree(AST) 형태로 parsing된다.

- 3.2. Logical Plan Generation
    - AST를 logical plan으로 변환한다. 이때, logical plan은 filter, project, join과 같은 relational operator로 구성된 tree로, query에서 요구하는 계산을 나타낸다.

- 3.3. Logical Plan Optimization
    - Logical Plan은 Catalyst가 적용하는 다양한 optimization rule에 의해 아래와 같은 여러 단계의 optimization phase를 거친다. 
        - Constant Folding : compile time에 constant expression을 evaluating 하여 expression을 단순화한다.
        - Predicate Pushdown : filter를 data source에 최대한 빠르게 적용하여, 처리해야 할 데이터 양을 줄인다.
        - Join Reordering : join을 reordering하여 중간 결과의 크기를 최소화한다.
        - Projection Pruning : 불필요한 column을 제거하여 읽고, 처리하는 데이터 양을 줄인다.

- 3.4. Physical Plan Generation
    - 최적화된 logical plan은 하나 이상의 physical plan으로 변환한다. 
    - 각 physical plan은 다양한 join algorithm(ex. broadcast join, sort-merge join)과 같은 다양한 전략을 고려하여 쿼리를 실행하는 방식을 나타낸다.

- 3.5. Physical Plan Optimization
    - Catalyst는 다양한 physical plan을 비교하고 cost model을 기반으로 가장 효율적인 계획을 선택한다.
    - Cost model은 필요한 계산 리소스(예: CPU, I/O)를 추정한다.

- 3.6. Code Generation
    - 마지막으로, 선택된 physical plan은 Tungsten의 code generation 기능을 사용하여 최적화된 Java 바이트코드로 컴파일되고, 이는 Spark의 런타임 엔진에서 실행된다.

### 4. Whole-Stage Code Generation
- Apache Spark execution engine의 핵심 기능으로, Tungsten 프로젝트의 일부이다.
- 스테이지 내의 전체 transform을 single, efficient 함수로 표현하는 과정으로, 최적화된 Java bytecode를 생성한다.
- 이를 통해, logical plan을 해석하기 위한 overhead를 줄이고, 불필요한 연산에 낭비되는 CPU cycle을 최소화함으로써 성능을 높인다.

### 5. Dynamic Partition Pruning
- Dynamic Partition Pruning = Predicate Push Down + Broadcast Hash Join
- 더 작은 table이 query 및 filtering된다. 
- Spark는 이 결과를 사용하여 broadcast variable을 생성한다.
- Runtime에, Spark의 physical plan이 변경되어 dynamic filter를 더 큰 table에 적용한다. 
- Dynamic filter는 기본적으로 Spark가 더 작은 table에 적용된 filter를 기반으로 만드는 internal subquery 이다. Spark가 더 큰 table을 스캔할 때 이 dynamic filter를 적용하여 기준을 충족하지 않는 파티션을 skip하므로, 처리하는 데이터의 양이 크게 줄어든다.
- ex. 판매 기록이 존재하는 fact table과 날짜가 있는 dimension table이 존재한다고 가정
    - date table을 filtering하여 2024년 1월 날짜만 포함하도록 하면, Spark는 DPP를 사용하여 전체 sales table을 확인하는 대신, 2024년 1월의 기록이 포함된 Sales table의 partition만을 스캔한다.

![image](https://github.com/user-attachments/assets/e26d9711-5656-47a9-8b97-ca7cb004dd12)

### 6. Constraints of Dynamic Partition Pruning
- Pruning 될 table은 join key column 중 하나로 partitioning 되어 있어야 한다.
- Equi-join(조건이 '='인 조인)에서만 작동한다.
- DPP는 상관 관계가 있는 subquery에 적용되지 않는다.
- DPP는 Star-schema architecture model을 따르는 query에 유용하다.

### 7. Spark Web UI
- https://spark.apache.org/docs/latest/web-ui.html

### 8. AWS EMR Best Practices
- https://aws.github.io/aws-emr-best-practices/docs/bestpractices/ 