{{
    config(materialized='table', schema='curated')
}}

/*
  Wide pivot fact for the Health dashboard.

  Source: curated.hlt_indicators (intermediate, domain_id = 'HLT').
  Pivots five Eurostat HLT series into a single (geo, period_year) annual grain.

  All series are annual.
  MAX collapses each (geo, period_year) to a single value — at most one
  non-null value per cell after the pivot.

  Grain: one row per (geo, period_year).

  Indicators:
    - life_expectancy_f_years  ← hlt.life_expectancy_f / demo_mlexpec
                                  (age=Y_LT1, sex=F, unit=YR — female life expectancy at birth)
    - life_expectancy_m_years  ← hlt.life_expectancy_m / demo_mlexpec
                                  (age=Y_LT1, sex=M, unit=YR — male life expectancy at birth)
    - infant_mortality_rt      ← hlt.infant_mortality_rate / demo_minfind
                                  (indic_de=INFMORRT, unit=RT — infant deaths per 1,000 live births)
    - hospital_beds_per_100k   ← hlt.hospital_bed_density / hlth_rs_bds
                                  (facility=HBEDT, unit=P_HTHAB — curative hospital beds per 100,000 inhabitants)
    - cardiovascular_deaths_nr ← hlt.cardiovascular_mortality / hlth_cd_anr
                                  (icd10=I, age=TOTAL, sex=T, unit=NR — cardiovascular disease deaths, absolute)
*/

select
    geo,
    extract(year from period_date)::integer                                      as period_year,
    cast(cast(extract(year from period_date) as integer) || '-12-31' as date)   as period_date,

    max(case
            when detail_id = 'hlt.life_expectancy_f'
            then value
        end) as life_expectancy_f_years,

    max(case
            when detail_id = 'hlt.life_expectancy_m'
            then value
        end) as life_expectancy_m_years,

    max(case
            when detail_id = 'hlt.infant_mortality_rate'
            then value
        end) as infant_mortality_rt,

    max(case
            when detail_id = 'hlt.hospital_bed_density'
            then value
        end) as hospital_beds_per_100k,

    max(case
            when detail_id = 'hlt.cardiovascular_mortality'
            then value
        end) as cardiovascular_deaths_nr

from {{ ref('hlt_indicators') }}
where value is not null
  and detail_id in (
      'hlt.life_expectancy_f',
      'hlt.life_expectancy_m',
      'hlt.infant_mortality_rate',
      'hlt.hospital_bed_density',
      'hlt.cardiovascular_mortality'
  )
group by geo, extract(year from period_date)
