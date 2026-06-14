# Data domain taxonomy — grounded in statistical classifications

The **topic framework** for source discovery, built on the authoritative statistical
standards (ESA 2010 National Accounts + the EU/UN classification family) rather than
ad-hoc portal categories. Start from **GDP structure**, then branch by standard
classification. This is how GUS/Eurostat actually organise economic and social data,
so our domains map 1:1 to the series we'll ingest and stay EU-comparable.

---

## Apex: National Accounts (ESA 2010) — the GDP frame

GDP is measured three ways; each gives a branch of topics:

| Approach | Decomposition | Classification |
|---|---|---|
| **Production** | Gross value added **by economic activity** + taxes − subsidies | **NACE / PKD** (sections A–U) |
| **Expenditure** | household consumption · government consumption · gross capital formation (investment) · exports − imports | COICOP (consumption), trade nomenclatures |
| **Income** | compensation of employees · gross operating surplus · taxes − subsidies on production | — |
| **Sector accounts** | households · non-financial corporations · financial corporations · government · rest-of-world | ESA institutional sectors |

GDP is the root; everything below is a structured breakdown of it or a satellite.

---

## Backbone: economic activity — NACE Rev.2 / PKD 2025 (sections A–U)

The production structure of the economy. For each section we want: GVA, employment,
wages, enterprise demography, production/PRODCOM, prices (PPI).

| Sec | Activity | Sec | Activity |
|--|--|--|--|
| **A** | Agriculture, forestry & fishing | **L** | Real estate |
| **B** | Mining & quarrying | **M** | Professional, scientific & technical |
| **C** | Manufacturing | **N** | Administrative & support services |
| **D** | Energy supply | **O** | Public administration, defence, social security |
| **E** | Water, sewage, waste | **P** | Education |
| **F** | Construction | **Q** | Health & social work |
| **G** | Trade, vehicle repair | **R** | Arts, entertainment, recreation |
| **H** | Transport & storage | **S** | Other services |
| **I** | Accommodation & food service | **T** | Households as employers / own-use production |
| **J** | Information & communication | **U** | Extraterritorial organisations |
| **K** | Finance & insurance | | |

---

## Thematic statistical domains (each with its standard classification)

GDP/NACE covers economic *activity*; these are the cross-cutting statistical domains,
each anchored to an official classification so the data is structured, not ad-hoc:

| Domain | Standard classification | Key topics |
|---|---|---|
| **National accounts & GDP** | ESA 2010 | GDP, GVA, GNI, investment, savings, sector accounts |
| **Prices** | COICOP (consumer), PPI/CPA (producer) | CPI/HICP, inflation, PPI, construction prices |
| **Public finance** | **COFOG** | budget execution, expenditure by function, debt, deficit, taxes |
| **Labour market** | NACE × ISCO (occupations) × status | employment, unemployment, wages, hours, vacancies |
| **Foreign trade** | CN / HS / BEC | exports, imports, balance, by product & partner |
| **Business demography** | NACE | enterprises by size/activity, births/deaths, REGON |
| **Population & demography** | — (vital events) | population, births, deaths, migration, age structure |
| **Households** | COICOP | income, consumption, poverty, living conditions |
| **Health** | ICD-10/11, ICHA (health accounts) | morbidity, mortality, providers, spending, drugs |
| **Education** | **ISCED** | enrolment, levels, outcomes, R&D (Frascati) |
| **Environment & energy** | SEEA, energy balances, CRF (emissions) | air/water, waste, energy balance, emissions, climate |
| **Money & finance** | ESA financial accounts, MFI stats | money supply, rates, FX, credit, financial markets |
| **Government & justice** | COFOG + administrative | elections, legislation, courts, crime, public registers |
| **Regions** | NUTS / TERYT | all the above at regional/local level |

---

## How this drives source discovery

1. **Start from GDP** → its production breakdown is NACE A–U → for each section, which
   sources give GVA/employment/prices? (GUS BDL/DBW, Eurostat national accounts.)
2. **Each thematic domain** is anchored to a classification we already model or will
   (we use COFOG for public finance today; COICOP, ISCED, ICD, NACE next).
3. **Coverage = every (domain × classification breakdown) has a feeding source.**
   Gaps in that matrix are the source-hunting and product backlog.

This replaces the dane.gov.pl-category framing: classifications are authoritative,
stable, EU-comparable, and map directly onto the actual data series.

## Status
Taxonomy defined (classification-grounded). Next: tag sources with the domains they
serve and build a domain × source coverage matrix.
