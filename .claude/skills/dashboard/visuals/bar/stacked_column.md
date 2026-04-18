# Stacked Column

## When to use
Showing total value AND composition across categories or time periods.
**Not:** when individual segment comparison matters (use Clustered Column);
when composition share matters more than absolute (use 100% Stacked Column).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| X AXIS | Yes | 1 dimension (year, category) |
| VALUES | Yes | 2–6 measures stacked into total |
| Y MEASURE | Yes | primary measure — controls axis label + tick format |

## Import
```python
from products.visuals.components.bar_chart import stacked_column
```

## Template
```python
# X AXIS:    [dimension]
# VALUES:    [measure_1, …] — stacked, order = visual stack order bottom to top
# Y MEASURE: [primary measure]

html.Div(style=S["card"], children=[
    stacked_column(
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
- Stack order: largest / most important segment at bottom
- Y axis always starts at zero
