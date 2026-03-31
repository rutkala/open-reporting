# Domain Brief: Public Finance

**Prepared for:** OR-103 — Research: Public Finance data sources
**Date:** 2026-03-30
**Status:** Complete

---

## 1. Domain Scope

Public finance covers how governments mobilise resources, allocate them across public services, and manage the resulting financial stocks.

**In scope:** Government revenue (taxes, social contributions, grants), government expenditure (social transfers, wages, investment, debt service), fiscal balance (deficit/surplus), government debt, fiscal policy and rules, sub-national finance (voivodeships, powiats, gminy).

**Out of scope:** Monetary policy (central bank), private sector finance, balance of payments (adjacent).

| Sub-domain | Scope |
|---|---|
| Government revenue | Tax structure, tax-to-GDP, social contributions, non-tax revenues |
| Government expenditure | Functional (COFOG), economic classification |
| Fiscal balance | Headline deficit/surplus, primary balance, structural/cyclically-adjusted balance |
| Government debt | Level, composition, maturity, sustainability |
| Fiscal rules | Expenditure rules, constitutional debt limits, Maastricht criteria |
| Fiscal decentralisation | Central vs. local split of revenue and spending |

---

## 2. Key Analytical Questions by Audience

### Economists
- Is fiscal policy procyclical or countercyclical?
- What is the structural (cyclically-adjusted) balance, stripped of one-off factors?
- Is the primary balance consistent with debt stabilisation?
- How does Poland's expenditure composition compare to EU peers?
- Are off-budget instruments (BGK funds) properly captured?

### Journalists and Policy Commentators
- What is Poland's deficit — is it above the EU 3% limit?
- Is Poland heading into / already in an Excessive Deficit Procedure?
- How fast is public debt growing and when will it hit the 60% constitutional limit?
- How much is spent on what (social vs. roads vs. defence)?
- Are there "hidden debts" outside the official budget?

### Policymakers (Ministry of Finance)
- Is the trajectory consistent with the Stabilising Expenditure Rule (SER)?
- What adjustment is needed to meet EDP commitments to the European Commission?
- How is budget execution tracking against the annual Budget Act?
- What is the financing need — how much must the Treasury borrow?

### EU Institutions
- Does Poland breach the 3% Maastricht reference value?
- Is Poland's debt on a declining path toward 60% of GDP?
- What adjustment path is needed under the post-2023 EU fiscal framework?
- Are reported deficits consistent with ESA 2010 methodology?

### Citizens
- How much tax do I pay and what does it fund?
- Is the deficit growing — will I or my children pay for it?
- How does Poland compare to other EU countries?

### What "good fiscal performance" vs. "fiscal stress" looks like

| Dimension | Healthy | Stress Signals |
|---|---|---|
| Deficit / GDP | Below 3%; declining structural deficit | >3% for multiple years; rising structural deficit |
| Debt / GDP | Below 60%; declining trend | >60% and rising |
| Primary balance | Positive; consistent with debt stabilisation | Persistently negative |
| Interest / Revenue | Below 10% | >15%; crowding out primary spending |
| Expenditure quality | High investment + education share | Dominated by rigid entitlements; low investment |
| Fiscal rule compliance | SER respected; constitutional limit safe | Rule suspended; thresholds at risk |

---

## 3. Standard KPIs

KPIs used consistently across IMF Fiscal Monitor, Eurostat GFS, OECD, World Bank:

| KPI | Definition | Unit | Standard Breakdown |
|---|---|---|---|
| Overall fiscal balance (net lending/borrowing) | Revenue minus expenditure | % of GDP | By sector (S.1311, S.1313, S.1314, S.13) |
| Primary balance | Overall balance excl. interest payments | % of GDP | General government |
| Structural (cyclically-adjusted) balance | Balance adjusted for the economic cycle | % of potential GDP | General government |
| Gross debt (Maastricht) | Currency, deposits, debt securities, loans | % of GDP; PLN | By instrument; by sector |
| Total revenue / GDP | All revenues incl. taxes + social contributions | % of GDP | By ESA source |
| Tax revenue / GDP (tax-to-GDP) | All compulsory levies excl. social contributions | % of GDP | By tax type |
| Social contributions / GDP | Employers' + employees' + self-employed | % of GDP | |
| Total expenditure / GDP | All government outlays | % of GDP | By COFOG function or ESA type |
| Interest expenditure / GDP | D.41 interest paid | % of GDP | |
| Government investment (GFCF) / GDP | Gross fixed capital formation P.51g | % of GDP | By level of government |
| Social transfers / GDP | D.62 cash + D.63 in-kind | % of GDP | |
| Expenditure by COFOG function | 10 functional categories | % of GDP; % of total | All 10 divisions |

