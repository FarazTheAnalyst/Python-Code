from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import os
from datetime import datetime
import logging
from airflow.utils.dates import days_ago
from datetime import timedelta



LOCAL_FILE_PATH = r"/opt/airflow/dags/yellow_tripdata_2019-01.csv/yellow_tripdata_2019-01.csv"
CLEANED_FILE_PATH = r"/opt/airflow/dags/cleaned_tripdata_2029-01.csv"

def transform_data():
    df = pd.read_csv(LOCAL_FILE_PATH)
    df.head()

    #Remove rows with missing  values
    df = df.dropna()
    df = df[(df["passenger_count"] > 0) & (df["trip_distance"] > 0)]
    df = df[(df["fare_amount"] > 2.5) & (df["fare_amount"] < 500)]
    df = df[(df["trip_distance"] < 100)]

    # Remove duplicates
    df = df.drop_duplicates()

    # Handle negative values in trip_distance and passenger_count
    df = df[df["trip_distance"] >=0]
    df = df[df["passenger_count"] > 0]

    # Ensure valid datetime formats
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"], errors="coerce")
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"], errors="coerce")

    # Drop rows with invalid datetimes (coersing errors results in NaT)
    df = df.dropna(subset=["tpep_pickup_datetime", "tpep_dropoff_datetime"])

    # Create a new features: trip_duration (in minutes)
    df["trip_duration"] = (df["tpep_pickup_datetime"] - df["tpep_dropoff_datetime"]).dt.total_seconds()/60
    df = df[df["trip_duration"] > 0]

    # Normalize  column names (convert to lowercase and replace spaces with underscores)
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # Convert categorical column to string
    categorical_cols = ["vendorid", "store_and_fwd_flag", "ratecodeid", "payment_type"]
    for col in categorical_cols:
        df[col] = df[col].astype(str)

    # Save the cleaned data to a new CSV file
    df.to_csv(CLEANED_FILE_PATH, index=False)

    # Log the first 5 rows of the DataFrame for inspection
    logging.info("Data after initial transformation")
    logging.info(df.head())

def load_data():
    # Read the cleaned CSV file
    df = pd.read_csv(CLEANED_FILE_PATH)
    # optionally, you can save or process the data further here
    df.to_csv(CLEANED_FILE_PATH, index=False) # Overwrite with cleaned data for demonstration

# Define Airflow
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "execution_timeout": timedelta(minutes=30)
}

dag = DAG(
    "dag_etl_nyc_taxi",
    default_args=default_args,
    schedule_interval="@daily", 
    catchup=False
)

# As the file is already downloaded we don't need any extraction step.
transform_task = PythonOperator(
    task_id="transform_data",
    python_callable=transform_data,
    dag=dag
)


load_task = PythonOperator(
    task_id = "load_data",
    python_callable=load_data,
    dag=dag
)

transform_task >> load_task