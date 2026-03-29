# Data Model

Decision record for the Open Reporting analytical warehouse schema design.

---

## Decision: Kimball Dimensional Modelling

**Date:** 2026-03-29 | **Issue:** OR-100

### Approaches evaluated

| Approach | Score | Rationale |
|----------|-------|-----------|
| Kimball (star schema) | 28/30 | Best fit: simple, query-fast, self-service ready |
| Data Vault 2.0 | 20/30 | Better for large teams / auditability; overkill for one-person operation |
| Inmon (3NF) | 15/30 | Normalised, great for operational systems; poor dashboard query performance |

Kimball was chosen because:
- Flat, wide fact table = fast dashboard queries with no joins
- Named semantic columns = consistent filtering across all sources
- Self-service friendly for future public access
- Right-sized for current scale (one person, ~600k rows)

---

## Central Fact Table: `curated.all_indicators`

A conformed wide fact table. All data sources — Eurostat, NBP, GUS DBW — are staged and unioned into this single table. Dashboards and the Explorer query only this table.

### Grain

One row per: `source_id + detail_id + geo + period_date + [all populated dim columns]`

### Schema

| Column | Type | Description |
|--------|------|-------------|
| `source_id` | VARCHAR | Data source: `eurostat`, `nbp`, `dbw` |
| `domain_id` | VARCHAR | 18 domain codes: MAC, LAB, PUB, POP, PRC, etc. |
| `detail_id` | VARCHAR | Indicator key from `curated.dim_domain_detail` |
| `geo` | VARCHAR | NUTS code (`PL`, `PL1`, `PL11`, etc.) or national |
| `period_date` | DATE | All granularities truncated to first day of period |
| `dim_sex` | VARCHAR | Sex breakdown (Total / Males / Females) |
| `dim_age_group` | VARCHAR | Age group (e.g. "15–64 years") |
| `dim_type_of_locality` | VARCHAR | Urban / rural classification |
| `dim_nace_sector` | VARCHAR | NACE economic sector code or name |
| `dim_employment_status` | VARCHAR | Employment status (employed, self-employed, etc.) |
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
| `dim_asset_classification` | VARCHAR | Fixed asset type (AN.11, etc.) |
| `dim_tourist_origin` | VARCHAR | Tourist country/region of origin |
| `dim_trip_direction` | VARCHAR | Inbound / outbound |
| `dim_trip_duration` | VARCHAR | Trip duration category |
| `dim_quintile_group` | VARCHAR | Income quintile group |
| `dim_citizenship` | VARCHAR | Citizenship category |
| `dim_resources_uses` | VARCHAR | National accounts resources/uses side |
| `dim_transport_mode` | VARCHAR | Transport mode (road, rail, air, etc.) |
| `dim_accommodation_type` | VARCHAR | Tourist accommodation type |
| `value` | DOUBLE | Observed numeric value |
| `obs_status` | VARCHAR | Data quality flag from source |
| `fetched_at` | TIMESTAMPTZ | When the raw row was ingested |
| `updated_at` | TIMESTAMPTZ | When the curated row was last transformed |

**Total: 33 columns** (5 core + 24 semantic dimensions + 4 metadata)

### Dimension population by source

| Source | Rows | Dimensions populated |
|--------|------|---------------------|
| `eurostat` | ~2,500 | None (all dim columns NULL) |
| `nbp` | ~24,000 | None (all dim columns NULL) |
| `dbw` | ~568,000 | 1–3 per indicator (sex, age_group, nace_sector most common) |

---

## Dimension Tables

| Table | Rows | Purpose |
|-------|------|---------|
| `curated.dim_domain_detail` | 305 | Indicator catalogue — all valid `detail_id` values, labels, domains, units, default aggregation |
| `curated.dim_source` | 3 | Source registry — source_id, name, type |
| `curated.dim_geo` | 25 | Geographic hierarchy — PL + 7 NUTS1 + 17 NUTS2 regions |
| `curated.dim_calendar` | ~420 | Monthly spine 1995–2029 |

These are Kimball conformed dimensions — small lookup tables joined to the fact as needed.

---

## Staging Layer

Each source has a `stg_{source}.sql` dbt model that:
1. Reads from `raw.*` (the bronze layer)
2. Conforms column names, types, and grain to the shared schema
3. Maps source-native dimension slots to named semantic columns
4. Outputs to `curated.stg_{source}` (internal — not queried by dashboards)

`curated.all_indicators` unions all three staging models:
```sql
select * from {{ ref('stg_eurostat') }}
union all
select * from {{ ref('stg_nbp') }}
union all
select * from {{ ref('stg_dbw') }}
```

### DBW dimension mapping

GUS DBW data has up to 3 dimension slots per observation (`dim1`, `dim2`, `dim3`). Each slot has a `dim_id` that identifies its semantic type. The staging model uses CASE expressions on `dim_id` to route each slot to the correct named column:

```sql
CASE
    WHEN o.dim1_type_id IN (1, 67, 339) THEN o.dim1_pos_name
    WHEN o.dim2_type_id IN (1, 67, 339) THEN o.dim2_pos_name
    WHEN o.dim3_type_id IN (1, 67, 339) THEN o.dim3_pos_name
END AS dim_sex
```

The `dim_id` values are authoritative — they come from `raw.dbw_positions` and are stable across variables. Slot position (which slot a dimension occupies for a given indicator) is irrelevant.

---

## Rules

1. **Named semantic columns only** — no generic `dim1_name/dim1_value` EAV slots. Every dimension must have a named column with a clear business meaning.
2. **Dashboards query `curated.*` only** — never `raw.*` directly.
3. **All sources union into `all_indicators`** — source is a filter attribute, not a separate tab or table.
4. **NULL for absent dimensions** — if an indicator has no sex breakdown, `dim_sex` is NULL. Do not use empty string or placeholder values.
5. **Adding a new dimension** — if a new source introduces a dimension not in the current 24, add a new named column to the schema (update all `stg_*.sql` models and `storage.md`). Do not reuse an existing dim column for a different semantic concept.

---

## Adding a New Source (checklist)

1. Ingest to `raw.{source}_{entity}` following `standards/ingestion.md`
2. Create `platform/processing/dbt/models/{source}/stg_{source}.sql` — conform to shared schema
3. Map source dimension slots to named semantic columns; add `null::varchar as dim_{name}` for all 24 columns not populated by this source
4. If source introduces a new dimension type not in the 24: add a new `dim_{name} VARCHAR` column to all staging models and update this document
5. Union `select * from {{ ref('stg_{source}') }}` into `all_indicators.sql`
6. Add source row to `dim_source.csv` seed
7. Add new indicator rows to `dim_domain_detail.csv` seed
8. Run `dbt seed --full-refresh && dbt run`
9. Validate: row counts per source, NULL rates per dim column, sample values
