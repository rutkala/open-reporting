# Processing Standard

## Position in Pipeline

This standard covers the **Transform phase**: moving data from `raw.{source}_{entity}` to `curated.{domain}_{metric}`.

```
raw.{source}_{entity}       ← Bronze: untouched, native format
        ↓
   processing/{source}_process.py
        ↓
curated.{domain}_{metric}   ← Gold: clean, typed, analysis-ready
```

Processing scripts live in `processing/`. One script per source-to-curated mapping. Input is always `raw`, output is always `curated`. Raw data is never modified.

---

## Data Quality Framework

Cleaning is organised into six categories, applied in the order below. This ordering is deliberate: structural problems (encoding, types) must be resolved before business logic checks (validity, consistency) can be reliable.

| Order | Category | What it covers |
|-------|----------|---------------|
| 1 | Encoding | Character encoding, diacritics, whitespace |
| 2 | Completeness | Nulls, missing required fields |
| 3 | Type casting | Parsing strings to correct Python/PostgreSQL types |
| 4 | Validity | Range checks, allowed values, format patterns |
| 5 | Consistency | Cross-field logic, referential integrity |
| 6 | Deduplication | Duplicate rows within the source |

All issues found are logged and counted. The pipeline does not silently discard data — every dropped or corrected row is recorded.

---

## Category 1: Encoding

**Goal:** Ensure all string data is valid UTF-8 and normalised before any other processing.

Polish sources frequently deliver data in Windows-1250, ISO-8859-2, or mixed encodings. Diacritics (ą ę ś ó ź ż ć ń ł) must be preserved — they are semantically significant in Polish region names and category labels.

**Steps:**
- Decode bytes with explicit encoding (never rely on `chardet` guessing in production)
- Normalise to NFC Unicode (composed form) — handles cases where diacritics arrive as combining characters
- Strip leading/trailing whitespace from all string columns
- Collapse internal multiple spaces to single space
- Replace non-breaking spaces (`\u00a0`) with regular spaces
- Remove null bytes (`\x00`) that can appear in some exports

```python
import unicodedata

def clean_string(value: str | None) -> str | None:
    if value is None:
        return None
    value = unicodedata.normalize("NFC", value)
    value = value.replace("\u00a0", " ").replace("\x00", "")
    value = " ".join(value.split())   # strip + collapse internal whitespace
    return value if value else None

# Apply to all string columns at load time
df[str_cols] = df[str_cols].applymap(clean_string)
```

**Reading files with explicit encoding:**
```python
import pandas as pd

# Try UTF-8 first, fall back to Windows-1250 for Polish government sources
try:
    df = pd.read_csv(path, encoding="utf-8")
except UnicodeDecodeError:
    df = pd.read_csv(path, encoding="windows-1250")
    log.warning(f"Fell back to windows-1250 for {path}")
```

---

## Category 2: Completeness

**Goal:** Identify and handle missing values. Every column must have an explicit policy.

### Required vs. optional columns

Define a schema for each curated table. Every column is either:
- **Required** — null is invalid; row must be dropped or rejected
- **Optional** — null is allowed; document what null means (unknown, not applicable, not yet published)

```python
REQUIRED_COLUMNS = ["region_code", "year", "variable_id"]
OPTIONAL_COLUMNS = ["value", "unit"]   # null value = data not published for that period

# Check required columns
null_mask = df[REQUIRED_COLUMNS].isnull().any(axis=1)
if null_mask.any():
    log.warning(f"Dropped {null_mask.sum()} rows with null in required columns")
    dropped_df = df[null_mask].copy()
    dropped_df["drop_reason"] = "null_in_required_column"
    _log_quality_issues(dropped_df)
    df = df[~null_mask]
```

### Null handling policy

| Situation | Action |
|-----------|--------|
| Null in primary key / required dimension | Drop row, log |
| Null in optional metric (e.g. value not yet published) | Keep as `NULL` in curated — do not impute |
| Null in supplementary label that can be looked up | Fill from reference table |
| Null in derived/computed column | Compute it or leave null with documentation |

**Do not impute** statistical measures (mean, median) into `curated` — imputation belongs in the analysis layer, not the data layer. The curated layer represents what the source actually reported.

---

## Category 3: Type Casting

**Goal:** Convert all columns to their correct Python types before writing to PostgreSQL. Type mismatches silently become `NULL` or raise errors at insert time — catch them explicitly here.

