# Week 2 (python multiprocessing, AWS)

## 1. Python Multi Processing vs Multi Threading
### 1.1. Multi Threading
- 파이썬에서의 multi threading은 C, C++과는 달리 실제로는 parall하게 동작하지 않는다. 
    - 파이썬에서는 cpython의 memory관리가 thread-safe하지 않기 때문에, GIL(Global Interpreter Lock)을 사용하고, 이로 인해 한 시점에는 하나의 thread만이 수행될 수 있다. 

- 이로 인해 CPU-Bound 작업의 경우, multi threading은 큰 성능향상을 보이지 않는다.   
    - thread를 생성하는 과정에서 소요되는 시간 
    - context switching 비용

- But, I/O Bound 작업의 경우에는 multi threading으로도 유의미한 성능 향상을 보일 수 있다.

### 1.2. Multi Processing
- 위와 같은 이유로, CPU Bound 작업의 경우 multi processing을 사용하는 것이 바람직하다.
- 파이썬에서는 Pool, Process 등의 방식을 통해 multi processing을 구현할 수 있으며, 각 process들 사이의 communication을 위해 Queue, Pipe 등의 방식을 이용할 수 있다.

#### 1.2.1. Pool
- Input data를 다양한 process에 편리하게 분배하여 (동일한) 함수 실행의 병렬화를 편리하게 구현할 수 있다. 

#### 1.2.2. Process
- Pool보다 detail한 설정이 가능하다. 각 process에서 수행할 함수와 입력 데이터를 각각 할당할 수 있으며, start, join의 시점 역시 각각 설정할 수 있다.

#### 1.2.3. Queue
- 다양한 process 사이의 안전한 communication이 가능하도록 한다. 
- get, put method를 통해 queue에 데이터를 넣거나, queue에서 데이터를 꺼내올 수 있다.
    - 이때, get의 경우 queue에 데이터가 없는 경우 queue에 데이터가 들어올 때 까지 wait한다.
    - 이를 원치 않는 경우, get_nowait method를 사용하여 queue에 데이터가 없을 때 예외가 발생하도록 할 수 있다.

## 2. AWS
### 2.1. EC2 (ECC, Elastic Compute Cloud )
- Amazon Web Service의 public cloud를 활용할 수 있는 web 기반의 service.
- H/W spec에 따라 다양한 가격대의 instance 생성 및 사용 가능
- 사용량이 높아지면, 자동으로 scale out 되도록 할 수 있음
- Instance를 생성할 때, user data를 통해 생성 후 수행할 명령어들을 지정할 수 있다.
- Free-tier instance는 생각보다 더 느려서, 시간적 여유를 두고 결과를 확인해봐야 함.

### 2.2. IAM (Identity and Access Management)
- AWS 리소스에 대한 액세스를 안전하게 제어할 수 있는 서비스 
- 사용자가 액세스할 수 있는 AWS 리소스를 제어하는 권한을 중앙에서 관리
- 인증(로그인) 및 권한 부여(권한 있음)된 대상을 제어

### 2.3. ECR (Elastic Container Registry)
- private Docker hub. 
- Docker Hub에서도 private하게 사용할 수 없다. (기업은 불가, 개인은 1개 가능)
- ECR을 사용하기 위해서는 계정에 적절한 권한을 부여한 후, access key, secret access key 등의 정보를 사용해야 함.

## 3. Docker
### 3.1. Dockerfile
- COPY 명령어를 통해 build한 docker image에 파일들을 포함 시킬 수 있음.
```
COPY {source} {target}
ex. COPY resources /home/jupyter

```
- 이때, 포함시킬 파일들은 Dockerfile 하위(?)에 존재해야 함.
```
/docker/Dockerfile
/docker/resources/mtcars.csv
/docker/resources/mission1.ipynb
```

## 4. Depoly with EC2, Trouble Shooting
### 4.1. ECR에 Image push
- 계속 no basic auth credentials와 같은 error 발생
- user group, user의 적절한 권한 부여(AmazonEC2ContainerRegistryFullAccess)로 해결 

