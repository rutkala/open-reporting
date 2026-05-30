{{
    config(materialized='table', schema='curated')
}}

/*
  Wide pivot fact for the Energy dashboard.

  Source: curated.ene_indicators (intermediate, domain_id = 'ENE').
  Pivots two Eurostat ENE series into a single (geo, period_year) annual grain.

  All series are annual.
  MAX collapses each (geo, period_year) to a single value — at most one
  non-null value per cell after the pivot.

  Grain: one row per (geo, period_year).

  Indicators:
    - renewable_energy_pct  ← ene.renewable_energy_share / nrg_ind_ren
                               (nrg_bal=REN, unit=PC — % gross final energy consumption from renewables)
    - energy_intensity      ← ene.energy_intensity / sdg_07_30
                               (unit=EUR_KGOE — GDP in EUR per kg oil equivalent; higher = more efficient)
*/

select
    geo,
    extract(year from period_date)::integer                                      as period_year,
    cast(cast(extract(year from period_date) as integer) || '-12-31' as date)   as period_date,

    max(case
            when detail_id = 'ene.renewable_energy_share'
            then value
        end) as renewable_energy_pct,

    max(case
            when detail_id = 'ene.energy_intensity'
            then value
        end) as energy_intensity_eur_kgoe

from {{ ref('ene_indicators') }}
where value is not null
  and detail_id in (
      'ene.renewable_energy_share',
      'ene.energy_intensity'
  )
group by geo, extract(year from period_date)
