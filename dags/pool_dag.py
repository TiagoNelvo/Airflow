from datetime import datetime
from airflow import DAG
from airflow.decorators import task

AIRFLOW_HOME = "/mnt/c/Users/Tilto/Desktop/Work/Airflow/"

with DAG(
    dag_id="pools_dag",
    schedule_interval=None,
    start_date=datetime(2023,8,20)
):
    
    @task
    def task_default_pool():
        print('task_default_pool')
        
    @task(pool='pool_teste1')
    def task_pool():
        print('task_pool')
        
    @task(pool='pool_teste2')
    def task_pool2():
        print('task_pool2')
        
    @task(pool='pool_teste1')
    def task_pool1_2():
        print('task_pool1_2')
        
    @task(pool='pool_teste2')
    def task_pool2_2():
        print('task_pool2_2')    
    
    task_default_pool() >> [task_pool1(),task_pool1_2()] >> task_default_pool() >> [task_pool2(),task_pool2_2()]
    
