# Bullet

## When to use
KPI value vs target with a background range — the IBCS-preferred alternative to Gauge.
More precise, less chart junk. E.g. actual revenue vs budget, actual deficit vs Maastricht limit.
**Not:** for multiple KPIs in a row (use KPI Card row); for trends (use Line).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| VALUE | Yes | current scalar value |
| TARGET | Yes | target / threshold value |
| MAX VAL | Yes | maximum of the background range |
| Y MEASURE | Yes | primary measure |

## Import
```python
from products.visuals.components.special_chart import bullet
```

## Template
```python
html.Div(style={"maxWidth": "360px"}, children=[
    html.Div(style=S["card"], children=[
        bullet(
            "TODO: analytical conclusion as title",
            subtitle="TODO: Źródło: GUS — dane za 2024 r.",
            value=_scalars["TODO_metric"],
            target=TODO_TARGET,
            max_val=TODO_MAX,
            y_measure=m.MEASURES["TODO_1"],
        )
    ])
])
```

## Rules
- Preferred over Gauge for KPI vs target (IBCS)
- Wrap in `maxWidth: 360px` div
- `target` line shown as vertical marker; `value` bar extends from zero
- Set `max_val` to a meaningful upper bound (not just value + 20%)
