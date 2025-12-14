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


## Pipeline Overview
- In Airflow if we want to go and hit an API, we have to use simple HTTP operator. More info about Airflow http operator:
https://airflow.apache.org/docs/apache-airflow-providers-http/stable/operators.html

- We need to insert the data inside the postgres database so for that we have something called as Postgres hook. The PostgresHook is a specialized interface used to interact with a PostgreSQL database. To create the table, we need to interact with the Database, like here Postgres and for that we will need "Postgres hook".

- We are creating postgres as a docker container, and as Astronomer is running the entire Airflow in a Docker container, both of these docker containers will need to interact with each other. So that entire configuration will be written in docker-compose.yml. Because we want multiple containers to interact with each other, let say a postgres and a mySQL container wants to interact so they should have a common Network to communicate with each other.
- Now we will generate the API key. Go to htttps://api.nasa.gov and fill in the details. Will receive an API key over email which we will use for interaction.</br>
   <img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/31c20d68-a2ce-4a3e-abab-593633a827a5" /></br>
  SimpleHttpdOperator is responsible for hitting the API and retreiving the information.</br>
  To check whether the API key is working or not, we will send a GET request and this will have all the details about the API like name, date, image etc.</br>
 using this: https://api.nasa.gov/planetary/apod?api_key=<key-value>. We'll get something like this: </br>
<img width="2744" height="318" alt="image" src="https://github.com/user-attachments/assets/a268f550-c93e-44f4-bbbd-d4b3a65acbdd" /></br>
  "http_conn_id" should basically map to this URL mentioned above. "planetary/apod" is written as an endpoint over here. Also we could've hardcoded the API key value but we want that AirFlow connection should provide the API key, so api+key" will be retreived from connection string of the airflow and this is specifically how we read that particular connection.
```bash
extract_apod=SimpleHttpOperator(
        task_id='extract_apod',
        http_conn_id='nasa_api',                                      # Coonection ID defined in Airflow for NASA API
        endpoint='planetary/apod',                                    # NASA API endpoint for APOD
        method='GET',
        data={"api_key":"{{conn.nasa_api.extra_dejson.api_key}}"},    # Use the API key for connection.
        response_filter=lambda response:response.json(),              # To convert data received to JSON (response to json)
    )
```
- Building Transformation & Load Pipeline: Once we receive the response from previous step, then only we can do the transformation. I'll be selecting some of the fields from the entire response and to get those field values, I'll use "response.get". If a particular key or field is not available, it will give me a blank response.
```bash
@task
    def transform_apod_data(response):
        apod_data={
            'title': response.get('title',''),
            'explanation': response.get('explanation',''),
            'url': response.get('url',''),
            'date': response.get('date',''),
            'media_type': response.get('media_type','')
        }
        return apod_data
```
- Loading the data into postgres: Inside the function, we'll ue postgres_hook which will further use postgres connection id.
```bash
@task
    def load_data_to_postgres(apod_data):

        ## Initialize the PostgresHook
        postgres_hook=PostgresHook(postgres_conn_id='my_postgres_connection')

        ## Define the SQL Insert query
        insert_query="""
        INSERT INTO apod_data (title, explanation, url, date, media_type)
        VALUES (%s, %s, %s, %s, %s);
        """

        ## Execute the SQL query
        postgres_hook.run(insert_query,parameters=(
            apod_data['title'],
            apod_data['title'],
            apod_data['title'],
            apod_data['title'],
            apod_data['title']
        ))
```
- DBViewer is used to confirm if the data is loaded into the database or not. Foe g: here it will check if the data is loaded into postgres or not.
- We'll specify the order of tasks because there will be dependencies. Like we need to ensure that table is created before extraction.</br>
  Usually in http operators, whatever variable is basically created, there will be a variable called output and inside that our entire response will be available.
```bash
    create_table_task=create_table()
    api_response=extract_apod.output
    # transform
    transformed_data=transform_apod_data(api_response)
    # load
    load_data_task=load_data_to_postgres(transformed_data)

    create_table_task >> extract_apod >> transformed_data >> load_data_task
```
- And then to run this DAG, we'll do
```bash
astro dev start
```
- In Airflow UI, go to Admin > Connections > Add 2 different connections
- Troubleshooting Tip: If in case you get port binding error while starting Airflow using Astro, like using "astro dev start", then stop the existing containers in Docker desktop that are using that specific port. error statement will be like this:
```bash
Error: error building, (re)creating or starting project containers: Error response from daemon: driver failed programming external
connectivity on endpoint etl-using-air-flow_a7e7a7-postgres-1 (c4a63a3c92abd405aa627363c6d050e2a19fd325e1648054d83a92e58833e705):
Bind for 127.0.0.1:5432 failed: port is already allocated
```
