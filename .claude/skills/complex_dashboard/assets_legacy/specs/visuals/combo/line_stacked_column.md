# Line + Stacked Column

## When to use
Stacked bars show composition, line shows an aggregate or rate on the same scale.
E.g. employment by sector (stacked bars) + total employment index (line) over time.
**Not:** different scales (use separate charts); when composition isn't the main message.

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| X AXIS | Yes | time dimension |
| BAR VALUES | Yes | 2–5 measures stacked |
| LINE VALUES | Yes | 1–2 aggregate/rate measures as lines |
| Y MEASURE | Yes | primary measure — shared scale |

## Import
```python
from complex_dashboard.assets.components.combo_chart import line_stacked_column
```

## Template
```python
html.Div(style=S["card"], children=[
    line_stacked_column(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: GUS — dane za 2018–2024",
        x=m.DIMS["TODO_DIM"].values(_df_by_TODO),
        bar_series=[
            m.MEASURES["TODO_1"].to_series(_df["TODO_col_1"].tolist()),
            m.MEASURES["TODO_2"].to_series(_df["TODO_col_2"].tolist()),
            m.MEASURES["TODO_3"].to_series(_df["TODO_col_3"].tolist()),
        ],
        line_series=[
            m.MEASURES["TODO_LINE"].to_series(_df["TODO_line_col"].tolist()),
        ],
        y_measure=m.MEASURES["TODO_1"],
    )
])
```

## Rules
- Same scale only
- Line series should represent an aggregate or derived measure of the bar series
