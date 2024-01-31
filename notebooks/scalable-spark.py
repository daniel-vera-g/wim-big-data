#!/usr/bin/env python

from helper import logger

## --- Project configuration --- ##

import os
from pyspark.sql import SparkSession
import findspark
findspark.init()

# Java configuration
jarConfigPath = "/Users/d.veragillard/edu/semester/WIM-1/big-data-advanced-database/bd-project/postgresql-42.7.1.jar"

# Spark configuration
allocated_memory = "6g"
allocated_cores = "6"  

# Database configuration
database_url = "jdbc:postgresql://localhost:5432/musicbrainz"
properties = {"user": "musicbrainz", "password": "musicbrainz", "driver": "org.postgresql.Driver"}

# Processed batches configuration
output_dir = "./notebooks/batches_dir"
fetchsize = 10000  # Define batch size
total_rows = 1000000  # Total number of rows in feature table (Is dynamically determined for each feature)

# Initialize Spark session with some spark tunings:
# We attach more memory to the driver and executors
# We use the G1 garbage collector for better performance
# We add more cores to the driver and executors
spark = SparkSession \
    .builder \
    .appName("MusicBrainz PostgreSQL Connection") \
    .config("spark.jars", jarConfigPath) \
    .config("spark.executor.memory", allocated_memory) \
    .config("spark.driver.memory", allocated_memory) \
    .config("spark.executor.extraJavaOptions", "-XX:+UseG1GC") \
    .config("spark.driver.extraJavaOptions", "-XX:+UseG1GC") \
    .config("spark.executor.cores", allocated_cores) \
    .config("spark.driver.cores", allocated_cores) \
    .config("spark.eventLog.gcMetrics.youngGenerationGarbageCollectors", "G1 Young Generation") \
    .config("spark.eventLog.gcMetrics.oldGenerationGarbageCollectors", "G1 Old Generation") \
    .getOrCreate()

## --- Data collection --- ##

from pyspark.sql.functions import broadcast

# Collect data from database and join tables
# Uses fetchsize and offset to support incremental processing
def collect_data(spark, database_url, properties, limit, offset):
    # First get general Artist and Area(The country to predict) and additional Artist/Country information that could hint about the artist country
    # Already do cleaning in this stage by only selecting relevant columns
    
    artist_query = f"(SELECT * FROM artist order by name LIMIT {limit} OFFSET {offset}) AS temp_table"
    area_query = f"(SELECT * FROM area order by name LIMIT {limit} OFFSET {offset}) AS temp_table"
    language_query = f"(SELECT * FROM language LIMIT {limit} OFFSET {offset}) AS temp_table"
    alias_query = f"(SELECT * FROM artist_alias LIMIT {limit} OFFSET {offset}) AS temp_table"

    # TODO DOING!
    
    # Read data from artist and area tables with only necessary columns
    artist_df = spark.read.jdbc(url=database_url, table=artist_query, properties=properties).select("id", "name", "area")
    area_df = spark.read.jdbc(url=database_url, table=area_query, properties=properties).select("id", "name")
    
    # Assuming area_df is smaller and can be broadcasted
    # Broadcast join for artist and area tables
    artist_country_df = artist_df.join(broadcast(area_df), artist_df.area == area_df.id)
    
    # Select relevant columns
    artist_country_df = artist_country_df.select(artist_df.name, area_df.name.alias("country"))
    
    # Read more that could be useful for the analysis
    language_df = spark.read.jdbc(url=database_url, table=language_query, properties=properties).select("id", "name")
    alias_df = spark.read.jdbc(url=database_url, table=alias_query, properties=properties).select("artist", "name")
    
    # Join tables...
    # Use explicit column names to avoid ambiguity
    artist_language_df = artist_df.join(language_df, artist_df.id == language_df.id).select(artist_df.name, language_df.name.alias("language"))
    artist_alias_df = artist_df.join(alias_df, artist_df.id == alias_df.artist).select(artist_df.name, alias_df.name.alias("alias"))
    
    # Combining all data into one dataframe with left outer join
    combined_artist_df = artist_country_df \
        .join(artist_alias_df, ["name"], "left_outer") \
        .join(artist_language_df, ["name"], "left_outer")

    logger(combined_artist_df.show(10))

    return combined_artist_df

## --- Data preprocessing --- ##

from pyspark.sql.functions import col, when

