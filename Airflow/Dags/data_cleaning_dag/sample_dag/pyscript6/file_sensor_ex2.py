import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator

## custom function to get the file name - txn_data_yyyymmdd.csv (Daily check for new file)
# Function to generate the file name on execution_date
def get_filename(exec_date, **kwargs):
    if exec_date:
        print(f"Date Passed - {exec_date}")
        # Ensure that "exec_date" is a datetime object. if it's a string, convert it to datetime.
        if isinstance(exec_date, str):
            # Adjust the format to handle timezone as well
            exec_date = datetime.strptime(exec_date, "%Y-%m-%d")

        # Now generate the filename using the datetime object txn_data_yyyymmdd.csv
        filename = f"txn_data_{exec_date.strftime('%Y%m%d')}.csv"
    else:
        # default to today's date if no date is passed
        filename = f"txn_data_{datetime.now().strftime('%Y%m%d')}.csv"
        print("No Date found, so passing default date")

    # Push the filename to Xcom for later use in the FileSensor task
    print(f"Final file name from function - {filename}")
    ti = kwargs["ti"]
    ti.xcom_push(key="filename", value=filename)

# Define the Python function for processing the file
def process_file(filename, **kwargs):
    print(f"Current Working Directory {os.getcwd()}")
    print(f"Processing file: {filename}")
    # add your file processing logic here (e.g., read data, transform, etc.)

# Default arguments for the DAG
default_args = {
    "owner": "airflow",
    "retries": 3,
    "retry_delay": timedelta(minutes=5)
}

# Define the DAG
with DAG(
    dag_id="Dag_file_sensor_ex2",
    default_args=default_args,
    description="A sample DAG using FileSensor",
    schedule_interval="@daily",
    start_date=datetime(2025, 1, 22),
    catchup=False
) as dag:
    
    # Task 1: Generate the filename based on execution_date
    generate_filename = PythonOperator(
        task_id="generate_filename",
        python_callable=get_filename,  # Correct reference to function
        op_args=["{{ ds }}"],  # {{ ds }} is a Jinja template variable representing a date object
        provide_context=True   # Ensure context variables (like execution_date) are available
    )

    # Task 2: wait for the file to appear
    wait_for_file = FileSensor(
        task_id="wait_for_file",
        filepath="{{ task_instance.xcom_pull(task_ids='generate_filename', key='filename') }}",
        poke_interval=10,  # Check every 10 seconds
        timeout=600,     # Timeout after 10 minutes
        mode="poke",
        fs_conn_id="fs_default"  # need absolute file path, this is custom connection id with no path
    )
    
    # Task 3: Process the file
    process_file_task = PythonOperator(
        task_id="process_file",
        python_callable=process_file,  # Correct reference to function
        op_kwargs={"filename": "{{ task_instance.xcom_pull(task_ids='generate_filename', key='filename') }}"}
    )

    # Define task dependencies
    generate_filename >> wait_for_file >> process_file_task
