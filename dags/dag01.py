from datetime import datetime
from airflow import DAG, Dataset
from airflow.operators.generic_transfer import GenericTransfer
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator

AIRFLOW_HOME = "/mnt/c/Users/Tilto/Desktop/Work/Airflow/"


with DAG(
    dag_id='dataset_dag',
    schedule_interval=None,
    start_date=datetime(2020,1,1)
) as dag:

