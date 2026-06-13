# Open Reporting — Data Sources

> **Live operational status:** this document is the research catalogue (what exists, what we decided).
> The *current* ingestion state of every source — status, file counts, quotas, last run — lives in the
> admin portal: [portal.open-reporting.dev/source-registry.html](https://portal.open-reporting.dev/source-registry.html),
> generated from `products/ingestion/registry/source_registry.yaml`. All 44 sources below are mirrored
> there under the same 4-category grouping. When statuses here and there disagree, the portal is right.

## Policy & Rules

All data used in Open Reporting must come from official, publicly accessible sources.

### Source categories (use in this order — move to next only when prior category lacks the data)

| Priority | Category | When to use |
|----------|----------|-------------|
| **1 — GUS** | Statistics Poland — main national statistical aggregator | Default for all Polish data |
| **2 — Institutional** | Polish government agencies, ministries, regulators | When GUS does not cover the topic |
| **3 — International** | Multinational statistical aggregators | For cross-country comparisons or data not collected nationally |
| **4 — Market** | Private / commercial organisations | Requires explicit approval before use — document why 1–3 are insufficient |

### Rules
- No scraping — API or official file download only
- Source must be publicly accessible without payment
- No private or commercial data unless explicitly approved (category 4)
- If nothing found in categories 1–3 → present research findings and get approval

---

## 1. GUS — Główny Urząd Statystyczny (Statistics Poland)

**Portal**: https://stat.gov.pl (→ new.stat.gov.pl) · **API hub**: https://api.stat.gov.pl · **Databases hub**: https://bazydanych.new.stat.gov.pl

GUS is Poland's central statistical office. It operates 13 database systems, 9 programmatic APIs, and 8 thematic dashboards.

### Database Systems

#### GUS / DBW — Dziedzinowe Bazy Wiedzy (Domain Knowledge Bases)
- **URL**: https://dbw.stat.gov.pl
- **Catalogue API**: `https://dbw.stat.gov.pl/api_app/getCatalogValues` — returns all download links (no auth)
- **REST API**: `https://api-dbw.stat.gov.pl/api/` · Docs: https://api.stat.gov.pl/Home/DBWApi
- **Bulk download**: **Yes** — 426 files (ZIP/CSV), 21 HVD categories (EU regulation 2023/138)
- **Auth**: None for bulk; free key (`DBW_API_KEY`, `X-ClientId` header) for API — 500 req/15min, 5,000 req/12h, 50,000 req/7d (all actively enforced). API mirror in progress (2026-06) via `extractors/dbw_extractor.py` (API 1.2.0): 1,518 variables, cron 04:00+16:00 UTC
- **Coverage**: GDP, government expenditure/debt, employment, unemployment, population, poverty, HICP, tourism, industrial production; 1995–2026
- **File format**: ZIP → `<id>.csv` (semicolon-delimited, comma decimal) + `<id>_Dict.csv` (dimension labels)
- **Ingestion status**: **DONE** — 426 files in `data/landing/gus_hvd/` via `bulk/run_bulk.py`
- **Raw tables**: `raw.dbw_observations`, `raw.dbw_positions`, `raw.dbw_variables`
- **Notes**: Bulk preferred over API — avoids rate limits. Dimension position IDs exceed INT32 → BIGINT. `no_value_id != 0` = suppressed/NULL.

#### GUS / BDL — Bank Danych Lokalnych (Local Data Bank)
- **URL**: https://bdl.stat.gov.pl · **API**: https://bdl.stat.gov.pl/api/v1/ · **Docs**: https://api.stat.gov.pl/Home/BdlApi
- **Bulk download**: **No** — API only, paginated queries
- **Auth**: Optional free key (`X-ClientId`); register at bdl.stat.gov.pl → `BDL_API_KEY` env var
- **Rate limit**: Anonymous: 10k req/week · Registered: 50k req/week (≈7k/day)
- **Format**: JSON or XML
- **Coverage**: 40 000+ variables, all admin levels (kraj → województwo → powiat → gmina → miejscowość), 1995–present, CC BY 4.0
- **Key endpoints**: `/subjects` (topic tree) · `/variables?subject-id={id}` · `/data/by-variable/{varId}?unit-level={0-6}`
- **Ingestion status**: **In progress (2026-06)** — resumable full mirror via `extractors/bdl_extractor.py`; 17/33 subjects complete, 46k+ variables in `gus_bdl_api/`; daily cron 03:30 UTC, weekly-budget paced
- **Notes**: Only the weekly 50k cap is observed enforced (docs also list 10/s, 500/15min, 5k/12h tiers). Unit-level 2 (województwa) only.

#### GUS / BDM — Bank Danych Makroekonomicznych (Macroeconomic Data Bank)
- **URL**: https://bdm.stat.gov.pl
- **Bulk download**: **Unknown — Blocked**
- **Auth**: None
- **Coverage**: National accounts, money supply, CPI, trade, employment, finance — macro time series
- **Ingestion status**: **Blocked** — JS SPA (page returns 1 KB skeleton); no API, no XLS/CSV links found in source; no documented REST endpoint; requires browser with JS to render content. Likely overlaps heavily with BDL and DBW — assess overlap before investing in browser scraping.

#### GUS / BDP — Bank Danych Polska (Data Bank Poland)
- **URL**: https://bdp.stat.gov.pl
- **Bulk download**: **Unknown — Blocked**
- **Auth**: None
- **Coverage**: Unclear — likely a Poland-only aggregated view of cross-GUS data
- **Ingestion status**: **Blocked** — JS SPA; content not accessible without browser rendering

#### GUS / SDG — Cele Zrównoważonego Rozwoju (Sustainable Development Goals)
- **URL**: https://sdg.gov.pl · **API hub**: https://api.stat.gov.pl/Home/SDGApi
- **Bulk download**: **Yes** — 2 JSON files, no auth, CC BY 4.0
  - `https://sdg.gov.pl/api/v1/en/national_data.json` → 144 national indicators, 17 goals (full data)
  - `https://sdg.gov.pl/api/v1/en/global_data.json` → 250 global SDG indicators
  - Index: `https://sdg.gov.pl/api/v1/en/national/list.json`
  - Per-goal: `https://sdg.gov.pl/api/v1/en/national/{1-17}.json`
- **Auth**: None
- **Coverage**: 144 national + 250 global SDG indicators for Poland
- **Ingestion status**: **DONE** — `gus_sdg_bulk/` in landing, 2 files (national_data.json + global_data.json)

#### GUS / STRATEG — Monitoring Strategii Rozwoju (Development Strategy Monitoring)
- **URL**: https://strateg.stat.gov.pl · **API docs**: https://strateg.stat.gov.pl/apidocs/
- **Bulk download**: Via API (paginated REST, Flasgger/Swagger UI)
- **Auth**: Optional free key — obtain via "Pobierz klucz do API" on strateg.stat.gov.pl
- **Rate limit**: Anon: 5 req/s, 100/15min · Registered: 10 req/s, 500/15min
- **Format**: JSON
- **Coverage**: EU cohesion policy indicators + national development strategy indicators, NUTS2
- **Ingestion status**: **Blocked** — API paths return 404 via curl; Swagger UI is JS-only; exact endpoints need browser/network inspector

#### GUS / SMUP — System Monitorowania Usług Publicznych (Public Services Monitoring)
- **URL**: https://smup.gov.pl · **API**: https://api.smup.gov.pl · **API docs**: https://api.smup.gov.pl/apidocs/index.html
- **Bulk download**: Via API (paginated REST, Flasgger/Swagger UI)
- **Auth**: Optional free key (contact: api-smup@stat.gov.pl)
- **Rate limit**: Anon: 5 req/s, 100/15min · Registered: 10 req/s, 500/15min
- **Format**: JSON
- **Coverage**: Education, healthcare, transport, social services — at gmina level
- **Ingestion status**: **Blocked** — API exists (rate limit headers confirmed), but endpoint paths return 404; Swagger UI is JS-only; exact paths need browser/network inspector

#### GUS / TranStat — Statystyki transportu (Transport Statistics — experimental)
- **URL**: https://transtat.stat.gov.pl · **API**: https://api-transtat.stat.gov.pl · **API docs**: https://api-transtat.stat.gov.pl/apidocs/index.html
- **Bulk download**: Via API (paginated REST, Flasgger/Swagger UI)
- **Auth**: None documented
- **Coverage**: Road and maritime transport statistics (experimental series)
- **Ingestion status**: **Blocked** — API paths unknown; transtat.stat.gov.pl returning HTTP 500; Swagger UI JS-only; marked experimental by GUS

#### GUS / Biuletyn statystyczny — długie szeregi (Statistical Bulletin — Long Time Series)
- **URL**: https://new.stat.gov.pl/biuletyn-statystyczny-dlugie-szeregi
- **Bulk download**: **Yes** — 62 Excel files, no auth, updated monthly
  - URL pattern: `https://new.stat.gov.pl/sites/default/files/2026-05/tabl{01-62}_*.xlsx`
  - Topics: GDP, population, employment, wages, social benefits, state budget, public debt, enterprise finance, price indices, investments, housing, agriculture, industry, construction, transport, retail/wholesale trade, foreign trade, tourism, business sentiment
- **Auth**: None
- **Coverage**: Monthly time series 2010–present (some series earlier); latest: No. 4/2026 (May 2026)
- **Ingestion status**: **DONE** — `gus_biuletyn_bulk/` in landing, 63 XLSX scraped from page (`file-url` spans, self-updating)

#### GUS / SVS — Statystyczne Vademecum Samorządowca (Statistical Handbook for Local Government)
- **URL**: https://svs.stat.gov.pl
- **Bulk download**: **No** — web-only profile sheets per administrative unit
- **Coverage**: ~100 key indicators per gmina/powiat/województwo
- **Ingestion status**: **Skip** — data originates from BDL/BDM; source there instead

#### GUS / Atlas Regionów (Regional Atlas)
- **URL**: https://atlas.stat.gov.pl (connection refused 2026-06 — may be retired)
- **Ingestion status**: **Skip** — visualisation layer on BDL data; no separate content

#### GUS / SDDS — Special Data Dissemination Standard
- **URL**: https://stat.gov.pl/banki-i-bazy-danych/sdds/ → dsbb.imf.org (Poland at IMF)
- **Ingestion status**: **Skip** — Poland's SDDS submission to IMF; data covered by IMF/Eurostat sources

#### GUS / Baza organizacji polskich za granicą (Polish Organisations Abroad)
- **URL**: https://polonia.stat.gov.pl
- **Coverage**: Directory of Polish organisations and institutions abroad
- **Ingestion status**: **Not a priority** — reference directory, not statistical series

### APIs

#### GUS / TERYT — Geographic Unit Codes
- **URL**: https://api.stat.gov.pl/Home/TerytApi
- **Native service**: SOAP/XML web service (ws1) at wyszukiwarkaregon.stat.gov.pl — registration required (teryt_ws1@stat.gov.pl); provides TERC, SIMC, ULIC catalogues
- **Practical bulk method**: **Use BDL API** — `https://bdl.stat.gov.pl/api/v1/units?level={0-6}&lang=pl&page={n}&per-page=100` returns all units with TERYT codes; no registration needed
  - Level 0: 1 unit (kraj) · Level 1: 7 (makroregiony) · Level 2: 16 (województwa)
  - Level 3: 17 · Level 4: 73 · Level 5: 382 (powiaty) · Level 6: 4 198 (gminy)
  - Total: ~4 714 units — fits in ~50 paginated requests
- **Auth**: None (BDL anonymous tier sufficient)
- **Coverage**: Full Polish administrative unit hierarchy with TERYT codes, names, parent IDs
- **Ingestion status**: **DONE** — `gus_teryt_bulk/` in landing, 51 paginated JSON files (7 levels, ceiling-paged at 100/request)

#### GUS / REGON — Business Register
- **URL**: https://api.stat.gov.pl/Home/RegonApi
- **Bulk download**: **No** — entity-level queries only (by REGON/NIP/KRS)
- **Auth**: **Free key required** — email regon_bir@stat.gov.pl
- **Rate limit**: 6 000 calls/h peak, 10 000/h off-peak
- **Coverage**: Full Polish business register — all legal entities
- **Ingestion status**: **Not started** — no bulk export; useful for company enrichment queries only

#### GUS / SDP — Statistical Data Publications
- **URL**: https://api.stat.gov.pl/Home/SDPApi
- **Bulk download**: Partial
- **Auth**: None
- **Coverage**: Publication index — links to GUS statistical publications
- **Ingestion status**: **Not started** — low priority

---

## 2. Institutional — Polish Government Agencies & Regulators

#### NBP — Narodowy Bank Polski (National Bank of Poland)
- **URL**: https://www.nbp.pl · **API**: https://api.nbp.pl/api/
- **Archival bulk**: `https://nbp.pl/wp-content/uploads/{current_year}/{year}/archiwum_tab_a_{year}.xlsx` (2010–present)
- **Bulk download**: **Yes** — annual XLSX archives 2010–present + daily JSON via API
- **Auth**: None
- **Format**: JSON (API), XLSX (archival)
- **Coverage**: Exchange rates (tables A/B/C), interest rates, gold price, monetary aggregates
- **Ingestion status**: **DONE** — archival XLSX in `data/landing/nbp/`; daily rates via `incremental/run_incremental.py`
- **Notes**: Direct URL pattern for archival files verified for 2010–2025.

#### MF — Ministerstwo Finansów (Ministry of Finance)
- **URL**: https://www.gov.pl/web/finanse · **dane.gov.pl**: institution ID `18`
- **OpenBudget API**: https://openbudget.gov.pl/api/v1/datasets
- **Bulk download**: **Yes** — 303 files via dane.gov.pl; OpenBudget JSON catalogue
- **Auth**: None
- **Coverage**: Budget execution (revenue/expenditure by chapter), public debt, tax statistics; updated quarterly
- **Ingestion status**: **DONE** — 303 files in `data/landing/mf_dane/`
- **Notes**: OpenBudget domain (`openbudget.gov.pl`) had DNS resolution failures — investigate separately.

#### NFZ — Narodowy Fundusz Zdrowia (National Health Fund)
- **URL**: https://dane.nfz.gov.pl · **dane.gov.pl**: institution ID `31`
- **Bulk download**: **Yes** — 2 253 files via dane.gov.pl
- **Auth**: None
- **Coverage**: Healthcare services, drug reimbursement, medical procedures, regional health fund data
- **Ingestion status**: **DONE** — 2 253 files in `data/landing/nfz/` via `bulk/run_bulk.py`

#### ZUS — Zakład Ubezpieczeń Społecznych (Social Insurance Institution)
- **URL**: https://www.zus.pl · **dane.gov.pl**: institution ID `47`
- **Bulk download**: **Yes** — 26 files via dane.gov.pl
- **Auth**: None
- **Coverage**: Pension and disability benefits, contribution statistics, insured persons
- **Ingestion status**: **DONE** — 26 files in `data/landing/zus/` via `bulk/run_bulk.py`

#### MEN / CIE — Centrum Informatyczne Edukacji (Ministry of Education)
- **URL**: https://www.gov.pl/web/edukacja · **dane.gov.pl**: institution ID `15`
- **Bulk download**: Unknown — institution ID 15 returned 0 resources on dane.gov.pl
- **Auth**: None
- **Coverage**: School statistics, student numbers, teachers, exam results
- **Ingestion status**: **Blocked** — institution ID may be wrong; needs investigation

#### KNF — Komisja Nadzoru Finansowego (Financial Supervision Authority)
- **URL**: https://www.knf.gov.pl/dane_statystyczne
- **Bulk download**: **No** — XLSX/PDF file downloads only, no API
- **Auth**: None
- **Coverage**: Banking sector, insurance, capital markets, pension funds
- **Ingestion status**: **Not started** — investigate if structured export exists; file scraping not allowed

#### GDDKiA — Generalna Dyrekcja Dróg Krajowych i Autostrad (National Roads Authority)
- **URL**: https://www.gddkia.gov.pl · **dane.gov.pl**: institution ID `106`
- **Bulk download**: **Yes** — 60 files via dane.gov.pl
- **Auth**: None
- **Coverage**: Road network, traffic counts, accidents, investment projects
- **Ingestion status**: **Done** — 55/60 files in `data/landing/gddkia/` (5 failed — filename length issue)

#### URE — Urząd Regulacji Energetyki (Energy Regulatory Office)
- **URL**: https://www.ure.gov.pl · **dane.gov.pl**: institution ID `58`
- **Bulk download**: **Yes** — 3 files via dane.gov.pl
- **Auth**: None
- **Coverage**: Energy and gas market statistics, tariffs, licensed operators
- **Ingestion status**: **Done** — 3 files in `data/landing/ure/`

#### GIOŚ — Główny Inspektorat Ochrony Środowiska (Chief Inspectorate for Environmental Protection)
- **URL**: https://www.gios.gov.pl · **API v1**: https://api.gios.gov.pl/pjp-api/v1/rest/
- **Bulk download**: **Yes** — station catalogue + per-station sensor data via v1 API
- **Auth**: None
- **Coverage**: Air quality monitoring — PM2.5, PM10, NO2, SO2, O3; 500+ stations nationwide
- **Ingestion status**: **Done** — station catalogue + sensor lists in `data/landing/gios/`; daily AQ readings via `incremental/run_incremental.py`
- **Notes**: Use v1 API (`/pjp-api/v1/rest/`) — old v0 returns HTTP 410 Gone.

#### MRiRW — Ministerstwo Rolnictwa i Rozwoju Wsi (Ministry of Agriculture)
- **URL**: https://www.gov.pl/web/rolnictwo · **dane.gov.pl**: institution ID `204`
- **Bulk download**: Unknown — institution ID 204 returned 0 resources on dane.gov.pl
- **Auth**: None
- **Coverage**: Agricultural production, food trade, rural development
- **Ingestion status**: **Blocked** — institution ID may be wrong; needs investigation

#### SAOS — System Analizy Orzeczeń Sądowych (Court Judgments)
- **URL**: https://www.saos.org.pl/api
- **Bulk download**: Via paginated API
- **Auth**: None
- **Coverage**: Polish court judgments — civil, criminal, administrative
- **Ingestion status**: **Blocked** — API returning 301→404 as of 2026-06; endpoint may have moved

#### KRS — Krajowy Rejestr Sądowy (National Court Register)
- **URL**: https://prs.ms.gov.pl/krs/openApi
- **Bulk download**: **No** — entity-level queries only
- **Auth**: None
- **Coverage**: Registered companies, associations, foundations
- **Ingestion status**: **Not started** — no bulk export; entity-level access only

#### OPI RAD-on — Rejestr Nauki (Research Institutions Register)
- **URL**: https://radon.nauka.gov.pl/opendata/polon/
- **Bulk download**: **Partial** — `/institutions` works; `/universities`, `/institutes`, `/researchUnits` return 404
- **Auth**: None
- **Coverage**: Polish universities, research institutes, scientific units
- **Ingestion status**: **Partial** — `/institutions` endpoint only; others blocked (404)

---

## 3. International — Multinational Statistical Aggregators

#### Eurostat — European Statistical Office
- **URL**: https://ec.europa.eu/eurostat/web/main/data/database
- **Bulk download API**: `https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/{code}/?format=TSV&compressed=true`
- **TOC API**: `https://ec.europa.eu/eurostat/api/dissemination/catalogue/toc/txt?lang=en`
- **Bulk download**: **Yes** — one TSV.gz per dataset, named by dataset code
- **Auth**: None
- **Coverage**: 10 000+ datasets, all EU member states + candidates, NUTS2/3, 1960s–present; macro, social, environment, trade, agriculture, transport
- **Ingestion status**: **DONE** — 10 379 datasets in `data/landing/eurostat/`; nightly incremental refresh via TOC diff

#### OECD Data Explorer
- **URL**: https://data-explorer.oecd.org · **API**: https://sdmx.oecd.org/public/rest/ (SDMX REST)
- **Bulk download**: **Yes** — via API; CSV/JSON/XML; `?contentType=csv` for simple extraction
- **Auth**: None
- **Coverage**: OECD member + partner countries; macro (GDP, trade, fiscal), social (education, health, inequality), environment, labour; long historical series
- **Key datasets for Poland**: National Accounts (SNA), Labour Force Statistics, Government Finance Statistics, Education at a Glance
- **Ingestion status**: **Not started**

#### World Bank — World Development Indicators (WDI)
- **URL**: https://databank.worldbank.org/source/world-development-indicators · **API**: https://api.worldbank.org/V2/
- **Bulk download**: **Yes** — full ZIP at data.worldbank.org/data-catalog/world-development-indicators; or `?downloadformat=csv` per query
- **Auth**: None
- **Format**: JSON, XML, CSV
- **Coverage**: 1 400+ indicators, 200+ countries, 1960–present; poverty, health, education, environment, economy, gender
- **Key datasets for Poland**: GDP per capita, Gini, FDI, government debt, unemployment, life expectancy · Country code: `POL`
- **Ingestion status**: **Not started**

#### IMF — World Economic Outlook (WEO)
- **URL**: https://www.imf.org/en/Publications/SPROLLs/world-economic-outlook-databases
- **Bulk download**: **Yes** — Excel and CSV, twice yearly (April + October)
- **Auth**: None
- **Coverage**: ~50 macro indicators, 190 countries, 1980–present + 5-year forecast; GDP, inflation, unemployment, current account, government balance/debt
- **Ingestion status**: **Not started**
- **Notes**: No live API — static file releases only. URL pattern: `imf.org/external/pubs/ft/weo/{year}/{month}/weodata/WEOApr{year}all.xls`

#### IMF — International Financial Statistics (IFS)
- **URL**: https://data.imf.org/?sk=4c514d48-b6ba-49ed-8ab9-52b0c1a0179b · **API**: https://dataservices.imf.org/REST/SDMX_JSON.svc/
- **Bulk download**: **Yes** — via SDMX JSON API
- **Auth**: None
- **Coverage**: Monetary, fiscal, external sector, interest rates; 190 countries, 1948–present
- **Ingestion status**: **Not started**

#### ECB — European Central Bank Statistical Data Warehouse
- **URL**: https://sdw.ecb.europa.eu · **API**: https://data-api.ecb.europa.eu/service/ (SDMX REST)
- **Bulk download**: **Yes** — via SDMX API; CSV/XML/JSON
- **Auth**: None
- **Coverage**: Euro area and EU monetary statistics — interest rates, exchange rates, monetary aggregates, balance of payments, government finance (EDP), securities
- **Key datasets for Poland**: PLN exchange rates, government debt/deficit (EDP notifications), bond yields
- **Ingestion status**: **Not started**

#### ILOSTAT — International Labour Organization
- **URL**: https://ilostat.ilo.org/data/ · **API**: https://sdmx.ilo.org/rest/ (SDMX REST)
- **Bulk download**: **Yes** — CSV per indicator or bulk ZIP; also API
- **Auth**: None
- **Coverage**: Labour market — employment, unemployment, wages, working hours, labour force, occupational injuries; 200+ countries, 1969–present
- **Key datasets for Poland**: Employment by sector, unemployment rate, wages, collective bargaining
- **Ingestion status**: **Not started**

#### UN — World Population Prospects (WPP)
- **URL**: https://population.un.org/wpp/
- **Bulk download**: **Yes** — Excel/CSV per indicator group; free; new edition every 2 years (latest: WPP 2024)
- **Auth**: None
- **Coverage**: Population estimates and projections 1950–2100, all countries; births, deaths, migration, age structure, fertility, mortality
- **Key datasets for Poland**: Population projections, age structure, fertility rate, life expectancy
- **Ingestion status**: **Not started**

#### FAO — FAOSTAT
- **URL**: https://www.fao.org/faostat/en/#data · **API**: https://fenixservices.fao.org/faostat/api/v1/
- **Bulk download**: **Yes** — CSV ZIP per domain (Production, Trade, Prices, Land, etc.)
- **Auth**: None
- **Coverage**: Food production, agricultural trade, land use, food security; 245 countries, 1961–present
- **Key datasets for Poland**: Crop production, livestock, food trade balance, agricultural prices
- **Ingestion status**: **Not started** — lower priority (agriculture not a primary domain yet)

#### WTO — World Trade Organization Statistics
- **URL**: https://stats.wto.org · **API**: https://api.wto.org/timeseries/v1/
- **Bulk download**: **Yes** — via API or manual CSV export from portal
- **Auth**: **Free API key required** — register at api.wto.org
- **Coverage**: Merchandise trade, commercial services, tariffs, trade profiles; 170+ countries, 1980–present
- **Key datasets for Poland**: Exports/imports by product and partner, trade in services
- **Ingestion status**: **Not started**

#### UN — UNdata
- **URL**: https://data.un.org · **API**: http://data.un.org/ws/rest/ (SDMX)
- **Bulk download**: **Yes** — CSV per dataset
- **Auth**: None
- **Coverage**: Aggregator — demographics, trade, agriculture, energy, health, education from UNSD, UNICEF, UNHCR, WHO and others
- **Ingestion status**: **Not started** — prefer agency-specific sources (ILOSTAT, FAOSTAT, WDI) for better documentation

---

## 4. Market — Private & Commercial Sources

*Research pending. No sources approved yet.*

Sources in this category require explicit approval before use. Must document source credibility and why categories 1–3 were insufficient.

---

## DB Schema Convention

```
raw.{source}_{entity}     ← ingested data, preserve original structure
curated.stg_{source}      ← staging, cleaned and typed
curated.fact_{domain}     ← analytical mart
```

Examples:
- `raw.dbw_observations` — raw GUS DBW data
- `raw.eurostat_nama_10_gdp` — raw Eurostat GDP dataset
- `curated.fact_public_finance` — analytical mart for public finance dashboard
