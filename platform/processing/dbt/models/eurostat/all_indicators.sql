{{
    config(materialized='table', schema='curated')
}}

/*
  Conformed fact table — all indicators from all sources.
  Grain: one row per (source_id, detail_id, geo, period_date).

  New sources are added by creating a stg_*.sql staging model that
  conforms to the shared schema and unioning it here.
*/

select * from {{ ref('stg_eurostat') }}

union all

select * from {{ ref('stg_nbp') }}
