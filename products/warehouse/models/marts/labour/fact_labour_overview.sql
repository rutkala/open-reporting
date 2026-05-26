{{
    config(materialized='table', schema='curated')
}}

/*
  Wide pivot fact for the Labour Market Overview KPI row.

  Source: curated.lab_indicators (intermediate, domain_id = 'LAB').
  The source is long-melted (one row per detail_id × geo × period_date),
  so this model pivots the four rate indicators into a single
  (geo, period_year, period_date) grain with one numeric column each.

  Grain: one row per (geo, period_year).

  Indicators included:
    - unemployment_rate_pct     ← lab.unemployment_rate   / Eurostat LFS (une_rt_a)
    - employment_rate_pct       ← lab.employment_rate     / Eurostat LFS (lfsa_ergan), age 20–64
    - activity_rate_pct         ← lab.activity_rate       / Eurostat LFS (lfsa_argan), age 15–74
    - youth_unemployment_rate_pct ← lab.youth_unemployment_rate / Eurostat (yth_empl_090), age 15–24

  period_date = December 31 of period_year — gives MetricFlow a date column
  to use as the canonical time spine join key (matches dim_calendar grain).
*/

select
    geo,
    extract(year from period_date)::integer                                      as period_year,
    cast(cast(extract(year from period_date) as integer) || '-12-31' as date)   as period_date,

    max(case
            when detail_id = 'lab.unemployment_rate'
            then value
        end) as unemployment_rate_pct,

    max(case
            when detail_id = 'lab.employment_rate'
            then value
        end) as employment_rate_pct,

    max(case
            when detail_id = 'lab.activity_rate'
            then value
        end) as activity_rate_pct,

    max(case
            when detail_id = 'lab.youth_unemployment_rate'
            then value
        end) as youth_unemployment_rate_pct

from {{ ref('lab_indicators') }}
where value is not null
  and detail_id in (
      'lab.unemployment_rate',
      'lab.employment_rate',
      'lab.activity_rate',
      'lab.youth_unemployment_rate'
  )
group by geo, extract(year from period_date)
