{{
    config(materialized='table', schema='curated')
}}

/*
  Wide pivot fact for the National Accounts & Macroeconomics dashboard.

  Source: curated.mac_indicators (intermediate, domain_id = 'MAC').
  Pivots five Eurostat MAC series into a single (geo, period_year) annual grain.

  Annual series (one row per year per geo; MAX collapses to a single value):
    - gdp_real_growth_pct       ← mac.gdp_real_growth   / tec00115 (CLV_PCH_PRE)
    - gdp_nominal_beur          ← mac.gdp_nominal        / nama_10_gdp (CP_MEUR ÷ 1000 → EUR bn)
    - gfcf_pct_gdp              ← mac.gross_fixed_capital_formation_growth / tec00011 (% of GDP)
    - industrial_output_pct     ← mac.industrial_output_growth / sts_inpr_a (YoY%)

  Quarterly series (4 rows/year; AVG collapses to annual mean):
    - current_account_pct_gdp   ← mac.current_account_gdp / bop_gdp6_q

  Grain: one row per (geo, period_year).
*/

select
    geo,
    extract(year from period_date)::integer                                      as period_year,
    cast(cast(extract(year from period_date) as integer) || '-12-31' as date)   as period_date,

    max(case
            when detail_id = 'mac.gdp_real_growth'
            then value
        end) as gdp_real_growth_pct,

    max(case
            when detail_id = 'mac.gdp_nominal'
            then value / 1000.0
        end) as gdp_nominal_beur,

    max(case
            when detail_id = 'mac.gross_fixed_capital_formation_growth'
            then value
        end) as gfcf_pct_gdp,

    max(case
            when detail_id = 'mac.industrial_output_growth'
            then value
        end) as industrial_output_pct,

    avg(case
            when detail_id = 'mac.current_account_gdp'
            then value
        end) as current_account_pct_gdp

from {{ ref('mac_indicators') }}
where value is not null
  and detail_id in (
      'mac.gdp_real_growth',
      'mac.gdp_nominal',
      'mac.gross_fixed_capital_formation_growth',
      'mac.industrial_output_growth',
      'mac.current_account_gdp'
  )
group by geo, extract(year from period_date)
