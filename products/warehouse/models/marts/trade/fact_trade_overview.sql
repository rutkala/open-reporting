{{
    config(materialized='table', schema='curated')
}}

/*
  Wide pivot fact for the Trade dashboard.

  Source: curated.trd_indicators (intermediate, domain_id = 'TRD').
  Pivots three Eurostat TRD series into a single (geo, period_year) annual grain.

  All series are annual.
  MAX collapses each (geo, period_year) to a single value — at most one
  non-null value per cell after the pivot.

  Grain: one row per (geo, period_year).

  Indicators:
    - exports_goods_mio_eur  ← trd.exports_goods_total / ext_lt_intratrd
                                (flow=EXP, partner=WORLD, unit=MIO_EUR — total goods exports)
    - imports_goods_mio_eur  ← trd.imports_goods_total / ext_lt_intratrd
                                (flow=IMP, partner=WORLD, unit=MIO_EUR — total goods imports)
    - trade_balance_mio_eur  ← trd.trade_balance_goods / ext_lt_intratrd
                                (flow=BAL, partner=WORLD, unit=MIO_EUR — goods trade balance)
*/

select
    geo,
    extract(year from period_date)::integer                                      as period_year,
    cast(cast(extract(year from period_date) as integer) || '-12-31' as date)   as period_date,

    max(case
            when detail_id = 'trd.exports_goods_total'
            then value
        end) as exports_goods_mio_eur,

    max(case
            when detail_id = 'trd.imports_goods_total'
            then value
        end) as imports_goods_mio_eur,

    max(case
            when detail_id = 'trd.trade_balance_goods'
            then value
        end) as trade_balance_mio_eur

from {{ ref('trd_indicators') }}
where value is not null
  and detail_id in (
      'trd.exports_goods_total',
      'trd.imports_goods_total',
      'trd.trade_balance_goods'
  )
group by geo, extract(year from period_date)
