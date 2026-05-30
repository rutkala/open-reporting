{{
    config(materialized='table', schema='curated')
}}

/*
  Wide pivot fact for the Production & Agriculture dashboard.

  Sources: curated.bus_indicators (domain_id = 'BUS') and
           curated.agr_indicators (domain_id = 'AGR').
  Pivots two series into a single (geo, period_year) annual grain.

  All series are annual. MAX collapses each (geo, period_year) to one value.

  Grain: one row per (geo, period_year).

  Indicators:
    - industrial_output_growth_pct ← bus.industrial_output_sectoral / sts_inpr_a
                                      (unit=PCH_PRE — % change vs prior year, industrial production)
    - cereal_production_kt         ← agr.crop_production_cereals / apro_cpsh1
                                      (crops=C1100, strucpro=PR_HU_EU, unit=thousands of tonnes)
*/

select
    geo,
    extract(year from period_date)::integer                                      as period_year,
    cast(cast(extract(year from period_date) as integer) || '-12-31' as date)   as period_date,

    max(case
            when detail_id = 'bus.industrial_output_sectoral'
            then value
        end) as industrial_output_growth_pct,

    max(case
            when detail_id = 'agr.crop_production_cereals'
            then value
        end) as cereal_production_kt

from (
    select detail_id, geo, period_date, value from {{ ref('bus_indicators') }}
    where detail_id = 'bus.industrial_output_sectoral'
    union all
    select detail_id, geo, period_date, value from {{ ref('agr_indicators') }}
    where detail_id = 'agr.crop_production_cereals'
)
where value is not null
group by geo, extract(year from period_date)
