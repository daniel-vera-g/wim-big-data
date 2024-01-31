# Project

## Description

This project aims to predict the country of origin of artists using the MusicBrainz Dataset. It leverages Apache Spark to optimize the data management and training of the model. The Goal of the project is to:

1. Implement a simple machine learning use case.
2. Scale data management and processing using Apache Spark.

## Motivation

Our "artist country of origin" use case is based on a relatively large dataset. Only the Artist <-> Country relationship data takes up over one million entries:

```sql
musicbrainz> SELECT COUNT(*) FROM artist JOIN area ON artist.area = area.id;
+---------+
| count   |
|---------|
| 1112886 |
+---------+
SELECT 1
Time: 0.089s
```

Trying to create a machine learning pipeline without taking in consideration the data management side of things inherently brings up memory issues. Our first version for example, had following errors:

```shell
23/12/27 10:06:08 WARN DAGScheduler: Broadcasting large task binary with size 254.3 MiB

...

Exception in thread "RemoteBlock-temp-file-clean-thread" java.lang.OutOfMemoryError: Java heap space Exception in thread "dispatcher-HeartbeatReceiver" java.lang.OutOfMemoryError: Java heap space Exception in thread "refresh progress" java.lang.OutOfMemoryError: Java heap space 23/12/27 10:08:06 ERROR Utils: Uncaught exception in thread executor-heartbeater java.lang.OutOfMemoryError: Java heap space

org.apache.spark.SparkException: Not enough memory to build and broadcast the table to all worker nodes. As a workaround, you can either disable broadcast by setting spark.sql.autoBroadcastJoinThreshold to -1 or increase the spark driver memory by setting spark.driver.memory to a higher value
```

Therefore, a bigger focus on the data scalability was needed.
