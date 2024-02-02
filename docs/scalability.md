# Scalability

To implement a machine learning pipeline, we initially adopted a straightforward approach that utilized standard pipelines, incorporating Apache Spark to leverage its scalability and efficient resource utilization features. This initial version was based on Spark's ability to parallelize tasks across the available hardware, optimizing the use of resources such as memory and CPU. However, the scalability and parallelization were inherently limited by the capacity of the provided Memory and CPU.

Recognizing the need for enhanced scalability, we planned and roughly prototyped a second version of the pipeline focused on optimizing resource usage. This version aimed to reduce the memory footprint through the strategic use of batch processing, thereby allowing for more efficient data handling and processing on the same hardware.

1. [Jupyter Notebook of machine learning pipeline](../notebooks/spark.ipynb) 
2. [Rough prototype of the batch processing version](../notebooks/scalable-spark.py) 

In the current configuration of our pipeline, scalability is achieved by distributing tasks across multiple Spark workers. Parallelization is accomplished by breaking down the machine learning tasks into smaller, manageable operations that can be executed concurrently across these workers. For this purpose, we utilize machine learning libraries from PySpark, which have been optimized for the use within the Spark Engine. Through this, data is also distributed among the workers in a manner that balances the load effectively, ensuring that each worker processes a roughly equal share of the data.  
Example use of the optimized logistic regression PySpark package in our machine learning pipeline:

```python
from pyspark.ml.classification import LogisticRegression

# Initialize the Logistic Regression model
lr = LogisticRegression(featuresCol="scaledFeatures", labelCol="country_index")

# Fit the model on the training data
lrModel = lr.fit(train_data)
```

This architecture allows our solution to scale dynamically with the addition of more Spark workers or resources, thereby accommodating larger datasets and more complex computational tasks.

## Scalability tests

<!-- ## Variable Memory and CPU -->

To evaluate the scalability of our Spark pipeline to varying resource allocations, we executed the pipeline multiple times, each time incrementing the executor memory and CPU allocations. This setup mirrored the configuration used in the fault tolerance test, comprising 1 master node and 3 worker nodes. During each iteration, we recorded the number of Java processes and the number of executors assigned to each worker. Furthermore, we measured the completion time for each stage of the pipeline to facilitate performance comparison:

| Executor Memory (GB) | Executor Cores | Number Java processes | Number executors per worker |
|---|---|---|---|
| 2 | 2 | 20 | 5 | 
3 | 3 | 14 | 3
6 | 6 | 8 | 1
8 | 8 | 8 | 1

The data above reveals a clear correlation between resource allocation and the number of executors per worker. This indicates that as the resource allocation per executor increases, fewer executors are required to manage the workload, resulting in a reduction in the total number of Java processes.
Regarding executor efficiency, it is observed that a plateau in the number of executors per worker is reached with 6 GB of memory and 6 cores. This suggests an optimal point of resource allocation, beyond which additional resources do not significantly impact the number of executors needed per worker.

Besides documenting ressource data, also the time for the pipeline stages was measured using the [`%%time`](https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-time) python expression on each code cell. The operation with the longest time was the evaluation step. In the following, the results of the different measurements are shown:

Executor Memory (GB) / Cores | Time to completion in seconds | Time for evaluation step in seconds
--- | --- | ---
2 | 434 | 336
3 | 399 | 316
6 | 363 | 294
8 | 356 | 284

As depicted in the table, time to completion improves as expected with the addition of resources. Interestingly, the time difference between the first three resource increases is quite substantial compared to the last increment. Specifically, the jump from 6 GB / 6 Cores to 8 GB / 8 Cores did not result in a significantly greater improvement in completion time. This indicates that adding more resources to a single executor beyond a certain point shows diminishing returns in terms of time saved.
It's important to highlight that these tests were conducted with a dataset of 800,000 rows in a standalone mode on a single computer. Deploying the solution on a more scalable infrastructure, such as a production-grade cluster, might get more benefits from additional resource allocation, especially when resources are distributed across multiple machines.

## Bottlenecks and Improvements

When identifying bottlenecks, it is crucial to analyze our code for steps that are intensive in terms of IO, memory, and CPU. 
The most IO-intensive phase in our code is the data collection, where data is fetched from the database. To improve this, we planned to implement data partition reading, which allows for fetching only specific segments of the data at a time. Further details on this strategy can be found in the [implementation section](./implementation.md).

Memory bottlenecks primarily arise in our pipeline from managing large DataFrames in memory, a consequence of operations such as joins and aggregations. These operations not only consume significant memory but also lead to CPU bottlenecks. The used data preprocessing steps like StringIndexer, OneHotEncoder, and VectorAssembler are particularly demanding in terms of computation. However, leveraging Spark's built-in functions helps a lot with improving performance by optimizing these resource-intensive processes.

The measurements indicate that the evaluation step is the most resource-intensive part of the process, primarily due to the demanding operations employed at this stage. Among these, the cross-validation process stands out as particularly resource-heavy. In the context of Spark, cross-validation necessitates multiple data splits, leading to extensive data shuffling. This data shuffling is resource-intensive, contributing significantly to the resource consumption.

## Scaling on production system

Summarizing, Spark demonstrates very good resource management capabilities by dynamically adjusting the number of executors based on the allocated resources, ensuring optimal utilization and efficiency. However, it's important to recognize that scalability on a local machine is limited to the given ressources. Transitioning to a cluster setup, where resources can be scaled horizontally by adding more nodes, can bring big scalability and performance improvements, allowing Spark to distribute workloads more effectively across a broader array of computational resources.

<!-- --- -->

<!-- 2: 2+18+4+13+8+13+30+5*60+36+10 = 434 -->
<!-- 3: 1+15+3+11+8+11+28+5*60+16+6 = 399 -->
<!-- 6: 2+10+3+8+7+8+26+4*60+54+5 = 363 -->
<!-- 8: 1+10+3+3+9+6+9+26+4*60+44+5 = 356 -->

<!-- **Input:**  -->

<!-- - Variable Ressourcen -->
<!-- - Konstante Datenmenge -->

<!-- **Output:**  -->

<!-- - Zeit -->
<!-- - Spark Auslastung -->

<!-- --- -->

<!-- To assess stability, we conducted two distinct evaluations. The first involved processing variable data volumes while keeping the resource allocation constant, and the second entailed processing a fixed data volume with varying levels of resources. Due to the batch processing version not being fully implemented, all tests were carried out using the Jupyter Notebook based machine learning pipeline. -->

<!-- ### Variable data and fixed resources -->

<!-- **Input:**  -->

<!-- - Konstante Ressourcen -->
<!-- - Variable Datenmenge -->
<!--     - What happens when the amount of data increases in the orders of magnitude (1x/10x/100x... or 2x/4x/8x/16x/...)? -->
<!--     - What happens if request or query intake increases ore latency conditions decrease in magnitude? -->

<!-- **Output:**  -->

<!-- - Zeit -->
<!-- - Spark Auslastung -->

<!-- TODO  -->

<!-- - What happens when data or queries skew and bias -->
<!-- - Is your system real-time capable? -->
<!-- - Are there any setup/bootstrapping etc. costs? -->
<!-- - How does the "data" run through the system? -->
<!-- How would you dimension a real system or setup given realistic data or query sets?" -->
