{{
    config(materialized='table', schema='curated')
}}

/*
  Wide pivot fact for the Income & Living Conditions dashboard.

  Source: curated.soc_indicators (intermediate, domain_id = 'SOC').
  Pivots four Eurostat ILC series into a single (geo, period_year) annual grain.

  All series are annual. Poland-only (Eurostat ingestion fetched geo='PL'
  for these ILC datasets).
  MAX collapses each (geo, period_year) to a single value — at most one
  non-null value per cell after the pivot.

  Grain: one row per (geo, period_year).

  Indicators:
    - gini_coefficient        ← soc.gini_coefficient        / ilc_di12
                                (statinfo=GINI_HND — Gini of equivalised disposable
                                 income, 0–100 index; lower is more equal)
    - at_risk_poverty_pct     ← soc.poverty_rate            / ilc_li02
                                (indic_il=LI_R_MD60, unit=PC — at-risk-of-poverty
                                 rate, cut-off 60% of median equivalised income)
    - material_deprivation_pct ← soc.severe_material_deprivation / ilc_mddd11
                                (unit=PC — severe material deprivation rate;
                                 series ends 2020, SMD→SMSD methodology change)
    - median_income_eur       ← soc.median_income_eur       / ilc_di03
                                (indic_il=MED_E, unit=EUR — median equivalised
                                 net income, euro)
*/

select
    geo,
    extract(year from period_date)::integer                                      as period_year,
    cast(cast(extract(year from period_date) as integer) || '-12-31' as date)   as period_date,

    max(case
            when detail_id = 'soc.gini_coefficient'
            then value
        end) as gini_coefficient,

    max(case
            when detail_id = 'soc.poverty_rate'
            then value
        end) as at_risk_poverty_pct,

    max(case
            when detail_id = 'soc.severe_material_deprivation'
            then value
        end) as material_deprivation_pct,

    max(case
            when detail_id = 'soc.median_income_eur'
            then value
        end) as median_income_eur

from {{ ref('soc_indicators') }}
where value is not null
  and detail_id in (
      'soc.gini_coefficient',
      'soc.poverty_rate',
      'soc.severe_material_deprivation',
      'soc.median_income_eur'
  )
group by geo, extract(year from period_date)
