# Big Data Project

> Artist Country of Origin Prediction

1. [Description](#description)
2. [Motivation](#motivation)
3. [Getting Started](#getting-started)
   * [Requirements](#requirements)
   * [Running](#running)
4. [References](#references)

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

Therefore a bigger focus on the data scalability was needed. For this, Spark was used.

## Getting Started

### Requirements

1. **MusicBrainz Dataset**: A the smaller version of the dataset is sufficient
2. **Software Setup**:
   - Java: Required for running Apache Spark.
   - Python3: The primary programming language for the project.
   - Apache Spark: For handling large-scale data processing. 

   A setup guide for MacOS can be found [here](https://gist.github.com/daniel-vera-g/2c3deb6f7c0574698ac5c32a4d9913ca).

### Running

1. Start Jupyter Notebook
2. Set configuration variables at the top of the notebook
3. Run!

## References

- [MusicBrainz Database Documentation](https://musicbrainz.org/doc/MusicBrainz_Database): Detailed information about the MusicBrainz Dataset.
- B. Chambers and M. Zaharia, Spark: The Definitive Guide : Big Data Processing Made Simple. 2017.
- S. Ryza, U. Laserson, S. Owen, and J. Wills, Advanced Analytics with Spark: Patterns for Learning from Data at Scale. O’Reilly Media, 2017.