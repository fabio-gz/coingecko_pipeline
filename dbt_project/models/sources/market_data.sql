{{
    config({
        "materialized": "table"
    })
}}

select * from {{ source('coingecko_data', 'coin_market_data') }}