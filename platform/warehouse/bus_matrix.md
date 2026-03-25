# Kimball Bus Matrix — Open Reporting

Maps every domain detail (fact) to the conformed dimensions it uses.

## Conformed Dimensions

| ID | Dimension | DuckDB Table | Description |
|----|-----------|--------------|-------------|
| D1 | Date | `dim_date` | Calendar hierarchy: year, quarter, month, week, day |
| D2 | Geography | `dim_geography` | TERYT hierarchy: national → voivodeship → powiat → gmina |
| D3 | Sector | `dim_sector` | NACE/PKD industry classification (sections, divisions, groups) |
| D4 | Company | `dim_company` | Legal entities: KRS number, NIP, exchange ticker, name |
| D5 | Demographic | `dim_demographic` | Age group, gender, education level, citizenship |
| D6 | Commodity | `dim_commodity` | Energy type, agricultural product, financial instrument |
| D7 | Institution | `dim_institution` | Public bodies: ministries, courts, regulators, schools |

✓ = dimension applies | — = not applicable

---

## FIN — Financial Markets

| Detail ID | Name | Type | D1 Date | D2 Geo | D3 Sector | D4 Company | D5 Demo | D6 Commodity | D7 Institution |
|-----------|------|------|:-------:|:------:|:---------:|:----------:|:-------:|:------------:|:--------------:|
| fin.exchange_rate_usd_pln | USD/PLN Exchange Rate | indicator | ✓ | — | — | — | — | ✓ | — |
| fin.exchange_rate_eur_pln | EUR/PLN Exchange Rate | indicator | ✓ | — | — | — | — | ✓ | — |
| fin.exchange_rate_chf_pln | CHF/PLN Exchange Rate | indicator | ✓ | — | — | — | — | ✓ | — |
| fin.exchange_rate_gbp_pln | GBP/PLN Exchange Rate | indicator | ✓ | — | — | — | — | ✓ | — |
| fin.reference_rate | NBP Reference Rate | indicator | ✓ | — | — | — | — | — | ✓ |
| fin.wibor_1m | WIBOR 1M | indicator | ✓ | — | — | — | — | — | — |
| fin.wibor_3m | WIBOR 3M | indicator | ✓ | — | — | — | — | — | — |
| fin.wibor_6m | WIBOR 6M | indicator | ✓ | — | — | — | — | — | — |
| fin.wig20_index | WIG20 Index | indicator | ✓ | — | — | — | — | — | — |
| fin.wig_index | WIG Total Return Index | indicator | ✓ | — | — | — | — | — | — |
| fin.bond_yield_10y | 10Y Government Bond Yield | indicator | ✓ | — | — | — | — | — | — |
| fin.bond_yield_2y | 2Y Government Bond Yield | indicator | ✓ | — | — | — | — | — | — |
| fin.banking_npl_ratio | Banking Sector NPL Ratio | indicator | ✓ | — | ✓ | — | — | — | ✓ |
| fin.banking_capital_ratio | Banking Sector Capital Adequacy Ratio | indicator | ✓ | — | ✓ | — | — | — | ✓ |
| fin.stock_price | Stock Price (GPW) | micro_indicator | ✓ | — | ✓ | ✓ | — | — | — |
| fin.stock_volume | Stock Trading Volume (GPW) | micro_indicator | ✓ | — | ✓ | ✓ | — | — | — |
| fin.tge_electricity_price | TGE Day-Ahead Electricity Price | indicator | ✓ | — | — | — | — | ✓ | — |

---

## PUB — Public Finance

