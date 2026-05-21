{{ config(materialized='table', schema='curated') }}

/*
  dim_calendar — the shared calendar dimension for the data model.

  Star-schema convention: this is THE dimension table any fact table joins
  to for date-based slicing. Also serves as MetricFlow's time spine (declared
  in dim_calendar.yml).

  Grain: one row per day, 1980-01-01 .. 2050-12-31.

  Date generation uses dbt's portable `date_spine()` macro so the model
  is adapter-agnostic (works on DuckDB, Postgres, Snowflake, BigQuery,
  …) without warehouse-specific syntax.

  Columns:
    date_key      DATE      — the join key (primary entity)
    year          INT       — e.g. 2024
    quarter       INT       — 1..4
    month         INT       — 1..12
    year_quarter  TEXT      — e.g. "2024 Q1"
    year_month    TEXT      — e.g. "2024-01"
*/

with spine as (
    {{ dbt.date_spine(
        datepart="day",
        start_date="cast('1980-01-01' as date)",
        end_date="cast('2050-12-31' as date)"
    ) }}
),
dates as (
    select cast(date_day as date) as date_key
    from spine
)
select
    date_key,
    extract(year    from date_key)::int as year,
    extract(quarter from date_key)::int as quarter,
    extract(month   from date_key)::int as month,
    extract(year from date_key)::text
        || ' Q' || extract(quarter from date_key)::text                       as year_quarter,
    extract(year from date_key)::text
        || '-' || lpad(extract(month from date_key)::text, 2, '0')            as year_month
from dates
