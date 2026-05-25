# Data Engineering Knowledge Base

**Agent reference for data pipeline design, SQL standards, DuckDB patterns, dbt conventions, and data quality.**
Read during `/plan` for any ingestion, processing, or warehouse task. Read during `/review` for the data engineering layer.

**Sources:** dbt Labs Developer Hub (docs.getdbt.com), DuckDB Documentation (duckdb.org), Real Python "Preventing SQL Injection Attacks", DAMA "Dimensions of Data Quality Research Paper" v1.2 (2020), Start Data Engineering "Why and How: Idempotent Data Pipelines", Meltano ELT 101, MotherDuck DuckDB Book, Collibra "6 Dimensions of Data Quality", Fivetran "ETL vs ELT".

---

## 1. ELT vs ETL — Why Load Raw First

### 1.1 The Fundamental Difference

ETL (Extract → Transform → Load) transforms data before it enters the warehouse. The transformation logic lives outside the warehouse — in a staging server, Spark job, or Python script — and only the shaped result is persisted.

ELT (Extract → Load → Transform) inverts the order: raw data is loaded immediately into the warehouse, untouched. Transformation happens inside the warehouse using SQL, dbt, or equivalent tools, operating on the persisted raw copy.

The modern default — and the architecture of this project — is ELT. The reasons are not stylistic; they are about correctness, debuggability, and reversibility.

### 1.2 Why ELT Is Correct for This Project

**Data preservation.** In ETL, if the transformation logic is wrong, the raw data may be gone — you cannot re-derive it without re-extracting from the source. In ELT, the raw copy is always available. Any transformation can be rerun from the source of truth at any time. This is the single most important operational property of the architecture.

**Separation of concerns is structurally enforced.** Extraction is a network I/O problem (reliability, retries, authentication). Transformation is a business logic problem (definitions, calculations, grain). In ELT, these are separate scripts with separate responsibilities and separate failure modes. Mixing them — performing transformation in the ingestion script — means a business logic change requires editing the script that talks to the network, which is a source of regression and confusion.

**Debuggability.** When a curated value is wrong, the raw layer lets you audit exactly what the source delivered. Without it, you cannot distinguish a source data problem from a transformation bug.

**Re-transformation without re-extraction.** As business definitions evolve (e.g., a KPI calculation changes), you rerun dbt against unchanged raw data. You do not need to call the external API again, which may have changed, rate-limited you, or disappeared.

**Transformation logic belongs in dbt, not ingestion scripts.** This is a hard rule with an architectural rationale: ingestion scripts talk to external systems and must be minimally complex. Every line of transformation logic in an ingestion script is logic that is not version-controlled in dbt, not testable with `dbt test`, not documented in the dbt DAG, and not runnable without re-triggering an external call. The ingestion boundary is: land data, nothing more.

### 1.3 What "No Business Logic in Ingestion" Means in Practice

Permitted in ingestion scripts:
- Stripping whitespace, fixing encoding
- Parsing well-known date formats into native types
- Casting obviously numeric strings to numbers (where no domain knowledge is required)
- Adding `fetched_at` metadata

Not permitted in ingestion scripts:
- Filtering rows based on domain criteria ("only active indicators")
- Deriving new columns (ratios, period offsets, category mappings)
- Joining to reference tables or the catalogue
- Applying business rules about what constitutes a valid value

The boundary is: if the decision requires knowledge of what the data means, it belongs in dbt.

---

## 2. DuckDB-Specific Patterns

### 2.1 Why DuckDB Outperforms Traditional RDBMS for Analytical Workloads

DuckDB uses columnar storage and vectorised execution. For analytical queries — aggregations over millions of rows, filtering on a handful of columns out of many — this produces dramatic performance advantages over row-oriented databases (PostgreSQL, MySQL):

- **Column pruning:** Only the columns referenced in the query are read from disk. A `SELECT year, value FROM raw.bdl_population` on a 50-column table reads 2 columns' storage pages, not 50.
- **Vectorised execution:** Rather than processing one row at a time, DuckDB processes batches of 1,024–2,048 values per column in tight CPU loops. This exploits modern CPU caches and SIMD instructions.
- **Predicate pushdown on Parquet:** When reading from `.parquet` files, DuckDB pushes `WHERE` clauses into the file reader — it skips row groups that cannot satisfy the predicate without reading them.
- **In-process:** No client-server round trips. The query runs in the same process as the Python script.

Use DuckDB for: analytical queries on the warehouse, reading CSV/Parquet landing files, bulk loads from landing to raw, all dbt models. Use PostgreSQL for: the operational catalogue, Ghost CMS data, any transactional workload with concurrent writes.

### 2.2 Reading Landing Files — Use Native File Functions

Never read CSV or Parquet files with Python iteration and then insert row-by-row. DuckDB's native file functions push the entire operation into the DuckDB engine:

