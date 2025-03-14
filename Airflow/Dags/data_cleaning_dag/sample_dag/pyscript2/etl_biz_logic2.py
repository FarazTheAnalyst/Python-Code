import pandas as pd
from datetime import timedelta
from datetime import datetime as dtime
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "pyscript2"))

from init import GV


def extract_fn():
    print("Logic To Extract Data")
    print("Value of Global Variable is: ", GV)
    rtn_val = "Faraz Making Data Pipelines"
    return rtn_val

    # creating a dataframe object
    #details = {
    #    "cust_id" : [1, 2, 3, 4],
     #   "Name" : ["Rajesh", "Jakhotia", "K2", "Analytics"]
    #}

    #df = pd.DataFrame(details)
    #return df

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