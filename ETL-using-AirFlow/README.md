# AirFlow ETL Pipeline

### Introduction to ETL
An ETL pipeline is a data-engineering workflow that Extracts data from source systems (such as APIs, Internal Databases, IoT devices etc), Transforms it into a usable format, and Loads it into a target system such as a data warehouse, data lake, or analytics store. ETL pipelines are foundational in 
analytics, BI, reporting, and ML workloads. 
- Extract: Pipeline ingests raw data from various sources: Databases(SQl, NoSQL), APIs and microservices, Log streams (Kafka, Kinesis), Files (CSV, Parquet, JSON) etc.
- Transform: Raw data is cleaned, structured, and enriched to meet business requirements. Common transformations include: Data cleaning (handling nulls, deduplication, type conversions), Normalization/denormalization, Aggregations and business metrics, Validation and quality rules. Transformations can
  be executed using SQL engines, Spark, dbt, Python, or workflow orchestrators (such as AirFlow, MLFlow etc).
- Load: The processed dataset is stored in the destination system: Data warehouse (Snowflake, BigQuery, Redshift), Data lake (S3, ADLS, GCS), Lakehouse (Databricks, Apache Iceberg/Hudi/Delta), Downstream ML pipelines. Load Strategies: Full loads, Incremental loads, Merge/upsert logic, Partitioning and indexing

###  A typical ETL system includes:
- Orchestration engine: Airflow, Dagster, Prefect
- Compute engine: Spark, AWS Glue, BigQuery SQL, Databricks
- Data stores: OLTP sources, S3/GCS lakes, warehouse
- CI/CD for pipeline code
- Observability: logs, metrics, data quality (Great Expectations, Monte Carlo)

### ETL v/s ELT
ELT is common in modern cloud architectures, but ETL is still used when heavy transformation is required before loading. ETL is suitable when transformation requires compute layer outside warehouse. ELT is suitable when warehouse is scalable enough to transform raw data


## Problem Statement
We'll take a specific API, we'll read the data from it. Then we'll be doing some kind of transformation (like converting it into Json) and then we save it into a database. We'll be taking NASA API
