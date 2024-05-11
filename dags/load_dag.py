from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

AIRFLOW_HOME = "/mnt/c/Users/Tilto/Desktop/Work/Airflow/"

def read_fs():
    with open(AIRFLOW_HOME + '/data/data.txt', r) as f:
        for line in f.readlines():
            data = line.split(',')
            print(data)

def read_pandas():
    df = pd.read_csv(AIRFLOW_HOME + '/data/data.csv')
    print(df.head())

def read_psql():
    pghook = PostgresHook(postgres_conn_id="PG_SWORDBLAST")
    pghook.copy_expert(
        "COPY (SELECT * FROM players) TO stdout WITH CSV HEADER",
        data + "/players.csv",
    )


with DAG(
    dag_id="load_dag",
    schedule_interval=None, 
    start_date=datetime(2020, 1, 1)
) as dag:

    task1 = PythonOperator(
        task_id='task1',
        python_callable=read_fs
    )

    task2 = PythonOperator(
        task_id='task2',
        python_callable=read_pandas()
    )

    task3 = PythonOperator(
        task_id='task3',
        python_callable=read_psql()
    )

    task1 >> task2 >> task3

