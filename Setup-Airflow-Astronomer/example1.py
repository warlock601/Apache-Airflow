from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

## Define task 1
def preprocess_data():
    print("preprocessing data")

## Define task 2
def train_model():
    print("Training Model...")

## Define Task 3
def evaluate_model():
    print("Evaluate model")

## Define the DAG
with DAG(
    'ml_pipeline',                          # name of DAG
    start_date=datetime(2025,12,10),
    schedule="@weekly"                                       
) as dag: 
    
    ## Define the task
    preprocess=PythonOperator(task_id="preprocess_task",python_callable=preprocess_data)
    train=PythonOperator(task_id="train_task",python_callable=train_model)
    evaluate=PythonOperator(task_id="evaluate_model",python_callable=evaluate_model)
    
    ## set dependencies (specify the order to execute tasks)
    preprocess >> train >> evaluate
