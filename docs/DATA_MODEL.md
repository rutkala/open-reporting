# Data Model

Architecture decision record for the Open Reporting analytical warehouse.

---

## Architecture: Medallion with Kimball-style Conformed Dimensions

The warehouse follows the **medallion pattern** (bronze / silver / gold), with Kimball-style
conformed dimensions used in the silver integration layer.

```
Bronze  raw.*                      Source-aligned, untouched, reproducible from source
        ↓  dbt stg_*.sql
Silver  curated.all_indicators     Integration layer — all sources unified, atomic grain
        curated.stg_*              Source-staging models (dbt-internal, not queried directly)
        curated.dim_*              Conformed dimensions (Kimball-style)
        ↓  dbt mart_*.sql (future)
Gold    curated.mart_labour        Domain-specific marts — pre-joined, Polish labels, derived metrics
        curated.mart_finance       (built per domain as dashboards mature)
        ...
```

### Silver layer — what it is and what it is not

`curated.all_indicators` is the **silver integration layer**: a single cross-domain observation
table that unifies all sources into a consistent, conformed schema. It is the single source of
truth for all analytical data in the warehouse.

It is **not** a Kimball fact table. Kimball requires one fact table per business process (one
for labour, one for public finance, one for prices, etc.). `all_indicators` spans all 18 domains
deliberately — this is the correct design for an integration layer. Kimball's principle of named,
conformed semantic columns **is** applied here (no EAV), but the table itself is the integration
layer, not the presentation layer.

**The Explorer queries silver directly** — this is correct. The Explorer is a cross-domain
discovery tool; no single gold mart can serve it.

**Domain dashboards should query gold marts**, not silver directly. Gold marts are built per
domain on top of the silver layer. They contain only domain-relevant columns, pre-joined Polish
labels, and any pre-computed metrics. The gold layer is built domain by domain as dashboards
mature.

### Conformed dimensions (Kimball-style)

The `curated.dim_*` tables are Kimball-style conformed dimensions — managed once, shared across
all queries:

| Table | Rows | Purpose |
|-------|------|---------|
| `curated.dim_domain_detail` | 305 | Indicator catalogue — all valid `detail_id` values, labels, domains, units |
| `curated.dim_source` | 3 | Source registry |
| `curated.dim_geo` | 25 | Geographic hierarchy — PL + NUTS1 + NUTS2 |
| `curated.dim_calendar` | ~420 | Monthly spine 1995–2029 |

---

## Central Fact Table: `curated.all_indicators`

One row per: `source_id + detail_id + geo + period_date + [all populated dim columns]`

### Schema (33 columns)

| Column | Type | Description |
|--------|------|-------------|
| `source_id` | VARCHAR | Data source: `eurostat`, `nbp`, `dbw` |
| `domain_id` | VARCHAR | 18 domain codes: MAC, LAB, PUB, POP, PRC, etc. |
| `detail_id` | VARCHAR | Indicator key from `curated.dim_domain_detail` |
| `geo` | VARCHAR | NUTS code (`PL`, `PL1`, `PL11`, etc.) |
| `period_date` | DATE | All granularities truncated to first day of period |
| `dim_sex` | VARCHAR | Sex breakdown — NULL if not applicable |
| `dim_age_group` | VARCHAR | Age group |
| `dim_type_of_locality` | VARCHAR | Urban / rural classification |
| `dim_nace_sector` | VARCHAR | NACE economic sector |
| `dim_employment_status` | VARCHAR | Employment status |
| `dim_education_level` | VARCHAR | ISCED education level |
| `dim_prodcom_product` | VARCHAR | PRODCOM product category |
| `dim_hicp_category` | VARCHAR | HICP price category |
| `dim_pollutant_type` | VARCHAR | Environmental pollutant type |
| `dim_waste_category` | VARCHAR | Waste category |
| `dim_healthcare_function` | VARCHAR | Healthcare function (HC.1–HC.9) |
| `dim_health_provider` | VARCHAR | Health service provider type |
| `dim_health_financing` | VARCHAR | Health financing scheme |
| `dim_govt_sector` | VARCHAR | Government sector (S.13, S.1311, etc.) |
| `dim_institutional_sector` | VARCHAR | Institutional sector (ESA 2010) |
| `dim_asset_classification` | VARCHAR | Fixed asset type |
| `dim_tourist_origin` | VARCHAR | Tourist country/region of origin |
| `dim_trip_direction` | VARCHAR | Inbound / outbound |
| `dim_trip_duration` | VARCHAR | Trip duration category |
| `dim_quintile_group` | VARCHAR | Income quintile group |
| `dim_citizenship` | VARCHAR | Citizenship category |
| `dim_resources_uses` | VARCHAR | National accounts resources/uses side |
| `dim_transport_mode` | VARCHAR | Transport mode |
| `dim_accommodation_type` | VARCHAR | Tourist accommodation type |
| `value` | DOUBLE | Observed numeric value |
| `obs_status` | VARCHAR | Data quality flag from source |
| `fetched_at` | TIMESTAMPTZ | When the raw row was ingested |
| `updated_at` | TIMESTAMPTZ | When the curated row was last transformed |

