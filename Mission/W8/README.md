# Week 8 
## Adaptive Query Execution in Spark
### Measuring the Cost of Physical Plans
- Physical plan의 cost는 다양한 요인을 기반으로 측정된다.
- Data Size: Record 수와 각 partition의 크기
- Operation Type: 특정 연산은 다른 연산들에 비해 훨씬 cost가 높다. (shuffling data)
- Data Distribution: Data가 어떻게 분포되어 있는지도 cost에 영향을 미친다.
- Join Strategy: join strategy에 따라 cost가 크게 변한다.
- Number of Stages: stage가 많을수록 일반적으로 task scheduling과 execution 관점에서 더 큰 overhead가 발생한다.

### Example of Cost Consideration
- 두개의 dataset들을 join 해야 하는 경우, Catalyst는 아래와 같은 여러 개의 physical plan을 세울 수 있다.
    - Broadcast Join: 만약 하나의 dataset이 충분히 작은 경우, 이를 모든 node에 broadcasting하여 shuffle을 피할 수 있다.
    - Sort-Merge Join: 만약 두 dataset이 모두 크다면, Spark는 sort-merge join을 선택할 수 있다. 이는 network를 통해 data를 정렬하고 shuffling하는 과정을 포함한다.
- Cost model은 dataset의 크기, partition의 수, network 통신량과 같은 요인을 기반으로 다양한 physical plan의 비용을 추정한다. 이후, 추정 비용이 가장 낮은 physical plan을 선택한다.

### Adaptive Query Execution
- Data의 runtime statistic을 통해 주어진 query에 대한 execution plan을 dynamic하게 조정하는 advanced optimization engine이다.
- 기존의 query execution engine은 data의 distribution이나 statistic에 대해 신경쓰지 않고 fiexed plan을 따랐다. 이로 인해 큰, 복잡한 dataset을 처리할 때 suboptimal한 성능을 보였다.
- 이를 해결하기 위해, AQE optimizer를 도입하여 data의 특성에 따른 execution plan을 dynamic하게 적용할 수 있도록 했다.
- 특히, data의 크기를 예측할 수 없거나, skew가 존재할 때 실행 효율성을 높일 수 있다.
- 최근 분산 시스템은 computing/storage layer를 분리하는 원칙에 따라 설계된다. 즉, remote storage에 persistent data를 저장하고 local storage에는 transient data만 저장한다.
- Spark 역시 이러한 idea를 기반으로 설계되었다. 이는 확장성과 가용성 측면에서 이점이 있지만, 예측할 수 없는 data를 만나게 될 경우 cost calculation의 신뢰성이 떨어지고 이로 인해 query optimization process 역시 부정적인 영향을 받는다.
- 기본적으로, operation들의 logical plan은 (1) catalog를 기반으로 resolve된 이후 (2) rule(constant folding, predicate and project pushdown 등)을 기반으로 optimize 되며 (3) Spark operator의 physical plan으로 변환된다.
- 이러한 방식의 가장 큰 단점은, 한 번 physical plan이 결정되면 runtime에 변경할 수 없다는 점이다. 
    - Plan은 DAG로 변환된 후 DAG Scheduler에 제출된다. DAG는 shuffle boundary에서 task set으로 분할된 후, Task Scheduler에 전달되어 physical resource에서 처리하도록 한다.
- Adaptive execution이 활성화되면, logical plan은 기존보다 일찍, Query Stage에서 독립적인 subgraph로 분할된다.