### Numeric parsing

Polish and European sources use comma as decimal separator and period or space as thousands separator.

```python
import re

def parse_numeric(value: str | float | int | None) -> float | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip()
    # Remove thousands separators (space or period used as grouping)
    s = re.sub(r"[\s]", "", s)          # remove spaces (e.g. "1 234 567")
    s = re.sub(r"\.(?=\d{3})", "", s)   # remove period-as-thousands "1.234.567"
    s = s.replace(",", ".")             # Polish decimal comma → dot
    # Strip trailing unit labels that slip through (e.g. "123 %", "456 tys.")
    s = re.sub(r"[^\d.\-].*$", "", s)
    try:
        return float(s)
    except ValueError:
        return None
```

### Date parsing

```python
from datetime import date, datetime

# Known format — always use strptime, never rely on pandas inference
def parse_date(value: str | None, fmt: str = "%Y-%m-%d") -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(str(value).strip(), fmt).date()
    except ValueError:
        log.warning(f"Could not parse date: {value!r}")
        return None

# For year-only columns (most statistical data)
def parse_year(value) -> int | None:
    try:
        y = int(value)
        if 1900 <= y <= 2100:
            return y
        return None
    except (ValueError, TypeError):
        return None
```

### Type conversion table

| Source pattern | Target PostgreSQL type | Python intermediate |
|---------------|----------------------|---------------------|
| String integer | `BIGINT` | `int()` with null guard |
| String decimal with comma | `NUMERIC(18,2)` | `parse_numeric()` above |
| String date "2024-01-15" | `DATE` | `datetime.strptime().date()` |
| String date "2024Q1" | `DATE` | custom parser → first day of quarter |
| "tak"/"nie", "1"/"0", "true"/"false" | `BOOLEAN` | normalised map |
| Region code (NUTS, TERYT) | `VARCHAR(10)` | strip + uppercase |

---

## Category 4: Validity

**Goal:** Ensure values fall within expected ranges and formats. Validity is domain-specific — define rules per table.

### Numeric range checks

```python
VALIDITY_RULES = {
    "population": {"min": 0, "max": 50_000_000},
    "rate_pct":   {"min": 0.0, "max": 100.0},
    "year":       {"min": 1990, "max": 2030},
}

def apply_range_checks(df: pd.DataFrame, rules: dict) -> pd.DataFrame:
    issues = []
    for col, bounds in rules.items():
        if col not in df.columns:
            continue
        lo, hi = bounds.get("min"), bounds.get("max")
        if lo is not None:
            mask = df[col].notna() & (df[col] < lo)
            if mask.any():
                issues.append(df[mask].assign(issue=f"{col}_below_minimum"))
                df.loc[mask, col] = None   # nullify, do not drop
                log.warning(f"{mask.sum()} values in {col} below minimum {lo} — set to NULL")
        if hi is not None:
            mask = df[col].notna() & (df[col] > hi)
            if mask.any():
                issues.append(df[mask].assign(issue=f"{col}_above_maximum"))
                df.loc[mask, col] = None
                log.warning(f"{mask.sum()} values in {col} above maximum {hi} — set to NULL")
    if issues:
        _log_quality_issues(pd.concat(issues))
    return df
```

### Allowed value sets (categorical columns)

```python
VALID_REGION_PREFIXES = {"PL"}   # NUTS codes for Poland start with PL

def validate_nuts_code(code: str | None) -> bool:
    if code is None:
        return False
    return code.startswith("PL") and 2 <= len(code) <= 5
```

### Format validation (codes, identifiers)

```python
import re

TERYT_PATTERN = re.compile(r"^\d{2}(\d{2}(\d{3}(\d{2})?)?)?$")   # 2, 4, 7, or 9 digits

def validate_teryt(code: str | None) -> bool:
    if code is None:
        return False
    return bool(TERYT_PATTERN.match(code))
```

### Outlier detection

For statistical time series, flag statistical outliers — do not drop them. Outliers in official statistical data are often real (crisis years, boundary changes).

