# Implementation

## Pipeline structure

**TODO most important steps** 

## Big Data

As a Big Data project, our machine learning pipeline encounters challenges in volume, variety, and velocity. 

1. **Volume**: Our dataset is composed of structured data, filled with different tables and relations. The challenge lies in discerning which data are most relevant and should be utilized, given the big dataset at our disposal.
2. **Variety**: Our dataset is notably structured, comprising various data forms and intricate relationships. This diversity necessitates good processing to effectively leverage the different data types and their associations.
3. **Velocity**: Although not directly used in the project, the concept of velocity is indirectly significant. The MusicBrainz dataset, our primary data source, supports continuous updates. This constant flow of updates suggests that an future extension of our project could involve periodically refreshing our model with the latest data from the database, thereby ensuring its relevance and accuracy over time. With this, a continuous integration of new data into our model could be possible.

Addressing our project's challenges with traditional technologies would introduce various difficulties, particularly in terms of scalability and feature management, as highlighted above. For instance, scaling the pipeline to accommodate an extensive set of features presents a significant hurdle when relying on conventional systems. These systems often lack the flexibility and efficiency needed to process and analyze large volumes of complex data effectively. This underscores the necessity for adopting more advanced, Big Data-oriented solutions to overcome these obstacles and achieve the desired outcomes in our project's conclusion.

## Correctness and shortcuts

Upon analyzing the entire pipeline, it should be noted that the results, in terms of machine learning and data science efficacy, are not optimal. However, optimizing machine learning outcomes was not the primary objective of this project. Instead, our focus was on exploring Spark's capabilities in managing machine learning pipelines for large datasets.

In future developments, there is potential to enhance the accuracy and effectiveness of the results, for instance, by refining the feature engineering and optimizing general machine learning and data science methodologies.

Despite these challenges, the project proved to be an insightful and valuable exploration into applying big data techniques within machine learning contexts. Our experiences have opened avenues for further investigation into aspects such as capability, reliability, and maintainability of big data solutions in machine learning applications.