```python
# Correct — single SQL operation, vectorised
conn.execute("""
    INSERT OR REPLACE INTO raw.gus_population (region_code, year, value, fetched_at)
    SELECT region_code, CAST(year AS INTEGER), TRY_CAST(value AS DOUBLE), NOW()
    FROM read_csv(
        '/opt/open-reporting/data/landing/population/*.csv',
        delim=';', header=true, ignore_errors=true,
        columns={'region_code': 'VARCHAR', 'year': 'VARCHAR', 'value': 'VARCHAR'}
    )
""")

# Wrong — Python row iteration is orders of magnitude slower
with open(path) as f:
    for row in csv.DictReader(f):
        conn.execute("INSERT INTO ...", (row['region_code'], ...))
```

The same applies to Parquet: `SELECT * FROM read_parquet('file.parquet')` is the correct entry point.

### 2.3 Upsert Pattern — ON CONFLICT DO UPDATE

DuckDB supports PostgreSQL-style upsert. The conflict target must be a column with a UNIQUE constraint or PRIMARY KEY:

```sql
INSERT INTO raw.eurostat_indicators (detail_id, geo, time_period, value, fetched_at)
VALUES (?, ?, ?, ?, NOW())
ON CONFLICT (detail_id, geo, time_period) DO UPDATE SET
    value     = EXCLUDED.value,
    fetched_at = EXCLUDED.fetched_at
```

DuckDB-specific caveats (confirmed against issue tracker):
- `current_timestamp` cannot be used in the UPDATE SET clause of ON CONFLICT — use `NOW()` or pass the timestamp as a parameter.
- If you need to update the conflict key column itself, use `MERGE` instead — updating the conflict column in an ON CONFLICT clause can produce NULLs in other columns (known DuckDB bug as of 2025).
- For complex upsert logic (conditional updates, multiple matched clauses), prefer `MERGE ... WHEN MATCHED THEN UPDATE / WHEN NOT MATCHED THEN INSERT`.

### 2.4 Data Types — Rules for This Project

| Situation | Type | Rationale |
|-----------|------|-----------|
| Surrogate keys, row counts, population figures | `BIGINT` | INTEGER overflows at ~2.1B rows; BIGINT never does |
| Natural/source IDs of unknown range | `BIGINT` | Defensive — source ID ranges often grow beyond initial expectations |
| Rates, percentages, ratios | `DOUBLE` | Acceptable precision for analytical queries; use `NUMERIC` only when rounding must be exact (financial) |
| Financial values requiring exact rounding | `DECIMAL(18,2)` | Floating-point arithmetic on financial figures is a correctness bug |
| Audit/ingestion timestamps | `TIMESTAMPTZ` | Always timezone-aware; store in UTC, convert to Europe/Warsaw for display only |
| Period dates (year, month, quarter) | `INTEGER` year or `DATE` first-day-of-period | Never store as VARCHAR — prevents date arithmetic |
| Boolean flags | `BOOLEAN` | Not `INTEGER 0/1`; DuckDB handles `TRUE`/`FALSE` natively |

### 2.5 The `fetched_at` Column Convention

Every raw table carries a `fetched_at TIMESTAMPTZ DEFAULT NOW()` column. Its purpose:

1. **Audit trail** — when was this row fetched from the source? Distinct from `period_date` (what time period the data describes) and `updated_at` (when the curated record last changed).
2. **Incremental load support** — `MAX(fetched_at)` in the raw table is the high-watermark for incremental loads.
3. **Debugging** — when a value looks wrong, `fetched_at` shows which ingestion run produced it.

`fetched_at` is always the ingestion timestamp, never the source's publication date. The source's publication date, if available, goes in a separate `published_at` or `reference_date` column.

### 2.6 TRY_CAST vs CAST

In DuckDB, `CAST(x AS INTEGER)` raises an error on failure. `TRY_CAST(x AS INTEGER)` returns NULL. Use `TRY_CAST` everywhere in raw-layer SQL — raw data is not guaranteed to be clean. Reserve `CAST` for curated-layer SQL where the type has already been validated.

---

## 3. dbt Conventions

### 3.1 Model Layer Architecture

```
sources (defined in sources.yml)
    ↓ SELECT FROM source()
stg_{source}.sql          ← Staging: one per source, atomic conforming
    ↓ SELECT FROM ref()
int_{domain}_{entity}.sql ← Intermediate: joins, aggregations (optional layer)
    ↓ SELECT FROM ref()
mart_{domain}.sql          ← Mart/gold: final analytical grain, dashboard-ready
```

The staging → (intermediate) → mart progression is not optional styling. It is a structural rule that enforces data lineage. Every model that reads from raw uses `{{ source() }}`. Every model that reads from another dbt model uses `{{ ref() }}`. This is how dbt builds the DAG and enforces execution order.

