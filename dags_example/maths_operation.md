# Maths Operation

## We'll define a DAG where the tasks are as follows
- Task 1: Start with an initial number (e.g. 10).
- Task 2: Add 5 to the number.
- Task 3: Multiple the result by 2
- Task 4: Subtract 3 from the result.
- Task 5: Compute the square of the result.


**context will be responsible in providing the information or the output from the previous function to the current one because there is a dependency.</br>
To define this context, we'll use a function called xcom_push which is provided by Airflow and this value, the reson we save it in that is that so that we can share those values within the task.
