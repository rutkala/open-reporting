# Ribbon (Bump Chart)

## When to use
Rank changes over time — showing which entities move up or down in ranking across
periods. Highest rank always at top. E.g. country rankings by competitiveness index,
regional rankings by employment rate over years.
**Not:** absolute value trends (use Line); static rankings (use Clustered Bar).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| X AXIS | Yes | sorted time periods |
| SERIES | Yes | `list[{"name": str, "ranks": list[int]}]` — rank per period |

## Import
```python
from products.visuals.components.special_chart import ribbon
```

## Template
```python
# SERIES: one entry per entity, ranks list must align with x periods
# Rank 1 = best position (top of chart)

_x_periods = sorted(_df_ribbon["dim_year"].unique().tolist())
_series = [
    {
        "name": entity,
        "ranks": _df_ribbon.loc[
            _df_ribbon["dim_entity"] == entity
        ].sort_values("dim_year")["val_rank"].tolist()
    }
    for entity in _df_ribbon["dim_entity"].unique().tolist()
]

html.Div(style=S["card"], children=[
    ribbon(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: GUS — dane za 2018–2024",
        x=_x_periods,
        series=_series,
    )
])
```

## Rules
- Rank 1 = best (rendered at top) — enforced by component
- Max ~8 entities before chart becomes cluttered
- All entities must have a rank for every period (no gaps)
