# Week 6 
## Optimizing Spark Job
### 1. Use an efficient file format and compression type
- 사용하는 file format과 compression type이 shuffling 성능에 큰 영향을 미칠 수 있다.
- Apache Parquet 또는 Apache ORC와 같이 Spark에 최적화된 file format, Snappy 또는 LZ4와 같이 shuffling에 효율적인 compression type을 이용하면 성능 개선에 도움이 된다.

### 2. Advantages of Columnar Storage Over Row-based Storage
- Compression Efficiency
    - column형 storage는 더 나은 압축 기술을 제공한다. 
    - column value는 주로 같은 type이므로, 압축 알고리즘을 해당 type에 맞게 조정할 수 있어 압축률이 높아진다. 이를 기반으로 storage requirement를 낮추고, data 전송 속도를 높일 수 있다.
- Column Pruning
    - 쿼리를 실행할 때, column 기반 데이터베이스는 관련없는 column을 skip할 수 있어 I/O를 줄이고 쿼리 성능을 높일 수 있다.
    - 반면, row 기반 데이터베이스에서는 몇 개의 column만 필요하더라도 전체 행을 읽어야 한다.
- Aggregation Performance
    - Column형 storage는 집계 쿼리에 효율적이다. 집계는 single column에 대한 집계를 포함하기 때문.
    - 따라서, 분석 작업에 대한 쿼리 성능을 더 빠르게 만들어준다.
- Predicate Pushdown
    - 컬럼형 데이터베이스는 메타데이터를 분석하여 쿼리 실행 프로세스 초기에 필터를 적용하여 스토리지에서 읽는 데이터 양을 최소화할 수 있다.
- Analytics and Data Warehousing
    - 컬럼형 스토리지는 분석 워크로드, 보고 및 데이터 웨어하우징에 적합하다. 대규모 데이터 세트에 대한 빠른 분석 및 보고가 가능하다.
- Schema Evolution
    - Parquet과 같은 column 기반 형식은 schema evolution을 지원하여 기존 데이터를 붕괴하지 않고도 새 열을 추가하거나 기존 열을 변경할 수 있다.

### 3. Apache Parquet vs Other Formats
- Parquet은 Write Once Read Many(WORM) 패러다임에 최적화되어 있다. 쓰기는 느리지만 읽기는 매우 빠르며, 특히 전체 열의 하위 집합에만 액세스할 때 특히 빠르다.
- 전체 row에 대해 동작하는 경우 CSV, JSON 또는 AVRO와 같은 형식을 사용해야 한다.

### 4. On Heap Memory
- Storage Memory
    - 주로 Spark cache data를 위해 사용한다.
- Execution Memory
    - 주로 shuffle, join, sort와 같은 연산의 temporary data를 저장하기 위해 사용한다.
- User Memory
    - 주로 RDD dependency와 같은 RDD conversion operation에 필요한 정보를 저장한다. 
- Reserved Memory
    - System을 위해 reserve된 공간.

<img width="377" alt="image" src="https://github.com/user-attachments/assets/f58e8eb5-b628-412a-bed9-d6f90063de74">

<img width="667" alt="image" src="https://github.com/user-attachments/assets/8df16948-f814-43ae-ad12-efacf76f0798">

### 5. Use SparkSQL
- 데이터를 필터링, 그룹화 또는 집계해야 하는 경우 SparkSQL을 사용하여 쿼리를 보다 효과적으로 표현할 수 있다. 
- 대부분의 경우 SparkSQL은 shuffling을 줄이고 쿼리의 실행을 개선할 수 있다.
- Spark SQL은 Parquet 파일 읽기와 쓰기를 모두 지원하며, 원래 데이터의 스키마를 자동으로 보존한다.

### 6. Shuffle in Spark
- groupBy 및 join과 같은 작업을 수행하는 경우, 동일한 키를 가진 모든 레코드가 동일한 node에 있는지 확인하기 위해 shuffling이 필요하다. 
- 이를 통해 모든 레코드를 한 번에 처리하고 결과를 결합할 수 있다.
- Shuffling은 다음 stage가 시작되기 전에 완료되어야 하며, 이는 데이터 처리를 지연시킨다.

### 7. Data Shuffling is a performance killer
- Node간 데이터 이동, 높은 Disk I/O, file rearranging 등으로 인해 network를 통한 데이터 전송이 발생하는 cost가 큰 작업이다.
- 따라서, 가능한 경우 Shuffling을 피함으로써 성능을 개선할 수 있다.

