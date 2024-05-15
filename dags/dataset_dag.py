from datetime import datetime
from airflow import DAG, Dataset
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


AIRFLOW_HOME = "/mnt/c/Users/Tilto/Desktop/Work/Airflow/"

CHARACTERS = Dataset('file://' + AIRFLOW_HOME + '/data/characters.csv')

def read_characters():
    pghook = PostgresHook(postgres_conn_id="PG_SWORDBLAST")
    pghook.copy_expert(
        "COPY (SELECT * FROM characters WHERE character_race = 'Fox') TO stdout WITH CSV HEADER",
        AIRFLOW_HOME + '/data/characters.csv'
    )

with DAG(
    dag_id='dataset_dag',
    schedule_interval=None,
    start_date=datetime(2020,1,1)
) as dag:

    task1 = PythonOperator(
        task_id='read_characters',
        python_callable=read_characters,
        outlets=[CHARACTERS]
    )

    task1