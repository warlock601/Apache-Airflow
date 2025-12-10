# Building DAGs with Airflow

- Whatever DAG we want to create, its code will be written inside a file in "dags" folder in the setup that is created using "astro dev init". Let say we created "mlpipeline.py". Consider this as a module for DAG in which we will define all the tasks. 
- PythonOperator is used to define a task based on a python function.
- Tasks will be having dependencies which we will be displaying or we'll follow a specific flow such that which task needs to be executed first and so on. 
- While defining tasks inside a DAG, we use "python_callable" which will call the function that we wanna use for that task. PythonOperator knows that this is a function.
</br>
Consider this example DAG: </br>

```bash

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
    schedule_interval='@weekly'                                       
) as dag: 
    
    ## Define the task
    preprocess=PythonOperator(task_id="preprocess_task",python_callable=preprocess_data)
    train=PythonOperator(task_id="train_task",python_callable=train_model)
    evaluate=PythonOperator(task_id="evaluate_model",python_callable=evaluate_model)
    
    ## set dependencies (specify the order to execute tasks)
    preprocess >> train >> evaluate

```
```bash
astro dev start
```
<img width="2736" height="1208" alt="image" src="https://github.com/user-attachments/assets/e40b2c63-8b9b-4c63-819e-bc7a5684309d" />

Note: If you are running Airflow 2.6+ or 2.7+ inside Astronomer, there might be some syntax changes such as the DAG constructor no longer accepts schedule_interval. Airflow deprecated "schedule_interval" and replaced it with "schedule"
