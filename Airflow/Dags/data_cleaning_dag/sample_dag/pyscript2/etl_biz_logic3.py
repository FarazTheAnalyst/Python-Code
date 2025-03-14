import pandas as pd
import os
import sys

def etl(a1, p1, p2, ti):
    e_rtn_obj = extract_fn()
    t_rtn_obj = transform_fn(a1, e_rtn_obj)
    l_rtn_obj = load_fn(p1, p2, e_rtn_obj)

sys.path.append(os.path.join(os.path.dirname(__file__), 'pyscript2'))

from init import *

def extract_fn():
    print("logic to Extract Data")
    print("Value of Global Varible Global Variable is: ", GV)
    #rtn_val = "Analytics Training"
    #return rtn_val

    #creating a dataframe object
    details = {
        "cust_id": [1, 2, 3, 4],
        "Name": ["Ali", "Usman", "Abubaker", "Umer"]
    }
    df = pd.DataFrame(details)
    return df

def transform_fn(a1, e_rtn_obj):
    extract_rtn_obj = e_rtn_obj
    print(f"the value of e_rtn_obj object is {extract_rtn_obj}")
    print("the value of a1 is ", a1)
    print("Logic to Transform Data")
    return 10

def load_fn(p1, p2, e_rtn_obj):
    extract_rtn_obj =  e_rtn_obj
    print("type of e_rtn_obj object is {}".format(type(extract_rtn_obj)))
    print("the value of e_rtn_obj object is :")
    print(extract_rtn_obj)
    print("The value of p1 is {}".format(p1))
    print("the value of p2 is {}".format(p1))
