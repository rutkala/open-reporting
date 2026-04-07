# Ingestion Standard

**Derived from:** `team/knowledge-base/data-engineering/engineering.md` ✓ (ELT principle, DuckDB read_csv/TRY_CAST/upsert/fetched_at, Python ETL standards, DAMA quality dimensions)
**Used by builders:** `data-architect` (writing scripts in `platform/ingestion/`)
**Evaluated by:** `code-reviewer`, `data-engineer-reviewer` (PR-phase)
**Does NOT cover:** transformation logic (see `processing.md`), schema design (see `storage.md`), semantic layer (see `measures.md`)

---

## Pipeline Architecture

Open Reporting uses **ELT (Extract → Load → Transform)**:

```
catalogue.domain_detail_sources (verified=true)
      ↓  series_id confirmed
Source API / file
      ↓
Extract (Python script)
      ↓
raw.{source}_{entity}       ← untouched, native format, PostgreSQL
      ↓
Transform (dbt / SQL)
      ↓
curated.{domain}_{metric}   ← clean, structured, analysis-ready
      ↓
Dashboard
```

Raw data is never modified after landing. Transformations always run from raw, not from curated. This means data can be re-transformed at any time if definitions change.

---

## Phase 0: Catalogue Verification (REQUIRED BEFORE ANY CODE)

Before writing a single line of ingestion code, the catalogue must be in a verified state for the indicator and source being built.

**Step 1 — Confirm the detail exists in `catalogue.domain_details`:**
```sql
SELECT detail_id, name, unit, frequency, detail_type, entity_level
FROM catalogue.domain_details
WHERE detail_id = '{detail_id}';
```
If missing: add the row to `platform/database/data/domain_details.csv` and re-run the loader.

**Step 2 — Confirm the source mapping exists and is verified in `catalogue.domain_detail_sources`:**
```sql
SELECT detail_id, source_id, series_id, verified, coverage_notes
FROM catalogue.domain_detail_sources
WHERE detail_id = '{detail_id}' AND source_id = '{source_id}';
```
- If the row is missing: add it to `platform/database/data/domain_detail_sources.csv`
- If `verified = false` or `series_id IS NULL`: **stop here**. Find the exact series in the source (endpoint, dataset code, variable ID), test it, then update the CSV:
  - Set `series_id` to the exact locator (see format per source type below)
  - Set `verified = true`
  - Re-run the catalogue loader
- Only proceed to Phase 1 once `verified = true` and `series_id` is populated

**`series_id` format by source type:**

| Source type | Format | Example |
|-------------|--------|---------|
| REST API (NBP, PSE, GIOS) | `endpoint_path?key=value` | `exchangerates/rates/A/USD` |
| SDMX API (Eurostat, ECB, ILO) | `dataset_code?filter_expression` | `une_rt_m?geo=PL&s_adj=SA&age=TOTAL&unit=PC_ACT&sex=T` |
| BDL API | `variables/{variable_id}` | `variables/72305` |
| XLSX / CSV file | `filename::sheet::column_header` | `bezrobocie_miesiac.xlsx::Tabl.1::Stopa bezrobocia` |
| HTML/report (tier-3) | `report_url#section` | `https://www.pmi.spglobal.com/...#manufacturing-pl` |

---

## Phase 1: Source Selection

Source authority is defined in the catalogue (`catalogue.sources`, tier column):
- Tier 1 — API sources: preferred; can be automated
- Tier 2 — File downloads (XLSX/CSV): acceptable; requires landing zone step
- Tier 3 — Reports/HTML: last resort; manual extraction only

No scraping. No undocumented commercial data providers. API or official file download only. If a source is not in `catalogue.sources`, add it there first.

**Check for bulk download before designing an API pipeline.**
Many official sources (GUS DBW, Eurostat) publish complete dataset exports as CSV/ZIP alongside their APIs. A bulk download loads the full dataset in seconds; a paginated API loop for the same data can take hours. Always check the source's download/export page before writing an API ingestion script.

**GUS DBW bulk CSV: `no_value_id` semantics differ from the REST API.**
The REST API uses `no_value_id=0` to mean "data exists" (non-zero = suppressed/missing). The bulk CSV export only includes rows where data exists — `no_value_id` is never 0. Do not apply a `!= 0 → NULL` filter on bulk CSV loads; just cast the value directly with `TRY_CAST`.

---

## Phase 2: Extraction Tool

**Default: custom Python scripts**
- Libraries: `requests`, `pandas`, `psycopg2`, `python-dotenv`
- One script per data source: `ingestion/{source}_ingest.py`
- Document the tool choice in the script docstring

**Alternative: dlt (data load tool)**
- Consider when: source has a native dlt connector, or source is complex (pagination, auth, retries)
- Document why dlt was chosen over plain Python

