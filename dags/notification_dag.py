from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def task1():
    print('task1')

def sucess_callback():
    print('sucesso')

def fail_callback():
    print('failure')

with DAG(
    dag_id='notification_dag',
    schedule_interval='@once',
    default_args={
        'email':'teste@teste.com',
        'email_on_sucess': True,
        'email_on_failure': True,
        'email_on_retry': True
    },
    start_date=datetime(2020,1,1)
    on_sucess_callback=sucess_callback,
    on_failure_callback=failure_callback
) as dag:

    task1= PythonOperator(
        task_id='task1',
        python_callable=task1
    )

    task1