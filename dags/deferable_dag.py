from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.time_sensor import TimeSensorAsync

AIRFLOW_HOME = "/mnt/c/Users/Tilto/Desktop/Work/Airflow/"

def task()
    print('Ola')

with DAG(
    dag_id="dag_deferable",
    schedule_interval=None,
    start_date=datetime(2020, 1, 1)
) as dag:

    sensor = TimeSensorAsync(
        task_id='sensor',
        target_time=datetime(2024,5,8, 18,15).time()
    )

    task1 = PythonOperator(
        task_id='task1',
        python_callable=task,

    )

    sensor >> task1