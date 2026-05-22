{{
    config(materialized='table', schema='curated')
}}

/*
  Staging: raw.imf_weo → curated.all_indicators (IMF WEO fiscal indicators)

  Covers 7 WEO fiscal subjects (all % GDP or % potential GDP):
    GGXCNL_NGDP  Overall fiscal balance          → pub.fiscal_balance_imf
    GGXONLB_NGDP Primary balance                  → pub.primary_balance_imf
    GGSB_NPGDP   Cyclically-adjusted balance       → pub.structural_balance_imf
    GGXWDG_NGDP  Gross government debt             → pub.gross_debt_imf
    GGXWDN_NGDP  Net government debt               → pub.net_debt_imf
    GGR_NGDP     Government revenue                → pub.revenue_imf
    GGX_NGDP     Government expenditure            → pub.expenditure_imf

  Countries: 27 EU member states (POL + V4 + all others).
  ISO code mapping: WEO uses 3-letter codes (POL); standard geo column uses 2-letter (PL).
  Greece: WEO uses GRC → Eurostat uses EL (used here for consistency).

  Projection rows (is_projection = TRUE, year >= 2026) are included.
  obs_status: 'p' (projection) or NULL (actual), consistent with Eurostat flag convention.
*/

with weo as (

    select
        weo_subject,
        iso_code,
        year,
        value,
        is_projection,
        weo_edition,
        fetched_at
    from {{ source('raw', 'imf_weo') }}
    where value is not null

),

mapped as (

    select
        'imf'               as source_id,
        'PUB'               as domain_id,

        case weo_subject
            when 'GGXCNL_NGDP'  then 'pub.fiscal_balance_imf'
            when 'GGXONLB_NGDP' then 'pub.primary_balance_imf'
            when 'GGSB_NPGDP'   then 'pub.structural_balance_imf'
            when 'GGXWDG_NGDP'  then 'pub.gross_debt_imf'
            when 'GGXWDN_NGDP'  then 'pub.net_debt_imf'
            when 'GGR_NGDP'     then 'pub.revenue_imf'
            when 'GGX_NGDP'     then 'pub.expenditure_imf'
        end                 as detail_id,

        -- Map WEO 3-letter ISO codes to 2-letter codes used in Eurostat convention
        case iso_code
            when 'AUT' then 'AT'
            when 'BEL' then 'BE'
            when 'BGR' then 'BG'
            when 'CYP' then 'CY'
            when 'CZE' then 'CZ'
            when 'DEU' then 'DE'
            when 'DNK' then 'DK'
            when 'ESP' then 'ES'
            when 'EST' then 'EE'
            when 'FIN' then 'FI'
            when 'FRA' then 'FR'
            when 'GRC' then 'EL'
            when 'HRV' then 'HR'
            when 'HUN' then 'HU'
            when 'IRL' then 'IE'
            when 'ITA' then 'IT'
            when 'LTU' then 'LT'
            when 'LUX' then 'LU'
            when 'LVA' then 'LV'
            when 'MLT' then 'MT'
            when 'NLD' then 'NL'
            when 'POL' then 'PL'
            when 'PRT' then 'PT'
            when 'ROU' then 'RO'
            when 'SVK' then 'SK'
            when 'SVN' then 'SI'
            when 'SWE' then 'SE'
            else iso_code
        end                 as geo,

        cast(year || '-01-01' as date) as period_date,

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

        case weo_subject
            when 'GGR_NGDP'     then 'Revenue'
            when 'GGX_NGDP'     then 'Expenditure'
            when 'GGXCNL_NGDP'  then 'Balance'
            when 'GGXONLB_NGDP' then 'Balance'
            when 'GGSB_NPGDP'   then 'Balance'
            when 'GGXWDG_NGDP'  then 'Debt'
            when 'GGXWDN_NGDP'  then 'Debt'
        end                 as dim_resources_uses,

        null::varchar       as dim_transport_mode,
        null::varchar       as dim_accommodation_type,

        weo.value           as value,
        case when weo.is_projection then 'p' end as obs_status,
        weo.fetched_at      as fetched_at,
        current_timestamp   as updated_at

    from weo

)

select * from mapped
where detail_id is not null
