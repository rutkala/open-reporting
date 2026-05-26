# Knowledge Base: Data Research & Source Evaluation

**Module:** `docs/data-research/principles.md`
**Version:** 1.0 — April 2026
**Status:** Ready for use

Agent reference for evaluating data sources before ingestion — source discovery, API/file format analysis, data quality assessment, licence considerations, and indicator selection methodology. Read before any data ingestion task.

**Does not duplicate:** `data-engineering/engineering.md` (ELT, DuckDB, dbt patterns). This file covers the pre-ingestion phase: finding data, evaluating it, and deciding whether and how to ingest it.

**Sources:** Eurostat Quality Assurance Framework (ESS QAF v2.0); European Statistics Code of Practice; Eurostat Handbook on Data Quality Assessment Methods and Tools; GUS Quality Standards (metodologia.stat.gov.pl); Data Is Plural dataset criteria; DAMA-DMBOK Data Quality dimensions (accuracy, completeness, consistency, timeliness, uniqueness, validity); Open Data Charter principles; OECD Data Quality Framework.

---

## 1. Source Discovery

### 1.1 Primary Data Sources for Polish Public Data

| Source | Coverage | Format | Update frequency | Access |
|--------|----------|--------|-----------------|--------|
| **GUS BDL** (Bank Danych Lokalnych) | Regional and national statistics across all domains | API (REST), web interface, Excel | Monthly/quarterly/annual per series | Free, registration required for API |
| **GUS publications** | Detailed statistical reports, yearbooks | PDF, Excel, CSV | Monthly/quarterly/annual | Free download |
| **Eurostat** | EU-wide statistics, cross-country comparisons | API (SDMX), bulk download, JSON | Monthly/quarterly/annual | Free, open |
| **NBP** (National Bank of Poland) | Monetary policy, exchange rates, interest rates, banking sector | API (REST), CSV, XML | Daily/monthly | Free, open |
| **MF** (Ministry of Finance) | Public finance, budget execution, tax revenue | CSV, Excel, API | Monthly/annual | Free, open |
| **ZUS** (Social Insurance Institution) | Social security, employment, contributions | Reports (PDF, Excel) | Monthly/quarterly | Free download |
| **Open Data portals** (dane.gov.pl) | Various government datasets | CSV, JSON, API | Varies | Free, open |

### 1.2 Source Evaluation Criteria

Before ingesting any data source, evaluate it against these criteria:

| Criterion | Question | Red flag |
|-----------|----------|----------|
| **Authority** | Is the source an official statistical office, central bank, ministry, or recognised international organisation? | Blog, think tank, or commercial source as primary data |
| **Methodology transparency** | Is the methodology documented? Are definitions, sampling methods, and limitations described? | No methodology note or methodological report available |
| **Update regularity** | Is there a published release calendar? Has the source maintained its schedule historically? | Irregular updates, gaps in time series without explanation |
| **Data format** | Is the data available in a machine-readable format (CSV, JSON, API, Parquet)? | PDF-only, scanned images, proprietary formats without open specification |
| **Historical depth** | How far back does the time series go? Is it consistent over time? | Short history (< 3 years for annual data, < 2 years for monthly) |
| **Granularity** | What is the finest level of disaggregation (time, geography, demographic)? | Only national aggregates when regional or demographic breakdown is needed |
| **Revision policy** | Does the source publish revisions? Is the revision policy documented? | Data is silently revised without notification |
| **Licence** | Is the data openly licensed for reuse? Are there attribution requirements? | No licence stated; restrictive terms; commercial use prohibited |

### 1.3 Source Authority Hierarchy