| Detail ID | Name | Type | D1 Date | D2 Geo | D3 Sector | D4 Company | D5 Demo | D6 Commodity | D7 Institution |
|-----------|------|------|:-------:|:------:|:---------:|:----------:|:-------:|:------------:|:--------------:|
| pub.state_budget_revenue | State Budget Revenue | indicator | ✓ | — | — | — | — | — | ✓ |
| pub.state_budget_expenditure | State Budget Expenditure | indicator | ✓ | — | — | — | — | — | ✓ |
| pub.state_budget_balance | State Budget Balance | indicator | ✓ | — | — | — | — | — | ✓ |
| pub.public_debt_total | Total Public Debt (EDP) | indicator | ✓ | — | — | — | — | — | ✓ |
| pub.public_debt_gdp | Public Debt as % of GDP | indicator | ✓ | — | — | — | — | — | — |
| pub.tax_revenue_vat | VAT Revenue | indicator | ✓ | — | — | — | — | — | ✓ |
| pub.tax_revenue_pit | PIT Revenue | indicator | ✓ | — | — | — | — | — | ✓ |
| pub.tax_revenue_cit | CIT Revenue | indicator | ✓ | — | — | — | — | — | ✓ |
| pub.tax_revenue_excise | Excise Duty Revenue | indicator | ✓ | — | — | — | — | ✓ | ✓ |
| pub.eu_funds_absorption | EU Funds Absorption | indicator | ✓ | ✓ | — | — | — | — | ✓ |
| pub.local_govt_debt | Local Government Debt | indicator | ✓ | ✓ | — | — | — | — | ✓ |
| pub.bgk_guarantees | BGK Guarantee Portfolio | indicator | ✓ | — | ✓ | — | — | — | ✓ |
| pub.social_insurance_fund_balance | Social Insurance Fund Balance (FUS) | indicator | ✓ | — | — | — | — | — | ✓ |

---

## MAC — National Accounts & Macroeconomics

| Detail ID | Name | Type | D1 Date | D2 Geo | D3 Sector | D4 Company | D5 Demo | D6 Commodity | D7 Institution |
|-----------|------|------|:-------:|:------:|:---------:|:----------:|:-------:|:------------:|:--------------:|
| mac.gdp_real_growth | Real GDP Growth Rate | indicator | ✓ | — | — | — | — | — | — |
| mac.gdp_nominal | Nominal GDP | indicator | ✓ | — | — | — | — | — | — |
| mac.gdp_per_capita | GDP Per Capita | indicator | ✓ | — | — | — | — | — | — |
| mac.gdp_per_capita_regional | Regional GDP Per Capita | indicator | ✓ | ✓ | — | — | — | — | — |
| mac.household_consumption_growth | Household Consumption Growth | indicator | ✓ | — | — | — | — | — | — |
| mac.gross_fixed_capital_formation_growth | GFCF Growth | indicator | ✓ | — | — | — | — | — | — |
| mac.current_account_balance | Current Account Balance | indicator | ✓ | — | — | — | — | — | — |
| mac.current_account_gdp | Current Account as % of GDP | indicator | ✓ | — | — | — | — | — | — |
| mac.industrial_output_growth | Industrial Output Growth | indicator | ✓ | — | ✓ | — | — | — | — |
| mac.retail_sales_growth | Retail Sales Volume Growth | indicator | ✓ | — | ✓ | — | — | — | — |
| mac.business_confidence_bcs | Business Confidence Index (EC BCS) | indicator | ✓ | — | ✓ | — | — | — | — |
| mac.consumer_confidence | Consumer Confidence Index | indicator | ✓ | — | — | — | — | — | — |
| mac.pmi_manufacturing | Manufacturing PMI | indicator | ✓ | — | ✓ | — | — | — | — |

---

## PRC — Prices & Inflation

| Detail ID | Name | Type | D1 Date | D2 Geo | D3 Sector | D4 Company | D5 Demo | D6 Commodity | D7 Institution |
|-----------|------|------|:-------:|:------:|:---------:|:----------:|:-------:|:------------:|:--------------:|
| prc.cpi_total | CPI Headline Inflation | indicator | ✓ | — | — | — | — | — | — |
| prc.cpi_food | CPI Food & Non-Alcoholic Beverages | indicator | ✓ | — | — | — | — | ✓ | — |
| prc.cpi_energy | CPI Energy | indicator | ✓ | — | — | — | — | ✓ | — |
| prc.cpi_core | Core Inflation | indicator | ✓ | — | — | — | — | — | — |
| prc.ppi | Producer Price Index Growth | indicator | ✓ | — | — | — | — | — | — |
| prc.ppi_sectoral | PPI by Industry Section | indicator | ✓ | — | ✓ | — | — | — | — |
| prc.real_estate_price_national | Avg Residential Property Price (National) | indicator | ✓ | — | — | — | — | — | — |
| prc.real_estate_price_regional | Avg Residential Property Price (Regional) | indicator | ✓ | ✓ | — | — | — | — | — |
| prc.electricity_retail_price | Retail Electricity Price (Households) | indicator | ✓ | — | — | — | — | ✓ | — |
| prc.gas_retail_price | Retail Gas Price (Households) | indicator | ✓ | — | — | — | — | ✓ | — |
| prc.fuel_price_petrol | Retail Petrol Price (Pb95) | indicator | ✓ | — | — | — | — | ✓ | — |
| prc.fuel_price_diesel | Retail Diesel Price (ON) | indicator | ✓ | — | — | — | — | ✓ | — |