```python
def flag_outliers_zscore(df: pd.DataFrame, col: str, threshold: float = 3.5) -> pd.DataFrame:
    """Flag outliers using modified Z-score (robust to non-normal distributions)."""
    series = df[col].dropna()
    median = series.median()
    mad = (series - median).abs().median()
    if mad == 0:
        return df
    modified_z = 0.6745 * (df[col] - median) / mad
    df[f"{col}_outlier_flag"] = modified_z.abs() > threshold
    flagged = df[f"{col}_outlier_flag"].sum()
    if flagged:
        log.info(f"Flagged {flagged} outliers in {col} (modified Z-score > {threshold})")
    return df
```

---

## Category 5: Consistency

**Goal:** Enforce cross-field business rules and referential integrity.

### Cross-field checks

```python
def check_consistency(df: pd.DataFrame) -> pd.DataFrame:
    issues = []

    # Year must be consistent with date column if both present
    if "year" in df.columns and "period_date" in df.columns:
        mismatch = df["year"] != df["period_date"].dt.year
        if mismatch.any():
            issues.append(df[mismatch].assign(issue="year_date_mismatch"))
            log.warning(f"{mismatch.sum()} rows where year != period_date.year")

    # Value and unit must both be present or both absent
    if "value" in df.columns and "unit" in df.columns:
        inconsistent = df["value"].notna() & df["unit"].isna()
        if inconsistent.any():
            issues.append(df[inconsistent].assign(issue="value_without_unit"))
            log.warning(f"{inconsistent.sum()} rows have value but no unit")

    if issues:
        _log_quality_issues(pd.concat(issues))
    return df
```

### Reference table joins

Region codes must exist in the reference table. Rows with unknown region codes are flagged.

```python
def validate_region_codes(df: pd.DataFrame, conn, code_col: str = "region_code") -> pd.DataFrame:
    cur = conn.cursor()
    cur.execute("SELECT code FROM reference.regions")
    valid_codes = {row[0] for row in cur.fetchall()}
    unknown = ~df[code_col].isin(valid_codes) & df[code_col].notna()
    if unknown.any():
        log.warning(f"{unknown.sum()} rows with unknown region codes: {df.loc[unknown, code_col].unique()}")
        _log_quality_issues(df[unknown].assign(issue="unknown_region_code"))
    return df
```

---

## Category 6: Deduplication

**Goal:** Ensure each logical record appears exactly once in curated.

### Identifying duplicates

Define the natural key for each curated table (the columns that uniquely identify a record). Duplicates on the natural key are a data quality problem, not a normal state.

```python
NATURAL_KEY = ["region_code", "year", "variable_id"]

def deduplicate(df: pd.DataFrame, key_cols: list[str], keep: str = "last") -> pd.DataFrame:
    """
    Deduplicate on natural key.
    keep='last' — if source sent multiple values for same key, keep the most recent row.
    This is appropriate when source data has been corrected or republished.
    """
    duplicates = df.duplicated(subset=key_cols, keep=False)
    if duplicates.any():
        dup_count = df.duplicated(subset=key_cols, keep=keep).sum()
        log.warning(
            f"Found {duplicates.sum()} rows involved in duplicates on {key_cols}. "
            f"Dropping {dup_count} earlier/duplicate rows (keep='{keep}')."
        )
        _log_quality_issues(
            df[df.duplicated(subset=key_cols, keep=keep)].assign(issue="duplicate_natural_key")
        )
        df = df.drop_duplicates(subset=key_cols, keep=keep)
    return df
```

### Deduplication against existing curated data

When doing incremental loads, check that incoming rows do not conflict with existing curated rows from a different source or period:

```python
# Use ON CONFLICT in the upsert — PostgreSQL handles this at write time
# The conflict target is the natural key defined on the curated table
```

---

## Date and Time Standardisation

All timestamps written to PostgreSQL must be timezone-aware (`TIMESTAMPTZ`). Use UTC internally; convert to Europe/Warsaw only for display.

```python
from datetime import timezone
import pytz

WARSAW = pytz.timezone("Europe/Warsaw")

def to_utc(dt) -> datetime | None:
    if dt is None:
        return None
    if dt.tzinfo is None:
        # Assume Warsaw local time if no tz info (common in Polish government data)
        dt = WARSAW.localize(dt)
    return dt.astimezone(timezone.utc)
```

**Date-only columns** (year, month, quarter): store as `DATE` (first day of period) or `INT` (year). Do not store as strings.

