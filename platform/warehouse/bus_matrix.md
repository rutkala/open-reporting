# Kimball Bus Matrix — Open Reporting

Maps every domain detail (fact) to the conformed dimensions it uses.
Built incrementally as domain_details.csv is populated.

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

---

## Bus Matrix

✓ = dimension applies | — = not applicable

| Detail ID | Name | Domain | D1 Date | D2 Geo | D3 Sector | D4 Company | D5 Demo | D6 Commodity | D7 Institution |
|-----------|------|--------|:-------:|:------:|:---------:|:----------:|:-------:|:------------:|:--------------:|
| *to be populated domain by domain* | | | | | | | | | |

---

## FIN — Financial Markets

| Detail ID | Name | Type | D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|-----------|------|------|----|----|----|----|----|----|----|
| *pending* | | | | | | | | | |

## PUB — Public Finance

| Detail ID | Name | Type | D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|-----------|------|------|----|----|----|----|----|----|----|
| *pending* | | | | | | | | | |

## MAC — National Accounts & Macroeconomics

| Detail ID | Name | Type | D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|-----------|------|------|----|----|----|----|----|----|----|
| *pending* | | | | | | | | | |

## PRC — Prices & Inflation

| Detail ID | Name | Type | D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|-----------|------|------|----|----|----|----|----|----|----|
| *pending* | | | | | | | | | |

## LAB — Labour Market

| Detail ID | Name | Type | D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|-----------|------|------|----|----|----|----|----|----|----|
| *pending* | | | | | | | | | |

## BUS — Business & Industry

| Detail ID | Name | Type | D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|-----------|------|------|----|----|----|----|----|----|----|
| *pending* | | | | | | | | | |

## TRD — International Trade

| Detail ID | Name | Type | D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|-----------|------|------|----|----|----|----|----|----|----|
| *pending* | | | | | | | | | |

## AGR — Agriculture & Forestry

| Detail ID | Name | Type | D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|-----------|------|------|----|----|----|----|----|----|----|
| *pending* | | | | | | | | | |

## TRP — Transport

| Detail ID | Name | Type | D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|-----------|------|------|----|----|----|----|----|----|----|
| *pending* | | | | | | | | | |

## ENE — Energy

| Detail ID | Name | Type | D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|-----------|------|------|----|----|----|----|----|----|----|
| *pending* | | | | | | | | | |

## POP — Population & Demographics

| Detail ID | Name | Type | D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|-----------|------|------|----|----|----|----|----|----|----|
| *pending* | | | | | | | | | |

## HLT — Health

| Detail ID | Name | Type | D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|-----------|------|------|----|----|----|----|----|----|----|
| *pending* | | | | | | | | | |

## EDU — Education

| Detail ID | Name | Type | D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|-----------|------|------|----|----|----|----|----|----|----|
| *pending* | | | | | | | | | |

## SOC — Income, Living Conditions & Social Protection

| Detail ID | Name | Type | D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|-----------|------|------|----|----|----|----|----|----|----|
| *pending* | | | | | | | | | |

## CRM — Crime & Justice

| Detail ID | Name | Type | D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|-----------|------|------|----|----|----|----|----|----|----|
| *pending* | | | | | | | | | |

## CLT — Culture, Tourism & Sport

| Detail ID | Name | Type | D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|-----------|------|------|----|----|----|----|----|----|----|
| *pending* | | | | | | | | | |

## ENV — Environment & Climate

| Detail ID | Name | Type | D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|-----------|------|------|----|----|----|----|----|----|----|
| *pending* | | | | | | | | | |

## SCI — Science, Technology & Digital Society

| Detail ID | Name | Type | D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|-----------|------|------|----|----|----|----|----|----|----|
| *pending* | | | | | | | | | |
