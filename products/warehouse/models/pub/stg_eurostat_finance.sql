{{
    config(materialized='table', schema='curated')
}}

/*
  Staging: raw.eurostat_observations → curated.all_indicators (PUB / GFS indicators)

  Covers three Eurostat GFS datasets:
    gov_10a_main     — ESA 2010 main aggregates (B9, TR, TE, D41PAY, P51G, D62_D632PAY,
                        D2REC, D5REC, D61REC, D1PAY) — all EU countries, % GDP, S.13
    gov_10dd_edpt1   — EDP official Maastricht notifications — deficit (B9), all EU countries
    gov_10a_exp      — COFOG functional expenditure GF01–GF10 — all EU countries, % GDP, S.13

  Mapping: dimension_key → detail_id via inline CASE expressions.
  All rows use sector S.13 (general government), so dim_govt_sector = 'General government'.
  dim_resources_uses is assigned by indicator type (Revenue / Expenditure / Balance).

  Note: pub.public_debt_gdp (gov_10dd_edpt1, na_item=GD) is handled by stg_eurostat.sql
  via eurostat_series seed; pub.edp_deficit_gdp (B9) is handled here.
*/

with obs as (

    select
        dataset_code,
        geo,
        period,
        dimension_key,
        value,
        obs_status,
        fetched_at
    from {{ source('raw', 'eurostat_observations') }}
    where dataset_code in ('gov_10a_main', 'gov_10dd_edpt1', 'gov_10a_exp')
      and value is not null

),

mapped as (

    select
        'eurostat'          as source_id,
        'PUB'               as domain_id,

        case dataset_code

            -- gov_10a_main: ESA main aggregates (all % GDP, sector S.13)
            when 'gov_10a_main' then case dimension_key
                when 'na_item=B9&sector=S13&unit=PC_GDP'             then 'pub.fiscal_balance_gdp'
                when 'na_item=TR&sector=S13&unit=PC_GDP'             then 'pub.revenue_gdp'
                when 'na_item=TE&sector=S13&unit=PC_GDP'             then 'pub.expenditure_gdp'
                when 'na_item=D41PAY&sector=S13&unit=PC_GDP'         then 'pub.interest_expenditure_gdp'
                when 'na_item=P51G&sector=S13&unit=PC_GDP'           then 'pub.govt_investment_gdp'
                when 'na_item=D62_D632PAY&sector=S13&unit=PC_GDP'    then 'pub.social_transfers_gdp'
                when 'na_item=D2REC&sector=S13&unit=PC_GDP'          then 'pub.taxes_prod_imports_gdp'
                when 'na_item=D5REC&sector=S13&unit=PC_GDP'          then 'pub.taxes_income_gdp'
                when 'na_item=D61REC&sector=S13&unit=PC_GDP'         then 'pub.social_contributions_gdp'
                when 'na_item=D1PAY&sector=S13&unit=PC_GDP'          then 'pub.compensation_employees_gdp'
            end

            -- gov_10dd_edpt1: EDP official notifications — deficit only (debt handled in stg_eurostat)
            when 'gov_10dd_edpt1' then case dimension_key
                when 'na_item=B9&sector=S13&unit=PC_GDP'             then 'pub.edp_deficit_gdp'
            end

            -- gov_10a_exp: COFOG functional expenditure breakdown
            when 'gov_10a_exp' then case dimension_key
                when 'cofog99=GF01&na_item=TE&sector=S13&unit=PC_GDP' then 'pub.cofog_01_gdp'
                when 'cofog99=GF02&na_item=TE&sector=S13&unit=PC_GDP' then 'pub.cofog_02_gdp'
                when 'cofog99=GF03&na_item=TE&sector=S13&unit=PC_GDP' then 'pub.cofog_03_gdp'
                when 'cofog99=GF04&na_item=TE&sector=S13&unit=PC_GDP' then 'pub.cofog_04_gdp'
                when 'cofog99=GF05&na_item=TE&sector=S13&unit=PC_GDP' then 'pub.cofog_05_gdp'
                when 'cofog99=GF06&na_item=TE&sector=S13&unit=PC_GDP' then 'pub.cofog_06_gdp'
                when 'cofog99=GF07&na_item=TE&sector=S13&unit=PC_GDP' then 'pub.cofog_07_gdp'
                when 'cofog99=GF08&na_item=TE&sector=S13&unit=PC_GDP' then 'pub.cofog_08_gdp'
                when 'cofog99=GF09&na_item=TE&sector=S13&unit=PC_GDP' then 'pub.cofog_09_gdp'
                when 'cofog99=GF10&na_item=TE&sector=S13&unit=PC_GDP' then 'pub.cofog_10_gdp'
            end

        end                 as detail_id,

        obs.geo             as geo,

        case
            when length(obs.period) = 4
                then cast(obs.period || '-01-01' as date)
            when obs.period like '____-Q_'
                then case right(obs.period, 1)
                    when '1' then cast(left(obs.period, 4) || '-01-01' as date)
                    when '2' then cast(left(obs.period, 4) || '-04-01' as date)
                    when '3' then cast(left(obs.period, 4) || '-07-01' as date)
                    when '4' then cast(left(obs.period, 4) || '-10-01' as date)
                end
            when obs.period like '____-S_'
                then case right(obs.period, 1)
                    when '1' then cast(left(obs.period, 4) || '-01-01' as date)
                    when '2' then cast(left(obs.period, 4) || '-07-01' as date)
                end
            when obs.period like '____-__'
                then cast(obs.period || '-01' as date)
        end                 as period_date,

        null::varchar       as dim_sex,
        null::varchar       as dim_age_group,
        null::varchar       as dim_type_of_locality,
        null::varchar       as dim_nace_sector,
        null::varchar       as dim_employment_status,
        null::varchar       as dim_education_level,
        null::varchar       as dim_prodcom_product,
        null::varchar       as dim_hicp_category,
        null::varchar       as dim_pollutant_type,
        null::varchar       as dim_waste_category,
        null::varchar       as dim_healthcare_function,
        null::varchar       as dim_health_provider,
        null::varchar       as dim_health_financing,
        'General government' as dim_govt_sector,
        null::varchar       as dim_institutional_sector,
        null::varchar       as dim_asset_classification,
        null::varchar       as dim_tourist_origin,
        null::varchar       as dim_trip_direction,
        null::varchar       as dim_trip_duration,
        null::varchar       as dim_quintile_group,
        null::varchar       as dim_citizenship,

        -- Revenue / Expenditure / Balance by indicator type
        case
            when obs.dimension_key like 'na_item=TR%'
              or obs.dimension_key like 'na_item=D2REC%'
              or obs.dimension_key like 'na_item=D5REC%'
              or obs.dimension_key like 'na_item=D61REC%'
                then 'Revenue'
            when obs.dimension_key like 'na_item=TE%'
              or obs.dimension_key like 'na_item=D1PAY%'
              or obs.dimension_key like 'na_item=P51G%'
              or obs.dimension_key like 'na_item=D41PAY%'
              or obs.dimension_key like 'na_item=D62_D632PAY%'
              or obs.dimension_key like 'cofog99=%'
                then 'Expenditure'
            when obs.dimension_key like 'na_item=B9%'
                then 'Balance'
        end                 as dim_resources_uses,

        null::varchar       as dim_transport_mode,
        null::varchar       as dim_accommodation_type,

        obs.value           as value,
        obs.obs_status      as obs_status,
        obs.fetched_at      as fetched_at,
        current_timestamp   as updated_at

    from obs

)

select * from mapped
where detail_id is not null
