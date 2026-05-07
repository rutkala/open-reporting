# Stacked Bar (Horizontal)

## When to use
Composition across categories with horizontal orientation — when category names are long
and you need both total and segment breakdown.
**Not:** time series; when only shares matter (use 100% Stacked Bar).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| CATEGORIES | Yes | 1 dimension — displayed on Y axis |
| VALUES | Yes | 2–6 measures stacked |
| Y MEASURE | Yes | primary measure |

## Import
```python
from complex_dashboard.assets.components.bar_chart import stacked_bar
```

## Template
```python
html.Div(style=S["card"], children=[
    stacked_bar(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: GUS — dane za 2024 r.",
        categories=m.DIMS["TODO_DIM"].values(_df_by_TODO),
        series=[
            m.MEASURES["TODO_1"].to_series(_df["TODO_col_1"].tolist()),
            m.MEASURES["TODO_2"].to_series(_df["TODO_col_2"].tolist()),
            m.MEASURES["TODO_3"].to_series(_df["TODO_col_3"].tolist()),
        ],
        y_measure=m.MEASURES["TODO_1"],
    )
])
```

## Rules
- Max 6 segments
- Sort categories by total value descending
