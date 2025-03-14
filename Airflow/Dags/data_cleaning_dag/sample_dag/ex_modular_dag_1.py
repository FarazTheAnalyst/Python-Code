from datetime import datetime as dtime
from datetime import timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator

import pandas as pd
import sys
import os

# Uncomment the path changes if needed
# root_folder_path = r"D:\AIRFLOW-DOCKER\dags\data_cleaning_dag\sample_dag\pyscript2"
# os.chdir(root_folder_path)



# Add the pyscript2 directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'pyscript2'))

# Now you should be able to import the modules
from init import GV
from etl_biz_logic import extract_fn, transform_fn, load_fn

def_args = {
    "owner": "Faraz",
    "retries": 0,
    "retry_delay": timedelta(minutes=1),
    "start_date": dtime(2025, 1, 21)
}

with DAG(
    dag_id="dag_1_ex_modular_",
         default_args=def_args,
         catchup=False
         ) as dag:
    start = DummyOperator(task_id="START")
    
    e = PythonOperator(
        task_id="EXTRACT", 
        python_callable=extract_fn
    )
    
    t = PythonOperator(
        task_id="TRANSFORM", 
        python_callable=transform_fn,
        op_args=["Faraz Gill Learning Airflow pipelines"],  # Provide the correct arguments as a list
        do_xcom_push=True  # Ensure this is set if you want to push the return value to XCom
    )

    l = PythonOperator(
        task_id="LOAD", 
        python_callable=load_fn,
        op_args=["k2", "Analytics"]  # Correct the arguments here
    )
    
    end = DummyOperator(task_id="END")

# Define task dependencies
start >> e >> t >> l >> end
