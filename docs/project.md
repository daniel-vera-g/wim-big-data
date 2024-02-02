# Project

## Motivation

In the past, we have successfully acquired insights into how machine learning pipelines work and consider them a fascinating aspect of data processing and information technology. Our previous experience has given us an understanding of the challenges involved in developing and optimizing these pipelines.

For this reason, we were very interested in exploring the implementation and performance of machine learning pipelines in Apache Spark and working out the differences between a “regular” machine learning pipeline in Python and one in Pyspark. We were also curious to find out how Spark scales using an example.

Therefore we wanted to implement a simple machine learning use case and use it as an example to scale data management using Apache Spark. This requires a relatively large data set in order to fulfill the requirements of a "big data" use case.

## Description

We started by looking for a suitable data set that was both easily scalable and appealing in terms of content. [The Million Song dataset](http://millionsongdataset.com/) was our first choice as it provided a large amount of data and the music theme suited us. Unfortunately, this dataset is quite “old” as it has not been updated since the 2010s and the additional code was rather outdated (very old Python version). Furthermore, we were not able to access the dataset because the links provided did not work properly and the underlying data was missing.

Therefore, we looked for another music-related dataset that fulfilled our requirements. The [MusicBrainz’ dataset](https://musicbrainz.org/doc/MusicBrainz_Database) is equally large and provides easy (and free) access. The MusicBrainz Database is built on the PostgreSQL relational database engine and contains all of MusicBrainz’ music metadata. This data includes information about artists, releases, recordings, labels and more, as well as the many relationships between them. The database also contains a full history of all the changes that the MusicBrainz’ community has made to the data.

More information on the first steps with the database can be found under [Getting started](./getting-started.md) 

As the schema on the MusicBrainz’ website suggests, the database contains many tables and relations between them. As we preferred a basic/ simple use case, we only used a small amount of the tables provided for our prototype. More information about the used data is documented under the [data](./data.md) section.

This project aims to predict the country of origin of artists with the information of the artists name, its alias and language. It leverages Apache Spark to optimize the data management and training of the model. The most important libraries that were used will be explained in the following:

As seen in the [Jupyter Notebook](../notebooks/spark.ipynb), several packages from the Apache Spark/Pyspark library "pyspark.ml" such as the pipeline package were important for building the pipeline for machine learning. Packages from the "pyspark.ml.feature" library were used for the transformation and normalization of features. The machine learning model, a logistic regression, originates from the "pyspark.ml.classification" library. This includes the algorithm for the regression, but also for the subsequent evaluation of the results.

This use case does not focus on the optimization of the machine learning model with its hyperparameters, but is primarily intended to demonstrate the general use of Apache Spark for machine learning applications.
