from datetime import datetime as dtime
from datetime import timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'pyscript2'))

from init import *
from etl_biz_logic3 import extract_fn, transform_fn, load_fn, etl



# Define default arguments for the DAG
def_args = {
    "owner": "airflow",
    "retries": 0,
    "retry_delay": timedelta(minutes=1),
    "start_date": dtime(2025, 1, 20)
}

# Define the DAG
with DAG(
    dag_id="dag_ex_etl", 
    default_args=def_args,
    catchup=False
) as dag:

    # Define tasks
    start = DummyOperator(task_id="START")

    e_t_l = PythonOperator(task_id = "EXTRACT_TRANSFORM_LOAD", python_callable = etl,
                           op_args=["Faraz Gill learning Airflow", "K2", "Analytics"])

    end = DummyOperator(task_id = "END")

start >> e_t_l >> end