{{
    config(materialized='table', schema='curated')
}}

/*
  MetricFlow time spine — required by the dbt semantic layer.
  Day-grain calendar 1980-01-01 .. 2050-12-31 covering all warehouse data.
*/

select cast(d as date) as date_day
from generate_series(date '1980-01-01', date '2050-12-31', interval '1 day') t(d)
