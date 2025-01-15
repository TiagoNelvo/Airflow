import pandas as pd
from airflow import DAG
from airflow.decorators import task
from airflow.models import Param
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from pandas import DataFrame


with DAG(
    dag_id="pipeline_etl_dag",
    schedule_interval=None,
    start_date=datetime(2023,8,20),
)as dag:
    
    @task
    def load_products_metadata():
        hook = S3Hook(asw_conn_id='AWS-SANDBOX')
        hook.download_file(
            key='data/json/products.json',
            bucket_name='geekfox-sb-descomplica',
            local_path='data/etl/json/',
            preserve_file_name=True
            use_autogenerated_subdir=False
        )
        
    
    @task
    def load_salesperson_metadata():
        hook = S3Hook(asw_conn_id='AWS-SANDBOX')
        hook.download_file(
            key='data/json/salesperson.json',
            bucket_name='geekfox-sb-descomplica',
            local_path='data/etl/json/',
            preserve_file_name=True
            use_autogenerated_subdir=False
        )
        
        
    @task
    def load_stores_metadata():
        hook = S3Hook(asw_conn_id='AWS-SANDBOX')
        hook.download_file(
            key='data/json/stores.json',
            bucket_name='geekfox-sb-descomplica',
            local_path='data/etl/json/',
            preserve_file_name=True
            use_autogenerated_subdir=False
        )
        
    @task
    def load_csv_s3(**context):
        hook = S3Hook(aws_conn_id='AWS-SANDBOX')
        for data in pd.date_range(context['params']['start-data'],context['params']['start-data']):
            hook.download_file(
                key=f'data/csv/data_{date.strftime("%Y-%m-%d")}.csv',
                bucket_name='geekfox-sb-descomplica',
                local_path='data/etl/csv/',
                preserve_file_name=True,
                use_autogenerated_subdir=False
        )
    
    @task
    def merge_csv(**context):
        df = DataFrame()
        
      
    @task
    def load_csv_s3(**context):
        hook = S3Hook(aws_conn_id='AWS-SANDBOX')
        for data in pd.date_range(context['params']['start-data'],context['params']['start-data']):
            df = pd.concat([df, pd.read_csv(f'data/etl/csv/data_{date.strftime("%Y-%m-%d")}')])
    
        if not os.path.exists('data/elt/results'):
            os.mkdir('data/etl/results')
        df.to_csv('data/etl/results/main_data.csv', index=False)
    
    @task
    def transform_data():
        main_df = pd.read_csv('data/etl/results/main_data.csv')
        products_df = pd.read_json('data/etl/json/products.json')
        stores_df = pd.read_json('data/etl/json/stores.json')
        salesperson_df = pd.read_json('data/etl/json/salesperson.json')
        
        products_df.rename(columns={'id': 'product_id'}, inplace=True)
        salesperson_df.rename(columns={'id':'salesperson_id'}, inplace=True)
        
        final_df = main_df.merge(products_df,left_on='product',right_on='product_id',how='left')
        final_df = final_df.merge(stores_df,left_on='store',right_on='store_id',how='left')
        final_df = final_df.merge(salesperson_df,left_on='salesperson',right_on='salesperson_id',how='left')
        
        final_df = final_df[['id','name', 'state', 'store_name', 'store_address', 'product_name','product_value','person_name','person_address','quantity','value','date_purchase']]
    
    @task
    def create_insert_sql():
        df = pd.read_csv('data/etl/results/final_data.csv')
        file_string = ''
        for index, row in df.iterrows():
            file_string += (f"INSERT INTO sales" 
                            f"(id','name', 'state', 'store_name', 'store_address', 'product_name','product_value','person_name','person_address','quantity','value','date_purchase')"
                            f"VALUES ('{row['id']}, {row['name']}, {row['state']}, {row['store_name']}, {row['store_address']}, {row['product_name']},{row['product_value']},{row['person_name']},{row['person_address']},{row['quantity']},{row['value']},{row['date_purchase']}');\n")
                            
        with open('data/etl/results/result.sql', 'w') as f:
            f.write(file_string)                    
                            
    @task(trigger_rule='all_done')
    def cleanup_data():
        shutil.rmtree('data/etl', ignore_errors=True)
    
    insert_table = PostgresOperator(
        task_id='insert_table',
        postgres_conn_id='PG-SALES',
        sql='result.sql'
    )
    
    load_csv_s3() >> [load_products_metadata(), load_stores_metadata(), load_salesperson_metadata()] >> merge_csv() >> transform_data() >> create_insert_sql() >> insert_table() >> cleanup_data()
    
    
    
    
    
    
    
    