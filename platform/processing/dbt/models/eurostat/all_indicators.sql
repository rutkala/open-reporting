{{
    config(materialized='table', schema='curated')
}}

/*
  Combined view of all Eurostat indicators across all domains.
  Grain: one row per (detail_id, period).
  Prefer this over individual domain tables when exploring cross-domain data.
*/

select * from {{ ref('stg_eurostat') }}
