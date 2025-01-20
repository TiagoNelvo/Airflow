



AIRFLOW_HOME = "/mnt/c/Users/Tilto/Desktop/Work/Airflow/"

def test_file_exists():
    assert os.path.exist(f'{AIRFLOW_HOME}/data/arquivo.csv')

def test_read():
    df = le_arquivo()
    assert df.shape(5,5)
    
def test_masking():
    df = le_arquivo()
    df = mascara_senha(df)
    assert df[2][2] == '********'

def test_task(test_dag):
    
    def _task_defion():
        df = le_arquivo()
        df = mascara_senha(df)
        salva_arquivo(df)
        
    task = PythonOperator(
        task_id='mascara_senha',
        python_callable=_task_defion(),
        dag=test_dag
    )

    pytest.helpers.run_task(task, test_dag)

    assert os.path.exists(f'{AIRFLOW_HOME}/data/arquivo_final.csv')





