# Waterfall — Contribution

## When to use
Showing how individual components add up to a total — additive decomposition.
E.g. "what components make up the fiscal deficit?" or "which sectors contribute
most to GDP growth?". Use when the parts → total story is the main message.
**Not:** comparing two absolute values (use Waterfall Variance); trends (use Line).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| CATEGORIES | Yes | list of component labels + total label |
| VALUES | Yes | contribution values (positive = adds, negative = subtracts) |
| TOTAL LABEL | Yes | label of the final bar (the sum) |
| Y MEASURE | Yes | primary measure |

## Import
```python
from complex_dashboard.assets.components.waterfall_chart import waterfall_contribution
```

## Data structure
The source DataFrame must have columns: `dim_stage`, `val_amount`, `is_total`, `is_base`.

```python
# Build from a data loader or inline:
_df_wf = pd.DataFrame({
    "dim_stage":  ["TODO_COMP_A", "TODO_COMP_B", "TODO_ADJ", "TODO_TOTAL"],
    "val_amount": [295.0,          135.0,         -90.0,       340.0],
    "is_total":   [False,           False,          False,       True],
    "is_base":    [False,           False,          False,       False],
})
```

## Template
```python
html.Div(style=S["card"], children=[
    waterfall_contribution(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: GUS — dane za 2024 r.",
        categories=_df_wf["dim_stage"].tolist(),
        values=_df_wf["val_amount"].tolist(),
        total_label=_df_wf.loc[_df_wf["is_total"], "dim_stage"].iloc[0],
        y_measure=m.MEASURES["TODO_1"],
    )
])
```

## Rules
- Sum of non-total bars must equal the total bar value
- Positive contributions: `POSITIVE` green; negative: `NEGATIVE` red; total: `SLATE_1` grey (enforced)
- Value labels shown on every bar (enforced)
- Sort components by magnitude (largest contribution first) unless logical order applies