### 3.2 Staging Model Rules (stg_{source}.sql)

Staging models are the **only** models that reference raw source tables. They perform one function: conform the raw schema to the shared fact schema.

Permitted in staging:
- Renaming columns to project-standard names
- Type casting with `TRY_CAST`
- `COALESCE` for null handling
- Filtering rows with no usable `detail_id` mapping
- Adding `source_name` constant for lineage

Not permitted in staging:
- Joining to other models or reference tables
- Aggregations or window functions
- Business logic calculations
- `GROUP BY` or `HAVING`

```sql
-- stg_eurostat.sql
SELECT
    detail_id_mapped                                AS detail_id,
    TRY_CAST(geo_code AS VARCHAR)                  AS geo_code,
    TRY_CAST(time_period AS INTEGER)               AS year,
    TRY_CAST(obs_value AS DOUBLE)                  AS value,
    unit_label                                      AS unit,
    fetched_at,
    'eurostat'                                      AS source_name
FROM {{ source('raw', 'eurostat_indicators') }}
WHERE detail_id_mapped IS NOT NULL
```

### 3.3 Source Definitions and Tests (sources.yml)

Every raw table used by dbt must be declared in `sources.yml`. This is where source freshness checks, column-level tests, and documentation live.

```yaml
sources:
  - name: raw
    database: open_reporting
    schema: raw
    tables:
      - name: eurostat_indicators
        description: "Raw Eurostat SDMX data — one row per indicator × geo × period"
        loaded_at_field: fetched_at
        freshness:
          warn_after: {count: 7, period: day}
          error_after: {count: 30, period: day}
        columns:
          - name: detail_id_mapped
            description: "Mapped detail_id from catalogue"
          - name: obs_value
            tests:
              - not_null:
                  where: "unit_multiplier = 1"
```

### 3.4 dbt Tests — Required vs Optional

| Test | Applies to | Severity |
|------|-----------|----------|
| `not_null` | All primary key columns | Required |
| `unique` | Primary key or natural key columns | Required |
| `accepted_values` | Categorical dimension columns | Required where finite set is known |
| `relationships` | Foreign keys to reference models | Required |
| `not_null` on measure columns | Optional — often legitimately null | Optional, use `where` clause if partial |

Define tests in `schema.yml` co-located with models. A model with no tests is incomplete.

### 3.5 Incremental vs Full Refresh — Decision Rule

| Data pattern | Strategy | Rationale |
|-------------|----------|-----------|
| Immutable event log (new rows only, no updates) | `incremental` + `append` | No risk of duplicates; fast |
| Slowly changing dimensions, fact updates possible | `incremental` + `merge` (unique_key required) | Handles updates without full rewrite |
| Small reference/lookup tables | `table` (full refresh every run) | Simpler; the cost of full refresh is trivial |
| Large historical dataset, data arrives by partition | `incremental` + `delete+insert` | Replaces whole partition atomically; handles late-arriving corrections |
| Any model after a definition change | `dbt run --full-refresh` | Forces complete rewrite from source |

Always set `unique_key` on incremental models. Without it, rerunning the model produces duplicates. For this project (annual/monthly statistical data), `merge` strategy with `unique_key: [detail_id, geo_code, year]` is the default.

### 3.6 Seeds

Seeds (`/seeds/*.csv`) are for small, stable reference datasets: NUTS code → region name mappings, currency codes, indicator classification trees. Seeds are version-controlled in the repo and loaded with `dbt seed`. They are not appropriate for data that changes frequently or is larger than a few thousand rows.

### 3.7 SQL Style in dbt Models

Following dbt Labs SQL style guide (docs.getdbt.com/best-practices/how-we-style/2-how-we-style-our-sql):

- Keywords in UPPERCASE: `SELECT`, `FROM`, `WHERE`, `JOIN`, `LEFT JOIN`, `GROUP BY`
- One column per line, comma-first style or trailing-comma — be consistent within the project (trailing comma is the project default)
- Alias all columns with meaningful names, not source column names when they differ from the standard schema
- Primary key named `<entity>_id` (e.g. `indicator_id`, `region_id`)
- Timestamp columns named `<event>_at` (e.g. `fetched_at`, `created_at`)
- Date columns named `<event>_date` (e.g. `period_date`, `reference_date`)
- Boolean columns named `is_<condition>` (e.g. `is_active`, `is_revised`)
- Aggregations after field list, not before
- CTEs preferred over subqueries for readability; each CTE named for what it represents

---

## 4. Idempotency

### 4.1 Definition

A pipeline is idempotent if running it multiple times produces the same result as running it once. Concretely: re-running a full ingestion and transformation pipeline on a table that already contains the data should leave the table identical to its state after the first run.

