import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

#AIRFLOW_HOME = "C/Users/Tilto/Desktop/Work/Airflow/"
data = "/mnt/c/Users/Tilto/Desktop/Work/Airflow/"
#AIRFLOW_HOME = $(pwd)


def gera_arquivo():
    with open(data + "/data/arquivo.txt", "w") as f:
        for i in range(100):
            f.write("Arquivo text linha {}\n".format(i))


def processa_arquivo():
    arquivo = ""
    with open(data + "/data/arquivo.txt", "r") as f:
        for line in f:
            arquivo += line.strip("\n") + " - Processado\n"

    with open(data + "/data/arquivo_processado.txt", "w") as f:
        f.write(arquivo)


with DAG(
    dag_id="dag_exemplo",
    schedule_interval=None,
    start_date=datetime(2020, 1, 1)
) as dag:

    gera_arquivo = PythonOperator(task_id="gera_arquivo", python_callable=gera_arquivo)

    processa_arquivo = PythonOperator(
        task_id="processa_arquivo", python_callable=processa_arquivo
    )

    gera_arquivo >> processa_arquivo
