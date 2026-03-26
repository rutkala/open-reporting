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

    select *
    from {{ source('raw', 'eurostat_observations') }}
    where geo = 'PL'
      and value is not null

),

seed as (

    select *
    from {{ ref('eurostat_series') }}

),

joined as (

    select
        s.detail_id,
        s.domain_id,
        o.geo,
        o.period,
        o.value,
        o.obs_status,
        o.dataset_code,
        o.fetched_at,
        row_number() over (
            partition by s.detail_id, o.geo, o.period
            order by o.fetched_at desc
        ) as rn

    from obs o
    inner join seed s
        on  o.dataset_code   = s.dataset_code
        and o.dimension_key  = s.dimension_key

)

select
    detail_id,
    domain_id,
    geo,
    period,
    value,
    obs_status,
    dataset_code,
    fetched_at,
    current_timestamp as updated_at

from joined
where rn = 1