### Sparsity is expected and correct

Eurostat and NBP rows have all 24 dim columns as NULL — these sources provide pre-aggregated
national series with no breakdown dimensions. DBW rows populate 1–3 dim columns per indicator.
This sparsity is intentional: DuckDB's columnar storage makes NULL columns essentially free.
The named columns exist to accommodate all current and future sources in a consistent schema.

| Source | Rows | Dimensions populated |
|--------|------|---------------------|
| `eurostat` | ~2,500 | None (all NULL) |
| `nbp` | ~24,000 | None (all NULL) |
| `dbw` | ~568,000 | 1–3 per indicator |

---

## Staging Layer

Each source has a `stg_{source}.sql` dbt model that:
1. Reads from `raw.*` (bronze)
2. Conforms column names, types, and grain to the shared 33-column schema
3. Maps source dimension slots to named semantic columns (NULL for absent dims)

`curated.all_indicators` unions all three:
```sql
select * from {{ ref('stg_eurostat') }}
union all
select * from {{ ref('stg_nbp') }}
union all
select * from {{ ref('stg_dbw') }}
```

### DBW dimension mapping

DBW has up to 3 dimension slots per observation (`dim1`, `dim2`, `dim3`), each identified by
a `dim_id` that encodes the semantic type. The staging model routes each slot to the correct
named column via CASE expressions on `dim_id` — slot position does not matter:

```sql
CASE
    WHEN o.dim1_type_id IN (1, 67, 339) THEN o.dim1_pos_name
    WHEN o.dim2_type_id IN (1, 67, 339) THEN o.dim2_pos_name
    WHEN o.dim3_type_id IN (1, 67, 339) THEN o.dim3_pos_name
END AS dim_sex
```

---

## Gold Layer (domain data marts)

Domain dashboards (Labour, Public Finance, etc.) should query **gold marts**, not
`curated.all_indicators` directly. Gold marts are built per domain as domain dashboards mature.

A gold mart differs from the silver layer in:
- **Domain scope** — only the indicators relevant to that domain; all 22+ irrelevant dim columns removed
- **Pre-joined labels** — Polish indicator names, unit labels, geographic names resolved at build time
- **Derived metrics** — YoY change, gender gap, ratios pre-computed as columns
- **Business hierarchy** — domain-specific groupings (e.g. Revenue / Expenditure / Balance for finance)

Gold marts are built as dbt models in `platform/processing/dbt/models/marts/`:
```
marts/
├── labour/mart_labour.sql
├── finance/mart_finance.sql
└── ...
```

Each is a `SELECT` from `curated.all_indicators` with pre-joins to dim tables, column pruning,
and any computed columns. Adding a gold mart does not change the silver layer.

---

## Rules

1. **Dashboards query `curated.*` only** — never `raw.*` directly.
2. **Explorer queries silver** (`curated.all_indicators`) — this is correct and intentional.
3. **Domain dashboards query gold** (their domain mart) — not silver.
4. **Silver is append/replace, never modified** — re-run `dbt run` to refresh.
5. **NULL for absent dimensions** — do not use empty string or placeholder values in dim columns.
6. **Adding a new dimension** — if a new source introduces a dimension not in the current 24,
   add a new `dim_{name} VARCHAR` column to all staging models and update this document.

---

## Adding a New Source (checklist)

1. Ingest to `raw.{source}_{entity}` — follow `standards/ingestion.md`
2. Create `platform/processing/dbt/models/{source}/stg_{source}.sql` — conform to 33-column schema
3. Map source dimension slots to named semantic columns; `null::varchar` for unpopulated dims
4. If source has a new dimension type not in the 24: add `dim_{name} VARCHAR` to all staging models
5. Union `select * from {{ ref('stg_{source}') }}` into `all_indicators.sql`
6. Add source row to `dim_source.csv` seed
7. Add indicator rows to `dim_domain_detail.csv` seed
8. Run `dbt seed --full-refresh && dbt run`
9. Validate: row counts per source, NULL rates per dim column, sample values in Explorer
