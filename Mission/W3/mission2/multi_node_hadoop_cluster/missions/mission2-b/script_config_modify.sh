#! /bin/bash

mkdir cfg_backup
echo Backing up core-site.xml...
cp /usr/local/hadoop-3.3.6/etc/hadoop/core-site.xml ~/cfg_backup/core-site.xml
echo Modifying core-site.xml...
python3 ~/missions/mission2-b/modify_config.py /usr/local/hadoop-3.3.6/etc/hadoop/core-site.xml

echo Backing up hdfs-site.xml...
cp /usr/local/hadoop-3.3.6/etc/hadoop/hdfs-site.xml ~/cfg_backup/hdfs-site.xml
echo Modifying hdfs-site.xml...
python3 ~/missions/mission2-b/modify_config.py /usr/local/hadoop-3.3.6/etc/hadoop/hdfs-site.xml


echo Backing up mapred-site.xml...
cp /usr/local/hadoop-3.3.6/etc/hadoop/mapred-site.xml ~/cfg_backup/mapred-site.xml
echo Modifying mapred-site.xml...
python3 ~/missions/mission2-b/modify_config.py /usr/local/hadoop-3.3.6/etc/hadoop/mapred-site.xml

echo Backing up yarn-site.xml...
cp /usr/local/hadoop-3.3.6/etc/hadoop/yarn-site.xml ~/cfg_backup/yarn-site.xml
echo Modifying yarn-site.xml...
python3 ~/missions/mission2-b/modify_config.py /usr/local/hadoop-3.3.6/etc/hadoop/yarn-site.xml

echo Stopping Hadoop DFS...
stop-dfs.sh
echo Stopping YARN...
stop-yarn.sh

if [[ "$HOSTNAME" == "namenode" ]]; then
  output=$(hdfs getconf -confKey dfs.namenode.name.dir)
  if [ ! -d $output ]; then
    $HADOOP_HOME/bin/hdfs namenode -format && echo "OK : HDFS namenode format operation finished successfully !"
  fi
  echo Starting Hadoop DFS...
  $HADOOP_HOME/bin/hdfs --daemon start namenode
  $HADOOP_HOME/bin/hdfs --daemon start secondarynamenode

  echo Starting YARN...
  $HADOOP_HOME/bin/yarn --daemon start nodemanager
  $HADOOP_HOME/bin/yarn --daemon start resourcemanager
else
  $HADOOP_HOME/bin/hdfs datanode -format && echo "OK : HDFS datanode format operation finished successfully !"
  $HADOOP_HOME/bin/yarn --daemon start nodemanager
  $HADOOP_HOME/sbin/hadoop-daemon.sh start datanode
fi

echo Configuration changes applied and services restarted.
# start-dfs.sh
# start-yarn.sh