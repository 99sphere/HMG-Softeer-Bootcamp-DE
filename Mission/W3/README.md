# Week 3
## Hadoop
### Hadoop Components
- HDFS : storage layer
- Hadoop Yarn: rasource management
- Hadoop MapReduce: application layer

### HDFS(Haddop Distributed FileSystem)
- 데이터를 block 단위로 쪼개서 저장.
- 각 block은 복제되어 저장되며, 그 정도는 hdfs-site.xml에서 아래와 같이 설정 가능
```
    <property>
        <name>dfs.replication</name>
        <value>3</value>
    </property>
```
- namenode와 datanode는 Master-Slave 구조를 갖는다. 
    - namenode는 metadata를 관리하며, 실제 데이터는 datanode에 block단위로 저장된다.
    - namenode와 datanode는 heartbeat를 주고 받아, healthy check
![alt text](https://velog.velcdn.com/images/jochedda/post/ae3e8a2c-de7f-4ab6-b64c-4e001887b5f7/image.png)

### YARN(Yet Another Resource Negotiator)
- CPU, Memory와 같은 Hadoop Cluster Resource를 관리하고 스케쥴링 한다.
![alt text](https://miro.medium.com/v2/resize%3Afit%3A1400/format%3Awebp/1%2A_lJryG5c4UOMqXnY7YeylA.png)

### MapReduce
- HDFS를 기반으로 분산되어 있는 대용량 데이터에 대한 분산 처리 솔루션
- 특정 데이터를 가지고 있는 데이터 노드에 대한 연산 수행 후, 이를 취합한다.
- Mapper
    - Mapper는 input key/value pairs를 임시 key, value로 저장한다.
- Reducer
    - Reducer는 shuffle, sort and reduce 3개의 phase로 구성된다. 
    - Reducer의 input은 mapper의 output이 sorting 된 형태이다. 
    - 최종적으로 reducer는 mapper의 output을 이용하여 더 적은 수의 value가 키를 공유하도록 한다.

- [참고] (https://hadoop.apache.org/docs/r3.3.6/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html)
![alt text](https://velog.velcdn.com/images/jochedda/post/619bddb6-e46a-4b28-bc84-d600b5f6a63e/image.png)

### Port Number ((for check Web UI))
<img width="546" alt="image" src="https://github.com/user-attachments/assets/9d9e983d-eac4-4c50-a86a-20e26c39e824">

### SSH Config
- StrictHostKeyChecking
    - ~/.ssh/known_hosts에 자동으로 호스트를 추가하는 설정
    - 기본 설정은 저장 여부를 묻는다.
    - 비활성 설정: “no”

- UserKnownHostsFile
    - 연결된 호스트에 대한 정보를 남기는 파일을 지정하는 설정
    - 기본 값: ~/.ssh/known_hosts
    - 일반적으로 이 설정을 변경하지 않음
    - StrictHostKeyChecking을 “no”로 설정할 경우에 이 설정을 “/dev/null”로 설정

### ETC
- Docker container끼리는 container name을 이용해서 통신할 수 있다. ex) ssh {user}@{container name}