| Source format | Store as | Notes |
|--------------|----------|-------|
| 2024 | `INT` year column | Most statistical data is annual |
| 2024-01 | `DATE` → 2024-01-01 | First day of month |
| 2024Q1 | `DATE` → 2024-01-01 | First day of quarter |
| 2024-01-15 | `DATE` | As-is |
| 2024-01-15T12:00:00 | `TIMESTAMPTZ` | Localise then convert to UTC |

---

## Numeric Precision

Follow the type table in `storage.md`:
- Financial values: `NUMERIC(18,2)` — never `FLOAT`
- Rates and percentages: `NUMERIC(8,4)`
- Counts: `BIGINT`

When writing to PostgreSQL via `psycopg2`, Python `float` maps to PostgreSQL `FLOAT8`, which introduces rounding. Use Python `Decimal` for financial values:

```python
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

def to_numeric_2dp(value: float | None) -> Decimal | None:
    if value is None:
        return None
    try:
        return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except InvalidOperation:
        return None
```

---

## Quality Issue Logging

Every data quality issue found is recorded during processing. This creates an audit trail and enables monitoring.

### Issue record structure

```python
import json
from datetime import datetime, timezone

def _log_quality_issues(issue_df: pd.DataFrame, source: str, table: str) -> None:
    """
    Write quality issues to processing_log.quality_issues.
    Called internally whenever rows are dropped, nullified, or flagged.
    """
    # Caller passes a DataFrame with an 'issue' column describing the problem
    records = []
    for _, row in issue_df.iterrows():
        records.append({
            "source": source,
            "table": table,
            "issue_type": row.get("issue", "unknown"),
            "row_data": json.dumps(row.drop("issue", errors="ignore").to_dict(), default=str),
            "detected_at": datetime.now(timezone.utc),
        })
    # Batch insert to quality issues log table
    ...
```

### Quality log table

```sql
CREATE SCHEMA IF NOT EXISTS processing_log;

CREATE TABLE IF NOT EXISTS processing_log.quality_issues (
    id            BIGSERIAL PRIMARY KEY,
    source        VARCHAR(100)    NOT NULL,   -- e.g. 'bdl', 'eurostat'
    table_name    VARCHAR(100)    NOT NULL,   -- target curated table
    issue_type    VARCHAR(100)    NOT NULL,   -- e.g. 'null_in_required_column'
    row_data      JSONB,                      -- serialised problem row for diagnosis
    detected_at   TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

CREATE INDEX quality_issues_source_idx ON processing_log.quality_issues (source, detected_at);
CREATE INDEX quality_issues_type_idx   ON processing_log.quality_issues (issue_type);
```

### Standard issue_type values

| issue_type | Meaning |
|-----------|---------|
| `null_in_required_column` | Row dropped — required field was null |
| `type_cast_failure` | Value could not be parsed to target type — set to NULL |
| `below_minimum` | Numeric value below valid range — set to NULL |
| `above_maximum` | Numeric value above valid range — set to NULL |
| `invalid_region_code` | Region code not in reference table |
| `duplicate_natural_key` | Duplicate row removed |
| `unknown_unit` | Unit label not in allowed set |
| `outlier_flagged` | Value statistically anomalous — kept, flagged |
| `year_date_mismatch` | year column contradicts period_date year |

### Processing run summary

Log a summary at the end of every run:

```python
log.info(
    f"Processing complete — "
    f"input: {input_count} rows, "
    f"output: {output_count} rows, "
    f"dropped: {input_count - output_count} rows, "
    f"quality issues: {issue_count}"
)
```

---

## Script Structure

