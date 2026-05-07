# 100% Stacked Bar (Horizontal)

## When to use
Relative composition across categories with horizontal orientation — shares only,
no absolute values. Best for survey results, demographic splits, budget allocations.
**Not:** when absolute totals matter (use Stacked Bar).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| CATEGORIES | Yes | 1 dimension — displayed on Y axis |
| VALUES | Yes | 2–6 measures normalised to 100% |

## Import
```python
from complex_dashboard.assets.components.bar_chart import pct_stacked_bar
```

## Template
```python
html.Div(style=S["card"], children=[
    pct_stacked_bar(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: GUS — dane za 2024 r.",
        categories=m.DIMS["TODO_DIM"].values(_df_by_TODO),
        series=[
            m.MEASURES["TODO_1"].to_series(_df["TODO_col_1"].tolist()),
            m.MEASURES["TODO_2"].to_series(_df["TODO_col_2"].tolist()),
            m.MEASURES["TODO_3"].to_series(_df["TODO_col_3"].tolist()),
        ],
    )
])
```

## Rules
- Max 6 segments
- X axis fixed 0–100% — enforced by component
- No `y_measure` needed — axis is always percentage
