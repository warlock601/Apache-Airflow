# Apache-Airflow
### Airflow for MLOps
Airflow is an open-source platform used to programmatically author, schedule and monitor workflows. It allows you to define complex workflows as code and manage their execution. Airflow is commonly used for data pipelines where tasks like ETL are orchestrated across multiple systems. </br>
Airflow can be easily integrated with Amazon Sagemaker, MySQL, Presto, Hive, Spark on k8s, Elasticsearch etc. 
### Use cases
- ELT/ETL: Airflow can be used to define ETL/ELT pipelines as Python code for any data source or destination. We can define dynamic tasks, which serve as placeholders to adapt at runtime based on changing input. Dynamic & Scalable in nature.
- Infrastructure Management: With Airflow you can spin up, manage and tear down your infrastructure at the exact time you need it.
- MLOps: Airflow is used for orchestrating the entire machine learning lifecycle.

### Working
Airflow uses Directed Acyclic Graphs (DAGs) to represent a data pipeline that efficiently executes the tasks. Why DAGs? Directed Acyclic Graph (DAG) comprises directed edges, nodes, and no loop or cycles. Acyclic means there are no circular dependencies in the graph between tasks. Circular dependency creates a problem in task execution. for example, if task-1 depends upon task-2 and task-2 depends upon task-1 then this situation will cause deadlock and leads to logical inconsistency.
<img width="740" height="282" alt="image" src="https://github.com/user-attachments/assets/23c2d48d-781f-430e-84b9-562327a3c51b" />

#### Data Pipeline Execution in Airflow
In Airflow, we can write our DAGs in python and schedule them for execution at regular intervals such as every minute, every hour, every day, every week, and so on. Airflow is comprising four main components:
- Airflow scheduler: It parses the DAGs and schedules the task as per the scheduled time. After scheduling, it submits the task for execution to Airflow workers.
- Airflow workers: It selects the scheduled tasks for execution. Workers are the main engine that is responsible for performing the actual work.
- Airflow webserver: It visualizes the DAGs on the UI web interface and monitors the DAG runs.
- Metadata Database – It is used for storing the pipeline task status.
<img width="731" height="437" alt="image" src="https://github.com/user-attachments/assets/d70ab2c9-b578-4f4b-b606-40ec100d95b2" />

