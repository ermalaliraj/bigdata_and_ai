# Data Science tooling


```
import pandas as pd 
df = pd.read_csv('2015 01 01.csv') 
df.groupby(df.user_id).value.mean()

import dask.dataframe as dd
df = dd.read_csv('2015 --**--*.csv')
df.groupby(df.user_id).value.mean().compute()

import graphlab
import graphlab.aggregate as agg
sf = graphlab.SFrame.read_csv('2018 01 01.csv’)
sf.groupby(key_columns='user_id', operations={'avg': agg.MEAN('value')})
```

Before jumping to Spark and other think if this can solved with a bunch of servers and a (distributed) on disk library.


### Hadoop 
Hadoop is part of an ecosystem of technologies which are managed by Apache Software foundation.
Hadoop basic stack: 
1. `Hadoop Commo` a set of shared libraries
2. `Hadoop Distributed File System (HDFS)` a Java based file system to store data across multiple machines
3. `MapReduce` a programming model to process large sets of data in parallel
4. `YARN` (Yet Another Resource Negotiator), a framework to schedule and handle resource requests in a distributed environment


### HDFS
`HDFS` is the distributed file system used by Hadoop to store data in the cluster.
- Lets you connect nodes (commodity personal computers) contained within clusters over which data files are distributed
- You can then access and store the data files as one seamless file system
- Is fault tolerant and provides high throughput access (by replicating data on multiple nodes)

| | |
|---|---|
|hadoop fs mkdir mydir | Create a directory (mydir) in HDFS|
|hadoop fs ls |List files and directories in HDFS|
|hadoop fs cat |myfile View a file content|
|hadoop fs du |Check disk space usage in HDFS|
|hadoop fs expunge |Empty trash on HDFS|
|hadoop fs chgrp hadoop file1 |Change group membership of a file|
|hadoop fs chown huser file1 |Change file ownership|
|hadoop fs rm file1 |Delete a file in HDFS|
|hadoop fs touchz file2 |Create an empty file|
|hadoop fs stat file1 |Check the status of a file|
|hadoop fs test e file1 |Check if file exists on HDFS|
|hadoop fs test z file1 |Check if file is empty on HDFS|
|hadoop fs test d file1 |Check if file1 is a directory on HDFS|

### HDFS example
Provides a native Java API and a native C language wrapper for the Java API, as well as shell commands to interface with the file system

```
byte[] fileData = readFile();
String filePath = "/data/course/participants.csv"
Configuration config = new Configuration();
org.apache.hadoop.fs.FileSystem hdfs = org.apache.hadoop.fs.FileSystem.get(config);
org.apache.hadoop.fs.Path path = new org.apache.hadoop.fs.Path(filePath);
org.apache.hadoop.fs.FSDataOutputStream outputStream = hdfs.create(path);
outputStream.write(fileData , 0, fileData.length);
```

### MapReduce

- A "programming framework" for coordinating tasks in a distributed environment
- Can be used to construct scalable and fault tolerant operations in general
- Map: apply function on every item in list
  - Result is a new list of values
- Reduce: apply function on a list
  - Result is a value

```
numbers = [1, 2, 3, 4, 5]
numbers.map(lambda x : x * x)
[1, 4, 9, 16, 25]
numbers.reduce(lambda x : sum(x))
15
```

### Content 

- [Azure Studio Machine Learning](https://studio.azureml.net)
- [Azure machine-learning](https://docs.microsoft.com/en-us/azure/machine-learning/)
- [Online notebook google](https://colab.research.google.com/)
- [Hadoop Video](https://www.youtube.com/watch?v=aReuLtY0YMI)

- [anaconda](https://www.anaconda.com/products/individual) Includes Jupyter, Python, data science package repository (also for R)

###
- [Back to Bid Data & AI](https://github.com/ermalaliraj/bigdata_and_ai)