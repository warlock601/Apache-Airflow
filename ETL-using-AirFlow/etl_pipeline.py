from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import json

## Define the DAG
with DAG(
    dag_id='nasa_apod_postgres',
    start_date=datetime(2025,12,14),
    schedule='@daily',
    catchup=False
) as dag:
    
    ## Step 1: Create the table if it does not exist
    @task
    def create_table():
        ## initialize the postgreshook
        postgres_hook=PostgresHook(postgres_conn_id="my_postgres_connection")

        ## sql query to create the table
        create_table_query="""
        CREATE TABLE IF NOT EXISTS apod_data (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            explanation TEXT,
            url TEXT,
            date DATE,
            media_type VARCHAR(50)
        );
        """

        ## Execute the table creation query 
        postgres_hook.run(create_table_query)

    ## Step 2: Extract the NASA API data(APOD)-Astronomy Picture of the Day [Extract Pipeline]
    extract_apod=SimpleHttpOperator(
        task_id='extract_apod',
        http_conn_id='nasa_api',                                      # Coonection ID defined in Airflow for NASA API
        endpoint='planetary/apod',                                    # NASA API endpoint for APOD
        method='GET',
        data={"api_key":"{{conn.nasa_api.extra_dejson.api_key}}"},    # Use the API key for connection.
        response_filter=lambda response:response.json(),              # To convert data received to JSON (response to)
    )



    ## Step 3: Transform the data (pick the info that I need to save)
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


    ## Step 4: Load the data into Postgres SQL
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

    ## Step 5: Verify the data DBViewer



    ## Step 6: Define the task dependencies.
    create_table_task=create_table()
    #create_table >> extract_apod      # Ensure the table is created before extraction
    api_response=extract_apod.output
    # transform
    transformed_data=transform_apod_data(api_response)
    # load
    load_data_task=load_data_to_postgres(transformed_data)

    create_table_task >> extract_apod >> transformed_data >> load_data_task
