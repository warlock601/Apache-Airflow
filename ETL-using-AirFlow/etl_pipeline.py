from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
import json

## Define the DAG
with DAG(
    dag_id='nasa_apod_postgres',
    start_date=days_ago(1),
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



    ## Step 4: Load the data into Postgres SQL



    ## Step 5: Verify the data DBViewer



    ## Step 6: Define the task dependencies.