### 8. Causes of Shuffle
- Data Skew
    - Dataset의 일부 key가 다른 key에 비해 훨씬 더 많은 데이로 채워질 때 발생할 수 있다. 이런 현상을 data skew라 부른다. 
- Partitioning
    - Spark는 partitioning을 통해 node들 사이에 데이터를 나눈다. 이때, 데이터가 균등하게 분배되지 않으면 shuffling이 발생할 수 있다.
- Spark Operations
    - 키로 데이터를 그룹화 및 집계하거나 두 데이터 세트를 결합할 때 groupByKey, reduceByKey와 같은 연산은 shuffling을 발생시킨다.
- Caching
    - Dataset이 memory에 cache될 때, data의 양이 single node의 memory 양을 초과하는 경우 shuffling이 발생할 수 있다.
- Data Locality
    - Spark는 연산을 수행할 node에 데이터를 배치하여 shuffling을 줄이려 한다. 하지만, 데이터가 아직 저장되어 있지 않다면 계산이 수행될 node로 데이터를 이동시켜야 한다.

### 9. Transformation Optimization
- 효율적인 transform을 사용하고 불필요한 shuffle을 피하면 성능을 향상시킬 수 있다.
    - Use the sortWithinPartitions transform
        - 각 파티션 내에서 데이터를 정렬해야 하는 경우 sort 대신 sortWithinPartitions 변환을 사용할 수 있다. 이를 통해 전체 partition이 아닌, 각 partition 내에서 데이터를 정렬하여 shuffling을 최소화할 수 있다.
    - Use the repartitionByRange transform
        - 데이터를 정렬해야 하고 RangePartitioner와 같은 범위 기반 partitioner를 사용하는 경우 sort 대신 repartitionByRange transform을 사용할 수 있다. 이를 통해 각 partition 내에서 데이터를 정렬하고 동일한 키를 가진 데이터가 동일한 partition에 배치되도록 하여 셔플링을 최소화할 수 있다.
    - Use the window function
        - 윈도우 집계를 수행해야 하는 경우 윈도우 함수를 사용하면 윈도우와 집계 함수를 지정하는 데 도움이 될 수 있다. 윈도우 함수는 각 파티션 내의 데이터에서 작동하므로 shuffling을 trigger하지 않는다.
    - Use filtering and aggregation instead of groupBy
        - 데이터만 필터링하거나 간단한 집계를 수행해야 하는 경우 groupBy 대신 filter 및 agg transform을 사용할 수 있다. 이러한 transform은 shuffling을 trigger하지 않는다.

### 10. Caching in Spark
- Caching은 계산 실행 및 데이터 저장과 같은 작업을 수행하는 Spark의 worker node의 memoory resource를 활용하기 때문에 신중한 계획이 필요하다.
- Data set이 사용 가능한 memory보다 크거나 이후 재사용하지 않는 RDD 또는 DataFrames을 caching하는 경우 잠재적인 overflow 및 기타 memory management 문제로 인해 성능에 bottleneck이 발생할 수 있다.

### 11. Persist in Spark
- Persist는 Cache와 비슷하며, optional하게 argument를 전달할 수 있다. 인수가 주어지지 않으면 기본적으로 MEMORY_AND_DISK 스토리지 레벨에 저장하고, 그렇지 않은 경우 StorageLevel을 인수로 받아서 다른 스토리지 레벨에 저장한다.

### 12. When to use Persist
- 동일한 dataset에서 반복되는 연산이 포함된 작업이 있는 경우 persist를 사용한다. Persist가 없으면 Spark의 각 작업은 RDD를 처음부터 다시 계산하는데, 이는 크고 계산이 복잡한 경우 비효율적이다. RDD를 persist함으로써 반복되는 연산에 대한 cost를 절약할 수 있습니다.

### 13. Checkpoint in Spark
- Checkpoint는 RDD lineage를 자르는 데 사용한다. 즉 Spark가 RDD를 안정적인 저장소(HDFS, S3 등)에 저장하고, 그 후 부터는 기존 source에서 다시 계산하는 대신 체크포인트가 지정된 파일에서 RDD를 읽어온다.
- 이는 실패에 대한 risk가 있으므로, 처음부터 RDD를 다시 계산하는 데 비용이 많이 드는 long-running job에 유용하다.

