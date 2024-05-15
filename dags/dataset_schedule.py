from datetime import datetime
from airflow import DAG, Dataset
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

AIRFLOW_HOME = "/mnt/c/Users/Tilto/Desktop/Work/Airflow/"

CHARACTERS = Dataset('file://' + AIRFLOW_HOME + '/data/characters.csv')

def read_character():
    df = pd.read_csv(AIRFLOW_HOME + '/data/characters.csv')

with DAG(
    dag_id='dataset_dag',
    schedule=[CHARACTERS],
    start_date=datetime(2020,1,1)
) as dag:

    task = PythonOperator(
        task_id='read_character',
        python_callable=read_character
    )

    task