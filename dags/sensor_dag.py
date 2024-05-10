import os
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor

AIRFLOW_HOME = "/mnt/c/Users/Tilto/Desktop/Work/Airflow/"

def read_file()
    for path in os.listdir(AIRFLOW_HOME + '/data/'):
        print(path)

with DAG(
    dag_id="sensor_dag",
    schedule_interval=None,
    start_date=datetime(2020, 1, 1)
) as dag:

    sensor = FileSensor(
        task_id='filesensor',
        filepath=AIRFLOW_HOME + '/data/',
        fs_conn_id='FS_CONN',
        poke_interval=5,
        timeout=300
    )

    read_file = PythonOperator(
        task_id='read_file',
        python_callable=read_file,

    )

    sensor >> read_file