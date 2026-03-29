# Database Standard

## Architecture

Three-layer data pipeline in DuckDB (analytical warehouse):

```
raw.{source}_{entity}        ← Bronze: native format, untouched
        ↓
    dbt staging models        ← Internal to dbt — not a separate DuckDB schema
    (stg_{source}.sql)        conform each source to the shared fact schema
        ↓
curated.{domain}_{metric}    ← Gold: cleaned, typed, dashboard-ready
```

**`raw` schema** — data as received from source. Never modified after landing. Always reproducible from source.

**Staging (dbt-internal)** — `stg_{source}.sql` models in `platform/processing/dbt/models/`. Each staging model conforms one source to the shared `all_indicators` schema. These produce DuckDB tables in the `curated` schema prefixed with `stg_` (dbt materialises them there). They are not queried directly by dashboards.

**`curated` schema** — clean, structured, analysis-ready. This is what all dashboards and the Explorer query. Never bypass curated — dashboards must never query `raw.*` directly.

**Dimensional modelling approach: Kimball star schema** — named semantic columns in the fact table, conformed dimension lookup tables. No EAV (generic dim_name/dim_value) slots — every dimension must have a named column with a clear business meaning. See `docs/DATA_MODEL.md` for the full decision record.

**Shared staging schema** (all `stg_*.sql` models must output these 33 columns in this order):
```
source_id                VARCHAR    -- 'eurostat', 'nbp', 'dbw'
domain_id                VARCHAR    -- 18 domain codes: MAC, LAB, PUB, POP, PRC, etc.
detail_id                VARCHAR    -- indicator key from curated.dim_domain_detail seed
geo                      VARCHAR    -- NUTS code or 'PL' for national
period_date              DATE       -- all granularities truncated to first day of period
dim_sex                  VARCHAR    -- NULL if not applicable
dim_age_group            VARCHAR
dim_type_of_locality     VARCHAR
dim_nace_sector          VARCHAR
dim_employment_status    VARCHAR
dim_education_level      VARCHAR
dim_prodcom_product      VARCHAR
dim_hicp_category        VARCHAR
dim_pollutant_type       VARCHAR
dim_waste_category       VARCHAR
dim_healthcare_function  VARCHAR
dim_health_provider      VARCHAR
dim_health_financing     VARCHAR
dim_govt_sector          VARCHAR
dim_institutional_sector VARCHAR
dim_asset_classification VARCHAR
dim_tourist_origin       VARCHAR
dim_trip_direction       VARCHAR
dim_trip_duration        VARCHAR
dim_quintile_group       VARCHAR
dim_citizenship          VARCHAR
dim_resources_uses       VARCHAR
dim_transport_mode       VARCHAR
dim_accommodation_type   VARCHAR
value                    DOUBLE
obs_status               VARCHAR    -- data quality flag from source
fetched_at               TIMESTAMPTZ
updated_at               TIMESTAMPTZ
```

**Rule:** Use `null::varchar as dim_{name}` for every named dimension column that a source does not populate. Never use empty string or placeholder values.

**Adding a new source** (checklist):
1. Ingest to `raw.{source}_{entity}` following ingestion standard
2. Create `platform/processing/dbt/models/{source}/stg_{source}.sql` — conform to shared schema above
3. Map source dimension slots to named semantic columns; add `null::varchar as dim_{name}` for all 24 dim columns not populated
4. If source introduces a new dimension type: add a new `dim_{name} VARCHAR` column to ALL staging models and update `docs/DATA_MODEL.md`
5. Union `select * from {{ ref('stg_{source}') }}` into `all_indicators.sql`
6. Add source row to `dim_source.csv` seed
7. Add new indicator rows to `dim_domain_detail.csv` seed for any new detail_ids
8. Run `dbt seed --full-refresh && dbt run`
9. Validate: row counts per source, NULL rates per dim column, sample values

**PostgreSQL** — used only by Ghost CMS (operational DB). No analytics, no dashboards.

---

## Schema Naming Conventions

### Raw layer
```
raw.{source}_{entity}
```
- `source` — short identifier for the data source
- `entity` — what the table contains

Examples:
```
raw.bdl_population
raw.bdl_employment
raw.eurostat_gdp
raw.nbp_exchange_rates
raw.openbudget_execution
```

### Curated layer
```
curated.{domain}_{metric}
```
- `domain` — business domain from DOMAINS.md (demographics, finance, labour, health, etc.)
- `metric` — what is being measured

Examples:
```
curated.demographics_population
curated.finance_gdp
curated.labour_employment_rate
curated.budget_execution
```

---

## Column Naming

