{{
    config(materialized='table', schema='curated')
}}

/*
  Intermediate: curated.int_finance_consolidated
  Domain: Public Finance (domain_id = 'PUB')

  Sources:
    - eurostat: Eurostat GFS (gov_10a_main, gov_10dd_edpt1, gov_10a_exp) — multi-country % GDP
    - imf:      IMF WEO fiscal indicators — 27 EU countries, 1980–2029 (includes projections)
    - dbw:      GUS DBW HVD — Poland-only, ESA 2010 compliant, PLN mn

  Key design decisions:
    - fiscal_category: domain hierarchy classifying each indicator into policy-relevant groups
    - country_name: EU country names mapped from 2-letter Eurostat codes (inline CASE)
    - is_poland / is_eu_aggregate: boolean flags for easy cross-country comparisons
    - is_projection: TRUE for IMF WEO forecast years (obs_status = 'p')
    - period_year: INTEGER year — all public finance data is annual
    - detail_unit: carried from dim_domain_detail for unit-aware dashboard queries
    - source_id kept: dashboard source-comparison tab distinguishes eurostat vs imf vs dbw
    - All 24 dim columns dropped except dim_govt_sector, dim_resources_uses (domain-relevant)

  Grain: one row per (source_id, detail_id, geo, period_year)
*/

with silver as (

    select
        source_id,
        domain_id,
        detail_id,
        geo,
        period_date,
        dim_govt_sector,
        dim_resources_uses,
        value,
        obs_status,
        fetched_at
    from {{ ref('all_indicators') }}
    where domain_id = 'PUB'
      and value is not null

),

details as (

    select
        detail_id,
        detail_name,
        detail_unit
    from {{ ref('dim_domain_detail') }}
    where domain_id = 'PUB'

),

