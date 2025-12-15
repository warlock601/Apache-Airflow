# ETL Pipeline Deployemnt in Astronomer-Cloud & AWS
- Create an account in Astro-cloud: https://www.astronomer.io/ & then create a Workspace.
- In order to do the deployment, in the project folder open terminal and do "astro login". It will tell you to Open a browser, open it and perform authentication.
- From the same directory path
  ```bash
  astro deploy
  ```
  And then it will ask to name the deployment and select a Region for the Deployment. Then it will ask which Deployment to update and then it will prepare the setup. After this is done, we'll able to see all the DAGs that we created.
  <img width="1482" height="548" alt="image" src="https://github.com/user-attachments/assets/859c384e-270f-44d1-b323-a8dbf95b290e" />

- Astronomer does not provide any option to create a Database directly so we go to AWS Console and create a DB ourselves. Go to RDS and create a Postgres DB. (For the purpose of this demo, Public Access for the Database has been turned on). </br>
  Open the vpc security-group of the Database, Edit Inbound rules > Add Rule > Type: PostgreSQL, Source: Anywhere (0.0.0.0/0). </br>
  Then go to the database, Select Connectivity & Security and copy the endpoint address and this will be put as Host in Connections in Astro UI.

- In Astronomer.io UI, select DAGs > select "nasa_apod_postgres" > Top right corner "Open Airflow". Apache Airflow UI will open and we'll need to add the connections again now because now we're using AWS. </br>
  Add the connections for postgres (add the RDS postgres database endpoint as Host) and nasa_api (using the API key that we got as email).

- Trigger the DAG. To check whether the data has been added tot he databse or not, check DBeaver. First add a new connection in DBeaver for this RDS database (use the host address as Endpoint of RDS DB).
- New row will be added to the RDS Postgres DB. 
  
