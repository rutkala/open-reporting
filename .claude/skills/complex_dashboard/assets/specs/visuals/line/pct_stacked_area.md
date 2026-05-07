# 100% Stacked Area

## When to use
Relative composition over time — shows how shares of a whole evolve.
Use when absolute totals are irrelevant and only the changing proportions matter.
**Not:** when absolute values matter (use Stacked Area).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| X AXIS | Yes | time dimension |
| VALUES | Yes | 2–5 measures normalised to 100% |

## Import
```python
from complex_dashboard.assets.components.line_chart import pct_stacked_area
```

## Template
```python
html.Div(style=S["card"], children=[
    pct_stacked_area(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: GUS — dane za 2018–2024",
        x=m.DIMS["TODO_DIM"].values(_df_by_TODO),
        series=[
            m.MEASURES["TODO_1"].to_series(_df["TODO_col_1"].tolist()),
            m.MEASURES["TODO_2"].to_series(_df["TODO_col_2"].tolist()),
            m.MEASURES["TODO_3"].to_series(_df["TODO_col_3"].tolist()),
        ],
    )
])
```

## Rules
- Max 5 series
- Y axis fixed 0–100% — enforced
- No `y_measure` needed — axis is always percentage
