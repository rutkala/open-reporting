{{
    config(materialized='table', schema='curated')
}}

/*
  Regional (NUTS2) macroeconomic fact for the voivodeship choropleth (OR-167).

  Source: curated.mac_indicators (intermediate, domain_id = 'MAC').
  Grain:  one row per (geo, period_year), restricted to Poland's 17 NUTS2
          voivodeship regions (geo_level = 'nuts2' in dim_geo — the seed is
          Poland-only, so this yields exactly the 17 PL2x…PL9x codes that
          match the bundled `poland_nuts2` GeoJSON NUTS_ID keys 1:1).

  Why a dedicated regional fact (not fact_macro_overview):
    fact_macro_overview is national grain (geo = country). Mixing NUTS2 rows
    into it would pollute every national metric. This fact is the NUTS2-grain
    surface the choropleth + ranked bar bind to.

  Measures:
    - gdp_per_capita_eur ← mac.gdp_per_capita_regional / Eurostat nama_10r_2gdp
                           (unit = EUR_HAB, current-price EUR per inhabitant).

  Aggregate / higher-level codes (PL, PL2, PL4 … NUTS0/NUTS1) are excluded by
  the geo_level = 'nuts2' join — guards against the silent-drop the choropleth
  warns about when a `geo` value has no GeoJSON feature.
*/

with nuts2 as (
    select geo
    from {{ ref('dim_geo') }}
    where geo_level = 'nuts2'
)

select
    a.geo,
    extract(year from a.period_date)::integer                                    as period_year,
    cast(cast(extract(year from a.period_date) as integer) || '-12-31' as date)  as period_date,

    max(case
            when a.detail_id = 'mac.gdp_per_capita_regional'
            then a.value
        end) as gdp_per_capita_eur

from {{ ref('mac_indicators') }} a
inner join nuts2 using (geo)
where a.value is not null
  and a.detail_id in (
      'mac.gdp_per_capita_regional'
  )
group by a.geo, extract(year from a.period_date)
