# Week 3 (Hadoop)

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

![alt text](https://velog.velcdn.com/images/jochedda/post/619bddb6-e46a-4b28-bc84-d600b5f6a63e/image.png)


### Port Number 
<img width="546" alt="image" src="https://github.com/user-attachments/assets/9d9e983d-eac4-4c50-a86a-20e26c39e824">


### Reference
> [참조 1](https://velog.io/@jochedda/%ED%95%98%EB%91%A1Hadoop%EC%9D%B4%EB%9E%80), [참조 2](https://vnvn31.tistory.com/entry/Hadoop-23%EB%B2%84%EC%A0%84-port-list-%EC%A0%95%EB%A6%AC)