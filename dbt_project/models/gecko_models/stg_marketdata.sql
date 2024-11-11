{{
    config({
        "materialized": "table",
        "alias": "stg_marketdata"
    })
}}

SELECT id, symbol, market_cap, total_volume, RANK() OVER (ORDER BY market_cap DESC) AS market_cap_rank
FROM {{ ref('sources.market_data') }}