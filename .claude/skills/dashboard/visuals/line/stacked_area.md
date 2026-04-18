# Stacked Area

## When to use
Composition over time in absolute values — shows both the total and how its parts
change. Use when the total trend AND the segment breakdown both matter.
**Not:** when only shares matter (use 100% Stacked Area); when segments frequently
reverse order (use Stacked Column for discrete periods instead).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| X AXIS | Yes | time dimension |
| VALUES | Yes | 2–5 measures stacked cumulatively |
| Y MEASURE | Yes | primary measure |

## Import
```python
from products.visuals.components.line_chart import stacked_area
```

## Template
```python
html.Div(style=S["card"], children=[
    stacked_area(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: GUS — dane za 2018–2024",
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
- Max 5 stacked series
- Stack order: largest / most stable series at bottom
- Y axis starts at zero — enforced
