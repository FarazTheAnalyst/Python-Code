"""Product Master DAG"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

default_args = {
    "start_date": datetime(2025, 1, 25),
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

def fn_master_dag(ds):
    # Logic for Auditing Purpose
    print(f"Running Master DAG for date: {ds}")

with DAG(
    "etl_master_dag",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
) as dag:
    
    start = PythonOperator(
        task_id="start_audit",
        python_callable=fn_master_dag
    )


    branch_mst_etl = TriggerDagRunOperator(
        task_id="trigger_branch_dag",
        trigger_dag_id="branch_mst_dag",
        execution_date="{{ ds }}",
        reset_dag_run=True,
        wait_for_completion=True,
        poke_interval=3,
    )
    
    channel_mst_etl = TriggerDagRunOperator(
        task_id="trigger_channel_dag",
        trigger_dag_id="channel_mst_dag",
        execution_date="{{ ds }}",
        reset_dag_run=True,
        wait_for_completion=True,
        poke_interval=3,
    )
    
    cust_mst_etl = TriggerDagRunOperator(
        task_id="trigger_customer_dag",
        trigger_dag_id="customer_master_dag",
        execution_date="{{ ds }}",
        reset_dag_run=True,
        wait_for_completion=True,
        poke_interval=3
    )

    acct_mst_etl = TriggerDagRunOperator(
        task_id="trigger_account_dag",
        trigger_dag_id="account_master_dag",
        execution_date="{{ ds }}",
        reset_dag_run=True,
        wait_for_completion=True,
        poke_interval=3
    )

    txn_mst_etl = TriggerDagRunOperator(
        task_id="trigger_transaction_dag",
        trigger_dag_id="transaction_master_dag",
        execution_date="{{ ds }}",
        reset_dag_run=True,
        wait_for_completion=True,
        poke_interval=3
    )

    end = EmptyOperator(task_id="end_process")

# Define task dependencies
start >> [branch_mst_etl, channel_mst_etl] >> cust_mst_etl >> acct_mst_etl >> txn_mst_etl >> end
