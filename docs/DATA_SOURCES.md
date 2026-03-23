# Open Reporting — Data Sources

Known public data sources, their access methods, and status.

## Tier 1: Free API, No Auth Required

### Eurostat
- **URL**: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{dataset_id}`
- **Format**: JSON-stat
- **Docs**: `https://wikis.ec.europa.eu/display/EUROSTATHELP/API+Statistics+-+data+query`
- **Rate limit**: Generous, no key required
- **Notes**: Use `?format=JSON` param; pyjstat library helpful for parsing

### OpenBudget (Ministry of Finance)
- **URL**: `https://openbudget.gov.pl/api/`
- **Format**: JSON
- **Coverage**: Central government budget execution by year and chapter
- **Notes**: Data updated quarterly; good for revenue/expenditure breakdowns

### NBP (National Bank of Poland)
- **URL**: `https://api.nbp.pl/api/`
- **Format**: JSON or XML
- **Docs**: `https://api.nbp.pl/`
- **Coverage**: Exchange rates (table A, B, C), interest rates, gold price

## Tier 2: Free API, Key Required

### GUS BDL (Local Data Bank)
- **URL**: `https://bdl.stat.gov.pl/api/v1/`
- **Auth**: `BDL_API_KEY` env var (register at `https://bdl.stat.gov.pl/`)
- **Format**: JSON
- **Coverage**: 40,000+ variables across all domains, NUTS-2/NUTS-3 regional data
- **Rate limit**: 1000 requests/day on free tier
- **Notes**: Variable IDs required; use `/variables` endpoint to discover

### GUS StatsAPI (newer, experimental)
- **URL**: `https://stat.gov.pl/api/`
- **Notes**: Complements BDL for some newer datasets

## Tier 3: File Downloads (No API)

### MEN (Ministry of Education)
- **URL**: `https://www.gov.pl/web/edukacja/`
- **Format**: XLSX files, annual releases
- **Notes**: Manual download, import with pandas

### NFZ (National Health Fund)
- **URL**: `https://dane.nfz.gov.pl/`
- **Format**: API available for some datasets
- **Notes**: API quality varies by dataset

### KNF (Financial Supervision Authority)
- **URL**: `https://www.knf.gov.pl/dane_statystyczne`
- **Format**: XLSX, PDF
- **Notes**: No API; scraping or manual download

## DB Schema Convention

```
raw.{source}_{entity}     ← ingested data, preserve original structure
public.{domain}_{metric}  ← processed, analysis-ready
```

Examples:
- `raw.bdl_population` — raw GUS BDL population data
- `raw.eurostat_gdp` — raw Eurostat GDP data
- `public.demographics_population` — clean population for dashboards