**Most commonly visualised in official dashboards:**
1. Deficit/surplus % GDP — country comparison bar chart with -3% threshold line
2. Debt % GDP — bar or line chart with 60% threshold line
3. Revenue and expenditure % GDP — paired time series or bars
4. Revenue composition — stacked bar: taxes, social contributions, other
5. Expenditure by COFOG — stacked bar or treemap
6. Debt composition by instrument — stacked bar

---

## 4. Analytical Frameworks

### ESA 2010 — Sector Classification

General government (S.13) comprises:

| Sub-sector | Code | Polish coverage |
|---|---|---|
| Central government | S.1311 | State budget + off-budget central entities (including BGK-managed funds) |
| State government | S.1312 | Not applicable (Poland is a unitary state) |
| Local government | S.1313 | 16 voivodeships, 314 powiats, 2477 gminy |
| Social security funds | S.1314 | ZUS (pension/disability/health), KRUS (farmers) |
| General government consolidated | S.13 | All above, intragroup transfers eliminated |

### Revenue classification (ESA transactions)
- **D.2** Taxes on production and imports (VAT, excise, property taxes)
- **D.5** Current taxes on income and wealth (PIT, CIT)
- **D.61** Net social contributions
- **D.7** Other current transfers
- **P.11/P.12** Market/non-market output (fees and charges)

### COFOG — Classification of Functions of Government (Expenditure)

| Division | Code |
|---|---|
| General public services | 01 |
| Defence | 02 |
| Public order and safety | 03 |
| Economic affairs (transport, energy, agriculture) | 04 |
| Environmental protection | 05 |
| Housing and community amenities | 06 |
| Health | 07 |
| Recreation, culture and religion | 08 |
| Education | 09 |
| Social protection | 10 |

### Maastricht / Stability and Growth Pact

| Criterion | Reference value | Measured by |
|---|---|---|
| Government deficit | ≤ 3% of GDP | ESA 2010 net lending/borrowing, S.13 |
| Government debt | ≤ 60% of GDP | Consolidated gross debt (EDP definition) |

### Poland's Fiscal Rules

| Rule | Legal basis | Mechanism |
|---|---|---|
| Constitutional debt limit | Polish Constitution Art. 216 | Prohibits public debt exceeding 60% of GDP |
| Prudential thresholds | Public Finance Act | Two thresholds: 55% and 60% (national methodology); trigger corrective spending cuts |
| Stabilising Expenditure Rule (SER) | Public Finance Act Art. 112aa | Upper limit on expenditure growth = 8-year average real GDP growth + expected inflation |

**Critical Polish-specific distinction:** Poland maintains two parallel debt measures — national (typically 10–15 pp lower, excludes some off-balance-sheet items) and EU/Maastricht. The constitutional 60% limit uses the national measure. Both must be tracked separately.

---

## 5. Visualization Conventions

Based on Eurostat Statistics Explained, IMF Fiscal Monitor, OECD Government at a Glance:

| Chart type | Standard use |
|---|---|
| Horizontal bar (sorted countries) | Cross-country comparison with EU/EA average line and Maastricht threshold line |
| Stacked bar (horizontal, many countries) | Revenue/expenditure composition comparison across EU |
| Time series line | Trend over time; often with recession shading |
| Waterfall / bridge | Decomposing year-on-year changes in deficit |
| Stacked column (vertical, over time) | COFOG expenditure evolution over years |
| Scatter plot | Structural balance vs. debt level (sustainability space) |
| Debt fan chart | DSA projections with baseline + stress scenarios |
| Treemap | COFOG function shares at a point in time |

**Standard reference lines always shown:**
- -3% GDP: Maastricht deficit limit
- 60% GDP: Maastricht debt limit
- EU-27 average and Euro area (EA-20) average

**Standard comparison group for Poland:** Visegrad Four (V4 — Poland, Czech Republic, Slovakia, Hungary) + EU average.

---

## 6. Polish Context — The Central Fiscal Story (2024–2026)

Poland is experiencing a structural fiscal deterioration that is currently the dominant story in Polish public finance:

- **Deficit:** 6.5% of GDP in 2024 — second-highest in the EU after France
- **Debt:** 55.1% of GDP (Maastricht measure); rising rapidly; projected to breach 60% Maastricht level by 2026; Polish national measure also approaching constitutional 60% threshold around same time
- **EDP:** Poland placed under EU Excessive Deficit Procedure in 2024; committed to returning below 3% by 2028 — requiring ~3.5 pp of GDP fiscal adjustment over 4 years
- **Root cause:** Expenditure-driven. Total public spending increased ~6.5 pp of GDP since 2021; revenues rose only ~1.2 pp. Key drivers: defence (from ~2% to ~4.7% of GDP), social transfers (800+ programme, social pension reform, 14th pension), public sector wage increases
- **Off-budget controversy:** Over PLN 135bn in public tasks financed off-budget via BGK. Flagged by NIK (Supreme Audit Office) as undermining budget transparency. The true ESA 2010 deficit is higher than the headline budget figure.

