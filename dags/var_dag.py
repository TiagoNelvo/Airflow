from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.models import Variable


with DAG(
    dag_id="dag_variables",
    schedule_interval=None,
    start_date=datetime(2023,8,20)
):
    @task
    def le_mensagem():
        msg = Variable.get
        print(msg)
        
    @task
    def le_json():
        json = Variable.get("Join_TESTE", deserialize_json=True)
        print(json["campo1"] + " " + json["campo2"])
        
    le_mensagem() >> le_json()    










