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
    - rd_expenditure_pct_gdp    ← sci.rd_expenditure_gdp / rd_e_gerdtot
                                   (unit=PC_GDP — R&D expenditure as % of GDP, GERD)
    - rd_expenditure_total      ← sci.rd_expenditure_total / rd_e_gerdtot
                                   (unit=MIO_EUR — R&D expenditure, millions of euros)
    - researchers_count         ← sci.researchers_count / rd_p_persocc
                                   (unit=FTE — researchers in full-time equivalents)
    - patent_applications       ← sci.patent_applications / pat_ep_ntot
                                   (unit=P_MHAB — EPO patent applications per million inhabitants)
    - internet_usage_rate_pct   ← sci.internet_usage_rate / isoc_ci_ifp_iu
                                   (ind_type=IND_TOTAL, indic_is=I_ILT12, unit=PC_IND — % individuals using internet in last 12 months)
    - digital_public_services_pct ← sci.digital_public_services / isoc_ci_ac_i
                                     (ind_type=IND_TOTAL, indic_is=I_IHIF, unit=PC_IND — % individuals using internet for public services)
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
        end) as patent_apps_per_mhab,

    max(case
            when detail_id = 'sci.internet_usage_rate'
            then value
        end) as internet_usage_rate_pct,

    max(case
            when detail_id = 'sci.digital_public_services'
            then value
        end) as digital_public_services_pct

from {{ ref('sci_indicators') }}
where value is not null
  and detail_id in (
      'sci.rd_expenditure_gdp',
      'sci.rd_expenditure_total',
      'sci.researchers_count',
      'sci.patent_applications',
      'sci.internet_usage_rate',
      'sci.digital_public_services'
  )
group by geo, extract(year from period_date)
