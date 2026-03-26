{{
    config(materialized='table', schema='curated')
}}

/*
  Calendar dimension — monthly spine.
  Grain: one row per calendar month from 1995-01-01 to ~3 years ahead.

  date_day is the primary key (first day of month).
  Fact tables join on: fact.period_date = dim_calendar.date_day

  Supports Year → Quarter → Month drill-down in dashboards.
*/

with spine as (

    select unnest(
        generate_series(
            date '1995-01-01',
            (date_trunc('year', current_date) + interval '3 years')::date,
            interval '1 month'
        )
    )::date as date_day

)

select
    date_day,
    year(date_day)                                      as year,
    quarter(date_day)                                   as quarter,
    month(date_day)                                     as month,
    year(date_day)::varchar || '-Q' || quarter(date_day)::varchar  as year_quarter,
    strftime(date_day, '%Y-%m')                         as year_month
from spine
