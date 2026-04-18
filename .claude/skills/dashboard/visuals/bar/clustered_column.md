# Clustered Column

## When to use
Comparing values of 2–6 measures side by side across categories.
**Not:** trends over time (use Line); single series ranking (use Clustered Bar horizontal);
more than 6 series (group remainder as "Pozostałe").

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| X AXIS | Yes | 1 dimension (category, region, sector) |
| VALUES | Yes | 1–6 measures compared side by side |
| Y MEASURE | Yes | primary measure — controls axis label + tick format |

## Import
```python
from products.visuals.components.bar_chart import clustered_column
```

## Template
```python
# X AXIS:    [dimension] — e.g. m.DIMS["category"], m.DIMS["sector"]
# VALUES:    [measure_1, …] up to 6 series
# Y MEASURE: [primary measure]

html.Div(style=S["card"], children=[
    clustered_column(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: GUS — dane za 2024 r.",
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
- Max 6 series
- Sort categories descending by primary measure value unless natural order applies
- Y axis always starts at zero — enforced by component
- Prefer Clustered Bar (horizontal) when category names are long