### 4.2. User data의 사용
- 서버가 init 된 후 바로 실행할 shell script.
- update, docker install, ECR에서 image pull, jupyter 실행 등을 순서대로 수행해야 함
- ECR에 이미지를 push할 때는 aws ecr get-login-password와 같은 명령어로 login 해야하고, 이를 위해서는 access key, secret access key 정보를 user-data로 넣어줘야 하나?
    - instance 자체에 적절한 권한(AmazonEC2ContainerRegistryReadOnly)을 부여하면, access key 정보 없이 login이 가능하다. 

### 4.3. Jupyter token 확인
- user data로 jupyter를 실행한 후, ssh 등의 방식으로 instance에 접속하면 이미 token 정보가 날아가 있다. 확인할 수 있는 방법은?
    - docker logs 명령어 또는 /var/log/cloud-init-output.log 파일에서 확인할 수 있다. 

## 5. About Sentiment Analysis
### World Cloud 시각화 logic
- WordCloud class의 generate method를 호출하면, process_text와 generate_from_frequencies를 호출하게 된다.
    - process_text method: 각 단어와, 해당 단어의 등장 빈도를 key, value로 갖는 dictionary를 반환한다.
    - generate_from_frequencies: process_text의 결과를 입력받아 사용 
        - 입력받은 dictionary를 value를 기준으로 내림차순 정렬 후, max_words만큼 slicing하여 사용
        - 이후, 자주 등장하는 단어부터 image에 그린다. 
        - 단어의 회전 여부는 random하게 결정한다.
        - IntegralOccupancyMap class를 이용하여, 단어가 기존의 단어들과 겹치는지 확인한다.
        - 이때, 겹치지 않게 넣을 수 있는 위치가 없는 경우 font size를 줄여가며 반복적으로 수행한다.
        - font_size가 min_font_size보다 작아지는 경우, 그리지 않는다.
        
## 6. 추가 학습거리
<details><summary>Summary</summary> 

Introduction   

In the present scenario, social media network plays a significant role in sharing information between individuals. This incorporates information about news and events that are presently occurring in the real world. Anticipating election results is presently turning in to a fascinating research topic through social media. In this article, we proposed a strategy to anticipate election results by consolidating sub-event discovery and sentimental analysis in micro blogs to break down as well as imagine political inclinations un covered by those social media users

Methodology

This approach discovers and investigates sentimental data from micro-blogs to anticipate the popularity of contestants. In general, many organizations and media houses conduct prepoll review and expert’s perspectives to anticipate the result of the election, but for our model, we use twitter data to predict the result of an election by gathering twitter information and evaluate it to anticipate the result of the election by analyzing the sentiment of twitter information about the contestants.

Results

The number of seats won by the first, second and the third party in AP Assembly Election 2019 has been deter-mined by utilizing PSS’s of these parties by means of equation(2),(3), and(4), respectively. In Table 2 actual results of the election and our model prediction results are shown and these outcomes are very close to actual results. We utilized SVM with 15-fold cross-validation, for sentiment polarity classification utilizing our training set, which gives us the precision of 94.2%. There are 7500 tuples in our training data set, with 3750 positive tweets and 3750 negative tweets.

Conclusions

Our outcomes state that the proposed model can precisely forecast the election results with accuracy (94.2 %) over the given baselines. The experimental outcomes are very closer to actual election results and contrasted with conventional strategies utilized by various survey agencies for exit polls and approval of results demonstrated that social media data can foresee with better exactness.

Discussion

In the future we might want to expand this work into different areas and nations of the reality where Twitter is picking up prevalence as a political battling tool and where politicians and individuals are turning towards micro-blogs for political communicates and data. We would likewise expand this research into various fields other than general elections and from politicians to state organizations.
</details>

### 소감
 - 연구가 수행된 Andhra Pradesh는 인도 남부 지방으로, 해당 지역에 출마한 후보와 유권자들의 연령대별 인구 분포 및 트위터 사용 비율이 궁금하다. 
- 무수히 쏟아져 나오는 트윗들을 유의미한 학습 데이터로 변환하는 과정은 어떻게 구성하였을까?
- 트위터에 포함된 정보들의 활용도가 높아지면, crawling의 시도가 빈번하게 발생할 것이고 기업 입장에서는 증가하는 traffic으로 인해 유지 비용이 증가할 것이다. 이를 해결하기 위한 방법을 모색해야 한다.
