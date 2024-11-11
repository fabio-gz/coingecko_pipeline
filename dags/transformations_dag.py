from airflow.decorators import dag, task
from airflow import Dataset
from include.global_variables.vars import default_args, task_log
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
import pandas as pd

@dag(
    dag_id = 'coingecko_transformations_data',
    default_args = default_args,
    schedule_interval = None
)
def transformation_data():
    @task
    def load_data_to_bigquery(object_name: str):
        gcs_hook = GCSHook(bucket_name='mage-zoomcamp-fab')
        data = gcs_hook.download(object_name=object_name)
        
        df = pd.read_parquet(data)
        
        project_id = 'airbnb-360816'
        dataset_id = 'coingecko_data'
        table_id = object_name.replace('.parquet', '')

        bq_hook = BigQueryHook()
        
        records = df.to_dict('records')
        
        bq_hook.insert_all(
            project_id=project_id,
            dataset_id=dataset_id,
            table_id=table_id,
            rows=records,
            ignore_unknown_values=True
        )
        
        task_log.info(f"Loaded {object_name} to BigQuery table {dataset_id}.{table_id}")
        return

    

