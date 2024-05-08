from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd
from airflow.providers.postgres.operators.postgres import PostgresOperator

data = "/mnt/c/Users/Tilto/Desktop/Work/Airflow/"

def read_players():
    pghook = PostgresHook(postgres_conn_id="PG_SWORDBLAST")
    pghook.copy_expert(
        "COPY (SELECT * FROM players) TO stdout WITH CSV HEADER",
        data + "/data/players.csv"
    )

def read_currency():
    pghook = PostgresHook(postgres_conn_id="PG_SWORDBLAST")
    pghook.copy_expert(
        "COPY (SELECT * FROM currency) TO stdout WITH CSV HEADER",
        data + "/data/currency_modified.csv"
    )

def read_currency_modified():
    pghook = PostgresHook(postgres_conn_id="PG_SWORDBLAST")
    pghook.copy_expert(
        "COPY (SELECT * FROM currency) TO stdout WITH CSV HEADER",
        data + "/data/currency.csv"
    )

def read_player_ids(ti):
    df = pd.read_csv(data + '/data/players.csv')
    list_ids = df['player_id'].tolist()
    ids = str(list_ids).replace('[','(',).replace(']',')')
    ti.xcom_push(key='player_ids',value=ids)



with DAG(
    dag_id="xcom_dag",
    schedule_interval=None,
    start_date=datetime(2020,1,1)
) as dag:

    task1 = PythonOperator(
        task_id='read_players',
        python_callable=read_players
    )

    task2 = PythonOperator(
        task_id='read_currency',
        python_callable=read_currency
    )

    task3 = PythonOperator(
        task_id='read_playerid',
        python_callable=read_player_ids
    )

    task5 = PythonOperator(
        task_id='read_currency_modified',
        python_callable=read_currency_modified
    )

    task4 = PostgresOperator(
        task_id='update_currency',
        postgres_conn_id='PG_SWORDBLAST',
        sql='UPDATE currency SET currency_amount = currency_amount + 500 WHERE player_id in'
            "{{task_instance.xcom_pull(task_ids='read_playerid', key='player_ids')}}"
    )

    task1 >> task2 >> task3 >> task4 >> task5