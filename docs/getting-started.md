# Getting started

> This getting started guide is made to be able to run the [Jupyter notebook](../notebooks/spark.ipynb) with it's associated pipeline

## Get Dataset

Our pipeline leverages the MusicBrainz Dataset, an extensive music database encompassing a wide range of data, including music recordings, artist profiles, and album details. This documentation outlines two approaches for integrating the dataset: one for deploying the full dataset and another for utilizing a subset of the dataset. While our analyses throughout this documentation are based on the complete dataset, we recommend starting with the smaller version for simplicity and ease of use. This approach allows for quicker setup and initial testing, providing a more manageable entry point into working with the MusicBrainz data.

### Full dataset

For our pipeline implementation, we utilized the PostgreSQL data dump from the MusicBrainz dataset. The complete dump is available for download at [Metabrainz](https://metabrainz.org/datasets/postgres-dumps#musicbrainz). Following the download, we employed MusicBrainz's PostgreSQL importer, [mbslave](https://github.com/acoustid/mbslave#database-setup), to integrate the dataset into our environment. The critical command for initializing the database with this tool is `mbslave init`. Detailed instructions for executing this command can be found on the [mbslave GitHub page](https://github.com/acoustid/mbslave#database-setup). This setup process is essential for preparing the MusicBrainz dataset for analysis within our pipeline.

### Smaller dataset

For testing purposes, utilizing a smaller dataset is more convenient. We provide such a dataset, accessible via our [OneDrive](https://1drv.ms/f/s!AqG36zRZC6b8kE_cVyJCYsaPgnTE?e=EFnXUW). Downloading this dataset should take approximately 5 to 10 minutes. Ensure you download both the actual data dump and the accompanying schema dump provided in the link. After acquiring the dump, proceed with the following steps to set up the PostgreSQL database:

1. Install a PostgresSQL. On Mac, the easiest way is with the [Postgresapp](https://postgresapp.com/) 
2. Connect to the PostgreSQL Database: `psql`
3. Create User: `CREATE USER musicbrainz WITH PASSWORD 'yourpassword';`
4. Create DB: `CREATE DATABASE musicbrainz OWNER musicbrainz;`
5. Exit an enter musicbrainz DB: `psql -U musicbrainz -d musicbrainz`
6. Create Schema: `CREATE SCHEMA musicbrainz;`
7. Import Schema: `psql -U musicbrainz -d musicbrainz -f schema_dump.sql` (Ignore the errors for the data that does not exist)
8. Import Dump: `psql -U musicbrainz -d musicbrainz -f dump.sql`
9. Check the data:
    a. `psql -U musicbrainz -d musicbrainz`
    b. `select name from artist limit 10;`

## Jupyter Notebook

To start the pipeline, a Jupyter Notebook is employed, which establishes connections to both the PostgreSQL database and the Spark engine. The following requirements are necessary:

1. Java: Required for running Apache Spark.
1. Python3: The primary programming language for the project.
1. Apache Spark: For handling large-scale data processing. 

A guide on how to install the technologies above for Mac, can be found [here](https://gist.github.com/daniel-vera-g/2c3deb6f7c0574698ac5c32a4d9913ca). After installing the needed requirements, the jupyter notebook can be run:

1. Create virtual environment: `python3 -m venv $PWD`
2. Activate virtual environment: `source ./bin/activate`
3. Install packages:
  - `pip3 install notebook`
  - `pip3 install findspark`
4. Start jupyter notebook: `jupyter notebook`
5. Start Spark Nodes:
  - Master: `./bin/spark-class org.apache.spark.deploy.master.Master`
  - 3x Worker: `./bin/spark-class org.apache.spark.deploy.worker.Worker spark://192.168.178.28:7077`
6. Download the [PostgreSQL JDBC Driver](https://jdbc.postgresql.org/) and set the path in the jupyter notebook
7. Set configuration variables at the top of the notebook
8. Run! (Make sure Spark is running and the database connection works)
