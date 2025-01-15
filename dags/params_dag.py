from datetime import datetime
from airflow import DAG
from airflow.decorators import task
from airflow.models import Param

AIRFLOW_HOME = "/mnt/c/Users/Tilto/Desktop/Work/Airflow/"

with DAG(
    dag_id="dag_params",
    schedule_interval=None,
    start_date=datetime(2023,8,20),
    params={
        'number_of_runs': 10,
        'added_value': Param(100, minimum=100, maximum=1000)
    }
):
    
    @task
    def task1(**context):
        added_value = context['params']['added_value']
        value = 0
        for i in range(context['params']['number_of_runs']):
            print(f'{i} - {value}')
            value += added_value            
            
    task()









