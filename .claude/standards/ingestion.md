# Ingestion Standard

## Pipeline Architecture

Open Reporting uses **ELT (Extract → Load → Transform)**:

```
Source API / file
      ↓
Extract (Python script)
      ↓
raw.{source}_{entity}       ← untouched, native format, PostgreSQL
      ↓
Transform (Python / SQL)
      ↓
public.{domain}_{metric}    ← clean, structured, analysis-ready
      ↓
Dashboard
```

Raw data is never modified after landing. Transformations always run from raw, not from public. This means data can be re-transformed at any time if definitions change.

---

## Phase 1: Source Selection

Follow the hierarchy defined in `docs/DATA_SOURCES.md`:
1. Level 1 — Official government and EU (GUS, Eurostat, NBP, OpenBudget)
2. Level 2 — Official Polish institutional (KNF, ZUS, GDDKiA)
3. Level 3 — Trusted international (World Bank, IMF, OECD)
4. Level 4 — Requires explicit user approval

No scraping. No commercial data providers. API or official file download only.

---

## Phase 2: Extraction Tool

**Default: custom Python scripts**
- Libraries: `requests`, `pandas`, `psycopg2`, `python-dotenv`
- One script per data source: `ingestion/{source}_ingest.py`
- Document the tool choice in the script docstring

**Alternative: dlt (data load tool)**
- Consider when: source has a native dlt connector, or source is complex (pagination, auth, retries)
- Document why dlt was chosen over plain Python

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
Tool: Python / requests
API: {API URL}
Update method: upsert / incremental / full load
Schema: raw.{source}_{entity}
Usage: python3 ingestion/{name}_ingest.py [--backfill]
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
- Scheduled refresh: cron job (follow pattern from `nginx/renew-certs.sh`)
- Schedule defined per dataset — document in script header and in `docs/DATA_SOURCES.md`
