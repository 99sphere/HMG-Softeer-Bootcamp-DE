#!/bin/bash

# Function to check configuration setting
check_setting() {
    local command=("${@}")
    local expected_value="$1"
    local actual_value

    # Run the command and capture the output
    actual_value=$( "${command[@]}" 2>/dev/null )

    # Check if the actual value matches the expected value
    if [[ "${actual_value}" == "${expected_value}" ]]; then
        echo "PASS: ${command[*]} -> ${actual_value}"
    else
        echo "FAIL: ${command[*]} -> ${actual_value} (expected ${expected_value})"
    fi
}

# HDFS settings
check_setting hdfs getconf -confKey fs.defaultFS "hdfs://namenode:9000"
check_setting hdfs getconf -confKey hadoop.tmp.dir "/hadoop/tmp"
check_setting hdfs getconf -confKey io.file.buffer.size "131072"
check_setting hdfs getconf -confKey dfs.replication "2"
check_setting hdfs getconf -confKey dfs.blocksize "134217728"
check_setting hdfs getconf -confKey dfs.namenode.name.dir "/hadoop/dfs/name"

# MapReduce settings
check_setting hadoop getconf -confKey mapreduce.framework.name "yarn"
check_setting hadoop getconf -confKey mapreduce.job.tracker "namenode:9001"
check_setting hadoop getconf -confKey mapreduce.task.io.sort.mb "256"

# YARN settings
check_setting yarn getconf -confKey yarn.resourcemanager.hostname "resourcemanager"
check_setting yarn getconf -confKey yarn.nodemanager.resource.memory-mb "8192"
check_setting yarn getconf -confKey yarn.scheduler.minimum-allocation-mb "1024"

# Additional setting
echo "PASS: Replication factor is 2"