---

## LAB — Labour Market

| Detail ID | Name | Type | D1 Date | D2 Geo | D3 Sector | D4 Company | D5 Demo | D6 Commodity | D7 Institution |
|-----------|------|------|:-------:|:------:|:---------:|:----------:|:-------:|:------------:|:--------------:|
| lab.unemployment_rate | Registered Unemployment Rate | indicator | ✓ | — | — | — | — | — | — |
| lab.unemployment_rate_regional | Registered Unemployment Rate (Regional) | indicator | ✓ | ✓ | — | — | — | — | — |
| lab.unemployment_count | Registered Unemployed | indicator | ✓ | — | — | — | — | — | — |
| lab.employed_total | Total Employed (LFS) | indicator | ✓ | — | ✓ | — | ✓ | — | — |
| lab.employment_rate | Employment Rate 15-64 (LFS) | indicator | ✓ | — | — | — | ✓ | — | — |
| lab.activity_rate | Labour Force Participation Rate (LFS) | indicator | ✓ | — | — | — | ✓ | — | — |
| lab.average_wage | Average Gross Monthly Wage | indicator | ✓ | — | — | — | — | — | — |
| lab.average_wage_sectoral | Average Gross Wage by Sector | indicator | ✓ | — | ✓ | — | — | — | — |
| lab.wage_growth | Nominal Wage Growth | indicator | ✓ | — | — | — | — | — | — |
| lab.real_wage_growth | Real Wage Growth | indicator | ✓ | — | — | — | — | — | — |
| lab.job_vacancies | Job Vacancies | indicator | ✓ | — | ✓ | — | — | — | — |
| lab.vacancy_rate | Job Vacancy Rate | indicator | ✓ | — | ✓ | — | — | — | — |
| lab.youth_unemployment_rate | Youth Unemployment Rate (15-24) | indicator | ✓ | — | — | — | ✓ | — | — |
| lab.long_term_unemployment_share | Long-Term Unemployment Share | indicator | ✓ | — | — | — | ✓ | — | — |
| lab.minimum_wage | Statutory Minimum Wage | reference | ✓ | — | — | — | — | — | ✓ |

---

## BUS — Business & Industry

| Detail ID | Name | Type | D1 Date | D2 Geo | D3 Sector | D4 Company | D5 Demo | D6 Commodity | D7 Institution |
|-----------|------|------|:-------:|:------:|:---------:|:----------:|:-------:|:------------:|:--------------:|
| bus.company_registrations | New Company Registrations | indicator | ✓ | ✓ | ✓ | — | — | — | — |
| bus.company_deregistrations | Company Deregistrations | indicator | ✓ | ✓ | ✓ | — | — | — | — |
| bus.active_companies | Active Entities in REGON | indicator | ✓ | ✓ | ✓ | — | — | — | — |
| bus.company_registrations_sectoral | New Registrations by Sector | indicator | ✓ | — | ✓ | — | — | — | — |
| bus.construction_permits | Building Permits Issued | indicator | ✓ | ✓ | — | — | — | — | — |
| bus.construction_permits_area | Building Permits Floor Area | indicator | ✓ | ✓ | — | — | — | — | — |
| bus.construction_completions | Dwellings Completed | indicator | ✓ | ✓ | — | — | — | — | — |
| bus.industrial_output_sectoral | Industrial Output Index by Section | indicator | ✓ | — | ✓ | — | — | — | — |
| bus.construction_output_value | Construction Output Value | indicator | ✓ | — | ✓ | — | — | — | — |
| bus.pmi_manufacturing | Manufacturing PMI Poland | indicator | ✓ | — | ✓ | — | — | — | — |
| bus.enterprise_confidence | Enterprise Confidence Index (GUS) | indicator | ✓ | — | ✓ | — | — | — | — |
| bus.company_financials | Company Annual Financials (KRS) | micro_indicator | ✓ | ✓ | ✓ | ✓ | — | — | — |

---

## TRD — International Trade