joined as (

    select
        s.source_id,
        s.detail_id,
        d.detail_name,
        d.detail_unit,
        s.geo,

        -- Human-readable country name (EU-27 + aggregates + Poland)
        case s.geo
            when 'AT'          then 'Austria'
            when 'BE'          then 'Belgium'
            when 'BG'          then 'Bulgaria'
            when 'CY'          then 'Cyprus'
            when 'CZ'          then 'Czech Republic'
            when 'DE'          then 'Germany'
            when 'DK'          then 'Denmark'
            when 'EE'          then 'Estonia'
            when 'EL'          then 'Greece'
            when 'ES'          then 'Spain'
            when 'FI'          then 'Finland'
            when 'FR'          then 'France'
            when 'HR'          then 'Croatia'
            when 'HU'          then 'Hungary'
            when 'IE'          then 'Ireland'
            when 'IT'          then 'Italy'
            when 'LT'          then 'Lithuania'
            when 'LU'          then 'Luxembourg'
            when 'LV'          then 'Latvia'
            when 'MT'          then 'Malta'
            when 'NL'          then 'Netherlands'
            when 'PL'          then 'Poland'
            when 'PT'          then 'Portugal'
            when 'RO'          then 'Romania'
            when 'SE'          then 'Sweden'
            when 'SI'          then 'Slovenia'
            when 'SK'          then 'Slovakia'
            when 'EU27_2020'   then 'EU-27 Average'
            when 'EA20'        then 'Euro Area (EA-20)'
            when 'EA19'        then 'Euro Area (EA-19)'
            when 'EA21'        then 'Euro Area (EA-21)'
            when 'CH'          then 'Switzerland'
            when 'NO'          then 'Norway'
            when 'IS'          then 'Iceland'
            else s.geo
        end                    as country_name,

        -- Convenience flags for cross-country analysis
        (s.geo = 'PL')         as is_poland,
        (s.geo in ('EU27_2020', 'EA20', 'EA19', 'EA21')) as is_eu_aggregate,

        -- V4 group flag (Poland + Czech Republic + Slovakia + Hungary)
        (s.geo in ('PL', 'CZ', 'SK', 'HU')) as is_v4,

        extract(year from s.period_date)::integer as period_year,

        -- Fiscal policy category — domain hierarchy for grouping in charts
        case s.detail_id
            -- Fiscal balance
            when 'pub.fiscal_balance_gdp'       then 'Fiscal balance'
            when 'pub.fiscal_balance_imf'       then 'Fiscal balance'
            when 'pub.edp_deficit_gdp'          then 'Fiscal balance'
            when 'pub.net_lending_borrowing'    then 'Fiscal balance'
            -- Primary balance (excl. interest)
            when 'pub.primary_balance_imf'      then 'Primary balance'
            -- Structural/cyclically-adjusted balance
            when 'pub.structural_balance_imf'   then 'Structural balance'
            -- Government debt
            when 'pub.edp_debt_gdp'             then 'Government debt: gross'
            when 'pub.gross_debt_imf'           then 'Government debt: gross'
            when 'pub.public_debt_gdp'          then 'Government debt: gross'
            when 'pub.public_debt_total'        then 'Government debt: gross'
            when 'pub.net_debt_imf'             then 'Government debt: net'
            when 'pub.local_govt_debt'          then 'Government debt: local'
            when 'pub.public_debt_components'   then 'Government debt: composition'
            -- Total revenue and expenditure
            when 'pub.revenue_gdp'              then 'Total revenue'
            when 'pub.revenue_imf'              then 'Total revenue'
            when 'pub.govt_revenue'             then 'Total revenue'
            when 'pub.expenditure_gdp'          then 'Total expenditure'
            when 'pub.expenditure_imf'          then 'Total expenditure'
            when 'pub.govt_expenditure'         then 'Total expenditure'
            -- Revenue decomposition
            when 'pub.taxes_prod_imports_gdp'   then 'Revenue: taxes on production & imports'
            when 'pub.taxes_on_production_imports' then 'Revenue: taxes on production & imports'
            when 'pub.taxes_income_gdp'         then 'Revenue: taxes on income & wealth'
            when 'pub.taxes_on_income'          then 'Revenue: taxes on income & wealth'
            when 'pub.social_contributions_gdp' then 'Revenue: social contributions'
            when 'pub.net_social_contributions' then 'Revenue: social contributions'
            when 'pub.other_taxes_on_production' then 'Revenue: other taxes on production'
            when 'pub.market_output_govt'       then 'Revenue: market output'
            when 'pub.payments_for_nonmarket_output' then 'Revenue: payments for output'
            when 'pub.output_own_final_use'     then 'Revenue: output for own use'
            when 'pub.other_current_transfers'  then 'Revenue/expenditure: other transfers'
            -- Expenditure decomposition (ESA economic classification)
            when 'pub.interest_expenditure_gdp' then 'Expenditure: interest'
            when 'pub.property_income_govt'     then 'Expenditure: property income paid'
            when 'pub.govt_investment_gdp'      then 'Expenditure: investment (GFCF)'
            when 'pub.gross_capital_formation_govt' then 'Expenditure: investment (GFCF)'
            when 'pub.nonproduced_assets'       then 'Expenditure: non-produced assets'
            when 'pub.social_transfers_gdp'     then 'Expenditure: social transfers'
            when 'pub.social_benefits_in_kind'  then 'Expenditure: social transfers'
            when 'pub.social_transfers_in_kind' then 'Expenditure: social transfers'
            when 'pub.compensation_employees_gdp' then 'Expenditure: compensation of employees'
            when 'pub.compensation_of_employees_govt' then 'Expenditure: compensation of employees'
            when 'pub.intermediate_consumption_govt' then 'Expenditure: intermediate consumption'
            when 'pub.subsidies_esa'            then 'Expenditure: subsidies'
            when 'pub.capital_transfers_govt'   then 'Expenditure: capital transfers'
            -- COFOG functional classification
            when 'pub.cofog_01_gdp'             then 'COFOG: General public services'
            when 'pub.cofog_02_gdp'             then 'COFOG: Defence'
            when 'pub.cofog_03_gdp'             then 'COFOG: Public order & safety'
            when 'pub.cofog_04_gdp'             then 'COFOG: Economic affairs'
            when 'pub.cofog_05_gdp'             then 'COFOG: Environmental protection'
            when 'pub.cofog_06_gdp'             then 'COFOG: Housing'
            when 'pub.cofog_07_gdp'             then 'COFOG: Health'
            when 'pub.cofog_08_gdp'             then 'COFOG: Recreation & culture'
            when 'pub.cofog_09_gdp'             then 'COFOG: Education'
            when 'pub.cofog_10_gdp'             then 'COFOG: Social protection'
            -- State budget (Poland-specific, monthly GUS data)
            when 'pub.state_budget_balance'     then 'State budget: balance'
            when 'pub.state_budget_revenue'     then 'State budget: revenue'
            when 'pub.state_budget_expenditure' then 'State budget: expenditure'
            when 'pub.tax_revenue_vat'          then 'State budget: VAT revenue'
            when 'pub.tax_revenue_pit'          then 'State budget: PIT revenue'
            when 'pub.tax_revenue_cit'          then 'State budget: CIT revenue'
            when 'pub.tax_revenue_excise'       then 'State budget: excise revenue'
            -- Other Polish-specific
            when 'pub.bgk_guarantees'           then 'Off-budget: BGK guarantees'
            when 'pub.eu_funds_absorption'      then 'EU funds absorption'
            when 'pub.social_insurance_fund_balance' then 'Social security: FUS balance'
            else 'Other'
        end                    as fiscal_category,

        s.dim_govt_sector,
        s.dim_resources_uses,

        s.value,
        d.detail_unit          as unit,
        (s.obs_status = 'p')   as is_projection,
        s.obs_status,
        s.fetched_at

    from silver s
    inner join details d on s.detail_id = d.detail_id

)

select * from joined
