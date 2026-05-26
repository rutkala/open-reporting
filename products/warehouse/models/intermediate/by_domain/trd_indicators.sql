{{
    config(materialized='table', schema='curated')
}}

select * from {{ ref('stg_eurostat') }}
where domain_id = 'TRD'