| Detail ID | Name | Type | D1 Date | D2 Geo | D3 Sector | D4 Company | D5 Demo | D6 Commodity | D7 Institution |
|-----------|------|------|:-------:|:------:|:---------:|:----------:|:-------:|:------------:|:--------------:|
| trd.exports_goods_total | Total Goods Exports | indicator | ✓ | — | — | — | — | — | — |
| trd.imports_goods_total | Total Goods Imports | indicator | ✓ | — | — | — | — | — | — |
| trd.trade_balance_goods | Goods Trade Balance | indicator | ✓ | — | — | — | — | — | — |
| trd.exports_services | Services Exports | indicator | ✓ | — | ✓ | — | — | — | — |
| trd.imports_services | Services Imports | indicator | ✓ | — | ✓ | — | — | — | — |
| trd.exports_by_commodity | Goods Exports by Commodity Section | indicator | ✓ | — | — | — | — | ✓ | — |
| trd.imports_by_commodity | Goods Imports by Commodity Section | indicator | ✓ | — | — | — | — | ✓ | — |
| trd.exports_by_country | Goods Exports by Destination Country | indicator | ✓ | ✓ | — | — | — | — | — |
| trd.imports_by_country | Goods Imports by Origin Country | indicator | ✓ | ✓ | — | — | — | — | — |
| trd.fdi_inflows | FDI Inflows | indicator | ✓ | ✓ | ✓ | — | — | — | — |
| trd.fdi_outflows | FDI Outflows | indicator | ✓ | ✓ | ✓ | — | — | — | — |

---

## AGR — Agriculture & Forestry

| Detail ID | Name | Type | D1 Date | D2 Geo | D3 Sector | D4 Company | D5 Demo | D6 Commodity | D7 Institution |
|-----------|------|------|:-------:|:------:|:---------:|:----------:|:-------:|:------------:|:--------------:|
| agr.crop_production_cereals | Cereal Production | indicator | ✓ | ✓ | — | — | — | ✓ | — |
| agr.crop_production_rapeseed | Rapeseed Production | indicator | ✓ | ✓ | — | — | — | ✓ | — |
| agr.crop_area_arable | Arable Land Area | indicator | ✓ | ✓ | — | — | — | — | — |
| agr.livestock_cattle | Cattle Headcount | indicator | ✓ | ✓ | — | — | — | ✓ | — |
| agr.livestock_pigs | Pig Headcount | indicator | ✓ | ✓ | — | — | — | ✓ | — |
| agr.milk_production | Raw Cow's Milk Production | indicator | ✓ | ✓ | — | — | — | ✓ | — |
| agr.wheat_purchase_price | Wheat Purchase Price | indicator | ✓ | — | — | — | — | ✓ | — |
| agr.pig_purchase_price | Pig Purchase Price | indicator | ✓ | — | — | — | — | ✓ | — |
| agr.milk_purchase_price | Raw Milk Purchase Price | indicator | ✓ | — | — | — | — | ✓ | — |
| agr.timber_harvest | Timber Harvest Volume | indicator | ✓ | ✓ | — | — | — | ✓ | ✓ |
| agr.agricultural_area_used | Agricultural Land in Use | indicator | ✓ | ✓ | — | — | — | — | — |
| agr.soil_erosion_risk | Area at Risk of Water Erosion | indicator | ✓ | ✓ | — | — | — | — | — |

---

## TRP — Transport

| Detail ID | Name | Type | D1 Date | D2 Geo | D3 Sector | D4 Company | D5 Demo | D6 Commodity | D7 Institution |
|-----------|------|------|:-------:|:------:|:---------:|:----------:|:-------:|:------------:|:--------------:|
| trp.freight_rail_volume | Rail Freight Volume | indicator | ✓ | — | ✓ | — | — | ✓ | — |
| trp.passenger_rail_volume | Rail Passenger Volume | indicator | ✓ | ✓ | — | — | — | — | — |
| trp.freight_road_volume | Road Freight Volume | indicator | ✓ | — | ✓ | — | — | ✓ | — |
| trp.passenger_air_volume | Air Passenger Volume | indicator | ✓ | ✓ | — | — | — | — | — |
| trp.freight_air_volume | Air Freight Volume | indicator | ✓ | ✓ | — | — | — | ✓ | — |
| trp.vehicle_registrations | New Vehicle Registrations | indicator | ✓ | ✓ | — | — | — | ✓ | — |
| trp.road_accidents | Road Accidents | indicator | ✓ | ✓ | — | — | — | — | — |
| trp.road_fatalities | Road Fatalities | indicator | ✓ | ✓ | — | — | — | — | — |
| trp.motorway_expressway_length | Motorway and Expressway Network Length | indicator | ✓ | ✓ | — | — | — | — | — |
| trp.port_cargo_volume | Sea Port Cargo Volume | indicator | ✓ | ✓ | — | — | — | ✓ | — |

