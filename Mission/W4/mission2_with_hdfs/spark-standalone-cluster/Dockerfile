FROM ubuntu:22.04

ARG SPARK_VERSION=3.3.3

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openssh-server \
    sudo \
    curl \
    vim \
    unzip \
    rsync \
    ssh && \
    openjdk-11-jdk \
    build-essential \
    software-properties-common \
    python3-pip && \ 
    apt-get clean 
    # rm -rf /var/lib/apt/lists/*

RUN useradd -m spark_user && echo "spark_user:supergroup" | chpasswd && adduser spark_user sudo && echo "spark_user     ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && cd /usr/bin/ && sudo ln -s python3 python
USER spark_user
RUN sudo chown -R spark_user /home/spark_user

WORKDIR /home/spark_user

ENV SPARK_HOME=${SPARK_HOME:-"/home/spark_user/spark"}
RUN sudo curl https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz -o spark-${SPARK_VERSION}-bin-hadoop3.tgz \
 && sudo tar xvzf spark-${SPARK_VERSION}-bin-hadoop3.tgz --directory /home/spark_user/spark --strip-components 1 \
 && sudo rm -rf spark-${SPARK_VERSION}-bin-hadoop3.tgz

COPY requirements/requirements.txt .
RUN pip3 install -r requirements.txt

ENV PATH="${SPARK_HOME}/sbin:${SPARK_HOME}/bin:${PATH}"
ENV SPARK_MASTER="spark://spark-master:7077"
ENV SPARK_MASTER_HOST spark-master
ENV SPARK_MASTER_PORT 7077
ENV PYSPARK_PYTHON python3

COPY conf/spark-defaults.conf "$SPARK_HOME/conf"
# COPY data/ /home/spark_user/data

RUN chmod u+x $SPARK_HOME/sbin/* && \
    chmod u+x $SPARK_HOME/bin/*

ENV PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH
RUN mkdir -p ${SPARK_HOME}/spark-events

COPY scripts/* .
RUN mkdir code
RUN sudo chmod +x entrypoint.sh && \
    sudo chmod +x mission1.sh

CMD tail -f /dev/null

# RUN useradd -m hduser && echo "hduser:supergroup" | chpasswd && adduser hduser sudo && echo "hduser     ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && cd /usr/bin/ && sudo ln -s python3 python
# USER hduser
# WORKDIR /home/hduser

# ENV HADOOP_VERSION=3.3.6
# ENV HADOOP_HOME=/home/hduser/hadoop-$HADOOP_VERSION
# RUN curl -sL --retry 3 \
#   "http://archive.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz" \
#   | gunzip \
#   | tar -x -C /home/hduser/ \
#  && rm -rf ${HADOOP_HOME}/share/doc

#  ENV HDFS_NAMENODE_USER hduser
#  ENV HDFS_DATANODE_USER hduser
#  ENV HDFS_SECONDARYNAMENODE_USER hduser
#  ENV YARN_RESOURCEMANAGER_USER hduser
#  ENV YARN_NODEMANAGER_USER hduser

# # ssh without key
# RUN ssh-keygen -t rsa -f ~/.ssh/id_rsa -P '' && \
# cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

# RUN mkdir $HADOOP_HOME/logs
# COPY hadoop_config/* /tmp/

# RUN mv /tmp/ssh_config ~/.ssh/config && \
#     # mv /tmp/hadoop-env.sh $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
#     mv /tmp/hdfs-site.xml $HADOOP_HOME/etc/hadoop/hdfs-site.xml && \ 
#     mv /tmp/core-site.xml $HADOOP_HOME/etc/hadoop/core-site.xml && \
#     mv /tmp/mapred-site.xml $HADOOP_HOME/etc/hadoop/mapred-site.xml && \
#     mv /tmp/yarn-site.xml $HADOOP_HOME/etc/hadoop/yarn-site.xml && \
#     mv /tmp/slaves $HADOOP_HOME/etc/hadoop/slaves && \
#     mv /tmp/start-hadoop.sh ~/start-hadoop.sh 

# RUN chmod +x $HADOOP_HOME/sbin/start-dfs.sh && \
#     chmod +x $HADOOP_HOME/sbin/start-yarn.sh && \
#     chmod +x ~/start-hadoop.sh

# RUN service ssh start && ~/start-hadoop.sh 

# USER spark_user
# WORKDIR /home/spark_user
# CMD ["sh", "-c", "entrypoint.sh"]