from datetime import datetime as dtime
from datetime import timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator

import pandas as pd

# All Constants declared as Global Variable
GV = "Faraz Gill Learning Airflow"

def extract_fn():
    print("Logic To Extract Data")
    print("Value of Global Variable is: ", GV)
    #rtn_val = "Faraz Making Data Pipelines"
    #return rtn_val

    # creating a dataframe object
    details = {
        "cust_id" : [1, 2, 3, 4],
        "Name" : ["Rajesh", "Jakhotia", "K2", "Analytics"]
    }

    df = pd.DataFrame(details)
    return df

def transform_fn(a1, ti):
    xcom_pull_obj = ti.xcom_pull(task_ids=["EXTRACT"])
    print(f"type of xcom pull object is {type(xcom_pull_obj)}")
    extract_rtn_obj = xcom_pull_obj[0]
    print(f"the value of xcom pull object is {extract_rtn_obj}")
    print(f"The value of a1 is {a1}")
    print("Logic to Transform Data")
    return 10

def load_fn(p1, p2, ti):
    xcom_pull_obj = ti.xcom_pull(task_ids=["EXTRACT"])
    print(f"type of xcom pull object is {type(xcom_pull_obj)}")
    extract_rtn_obj = xcom_pull_obj[0]
    print("the value of xcom pull object is {}".format(extract_rtn_obj))
    print(f"The value of p1 is {p1}")
    print(f"The value of p2 is {p2}")
    print("Logic to Load Data")

# Define default arguments for the DAG
def_args = {
    "owner": "airflow",
    "retries": 0,
    "retry_delay": timedelta(minutes=1),
    "start_date": dtime(2025, 1, 20)
}

# Define the DAG
with DAG(
    dag_id="dag_xcom_push_pull", 
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
