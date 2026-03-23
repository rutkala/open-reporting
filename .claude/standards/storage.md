# Database Standard

## Architecture

Two-layer data architecture in PostgreSQL:

```
raw.{source}_{entity}        ← Bronze: native format, untouched
        ↓
    Python transform
        ↓
curated.{domain}_{metric}    ← Gold: cleaned, typed, dashboard-ready
```

**`raw` schema** — data as received from source. Never modified after landing. Always reproducible from source.

**`curated` schema** — clean, structured, analysis-ready. This is what dashboards query.

If transformations become complex enough to warrant an intermediate validation step, a `staging` schema can be added between raw and curated. Add it as a deliberate decision, not by default.

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

## Rules

- Never query `raw` schema from dashboards — always query `curated`
- Never modify `raw` data after landing — re-ingest if correction needed
- Transformations are idempotent — safe to run multiple times
- Schema changes require a plan — do not alter production tables without user approval
