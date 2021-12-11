# Hadoop


### Steps
- Download and install hadoop in c:/hadoop 
- Unzip `HadoopConfiguration-FIXbin.rar` and replace its bin folder with hadoop/bin
- Create `c:/hadoop/data/datanode` and `c:/hadoop/data/namenode` folders
- replace 1 cmd and 4 xml files


### Run
```
hdfs namenode -format

cd hadoop
cd sbin
start-all
```

Console1
```
spark-class org.apache.spark.deploy.master.Master
```
GUI
```
http://LAPTOP-HFC8LI3B:8080 GUI
```
Console2
```
spark-shell --master spark://LAPTOP-HFC8LI3B:7077
```


### See

- [downloads spark](https://spark.apache.org/downloads.html)
- [install-spark-on-windows-10](https://phoenixnap.com/kb/install-spark-on-windows-10)
- [Video Install Hadoop on Windows 10](https://www.youtube.com/watch?v=g7Qpnmi0Q-s)
- [Hadoop on Windows 10](https://cwiki.apache.org/confluence/display/HADOOP2/Hadoop2OnWindows)
- [KU Leuven courses](./kuleuven)

