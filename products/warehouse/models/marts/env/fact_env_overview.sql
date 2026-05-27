{{
    config(materialized='table', schema='curated')
}}

/*
  Wide pivot fact for the Environment & Energy dashboard.

  Source: curated.env_indicators (intermediate, domain_id = 'ENV').
  Pivots four Eurostat ENV series into a single (geo, period_year) annual grain.

  All series are annual.
  MAX collapses each (geo, period_year) to a single value — at most one
  non-null value per cell after the pivot.

  Grain: one row per (geo, period_year).

  Indicators:
    - ghg_emissions_mio_t       ← env.ghg_emissions_total    / env_air_gge
                                   (airpol=GHG, src_crf=TOTXMEMO, unit=MIO_T — millions of tonnes CO2e)
    - renewable_energy_pct      ← env.renewable_energy_share / nrg_ind_ren
                                   (nrg_bal=REN, unit=PC — % gross final energy consumption)
    - waste_kg_hab              ← env.municipal_waste_generated / env_wasmun
                                   (unit=KG_HAB, wst_oper=GEN — kg per inhabitant)
    - water_abstractions_mio_m3 ← env.water_abstractions      / env_wat_abs
                                   (unit=MIO_M3, wat_proc=ABST, wat_src=FRW — millions of cubic metres)
*/

select
    geo,
    extract(year from period_date)::integer                                      as period_year,
    cast(cast(extract(year from period_date) as integer) || '-12-31' as date)   as period_date,

    max(case
            when detail_id = 'env.ghg_emissions_total'
            then value
        end) as ghg_emissions_mio_t,

    max(case
            when detail_id = 'env.renewable_energy_share'
            then value
        end) as renewable_energy_pct,

    max(case
            when detail_id = 'env.municipal_waste_generated'
            then value
        end) as waste_kg_hab,

    max(case
            when detail_id = 'env.water_abstractions'
            then value
        end) as water_abstractions_mio_m3

from {{ ref('env_indicators') }}
where value is not null
  and detail_id in (
      'env.ghg_emissions_total',
      'env.renewable_energy_share',
      'env.municipal_waste_generated',
      'env.water_abstractions'
  )
group by geo, extract(year from period_date)
