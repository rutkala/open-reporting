{{
    config(materialized='table', schema='curated')
}}

/*
  Wide pivot fact for the Labour Market Wages & Vacancies row.

  Source: curated.lab_indicators (intermediate, domain_id = 'LAB').
  The source is long-melted (one row per detail_id × geo × period_date),
  so this model pivots the three wages/vacancies indicators into a single
  (geo, period_year, period_date) grain with one numeric column each.

  Grain: one row per (geo, period_year).

  Indicators included:
    - wage_growth_pct     ← lab.wage_growth     / Eurostat LCI (lc_lci_r2_a), sector B–S, yoy
    - minimum_wage_eur    ← lab.minimum_wage     / Eurostat (earn_mw_cur), EUR/month
    - vacancy_rate_pct    ← lab.vacancy_rate     / Eurostat JVS (jvs_a_nace2), sector B–S

  period_date = December 31 of period_year — gives MetricFlow a date column
  to use as the canonical time spine join key (matches dim_calendar grain).
*/

select
    geo,
    extract(year from period_date)::integer                                      as period_year,
    cast(cast(extract(year from period_date) as integer) || '-12-31' as date)   as period_date,

    max(case
            when detail_id = 'lab.wage_growth'
            then value
        end) as wage_growth_pct,

    max(case
            when detail_id = 'lab.minimum_wage'
            then value
        end) as minimum_wage_eur,

    max(case
            when detail_id = 'lab.vacancy_rate'
            then value
        end) as vacancy_rate_pct

from {{ ref('lab_indicators') }}
where value is not null
  and detail_id in (
      'lab.wage_growth',
      'lab.minimum_wage',
      'lab.vacancy_rate'
  )
group by geo, extract(year from period_date)
