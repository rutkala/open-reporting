# Open Reporting — Domain Taxonomy

Based on: Eurostat Statistical Themes (2nd level) + GUS Obszary Tematyczne

Domains drive everything: portal sections, dashboard groupings, article categories, data pipelines, and Linear issue labels.

## How to read this

- **Domain** = primary category used across all products (portal navigation, article tags, Linear labels)
- **Eurostat theme** = which of the 9 top-level Eurostat themes it falls under
- **GUS equivalent** = matching Polish GUS "obszary tematyczne" for data sourcing
- **Subcategories** = specific topics within the domain (drive individual dashboards and pipelines)

---

## 1. Public Finance

| Field | Value |
|-------|-------|
| **Eurostat theme** | Economy and finance |
| **GUS equivalent** | Finanse publiczne |
| **Subcategories** | State budget (revenues, expenditures, deficit), regional budgets (voivodship), local government budgets, public debt, taxes, EU funds absorption |

## 2. National Accounts & Macroeconomics

| Field | Value |
|-------|-------|
| **Eurostat theme** | Economy and finance |
| **GUS equivalent** | Rachunki narodowe, Wskaźniki makroekonomiczne |
| **Subcategories** | GDP (national and per capita), GNI, economic growth, sector accounts, economic sentiment |

## 3. Prices & Inflation

| Field | Value |
|-------|-------|
| **Eurostat theme** | Economy and finance |
| **GUS equivalent** | Ceny |
| **Subcategories** | CPI, HICP, housing prices, purchasing power parities, consumer price indices by category |

## 4. Financial Markets

| Field | Value |
|-------|-------|
| **Eurostat theme** | Economy and finance |
| **GUS equivalent** | (NBP, GPW, KNF data) |
| **Subcategories** | Stock exchange (GPW — WIG20, mWIG40, sWIG80), interest rates (NBP), exchange rates, bond yields, banking sector |

## 5. Population & Demographics

| Field | Value |
|-------|-------|
| **Eurostat theme** | Population and social conditions |
| **GUS equivalent** | Ludność, Stan i struktura ludności |
| **Subcategories** | Population size and structure, age pyramid, birth/death rates, fertility, life expectancy, migration, urbanization |

## 6. Labour Market

| Field | Value |
|-------|-------|
| **Eurostat theme** | Population and social conditions |
| **GUS equivalent** | Rynek pracy, Wynagrodzenia |
| **Subcategories** | Employment, unemployment (registered and BAEL/LFS), wages (average, median, by sector), minimum wage, job vacancies, labour costs |

## 7. Health

| Field | Value |
|-------|-------|
| **Eurostat theme** | Population and social conditions |
| **GUS equivalent** | Ochrona zdrowia |
| **Subcategories** | Healthcare spending, hospital infrastructure, doctors/nurses per capita, causes of death, life expectancy, disease statistics, NFZ |

## 8. Education

| Field | Value |
|-------|-------|
| **Eurostat theme** | Population and social conditions |
| **GUS equivalent** | Edukacja |
| **Subcategories** | Schools, student numbers, graduation rates, exam results, education spending, PISA results |

## 9. Income, Living Conditions & Social Protection

| Field | Value |
|-------|-------|
| **Eurostat theme** | Population and social conditions |
| **GUS equivalent** | Warunki życia, Dochody i wydatki ludności, Pomoc społeczna |
| **Subcategories** | Household income, poverty rates, inequality (Gini), social transfers (800+, family benefits), housing conditions, pensions |

## 10. Crime & Justice

| Field | Value |
|-------|-------|
| **Eurostat theme** | Population and social conditions |
| **GUS equivalent** | Wymiar sprawiedliwości |
| **Subcategories** | Crime statistics (by type, by region), court cases, prison population, police data, road safety |

## 11. Culture, Tourism & Sport

| Field | Value |
|-------|-------|
| **Eurostat theme** | Population and social conditions |
| **GUS equivalent** | Kultura, Turystyka, Sport |
| **Subcategories** | Museums, theatres, cultural spending, tourist arrivals, sport participation, media |

## 12. Business & Industry

| Field | Value |
|-------|-------|
| **Eurostat theme** | Industry, trade, and services |
| **GUS equivalent** | Podmioty gospodarcze, Przemysł, Budownictwo |
| **Subcategories** | Enterprise statistics, business demography, industrial production, construction, business sentiment |

## 13. Agriculture & Forestry

| Field | Value |
|-------|-------|
| **Eurostat theme** | Agriculture, fisheries, and forestry |
| **GUS equivalent** | Rolnictwo, Leśnictwo |
| **Subcategories** | Crop production, livestock, agricultural prices, farm structure, forestry |

## 14. International Trade

| Field | Value |
|-------|-------|
| **Eurostat theme** | International trade |
| **GUS equivalent** | Handel zagraniczny |
| **Subcategories** | Imports/exports (by country, by commodity), trade balance, FDI |

## 15. Transport

| Field | Value |
|-------|-------|
| **Eurostat theme** | Transport |
| **GUS equivalent** | Transport |
| **Subcategories** | Road transport, railways, air transport, public transit, road accidents, infrastructure investment |

## 16. Environment & Climate

| Field | Value |
|-------|-------|
| **Eurostat theme** | Environment and energy |
| **GUS equivalent** | Środowisko |
| **Subcategories** | Air quality (PM2.5, PM10), emissions (CO2, greenhouse gases), waste management, water quality, climate indicators |

## 17. Energy

| Field | Value |
|-------|-------|
| **Eurostat theme** | Environment and energy |
| **GUS equivalent** | Energia |
| **Subcategories** | Energy production, consumption, mix (coal/gas/renewables), electricity prices, renewable energy share |

## 18. Science, Technology & Digital Society

| Field | Value |
|-------|-------|
| **Eurostat theme** | Science, technology, and digital society |
| **GUS equivalent** | Nauka i technika, Społeczeństwo informacyjne |
| **Subcategories** | R&D spending, patents, innovation, internet usage, broadband, ICT sector |

---

## Domain Prioritisation

Prioritise domains where:
1. Data is freely available via API (no scraping)
2. High public interest / search demand
3. Data is not already well-visualised by others
4. Time-series data available (trends are more interesting than snapshots)

Domain priority is managed in Linear (project: ORE).
