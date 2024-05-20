from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


AIRFLOW_HOME = "/mnt/c/Users/Tilto/Desktop/Work/Airflow/"

def read_data():
    pghook = PostgresHook(postgres_conn_id="PG_SWORDBLAST")
    pghook.copy_expert(
        "COPY (SELECT * FROM characters) TO stdout WITH CSV HEADER",
        AIRFLOW_HOME + "/data/characters.csv",
    )

def copy_data():
    lines = ''
    with open(data + "/characters.csv", "r") as f:
        for line in f:
            lines += line.replace(",", "-")
    with open(data + "/characters_new.csv", "w") as f:
        f.write(lines)



with DAG(
    dag_id="Hook_dag", schedule_interval=None, start_date=datetime(2020, 1, 1)
) as dag:

    task1 = PythonOperator(task_id="task1", python_callable=read_data)

    task2 = PythonOperator(task_id="task2", python_callable=copy_data)

    task1 >> task2
