# Line + Clustered Column

## When to use
Two measures on the same scale — one shown as bars (volume/discrete), one as a line
(trend/rate). E.g. employment count (bars) + employment growth rate (line) over time.
**Not:** two measures on different scales (no dual axis — use subplots instead).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| X AXIS | Yes | time dimension |
| BAR VALUES | Yes | 1–4 measures shown as grouped bars |
| LINE VALUES | Yes | 1–2 measures shown as lines |
| Y MEASURE | Yes | primary measure — shared scale for both |

## Import
```python
from products.visuals.components.combo_chart import line_clustered_column
```

## Template
```python
# SAME SCALE ONLY — both bar and line series must share the same unit/magnitude
# If scales differ, use two separate charts stacked vertically instead

html.Div(style=S["card"], children=[
    line_clustered_column(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: GUS — dane za 2018–2024",
        x=m.DIMS["TODO_DIM"].values(_df_by_TODO),
        bar_series=[
            m.MEASURES["TODO_BAR"].to_series(_df["TODO_bar_col"].tolist()),
        ],
        line_series=[
            m.MEASURES["TODO_LINE"].to_series(_df["TODO_line_col"].tolist()),
        ],
        y_measure=m.MEASURES["TODO_BAR"],
    )
])
```

## Rules
- Same-scale data only — no dual y-axis (IBCS rule)
- If scales differ: split into two separate charts
- Max 4 bar series + 2 line series
