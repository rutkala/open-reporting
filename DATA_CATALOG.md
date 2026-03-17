# Open Reporting — Data Catalog

**Last updated: March 2026**

All data currently ingested into the PostgreSQL warehouse on the VPS.

---

## 1. GUS BDL — Voivodship Budgets

| Field | Value |
|-------|-------|
| **Source name** | GUS Bank Danych Lokalnych (BDL) |
| **URL** | https://bdl.stat.gov.pl/api/v1 |
| **License** | Public domain — Polish public statistics (open government data) |
| **Update frequency** | Annual (data for year N typically available mid-year N+1) |
| **Ingestion script** | `ingestion/budget_ingest.py` |
| **PostgreSQL table** | `raw.bdl_budget` |
| **Coverage** | All 16 voivodships (NUTS-2), years available via BDL API |
| **Dashboards** | Regional Budgets (`charts/dashboards/voivodship.py`) |

### Columns — `raw.bdl_budget`

| Column | Type | Description |
|--------|------|-------------|
| `id` | SERIAL PK | Auto-increment row ID |
| `variable_id` | INTEGER | BDL variable code (6454 = revenues, 6476 = expenditures) |
| `variable_name` | TEXT | Human-readable name (`revenues` or `expenditures`) |
| `unit_id` | TEXT | BDL unit identifier for the voivodship |
| `unit_name` | TEXT | Voivodship name in Polish |
| `year` | INTEGER | Budget year |
| `value` | NUMERIC | Value in thousands PLN |
| `flag` | TEXT | BDL data quality flag (e.g. estimate, provisional) |
| `loaded_at` | TIMESTAMPTZ | Ingestion timestamp |

### BDL Variables used

| Variable ID | Name | Description |
|-------------|------|-------------|
| 6454 | revenues | Dochody budżetów województw (voivodship budget revenues) |
| 6476 | expenditures | Wydatki z budżetu (voivodship budget expenditures) |

### Notes
- Budget balance (surplus/deficit) is derived as `revenues - expenditures` at query time
- Administrative level = 2 (województwo / voivodship)
- API key stored in `.env` as `BDL_API_KEY`; unauthenticated requests are rate-limited

---

## 2. National Budget (Budżet Państwa) — Poland 2008–2024

| Field | Value |
|-------|-------|
| **Source name** | NIK (Najwyższa Izba Kontroli) + Ministerstwo Finansów |
| **URL (NIK)** | https://www.nik.gov.pl/analiza-budzetu-panstwa/archiwum |
| **URL (MF)** | https://www.gov.pl/web/finanse/szacunek-2024 |
| **License** | Public domain — Polish public institution reports |
| **Update frequency** | Annual (NIK publishes full-year execution ~mid following year) |
| **Ingestion script** | `processing/national_budget.py` (hardcoded data, not API-driven) |
| **PostgreSQL table** | `public.national_budget` |
| **Coverage years** | 2008–2024 |
| **Dashboards** | State Budget (`charts/dashboards/state_budget.py`) |

### Columns — `public.national_budget`

| Column | Type | Description |
|--------|------|-------------|
| `year` | INTEGER PK | Budget year |
| `revenues_bn` | NUMERIC(8,2) | Total revenues, billions PLN |
| `expenditures_bn` | NUMERIC(8,2) | Total expenditures, billions PLN |
| `deficit_bn` | NUMERIC(8,2) | Deficit (revenues − expenditures), billions PLN |
| `deficit_pct_revenue` | NUMERIC(6,2) | Deficit as % of revenues (generated/computed column) |
| `confidence` | VARCHAR(4) | `HIGH` = directly from NIK/MF; `EST` = estimated/calculated |
| `notes` | TEXT | Polish-language source note and context for the year |

### Notes
- Data is hardcoded in the script — not fetched live. Re-run script to update for new years.
- Years marked `EST` are calculated from surrounding data points where NIK source wasn't directly available
- 2020 spike (109.3 bn deficit) due to COVID-19 fiscal response
- 2024 record deficit (211 bn) driven by 800+ programme, defence spending, ZUS transfers

---

## 3. GPW Warsaw Stock Exchange — Daily Prices

| Field | Value |
|-------|-------|
| **Source name** | stooq.com |
| **URL** | https://stooq.com/q/d/l/?s={ticker}&i=d |
| **License** | Free for personal/educational use; no commercial redistribution |
| **Update frequency** | Daily after market close (GPW closes ~17:05 CET) |
| **Ingestion script** | `ingestion/gpw_ingest.py` |
| **PostgreSQL tables** | `public.stock_prices`, `public.companies`, `public.ingestion_log` |
| **Coverage years** | Full history available from stooq (~2000 for major tickers) |
| **Dashboards** | GPW Market (`charts/dashboards/gpw_market.py`) |

