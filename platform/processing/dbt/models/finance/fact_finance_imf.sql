{{
    config(materialized='table', schema='curated')
}}

/*
  Wide annual fact for IMF WEO public-finance projections.

  Source: curated.mart_finance, source_id='imf'. Each row is one country
  in one year, with four % of GDP metrics. The `is_projection` column
  comes straight from the WEO dataset — TRUE for forecast years (2026+
  as of the spring 2025 WEO), FALSE for historicals. mart_finance stores
  it as nullable BOOLEAN; we coalesce to FALSE here so MetricFlow can
  group on it as a categorical without NULL ambiguity.

  Used by the Prognozy MFW page: line visuals split each metric series
  by is_projection into solid (history) and dashed (forecast) traces.
*/

select
    geo,
    period_year,
    cast(period_year || '-12-31' as date) as period_date,
    coalesce(is_projection, false)        as is_projection,

    max(case when detail_id = 'pub.fiscal_balance_imf'    then value end) as fiscal_balance_imf,
    max(case when detail_id = 'pub.primary_balance_imf'   then value end) as primary_balance_imf,
    max(case when detail_id = 'pub.structural_balance_imf' then value end) as structural_balance_imf,
    max(case when detail_id = 'pub.gross_debt_imf'        then value end) as gross_debt_imf,
    max(case when detail_id = 'pub.net_debt_imf'          then value end) as net_debt_imf

from {{ ref('mart_finance') }}
where source_id = 'imf'
  and value is not null
  and detail_id in (
      'pub.fiscal_balance_imf',
      'pub.primary_balance_imf',
      'pub.structural_balance_imf',
      'pub.gross_debt_imf',
      'pub.net_debt_imf'
  )
group by geo, period_year, coalesce(is_projection, false)
