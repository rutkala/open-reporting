{{
    config(materialized='table', schema='curated')
}}

/*
  Wide intermediate model for the finance Overview KPI row.

  MetricFlow expects one column per measure on a semantic-model source.
  curated.mart_finance is long-melted (one row per detail_id × source_id × dim_*),
  so this view pivots the three Overview indicators into a single
  (geo, period_year, period_date) grain with one numeric column each.

  Indicators included (matching products/dashboards/finance/app.py
  _build_overview_kpis):
    - fiscal_balance_pct_gdp  ← pub.fiscal_balance_gdp / eurostat / General govt / Balance
    - public_debt_pct_gdp     ← pub.public_debt_gdp    / eurostat
    - govt_revenue_pln_mn     ← pub.govt_revenue       / dbw      / General govt

  period_date = December 31 of period_year — gives MetricFlow a date column
  to use as the canonical time spine join key.
*/

select
    geo,
    period_year,
    cast(period_year || '-12-31' as date) as period_date,

    max(case
            when detail_id = 'pub.fiscal_balance_gdp'
             and source_id = 'eurostat'
             and dim_govt_sector = 'General government'
             and dim_resources_uses = 'Balance'
            then value
        end) as fiscal_balance_pct_gdp,

    max(case
            when detail_id = 'pub.public_debt_gdp'
             and source_id = 'eurostat'
            then value
        end) as public_debt_pct_gdp,

    max(case
            when detail_id = 'pub.govt_revenue'
             and source_id = 'dbw'
             and dim_govt_sector = 'General government'
            then value
        end) as govt_revenue_pln_mn

from {{ ref('mart_finance') }}
where value is not null
  and detail_id in (
      'pub.fiscal_balance_gdp',
      'pub.public_debt_gdp',
      'pub.govt_revenue'
  )
group by geo, period_year
