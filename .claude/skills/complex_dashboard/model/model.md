# Semantic Model Binding

## What it is
The report (this dashboard) binds to exactly one semantic model. The report consumes the model — it does not define measures, write SQL, or aggregate data. This file specifies the **interface** the report expects the model to expose. Implementation lives in the `semantic-model` skill.

Power BI analogy: the Fields pane in Power BI Desktop lists tables, columns, and measures from the connected dataset. This document describes the equivalent binding for a Dash report.

---

## Required interface — `MEASURES` dict

The report imports a `MEASURES` dict from the dashboard's `measures.py` module. Every entry must expose:

| Attribute / Method | Signature | Used for |
|---|---|---|
| `.label` | `-> str` | Display label (Polish) in chart/KPI headings |
| `.plotly_ticksuffix` | `-> str` | Axis tick suffix (`%`, ` mln zł`, etc.) |
| `.to_series(values: list) -> dict` | returns `{"name": label, "y": values}` | Series payload for chart components |
| `.kpi_value(scalar: float) -> str` | formatted string | KPI card value rendering |

## Required interface — `DIMS` dict

The report imports a `DIMS` dict from `measures.py`. Every entry must expose:

| Attribute / Method | Signature | Used for |
|---|---|---|
| `.col` | `-> str` | Underlying DataFrame column name |
| `.values(df) -> list` | unique ordered values | Slicer options, chart X-axis values |

## Required interface — loader functions

The report imports loader functions from `semantic_service.py`. Each loader returns a pre-aggregated DataFrame ready to plot:

| Pattern | Signature | Used for |
|---|---|---|
| `load_*(...)` | `-> pandas.DataFrame` | One loader per chart or section |
| `load_scalars()` | `-> dict` | Single values for KPI cards |

---

## Usage in `app.py`

```python
import products.dashboards.TODO_DOMAIN.measures as m
import products.dashboards.TODO_DOMAIN.semantic_service as _svc

# Load once at startup — no aggregation in callbacks
_df_by_region = _svc.load_by_region()
_scalars      = _svc.load_scalars()

# Consume the interface
kpi_standard(
    label=m.MEASURES["unemployment"].label,
    value=m.MEASURES["unemployment"].kpi_value(_scalars["unemployment"]),
    unit=m.MEASURES["unemployment"].plotly_ticksuffix,
)

line(
    "TODO: title",
    x=m.DIMS["year"].values(_df_by_region),
    series=[m.MEASURES["unemployment"].to_series(_df_by_region["val_unemployment"].tolist())],
    y_measure=m.MEASURES["unemployment"],
)
```

---

## Rules

- The report **never instantiates** `Measure` or `Dimension` — only consumes them
- The report **never writes SQL** — only calls loader functions
- The report **never aggregates** (no `.groupby()`, no `SUM(...)`, no pivoting in `app.py`)
- Loaders are called **once at module load** — never inside callbacks
- Callbacks may filter an already-loaded DataFrame (e.g., by slicer value) but must not re-aggregate
- If a measure, dimension, or loader is missing, that's a **semantic-model bug** — fix it in the `semantic-model` skill, not here
- Column names returned by loaders must match the `col` field registered in `DIMS` / `MEASURES`
