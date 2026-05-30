{{
    config(materialized='table', schema='curated')
}}

/*
  Wide pivot fact for the Tourism dashboard.

  Source: curated.clt_indicators (intermediate, domain_id = 'CLT').
  Pivots two Eurostat CLT monthly series into a (geo, period_year) annual grain
  by summing monthly values within each calendar year.

  Source series are monthly (period_date = first day of month).
  SUM aggregation converts 12 months to an annual total.
  Years with fewer than 12 months of data (incomplete, e.g. current year) are included
  but will undercount — KPI cards use the latest complete year via semantic layer.

  Grain: one row per (geo, period_year).

  Indicators:
    - hotel_nights_total        ← clt.hotel_occupancy_rate / tour_occ_nim
                                   (c_resid=TOTAL, nace_r2=I551-I553, unit=NR — total hotel nights)
    - intl_tourist_arrivals     ← clt.tourist_arrivals_intl / tour_occ_arm
                                   (c_resid=FOR, nace_r2=I551-I553, unit=NR — foreign tourist arrivals)
*/

select
    geo,
    extract(year from period_date)::integer                                      as period_year,
    cast(cast(extract(year from period_date) as integer) || '-12-31' as date)   as period_date,
    count(distinct extract(month from period_date))                              as months_in_year,

    sum(case
            when detail_id = 'clt.hotel_occupancy_rate'
            then value
        end) as hotel_nights_total,

    sum(case
            when detail_id = 'clt.tourist_arrivals_intl'
            then value
        end) as intl_tourist_arrivals

from {{ ref('clt_indicators') }}
where value is not null
  and detail_id in (
      'clt.hotel_occupancy_rate',
      'clt.tourist_arrivals_intl'
  )
group by geo, extract(year from period_date)
having count(*) > 0
