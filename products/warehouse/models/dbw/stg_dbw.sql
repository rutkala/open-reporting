{{
    config(materialized='table', schema='curated')
}}

/*
  Staging: raw.dbw_observations → conformed indicators with named semantic dimension columns.

  Logic:
  1. Filters to period_id = 282 (annual data).
  2. Joins each observation dim slot (dim1_id ... dim3_id) to raw.dbw_positions
     using (section_id, position_id) to resolve label and dim_id (dimension type).
  3. Geographic dim_ids: 2, 4, 10, 78, 79, 679, 995, 1101 — whichever slot carries one of
     these becomes the geo column. The position_name is mapped to a NUTS code via CASE.
  4. Remaining slots are routed to 24 named semantic columns by dim_id — regardless of
     which raw slot they land in. This replaces the old EAV dim1/dim2/dim3/dim4 approach.
  5. variable_id is mapped to detail_id via an inline CASE expression.

  Output grain: one row per (variable_id, section_id, year, dim1_id, dim2_id, dim3_id).
  Conforms to the shared staging schema used by stg_eurostat and stg_nbp.
*/

with obs as (

    select
        o.variable_id,
        o.section_id,
        o.year,
        o.dim1_id,
        o.dim2_id,
        o.dim3_id,
        o.value,
        o.fetched_at,
        -- Resolve dim slot 1
        p1.dim_id    as dim1_type_id,
        p1.dim_name  as dim1_type_name,
        p1.position_name as dim1_pos_name,
        -- Resolve dim slot 2
        p2.dim_id    as dim2_type_id,
        p2.dim_name  as dim2_type_name,
        p2.position_name as dim2_pos_name,
        -- Resolve dim slot 3
        p3.dim_id    as dim3_type_id,
        p3.dim_name  as dim3_type_name,
        p3.position_name as dim3_pos_name
    from {{ source('raw', 'dbw_observations') }} o
    left join {{ source('raw', 'dbw_positions') }} p1
        on  p1.section_id  = o.section_id
        and p1.position_id = o.dim1_id
        and o.dim1_id      != 0
    left join {{ source('raw', 'dbw_positions') }} p2
        on  p2.section_id  = o.section_id
        and p2.position_id = o.dim2_id
        and o.dim2_id      != 0
    left join {{ source('raw', 'dbw_positions') }} p3
        on  p3.section_id  = o.section_id
        and p3.position_id = o.dim3_id
        and o.dim3_id      != 0
    where o.period_id = 282
      and o.value     is not null

),

/*
  Geographic dim_ids in the positions table:
    2    = Poland (national only)
    4    = Poland, voivodeships (NUTS 2)
    10   = Poland, voivodships, poviats
    78   = Poland, macroregions, regions, subregions (NUTS 0-3)
    79   = Poland, macroregions, regions (NUTS 0-2)
    679  = Poland, Regions (NUTS 2)
    995  = Poland, macroregions, voivodships, regions (NUTS 0-2)
    1101 = Poland, NUTS regions
*/

classified as (

    select
        o.*,

        -- Identify which dim slot carries the geographic position
        case
            when o.dim1_type_id in (2, 4, 10, 78, 79, 679, 995, 1101) then 1
            when o.dim2_type_id in (2, 4, 10, 78, 79, 679, 995, 1101) then 2
            when o.dim3_type_id in (2, 4, 10, 78, 79, 679, 995, 1101) then 3
            else null
        end as geo_slot,

        -- Extract the raw position_name for the geo slot
        case
            when o.dim1_type_id in (2, 4, 10, 78, 79, 679, 995, 1101) then o.dim1_pos_name
            when o.dim2_type_id in (2, 4, 10, 78, 79, 679, 995, 1101) then o.dim2_pos_name
            when o.dim3_type_id in (2, 4, 10, 78, 79, 679, 995, 1101) then o.dim3_pos_name
            else null
        end as geo_raw_name

    from obs o

),