def clean_data(combined_artist_df):
    # Dropping rows where 'country', 'name' is null or empty
    combined_artist_df = combined_artist_df.filter(combined_artist_df.country.isNotNull())
    combined_artist_df = combined_artist_df.filter(combined_artist_df.name.isNotNull())
    
    # Remove all rows in combined_artist_df that have null values
    combined_artist_df = combined_artist_df.na.drop()

    logger(f"Number of rows after dropping null values: {combined_artist_df.count()}")

    return combined_artist_df

from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler, StandardScaler
from pyspark.ml import Pipeline

def transform_data(combined_artist_df):
    # Transform feature strings into more suitable formats. To do this:
    # 1. Use `StringIndexer` to convert the strings in the columns into indices(Like unique IDs)
    # 2. Then use `OneHotEncoder` to convert the categorical indices into a binary vector(F.ex `[0,1,0,...]`)

    # String Indexing for all categorical columns
    indexers = [StringIndexer(inputCol=column, outputCol=column+"_index", handleInvalid="keep").fit(combined_artist_df) 
            for column in ["name"]]  # Exclude 'country'
    
    label_stringIdx = StringIndexer(inputCol="country", outputCol="country_index")

    # One-Hot Encoding for all indexed columns
    encoders = [OneHotEncoder(inputCol=indexer.getOutputCol(), outputCol=indexer.getOutputCol()+"_vec")
                for indexer in indexers]

    return indexers, encoders, label_stringIdx

def normalize_data(encoders):
    # Scale transformed values to fixed range. To do this:
    # 1. Use `VectorAssembler` to combine multiple columns into a single vector column. Helps with machine learning algorithms
    # 2. Then apply `StandardScaler`. It helps, to make sure that the model is not influenced by features with larger scales

    # Vector Assembling all the features
    assemblerInputs = [encoder.getOutputCol() for encoder in encoders]
    assembler = VectorAssembler(inputCols=assemblerInputs, outputCol="features")
    
    # Feature normalization
    scaler = StandardScaler(inputCol="features", outputCol="scaledFeatures")

    return assembler , scaler

def run_preprocessing_pipeline(combined_artist_df, indexers, encoders, label_stringIdx, assembler, scaler):
    # Finally combine all steps into one transformation / normalization pipeline and run it:

    # Building a Pipeline for transformations
    pipeline = Pipeline(stages=indexers + encoders + [assembler, scaler, label_stringIdx])

    
    # Transforming the data
    model = pipeline.fit(combined_artist_df)
    transformed_df = model.transform(combined_artist_df)

    return transformed_df

## --- Data splitting --- ##

def split_data(transformed_df):
    
    logger("Splitting data into training, validation, and testing sets ...")
    # Splitting the data into training, validation, and testing sets
    train_data, val_data, test_data = transformed_df.randomSplit([0.7, 0.15, 0.15], seed=42)
    
    # Show the count of each dataset
    logger(f"Training Data Count: {train_data.count()}")
    logger(f"Validation Data Count: {val_data.count()}")
    logger(f"Testing Data Count: {test_data.count()}")

    return train_data, val_data, test_data

## --- Model training --- ##

from pyspark.ml.classification import LogisticRegression

def train_model(train_data):
    # Initialize the Logistic Regression model
    from pyspark.ml.linalg import Vectors

    # Convert the scaledFeatures column to DenseVector
    from pyspark.ml.linalg import VectorUDT

    train_data = train_data.withColumn("scaledFeatures", train_data["scaledFeatures"].cast(VectorUDT()))

    lr = LogisticRegression(featuresCol="scaledFeatures", labelCol="country_index")

    # Fit the model on the training data
    lrModel = lr.fit(train_data)

    # logger the coefficients and intercept
    logger("Coefficients: " + str(lrModel.coefficientMatrix))
    logger("Intercept: " + str(lrModel.interceptVector))

    # You can also logger a summary of the model over the training set
    trainingSummary = lrModel.summary
    logger("Accuracy: ", trainingSummary.accuracy)
    logger("False Positive Rate: ", trainingSummary.weightedFalsePositiveRate)
    logger("True Positive Rate: ", trainingSummary.weightedTruePositiveRate)
    logger("F1-Measure: ", trainingSummary.weightedFMeasure())
    logger("Precision: ", trainingSummary.weightedPrecision)
    logger("Recall: ", trainingSummary.weightedRecall)

    return lr

## --- Model evaluation --- ##

from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

