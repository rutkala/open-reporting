{{
    config(materialized='table', schema='curated')
}}

select * from {{ ref('all_indicators') }}
where domain_id = 'FIN'
