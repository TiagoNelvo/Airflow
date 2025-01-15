from datetime import datetime
from airflow import DAG
from airflow.decorators import task
from mask_csv_operator import MaskCSVOperator



AIRFLOW_HOME = "/mnt/c/Users/Tilto/Desktop/Work/Airflow/"


with DAG(
    dag_id="dag_custom_op",
    schedule_interval=None,
    start_date=datetime(2023, 8, 20)
):
    
    @task
    def gera_arquivo_csv():
        with open(AIRFLOW_HOME + '/data/arquivo.csv', "w") as f:
            f.write('John Smith,john.smith,hard@password1234,20,true\n')
            f.write('Maria Fox,maria.fox,1234,10,false\n')
            f.write('Jason Matt,jason.matt,password, 125,true\n')
            f.write('William Richards,wiliam.richards,password1234,10000,false\n')
            f.write('Rose Williams,rose.williams,!Rsailkds2389012,156,true\n')
            
    mask_file = MaskCSVOperator(
        task_id='mask_file',
        input_file=AIRFLOW_HOME + '/data/arquivo.csv',
        output_file=AIRFLOW_HOME + '/data/arquivo_mask.csv',
        separator=',',
        column=2
    )
    
    gera_arquivo_csv() >> mask_file




