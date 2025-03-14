from datetime import datetime as dtime
from datetime import timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'pyscript2'))

from etl_biz_logic2 import extract_fn, transform_fn, load_fn



# Define default arguments for the DAG
def_args = {
    "owner": "airflow",
    "retries": 0,
    "retry_delay": timedelta(minutes=1),
    "start_date": dtime(2025, 1, 20)
}

# Define the DAG
with DAG(
    dag_id="dag_2_xcom_push_pull", 
    default_args=def_args,
    catchup=False
) as dag:

    # Define tasks
    start = DummyOperator(task_id="START")

    e = PythonOperator(
        task_id="EXTRACT",
        python_callable=extract_fn
    )

    t = PythonOperator(
        task_id="TRANSFORM",
        python_callable=transform_fn,
        op_args=["Learning Data Engineering with airflow"]
    )

    l = PythonOperator(
        task_id="LOAD",
        python_callable=load_fn,
        op_args=["k2", "Analytics"]
    )

    end = DummyOperator(task_id="END")

    # Set task dependencies
    start >> e >> t >> l >> end
