from airflow.decorators import dag, task
from airflow import Dataset
from include.global_variables.vars import default_args, task_log
from include.coingecko_requests import get_coins, get_coin_market_data, get_exchages_data
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
import pandas as pd


CURRENCY = 'usd'

dataset = Dataset('bq_tables')

@dag(
    dag_id = 'coingecko_data_to_gcs',
    default_args = default_args,
    schedule_interval = None
)
def coingecko_data():
    @task
    def coins_list():
        coins = get_coins()
        return coins

    @task
    def coin_market_data(coins: str):

        df = get_coin_market_data(CURRENCY, str(coins))
        return df
    
    @task
    def exchanges_data():
        ex = get_exchages_data()
        return ex
    
    @task()
    def load_data_to_gcs(df: pd.DataFrame, object_name: str, bucket_name: str):
        gcd_hook = GCSHook(bucket_name=bucket_name)
        parquet = df.to_parquet(index=False)
        gcd_hook.upload(bucket_name=bucket_name, object_name=object_name, data=parquet, mime_type='application/parquet')
        return object_name
    
    @task(outlets=[dataset])
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
    
    coin_market_data = coin_market_data(coins_list())
    exchanges_data = exchanges_data()
    coin_gcs = load_data_to_gcs(coin_market_data, 'coin_market_data.parquet', 'mage-zoomcamp-fab')
    exchange_gcs = load_data_to_gcs(exchanges_data, 'exchanges_data.parquet', 'mage-zoomcamp-fab')
    load_data_to_bigquery(coin_gcs)
    load_data_to_bigquery(exchange_gcs)

coingecko_data = coingecko_data()