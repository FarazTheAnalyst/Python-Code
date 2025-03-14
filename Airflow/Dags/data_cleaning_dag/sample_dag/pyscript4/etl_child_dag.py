"""Sub DAGS"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime



# Shared default arguments
default_args = {
    "start_date": datetime(2025, 1, 25)
}

#######################################################
# Product Master dag

def fn_product_mst_etl():
    print("Product Master DAG execution completed")

with DAG("product_mst_dag",
         schedule_interval=None,
         default_args=default_args,
         catchup=False) as dag1:

    product_etl_start = BashOperator(
        task_id="PRODUCT_MST_ETL_START",
        bash_command="sleep 1"
    )

    product_mst_proc = PythonOperator(
        task_id="PRODUCT_MST_DATA_PROCESS",
        python_callable=fn_product_mst_etl
    )

    # Set dependencies within the DAG
    product_etl_start >> product_mst_proc
#######################################################
# Branch Master Dag

def fn_branch_mst_etl():
    print("Branch Master DAG execution completed")

with DAG("branch_mst_dag",
         schedule_interval=None,
         default_args=default_args,
         catchup=False) as dag2:

    branch_etl_start = BashOperator(
        task_id="BRANCH_MST_ETL_START",
        bash_command="sleep 1"
    )

    branch_mst_proc = PythonOperator(
        task_id="BRANCH_MST_DATA_PROCESS",
        python_callable=fn_branch_mst_etl
    )

    # Set dependencies within the DAG
    branch_etl_start >> branch_mst_proc
########################################################

# Channel Master DAG
def fn_channel_mst_etl():
    print("Channel Master DAG execution completed")

with DAG("channel_mst_dag",
         schedule_interval=None,
         default_args=default_args,
         catchup=False) as dag3:
    
    channel_etl_start = BashOperator(
        task_id="CHANNEL_MST_ETL_START",
        bash_command="sleep 1"
    )

    channel_mst_proc = PythonOperator(
        task_id="CHANNEL_MST_DATA_PROCESS",
        python_callable=fn_channel_mst_etl
    )

    # Set dependencies within the DAG
    channel_etl_start >> channel_mst_proc
    

########################################################

# Customer Master DAG
def fn_customer_mst_etl():
    print("customer Master DAG execution completed")

with DAG("customer_master_dag",
         schedule_interval=None,
         default_args=default_args,
         catchup=False) as dag4:
    
    customer_etl_start = BashOperator(
        task_id="CUSTOMER_MST_ETL_START",
        bash_command="sleep 1"
    )

    cust_mst_proc = PythonOperator(
        task_id="CUSTOMER_MST_DATA_PROCESS",
        python_callable=fn_customer_mst_etl
    )

    # Set dependencies within the DAG
    customer_etl_start >> cust_mst_proc
   
########################################################

# Account Master DAG
def fn_account_mst_etl():
    print("Account Master DAG execution completed")

with DAG("account_master_dag",
         schedule_interval=None,
         default_args=default_args,
         catchup=False) as dag5:
    
    account_etl_start = BashOperator(
        task_id="ACCOUNT_MST_ETL_START",
        bash_command="sleep 1"
    )

    acct_mst_proc = PythonOperator(
        task_id="ACCOUNT_MST_DATA_PROCESS",
        python_callable=fn_account_mst_etl
    )

    # Set dependencies within the DAG
    account_etl_start >> acct_mst_proc
   
########################################################

# Transaction Master DAG
def fn_transaction_mst_etl():
    print("Transaction Master DAG execution completed")

with DAG("transaction_master_dag",
         schedule_interval=None,
         default_args=default_args,
         catchup=False) as dag8:
    
    transaction_etl_start = BashOperator(
        task_id="TRANSACTION_MST_ETL_START",
        bash_command="sleep 1"
    )

    txn_mst_proc = PythonOperator(
        task_id="TRANSACTION_MST_DATA_PROCESS",
        python_callable=fn_transaction_mst_etl
    )

    # Set dependencies within the DAG
    transaction_etl_start >> txn_mst_proc