### Query Stages in AQE
- Query Stage에서는 downstream stage를 처리하기 전, 처리 과정을 materialize한다. 이를 통해 map stage를 개별적으로 submit하고, output statistic object를 수집하며, 이를 기반으로 후속 단계를 위한 분석이 가능해진다.
![image](https://github.com/user-attachments/assets/4f1028c6-b252-4e97-98b9-bdc81277ab72)

- AQE plan에서는 두 가지 type의 query stage를 찾을 수 있다.
    - Shuffle Query Stage에서는 output을 shuffle file로 materialize한다.
    - Broadcast Query Stage에서는 output을 Driver memory의 array로 materialize한다.

|||
|------|---|
|Logical Plan|![image](https://github.com/user-attachments/assets/176398db-8981-4f09-8943-0890a87542f6)|
|Physical Plan|![image](https://github.com/user-attachments/assets/786fc72f-c217-4f93-a300-541be41067ec)|
|Physical Plan with AQE|![image](https://github.com/user-attachments/assets/1f19695f-6694-49fd-9689-81a840a6b390)|

- 이 새로운 기능을 포함하기 위해, DAG Scheduler는 single map stage를 지원한다. 또, Spark execution engine은 planning, execution phase에서의 수정을 지원한다.

|||
|------|---|
|without AQE|![image](https://github.com/user-attachments/assets/8c3fe73a-d7bd-4579-b4aa-c394e5c3ad26)|
|with AQE|![image](https://github.com/user-attachments/assets/4d5fde49-843a-4c8b-af83-2fca2417a182)|

- Execution phase에서, tree의 모든 Query Stage는 child stage를 참조하며 이를 recursive하게 수행한다. 
- Query Stage의 모든 child가 완료된 후, runtime shuffle write statistic을 수집하여 refinement를 진행한다. 이후, Spark는 다시 logical optimization과 physical planning phase를 수행하며, 그 최신 결과에 따라 query plan을 dynamic하게 update한다.

### When to Use AQE
- Parallelism on Reducers
- Join Strategy
- Skewed Joins

### Parallelism on Reducers
- Join 또는 aggregation 연산을 위한 shuffling 후의 parallelsim level은 복잡한 쿼리 성능에 큰 영향을 미친다.
- Reduce task의 수가 너무 작으면 partition의 크기가 너무 커져, executor의 memory에 저장할 수 없기 때문에 data를 disk로 spill해야 한다.
- 반면, reduce task의 수가 너무 큰 경우, scheduling overhead가 커지게 되어, 특정 수준 이상에서는 성능 저하가 발생할 수 있다.
- CoallesceShufflePartitions을 사용하면 Spark가 인접한 작은 partition을 병합하여 shuffle 이후 partition 수를 dynamic하게 조절할 수 있다.
- Runtime data size에 따라 최적의 partition 수를 설정함으로써 더 나은 load balancing이 가능하고, I/O operation의 수도 감소한다.
![image](https://github.com/user-attachments/assets/94c7f170-2375-4266-9ab8-c509e5710d9b)
- Spark는 spark.sql.adaptive.coalescePartitions.initialPartitionNum 구성을 통해 충분히 큰 initial shuffle partition 수를 설정하면 런타임에 적절한 shuffle partition 수를 선택할 수 있다.
![image](https://github.com/user-attachments/assets/73e63873-605b-494c-b2e0-0a34e87fd447)
![image](https://github.com/user-attachments/assets/12d053e8-dc71-41e1-bac6-c9e8dee21dd9)

### Join Strategy
- 복잡한 쿼리의 성능에 영향을 미치는 또 다른 요소는 physical join strategy의 선택이다. 실제로 Spark는 세 가지 physical join operator를 구현한다.
    - ShuffleHashJoin
        - ShuffleHashJoin은 해시 조인을 수행한다. 한 쪽의 콘텐츠를 사용하여 해시 테이블을 만든 후, 다른 쪽을 스캔한다.
    - SortMergeJoin
        - SortMergeJoin은 join attribute에 따라 양쪽을 정렬한 후, 동일한 키가 있는 row를 찾아 데이터를 반복적으로 조회하며 merge한다. Shuffle-join 연산으로 인한 traffic exchange는 아래 그림과 같다.모든 reducer는 모든 mapper에서 하나의 파일을 읽어야 하며, 이는 작업이 다른 worker에서 실행될 때 네트워크를 통해 많은 데이터를 전송해야 함을 의미한다.
        ![image](https://github.com/user-attachments/assets/259e8966-a253-44f3-803f-697de674d40c)
    - BroadcastHashJoin
        - 한 쪽이 다른 쪽에 비해 충분히 작을 때 주로 사용하는 방식으로, node간의 data 교환을 피할 수 있다. 
        - Reduce task의 수와 mapper의 수가 같으므로, 각 reducer는 single mapper의 출력을 읽어야 한다. 일반적으로 이 두 작업은 불필요한 network transfer를 피하기 위해 동일한 worker node에서 수행한다.
        ![image](https://github.com/user-attachments/assets/0b3c750f-46c1-4944-9c60-7b74a82f2f1c)
        - 두 개의 data 중 한쪽의 크기가 충분히 작을 때, sort-merge join을 broadcast-hash join으로 dynamic하게 대체하여 shuffle을 피할 수 있게 한다.
        
-  OptimizeLocalShuffleReader 설정에 따라 regular shuffle read를를 local shuffle read로 대체하여 네트워크 사용량을 줄임으로써 추가적인 optimize가 가능하다.
![image](https://github.com/user-attachments/assets/61ef9e0a-41de-4756-9f1f-c694c27edebb)

### Skewed Joins
- 쿼리 성능에서 또 다른 중요한 측면은 partition간의 data distribution으로, 이는 scheduled task의 크기를 정의한다. Shard가 고르지 않게 분산된 경우, 더 많은 양의 데이터에 대해 수행하는 task는 전체 스테이지를 느리게 하고 downstream stage의 시작을 막는다.
- 이러한 문제는 일반적으로 parallelism level을 높이거나 join key를 re-engineering하여 cardinality를 높이는 방식으로 해결한다.
- OptimizeSkewedJoin는 Spark가 간단한 규칙을 따라 더 나은 load balancing이 가능하도록 한다. Parameter F는 skewed factor, S는 skewed size, R은 skewed row count이며, partition은 아래와 같은 상황에서만 skewed 된 것으로 간주한다.
    - 크기가 S보다 크다. && 크기가 median partition size에 F를 곱한 것보다 크다.
    - row 수가 R보다 크다. && row 수가 median partition row count에 F를 곱한 것보다 크다.
- Partition이 skewed 되었다고 간주되면, 여러 개의 reducer task가 해당 partition에서 동작하도록 scheduling 한다. 이런 방식을 통해, 각 reducer는 single mapper의 output을 가져와 partition chunk에서 join 작업을 수행한다.
- 이는 아래의 그림과 같이 동작한다. Table A의 partition 0은 두 개의 reducer에 의해 처리되며, 후에 join한다.
- OptimizeLocalShuffleReader를 통해 physical plan을 더욱 최적화할 수 있다.
![image](https://github.com/user-attachments/assets/0dcd89f4-9e4f-43f6-8a47-512e063eeb13)

- Handling of Skewed Join (다른 예시)
![image](https://github.com/user-attachments/assets/a79afad6-d3ac-4e3e-8526-832105eec59c)
![image](https://github.com/user-attachments/assets/2af5cdcc-f184-42ed-b597-41f038b96eb8)

### When not to use AQE
- 최소 shuffle stage를 갖는 small job
- 예측 가능하며, 이해 가능한 performance를 보이는 workload
- Manual tuning이 더욱 효과적인 경우

### SQL Performance Tuning
- https://spark.apache.org/docs/latest/sql-performance-tuning.html

### Why is Join Followed by a Shuffle?
- Join은 종종 서로 다른 partition의 데이터를 합쳐야 한다. 예를 들어, 특정 key에 대한 두 DataFrame 간의 조인을 수행할 때 일치하는 키가 있는 row를 함께 가져와야 한다.
- Spark와 같은 distributed environment에서는 동일한 키의 데이터가 서로 다른 partition(또는 서로 다른 node)에 있을 수 있다. Join을 수행하려면 Spark가 partition 간에 data를 shuffle하여 동일한 키를 가진 모든 데이터가 동일한 partition에 있도록 해야 한다.
- 이 shuffling process에는 클러스터 전체에 데이터를 재분배하는 것이 포함되므로 join 후에는 일반적으로 shuffle이 수행된다.

### Does Shuffling Always Happen After a Join?
- 반드시 그런 것은 아니다.
    - Skewed Data : 데이터가 skewed 된 경우 불균형을 처리하기 위해 추가 shuffling이 필요할 수 있다. AQE는 이를 최적화할 수 있다.
    - Pre-existing Partitioning: 만약 join을 수행하는 두 DataFrame/RDD가 이미 동일한 방식으로 partitioning 된 경우, shuffle을 피할 수 있다.
    - Broadcast Joins: DataFrame 중 하나가 충분히 작은 경우 Spark는 broadcast join을 수행하여 더 작은 DataFrame을 모든 worker node로 보내 shuffle을 피할 수 있다. 이는 large dataset을 shuffle하는 것보다 훨씬 빠르다.
    - Hinting and Optimizations: AQE가 활성화되면 Spark는 runtime statistic에 따라 join strategy를 dynamic하게 조정하여 잠재적으로 shuffle을 줄이거나 피할 수 있다.

### Transformations Causing a Shuffle
1. groupBy and groupByKey
2. reduceByKey and aggregateByKey
3. join (including inner, outer, left, right joins)
4. distinct
5. repartition and coalesce
6. sortBy and sortByKey
7. cogroup
8. union