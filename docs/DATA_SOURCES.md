# Open Reporting — Data Sources

## Data Source Policy

All data used in Open Reporting must come from official, publicly accessible sources. No third-party commercial data providers. No scraping — API or official file download only.

### Source Hierarchy

When selecting a data source for a new dashboard or dataset, follow this hierarchy. Start at Level 1 and only move down if the required data is not available at the current level.

**Level 1: Official government and EU institutions**
The default and preferred source for all data. No justification needed.
- GUS BDL, GUS StatsAPI — Polish national statistics
- OpenBudget, Ministry of Finance — public finances
- NBP — monetary data, exchange rates
- NFZ — health fund data
- MEN — education data
- Eurostat — EU-wide statistics

**Level 2: Official Polish institutional sources**
Acceptable when Level 1 does not cover the required data. Document why Level 1 was insufficient.
- KNF — financial supervision
- GDDKiA — road infrastructure
- NIZP-PZH — epidemiology and public health
- ZUS — social insurance and pensions

**Level 3: Trusted international organisations**
Acceptable for international comparisons or when Polish-specific data is unavailable.
- World Bank, IMF, OECD, UN statistical divisions

**Level 4: Additional sources**
Requires explicit user approval before use. Must document source credibility and why Level 1-3 were insufficient. No commercial data providers.

### Rules
- No scraping — API or official file download only
- No private or commercial data providers
- Source must be publicly accessible without payment
- If nothing found in Level 1-3 → present research findings and get approval before proceeding

---

## Known Sources

### Level 1: Official Government & EU

#### GUS DBW (Domain Knowledge Databases) — **primary GUS source**
- **Bulk catalogue**: `https://dbw.stat.gov.pl/pl/katalog/bulk` — 213 CSV ZIPs, 21 HVD categories (EU regulation 2023/138)
- **Catalogue API**: `https://dbw.stat.gov.pl/api_app/getCatalogValues` — returns all download links (no auth required)
- **REST API**: `https://api-dbw.stat.gov.pl/api/` — for targeted variable queries; `DBW_API_KEY` env var (`X-ClientId` header); 10 req/s, 5,000 req/12h
- **Docs**: `https://api.stat.gov.pl/Home/DBWApi?lang=en`
- **Coverage**: 85 HVD variables (756k observations), 82 cross-sections, years 1995–2026
  - Categories: GDP, government expenditure/debt, employment, unemployment, population, poverty, HICP, tourism, industrial production
- **File format**: ZIP containing `<id>.csv` (data, semicolon-delimited, comma decimal) + `<id>_Dict.csv` (dimension labels)
- **Data model**: observations stored as integer position IDs; resolve labels by joining `raw.dbw_positions` on `(section_id, dim_id, position_id)`
- **Notes**:
  - Bulk download is the preferred approach for full HVD coverage — avoids API rate limits entirely
  - Dimension position IDs can exceed INT32 (e.g. 12193299000018) — schema uses BIGINT for all dim columns
  - `no_value_id != 0` indicates suppressed/missing value — stored as NULL
  - Landing zone has 426 files (~_data.csv + _dict.csv per dataset); full reload takes ~11s via DuckDB native CSV reader
- **Ingestion scripts**:
  - `platform/ingestion/to_landing/dbw_hvd.py` — downloads all ZIPs to `data/landing/dbw_hvd/`
  - `platform/ingestion/to_raw/dbw_observations.py` — bulk-loads landing CSVs into DuckDB
- **Raw tables**: `raw.dbw_observations`, `raw.dbw_positions`, `raw.dbw_variables`
  - `raw.dbw_variables`: 85-row lookup — variable_id → variable_name, section_id, category
    (populated from dict CSVs + catalogue API during `to_raw` ingestion)

#### GUS BDL (Local Data Bank) — legacy / alternative
- **URL**: `https://bdl.stat.gov.pl/api/v1/`
- **Auth**: `BDL_API_KEY` env var (register at `https://bdl.stat.gov.pl/`)
- **Format**: JSON
- **Coverage**: 172,000+ variables across all domains, NUTS-2/NUTS-3 regional data
- **Rate limit**: 1000 requests/day on free tier
- **Notes**: Variable IDs required; use `/variables` endpoint to discover

#### GUS StatsAPI (newer, experimental)
- **URL**: `https://stat.gov.pl/api/`
- **Notes**: Complements BDL for some newer datasets

#### OpenBudget (Ministry of Finance)
- **URL**: `https://openbudget.gov.pl/api/`
- **Format**: JSON
- **Coverage**: Central government budget execution by year and chapter
- **Notes**: Data updated quarterly; good for revenue/expenditure breakdowns

#### NBP (National Bank of Poland)
- **URL**: `https://api.nbp.pl/api/`
- **Format**: JSON or XML
- **Docs**: `https://api.nbp.pl/`
- **Coverage**: Exchange rates (table A, B, C), interest rates, gold price

#### Eurostat
- **URL**: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{dataset_id}`
- **Format**: JSON-stat
- **Rate limit**: Generous, no key required
- **Notes**: Use `?format=JSON` param; pyjstat library helpful for parsing

#### NFZ (National Health Fund)
- **URL**: `https://dane.nfz.gov.pl/`
- **Format**: API available for some datasets
- **Notes**: API quality varies by dataset

#### MEN (Ministry of Education)
- **URL**: `https://www.gov.pl/web/edukacja/`
- **Format**: XLSX files, annual releases
- **Notes**: Manual download, import with pandas

### Level 2: Official Polish Institutional

#### KNF (Financial Supervision Authority)
- **URL**: `https://www.knf.gov.pl/dane_statystyczne`
- **Format**: XLSX, PDF
- **Notes**: No API; file download only

---

## DB Schema Convention

```
raw.{source}_{entity}     ← ingested data, preserve original structure
public.{domain}_{metric}  ← processed, analysis-ready
```

Examples:
- `raw.bdl_population` — raw GUS BDL population data
- `raw.eurostat_gdp` — raw Eurostat GDP data
- `public.demographics_population` — clean population for dashboards
