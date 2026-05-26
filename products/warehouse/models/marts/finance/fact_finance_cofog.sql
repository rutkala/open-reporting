{{
    config(materialized='table', schema='curated')
}}

/*
  Long-format fact for COFOG functional spending.

  Each row is one (geo, period_year, cofog_function) tuple with the
  expenditure share as % of GDP. Source: Eurostat COFOG-10 published
  via curated.int_finance_consolidated under detail_id `pub.cofog_NN_gdp`.

  Star-schema joins:
    - `geo`            → dim_geo
    - `date_key`       → dim_calendar (via period_date)
    - `cofog_function` → dim_cofog

  Grain: (geo, period_year, cofog_function). One measure column:
  `cofog_pct_gdp`. Visuals can group by year + COFOG function to stack
  the 10 sub-categories.
*/

select
    m.geo,
    m.period_year,
    cast(m.period_year || '-12-31' as date) as period_date,
    c.cofog_function,
    m.value as cofog_pct_gdp

from {{ ref('int_finance_consolidated') }} m
join {{ ref('dim_cofog') }} c on c.cofog_code = m.detail_id
where m.detail_id like 'pub.cofog_%'
  and m.value is not null
  and m.dim_govt_sector = 'General government'
