# Week 5
## How Spark Works Internally: RDD and DAG
### 1. RDD
- Spark의 기본적인 data unit. 
- RDD는 cluster의 node들에 걸쳐 분산되어 있다.
- 이를 기반으로 parallel operation이 가능해진다.
- Immutable 하다. 기존 RDD를 변환하여 생성할 수는 있지만, RDD 자체를 변경할 수는 없다.

### 2. Lazy Evaluation
- Spark에서 RDD에 대한 transformation은 즉시 수행되지 않으며, 이를 Lazy Evaluation이라 한다.
- 대신, Spark는 각각의 RDD에 대해 적용된 operation을 기록하며(lineage), action이 수행될 때 까지 기다린다.
- 이로 인해 Spark에서는 execution plan에 대한 optimize가 가능해지며, 불필요한 연산을 최소화 할 수 있다.

### 3. Transform vs Action
- Transformation
    - 기존의 RDD 데이터를 이용하여 새로운 RDD를 생성한다.
    - 연산은 lazy evaluation되며, 새로운 RDD, DataFrame 또는 Dataset을 반환한다.
    - ex. map, filter, flatMap, groupBy, etc

- Actions
    - Action은 새로운 RDD를 생성하지 않고, 연산 결과를 반환한다.
    - Transform의 evaluation을 trigger하며, 그 결과를 driver program에 return하거나 외부 저장소에 write 한다.
    - ex. collect, count, SaveAsTextFile, reduce, etc

### 4. Narrow & Wide Transformation
- Narrow Transformation
    - 각 input partition이 오직 하나의 output partition에만 영향을 미치는 transformation
    - ex. map, filter, and flatMap
    - Narrow transformation은 partition들 사이의 shuffle 없이 연산을 parallel하게 수행할 수 있다.
- Wide Transformation
    - 각 input partition이 여러 개의 output partition에 영향을 미치는 transformation
    - ex. groupBy, reduceByKey, and join
    - Wide transformation은 여러 node에 위치한 partition들 간의 데이터 이동(shuffle)을 필요로 한다.

### 5. Partition
- 데이터를 더 작게 나눈 logical한 단위로, 연산이 병렬적으로 수행될 수 있도록 한다.
- 각 partition은 하나의 executor의 하나의 task에 의해 처리된다.
- Spark는 데이터의 크기와 사용 가능한 resource에 따라 자동으로 partition의 수를 결정한다.

### 6. Shuffle in Spark
- Shuffle은 cluster worker에 데이터를 분산시키는 과정이다.
- 이는 일반적으로, 아래와 같은 상황에 발생한다.
    - Data skewing이 발생한 경우
    - 처리를 위해 data를 특정 방식으로 배열해야 할 경우
    - Data를 여러 partition에 걸쳐 집계하거나 join해야 할 경우 또는 node간의 데이터 이동이 필요한 겅우.
    - Single node에서 처리하기 위한 memory가 충분하지 않은 경우

### 7. Executing Spark Jobs
- Spark submit을 수행하면 driver program이 시작되고, 이는 cluster manager에게 resource를 요청한다. 동시에 user processing program의 main program이 driver program에 의해 시작된다.
- 이를 기반으로 execution logic이 처리되며, 병렬적으로 Spark Context도 생성된다. 이를 이용하여 다양한 transformation과 action이 수행된다. Spark Context에는 action이 수행되기 전까지의  transform들을 DAG 형태의 RDD lineage로 기록한다.
- Action이 호출되면 job이 생성된다. Job은 task stage의 모음으로, 이는 cluster manager에 의해 시작되며, task scheduler에 의해 수행된다.
- RDD lineage를 task로 변환하는 작업은 DAG scheduler에 의해 수행된다. DAG는 다양한 transformation을 기반으로 생성되고, action이 호출되면 이를 다양한 stage의 task로 분할하여 task scheduler에게 제출한다.
- 이후, cluster manager를 통해 이를 여러 개의 executor에서 실행하도록 한다. 전체 resource 할당과 job들의 tracking은 cluster manager가 수행한다.
- Spark submit을 수행하자마자, user program과 앞서 언급한 configuration은 이용 중인 모든 node에 저장된다. 즉, worker node에서는 이를 local에서 읽을 수 있으며, 따라서 어떤 종류의 network routing도 수행할 필요 없다.
<img width="553" alt="image" src="https://github.com/user-attachments/assets/d3d98c49-d851-450d-8c4e-037934cefe70">

