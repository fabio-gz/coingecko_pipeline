from airflow.decorators import dag, task
from airflow import Dataset
from include.global_variables.vars import default_args
from include.coingecko_requests import get_coins, get_coin_market_data, get_exchages_data
from airflow.providers.google.cloud.hooks.gcs import GCSHook
import pandas as pd


CURRENCY = 'usd'

dataset = Dataset('gs://mage-zoomcamp-fab/')

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

        df = get_coin_market_data(CURRENCY, coins)
        df_parquet = df.to_parquet(index=False)
        return df_parquet
    
    @task
    def exchanges_data():
        ex = get_exchages_data()
        ex_parquet = ex.to_parquet(index=False)
        return ex_parquet
    
    @task(outlets=[dataset])
    def load_data_to_gcs(df: pd.DataFrame, object_name: str, bucket_name: str):
        gcd_hook = GCSHook(
            gcp_conn_id='gcp_conn_id',
            bucket_name=bucket_name
        )
        gcd_hook.upload(object_name=object_name, data=df, mime_type='application/parquet')
        return f"gs://{bucket_name}/{object_name}"
    
    coin_market_data = coin_market_data(coins_list())
    exchanges_data = exchanges_data()
    load_data_to_gcs(coin_market_data, 'coin_market_data.parquet', 'mage-zoomcamp-fab')
    load_data_to_gcs(exchanges_data, 'exchanges_data.parquet', 'mage-zoomcamp-fab')

coingecko_data = coingecko_data()