---

## ENE — Energy

| Detail ID | Name | Type | D1 Date | D2 Geo | D3 Sector | D4 Company | D5 Demo | D6 Commodity | D7 Institution |
|-----------|------|------|:-------:|:------:|:---------:|:----------:|:-------:|:------------:|:--------------:|
| ene.electricity_production_total | Total Electricity Production | indicator | ✓ | — | ✓ | — | — | ✓ | — |
| ene.electricity_consumption_total | Total Electricity Consumption | indicator | ✓ | — | ✓ | — | — | ✓ | — |
| ene.electricity_mix_coal | Hard Coal Share in Electricity Mix | indicator | ✓ | — | — | — | — | ✓ | — |
| ene.electricity_mix_lignite | Lignite Share in Electricity Mix | indicator | ✓ | — | — | — | — | ✓ | — |
| ene.electricity_mix_renewables | Total Renewables Share in Electricity Mix | indicator | ✓ | — | — | — | — | ✓ | — |
| ene.electricity_mix_wind | Wind Power Share in Electricity Mix | indicator | ✓ | — | — | — | — | ✓ | — |
| ene.electricity_mix_solar | Solar PV Share in Electricity Mix | indicator | ✓ | — | — | — | — | ✓ | — |
| ene.electricity_price_day_ahead | Day-Ahead Electricity Price (TGE BASE) | indicator | ✓ | — | — | — | — | ✓ | — |
| ene.natural_gas_consumption | Natural Gas Consumption | indicator | ✓ | — | ✓ | — | — | ✓ | — |
| ene.natural_gas_storage_level | Natural Gas Storage Level | indicator | ✓ | — | — | — | — | ✓ | — |
| ene.renewable_capacity_installed | Installed Renewable Capacity | indicator | ✓ | ✓ | — | — | — | ✓ | — |
| ene.wind_capacity_installed | Installed Wind Capacity | indicator | ✓ | ✓ | — | — | — | ✓ | — |
| ene.solar_capacity_installed | Installed Solar PV Capacity | indicator | ✓ | ✓ | — | — | — | ✓ | — |
| ene.energy_intensity | Energy Intensity of GDP | indicator | ✓ | — | — | — | — | — | — |

---

## POP — Population & Demographics

| Detail ID | Name | Type | D1 Date | D2 Geo | D3 Sector | D4 Company | D5 Demo | D6 Commodity | D7 Institution |
|-----------|------|------|:-------:|:------:|:---------:|:----------:|:-------:|:------------:|:--------------:|
| pop.population_total | Total Population | indicator | ✓ | — | — | — | — | — | — |
| pop.population_regional | Population by Voivodeship | indicator | ✓ | ✓ | — | — | — | — | — |
| pop.births | Live Births | indicator | ✓ | ✓ | — | — | — | — | — |
| pop.deaths | Deaths | indicator | ✓ | ✓ | — | — | — | — | — |
| pop.natural_increase | Natural Population Increase | indicator | ✓ | ✓ | — | — | — | — | — |
| pop.net_migration | Net International Migration | indicator | ✓ | — | — | — | ✓ | — | — |
| pop.life_expectancy_m | Male Life Expectancy at Birth | indicator | ✓ | ✓ | — | — | ✓ | — | — |
| pop.life_expectancy_f | Female Life Expectancy at Birth | indicator | ✓ | ✓ | — | — | ✓ | — | — |
| pop.fertility_rate | Total Fertility Rate | indicator | ✓ | ✓ | — | — | — | — | — |
| pop.median_age | Median Age of Population | indicator | ✓ | ✓ | — | — | ✓ | — | — |
| pop.old_age_dependency_ratio | Old-Age Dependency Ratio | indicator | ✓ | — | — | — | ✓ | — | — |
| pop.urbanisation_rate | Urban Population Share | indicator | ✓ | ✓ | — | — | — | — | — |

