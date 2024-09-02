# Week 4 (Spark)
## Spark
### 1. Spark란
- Data engineering, data science, machine learning을 위한 multi-language(Java, Scala, Python and R) engine으로 single node machine 또는 cluster에서 사용 가능
- Spark SQL, Pandas API, MLlib, GraphX, Structured Streaming과 같은 higher-level API 지원

### 2. 특징
- Speed - In-memory computing을 이용하여, hadoop의 MapReduce와 같은 traditional big data processing보다 빠르다.
- Ease of Use - 다양한 언어와 higher-level API를 이용하여 사용이 쉽다.
- Versatility - 다양한 workload를 지원한다. (batch processing, interactive queries, streaming data, and machine learning)
- Unified Platform - 다양한 workload에 대한 다양한 언어를 지원하는 unified platform.

### 3. Cluster Manager Type
- Standalone, Yarn, Mesos, Kubernetes 이용 가능.

### 4. Deploy Options
<img width="471" alt="image" src="https://github.com/user-attachments/assets/e5ae5443-6b46-40a9-896a-3475842a30d5">

### 5. Driver and Executors
- Driver
    - Spark application의 실행을 coordinate하는 main process.
    - Spark 기능과 상호작용하기 위한 entry point인 SparkContext를 포함한다.
    - RDD의 state와 DAG에 대한 정보를 유지한다.
- Executor
    - Spark application의 연산을 실제로 수행하고 저장한다.
    - Task를 수행하고, 중간 결과를 memory 또는 disk에 저장한다.
    - Executor는 cluster의 각 node에서 실행되며, task를 전달받고 status를 update하기 위해 driver와 통신한다.

### 6. Scheduling Side vs Executor Side
- 각 application들은 application이 끝날 때 까지 유지되는 고유한 executor process들을 할당받으며, 각 process에서는 multiple thread로 작업을 수행한다.
- 이를 통해 scheduling side와 executor side 모두에서 application을 서로 분리할 수 있다.
- But, 이로 인해 Spark application(SparkContext Instance) 사이에서는 외부 저장소를 이용하지 않는 한 데이터를 공유할 수 없다.

### 7. Deploy Modes
- Local mode, Client mode, Cluster mode가 존재한다.
- Local mode: spark application을 single machine에서 수행한다. 주로 spark 학습, local development의 테스트를 목적으로 사용한다.
- Client mode: Spark driver를 client machine에서 실행한다. 즉, Client machine이 Spark driver process를, Cluster manager가 Executor process를 관리한다.
- Cluster mode: Cluster 내부에서 Spark driver를 실행한다. 즉, Cluster manager가 모든 Spark application 관련 process를 관리한다.
<img width="646" alt="image" src="https://github.com/user-attachments/assets/4d220878-a375-467b-831f-76f0402b2a82">

### 8. Client vs Cluster
- Client mode
    - client(edge node)가 cluster의 모든 node와 communicate 할 수 있어야 한다. (network issue에 취약하다.)
    - User가 직접 driver에 접근할 수 있기에, interactive application, debugging 그리고 development 과정에 유리하다.
- Cluster mode
    - Application이 cluster manager에게 submitted 되었으므로, 그 후에는 client가 disconnect 되어도 아무 문제 없다.
    - 일반적으로 보다 강인하며 failure에 대해 resilient하므로, production job 또는 long-running task에 적합하다.


### 9. Web UI Port Number (for Week4 Missions)
<img width="1020" alt="image" src="https://github.com/user-attachments/assets/4fa6e71b-a008-4ad8-8923-0ccf6194f1db">