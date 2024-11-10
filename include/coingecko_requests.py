import requests
import pandas as pd
from variables.vars import api_key, task_log

def get_simple_price(coin_id: str, currency: str) -> pd.DataFrame:
    """
    Get the simple price for given list of coins.
    """

    url = "https://api.coingecko.com/api/v3/simple/price"

    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": api_key
    }

    params = {
        "ids": coin_id,
        "vs_currencies": currency,
        "include_market_cap": "true",
        "include_24hr_vol": "true",
        "include_24hr_change": "true",
    }
    try:
        res = requests.get(url, headers=headers, params=params)
        data = res.json()
        return pd.DataFrame(data)
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
                'order': 'market_cap_desc',
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

        return pd.DataFrame(data)
    except Exception as e:
        task_log.error(f"Error getting exchanges data: {e}")
        raise e