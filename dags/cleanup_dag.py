from datetime import datetime
from airflow import DAG, Dataset
from airflow.operators.generic_transfer import GenericTransfer
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
import pandas as pd

AIRFLOW_HOME = "/mnt/c/Users/Tilto/Desktop/Work/Airflow/"

def read_characters():
    pghook = PostgresHook(postgres_conn_id="PG_SWORDBLAST")
    pghook.copy_expert(
        "COPY (SELECT * FROM characters WHERE character_race = 'Fox') TO stdout WITH CSV HEADER",
        AIRFLOW_HOME + '/data/characters.csv'
    )

def transform_data():
    data = pd.read_csv(AIRFLOW_HOME + '/data/characters.csv')
    data['character_level'] = data['character_level'].apply(lambda x: x + 10)
    data.to_csv(AIRFLOW_HOME + '/data/characters_modified.csv')
def cleanup():
    os.remove(AIRFLOW_HOME + '/data/characters.csv')
    os.remove(AIRFLOW_HOME + '/data/characters_modified.csv')

with DAG(
    dag_id='cleanup_dag',
    schedule_interval=None,
    start_date=datetime(2020,1,1)
) as dag:

    task1 = PythonOperator(
        task_id='read_data',
        python_callable=read_characters
    )

    task2 = PythonOperator(
        task_id='transfer_data',
        python_callable=transform_data
    )

    task3 = PythonOperator(
        task_id='cleanup',
        python_callable=cleanup,
        trigger_rule='all_done'
    )

    task1 >> task2 >> task3



