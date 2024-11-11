import requests
import pandas as pd
from include.global_variables.vars import api_key, task_log

def get_coins() -> str:
    """
    Get list of coins.
    """

    url = "https://api.coingecko.com/api/v3/coins/list"

    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": api_key
    }

    try:
        res = requests.get(url, headers=headers)
        data = res.json()
        df = pd.DataFrame(data)
        st = ', '.join(df['id'].iloc[:10])
        return st
    except Exception as e:
        task_log.error(f"Error getting simple price: {e}")
        raise e
    

def get_coin_market_data(vs_currency: str, ids: str) -> pd.DataFrame:
    """
    Get the market data for given list of coins.
    """

    try:
        all_data = []
        page = 1
        url = "https://api.coingecko.com/api/v3/coins/markets"
        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": api_key
        }

        while True:
            params = {
                'vs_currency': vs_currency,
                'ids': ids,
                'per_page': 200,
                'page': page,
            }
            
            res = requests.get(url, headers=headers, params=params)
            data = res.json()
            
            if not data:
                break
                
            all_data.extend(data)
            page += 1
            
        return pd.DataFrame(all_data)
    except Exception as e:
        task_log.error(f"Error getting coin market data: {e}")
        raise e


def get_exchages_data() -> pd.DataFrame:
    """
    Get the exchanges data.
    """
    try:
        url = "https://api.coingecko.com/api/v3/exchanges"
        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": api_key
        }
        params = {
            'per_page': 200,
        }
        res = requests.get(url, headers=headers, params=params)
        data = res.json()

        return pd.DataFrame(data, dtype=str)
    except Exception as e:
        task_log.error(f"Error getting exchanges data: {e}")
        raise e