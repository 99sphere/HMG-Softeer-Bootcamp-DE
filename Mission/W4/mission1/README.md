# W4M1 - Building Apache Spark Standalone Cluster on Docker
## 1. Build & Run Spark Standalone Cluster
```
cd spark-spark-standalone-cluster
docker compose up
```

## 2. Run Spark Job & Check Result
```
docker exec -it spark-master /bin/bash
./mission1.sh
```

- mission1.sh is consist below commands.

```
# mission1.sh
cd ~
spark-submit ./spark/examples/src/main/python/pi.py &> result.txt
cat result.txt
```
(Result Example)
<img width="1039" alt="image" src="https://github.com/user-attachments/assets/875993f9-a422-446d-91c1-ea8cab665dff">
