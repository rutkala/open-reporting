# Funnel

## When to use
Sequential stages with progressive drop-off — conversion tracking, process pipelines.
E.g. job applications → interviews → offers → hires; budget → commitments → disbursements.
**Not:** when stages are not sequential; when volumes are similar across stages (use Bar).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| STAGES | Yes | ordered list of stage labels |
| VALUES | Yes | volume at each stage (descending order) |

## Import
```python
from complex_dashboard.assets.components.special_chart import funnel
```

## Template
```python
html.Div(style=S["card"], children=[
    funnel(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: GUS — dane za 2024 r.",
        stages=_df_funnel["dim_stage"].tolist(),   # ordered Stage 1 → Stage N
        values=_df_funnel["val_count"].tolist(),
    )
])
```

## Rules
- Stages must be in sequential order (first = largest)
- Values should be strictly decreasing (funnel logic)
- Label each stage with absolute value and conversion rate if available