mapped as (

    select
        c.*,

        -- Map geo position_name to NUTS code
        -- Voivodeships (bare names, dim_name = 'Poland, voivodeships' or 'Poland, macroregions, voivodships, regions')
        case c.geo_raw_name
            when 'POLAND'                    then 'PL'
            when 'POLSKA'                    then 'PL'
            -- bare voivodeship names
            when 'DOLNOSLASKIE'              then 'PL51'
            when 'KUJAWSKO-POMORSKIE'        then 'PL61'
            when 'LUBELSKIE'                 then 'PL81'
            when 'LUBUSKIE'                  then 'PL43'
            when 'LODZKIE'                   then 'PL71'
            when 'MALOPOLSKIE'               then 'PL21'
            when 'MAZOWIECKIE'               then 'PL91'
            when 'OPOLSKIE'                  then 'PL52'
            when 'PODKARPACKIE'              then 'PL82'
            when 'PODLASKIE'                 then 'PL84'
            when 'POMORSKIE'                 then 'PL63'
            when 'SLASKIE'                   then 'PL22'
            when 'SWIETOKRZYSKIE'            then 'PL72'
            when 'WARMINSKO-MAZURSKIE'       then 'PL62'
            when 'WIELKOPOLSKIE'             then 'PL41'
            when 'ZACHODNIOPOMORSKIE'        then 'PL42'
            -- REGION prefix (dim_name = 'Poland, Regions' or 'Poland, macroregions, regions, subregions')
            when 'REGION DOLNOSLASKIE'       then 'PL51'
            when 'REGION KUJAWSKO-POMORSKIE' then 'PL61'
            when 'REGION LUBELSKIE'          then 'PL81'
            when 'REGION LUBUSKIE'           then 'PL43'
            when 'REGION LODZKIE'            then 'PL71'
            when 'REGION MALOPOLSKIE'        then 'PL21'
            when 'REGION MAZOWIECKI REGIONAL' then 'PL92'
            when 'REGION OPOLSKIE'           then 'PL52'
            when 'REGION PODKARPACKIE'       then 'PL82'
            when 'REGION PODLASKIE'          then 'PL84'
            when 'REGION POMORSKIE'          then 'PL63'
            when 'REGION SLASKIE'            then 'PL22'
            when 'REGION SWIETOKRZYSKIE'     then 'PL72'
            when 'REGION WARMINSKO-MAZURSKIE' then 'PL62'
            when 'REGION WARSAW CAPITAL'     then 'PL91'
            when 'REGION WIELKOPOLSKIE'      then 'PL41'
            when 'REGION ZACHODNIOPOMORSKIE' then 'PL42'
            -- Macroregions
            when 'MAKROREGION SOUTH'         then 'PL2'
            when 'MAKROREGION NORTH'         then 'PL6'
            when 'MAKROREGION CENTRAL'       then 'PL7'
            when 'MAKROREGION EASTERN'       then 'PL8'
            when 'MAKROREGION NORTH WEST'    then 'PL4'
            when 'MAKROREGION SOUTH WEST'    then 'PL5'
            when 'MAKROREGION MAZOVIA VOIVODESHIP' then 'PL9'
            else null
        end as geo_nuts,

        -- Map variable_id to detail_id
        case c.variable_id
            -- Unemployment
            when 1514 then 'lab.unemployment_rate'
            when 1618 then 'lab.long_term_unemployment_rate_lfs'
            -- Employment
            when 1513 then 'lab.employment_rate_regional'
            when 1617 then 'lab.part_time_employment_share'
            -- Potential labour force
            when 1518 then 'lab.economically_inactive_available'
            when 1519 then 'lab.economically_inactive_seeking'
            -- Population
            when 593  then 'pop.infant_mortality_rate'
            when 961  then 'pop.life_expectancy_by_age'
            when 1593 then 'pop.median_age_regional'
            when 1594 then 'pop.birth_rate'
            when 1595 then 'pop.fertility_rate_by_age'
            when 1596 then 'pop.fertility_rate'
            when 1597 then 'pop.death_rate'
            when 1600 then 'pop.usual_residence_population'
            when 1601 then 'pop.old_age_dependency_ratio_regional'
            -- GDP & national accounts
            when 1038 then 'mac.gdp_nominal'
            when 1173 then 'mac.gdp_regional'
            when 1022 then 'mac.gni'
            when 1044 then 'mac.gva_sectoral'
            when 1174 then 'mac.gva_regional'
            when 1036 then 'mac.employment_esa'
            when 1659 then 'mac.employment_esa_regional'
            when 1172 then 'mac.compensation_of_employees_regional'
            when 1026 then 'mac.compensation_of_employees'
            when 1198 then 'mac.gross_fixed_capital_formation'
            when 1660 then 'mac.gross_fixed_capital_formation_regional'
            when 1391 then 'mac.household_final_consumption'
            when 1028 then 'mac.gross_operating_surplus'
            when 1021 then 'mac.gross_disposable_income'
            when 1029 then 'mac.gross_saving'
            when 1588 then 'mac.net_disposable_income_regional'
            -- PRODCOM industrial production
            when 1589 then 'mac.prodcom_sold'
            when 1590 then 'mac.prodcom_subcontracted'
            when 1591 then 'mac.prodcom_actual'
            when 1581 then 'mac.volume_of_sales_by_activity'
            -- Public debt
            when 1061 then 'pub.public_debt_total'
            when 1401 then 'pub.public_debt_components'
            when 1402 then 'pub.public_debt_components'
            when 1403 then 'pub.public_debt_components'
            -- Government expenditure and revenue
            when 1019 then 'pub.gross_capital_formation_govt'
            when 1030 then 'pub.taxes_on_income'
            when 1033 then 'pub.taxes_on_production_imports'
            when 1045 then 'pub.intermediate_consumption_govt'
            when 1062 then 'pub.govt_revenue'
            when 1064 then 'pub.govt_expenditure'
            when 1065 then 'pub.subsidies_esa'
            when 1394 then 'pub.property_income_govt'
            when 1396 then 'pub.other_taxes_on_production'
            when 1397 then 'pub.payments_for_nonmarket_output'
            when 1398 then 'pub.social_benefits_in_kind'
            when 1399 then 'pub.social_transfers_in_kind'
            when 1400 then 'pub.nonproduced_assets'
            when 1406 then 'pub.other_current_transfers'
            when 1407 then 'pub.capital_transfers_govt'
            when 1408 then 'pub.net_social_contributions'
            when 1582 then 'pub.net_lending_borrowing'
            when 1670 then 'pub.market_output_govt'
            when 1671 then 'pub.output_own_final_use'
            -- Healthcare
            when 1681 then 'hlt.healthcare_expenditure_by_function'
            -- HICP
            when 1672 then 'prc.ooh_price_index'
            when 1673 then 'prc.hicp_constant_tax'
            when 1674 then 'prc.cpi_total'
            -- Producer prices
            when 1667 then 'prc.producer_prices_industry'
            when 1668 then 'prc.service_producer_prices'
            when 1669 then 'prc.construction_producer_prices'
            -- Environment
            when 1613 then 'env.air_pollutants_aea'
            when 1621 then 'env.landfill_closed'
            when 1622 then 'env.landfill_capacity'
            when 1623 then 'env.landfill_facilities'
            when 1624 then 'env.recovery_incineration_capacity'
            when 1625 then 'env.recovery_incineration_facilities'
            when 1626 then 'env.waste_treated_by_category'
            when 1627 then 'env.waste_generated_by_category'
            -- Tourism
            when 94   then 'clt.overnight_stays_regional'
            when 1584 then 'clt.tourism_participation_rate'
            when 1585 then 'clt.tourism_trips'
            when 1586 then 'clt.tourism_nights_spent'
            when 1587 then 'clt.tourism_expenditure'
            -- Inequality / poverty
            when 1607 then 'soc.income_quintile_ratio'
            when 1608 then 'soc.gini_coefficient_dbw'
            when 527  then 'soc.at_risk_poverty_rate'
            when 1603 then 'soc.arope_rate'
            when 1604 then 'soc.severe_material_deprivation_rate'
            when 1605 then 'soc.material_deprivation_rate'
            when 1606 then 'soc.low_work_intensity_rate'
            else null
        end as detail_id_mapped,

        -- Domain lookup (derived from detail_id prefix)
        case c.variable_id
            when 1514 then 'LAB'
            when 1618 then 'LAB'
            when 1513 then 'LAB'
            when 1617 then 'LAB'
            when 1518 then 'LAB'
            when 1519 then 'LAB'
            when 593  then 'POP'
            when 961  then 'POP'
            when 1593 then 'POP'
            when 1594 then 'POP'
            when 1595 then 'POP'
            when 1596 then 'POP'
            when 1597 then 'POP'
            when 1600 then 'POP'
            when 1601 then 'POP'
            when 1038 then 'MAC'
            when 1173 then 'MAC'
            when 1022 then 'MAC'
            when 1044 then 'MAC'
            when 1174 then 'MAC'
            when 1036 then 'MAC'
            when 1659 then 'MAC'
            when 1172 then 'MAC'
            when 1026 then 'MAC'
            when 1198 then 'MAC'
            when 1660 then 'MAC'
            when 1391 then 'MAC'
            when 1028 then 'MAC'
            when 1021 then 'MAC'
            when 1029 then 'MAC'
            when 1588 then 'MAC'
            when 1589 then 'MAC'
            when 1590 then 'MAC'
            when 1591 then 'MAC'
            when 1581 then 'MAC'
            when 1061 then 'PUB'
            when 1401 then 'PUB'
            when 1402 then 'PUB'
            when 1403 then 'PUB'
            when 1019 then 'PUB'
            when 1030 then 'PUB'
            when 1033 then 'PUB'
            when 1045 then 'PUB'
            when 1062 then 'PUB'
            when 1064 then 'PUB'
            when 1065 then 'PUB'
            when 1394 then 'PUB'
            when 1396 then 'PUB'
            when 1397 then 'PUB'
            when 1398 then 'PUB'
            when 1399 then 'PUB'
            when 1400 then 'PUB'
            when 1406 then 'PUB'
            when 1407 then 'PUB'
            when 1408 then 'PUB'
            when 1582 then 'PUB'
            when 1670 then 'PUB'
            when 1671 then 'PUB'
            when 1681 then 'HLT'
            when 1672 then 'PRC'
            when 1673 then 'PRC'
            when 1674 then 'PRC'
            when 1667 then 'PRC'
            when 1668 then 'PRC'
            when 1669 then 'PRC'
            when 1613 then 'ENV'
            when 1621 then 'ENV'
            when 1622 then 'ENV'
            when 1623 then 'ENV'
            when 1624 then 'ENV'
            when 1625 then 'ENV'
            when 1626 then 'ENV'
            when 1627 then 'ENV'
            when 94   then 'CLT'
            when 1584 then 'CLT'
            when 1585 then 'CLT'
            when 1586 then 'CLT'
            when 1587 then 'CLT'
            when 1607 then 'SOC'
            when 1608 then 'SOC'
            when 527  then 'SOC'
            when 1603 then 'SOC'
            when 1604 then 'SOC'
            when 1605 then 'SOC'
            when 1606 then 'SOC'
            else null
        end as domain_id_mapped

    from classified c

),

