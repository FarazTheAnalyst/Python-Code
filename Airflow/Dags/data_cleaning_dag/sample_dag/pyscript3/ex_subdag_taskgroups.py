from datetime import datetime
from datetime import timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime

from airflow.utils.task_group import TaskGroup

with DAG ("dag_ex_task_groups", default_args={
    "owner": "airflow", "start_date": datetime(2022, 1, 1)
}) as dag:
    
    start = DummyOperator(task_id = "Start")
    # a = DummyOperator(task_id = "Task_A")
    # a1 = DummyOperator(task_id = "Task_A1")
    # b = DummyOperator(task_id = "Task_b")
    # c = DummyOperator(task_id = "Task_c")
    # d = DummyOperator(task_id = "Task_d")
    # e = DummyOperator(task_id = "Task_e")
    # f = DummyOperator(task_id = "Task_f")
    # g = DummyOperator(task_id = "Task_g")
    end = DummyOperator(task_id = "END")

#start >> a >> a1 >> b >> c >> d >> e >> f >> g >> end

    # # [SIMPLE SEQUENTIAL TASK GROUP]
    with TaskGroup("A-A1", tooltip="Task Group for A & A1") as gr_1:

        a = DummyOperator(task_id="Task_A")
        a1 = DummyOperator(task_id="Task_1")
        b = DummyOperator(task_id = "Task_b")
        c = DummyOperator(task_id = "Task_c")

        a >> a1
    # # [End of SIMPLE SEQUENTIAL TASK GROUP]

# start >> gr_1 >> d >> e >> f >> g >> end


#   #[Nested Task Group]
    with TaskGroup("D-E-F", tooltip="Nested Task Group") as gr_2:
        d = DummyOperator(task_id = "Task_D")

        with TaskGroup("E-F-G", tooltip="Inner Nested Task Group") as sgr_2:
            e = DummyOperator(task_id = "Task_E")
            f = DummyOperator(task_id = "Task_f")
            g = DummyOperator(task_id = "Task_G")
            e >> f
            e >> g

#   #[End of Nested TASK GROUP]
start >> gr_1 >> gr_2 >> end