### Columns — `public.stock_prices`

| Column | Type | Description |
|--------|------|-------------|
| `ticker` | TEXT | Exchange ticker symbol (e.g. `PKN`, `CDR`) |
| `date` | DATE | Trading date |
| `open` | NUMERIC | Opening price (PLN) |
| `high` | NUMERIC | Intraday high (PLN) |
| `low` | NUMERIC | Intraday low (PLN) |
| `close` | NUMERIC | Closing price (PLN) |
| `volume` | INTEGER | Daily traded volume (shares) |

Unique constraint on `(ticker, date)`.

### Columns — `public.companies`

| Column | Type | Description |
|--------|------|-------------|
| `ticker` | TEXT PK | Exchange ticker symbol |
| `name` | TEXT | Company full name |
| `sector` | TEXT | Sector classification |

### Columns — `public.ingestion_log`

| Column | Type | Description |
|--------|------|-------------|
| `id` | SERIAL PK | Auto-increment |
| `ticker` | TEXT | Ticker processed |
| `rows_inserted` | INTEGER | Rows upserted in this run |
| `date_from` | TEXT | Start date of fetched range |
| `date_to` | TEXT | End date of fetched range |
| `status` | TEXT | `ok` or `error` |
| `error` | TEXT | Error message if status = error |

### Tickers covered
140+ WSE tickers across three segments:
- **WIG20** (20 large caps): ALR, ALE, CDR, CPS, DNP, JSW, KGH, KRU, LPP, MBK, OPL, PEO, PGE, PKN, PKO, PZU, SPL, XTB, ATC, BDX
- **mWIG40** (mid caps): ~35 tickers
- **sWIG80 + other main market**: ~85 tickers

Full list in `ingestion/gpw_ingest.py` — `GPW_TICKERS` constant.

### Notes
- Incremental mode: fetches from last known date to today
- Backfill mode (`--backfill`): fetches full history from stooq
- Rate limited to 0.5s between requests to avoid being blocked

---

## Summary table

| Table | Schema | Rows (approx) | Updated | Used by |
|-------|--------|--------------|---------|---------|
| `raw.bdl_budget` | raw | ~500 | Manually / annually | voivodship.py |
| `national_budget` | public | 17 | Manually / annually | state_budget.py |
| `stock_prices` | public | 500k+ | Daily | gpw_market.py |
| `companies` | public | 140+ | On ingestion | gpw_market.py |
| `ingestion_log` | public | grows daily | Daily | (ops only) |

---

---

## 4. GUS BDL — Labour Market by Voivodship

| Field | Value |
|-------|-------|
| **Source name** | GUS Bank Danych Lokalnych (BDL) |
| **URL** | https://bdl.stat.gov.pl/api/v1 |
| **License** | Public domain — Polish public statistics (open government data) |
| **Update frequency** | Annual (unemployment quarterly, wages/GDP annually) |
| **Ingestion script** | `ingestion/labour_ingest.py` |
| **PostgreSQL table** | `raw.bdl_labour` |
| **Coverage** | All 16 voivodships (NUTS-2) |
| **Dashboards** | Labour Market (`charts/dashboards/labour_market.py`) |

### Columns — `raw.bdl_labour`

| Column | Type | Description |
|--------|------|-------------|
| `id` | SERIAL PK | Auto-increment row ID |
| `variable_id` | INTEGER | BDL variable code |
| `variable_name` | TEXT | `unemployment_rate`, `avg_wages`, or `gdp_per_capita` |
| `unit_id` | TEXT | BDL unit identifier for the voivodship |
| `unit_name` | TEXT | Voivodship name in Polish |
| `year` | INTEGER | Data year |
| `value` | NUMERIC | Value (see units below) |
| `flag` | TEXT | BDL data quality flag |
| `loaded_at` | TIMESTAMPTZ | Ingestion timestamp |

### BDL Variables used

| Variable ID | Name | Unit | Coverage |
|-------------|------|------|----------|
| 60270 | unemployment_rate | % | 2004–present |
| 64428 | avg_wages | PLN/month | 2002–present |
| 458421 | gdp_per_capita | PLN | 2000–present |

---

## Summary table

| Table | Schema | Rows (approx) | Updated | Used by |
|-------|--------|--------------|---------|---------|
| `raw.bdl_budget` | raw | ~500 | Manually / annually | voivodship.py |
| `raw.bdl_labour` | raw | ~1,200 | Manually / annually | labour_market.py |
| `national_budget` | public | 17 | Manually / annually | state_budget.py |
| `stock_prices` | public | 500k+ | Daily | gpw_market.py |
| `companies` | public | 140+ | On ingestion | gpw_market.py |
| `ingestion_log` | public | grows daily | Daily | (ops only) |
