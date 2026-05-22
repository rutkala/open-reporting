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

  Conforms to the shared staging schema: source_id, domain_id, detail_id,
  geo, period, period_date, value, obs_status, fetched_at, updated_at.
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
    where value is not null

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
    'eurostat'        as source_id,
    s.domain_id       as domain_id,
    s.detail_id       as detail_id,
    o.geo             as geo,
    case
        when length(o.period) = 4
            then cast(o.period || '-01-01' as date)
        when o.period like '____-Q_'
            then case right(o.period, 1)
                when '1' then cast(left(o.period, 4) || '-01-01' as date)
                when '2' then cast(left(o.period, 4) || '-04-01' as date)
                when '3' then cast(left(o.period, 4) || '-07-01' as date)
                when '4' then cast(left(o.period, 4) || '-10-01' as date)
            end
        when o.period like '____-S_'
            then case right(o.period, 1)
                when '1' then cast(left(o.period, 4) || '-01-01' as date)
                when '2' then cast(left(o.period, 4) || '-07-01' as date)
            end
        when o.period like '____-__'
            then cast(o.period || '-01' as date)
    end               as period_date,
    null::varchar     as dim_sex,
    null::varchar     as dim_age_group,
    null::varchar     as dim_type_of_locality,
    null::varchar     as dim_nace_sector,
    null::varchar     as dim_employment_status,
    null::varchar     as dim_education_level,
    null::varchar     as dim_prodcom_product,
    null::varchar     as dim_hicp_category,
    null::varchar     as dim_pollutant_type,
    null::varchar     as dim_waste_category,
    null::varchar     as dim_healthcare_function,
    null::varchar     as dim_health_provider,
    null::varchar     as dim_health_financing,
    null::varchar     as dim_govt_sector,
    null::varchar     as dim_institutional_sector,
    null::varchar     as dim_asset_classification,
    null::varchar     as dim_tourist_origin,
    null::varchar     as dim_trip_direction,
    null::varchar     as dim_trip_duration,
    null::varchar     as dim_quintile_group,
    null::varchar     as dim_citizenship,
    null::varchar     as dim_resources_uses,
    null::varchar     as dim_transport_mode,
    null::varchar     as dim_accommodation_type,
    o.value           as value,
    o.obs_status      as obs_status,
    o.fetched_at      as fetched_at,
    current_timestamp as updated_at

from obs o
inner join seed s
    on  o.dataset_code  = s.s_dataset_code
    and o.dimension_key = s.s_dimension_key