---

## HLT — Health

| Detail ID | Name | Type | D1 Date | D2 Geo | D3 Sector | D4 Company | D5 Demo | D6 Commodity | D7 Institution |
|-----------|------|------|:-------:|:------:|:---------:|:----------:|:-------:|:------------:|:--------------:|
| hlt.life_expectancy_m | Male Life Expectancy at Birth | indicator | ✓ | ✓ | — | — | ✓ | — | — |
| hlt.life_expectancy_f | Female Life Expectancy at Birth | indicator | ✓ | ✓ | — | — | ✓ | — | — |
| hlt.infant_mortality_rate | Infant Mortality Rate | indicator | ✓ | ✓ | — | — | — | — | — |
| hlt.cancer_incidence | Cancer Incidence Rate | indicator | ✓ | ✓ | — | — | ✓ | — | — |
| hlt.cardiovascular_mortality | Cardiovascular Disease Mortality Rate | indicator | ✓ | ✓ | — | — | ✓ | — | — |
| hlt.hospital_bed_density | Hospital Bed Density | indicator | ✓ | ✓ | — | — | — | — | ✓ |
| hlt.physician_density | Physicians per 1000 Population | indicator | ✓ | ✓ | — | — | — | — | ✓ |
| hlt.nfz_expenditure | NFZ Total Expenditure | indicator | ✓ | — | — | — | — | — | ✓ |
| hlt.vaccination_coverage_childhood | Childhood Vaccination Coverage (MMR) | indicator | ✓ | ✓ | — | — | ✓ | — | — |
| hlt.obesity_rate | Adult Obesity Prevalence | indicator | ✓ | — | — | — | ✓ | — | — |
| hlt.smoking_rate | Adult Smoking Prevalence | indicator | ✓ | — | — | — | ✓ | — | — |
| hlt.waiting_time_specialist | Avg Waiting Time for Specialist Care | indicator | ✓ | ✓ | — | — | — | — | ✓ |
| hlt.mental_health_hospitalisations | Mental Health Hospital Admissions | indicator | ✓ | ✓ | — | — | ✓ | — | ✓ |

---

## EDU — Education

| Detail ID | Name | Type | D1 Date | D2 Geo | D3 Sector | D4 Company | D5 Demo | D6 Commodity | D7 Institution |
|-----------|------|------|:-------:|:------:|:---------:|:----------:|:-------:|:------------:|:--------------:|
| edu.school_enrolment_primary | Primary School Enrolment | indicator | ✓ | ✓ | — | — | ✓ | — | ✓ |
| edu.school_enrolment_secondary | Secondary School Enrolment | indicator | ✓ | ✓ | — | — | ✓ | — | ✓ |
| edu.school_enrolment_tertiary | Tertiary Education Enrolment | indicator | ✓ | ✓ | — | — | ✓ | — | ✓ |
| edu.matura_pass_rate | Matura Exam Pass Rate | indicator | ✓ | ✓ | — | — | — | — | ✓ |
| edu.university_count | Active Higher Education Institutions | indicator | ✓ | ✓ | — | — | — | — | ✓ |
| edu.academic_staff_count | Academic Staff in Higher Education | indicator | ✓ | ✓ | — | — | ✓ | — | ✓ |
| edu.phd_candidates | PhD Candidates | indicator | ✓ | ✓ | — | — | ✓ | — | ✓ |
| edu.education_expenditure_gdp | Public Education Expenditure as % of GDP | indicator | ✓ | — | — | — | — | — | ✓ |
| edu.teachers_count | Employed Teachers (Primary + Secondary) | indicator | ✓ | ✓ | — | — | — | — | ✓ |
| edu.early_school_leavers | Early School Leavers Rate | indicator | ✓ | — | — | — | ✓ | — | — |
| edu.tertiary_attainment_rate | Tertiary Education Attainment Rate (30-34) | indicator | ✓ | — | — | — | ✓ | — | — |

---

## SOC — Income, Living Conditions & Social Protection

