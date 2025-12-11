# Maths Operation

## We'll define a DAG where the tasks are as follows
- Task 1: Start with an initial number (e.g. 10).
- Task 2: Add 5 to the number.
- Task 3: Multiple the result by 2
- Task 4: Subtract 3 from the result.
- Task 5: Compute the square of the result.


**context will be responsible in providing the information or the output from the previous function to the current one because there is a dependency.</br>
To define this context, we'll use a function called xcom_push which is provided by Airflow and this value, the reson we save it in that is that so that we can share those values within the task.

```bash
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

## Define function for each task

def start_number(**context):
    context['ti'].xcom_push(key='current_value',value=10)
    print("Starting number 10")


def add_five(**context):
    current_value=context['ti'].xcom_pull(key='current_value',task_ids='start_task')
    new_value=current_value + 5
    context["ti"].xcom_push(key='current_value',value=new_value)
    print(f"Add 5:{current_value}+5={new_value}")

def multiply_by_two(**context):
    current_value=context['ti'].xcom_pull(key='current_value',task_ids='add_five_task')
    new_value=current_value*2
    context["ti"].xcom_push(key='current_value',value=new_value)
    print(f"Multiple by 2:{current_value} * 2 = {new_value}")

def subtract_three(**context):
    current_value=context["ti"].xcom_pull(key='current_value',task_ids='multiple_by_two_task')
    new_value=current_value-3
    context["ti"].xcom_push(key='current_value',value=new_value)
    print(f"Subtract by 3:{current_value} - 3 = {new_value}")

def square_number(**context):
    current_value=context["ti"].xcom_pull(key='current_value',task_ids='subtract_by_three_task')
    new_value=current_value ** 2
    context["ti"].xcom_push(key='current_value',value=new_value)
    print(f"Subtract by 3:{current_value}^2 = {new_value}")


## Define the DAG
with DAG(
    dag_id='math_sequence_dag',
    start_date=datetime(2023,1,1),
    schedule="@once",
    catchup=False  

)as dag:

    ## Define the task
  start_task=PythonOperator(
    task_id='start_task',
    python_callable=start_number,
    
)
  
  add_five_task=PythonOperator(
    task_id='add_five_task',
    python_callable=add_five,
    
)
  
  multiply_by_two_task=PythonOperator(
    task_id='multiply_by_two_task',
    python_callable=multiply_by_two,
    
)
  
  subtract_three_task=PythonOperator(
    task_id='subtract_three_task',
    python_callable=subtract_three,
    
)
  
  square_number_task=PythonOperator(
    task_id='square_number_task',
    python_callable=square_number,
    
)
  
  
## Set the dependencies

start_task >> add_five_task >> multiply_by_two_task >> subtract_three_task >> square_number_task


```
