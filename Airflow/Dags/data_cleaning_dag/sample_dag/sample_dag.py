from datetime import datetime as dtime
from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator


def extract_fn():
    print('Logic to Extract Data')

def transform_fn(a1):
    print("The value of a1 is ", a1)
    print("Logic to Transform Data")

def load_fn(p1, p2):
    print("The value of p1 is {}".format(p1))
    print("The value of p2 is {}".format(p2))
    print("Logic to Load Data")

def_args = {
    "owner": "Faraz",
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
    "start_date": dtime(2025, 1, 17)
}

with DAG(
    dag_id="dag_sample",
    default_args=def_args,
    catchup=False
) as dag:
    
    start = DummyOperator(task_id= "START")

    e = PythonOperator(
        task_id="EXTRACT",
        python_callable=extract_fn
    )

    t = PythonOperator(
        task_id="TRANSFORM",
        python_callable=transform_fn,
        op_args=["learning Data Engineering Pipelines with airflow"]
    )

    l = PythonOperator(
        task_id="LOAD",
        python_callable=load_fn,
        op_args=["Faraz", "Gill"]
    )
    
    end = DummyOperator(task_id="END")
    start >> e >> t >> l >> end