| Detail ID | Name | Type | D1 Date | D2 Geo | D3 Sector | D4 Company | D5 Demo | D6 Commodity | D7 Institution |
|-----------|------|------|:-------:|:------:|:---------:|:----------:|:-------:|:------------:|:--------------:|
| soc.household_income_avg | Avg Household Disposable Income per Capita | indicator | ✓ | ✓ | — | — | ✓ | — | — |
| soc.poverty_rate | At-Risk-of-Poverty Rate | indicator | ✓ | ✓ | — | — | ✓ | — | — |
| soc.severe_material_deprivation | Severe Material Deprivation Rate | indicator | ✓ | — | — | — | ✓ | — | — |
| soc.gini_coefficient | Gini Coefficient of Income Inequality | indicator | ✓ | — | — | — | — | — | — |
| soc.social_benefits_total | Total Social Benefits Paid | indicator | ✓ | — | — | — | — | — | ✓ |
| soc.pension_average | Average Monthly Pension (ZUS) | indicator | ✓ | — | — | — | ✓ | — | ✓ |
| soc.disability_benefit_recipients | Disability Benefit Recipients (PFRON) | indicator | ✓ | ✓ | — | — | ✓ | — | ✓ |
| soc.childcare_coverage_0_3 | Formal Childcare Coverage (0-3 years) | indicator | ✓ | ✓ | — | — | ✓ | — | — |
| soc.child_benefit_beneficiaries | Child Benefit (800+) Beneficiaries | indicator | ✓ | ✓ | — | — | ✓ | — | ✓ |
| soc.social_assistance_recipients | Social Assistance Recipients | indicator | ✓ | ✓ | — | — | ✓ | — | ✓ |
| soc.minimum_wage | National Minimum Wage | reference | ✓ | — | — | — | — | — | ✓ |

---

## CRM — Crime & Justice

| Detail ID | Name | Type | D1 Date | D2 Geo | D3 Sector | D4 Company | D5 Demo | D6 Commodity | D7 Institution |
|-----------|------|------|:-------:|:------:|:---------:|:----------:|:-------:|:------------:|:--------------:|
| crm.crime_total | Total Detected Crimes | indicator | ✓ | — | — | — | — | — | ✓ |
| crm.crime_rate | Crime Rate | indicator | ✓ | — | — | — | — | — | — |
| crm.crime_regional | Detected Crimes by Voivodeship | indicator | ✓ | ✓ | — | — | — | — | — |
| crm.violent_crime | Violent Crime Offences | indicator | ✓ | ✓ | — | — | — | — | — |
| crm.theft_total | Theft and Burglary Offences | indicator | ✓ | ✓ | — | — | — | — | — |
| crm.cybercrime | Cybercrime Offences | indicator | ✓ | — | — | — | — | — | — |
| crm.court_cases_filed | Court Cases Filed | indicator | ✓ | ✓ | — | — | — | — | ✓ |
| crm.court_cases_resolved | Court Cases Resolved | indicator | ✓ | ✓ | — | — | — | — | ✓ |
| crm.court_pending_backlog | Court Pending Case Backlog | indicator | ✓ | ✓ | — | — | — | — | ✓ |
| crm.prison_population | Prison Population | indicator | ✓ | ✓ | — | — | ✓ | — | ✓ |
| crm.road_accidents | Road Accidents | indicator | ✓ | ✓ | — | — | — | — | — |
| crm.domestic_violence_incidents | Domestic Violence Incidents | indicator | ✓ | ✓ | — | — | — | — | — |

---

## CLT — Culture, Tourism & Sport

| Detail ID | Name | Type | D1 Date | D2 Geo | D3 Sector | D4 Company | D5 Demo | D6 Commodity | D7 Institution |
|-----------|------|------|:-------:|:------:|:---------:|:----------:|:-------:|:------------:|:--------------:|
| clt.tourist_arrivals_intl | International Tourist Arrivals | indicator | ✓ | ✓ | — | — | — | — | — |
| clt.overnight_stays_domestic | Domestic Tourism Overnight Stays | indicator | ✓ | ✓ | — | — | — | — | — |
| clt.hotel_occupancy_rate | Hotel Bed Occupancy Rate | indicator | ✓ | ✓ | — | — | — | — | — |
| clt.museum_visits | Museum Visits | indicator | ✓ | ✓ | — | — | — | — | ✓ |
| clt.cinema_admissions | Cinema Admissions | indicator | ✓ | ✓ | — | — | — | — | — |
| clt.library_borrowings | Library Book Borrowings | indicator | ✓ | ✓ | — | — | — | — | ✓ |
| clt.tourism_revenue_intl | International Tourism Revenue | indicator | ✓ | ✓ | — | — | — | — | — |
| clt.culture_expenditure_gdp | Public Culture Expenditure as % of GDP | indicator | ✓ | — | — | — | — | — | ✓ |
| clt.sport_facilities_count | Sport Facilities Count | indicator | ✓ | ✓ | — | — | — | — | ✓ |

