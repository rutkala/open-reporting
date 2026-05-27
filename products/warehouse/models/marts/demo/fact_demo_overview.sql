{{
    config(materialized='table', schema='curated')
}}

/*
  Wide pivot fact for the Population & Demographics dashboard.

  Source: curated.pop_indicators (intermediate, domain_id = 'POP').
  Pivots five Eurostat POP series into a single (geo, period_year) annual grain.

  All series are annual (demo_gind YYYY format, demo_mlexpec YYYY format).
  MAX collapses each (geo, period_year) to a single value — at most one
  non-null value per cell after the pivot.

  Grain: one row per (geo, period_year).

  Indicators:
    - population_mln          ← pop.population_total / demo_gind (JAN, absolute → ÷1M)
    - birth_rate_per1000      ← pop.births            / demo_gind (GBIRTHRT, ‰)
    - death_rate_per1000      ← pop.deaths            / demo_gind (GDEATHRT, ‰)
    - natural_increase_per1000← births − deaths (derived, positive = net growth)
    - life_expectancy_f_years ← pop.life_expectancy_f / demo_mlexpec (age Y_LT1, sex=F, years)
    - life_expectancy_m_years ← pop.life_expectancy_m / demo_mlexpec (age Y_LT1, sex=M, years)
*/

select
    geo,
    extract(year from period_date)::integer                                      as period_year,
    cast(cast(extract(year from period_date) as integer) || '-12-31' as date)   as period_date,

    max(case
            when detail_id = 'pop.population_total'
            then value / 1000000.0
        end) as population_mln,

    max(case
            when detail_id = 'pop.births'
            then value
        end) as birth_rate_per1000,

    max(case
            when detail_id = 'pop.deaths'
            then value
        end) as death_rate_per1000,

    max(case when detail_id = 'pop.births'  then value end)
  - max(case when detail_id = 'pop.deaths' then value end) as natural_increase_per1000,

    max(case
            when detail_id = 'pop.life_expectancy_f'
            then value
        end) as life_expectancy_f_years,

    max(case
            when detail_id = 'pop.life_expectancy_m'
            then value
        end) as life_expectancy_m_years

from {{ ref('pop_indicators') }}
where value is not null
  and detail_id in (
      'pop.population_total',
      'pop.births',
      'pop.deaths',
      'pop.life_expectancy_f',
      'pop.life_expectancy_m'
  )
group by geo, extract(year from period_date)