### Job
- Spark action에 대한 응답으로 생성되는 여러 개의 task로 구성된 parallel computation.
- Spark shell과의 interactive session에서, driver는 spark application을 하나 또는 그 이상의 job으로 변환한다. 이후, 각 job을 DAG로 변환한다. 이는 본질적으로 Spark의 execution plan이며, DAG내의 각 node는 single or multiple Spark stage이다.

### Stage
- 각각의 job은 stage라고 불리는 더 작은 set으로 나뉜다. 
- DAG node의 일부로, stage는 연산이 병렬로 수행될 수 있는 지의 여부에 따라 생성된다. 모든 Spark 연산이 single stage에 수행될 수 있는 것은 아니므로, 여러 개의 stage로 나뉠 수 있다.
- Stage의 경계는 shuffle을 의미한다.

### Task 
- Spark executor에 전송되는 single unit of work(execution).
- 각 Stage는 여러 개의 Spark task로 구성되며, 이는 각 Spark executor에게 공급된다.
- 각 task는 각 partition에 mapping된다.

### Tasks and Stages in Spark
- Task and Stage Formation
    - tasks: 각 partition에 대해 수행되는 unit of work
    - stages: 함께 실행될 수 있는 Group of tasks. 전형적으로, shuffling을 요구하지 않는 narrow transforme들로 구성된다.
- Boundary of Stages
    - Stage의 boundary는 shuffle을 요구하는 operation에 의해 결정된다. 
    - ex. reduceByKey, groupByKey, join 등
- Data Transfer During Stage Execution
    - Stage 내에서, task는 이미 분할된 partition에 대해 동작한다. 동일한 stage 내에서의 task는 데이터를 교환할 필요 없이, 독립적으로 동작한다.
    - Stage가 완료된 후, shuffle boundary에서는 다음 stage의 요구사항에 따라 data를 재구성한다.
- Impact on Performance
    - Spark job performance를 위해서는 효율적인 stage 관리가 필수이다. Stage 수를 최소화하고, data partitioning을 최적화하면 데이터 shuffling과 관련된 overhead를 줄임으로써 execution time을 줄일 수 있다.
    - Stage boundary에 대한 이해는 불필요한 data 이동을 줄이고, resource utilization을 개선하여 spark job의 최적화를 돕는다. 

### RDD vs DataFrame
- RDD는 Spark의 basic data structure이지만, 이는 lower-level API로 더 상세한 syntax를 필요로 하며, higher-level data structure에 비해 최적화가 부족하다.
- Spark는 RDD 위에 구축한 DataFrame을 도입하며 사용자 친화적인, 최적화된 API를 제공한다. 이는 name column으로 구성되어 relational database와 유사하게 구조화한다.
- DataFrame에 대한 연산은 Catalyst의 이점도 누리며, 계산 효율성을 높여 성능을 개선한다.
- Transform과 action은 DataFrame에서도 RDD와 같이 실행된다.
- DataFrame은 일반적으로 사용하기 더 쉽고, 더 나은 성능을 제공한다.
- 하지만, 복잡한 data procesisng에 대한 debugging, custom operation의 정의 등의 작업에는 RDD가 유용할 수 있다. RDD는 partitioning 및 memory 사용에 대한 더욱 세부적인 제어가 가능하다.
- 같은 이유로, raw, unstructured data, binary file 또는 custorm ㄹ의 데이터를 처리할 때는 RDD가 더욱 유용할 수 있다.