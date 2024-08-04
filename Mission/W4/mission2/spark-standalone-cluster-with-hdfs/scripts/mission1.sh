#! /bin/bash

cd ~
spark-submit ./spark/examples/src/main/python/pi.py &> result.txt
cat result.txt