Idempotency is not a nice-to-have. It is an operational requirement: pipelines fail, are rerun for backfills, are triggered multiple times due to scheduler bugs, and must be tested by running them against existing data. A non-idempotent pipeline accumulates duplicates, corrupts aggregates, and produces silent wrong answers.

### 4.2 Strategies and When to Use Each

**Truncate-Insert (Full Load)**
Delete all rows from the target, then insert the full dataset.
- Simple, always correct, no key required.
- Appropriate for: small tables (< 100K rows), reference/lookup data, tables where the full history is always re-fetched.
- Not appropriate for: large tables, tables that cannot be fully re-fetched from source, tables where availability of the target during truncation matters.

```sql
-- DuckDB full load pattern
DELETE FROM raw.nuts_reference;
INSERT INTO raw.nuts_reference SELECT * FROM read_csv('landing/nuts.csv');
```

**Upsert (INSERT ON CONFLICT DO UPDATE)**
Insert new rows; update existing rows where the natural key matches.
- Correct for most time-series data from APIs.
- Requires a natural key (unique constraint on the target table).
- Does not remove rows that were deleted from the source — for source deletions, use delete-insert on a partition.
- Appropriate for: most raw API loads, curated table updates from dbt.

**Delete-Insert on a Partition**
Delete all rows for a specific partition (e.g. a year, a month), then insert the new data for that partition.
- Handles source corrections within a partition without touching other partitions.
- Appropriate for: large datasets where full reload is impractical but source data for a period can be fully re-fetched.

```sql
-- Delete-insert pattern for a year partition
DELETE FROM raw.bdl_population WHERE year = ?;
INSERT INTO raw.bdl_population SELECT ..., NOW() FROM read_csv(...);
```

**dbt `--full-refresh`**
Forces dbt to drop and recreate the target table from source. Equivalent to truncate-insert for dbt models. Use after logic changes to ensure old materialization is gone.

### 4.3 The Key Insight: Partition Your Idempotency Scope

A common mistake is trying to make an entire multi-year historical load idempotent at the row level. The better design is to partition the idempotency scope: each run is responsible for a specific time window (a year, a month). Within that window it truncates-and-inserts. This combines simplicity (no natural key required) with safety (only affects the current window).

---

## 5. Python ETL Conventions — Rules and Rationale

### 5.1 Imports and Initialisation

```python
#!/usr/bin/env python3          # Required on all directly-runnable scripts
"""
Module docstring — purpose, source, schema, usage.
"""
# stdlib
import logging
import os
import sys

# third-party
import requests
import duckdb
from dotenv import load_dotenv

# local
from platform.warehouse.connection import get_conn

load_dotenv(override=True)      # Must be BEFORE any os.getenv() call
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
```

**`load_dotenv(override=True)` before any `os.getenv()`**: `load_dotenv()` without `override=True` does not replace env vars already set in the process environment. In Docker and systemd contexts, env vars may already be set from the host. `override=True` ensures the `.env` file wins, which is what you want in development. Without the `override=True`, a stale value from the Docker environment silently shadows the `.env` value — the bug is invisible and hard to trace.

**`logging.getLogger(__name__)` not `print()`**: `print()` bypasses the logging system. Log output from scripts using `print()` cannot be filtered by level, redirected to a file, or captured by log aggregation tools. `__name__` as the logger name means the logger hierarchy mirrors the module hierarchy — you can configure log levels per module.

**Logger defined at module level, not inside functions**: A logger defined inside a function is recreated on each call. A module-level logger is shared and inherits configuration set at startup.

### 5.2 DSN Construction — Lazy Pattern

```python
# Wrong — DSN constructed at module import time; fails if env not yet loaded
DSN = f"postgresql://postgres:{os.environ['POSTGRES_PASSWORD']}@localhost:5432/open_reporting"

# Correct — DSN constructed lazily; constructed only when a connection is needed
def _dsn() -> str:
    return f"postgresql://postgres:{os.environ['POSTGRES_PASSWORD']}@localhost:5432/open_reporting"
```

The lazy pattern matters when scripts are imported (e.g. in tests, or when a module is loaded by another). Eager DSN construction at import time means the environment must be fully configured any time the module is imported, not just when it is run. The lazy pattern defers the requirement to the point of actual use.

### 5.3 Connection Management

```python
conn = None
try:
    conn = psycopg2.connect(_dsn())
    # ... work ...
except Exception:
    log.exception("Pipeline failed")
    sys.exit(1)
finally:
    if conn:
        conn.close()
```

The `finally` block runs even when an exception is raised. Closing the connection only on the happy path leaves connections open after failures — in a PostgreSQL environment this exhausts the connection pool. The `if conn:` guard handles the case where the connection itself failed.

### 5.4 Type Hints

Every new function must carry parameter and return type annotations:

