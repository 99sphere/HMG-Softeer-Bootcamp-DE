# Week 2 (python multiprocessing, AWS)

## Python multi processing

## AWS
### EC2 (ECC, Elastic Compute Cloud )
- Amazon Web Service의 public cloud를 활용할 수 있는 web 기반의 service.
- H/W spec에 따라 다양한 가격대의 instance 생성 및 사용 가능
- 사용량이 높아지면, 자동으로 scale out 되도록 할 수 있음
- Instance를 생성할 때, user data를 통해 생성 후 수행할 명령어들을 지정할 수 있다.
- Free-tier instance는 생각보다 더 느려서, 여유를 두고 결과를 확인해봐야 함.

### IAM (Identity and Access Management)
- AWS 리소스에 대한 액세스를 안전하게 제어할 수 있는 서비스 
- 사용자가 액세스할 수 있는 AWS 리소스를 제어하는 권한을 중앙에서 관리
- 인증(로그인) 및 권한 부여(권한 있음)된 대상을 제어

### ECR (Elastic Container Registry)
- private Docker hub. 
- Docker Hub에서도 private하게 사용할 수 없다. (기업은 불가, 개인은 1개 가능)
- ECR을 사용하기 위해서는 계정에 적절한 권한을 부여한 후, access key, secret access key 등의 정보를 사용해야 함.


### Trouble Shooting
#### 1. ECR에 Image push
- 계속 no basic auth credentials와 같은 error 발생
- user group, user의 적절한 권한 부여(AmazonEC2ContainerRegistryFullAccess)로 해결 

#### 2. User data의 사용
- 서버가 init 된 후 바로 실행할 shell script.
- update, docker install, ECR에서 image pull, jupyter 실행 등을 순서대로 수행해야 함
- ECR에 이미지를 push할 때는 aws ecr get-login-password와 같은 명령어로 login 해야하고, 이를 위해서는 access key, secret access key 정보를 user-data로 넣어줘야 하나?
    - instance 자체에 적절한 권한(AmazonEC2ContainerRegistryReadOnly)을 부여하면, access key 정보 없이 login이 가능하다. 
#### 3. Jupyter token 확인
- user data로 jupyter를 실행한 후, ssh 등의 방식으로 instance에 접속하면 이미 token 정보가 날아가 있다. 확인할 수 있는 방법은?
    - docker logs 명령어 또는 /var/log/cloud-init-output.log 파일에서 확인할 수 있다. 

## About Sentiment Analysis
