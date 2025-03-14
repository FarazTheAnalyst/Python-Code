""" This ETL is to demonstrate how to run a DAG CONTINUOUSLY"""
from datetime import datetime as dtime
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

def transform_fn():
    """Function Doc String to come here"""
    print("Current Execution Datetime ", dtime.now())
    print("Logic to Transform Data")

# Default arguments for the DAG
def_args = {
    "owner": "airflow", 
    "start_date": dtime(2022, 1, 1)
}

# DAG definition
with DAG(
    dag_id="ETL_Continuous",
    catchup=False,
    schedule_interval=None,
    max_active_runs=1,
    default_args=def_args,
) as dag:
    
    start = EmptyOperator(task_id="START")
    e = EmptyOperator(task_id="EXTRACT")
    t = PythonOperator(task_id="TRANSFORM", python_callable=transform_fn)
    l = EmptyOperator(task_id="LOAD")
    end = EmptyOperator(task_id="END")

    # Task dependencies
start >> e >> t >> l >> end