```python
# Correct
def fetch_series(series_id: str, year: int) -> list[dict]:
    ...

def upsert_rows(conn: psycopg2.connection, rows: list[tuple]) -> int:
    ...

# Wrong — no annotations
def fetch_series(series_id, year):
    ...
```

Type hints are not just documentation. They enable static analysis tools (mypy, Pyright) to catch type errors before runtime, and they make function signatures self-documenting at the call site.

### 5.5 Line Length and Import Ordering

- **100 characters** maximum line length. Applies to code, comments, and docstrings.
- **Import order**: stdlib → third-party → local, separated by blank lines. This is PEP 8 and enforced by `isort`. Mixing orders makes the dependency graph hard to read.

### 5.6 Error Handling

Never use bare `except:`. It catches `KeyboardInterrupt` and `SystemExit`, preventing Ctrl-C from working. Always catch the most specific exception class available:

```python
# Wrong
try:
    response = requests.get(url)
except:
    log.error("Failed")

# Correct
try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
except requests.exceptions.Timeout:
    log.error("Request timed out: %s", url)
    raise
except requests.exceptions.HTTPError as e:
    log.error("HTTP %s for %s", e.response.status_code, url)
    raise
```

---

## 6. Data Quality Dimensions

### 6.1 The Six DAMA Dimensions

The DAMA framework defines six primary dimensions for evaluating whether data is fit for purpose. Each dimension requires different validation techniques at different pipeline stages.

| Dimension | Definition | Where to validate |
|-----------|-----------|------------------|
| **Completeness** | All required data points are present and populated | Raw layer and curated layer |
| **Accuracy** | Data correctly represents the real-world entity or event | Spot-check against source; statistical outlier detection |
| **Consistency** | No conflicts between related data elements within or across datasets | Curated layer cross-field checks |
| **Timeliness** | Data is available when needed; freshness relative to publication schedule | Source freshness in dbt `sources.yml` |
| **Uniqueness** | Each entity is recorded exactly once | Deduplication in processing; unique tests in dbt |
| **Validity** | Data conforms to defined formats, types, and value ranges | Type casting and range checks in processing scripts |

### 6.2 Validation by Layer

**Raw layer checks (in ingestion scripts, post-load):**
- Row count is within expected range (warn if significantly below or above prior loads)
- Date range coverage — `MIN(period_year)`, `MAX(period_year)` — no unexpected truncation
- `fetched_at` populated on all rows (no nulls)
- Required key columns (`detail_id`, `geo_code`) are non-null

**Curated layer checks (dbt tests in schema.yml):**
- `not_null` on all primary key columns
- `unique` on natural key
- `accepted_values` on categorical columns
- `relationships` to reference models for foreign keys
- Source freshness tests in `sources.yml`

