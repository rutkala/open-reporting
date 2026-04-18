# Data Connection

## What it is
Every dashboard binds to a MetricFlow semantic model via two files:
- `measures.py` — dimension and measure display config (labels, units, format)
- `semantic_service.py` (or `data.py` in the template) — SQL loaders that return pre-aggregated DataFrames

The semantic model is a **separate product** — the dashboard only consumes it. No aggregation or business logic lives in the dashboard.

---

## measures.py — display config only

```python
"""
TODO_DOMAIN dashboard — dimension and measure display config.
Aggregation logic lives in semantic_service.py.
"""
from products.visuals.lib.semantic import Dimension, Measure

# ── Dimensions ────────────────────────────────────────────────────────────────

DIMS = {
    "TODO_DIM_KEY": Dimension(
        "TODO_DIM_KEY",   # internal key
        "TODO Label",     # display label (Polish)
        "TODO_col",       # DataFrame column name
    ),
    # Add one entry per dimension used in charts or slicers
}

# ── Measures ──────────────────────────────────────────────────────────────────

MEASURES = {
    "TODO_MEASURE_KEY": Measure(
        "TODO_MEASURE_KEY",  # internal key
        "TODO Label",        # display label (Polish)
        "TODO_col",          # DataFrame column name
        unit="TODO",         # e.g. "%", "mln zł", "tys. os."
        format_type="number",  # "number" | "percent" | "currency"
        decimals=1,
        currency_symbol="zł",   # only for format_type="currency"
        scale="M",              # "M" | "B" — only for currency
        show_unit=True,         # False to hide unit in axis labels
    ),
    # Add one entry per measure used in charts or KPI cards
}
```

### Measure API — key methods
```python
m.MEASURES["key"].to_series(y_list)      # → {"name": label, "y": values} — chart series
m.MEASURES["key"].kpi_value(scalar)      # → formatted string for KPI card value
m.MEASURES["key"].plotly_ticksuffix      # → tick suffix string for axis formatting
m.MEASURES["key"].label                  # → display label (Polish)
m.MEASURES["key"].unit                   # → raw unit string

m.DIMS["key"].values(df)                 # → list of unique values from df column (sorted)
m.DIMS["key"].col                        # → raw column name string
```

---

## semantic_service.py — SQL loaders

```python
"""
TODO_DOMAIN dashboard — data loaders.

Each function returns a pre-aggregated DataFrame ready for chart calls.
No further aggregation happens in app.py.
"""
import pandas as pd
from products.visuals.lib.db import query


def load_by_TODO_DIM() -> pd.DataFrame:
    """
    Aggregated by TODO_DIM — consumed by charts grouped by that dimension.

    Columns
    -------
    dim_TODO    : str/int  — dimension values
    val_TODO_1  : float    — primary measure
    val_TODO_2  : float    — secondary measure
    """
    return query("""
        SELECT TODO_dim_col               AS dim_TODO,
               AVG(TODO_measure_col)      AS val_TODO_1,
               SUM(TODO_other_col)        AS val_TODO_2
        FROM curated.mart_TODO_DOMAIN
        GROUP BY TODO_dim_col
        ORDER BY TODO_dim_col
    """)


def load_scalars() -> dict:
    """Single values for KPI cards."""
    row = query("""
        SELECT MAX(TODO_measure_col)  AS val_TODO_max,
               AVG(TODO_measure_col)  AS val_TODO_avg
        FROM curated.mart_TODO_DOMAIN
    """).iloc[0]
    return row.to_dict()
```

---

## app.py — wiring loaders to charts

```python
import products.dashboards.TODO_DOMAIN.measures as m
import products.dashboards.TODO_DOMAIN.semantic_service as _svc

# Load once at startup — no aggregation in callbacks
_df_by_TODO = _svc.load_by_TODO_DIM()
_scalars     = _svc.load_scalars()

# Dimension value lists — used for slicers
_TODO_values = m.DIMS["TODO_DIM_KEY"].values(_df_by_TODO)
```

---

## Rules
- All SQL lives in `semantic_service.py` — never in `app.py` or chart components
- Each loader returns one pre-aggregated DataFrame — no `.groupby()` in `app.py`
- Column names in SQL output must match the `col` field in `DIMS` and `MEASURES`
- `load_scalars()` returns a dict; use `m.MEASURES["key"].kpi_value(_scalars["col"])` in KPI cards
- Callbacks may re-filter an already-loaded DataFrame (e.g. by year) but must not re-aggregate
