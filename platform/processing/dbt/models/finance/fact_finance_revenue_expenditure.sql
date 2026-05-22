{{
    config(materialized='table', schema='curated')
}}

/*
  Wide annual fact: revenue and expenditure composition for the
  Dochody i wydatki page.

  Source: curated.mart_finance, Eurostat ESA 2010, General government
  sector. All values are % of GDP. One row per (geo, period_year).

  Revenue side (4 columns):
    - revenue_pct_gdp                ← pub.revenue_gdp
    - taxes_income_pct_gdp           ← pub.taxes_income_gdp
    - taxes_prod_imports_pct_gdp     ← pub.taxes_prod_imports_gdp
    - social_contributions_pct_gdp   ← pub.social_contributions_gdp

  Expenditure side (5 columns):
    - expenditure_pct_gdp            ← pub.expenditure_gdp
    - interest_expenditure_pct_gdp   ← pub.interest_expenditure_gdp
    - govt_investment_pct_gdp        ← pub.govt_investment_gdp
    - social_transfers_pct_gdp       ← pub.social_transfers_gdp
    - compensation_employees_pct_gdp ← pub.compensation_employees_gdp

  Star-schema joins: `geo` → dim_geo, `date_key` → dim_calendar
  (via period_date = December 31 of period_year).
*/

select
    geo,
    period_year,
    cast(period_year || '-12-31' as date) as period_date,

    -- Revenue side
    max(case when detail_id = 'pub.revenue_gdp'
                  and dim_govt_sector = 'General government'
             then value end) as revenue_pct_gdp,
    max(case when detail_id = 'pub.taxes_income_gdp'
                  and dim_govt_sector = 'General government'
             then value end) as taxes_income_pct_gdp,
    max(case when detail_id = 'pub.taxes_prod_imports_gdp'
                  and dim_govt_sector = 'General government'
             then value end) as taxes_prod_imports_pct_gdp,
    max(case when detail_id = 'pub.social_contributions_gdp'
                  and dim_govt_sector = 'General government'
             then value end) as social_contributions_pct_gdp,

    -- Expenditure side
    max(case when detail_id = 'pub.expenditure_gdp'
                  and dim_govt_sector = 'General government'
             then value end) as expenditure_pct_gdp,
    max(case when detail_id = 'pub.interest_expenditure_gdp'
                  and dim_govt_sector = 'General government'
             then value end) as interest_expenditure_pct_gdp,
    max(case when detail_id = 'pub.govt_investment_gdp'
                  and dim_govt_sector = 'General government'
             then value end) as govt_investment_pct_gdp,
    max(case when detail_id = 'pub.social_transfers_gdp'
                  and dim_govt_sector = 'General government'
             then value end) as social_transfers_pct_gdp,
    max(case when detail_id = 'pub.compensation_employees_gdp'
                  and dim_govt_sector = 'General government'
             then value end) as compensation_employees_pct_gdp

from {{ ref('mart_finance') }}
where source_id = 'eurostat'
  and value is not null
  and detail_id in (
      'pub.revenue_gdp',
      'pub.taxes_income_gdp',
      'pub.taxes_prod_imports_gdp',
      'pub.social_contributions_gdp',
      'pub.expenditure_gdp',
      'pub.interest_expenditure_gdp',
      'pub.govt_investment_gdp',
      'pub.social_transfers_gdp',
      'pub.compensation_employees_gdp'
  )
group by geo, period_year
