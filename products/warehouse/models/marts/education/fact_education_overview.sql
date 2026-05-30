{{
    config(materialized='table', schema='curated')
}}

/*
  Wide pivot fact for the Education dashboard.

  Source: curated.edu_indicators (intermediate, domain_id = 'EDU').
  Pivots four Eurostat EDU series into a single (geo, period_year) annual grain.

  All series are annual.
  MAX collapses each (geo, period_year) to a single value — at most one
  non-null value per cell after the pivot.

  Grain: one row per (geo, period_year).

  Indicators:
    - early_leavers_pct         ← edu.early_school_leavers / edat_lfse_14
                                   (age=Y18-24, sex=T, unit=PC, wstatus=POP — % early school leavers)
    - tertiary_attainment_pct   ← edu.tertiary_attainment_rate / edat_lfse_03
                                   (age=Y30-34, isced11=ED5-8, sex=T, unit=PC — % with tertiary education)
    - tertiary_enrolment_nr     ← edu.school_enrolment_tertiary / educ_uoe_enrt01
                                   (isced11=ED5-8, sector=TOT_SEC, sex=T, unit=NR, worktime=TOTAL — number of students)
    - phd_candidates_nr         ← edu.phd_candidates / educ_uoe_enrt01
                                   (isced11=ED8, sector=TOT_SEC, sex=T, unit=NR, worktime=TOTAL — PhD candidates)
*/

select
    geo,
    extract(year from period_date)::integer                                      as period_year,
    cast(cast(extract(year from period_date) as integer) || '-12-31' as date)   as period_date,

    max(case
            when detail_id = 'edu.early_school_leavers'
            then value
        end) as early_leavers_pct,

    max(case
            when detail_id = 'edu.tertiary_attainment_rate'
            then value
        end) as tertiary_attainment_pct,

    max(case
            when detail_id = 'edu.school_enrolment_tertiary'
            then value
        end) as tertiary_enrolment_nr,

    max(case
            when detail_id = 'edu.phd_candidates'
            then value
        end) as phd_candidates_nr

from {{ ref('edu_indicators') }}
where value is not null
  and detail_id in (
      'edu.early_school_leavers',
      'edu.tertiary_attainment_rate',
      'edu.school_enrolment_tertiary',
      'edu.phd_candidates'
  )
group by geo, extract(year from period_date)
