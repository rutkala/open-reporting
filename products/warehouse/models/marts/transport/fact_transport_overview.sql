{{
    config(materialized='table', schema='curated')
}}

/*
  Wide pivot fact for the Transport dashboard.

  Source: curated.trp_indicators (intermediate, domain_id = 'TRP').
  Pivots two Eurostat TRP quarterly series into a single (geo, period_year) annual grain
  by summing quarterly values within each year.

  Source series are quarterly (period_date = first day of quarter).
  SUM aggregation converts four quarters to an annual total.

  Grain: one row per (geo, period_year).

  Indicators:
    - rail_freight_mio_tkm      ← trp.freight_rail_volume / rail_go_quartal
                                   (unit=MIO_TKM — million tonne-kilometres, quarterly → annual SUM)
    - rail_passengers_mio_pkm   ← trp.passenger_rail_volume / rail_pa_quartal
                                   (unit=MIO_PKM — million passenger-kilometres, quarterly → annual SUM)
*/

select
    geo,
    extract(year from period_date)::integer                                      as period_year,
    cast(cast(extract(year from period_date) as integer) || '-12-31' as date)   as period_date,

    sum(case
            when detail_id = 'trp.freight_rail_volume'
            then value
        end) as rail_freight_mio_tkm,

    sum(case
            when detail_id = 'trp.passenger_rail_volume'
            then value
        end) as rail_passengers_mio_pkm

from {{ ref('trp_indicators') }}
where value is not null
  and detail_id in (
      'trp.freight_rail_volume',
      'trp.passenger_rail_volume'
  )
group by geo, extract(year from period_date)
having count(*) > 0
