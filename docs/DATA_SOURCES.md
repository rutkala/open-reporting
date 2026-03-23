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

#### GUS BDL (Local Data Bank)
- **URL**: `https://bdl.stat.gov.pl/api/v1/`
- **Auth**: `BDL_API_KEY` env var (register at `https://bdl.stat.gov.pl/`)
- **Format**: JSON
- **Coverage**: 40,000+ variables across all domains, NUTS-2/NUTS-3 regional data
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