### Key Polish Institutions

| Institution | Role |
|---|---|
| MF (Ministry of Finance) | Budget, debt management, tax policy |
| GUS | Official statistics, ESA notifications to Eurostat |
| NBP | Central bank; fiscal agent for Treasury; yields data |
| NIK | Supreme Audit Office; annual budget execution audit |
| ZUS | Social security fund (part of S.1314) |
| BGK | State development bank; off-budget financing vehicle |

### Specific Analytical Questions for Poland

1. What is the true deficit including BGK/off-budget items?
2. When will debt breach the constitutional 60% limit under the national measure?
3. Is the defence spending increase fiscally sustainable without structural adjustment elsewhere?
4. What is the fiscal cost of demographic ageing — pension expenditure trajectory?
5. What share of public spending flows through local governments (JST)?
6. How does Poland's public investment quality compare to peers?

---

## 7. Data Source Inventory

### Source 1: DBW HVD (GUS) — Already Ingested

- **Status:** In warehouse as `raw.dbw_observations`
- **Access:** Proprietary GUS API; already ingested
- **Geography:** Poland national only
- **Time:** Annual + some quarterly; 1995–2024 for revenue/expenditure; 2000–2025 for debt
- **Key variables in warehouse:** Revenue/expenditure/balance of S.13 total and sub-sectors (S.1311, S.1313, S.1314); Maastricht debt components (currency, debt securities, loans); GFCF; social benefits; compensation of employees; taxes; social contributions; interest; subsidies
- **Dimensions available:** `dim_govt_sector` (central/local/social funds/general), `dim_resources_uses` (Revenue/Expenditure)
- **Unique value:** Already available; ESA 2010 compliant; Poland-specific; long history from 1995

---

### Source 2: Eurostat GFS — Priority 1 to Ingest

- **URL:** https://ec.europa.eu/eurostat/web/government-finance-statistics
- **API:** `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{dataset_code}`
- **Python package:** `pip install eurostat`
- **Geography:** All 27 EU member states; country-level only
- **Time:** Annual (gov_10a_main, gov_10a_exp, gov_10dd_edpt1); quarterly (gov_10q_ggnfa); 1995–present
- **Update frequency:** Twice yearly (April/October EDP notifications); annually for COFOG detail

**Key datasets:**

| Dataset | Content | Why critical |
|---|---|---|
| `gov_10a_main` | Revenue, expenditure, all ESA transactions by sub-sector | Full revenue/expenditure breakdown by ESA code AND by govt level |
| `gov_10dd_edpt1` | Official EDP deficit and debt notifications | The definitive Maastricht numbers; includes methodology notes |
| `gov_10a_exp` | COFOG expenditure breakdown | 10 functional categories — **not available in DBW** |
| `gov_10q_ggnfa` | Quarterly non-financial accounts | Quarterly tracking |
| `gov_10a_taxag` | Tax revenue by type | Detailed tax category breakdown |

- **Python access:**
```python
import eurostat
df = eurostat.get_data_df('gov_10a_main', filter_pars={'geo': ['PL'], 'unit': ['PC_GDP']})
# For EU comparison: omit 'geo' filter to get all countries
```

- **Unique value:** Only source for COFOG functional breakdown; official EU-comparable data; enables EU/EA average benchmarking; covers all EU countries for cross-country comparison; COFOG is not available in DBW

---

### Source 3: IMF WEO / Fiscal Monitor — Priority 2 to Ingest

- **URL:** https://www.imf.org/en/publications/weo/weo-database
- **DataMapper:** https://www.imf.org/external/datamapper/datasets/FM
- **Python package:** `pip install weo`
- **Geography:** All IMF member countries; country groups (Advanced, Emerging, etc.)
- **Time:** Historical from ~1980; **projections 5 years ahead** — unique among all sources
- **Update frequency:** Twice yearly (April/October WEO releases)

**Key indicators:**

| Code | Indicator |
|---|---|
| `GGXCNL_NGDP` | Overall fiscal balance (% GDP) |
| `GGXONLB_NGDP` | Primary balance (% GDP) |
| `GGSB_NPGDP` | **Cyclically-adjusted balance (% potential GDP)** — only source |
| `GGXWDG_NGDP` | Gross debt (% GDP) |
| `GGXWDN_NGDP` | Net debt (% GDP) |
| `GGREV_NGDP` | Revenue (% GDP) |
| `GGEXP_NGDP` | Expenditure (% GDP) |

- **Python access:**
```python
import weo
w = weo.WEO()  # downloads latest release
df = w.get('GGXWDG_NGDP', 'POL')
```

- **Unique value:** Only source for IMF projections (2025–2030); only source for structural/cyclically-adjusted balance; enables forward-looking fiscal sustainability analysis; essential for debt trajectory charts

