import ...


with DAG(
    dag_id='inference_model',
    schedule_interval=None,
    start_date=datetime(2023,9,6)
) as dag:
    @task
    def load_data():
        hook = S3Hook(aws_conn_id='AWS-SANDBOX')
        hook.download_file(
            key='ml/input/test.csv',
            bucket_name='geekfox-sb-descomplica',
            local_path='data/ml/input',
            preserve_file_name=True,
            use_aotogenerated_subdir=False
        )
            
    @task
    def load_model():
        hook = S3Hook(aws_conn_id='AWS-SANDBOX')
        hook.download_file(
            key='ml/output/model.csv',
            bucket_name='geekfox-sb-descomplica',
            local_path='data/ml/output',
            preserve_file_name=True,
            use_aotogenerated_subdir=False
        )
        
    @task
    def inference_model():
        test_data = load_test_data('data/ml/input/test.csv')
        model = load_model('data/ml/output/model.pkl')
        predict(model, test_data,'data/ml/output')
    
    save_prediction = LocalFilesystemToS3Operator(
        aws_conn_id='AW-SANDBOX',
        task_id='save_prediction',
        filename='data/ml/output/predictions.csv',
        dest_key='ml/output/predictions.csv',
        dest_bucket='geekfox-sb-descomplica',
        replace=True
    )
    
    @task(trigger_rule='all_done')
    def cleanup():
        shutil.rmtree('data/ml', ignore_errors=True)
    
    load_data() >> load_model() >> inference_model() >> save_prediction() >> cleanup()
    
    
    
    