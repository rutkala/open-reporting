WITH src_gus_dbw_api AS (

    SELECT * FROM {{ source('warehouse', 'gus_dbw_api') }}

)

SELECT * FROM src_gus_dbw_api
