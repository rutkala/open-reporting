{{
    config(materialized='table', schema='curated')
}}

/*
  Wide pivot fact for the Financial Markets dashboard.

  Source: curated.fin_indicators (intermediate, domain_id = 'FIN').
  All FIN series are daily NBP exchange rates — aggregated to annual grain via AVG.

  Grain: one row per (geo, period_year).

  Indicators:
    - eur_pln_avg  ← fin.exchange_rate_eur_pln (NBP mid-rate, EUR/PLN annual average)
    - usd_pln_avg  ← fin.exchange_rate_usd_pln (NBP mid-rate, USD/PLN annual average)
    - chf_pln_avg  ← fin.exchange_rate_chf_pln (NBP mid-rate, CHF/PLN annual average)
    - gbp_pln_avg  ← fin.exchange_rate_gbp_pln (NBP mid-rate, GBP/PLN annual average)
*/

select
    geo,
    extract(year from period_date)::integer                                      as period_year,
    cast(cast(extract(year from period_date) as integer) || '-12-31' as date)   as period_date,

    avg(case
            when detail_id = 'fin.exchange_rate_eur_pln'
            then value
        end) as eur_pln_avg,

    avg(case
            when detail_id = 'fin.exchange_rate_usd_pln'
            then value
        end) as usd_pln_avg,

    avg(case
            when detail_id = 'fin.exchange_rate_chf_pln'
            then value
        end) as chf_pln_avg,

    avg(case
            when detail_id = 'fin.exchange_rate_gbp_pln'
            then value
        end) as gbp_pln_avg

from {{ ref('fin_indicators') }}
where value is not null
  and detail_id in (
      'fin.exchange_rate_eur_pln',
      'fin.exchange_rate_usd_pln',
      'fin.exchange_rate_chf_pln',
      'fin.exchange_rate_gbp_pln'
  )
group by geo, extract(year from period_date)