---

### Source 4: GUS BDL — Priority 3 to Ingest

- **URL:** https://bdl.stat.gov.pl
- **API:** `https://bdl.stat.gov.pl/api/v1/`
- **Geography:** Full Polish territorial hierarchy — voivodeships (NUTS 2), powiats (NUTS 4), gminy (LAU)
- **Time:** Annual; ~1995–present
- **Update frequency:** Annual
- **Key variables:** Local government revenues by source, expenditures by type, local government debt and deficit, investment expenditure by voivodeship
- **Python access:**
```python
import requests
r = requests.get('https://bdl.stat.gov.pl/api/v1/variables/search',
    params={'name': 'budget', 'lang': 'en'},
    headers={'X-ClientId': 'YOUR-KEY'})
```
- **Unique value:** Only source for regional/local public finance breakdown; enables analysis of fiscal decentralisation and spatial inequality in public investment

---

### Source 5: World Bank WDI — Priority 4

- **API:** `https://api.worldbank.org/v2/`
- **Python:** `pip install wbdata`
- **Geography:** Country-level; `PL` or `POL` for Poland
- **Time:** From 1972 for some indicators
- **Key indicators:** `GC.TAX.TOTL.GD.ZS` (tax/GDP), `GC.XPN.TOTL.GD.ZS` (expenditure/GDP), `GC.DOD.TOTL.GD.ZS` (debt/GDP — **central government only**)
- **Unique value:** Longest time series (from 1972) — enables analysis of Poland's full post-communist fiscal transition. Note: covers central government, not general government — not comparable to Eurostat for current analysis but valuable for historical depth.

---

### Source 6: dane.gov.pl — Ministry of Finance Budget Execution — Priority 5

- **URL:** https://dane.gov.pl, https://api.dane.gov.pl
- **Access:** REST API for file metadata; CSV downloads (Rb-series reports)
- **Geography:** National + regional/local (JST quarterly Rb34s reports)
- **Time:** 2014–present
- **Unique value:** Granular within-year budget execution at programme/chapter/paragraph level; JST quarterly data for local government monitoring. Not available from Eurostat or IMF.

---

### Source 7: OECD Revenue Statistics — Priority 6

- **URL:** https://stats.oecd.org
- **Time:** From 1965 for revenue statistics
- **Unique value:** Longest tax-to-GDP time series (1965–present); enables analysis of Poland's full post-communist tax transition

---

### Source 8: NBP Government Bond Yields — Priority 7

- **Note:** `api.nbp.pl` does NOT contain fiscal data — only FX rates and gold. Yield data is published as downloadable Excel files on NBP website.
- **Unique value:** Polish government bond yield curve; needed for debt cost analysis and fiscal sustainability modelling

---

## 8. Recommended Ingestion Order and Integration

| Priority | Source | Rationale | Effort |
|---|---|---|---|
| 1 | Eurostat GFS (`gov_10a_main`, `gov_10dd_edpt1`, `gov_10a_exp`) | COFOG breakdown not in DBW; EU comparison; clean Python API; highest analytical density per effort | Low |
| 2 | IMF WEO / Fiscal Monitor | Only source for projections and structural balance; `weo` package | Low |
| 3 | GUS BDL (regional public finance) | Unique regional dimension; fiscal decentralisation analysis | Medium |
| 4 | World Bank WDI | Long history from 1972 | Low |
| 5 | dane.gov.pl MF budget execution | Granular execution monitoring | Medium |
| 6 | OECD Revenue Statistics | Tax history from 1965 | Low |
| 7 | NBP yield data | Debt cost analysis | Medium |

**Dimension alignment:** Eurostat GFS sectors (S.1311, S.1313, S.1314, S.13) map directly to the existing `dim_govt_sector` semantic column. ESA transaction codes (D.2, D.5, D.61 for revenue; D.1, D.3, D.4, D.6, P.2, P.5 for expenditure) are a new dimension — currently not in the named semantic columns. The `dim_resources_uses` (Revenue/Expenditure/Balance/Debt) covers the top-level split.

**New dimension consideration:** ESA transaction type (the D.2/D.5/D.61/COFOG level) is more granular than anything currently in the semantic schema. Options: (a) encode it as a new `dim_fiscal_category` column in `curated.all_indicators`, or (b) handle it at the gold mart level only (`curated.mart_finance`). Recommend option (b) for now — the gold mart can carry `fiscal_category` as a dedicated column without changing the silver schema.

---

*Sources: IMF Fiscal Monitor, Eurostat Statistics Explained GFS, ECB GFS Guide, OECD Government at a Glance, NIK 2024 budget audit, GUS deficit/debt notifications, Poland EDP commitment documents, Eurostat API documentation, World Bank Open Data, IMF DataMapper, NBP statistics portal.*
