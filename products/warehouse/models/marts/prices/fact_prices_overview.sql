{{
    config(materialized='table', schema='curated')
}}

/*
  Wide pivot fact for the Prices & Inflation dashboard.

  Source: curated.prc_indicators (intermediate, domain_id = 'PRC').
  Pivots three Eurostat PRC series into a single (geo, period_year) annual grain.

  All series are annual.
  MAX collapses each (geo, period_year) to a single value — at most one
  non-null value per cell after the pivot.

  Grain: one row per (geo, period_year).

  Indicators:
    - inflation_rate_pct     ← prc.cpi_total  / prc_hicp_aind
                                (coicop=CP00, unit=RCH_A_AVG — % annual average rate of change)
    - food_hicp_idx          ← prc.cpi_food   / prc_hicp_aind
                                (coicop=CP01, unit=INX_A_AVG — food & non-alcoholic beverages index, 2015=100)
    - housing_hicp_idx       ← prc.cpi_energy / prc_hicp_aind
                                (coicop=CP04, unit=INX_A_AVG — housing, water, electricity & gas index, 2015=100)
*/

select
    geo,
    extract(year from period_date)::integer                                      as period_year,
    cast(cast(extract(year from period_date) as integer) || '-12-31' as date)   as period_date,

    max(case
            when detail_id = 'prc.cpi_total'
            then value
        end) as inflation_rate_pct,

    max(case
            when detail_id = 'prc.cpi_food'
            then value
        end) as food_hicp_idx,

    max(case
            when detail_id = 'prc.cpi_energy'
            then value
        end) as housing_hicp_idx

from {{ ref('prc_indicators') }}
where value is not null
  and detail_id in (
      'prc.cpi_total',
      'prc.cpi_food',
      'prc.cpi_energy'
  )
group by geo, extract(year from period_date)