| Level | Source type | Examples | Use for |
|-------|------------|----------|---------|
| **Tier 1 — Official statistics** | National statistical offices, central banks, EU institutions | GUS, NBP, Eurostat, ECB | Primary data for all dashboards and analysis |
| **Tier 2 — Government administrative data** | Ministries, agencies, local government | MF budget data, ZUS reports, PUP data | Supplementary data; note definitional differences from official statistics |
| **Tier 3 — International organisations** | IMF, World Bank, OECD, ILO | World Development Indicators, OECD.Stat | Cross-country benchmarks, methodological harmonisation |
| **Tier 4 — Academic and research** | University datasets, research institutes | NBER, CEIC, academic compilations | Contextual analysis; not primary data for dashboards |
| **Tier 5 — Commercial and media** | Bloomberg, Reuters, news aggregators | Market data, news reports | Not used as primary data; may provide leads |

**Rule:** Always prefer Tier 1 over Tier 2 for the same concept. If Tier 1 and Tier 2 disagree (e.g., GUS LFS vs. PUP registered unemployment), use both but clearly label the definitional difference.

---

## 2. Data Quality Assessment

### 2.1 DAMA Data Quality Dimensions

Apply all six DAMA dimensions to every new data source:

| Dimension | What it means | How to check |
|-----------|--------------|-------------|
| **Accuracy** | Does the data correctly represent the real-world entity? | Cross-check a sample against the published source; verify calculations |
| **Completeness** | Are all expected records and fields present? | Check for nulls, missing periods, missing geographies; compare row count to source documentation |
| **Consistency** | Is the data internally consistent and consistent with related sources? | Check that subtotals sum to totals; verify that related series (e.g., employment + unemployment = labour force) are consistent |
| **Timeliness** | Is the data available within the expected time after the reference period? | Compare data vintage to reference period; check against the source's published release calendar |
| **Uniqueness** | Are there duplicate records? | Check for duplicate primary keys; verify that each observation appears once |
| **Validity** | Do values conform to expected ranges and formats? | Check for out-of-range values (negative population, unemployment > 100%), incorrect date formats, invalid codes |

### 2.2 Quality Flagging System

Every ingested dataset should carry quality flags:

| Flag | Meaning | Action |
|------|---------|--------|
| **GREEN** | All six DAMA dimensions pass; source is Tier 1; methodology documented | Proceed with ingestion |
| **YELLOW** | One or two dimensions have minor issues (e.g., short history, limited granularity) | Proceed with ingestion; document the limitation in the catalogue |
| **RED** | Critical issues: no methodology, unreliable source, licence unclear, data integrity problems | Do not ingest; escalate to lead analyst |

### 2.3 API vs. File Assessment

| Factor | API preferred | File preferred |
|--------|--------------|---------------|
| **Update frequency** | Daily or more frequent | Monthly or less frequent |
| **Data volume** | Small to medium (incremental fetches) | Large bulk downloads |
| **Rate limits** | Generous or no limits | N/A |
| **Authentication** | Simple API key or open access | N/A |
| **Versioning** | API supports versioned endpoints | Files are versioned by date |
| **Reliability** | API has SLA or uptime history | Files are archived and permanent |

**Rule:** If both API and file access are available, prefer API for automated ingestion and file for initial bulk load and backup verification.

---

## 3. Licence Considerations

### 3.1 Common Licences for Public Data

| Licence | Can reuse? | Can modify? | Can distribute? | Attribution required? | Commercial use? |
|---------|-----------|------------|----------------|---------------------|----------------|
| **Public domain / CC0** | Yes | Yes | Yes | No (recommended) | Yes |
| **CC BY 4.0** | Yes | Yes | Yes | Yes | Yes |
| **CC BY-SA 4.0** | Yes | Yes | Yes (same licence) | Yes | Yes |
| **CC BY-NC 4.0** | Yes | Yes | Yes | Yes | No |
| **Open Government Licence (OGL)** | Yes | Yes | Yes | Yes | Yes |
| **EU Open Data Portal licence** | Yes | Yes | Yes | Yes (source + date) | Yes |
| **GUS statistics** | Yes (Polish law) | Yes | Yes | Yes (source) | Yes |
| **No licence stated** | Unclear | Unclear | Unclear | — | — |

### 3.2 Licence Assessment Rules

