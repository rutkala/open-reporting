# Line

## When to use
Trends over time — the primary choice for any temporal data. Shows direction,
rate of change, and multiple series on the same scale.
**Not:** discrete categories without natural order (use Clustered Column);
when volume/accumulation is the message (use Area).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| X AXIS | Yes | time dimension (year, quarter, month) |
| VALUES | Yes | 1–5 measures as separate lines |
| Y MEASURE | Yes | primary measure — controls axis label + tick format |
| REFERENCE | No | `{"value": float, "label": str}` — horizontal reference line |

## Import
```python
from products.visuals.components.line_chart import line
```

## Template
```python
# X AXIS:    [time dimension] — e.g. m.DIMS["year"]
# VALUES:    [measure_1, …] — max 5 series
# Y MEASURE: [primary measure]
# REFERENCE: optional — benchmark, target, EU average

html.Div(style=S["card"], children=[
    line(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: GUS — dane za 2018–2024",
        x=m.DIMS["TODO_DIM"].values(_df_by_TODO),
        series=[
            m.MEASURES["TODO_1"].to_series(_df["TODO_col_1"].tolist()),
            m.MEASURES["TODO_2"].to_series(_df["TODO_col_2"].tolist()),
        ],
        reference={"value": TODO_REFERENCE_VALUE, "label": "TODO: UE-27 / Cel"},  # optional
        y_measure=m.MEASURES["TODO_1"],
    )
])
```

## Rules
- Max 4–5 visible series (direct-label if ≤4)
- Beyond 5 series: show top series individually, group rest as "Pozostałe"
- No smoothing — linear interpolation only (enforced by component)
- Line width minimum 2px (enforced)
- Reference line in `ZERO_LINE` colour — never a data colour
