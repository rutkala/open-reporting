{{
    config(
        materialized='table',
        schema='curated'
    )
}}

/*
  Transform: raw.nbp_exchange_rates → curated.fin_exchange_rates
  Source:    NBP Table A daily mid-rates (USD, EUR, CHF, GBP / PLN)
  Grain:     one row per currency per business day

  DQ applied:
  1. Completeness  — exclude rows where rate_date or mid_rate is null
  2. Validity      — exclude rates <= 0 (NBP never publishes zero/negative, would indicate corrupt data)
  3. Deduplication — keep the most-recently-fetched row per (currency_code, rate_date)
                     in case of re-ingestion on the same day
*/

with source as (

    select *
    from {{ source('raw', 'nbp_exchange_rates') }}
    where rate_date  is not null
      and mid_rate   is not null
      and mid_rate   > 0

),

deduped as (

    select *
    from source
    qualify row_number() over (
        partition by currency_code, rate_date
        order by     fetched_at desc
    ) = 1

)

select
    currency_code,

    case currency_code
        when 'USD' then 'US Dollar'
        when 'EUR' then 'Euro'
        when 'CHF' then 'Swiss Franc'
        when 'GBP' then 'British Pound'
    end                        as currency_name,

    rate_date,
    mid_rate                   as mid_rate_pln,
    table_no,
    current_timestamp          as updated_at

from deduped