- **GUS data** — Polish statistical law permits reuse of official statistics with source attribution. No separate licence needed.
- **Eurostat data** — Covered by EU Open Data Portal licence (CC BY 4.0 equivalent). Free to reuse with attribution.
- **NBP data** — Free to reuse with source attribution.
- **MF data** — Open data; free to reuse.
- **No licence stated** — Contact the source owner for clarification before ingestion. Do not assume open access.
- **CC BY-NC (non-commercial)** — Open Reporting is a data media company; assess whether the use is commercial. When in doubt, seek legal advice.

### 3.3 Attribution Requirements

Every dataset ingested must record:
- **Source name** — the publishing organisation
- **Source URL** — the page where the data was obtained
- **Licence** — the specific licence under which the data is published
- **Access date** — when the data was fetched
- **Attribution text** — the exact attribution string required by the licence (e.g., "Źródło: GUS, Bank Danych Lokalnych")

---

## 4. Indicator Selection Methodology

### 4.1 From Data to Indicators

Not every data series is worth ingesting. Use this filter:

| Filter | Question | Outcome |
|--------|----------|---------|
| **Relevance** | Does this series answer a question that our audience cares about? | If no → skip |
| **Availability** | Is the data from a Tier 1 or Tier 2 source with documented methodology? | If no → flag as YELLOW or RED |
| **Regularity** | Is the data updated on a predictable schedule? | If no → consider one-time ingestion only |
| **Comparability** | Can this series be compared to benchmarks (EU average, prior year, peer group)? | If no → limited analytical value |
| **Actionability** | Would showing this data help a reader understand or decide something? | If no → interesting but not essential |

### 4.2 Indicator Prioritisation

| Priority | Criteria | Examples |
|----------|----------|---------|
| **P1 — Essential** | Official statistic, regular update, high audience relevance, benchmarkable | Unemployment rate, GDP growth, inflation, fiscal deficit |
| **P2 — Important** | Official statistic, regular update, moderate audience relevance | Regional employment, sectoral wages, public debt composition |
| **P3 — Useful** | Official statistic, irregular update, niche audience relevance | Detailed demographic breakdowns, specialised surveys |
| **P4 — Optional** | Non-official source, or low relevance, or unclear methodology | Commercial surveys, academic compilations, media aggregations |

### 4.3 Structural Break Documentation

For every indicator, document known structural breaks:

| Break type | Example | Documentation requirement |
|-----------|---------|--------------------------|
| **Methodology change** | GUS BAEL mode change 2021 | Note the break date, old vs. new definition, whether back-cast is available |
| **Classification change** | NACE Rev. 1 → Rev. 2 | Note the mapping table if available |
| **Geographic change** | Municipal boundary changes | Note affected geographies |
| **Currency change** | PLN redenomination 1995 | Note the conversion factor |
| **EU integration** | ESA 2010 adoption | Note the revision magnitude if available |

---

## 5. Output Format: Source Research Summary

Every source research task produces a structured summary:

```yaml
source:
  name: "Statistics Poland (GUS)"
  url: "https://stat.gov.pl"
  tier: 1
  access_method: "API (BDL) + Excel downloads"
  api_endpoint: "https://bdl.stat.gov.pl/BDL/api"
  requires_auth: true

data_series:
  - name: "Stopa bezrobocia rejestrowanego"
    english_name: "Registered unemployment rate"
    source_code: "BDL series code"
    frequency: "monthly"
    historical_depth: "1990-present"
    granularity: "national, voivodeship, powiat"
    revision_policy: "Preliminary → final; documented"
    structural_breaks:
      - date: "2021-01"
        description: "BAEL methodology change (CAPI/CAWI mode shift)"
    quality_flags:
      accuracy: GREEN
      completeness: GREEN
      consistency: GREEN
      timeliness: GREEN
      uniqueness: GREEN
      validity: GREEN
    priority: P1
    licence: "Polish statistical law — reuse with attribution"
    attribution: "Źródło: GUS, Bank Danych Lokalnych"

recommendation: "Proceed with ingestion. Monthly registered unemployment from GUS BDL is a Tier 1 source with full documentation, regular updates, and clear licence. Note the 2021 methodology break in the catalogue."
```
