# Semantic Layer — Dimension and Measure

All charts and KPI cards are driven by `Dimension` and `Measure` dataclasses from
`products/visuals/lib/semantic.py`. These are **display-config objects only** — they
carry labels, units, and format settings. All aggregation lives upstream in `data.py`
(template) or `semantic_service.py` (domain dashboards).

Define them in `measures.py` at the top of each dashboard. Never hardcode format
strings or axis labels in `app.py`.

---

## Import

```python
from products.visuals.lib.semantic import Dimension, Measure
```

---

## Dimension

Represents a categorical or temporal axis variable.

```python
@dataclass
class Dimension:
    name:   str   # machine key used in DIMS dict — e.g. "year"
    label:  str   # user-facing label for axis / legend — e.g. "Year"
    column: str   # DataFrame column that holds dimension values — e.g. "dim_year"
```

### Method

```python
dim.values(df) -> list
```
Returns ordered unique values from the dimension column (first-occurrence order,
matching typical `ORDER BY` from queries).

### Usage in app.py

```python
DIMS = {
    "year":     Dimension("year",     "Rok",       "dim_year"),
    "category": Dimension("category", "Kategoria", "dim_category"),
    "region":   Dimension("region",   "Region",    "dim_region"),
}

_years = m.DIMS["year"].values(_df_by_year)      # → [2018, 2019, ..., 2024]
_categories = m.DIMS["category"].values(_df_by_cat)
```

---

## Measure

Display metadata for a numeric indicator.

```python
@dataclass
class Measure:
    name:            str                                          # machine key
    label:           str                                          # user-facing label (Polish)
    column:          str                                          # DataFrame column
    unit:            str   = ""                                   # physical unit, e.g. "pp", "tys. osób"
    format_type:     Literal["number", "currency", "percent", "text"] = "number"
    scale:           Literal[None, "K", "M", "B"] = None          # magnitude divisor
    decimals:        int   = 1                                    # decimal places
    currency_symbol: str   = ""                                   # e.g. "zł", "€"
    show_unit:       bool  = True
```

### Properties

| Property | Returns | Use |
|----------|---------|-----|
| `.axis_label` | `str` | Y-axis title: `"Zatrudnienie (tys. osób)"` |
| `.plotly_tickformat` | `str` | D3 format: `",.1f"` or `".1f"` |
| `.plotly_ticksuffix` | `str` | Tick suffix: `" tys."`, `"%"`, `" zł"` |

### Methods

| Method | Returns | Use |
|--------|---------|-----|
| `.to_series(y: list)` | `{"name": label, "y": y}` | Drop-in for chart `series=` lists |
| `.kpi_value(v: float)` | `str` | Formatted number for `kpi_standard(value=)` |
| `.format_value(v: float)` | `str` | Fully formatted string with unit |
| `.fmt_labels(values: list)` | `list[str]` | Formatted strings for data labels |
| `.apply_to_yaxis(axis_dict)` | `None` | Updates Plotly yaxis dict in-place |
| `.apply_to_xaxis(axis_dict)` | `None` | Updates Plotly xaxis dict in-place |

### Usage in app.py

```python
MEASURES = {
    "employment": Measure(
        "employment", "Zatrudnienie", "val_employment",
        unit="tys. osób", format_type="number", decimals=1,
    ),
    "rate": Measure(
        "rate", "Stopa bezrobocia", "val_rate",
        format_type="percent", decimals=1,
    ),
    "gdp": Measure(
        "gdp", "PKB", "val_gdp",
        format_type="currency", scale="M", currency_symbol="zł", decimals=1,
    ),
}

# In chart calls:
line("Zatrudnienie 2018–2024",
    x=_years,
    series=[
        m.MEASURES["employment"].to_series(_df_by_year["val_employment"].tolist()),
    ],
    y_measure=m.MEASURES["employment"])

# In KPI cards:
kpi_standard(
    label=m.MEASURES["rate"].label,
    value=m.MEASURES["rate"].kpi_value(_scalars["rate"]),
    unit=m.MEASURES["rate"].plotly_ticksuffix,
    reference_value=m.MEASURES["rate"].kpi_value(5.0),
    reference_label="Cel",
    trend="▲ +0.3", trend_color=POSITIVE,
)
```

---

## format_type guide

| format_type | Example output | Use for |
|-------------|---------------|---------|
| `"number"`  | `"12,345.6 tys."` | Most economic indicators |
| `"percent"` | `"4.2%"` | Rates, shares, changes in pp |
| `"currency"` | `"1,234.5M zł"` | Monetary values |
| `"text"`    | raw string | Categorical labels, codes |

## scale guide

| scale | Divisor | axis_label suffix |
|-------|---------|-------------------|
| `None` | 1 (raw) | `(tys. osób)` — unit only |
| `"K"` | 1,000 | `(K tys.)` |
| `"M"` | 1,000,000 | `(M zł)` |
| `"B"` | 1,000,000,000 | `(B zł)` |

---

## Full measures.py example

```python
from products.visuals.lib.semantic import Dimension, Measure

DIMS = {
    "year":   Dimension("year",   "Rok",     "dim_year"),
    "region": Dimension("region", "Region",  "dim_region"),
    "sector": Dimension("sector", "Sektor",  "dim_sector"),
}

MEASURES = {
    # Primary measure — absolute value
    "employment": Measure(
        "employment", "Zatrudnienie", "val_employment",
        unit="tys. osób", format_type="number", scale=None, decimals=1,
    ),
    # Rate measure
    "unemployment_rate": Measure(
        "unemployment_rate", "Stopa bezrobocia", "val_unemployment_rate",
        format_type="percent", decimals=1,
    ),
    # YoY change (percent points)
    "employment_yoy": Measure(
        "employment_yoy", "Zmiana r/r", "val_employment_yoy",
        unit="pp", format_type="number", decimals=1,
    ),
    # Currency
    "avg_wage": Measure(
        "avg_wage", "Wynagrodzenie przeciętne", "val_avg_wage",
        format_type="currency", currency_symbol="zł", decimals=0,
    ),
}
```
