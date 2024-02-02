# Implementation

Our initial implementation of the machine learning pipeline was done via a Jupyter Notebook, serving as the project's first iteration.  
With optimization as a core goal for the second version, we planned and partially implemented a concept centered around batch processing. This approach was designed to continuously process the data required for the machine learning pipeline.

## Jupyter notebook Pipeline

As the explanation of the different pipeline steps is easier with the code next to it, you can find a description of each step in the [Jupyter Notebook](../notebooks/spark.ipynb) 

## Batch processing version

After developing a the machine learning pipeline with Apache Spark, we wanted to optimize its stages. The central idea was to incorporate batch processing to enhance efficiency. Our strategy was as follows:

1. **Batch Range Definition**: We established a range to iterate over the dataset in manageable segments.
2. **Data Retrieval**: For each batch, data was fetched from the database.
3. **Batch Processing and Storage**: Each batch was processed and subsequently stored in Parquet format for efficient disk space usage.
4. **Data Aggregation**: Processed batches were then reloaded into memory and merged into a single DataFrame for the upcoming model training.

### Main Logic:

The core logic involved iterating over data in batches, processing each segment, and then combining them for the subsequent stages of the machine learning workflow.

Pseudocode:

```python
# Main batching and processing loop
for offset in range(0, total_rows, fetchsize):
    batch_id = offset // fetchsize
    logger(f"Processing batch {batch_id} with offset {offset} and fetchsize {fetchsize} ...")

    combined_artist_df = collect_data(spark, database_url, properties, fetchsize, offset)
    if combined_artist_df.count() == 0:
        logger(f"Batch {batch_id} is empty. Skipping ...")
        continue

    logger(f"Number of rows in batch {batch_id}: {combined_artist_df.count()}")
    isBatchProcessed = process_and_write_batch(combined_artist_df, batch_id, output_dir)
    num_batches += isBatchProcessed

# Combine processed batches for analysis
combined_df = combine_batches(num_batches, output_dir)
```

### Processing and Writing Batches:

The `process_and_write_batch` function applies data transformations, normalization, and preprocessing before saving each batch to disk in Parquet format:

Pseudocode:

```python
def process_and_write_batch(batch_df, batch_id, output_dir):
    # Data transformation and cleaning
    batch_df = clean_data(batch_df)
    if batch_df.count() == 0:
        logger(f"Batch {batch_id} is empty. Skipping ...")
        return 0
    # Further data processing steps
    processed_data = run_preprocessing_pipeline(batch_df)
    # Save processed batch
    batch_output_path = f"{output_dir}/batch_{batch_id}.parquet"
    logger(f"Writing batch {batch_id} to {batch_output_path}")
    processed_data.write.mode('overwrite').parquet(batch_output_path)
    return 1
```

As mentioned this code is simplified pseudocode. The complete conceptual implementation is available in the [scalable-spark.py](../notebooks/scalable-spark.py) file.

### Challenges and Future Directions:

The primary challenges encountered were related to efficiently querying the data and merging the individual Parquet files. Despite aiming to optimize memory and CPU utilization, this batch processing approach still demands significant resources for model training. Future efforts would focus on getting the merging of the different Parquet files properly done and enhancing the efficiency of model training.

Although a fully working version was not implemented, this concept significantly contributed to our understanding of Spark and established a good foundation for future improvements in leveraging Spark for scalable machine learning pipelines.
