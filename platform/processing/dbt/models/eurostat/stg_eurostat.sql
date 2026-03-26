{{
    config(materialized='table', schema='curated')
}}

/*
  Staging: raw.eurostat_observations + catalogue seed → named indicators.

  Joins each raw observation to its catalogue detail_id using
  (dataset_code, dimension_key). dimension_key is a sorted
  "dim=val&dim=val" string excluding geo/freq/time — computed
  identically during ingestion and in the seed.

  Output grain: one row per (detail_id, geo, period).
  Multiple raw rows can map to one detail_id when a dataset contains
  more than one series matching the same seed filters — these are
  deduplicated by keeping the latest fetched_at.
*/

with obs as (

    select
        dataset_code,
        geo,
        period,
        dimension_key,
        value,
        obs_status,
        fetched_at
    from {{ source('raw', 'eurostat_observations') }}
    where geo = 'PL'
      and value is not null

),

seed as (

    select
        detail_id,
        domain_id,
        dataset_code  as s_dataset_code,
        dimension_key as s_dimension_key
    from {{ ref('eurostat_series') }}

)

select
    s.detail_id       as detail_id,
    s.domain_id       as domain_id,
    o.geo             as geo,
    o.period          as period,
    o.value           as value,
    o.obs_status      as obs_status,
    o.dataset_code    as dataset_code,
    o.fetched_at      as fetched_at,
    current_timestamp as updated_at

from obs o
inner join seed s
    on  o.dataset_code  = s.s_dataset_code
    and o.dimension_key = s.s_dimension_key
