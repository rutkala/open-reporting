# Line + 100% Stacked Column

## When to use
100% stacked bars show share composition, line overlays a rate or percentage on the
same 0–100 scale. E.g. employment share by sector (bars) + activity rate % (line).
**Not:** when the line measure is not on a 0–100% scale.

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| X AXIS | Yes | time dimension |
| BAR VALUES | Yes | 2–5 measures normalised to 100% |
| LINE VALUES | Yes | 1–2 percentage/rate measures |
| Y MEASURE | Yes | primary measure |

## Import
```python
from products.visuals.components.combo_chart import line_pct_stacked_column
```

## Template
```python
html.Div(style=S["card"], children=[
    line_pct_stacked_column(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: GUS — dane za 2018–2024",
        x=m.DIMS["TODO_DIM"].values(_df_by_TODO),
        bar_series=[
            m.MEASURES["TODO_1"].to_series(_df["TODO_col_1"].tolist()),
            m.MEASURES["TODO_2"].to_series(_df["TODO_col_2"].tolist()),
        ],
        line_series=[
            m.MEASURES["TODO_RATE"].to_series(_df["TODO_rate_col"].tolist()),
        ],
        y_measure=m.MEASURES["TODO_1"],
    )
])
```

## Rules
- Line measure must be a percentage/rate that makes sense on the 0–100 scale
- Y axis fixed 0–100% — enforced
