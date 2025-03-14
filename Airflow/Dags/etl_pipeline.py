from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
from datetime import datetime


# define the DAG
default_args = {
    "owner":"airflow",
    "start_date":datetime(2025, 1, 28),
    "retries":1
}

dag = DAG(
    "dag_etl_pipeline",
    default_args=default_args,
    description="A simpel ETL pipeline for CSV dataset",
    schedule_interval=None
)

# Step 1: Extract - Read the CSV file
def extract():
    data = pd.read_csv("/opt/airflow/dags/input_data.csv")
    return data.to_dict()

# Step 2: Transform - Perform any data cleaning of transformation
def transform(**kwargs):
    ti = kwargs["ti"]
    data_dict = ti.xcom_pull(task_ids="extract")  #Get extracted data
    df = pd.DataFrame.from_dict(data_dict)  #Convert back to DataFrame
    df["age"].fillna(0, inplace=True)
    return df.to_dict()  # Convert again for Xcom


# Step 3: Load - Save the transformed data to a new CSV file
def load(**kwargs):
    ti = kwargs["ti"]
    transformed_data = ti.xcom_pull(task_ids="transform")
    df = pd.DataFrame.from_dict(transformed_data)
    df.to_csv("/opt/airflow/dags/output_data.csv", index=False) 


# Define the tasks in the DAG
extract_task = PythonOperator(
    task_id="extract",
    python_callable=extract,
    provide_context=True,    #Allows passing kwargs
    dag=dag
)

transform_task = PythonOperator(
    task_id="transform",
    python_callable=transform,
    provide_context=True,
    dag=dag
)

load_task = PythonOperator(
    task_id="load",
    python_callable=load,
    provide_context=True,
    dag=dag
)

# Set task dependencies
extract_task >> transform_task >> load_task
