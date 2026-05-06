# Area (Clustered)

## When to use
Time series where volume or magnitude matters — the filled area emphasises the scale
of the values, not just direction. Best for a single dominant series or 2–3 overlapping
series where volume comparison is the message.
**Not:** many overlapping series (too cluttered); when only trend direction matters (use Line).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| X AXIS | Yes | time dimension |
| VALUES | Yes | 1–3 measures (overlapping fills) |
| Y MEASURE | Yes | primary measure |

## Import
```python
from products.visuals.components.line_chart import area
```

## Template
```python
html.Div(style=S["card"], children=[
    area(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: GUS — dane za 2018–2024",
        x=m.DIMS["TODO_DIM"].values(_df_by_TODO),
        series=[
            m.MEASURES["TODO_1"].to_series(_df["TODO_col_1"].tolist()),
            m.MEASURES["TODO_2"].to_series(_df["TODO_col_2"].tolist()),
        ],
        y_measure=m.MEASURES["TODO_1"],
    )
])
```

## Rules
- Max 3 overlapping series — each fills from zero with 0.25 opacity (enforced)
- Prefer Line when series cross frequently (overlapping fills become unreadable)
- Y axis always starts at zero
