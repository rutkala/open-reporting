{{
    config(materialized='table', schema='curated')
}}

/*
  Staging: raw.nbp_exchange_rates + nbp_series seed → conformed indicators.

  Joins each raw NBP rate to its catalogue detail_id using currency_code.
  Output conforms to the shared staging schema used by all source staging models:
  (source_id, domain_id, detail_id, geo, period, period_date, value, obs_status, fetched_at, updated_at)

  Output grain: one row per (detail_id, period_date).
  Deduplication: keeps the most-recently-fetched row per (currency_code, rate_date)
  in case of re-ingestion on the same day.
*/

with source as (

    select *
    from {{ source('raw', 'nbp_exchange_rates') }}
    where rate_date is not null
      and mid_rate  is not null
      and mid_rate  > 0

),

deduped as (

    select *
    from source
    qualify row_number() over (
        partition by currency_code, rate_date
        order by     fetched_at desc
    ) = 1

),

seed as (

    select
        detail_id,
        domain_id,
        currency_code as s_currency_code
    from {{ ref('nbp_series') }}

)

select
    'nbp'                      as source_id,
    s.domain_id                as domain_id,
    s.detail_id                as detail_id,
    'PL'                       as geo,
    d.rate_date                as period_date,
    null::varchar              as dim1_name,
    null::varchar              as dim1_value,
    null::varchar              as dim2_name,
    null::varchar              as dim2_value,
    null::varchar              as dim3_name,
    null::varchar              as dim3_value,
    null::varchar              as dim4_name,
    null::varchar              as dim4_value,
    cast(d.mid_rate as double) as value,
    null::varchar              as obs_status,
    d.fetched_at               as fetched_at,
    current_timestamp          as updated_at

from deduped d
inner join seed s
    on d.currency_code = s.s_currency_code
