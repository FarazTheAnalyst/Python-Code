from datetime import datetime, timedelta
from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator
import os

PATH = r"/opt/airflow/dags/data_cleaning_dag/input_data"  

def debug_file_path(path):
    print(f"Checking directory: {path}")
    print(f"Directory exists: {os.path.exists(path)}")
    print(f"Files in directory: {os.listdir(path) if os.path.exists(path) else 'N/A'}")

# Default arguments for the DAG
default_dag = {
    "owner": "airflow", 
    "retries": 3,
    "retry_delay": timedelta(minutes=5)
}

# Define the DAG
with DAG(
    dag_id="dag_file_sensor_ex1",
    default_args=default_dag,
    description="A sample DAG using FileSensor",
    schedule_interval=None,
    start_date=datetime(2025, 1, 1),
    catchup=False
) as dag:

    # Debug Task: Check directory and file existence
    debug_task = PythonOperator(
        task_id="debug_file_path",
        python_callable=debug_file_path,
        op_kwargs={"path": PATH}
    )

    # Wait for the file to appear
    wait_for_file = FileSensor(
        task_id="wait_for_file",
        filepath=os.path.join(PATH, "*.csv"),
        poke_interval=10,
        mode="reschedule",
        timeout=120  # Extended timeout for testing
    )

    # Task to process the file
    process_file_task = PythonOperator(
        task_id="process_file",
        python_callable=lambda: print("Processing file..."),
    )

    debug_task >> wait_for_file >> process_file_task
