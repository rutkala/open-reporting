# 100% Stacked Column

## When to use
Showing relative composition (shares) across categories — when absolute totals are
irrelevant or misleading and only proportions matter.
**Not:** when absolute values matter (use Stacked Column); single series (use Bar).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| X AXIS | Yes | 1 dimension (year, category) |
| VALUES | Yes | 2–6 measures normalised to 100% |
| Y MEASURE | Yes | primary measure — controls axis label |

## Import
```python
from products.visuals.components.bar_chart import pct_stacked_column
```

## Template
```python
# X AXIS:    [dimension]
# VALUES:    [measure_1, …] — normalised to 100%, no absolute scale

html.Div(style=S["card"], children=[
    pct_stacked_column(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: GUS — dane za 2024 r.",
        x=m.DIMS["TODO_DIM"].values(_df_by_TODO),
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
- Y axis fixed 0–100% — enforced by component
- Add data labels to show % values when segments are small