- All column names: `snake_case`
- No reserved words as column names (`year` is fine, `date` use `period_date` instead)
- Units in column name where ambiguous: `value_pln`, `rate_pct`, `count_persons`

---

## Required Columns

### Every `raw` table must include:
```sql
fetched_at   TIMESTAMPTZ DEFAULT NOW()   -- when the row was ingested
```

### Every `curated` table must include:
```sql
updated_at   TIMESTAMPTZ DEFAULT NOW()   -- when the row was last transformed
```

### Primary keys:
- Always define a primary key or unique constraint
- Use natural keys where they exist (year + region + category)
- Use `SERIAL` or `BIGSERIAL` only when no natural key exists

---

## Data Types

| Data | Type | Notes |
|------|------|-------|
| Dates | `DATE` | For year/month/day precision |
| Timestamps | `TIMESTAMPTZ` | Always with timezone, never `TIMESTAMP` |
| Financial values | `NUMERIC(18,2)` | Never `FLOAT` — avoids rounding errors |
| Rates, percentages | `NUMERIC(8,4)` | 4 decimal places |
| Counts, integers | `BIGINT` | Not `INT` — avoids overflow on large datasets |
| External source IDs | `BIGINT` | Always BIGINT for IDs from external sources — do not assume INT32 range; position/dimension IDs from GUS DBW can exceed 12 billion |
| Short strings | `VARCHAR(255)` | Codes, names, identifiers |
| Long text | `TEXT` | Descriptions, notes |
| Semi-structured | `JSONB` | Raw JSON from APIs, parse in transform |
| Flags | `BOOLEAN` | Not `CHAR(1)` or `INT` |

---

## Upsert Pattern

Default update method for all ingestion:

```sql
INSERT INTO raw.{table} (col1, col2, value, fetched_at)
VALUES %s
ON CONFLICT (col1, col2) DO UPDATE SET
    value = EXCLUDED.value,
    fetched_at = EXCLUDED.fetched_at
```

Always define the conflict target explicitly — never use `ON CONFLICT DO NOTHING` without justification.

---

## Indexes

Standard indexes to create on every table:

```sql
-- Primary key or unique constraint (always)
ALTER TABLE raw.{table} ADD CONSTRAINT {table}_pk PRIMARY KEY (col1, col2);

-- Date/year column (always if present — dashboards always filter by time)
CREATE INDEX {table}_year_idx ON raw.{table} (year);

-- Region/geography column (if present)
CREATE INDEX {table}_region_idx ON raw.{table} (region_code);
```

---

## Schema Creation Pattern

```sql
-- Create schemas (run once on new DB)
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS curated;

-- Example raw table
CREATE TABLE IF NOT EXISTS raw.bdl_population (
    variable_id   VARCHAR(50)    NOT NULL,
    region_code   VARCHAR(10)    NOT NULL,
    year          INT            NOT NULL,
    value         NUMERIC(18,2),
    unit          VARCHAR(50),
    fetched_at    TIMESTAMPTZ    DEFAULT NOW(),
    CONSTRAINT bdl_population_pk PRIMARY KEY (variable_id, region_code, year)
);

CREATE INDEX IF NOT EXISTS bdl_population_year_idx ON raw.bdl_population (year);
CREATE INDEX IF NOT EXISTS bdl_population_region_idx ON raw.bdl_population (region_code);

-- Example curated table
CREATE TABLE IF NOT EXISTS curated.demographics_population (
    region_code   VARCHAR(10)    NOT NULL,
    region_name   VARCHAR(100)   NOT NULL,
    year          INT            NOT NULL,
    population    BIGINT,
    updated_at    TIMESTAMPTZ    DEFAULT NOW(),
    CONSTRAINT demographics_population_pk PRIMARY KEY (region_code, year)
);
```

---

## Access

- Single user (`postgres`) for all operations — ingestion, transformation, dashboards
- Add a read-only `dashboard` user when the portal goes public (TBD)

---

## DuckDB Quirks

- **Cannot DELETE all rows from a table with a compound primary key index.** DuckDB throws a FatalException. For full-overwrite loads, use `DROP TABLE IF EXISTS` + recreate from DDL instead of `DELETE FROM`.
- **Full-overwrite pattern:**
  ```python
  conn.execute("DROP TABLE IF EXISTS raw.my_table")
  with open("platform/warehouse/raw/my_table.sql") as f:
      conn.execute(f.read())
  # then INSERT from read_csv(...)
  ```

---

## Rules

- Never query `raw` schema from dashboards — always query `curated`
- Never modify `raw` data after landing — re-ingest if correction needed
- Transformations are idempotent — safe to run multiple times
- Schema changes require a plan — do not alter production tables without user approval