**DuckDB bulk CSV load (for landing zone → raw)**
When loading multiple CSV files into DuckDB, use the native `read_csv` glob — never Python row iteration:
```python
conn.execute(f"""
    INSERT OR REPLACE INTO raw.{table} (col1, col2, value, fetched_at)
    SELECT col1, col2, value, NOW()
    FROM read_csv(
        '{landing_dir}/*.csv',
        delim=';', header=true, ignore_errors=true,
        columns={{'col1': 'INTEGER', 'col2': 'VARCHAR', 'value': 'VARCHAR'}}
    )
""")
```
DuckDB reads all matching files in a single SQL operation. Python `csv.DictReader` + `executemany` for the same data is orders of magnitude slower and should not be used for bulk loads.

---

## Phase 3: Update Method

Choose the appropriate method per dataset and document it in the script:

| Method | When to use | How |
|--------|------------|-----|
| **Upsert (merge)** | Default for most cases | `ON CONFLICT DO UPDATE` |
| **Incremental append** | Large datasets, source supports it | Append new records only, track last loaded date |
| **Full load** | Small datasets, no incremental support | Truncate + reload |
| **Overwrite** | Explicit justification required | Destructive — document why |

---

## Phase 4: Raw Loading Rules

- Land data in `raw.{source}_{entity}` — preserve original structure
- No business logic during extraction
- Minor cleaning allowed: strip whitespace, fix encoding, parse dates
- Always include `fetched_at TIMESTAMPTZ DEFAULT NOW()`
- Always include original source identifier columns
- Structured data → typed columns in PostgreSQL
- Semi-structured data (nested JSON) → `JSONB` column, parse in transform phase
- Unstructured data (PDFs, documents) → file storage, not DB (approach TBD when needed)

---

## Phase 5: Transform Rules

Transformations run as separate scripts in `processing/`:
- Input: `raw.` schema
- Output: `public.{domain}_{metric}` schema
- Idempotent — safe to run multiple times
- No side effects on raw data
- Document the transformation logic in the script docstring

---

## Phase 6: Validation Checklist

Run after every ingestion, before marking complete:
- [ ] `catalogue.domain_detail_sources` row exists with `verified=true` and `series_id` populated
- [ ] Row count matches expected range
- [ ] Date ranges complete — no unexpected gaps
- [ ] Spot-check 3-5 values against source website
- [ ] No nulls in required columns
- [ ] All validation results logged at `info` level

---

## Script Structure

```python
#!/usr/bin/env python3
"""
Ingestion: {Source Name}
Tool: Python / requests | dlt
API / File: {URL or path}
Update method: upsert | incremental | full load
Schema: raw.{source}_{entity}
Catalogue:
  detail_id  : {detail_id}          (catalogue.domain_details)
  source_id  : {source_id}          (catalogue.sources)
  series_id  : {series_id}          (catalogue.domain_detail_sources — verified=true)
Usage: PYTHONPATH=/opt/open-reporting python3 platform/ingestion/to_raw/{name}_ingest.py [--backfill]
"""
import logging
import os
import sys
import argparse
import requests
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

DSN = f"postgresql://postgres:{os.environ['POSTGRES_PASSWORD']}@localhost:5432/open_reporting"

def fetch(params: dict) -> list[dict]:
    response = requests.get(API_BASE, params=params, timeout=30)
    response.raise_for_status()
    return response.json()["data"]

def upsert(conn, rows: list[tuple]) -> int:
    cur = conn.cursor()
    execute_values(cur, """
        INSERT INTO raw.{table} (col1, col2, value, fetched_at)
        VALUES %s
        ON CONFLICT (col1, col2) DO UPDATE SET
            value = EXCLUDED.value,
            fetched_at = EXCLUDED.fetched_at
    """, rows)
    conn.commit()
    return cur.rowcount

def validate(conn) -> None:
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*), MIN(year), MAX(year) FROM raw.{table}")
    count, min_year, max_year = cur.fetchone()
    log.info(f"Validation: {count} rows, years {min_year}–{max_year}")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--backfill", action="store_true")
    args = parser.parse_args()

    conn = None
    try:
        conn = psycopg2.connect(DSN)
        data = fetch({"year": 2024})
        rows = [(r["id"], r["name"], r["value"]) for r in data]
        count = upsert(conn, rows)
        log.info(f"Upserted {count} rows")
        validate(conn)
    except Exception:
        log.exception("Ingestion failed")
        sys.exit(1)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
```

---

## Scheduling

- Default: manual trigger
- Scheduled refresh: cron job
- Schedule defined per dataset — document in script header; frequency must match `catalogue.domain_details.frequency` for the indicator
