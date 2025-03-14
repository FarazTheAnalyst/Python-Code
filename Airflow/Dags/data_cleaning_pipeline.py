from datetime import timedelta

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

def clean_data():
    '''
    This function reads raw data from a CSV file, cleans the data, and writes the cleaned data to a new CSV file.
    The cleaning process involes removing rows with missing values and removing duplicate rows based on "name", "age", and "salary" columns. The first occurence of the duplicate is kept.
    The function does not take the any arguments  and does not return any values. It operates solely through side effects
    (reading a file, cleaning the data, and writing to a file).'''

    # Read the raw data from CSV file\
    df = pd.read_csv(r"/opt/airflow/dags/raw_data_sample.csv")

    # Remove rows with missing values
    df_cleaned = df.dropna()

    # Remove duplicate rows based on "name", "age", and "salary" columns
    # The first occurence of the duplicate is kept
    df_cleaned = df_cleaned.drop_duplicates(subset=["name", "age", "salary"], keep="first")
    
    # Write the cleaned data to a new CSV file
    # The "index" parameter is set to False so that row indices are not saved
    df_cleaned.to_csv(r"/opt/airflow/dags/clean_data_sample.csv", index=False)

def analyze_data():
    '''
    This function reads the cleaned data from CSV file, perfomrs a statistical analysis on the data,
    and writes the summary statistics to a new CSV file.
    
    The function  does not take any arguments and does not return any values. It operates solely through
    side effects (reading a file, performing an analysis, and writing to a file).
    '''

    # Read the cleaned data from the CSV file
    df_cleaned = pd.read_csv(r"/opt/airflow/dags/clean_data_sample.csv")
    
    # Perform a statistical analysis on the data
    # The "describe" function returns the summary statistics  including count, mean, min, 25%, 50%, 75%, max
    summary_statistics = df_cleaned.describe()

    # Write the new summary statistics to a new CSV file
    # The "index" parameter is set to True so that the index (statistical measures) are saved
    summary_statistics.to_csv(r"/opt/airflow/dags/analysis_sample.csv", index=True)

# Define the default arguments for the DAG
default_args = {
    "owner": "Faraz Gill", # Owner of the DAG
    "depends_on_past": False, # The DAG does not have dependencies on past runs
    "start_date": days_ago(1), # The DAG started one day ago
    "email": ["farazgill12@icloud.com"], # Email to send notifications to 
    "email_on_failure": False, # Do not send email on task failure
    "email_on_retry": False, # Do not send email on task retry
    "retries": 1, # Number of retries if a task fails
    "retry_delay": timedelta(minutes=5), #Delay between retries 
}

#define the DAG
dag = DAG(
    "data_cleaning_pipeline", # Name of the DAG
    default_args=default_args, # Default arguments of the DAG
    description="A simple data cleaning and analysis pipeline", # Description of the DAG
    schedule_interval=timedelta(days=1), # Schedule the DAG to run once a day
)

# Define the "clean_data" task
clean_data_task = PythonOperator(
    task_id="clean_data", # ID of the task
    python_callable=clean_data, # Function to execute
    provide_context=True, # Provide Airflow context to the function
    dag=dag, # DAG the task belongs to
)

# Define the "analyze_data" task
analyze_data_task = PythonOperator(
    task_id = "analyze_data", # ID of the task
    python_callable=analyze_data, # Function to execute
    provide_context=True, # Provide Airflow context to the function
    dag=dag, # DAG the task belongs to 
)

# Define the order of tasks in the DAG
clean_data_task >> analyze_data_task  # "analyze_data" depends on "clean_data"