**Spot-check validation (manual, after ingestion):**
- Pick 3–5 values from the raw table and compare against the source website
- Verify that the latest period available matches what the source reports as its latest publication
- Check that known structural values (e.g. Poland's unemployment rate should be 2–6% in recent years) are in a plausible range

### 6.3 Row Count and Null Rate Thresholds

A single-number row count check is insufficient. The correct check compares the current load against the prior load:

```python
def validate_row_count(conn: duckdb.DuckDBPyConnection, table: str,
                       min_expected: int, warn_pct_drop: float = 0.10) -> None:
    result = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
    count = result[0]
    if count < min_expected:
        log.error("Row count %d below minimum expected %d in %s", count, min_expected, table)
        raise ValueError(f"Row count below minimum: {count} < {min_expected}")
    log.info("Row count OK: %d rows in %s", count, table)
```

Null rate check — flag columns where null rate exceeds a threshold:

```sql
SELECT
    column_name,
    COUNT(*) FILTER (WHERE value IS NULL)::DOUBLE / COUNT(*) AS null_rate
FROM raw.bdl_population
-- flag if null_rate > 0.05 on a required column
```

### 6.4 Timeliness — dbt Source Freshness

Configure source freshness in `sources.yml` so `dbt source freshness` reports stale sources:

```yaml
freshness:
  warn_after: {count: 7, period: day}   # warn if not refreshed in 7 days
  error_after: {count: 30, period: day}  # error if not refreshed in 30 days
```

The `loaded_at_field` must point to the `fetched_at` column. This is why `fetched_at` is mandatory on every raw table — it is the clock used by the freshness system.

---

## 7. Security in Data Pipelines

### 7.1 Parameterised Queries — Non-Negotiable

Every dynamic value inserted into a SQL query must use a parameter placeholder, never string formatting:

```python
# WRONG — SQL injection via f-string
geo = request_param  # could be "PL'; DROP TABLE raw.data; --"
conn.execute(f"SELECT * FROM raw.data WHERE geo = '{geo}'")

# WRONG — same problem, different syntax
conn.execute("SELECT * FROM raw.data WHERE geo = '%s'" % geo)

# CORRECT — psycopg2 parameterised query
conn.execute("SELECT * FROM raw.data WHERE geo = %s", (geo,))

# CORRECT — DuckDB parameterised query (positional)
conn.execute("SELECT * FROM raw.data WHERE geo = ?", [geo])

# CORRECT — DuckDB parameterised query (named)
conn.execute("SELECT * FROM raw.data WHERE geo = $geo", {"geo": geo})
```

The injection risk in data pipelines is real even when the "user" is another system or a configuration file. A series ID from the catalogue, a filename from the landing zone, or a parameter passed via CLI can all carry injection payloads. Parameterised queries eliminate the vulnerability entirely — the driver handles escaping, not the developer.

**Additional benefit:** Prepared statements allow the database engine to cache the query execution plan. Repeated execution of the same parameterised query is faster than repeated execution of a differently-formatted string query.

### 7.2 Credential Management Rules

- Secrets (passwords, API keys, tokens) live in `.env`. Never in Python source files, never in YAML configs that are committed, never in script arguments.
- `.env` is in `.gitignore`. `.env.example` is committed with placeholder values only.
- Load with `load_dotenv(override=True)` at script startup; access with `os.environ['KEY']` (not `os.getenv('KEY')` — the latter silently returns `None` when the key is missing, masking misconfiguration).
- For scheduled scripts (cron, systemd), pass secrets via environment variables set in the service unit, not via a `.env` file that requires `load_dotenv`.

### 7.3 Common Injection Vectors Specific to This Codebase

| Vector | Pattern | Mitigation |
|--------|---------|-----------|
| Dynamic table name in SQL | `f"SELECT * FROM {table_name}"` | Validate table name against allowed set before interpolating; DuckDB does not support parameterising table names |
| Column name from config | `f"SELECT {col} FROM ..."` | Same — validate against schema column list |
| Series ID from catalogue | Used in API URL construction | URL-encode with `urllib.parse.urlencode`; never string-format into SQL |
| Landing filename used in SQL | `read_csv('{filename}')` | Validate path is within the landing directory before use |
| API response field used as table name | Never, ever do this | Flag any pattern where API response content ends up in a table/schema name |

---

## 8. Applied Rules for Code Review — Data Engineering Extension

The following rules extend `docs/process/code-review.md`. They are specific to the data engineering layer and were not covered by the existing standard. Format: `RULE [P1/P2/P3] — [condition] → [why it is a problem]`.

---

### P1 — Blocks Merge

**RULE P1-DE-01** — Transformation logic (column derivations, ratio calculations, category mappings, filtering on domain criteria) appears in an ingestion script in `products/ingestion/` → Transformation in ingestion scripts bypasses dbt version control, cannot be tested with `dbt test`, and requires re-fetching from the external source to rerun — violates the ELT principle and makes the raw layer untrustworthy as a source of truth.

**RULE P1-DE-02** — A SQL query in Python uses f-string, `%` formatting, or `.format()` to construct the WHERE clause, INSERT values, or any dynamic part that carries external data → SQL injection vulnerability. External data includes: API responses, catalogue values, filenames, CLI arguments, config files. Use parameterised queries (`?` for DuckDB, `%s` for psycopg2).

**RULE P1-DE-03** — A raw table does not have a `fetched_at TIMESTAMPTZ` column, or `fetched_at` is populated with a business date (publication date, period date) rather than the ingestion timestamp → `fetched_at` is the ingestion audit clock and the high-watermark for dbt source freshness. Using it for anything else breaks the freshness system.

**RULE P1-DE-04** — An ingestion script performs a bare `INSERT INTO` (no `ON CONFLICT`) on a table that has a UNIQUE constraint or PRIMARY KEY → Re-running the script produces duplicate rows. All inserts on tables with a natural key must use upsert (`ON CONFLICT DO UPDATE` or `MERGE`).

**RULE P1-DE-05** — A dbt model references `raw.*` using `FROM raw.table_name` (literal) instead of `{{ source('raw', 'table_name') }}` → Source references that bypass `source()` are invisible to dbt's DAG, source freshness checks, and impact analysis. dbt cannot warn you when a source table changes if it doesn't know the model depends on it.

**RULE P1-DE-06** — A dbt model that is not a staging model references a source table directly (i.e. `{{ source() }}` in a mart or intermediate model) → Only staging models read from sources. All other models read from `{{ ref() }}`. Bypassing this breaks lineage and allows business logic to depend on unvalidated raw data.

**RULE P1-DE-07** — `CAST()` is used instead of `TRY_CAST()` in a staging model or raw-layer SQL → `CAST()` raises an error on malformed data; `TRY_CAST()` returns NULL. Raw data is not guaranteed clean. A single malformed row causes the entire staging model to fail when `CAST()` is used.

---

### P2 — Should Fix

**RULE P2-DE-01** — An incremental dbt model does not set `unique_key` → Without `unique_key`, every run appends all matching rows, producing duplicates. `unique_key` is required for correct incremental behaviour.

**RULE P2-DE-02** — A dbt model has no tests defined in `schema.yml` → Untested models are undocumented contracts. At minimum, primary key columns must have `not_null` and `unique` tests. A model with no tests provides no protection against silent data corruption.

**RULE P2-DE-03** — `os.getenv('KEY')` is used where the key is required (not optional) → `os.getenv()` returns `None` when the key is absent, and the failure is deferred to the first use of the value (which may produce a confusing `NoneType` error). Use `os.environ['KEY']` for required keys — it raises `KeyError` immediately at startup with a clear message.

**RULE P2-DE-04** — `load_dotenv()` is called without `override=True` in a script that runs in Docker or as a systemd service → In containerised environments, env vars are typically set by the container runtime before the script starts. `load_dotenv()` without `override=True` silently ignores the `.env` file when env vars are already present. The script appears to work but uses stale or wrong values from the container environment.

**RULE P2-DE-05** — A Python ingestion or processing script builds its DSN as a module-level constant (not inside a function) → Module-level DSN construction executes at import time. If the module is imported during testing or tool inspection without the full environment configured, it raises `KeyError`. Wrap DSN construction in a `_dsn()` function called lazily at connection time.

**RULE P2-DE-06** — A DuckDB query uses `CAST()` on a column read from a `read_csv()` call with typed `columns={}` → When `columns={}` already declares the target type, an additional `CAST()` on the same column is redundant and may mask intent. Either declare the type in `columns={}` or use `TRY_CAST()` in the SELECT — not both.

**RULE P2-DE-07** — A processing script iterates over a Parquet or CSV file with Python row-by-row iteration and then calls `conn.execute()` inside the loop → Single-row inserts inside a Python loop are orders of magnitude slower than using DuckDB's `read_parquet()` / `read_csv()` directly in SQL. The correct pattern is a single SQL INSERT ... SELECT FROM read_csv/parquet.

**RULE P2-DE-08** — A `validate()` function in an ingestion script checks only `COUNT(*)` without range-checking dates → Row count alone does not detect date truncation (e.g. a backfill that only loaded 2 of 20 years). Validation must check `MIN(period_year)` and `MAX(period_year)` (or equivalent) against expected coverage.

**RULE P2-DE-09** — A dbt model's staging SQL uses `SELECT *` → Wildcard selects in dbt staging models produce schemas that change silently when upstream tables gain or lose columns. Explicit column lists are required.

**RULE P2-DE-10** — An INTEGER type is used for a primary key, row count, or external source ID → INTEGER overflows at ~2.1 billion. BIGINT is the correct type for any identifier or count whose range is not guaranteed to stay below 2 billion. Use BIGINT by default; use INTEGER only with an explicit justification.

**RULE P2-DE-11** — A `FLOAT` / `DOUBLE` type is used for a financial or monetary value → Floating-point arithmetic introduces rounding errors on decimal fractions. Financial values must use `DECIMAL(18,2)` (DuckDB) or `NUMERIC(18,2)` (PostgreSQL) to ensure exact representation.

**RULE P2-DE-12** — A raw table uses `TIMESTAMP` (without timezone) instead of `TIMESTAMPTZ` for the `fetched_at` column → Naive timestamps are ambiguous when the server timezone changes (DST transitions, server moves). All pipeline timestamps are UTC and must be stored as `TIMESTAMPTZ`.

**RULE P2-DE-13** — A processing script drops rows with null in an optional column → Optional columns (those not in `REQUIRED_COLUMNS`) must not cause rows to be dropped. Null in an optional column means "not published for this period" and must be preserved in the curated layer. Imputation or dropping belongs in the analysis layer.

**RULE P2-DE-14** — A data quality issue (dropped row, nullified value, outlier flag) is logged only to stdout and not written to `processing_log.quality_issues` → Log messages are ephemeral. The quality issues table provides a persistent, queryable audit trail. All DQ events must be written there.

**RULE P2-DE-15** — A DuckDB `ON CONFLICT DO UPDATE SET` updates the conflict key column itself → Known DuckDB bug (confirmed 2025): updating the conflict column in an ON CONFLICT clause can silently set other columns to NULL. Use `MERGE` instead when the conflict key must be updated.

---

### P3 — Noted

**RULE P3-DE-01** — A dbt model lacks a `description` in `schema.yml` → Undocumented models accumulate. Every model should have at least a one-sentence description of what it represents and what grain it is at.

**RULE P3-DE-02** — A dbt model uses a subquery where a CTE would be clearer → CTEs make the transformation steps readable; nested subqueries obscure the data flow. Prefer CTEs. Not a blocking issue.

**RULE P3-DE-03** — SQL keywords are lowercase in a dbt model → Convention in this project is SQL keywords in UPPERCASE. Inconsistency within a file is worse than choosing either case consistently.

**RULE P3-DE-04** — A processing script does not log a final summary line (input rows → output rows → issues count) → The summary line is the single most useful operational signal from a pipeline run. Its absence makes monitoring harder.

**RULE P3-DE-05** — A dbt seed file is used for data that updates more frequently than quarterly → Seeds are for stable reference data. Frequently-changing data should be ingested as a source table, not hardcoded in a CSV in the repo.

**RULE P3-DE-06** — Magic numbers appear in validity range checks without a comment explaining their source → `{"max": 50_000_000}` is meaningful only if accompanied by a comment explaining it is Poland's population ceiling. Magic numbers in range checks without provenance are unverifiable.

**RULE P3-DE-07** — An ingestion script has no `--backfill` / `--year` argument for manual re-fetching → Scripts without a backfill mode require code changes to re-fetch historical data. A CLI argument is the correct mechanism; it should be noted as a missing affordance even if not currently needed.

**RULE P3-DE-08** — A DuckDB `read_csv()` call does not set `ignore_errors=true` in a raw-layer load → Without `ignore_errors=true`, a single malformed row in a CSV halts the entire load. In raw-layer ingestion, prefer `ignore_errors=true` and handle the row-level failures in the processing stage where the quality framework is applied.

---

## Summary Reference

| Topic | Key rule |
|-------|---------|
| ELT | Raw is loaded untouched; no transformation logic in ingestion scripts |
| DuckDB reads | Use `read_csv()` / `read_parquet()` in SQL; never Python row iteration |
| DuckDB upserts | `ON CONFLICT DO UPDATE`; use `MERGE` when conflict key is updated |
| DuckDB types | BIGINT for IDs/counts, TIMESTAMPTZ for all timestamps, TRY_CAST in raw layer |
| dbt structure | Staging only touches source(); all other models use ref() |
| dbt incremental | Always set unique_key; choose strategy by data pattern |
| dbt tests | Every model needs at minimum not_null + unique on primary key |
| Idempotency | Upsert for keyed data, truncate-insert for small tables, partition delete-insert for large history |
| Security | Parameterised queries everywhere; `os.environ[]` not `os.getenv()` for required keys |
| Credentials | load_dotenv(override=True) before os.environ; .env in .gitignore |
| Quality logging | All DQ events written to processing_log.quality_issues, not just stdout |
| Error handling | No bare `except:`; most specific exception class available |
| Connections | Always closed in `finally` block |

---

Sources:
- [ETL vs ELT: What's the difference and why it matters — dbt Labs](https://www.getdbt.com/blog/etl-vs-elt)
- [Understanding ELT: extract, load, transform — dbt Labs](https://www.getdbt.com/blog/extract-load-transform)
- [Staging: Preparing our atomic building blocks — dbt Developer Hub](https://docs.getdbt.com/best-practices/how-we-structure/2-staging)
- [How we style our SQL — dbt Developer Hub](https://docs.getdbt.com/best-practices/how-we-style/2-how-we-style-our-sql)
- [Configure incremental models — dbt Developer Hub](https://docs.getdbt.com/docs/build/incremental-models)
- [About incremental strategy — dbt Developer Hub](https://docs.getdbt.com/docs/build/incremental-strategy)
- [Why DuckDB — duckdb.org](https://duckdb.org/why_duckdb)
- [DuckDB in Depth: How It Works and What Makes It Fast — endjin](https://endjin.com/blog/2025/04/duckdb-in-depth-how-it-works-what-makes-it-fast)
- [DuckDB Optimization: A Developer's Guide — DZone](https://dzone.com/articles/developers-guide-to-duckdb-optimization)
- [How to run parameterized queries in DuckDB with Python — woteq](https://woteq.com/how-to-run-parameterized-queries-in-duckdb-with-python-to-prevent-sql-injection/)
- [Preventing SQL Injection Attacks With Python — Real Python](https://realpython.com/prevent-python-sql-injection/)
- [Idempotency in Data Engineering — Start Data Engineering](https://www.startdataengineering.com/post/why-how-idempotent-data-pipeline/)
- [6 Data Quality Dimensions — Collibra](https://www.collibra.com/blog/the-6-dimensions-of-data-quality)
- [Dimensions of Data Quality Research Paper v1.2 — DAMA NL (2020)](https://dama-nl.org/wp-content/uploads/2020/09/DDQ-Dimensions-of-Data-Quality-Research-Paper-version-1.2-d.d.-3-Sept-2020.pdf)
- [DuckDB Incremental Updates: MERGE, CDC, and Freshness — Medium/Codastra](https://medium.com/@2nick2patel2/duckdb-incremental-updates-merge-cdc-and-freshness-on-a-laptop-2e5e0e770e10)