### 14. When to use Checkpoint
- 계산의 중간 단계를 다시 계산하는 데 비용이 많이 들고, node failure나 다른 문제가 발생할 위험이 있는 작업이 있는 경우 체크포인트를 사용한다. RDD 변환의 계보를 끊어냄으로써 fault tolerance를 보장한다.

### 15. Cache vs Checkpoint
- Cache는 RDD를 memory(or disk)에 저장한다. 하지만, RDD lineage는 기억되므로 node failure가 발생하고 cached RDD의 일부가 손실된 경우 다시 생성할 수 있다.
- Checkpoint는 RDD를 HDFS 파일과 같은 storage에 저장한 후, lineage를 완전히 잊는다. 이를 통해 긴 계보를 잘라내고 데이터를 외부 storage(ex. HDFS, S3 등)에 안정적으로 저장할 수 있으며, 이는 replication에 의해 fault-tolerance를 보장한다.

### 16. Data Partitioning in Spark
- Spark는 일반적으로 사용 가능한 CPU 코어 수에 따라 기본 partitioning 전략을 제공하지만 사용자 지정 분할에 대한 옵션도 제공한다. 사용자는 특정 키에 대한 데이터 partitioning 같은 custom partitioning function을 지정할 수 있다.
- 병렬 처리의 효율성에 영향을 미치는 가장 중요한 요소 중 하나는 partition이다.
    - Partition이 충분하지 않으면 사용 가능한 memory와 resource가 충분히 활용되지 않을 수 있다.
    - 반면, partition이 너무 많으면 task scheduling과 같은 overhead가 증가할 수 있다.
    - 최적의 partition 수는 일반적으로 cluster에서 사용 가능한 core의 수로 설정한다.

### 17. repartition() and coalesce()
- repartition() method는 RDD 또는 DataFrame의 partition 수를 늘리거나 줄인다. 이때, 클러스터 전체에서 데이터의 전체 shuffle을 수행한다.
- coalesce() method는 RDD 또는 DataFrame의 파티션 수를 줄인다. 이때, repartition()과 달리 전체 셔플을 수행하지 않고 인접한 partition을 결합하여 전체 수를 줄인다.

### 18. Handling Data Skews
- Partitioning
    - 데이터를 적절히 partitioning하면 node 전체에 걸쳐 workload를 고르게 분산하는 데 도움이 된다.
- Sampling
    - Sampling을 통해 skewed key를 식별하고 custom partitioning 또는 filtering을 적용한다.
- Aggregation
    - pre-aggregation 또는 partial aggregation과 같은 대체 aggregation strategy를 사용하여 데이터 skew의 영향을 줄인다.

### 19. Broadcasting
- join()은 하나 이상의 공통 키를 기준으로 두 개의 dataset을 결합하는 일반적인 연산이다. 두 개의 서로 다른 dataset의 row는 지정된 column의 값을 기준으로 단일 dataset으로 병합된다. 이때, 여러 node에서 데이터 shuffling이 필요하기 때문에 join()은 network latency 관점에서 비용이 많이 드는 연산이다.

- 작은 dataset이 더 큰 dataset과 결합되는 경우, Spark는 broadcasting이라는 optimization technique을 제공한다.

- Dataset 중 하나가 각 worker node의 memory에 올라갈 수 있을 만큼 작으면 모든 node로 broadcasting하여 shuffling을 줄일 수 있다. 이 경우, join() 연산은 단순히 각 node에서 수행할 수 있다.

<img width="661" alt="image" src="https://github.com/user-attachments/assets/a78b6833-0330-4e2e-a708-50f812896a11">

### 20. Filtering Unused Data
- High-dimensional data로 작업할 때는 computational overhead를 최소화해야 한다. 이를 위해, 필요하지 않은 행이나 열은 제거해야 한다. 계산 복잡성과 메모리 사용량을 줄이기 위한 두 가지 핵심은 early filtering과 column pruning 이다.
    - Early Filtering
        - Filtering 작업은 데이터 처리 파이프라인에서 가능한 한 일찍 적용해야 한다. 이를 통해 이후의 transform에서 처리해야 하는 row가 줄어들어 computational cost와 사용하는 memory resource를 줄일 수 있다.
    - Column Pruning
        - 대부분의 연산에서, dataset의 column 일부만을 이용한다. 따라서, 데이터 처리에 필요하지 않은 column을 제거하면 처리 및 저장하는 데이터 양을 크게 줄일 수 있다.