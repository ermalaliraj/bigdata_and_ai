# Data Science tooling


```
type text.txt | python mapper.py
```

```
hdfs dfs -put word_input /user/cludera
ls /usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.0.0-mrl-cdh4.4.0.jar   # this will execute python code
```
mapred.reduce.tasks 1, 2 or 3 depending on how big is the file  -Dmapred.reduce.tasks=1
```
hadoop jar /usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.0.0-mrl-cdh4.4.0.jar 
    -file /home/cloudera/mapper.py /home/cloudera/reducer.py 
    -mapper "python mapper.py"
    -reducer "python reducer.py"
    -input /user/cloudera/word_input
    -output /user/cloudera/wc_output
```

```
hdfs dfs -ls /user/cludera/wc_output/
hdfs dfs -cat /user/cludera/wc_output/part*
```

###
- [Back to Bid Data & AI](https://github.com/ermalaliraj/bigdata_and_ai)