# Waterfall — Variance

## When to use
Explaining how a base value becomes an ending value — bridge between two absolutes.
E.g. "how did we go from last year's balance to this year's?" or "budget vs actual breakdown".
Use when the start → changes → end story is the main message.
**Not:** parts-to-total (use Waterfall Contribution); trends (use Line).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| CATEGORIES | Yes | stage labels: opening, change drivers, closing |
| VALUES | Yes | opening value, change values, closing value |
| Y MEASURE | Yes | primary measure |

## Import
```python
from complex_dashboard.assets.components.waterfall_chart import waterfall_variance
```

## Data structure
```python
_df_wf = pd.DataFrame({
    "dim_stage":  ["TODO_OPENING", "TODO_CHANGE_A", "TODO_CHANGE_B", "TODO_CLOSING"],
    "val_amount": [1240.0,          180.0,           -90.0,            1330.0],
    "is_total":   [False,            False,            False,            True],
    "is_base":    [True,             False,            False,            False],
})
```

## Template
```python
html.Div(style=S["card"], children=[
    waterfall_variance(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: GUS — dane za 2024 r.",
        categories=_df_wf["dim_stage"].tolist(),
        values=_df_wf["val_amount"].tolist(),
        y_measure=m.MEASURES["TODO_1"],
    )
])
```

## Rules
- Opening bar (`is_base=True`) and closing bar (`is_total=True`) rendered as full bars (enforced)
- Intermediate bars show deltas — positive: `POSITIVE` green, negative: `NEGATIVE` red (enforced)
- Value labels on every bar (enforced)
