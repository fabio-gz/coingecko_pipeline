{{
    config({
        "materialized": "table"
    })
}}

select {{ dbt_utils.generate_surrogate_key(['id']) }} as id, name, year_established, country, url, trust_score, trust_score_rank, trade_volume_24h_btc, trade_volume_24h_btc_normalized 
from {{ source('coingecko_data', 'exchanges_data') }}