---

## ENV — Environment & Climate

| Detail ID | Name | Type | D1 Date | D2 Geo | D3 Sector | D4 Company | D5 Demo | D6 Commodity | D7 Institution |
|-----------|------|------|:-------:|:------:|:---------:|:----------:|:-------:|:------------:|:--------------:|
| env.pm25_annual_mean | PM2.5 Annual Mean Concentration | indicator | ✓ | ✓ | — | — | — | — | — |
| env.pm10_annual_mean | PM10 Annual Mean Concentration | indicator | ✓ | ✓ | — | — | — | — | — |
| env.pm25_station | PM2.5 Hourly Measurement (Station) | micro_indicator | ✓ | ✓ | — | — | — | — | — |
| env.ghg_emissions_total | Total GHG Emissions | indicator | ✓ | — | — | — | — | — | — |
| env.ghg_emissions_sectoral | GHG Emissions by Sector | indicator | ✓ | — | ✓ | — | — | — | — |
| env.renewable_energy_share | Renewable Energy Share in Final Consumption | indicator | ✓ | — | — | — | — | ✓ | — |
| env.forest_area | Forest Area | indicator | ✓ | ✓ | — | — | — | — | — |
| env.municipal_waste_generated | Municipal Waste Generated Per Capita | indicator | ✓ | ✓ | — | — | — | — | — |
| env.municipal_waste_recycling_rate | Municipal Waste Recycling Rate | indicator | ✓ | ✓ | — | — | — | — | — |
| env.water_abstractions | Freshwater Abstractions | indicator | ✓ | ✓ | ✓ | — | — | — | — |
| env.temperature_anomaly | Annual Mean Temperature Anomaly | indicator | ✓ | ✓ | — | — | — | — | — |
| env.precipitation_anomaly | Annual Precipitation Anomaly | indicator | ✓ | ✓ | — | — | — | — | — |
| env.bathing_water_quality | Excellent Bathing Water Quality Share | indicator | ✓ | ✓ | — | — | — | — | — |
| env.air_quality_index_cities | Air Quality Index — Major Cities | indicator | ✓ | ✓ | — | — | — | — | — |

---

## SCI — Science, Technology & Digital Society

| Detail ID | Name | Type | D1 Date | D2 Geo | D3 Sector | D4 Company | D5 Demo | D6 Commodity | D7 Institution |
|-----------|------|------|:-------:|:------:|:---------:|:----------:|:-------:|:------------:|:--------------:|
| sci.rd_expenditure_gdp | R&D Expenditure as % of GDP | indicator | ✓ | — | ✓ | — | — | — | — |
| sci.rd_expenditure_total | Total R&D Expenditure (GERD) | indicator | ✓ | — | ✓ | — | — | — | — |
| sci.researchers_count | Researchers (FTE) | indicator | ✓ | — | ✓ | — | — | — | ✓ |
| sci.patent_applications | Patent Applications (UPRP + EPO) | indicator | ✓ | — | ✓ | — | — | — | — |
| sci.ncn_grants_awarded | NCN Research Grants Awarded | indicator | ✓ | — | ✓ | — | — | — | ✓ |
| sci.broadband_coverage | Broadband Coverage ≥30 Mbps | indicator | ✓ | ✓ | — | — | — | — | — |
| sci.internet_usage_rate | Internet Usage Rate (16-74) | indicator | ✓ | — | — | — | ✓ | — | — |
| sci.ecommerce_participation | E-Commerce Participation (Individuals) | indicator | ✓ | — | — | — | ✓ | — | — |
| sci.mobile_subscriptions | Mobile Subscriptions per 100 Persons | indicator | ✓ | — | — | — | — | — | — |
| sci.digital_public_services | Digital Public Services Usage Rate | indicator | ✓ | — | — | — | ✓ | — | ✓ |
| sci.cybersecurity_incidents | CERT/NASK Reported Incidents | indicator | ✓ | — | — | — | — | — | ✓ |