```python
#!/usr/bin/env python3
"""
Processing: {Source Name} → {Curated Table}
Input:  raw.{source}_{entity}
Output: curated.{domain}_{metric}
Run:    python3 processing/{source}_process.py

Transformations applied:
- Encoding normalisation (NFC, whitespace)
- Null checks: {required_col_1}, {required_col_2} required
- Type casting: value from string with comma decimal, year from int
- Validity: value in [0, 50_000_000], year in [1990, 2030]
- Deduplication on (region_code, year, variable_id)
"""
import json
import logging
import os
import sys
from datetime import datetime, timezone
from decimal import Decimal

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

SOURCE = "bdl"
TARGET_TABLE = "curated.demographics_population"
NATURAL_KEY = ["region_code", "year"]
REQUIRED_COLUMNS = ["region_code", "year"]
DSN = f"postgresql://postgres:{os.environ['POSTGRES_PASSWORD']}@localhost:5432/open_reporting"

_issue_buffer: list[dict] = []


def _log_quality_issues(issue_df: pd.DataFrame) -> None:
    for _, row in issue_df.iterrows():
        _issue_buffer.append({
            "source": SOURCE,
            "table_name": TARGET_TABLE,
            "issue_type": row.get("issue", "unknown"),
            "row_data": json.dumps(row.drop("issue", errors="ignore").to_dict(), default=str),
            "detected_at": datetime.now(timezone.utc),
        })


def extract(conn) -> pd.DataFrame:
    return pd.read_sql(
        "SELECT * FROM raw.bdl_population ORDER BY fetched_at",
        conn
    )


def transform(df: pd.DataFrame) -> pd.DataFrame:
    input_count = len(df)

    # 1. Encoding
    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].applymap(clean_string)

    # 2. Completeness
    null_mask = df[REQUIRED_COLUMNS].isnull().any(axis=1)
    if null_mask.any():
        _log_quality_issues(df[null_mask].assign(issue="null_in_required_column"))
        log.warning(f"Dropped {null_mask.sum()} rows with null in required columns")
        df = df[~null_mask].copy()

    # 3. Type casting
    df["year"] = df["year"].apply(parse_year)
    df["value"] = df["value"].apply(parse_numeric)

    # 4. Validity
    df = apply_range_checks(df, {"value": {"min": 0, "max": 50_000_000}, "year": {"min": 1990, "max": 2030}})

    # 5. Consistency (no cross-field rules for this table)

    # 6. Deduplication
    df = deduplicate(df, NATURAL_KEY)

    log.info(f"Transform: {input_count} → {len(df)} rows ({input_count - len(df)} removed)")
    return df


def load(conn, df: pd.DataFrame) -> int:
    rows = [
        (
            row["region_code"],
            row["year"],
            row["value"],
            datetime.now(timezone.utc),
        )
        for _, row in df.iterrows()
    ]
    cur = conn.cursor()
    execute_values(cur, """
        INSERT INTO curated.demographics_population
            (region_code, year, population, updated_at)
        VALUES %s
        ON CONFLICT (region_code, year) DO UPDATE SET
            population = EXCLUDED.population,
            updated_at = EXCLUDED.updated_at
    """, rows)
    conn.commit()
    return cur.rowcount


def flush_quality_issues(conn) -> None:
    if not _issue_buffer:
        return
    cur = conn.cursor()
    execute_values(cur, """
        INSERT INTO processing_log.quality_issues
            (source, table_name, issue_type, row_data, detected_at)
        VALUES %s
    """, [
        (r["source"], r["table_name"], r["issue_type"], r["row_data"], r["detected_at"])
        for r in _issue_buffer
    ])
    conn.commit()
    log.info(f"Logged {len(_issue_buffer)} quality issues")


def validate(conn) -> None:
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*), MIN(year), MAX(year), COUNT(DISTINCT region_code)
        FROM curated.demographics_population
    """)
    count, min_year, max_year, regions = cur.fetchone()
    log.info(f"Validation: {count} rows, years {min_year}–{max_year}, {regions} regions")


def main() -> None:
    conn = None
    try:
        conn = psycopg2.connect(DSN)
        df = extract(conn)
        df = transform(df)
        count = load(conn, df)
        flush_quality_issues(conn)
        log.info(f"Loaded {count} rows into {TARGET_TABLE}")
        validate(conn)
    except Exception:
        log.exception("Processing failed")
        sys.exit(1)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    main()
```

---

## Checklist: Before Marking a Processing Script Complete

- [ ] All six quality categories applied (encoding, completeness, types, validity, consistency, deduplication)
- [ ] Required vs. optional columns explicitly defined
- [ ] Null handling policy documented per column
- [ ] Type casting handles Polish decimal comma and thousand separators
- [ ] Date/time values are timezone-aware or stored as DATE/INT (no naive datetimes)
- [ ] Financial values use `Decimal` / `NUMERIC`, not `float`
- [ ] Quality issues written to `processing_log.quality_issues`
- [ ] Summary log line at end of run (input rows, output rows, issues)
- [ ] Script is idempotent — safe to run multiple times
- [ ] Script docstring lists all transformations applied
- [ ] Post-run validation query confirms expected row count and ranges