def evaluate_model(lr, val_data, train_data):

    # Create a ParamGrid for tuning parameters
    paramGrid = ParamGridBuilder() \
        .addGrid(lr.regParam, [0.01, 0.1, 1.0]) \
        .addGrid(lr.maxIter, [10, 50, 100]) \
        .build()
    
    # Create a CrossValidator
    cv = CrossValidator(estimator=lr, 
                        estimatorParamMaps=paramGrid, 
                        evaluator=MulticlassClassificationEvaluator(labelCol="country_index", predictionCol="prediction"), 
                        numFolds=3)
    
    # Run cross-validation, and choose the best set of parameters.
    cvModel = cv.fit(train_data)
    
    # Use the best model to make predictions on the validation data
    val_predictions = cvModel.transform(val_data)
    
    # Evaluate the model
    evaluator = MulticlassClassificationEvaluator(labelCol="country_index", predictionCol="prediction")
    accuracy = evaluator.evaluate(val_predictions, {evaluator.metricName: "accuracy"})
    f1 = evaluator.evaluate(val_predictions, {evaluator.metricName: "f1"})
    
    logger(f"Validation Accuracy: {accuracy}")
    logger(f"Validation F1 Score: {f1}")

    return cvModel, evaluator

## --- Model testing --- ##

def test_model(cvModel, evaluator, test_data):
    # Use the best model to make predictions on the test data
    test_predictions = cvModel.transform(test_data)
    
    # Evaluate the model on test data
    test_accuracy = evaluator.evaluate(test_predictions, {evaluator.metricName: "accuracy"})
    test_f1 = evaluator.evaluate(test_predictions, {evaluator.metricName: "f1"})
    
    logger(f"Test Accuracy: {test_accuracy}")
    logger(f"Test F1 Score: {test_f1}")

## --- Batch processing --- ##

# Function to process and write each batch
def process_and_write_batch(batch_df, batch_id, output_dir):
    # Apply transformations and cleaning
    # print batch
    batch_df = clean_data(batch_df)
    if batch_df.count() == 0:
        logger(f"Batch {batch_id} is empty. Skipping ...")
        return 0
    transformation_data = transform_data(batch_df)
    normalized_data = normalize_data(transformation_data[1])
    processed_data = run_preprocessing_pipeline(batch_df, transformation_data[0], transformation_data[1], transformation_data[2], normalized_data[0], normalized_data[1])

    # Write processed batch to disk in Parquet format
    batch_output_path = f"{output_dir}/batch_{batch_id}.parquet"

    logger(f"Writing batch {batch_id} to {batch_output_path}")
    processed_data.write.mode('overwrite').parquet(batch_output_path)

    return 1

## --- Main --- ##

# Incrementally process query the database and process each batch for each feature
total_rows = spark.read.jdbc(url=database_url, table="artist", properties=properties).count()
num_batches = total_rows // fetchsize
num_batches = 0

logger(f"Total number of rows in feature table: {total_rows}")

for offset in range(0, total_rows, fetchsize):
    batch_id = offset // fetchsize

    logger(f"Processing batch {batch_id} with offset {offset} and fetchsize {fetchsize} ...")

    combined_artist_df = collect_data(spark, database_url, properties, fetchsize, offset)

    if combined_artist_df.count() == 0:
        logger(f"loggerBatch {batch_id} is empty. Skipping ...")
        continue

    logger(f"Number of rows in batch {batch_id}: {combined_artist_df.count()}")

    # Count the number of batches processed to determine the number of batches to combine later
    isBatchProcessed = process_and_write_batch(combined_artist_df, batch_id, output_dir)
    num_batches += isBatchProcessed

# Reading and combining processed batches
combined_df = None

logger(f"Number of batches processed: {num_batches}")

for batch_id in range(num_batches):
    batch_output_path = f"{output_dir}/batch_{batch_id}.parquet"
    if not os.path.exists(batch_output_path):
        continue

    batch_df = spark.read.parquet(batch_output_path)

    logger(f"Combining batch {batch_id} to combined_df dataframe ...")
        
    if combined_df is None:
        combined_df = batch_df
    else:
        # combined_df = combined_df.union(batch_df).distinct()
        combined_df = combined_df.unionAll(batch_df)

logger(f"Number of rows in combined_df: {combined_df.count()}")

# Continue with model training and evaluation on combined_df
split_datasets = split_data(combined_df)
lr = train_model(split_datasets[0])
# evaluation_data = evaluate_model(lr, split_datasets[1], split_datasets[0])
# test_model(evaluation_data[0], evaluation_data[1], split_datasets[2])
