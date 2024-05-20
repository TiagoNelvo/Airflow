from datetime import datetime
from airflow import DAG, Dataset
from airflow.operators.generic_transfer import GenericTransfer
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator

AIRFLOW_HOME = "/mnt/c/Users/Tilto/Desktop/Work/Airflow/"

def read_data():
    pghook = PostgresHook(postgres_conn_id="PG_SWORDBLAST")
    pghook.copy_expert(
        "COPY (SELECT * FROM characters) TO stdout WITH CSV HEADER",
        AIRFLOW_HOME + "/data/fox_characters.csv",
    )


with DAG(
    dag_id='transfer_dag',
    schedule_interval=None,
    start_date=datetime(2020,1,1)
) as dag:

    task1 = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='PG_SWORDBLAST',
        sql="""
            CREATE TABLE IF NOT EXISTS fox_characters(
                name VARCHAR(50) NOT NULL,
                class VARCHAR(50) NOT NULL,
                level INT NOT NULL
            );
        """
    )

    task2 = GenericTransfer(
        task_id='transfer_tables',
        source_conn_id='PG_SWORDBLAST',
        destination_conn_id='PG_SWORDBLAST',
        destination_table='fox_characters',
        sql="""
            SELECT character_name, character_class, character_level FROM character WHERE characters_race = 'Fox'
        """
    )

    task3 = PythonOperator(
        task_id='read_table',
        python_callable=read_data

    )

    task1 >> task2 >> task3
