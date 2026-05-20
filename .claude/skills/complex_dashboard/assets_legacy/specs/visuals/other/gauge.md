# Gauge

## When to use
Single KPI progress against a range with a reference point — when the position within
a range is the message (not just the value). Use sparingly — prefer Bullet chart.
**Not:** as the default KPI visual (use KPI Card or Bullet); for comparing multiple values.

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| VALUE | Yes | current scalar value |
| MIN VAL | Yes | minimum of the range |
| MAX VAL | Yes | maximum of the range |
| REFERENCE | Yes | target / threshold value |
| Y MEASURE | Yes | primary measure |

## Import
```python
from complex_dashboard.assets.components.special_chart import gauge
```

## Template
```python
html.Div(style={"maxWidth": "360px"}, children=[
    html.Div(style=S["card"], children=[
        gauge(
            "TODO: analytical conclusion as title",
            subtitle="TODO: Źródło: GUS — dane za 2024 r.",
            value=_scalars["TODO_metric"],
            min_val=0,
            max_val=TODO_MAX,
            reference=TODO_TARGET,
            y_measure=m.MEASURES["TODO_1"],
        )
    ])
])
```

## Rules
- Use only when position within a range matters (e.g. debt-to-GDP vs Maastricht 60%)
- Prefer Bullet chart — more precise, less chart junk
- Wrap in `maxWidth: 360px` div — gauge is narrow by design
- Always set meaningful `min_val` and `max_val` (not 0–100 by default)
