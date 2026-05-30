{{
    config(materialized='table', schema='curated')
}}

/*
  Wide pivot fact for the Science & R&D dashboard.

  Source: curated.sci_indicators (intermediate, domain_id = 'SCI').
  Pivots four Eurostat SCI series into a single (geo, period_year) annual grain.

  All series are annual.
  MAX collapses each (geo, period_year) to a single value — at most one
  non-null value per cell after the pivot.

  Grain: one row per (geo, period_year).

  Indicators:
    - rd_expenditure_pct_gdp ← sci.rd_expenditure_gdp / rd_e_gerdtot
                                (unit=PC_GDP — R&D expenditure as % of GDP, GERD)
    - rd_expenditure_total   ← sci.rd_expenditure_total / rd_e_gerdtot
                                (unit=MIO_EUR — R&D expenditure, millions of euros)
    - researchers_count      ← sci.researchers_count / rd_p_persocc
                                (unit=FTE — researchers in full-time equivalents)
    - patent_applications    ← sci.patent_applications / pat_ep_ntot
                                (unit=P_MHAB — EPO patent applications per million inhabitants)
*/

select
    geo,
    extract(year from period_date)::integer                                      as period_year,
    cast(cast(extract(year from period_date) as integer) || '-12-31' as date)   as period_date,

    max(case
            when detail_id = 'sci.rd_expenditure_gdp'
            then value
        end) as rd_expenditure_pct_gdp,

    max(case
            when detail_id = 'sci.rd_expenditure_total'
            then value
        end) as rd_expenditure_mio_eur,

    max(case
            when detail_id = 'sci.researchers_count'
            then value
        end) as researchers_fte,

    max(case
            when detail_id = 'sci.patent_applications'
            then value
        end) as patent_apps_per_mhab

from {{ ref('sci_indicators') }}
where value is not null
  and detail_id in (
      'sci.rd_expenditure_gdp',
      'sci.rd_expenditure_total',
      'sci.researchers_count',
      'sci.patent_applications'
  )
group by geo, extract(year from period_date)