final as (

    select
        'dbw'::varchar                  as source_id,
        m.domain_id_mapped              as domain_id,
        m.detail_id_mapped              as detail_id,
        -- Use NUTS code when available, otherwise keep raw position name for national-only vars
        coalesce(m.geo_nuts, case when m.geo_slot is not null then m.geo_raw_name else 'PL' end)
                                        as geo,
        cast(m.year::varchar || '-01-01' as date)
                                        as period_date,

        -- 24 named semantic dimension columns, routed by dim_id regardless of raw slot position
        case
            when m.dim1_type_id in (1, 67, 339) then m.dim1_pos_name
            when m.dim2_type_id in (1, 67, 339) then m.dim2_pos_name
            when m.dim3_type_id in (1, 67, 339) then m.dim3_pos_name
        end as dim_sex,

        case
            when m.dim1_type_id in (107, 239, 526, 960, 1050, 1052, 1064, 1065, 1087, 1092)
                then m.dim1_pos_name
            when m.dim2_type_id in (107, 239, 526, 960, 1050, 1052, 1064, 1065, 1087, 1092)
                then m.dim2_pos_name
            when m.dim3_type_id in (107, 239, 526, 960, 1050, 1052, 1064, 1065, 1087, 1092)
                then m.dim3_pos_name
        end as dim_age_group,

        case
            when m.dim1_type_id in (3, 1099, 1100) then m.dim1_pos_name
            when m.dim2_type_id in (3, 1099, 1100) then m.dim2_pos_name
            when m.dim3_type_id in (3, 1099, 1100) then m.dim3_pos_name
        end as dim_type_of_locality,

        case
            when m.dim1_type_id in (25, 855, 948, 949, 1041, 1044, 1051, 1053, 1063, 1069,
                                    1080, 1097, 1114, 1116, 1117, 1119, 1120, 1130)
                then m.dim1_pos_name
            when m.dim2_type_id in (25, 855, 948, 949, 1041, 1044, 1051, 1053, 1063, 1069,
                                    1080, 1097, 1114, 1116, 1117, 1119, 1120, 1130)
                then m.dim2_pos_name
            when m.dim3_type_id in (25, 855, 948, 949, 1041, 1044, 1051, 1053, 1063, 1069,
                                    1080, 1097, 1114, 1116, 1117, 1119, 1120, 1130)
                then m.dim3_pos_name
        end as dim_nace_sector,

        case
            when m.dim1_type_id in (1068, 1115, 1118, 1088) then m.dim1_pos_name
            when m.dim2_type_id in (1068, 1115, 1118, 1088) then m.dim2_pos_name
            when m.dim3_type_id in (1068, 1115, 1118, 1088) then m.dim3_pos_name
        end as dim_employment_status,

        case
            when m.dim1_type_id in (1066) then m.dim1_pos_name
            when m.dim2_type_id in (1066) then m.dim2_pos_name
            when m.dim3_type_id in (1066) then m.dim3_pos_name
        end as dim_education_level,

        case
            when m.dim1_type_id in (272, 435, 500, 501) then m.dim1_pos_name
            when m.dim2_type_id in (272, 435, 500, 501) then m.dim2_pos_name
            when m.dim3_type_id in (272, 435, 500, 501) then m.dim3_pos_name
        end as dim_prodcom_product,

        case
            when m.dim1_type_id in (1127, 1129) then m.dim1_pos_name
            when m.dim2_type_id in (1127, 1129) then m.dim2_pos_name
            when m.dim3_type_id in (1127, 1129) then m.dim3_pos_name
        end as dim_hicp_category,

        case
            when m.dim1_type_id in (1056, 1057, 1058) then m.dim1_pos_name
            when m.dim2_type_id in (1056, 1057, 1058) then m.dim2_pos_name
            when m.dim3_type_id in (1056, 1057, 1058) then m.dim3_pos_name
        end as dim_pollutant_type,

        case
            when m.dim1_type_id in (1077, 1078, 1079, 1081, 1082, 1083) then m.dim1_pos_name
            when m.dim2_type_id in (1077, 1078, 1079, 1081, 1082, 1083) then m.dim2_pos_name
            when m.dim3_type_id in (1077, 1078, 1079, 1081, 1082, 1083) then m.dim3_pos_name
        end as dim_waste_category,

        case
            when m.dim1_type_id in (1126) then m.dim1_pos_name
            when m.dim2_type_id in (1126) then m.dim2_pos_name
            when m.dim3_type_id in (1126) then m.dim3_pos_name
        end as dim_healthcare_function,

        case
            when m.dim1_type_id in (1125) then m.dim1_pos_name
            when m.dim2_type_id in (1125) then m.dim2_pos_name
            when m.dim3_type_id in (1125) then m.dim3_pos_name
        end as dim_health_provider,

        case
            when m.dim1_type_id in (1124) then m.dim1_pos_name
            when m.dim2_type_id in (1124) then m.dim2_pos_name
            when m.dim3_type_id in (1124) then m.dim3_pos_name
        end as dim_health_financing,

        case
            when m.dim1_type_id in (790, 880) then m.dim1_pos_name
            when m.dim2_type_id in (790, 880) then m.dim2_pos_name
            when m.dim3_type_id in (790, 880) then m.dim3_pos_name
        end as dim_govt_sector,

        case
            when m.dim1_type_id in (787, 809, 889) then m.dim1_pos_name
            when m.dim2_type_id in (787, 809, 889) then m.dim2_pos_name
            when m.dim3_type_id in (787, 809, 889) then m.dim3_pos_name
        end as dim_institutional_sector,

        case
            when m.dim1_type_id in (1086) then m.dim1_pos_name
            when m.dim2_type_id in (1086) then m.dim2_pos_name
            when m.dim3_type_id in (1086) then m.dim3_pos_name
        end as dim_asset_classification,

        case
            when m.dim1_type_id in (190) then m.dim1_pos_name
            when m.dim2_type_id in (190) then m.dim2_pos_name
            when m.dim3_type_id in (190) then m.dim3_pos_name
        end as dim_tourist_origin,

        case
            when m.dim1_type_id in (1045) then m.dim1_pos_name
            when m.dim2_type_id in (1045) then m.dim2_pos_name
            when m.dim3_type_id in (1045) then m.dim3_pos_name
        end as dim_trip_direction,

        case
            when m.dim1_type_id in (1046) then m.dim1_pos_name
            when m.dim2_type_id in (1046) then m.dim2_pos_name
            when m.dim3_type_id in (1046) then m.dim3_pos_name
        end as dim_trip_duration,

        case
            when m.dim1_type_id in (273) then m.dim1_pos_name
            when m.dim2_type_id in (273) then m.dim2_pos_name
            when m.dim3_type_id in (273) then m.dim3_pos_name
        end as dim_quintile_group,

        case
            when m.dim1_type_id in (1054, 1055, 1089, 1090) then m.dim1_pos_name
            when m.dim2_type_id in (1054, 1055, 1089, 1090) then m.dim2_pos_name
            when m.dim3_type_id in (1054, 1055, 1089, 1090) then m.dim3_pos_name
        end as dim_citizenship,

        case
            when m.dim1_type_id in (1018) then m.dim1_pos_name
            when m.dim2_type_id in (1018) then m.dim2_pos_name
            when m.dim3_type_id in (1018) then m.dim3_pos_name
        end as dim_resources_uses,

        case
            when m.dim1_type_id in (1049) then m.dim1_pos_name
            when m.dim2_type_id in (1049) then m.dim2_pos_name
            when m.dim3_type_id in (1049) then m.dim3_pos_name
        end as dim_transport_mode,

        case
            when m.dim1_type_id in (1047, 1048) then m.dim1_pos_name
            when m.dim2_type_id in (1047, 1048) then m.dim2_pos_name
            when m.dim3_type_id in (1047, 1048) then m.dim3_pos_name
        end as dim_accommodation_type,

        cast(m.value as double)         as value,
        null::varchar                   as obs_status,
        m.fetched_at                    as fetched_at,
        current_timestamp               as updated_at

    from mapped m
    where m.detail_id_mapped is not null
      and m.domain_id_mapped  is not null

)

select * from final
