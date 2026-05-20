# Combo Subplots (stacked panels, shared X axis)

## When to use
Two or more measures with **different scales or units** that must be read
together across the same X axis. Each measure gets its own panel with its own
Y axis. This is the IBCS pattern for fiscal/macro reports when a dual y-axis
would misleadingly imply correlation.

Use instead of dual-axis whenever the scales differ. Dual-axis is banned
(see `chart-types.md` → Hard rules).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| X AXIS | Yes | shared time (or ordinal) dimension |
| PANELS | Yes | 2–4 panels — each is a `bar` or `line` view of one or more series |
| Panel title | Yes | per-panel Y-axis label with units |
| `diverging` flag | Optional | per panel — colours each point POSITIVE/NEGATIVE around zero |

## Import
```python
from complex_dashboard.assets.components.combo_chart import combo_subplots
```

## Template
```python
html.Div(style=S["card"], children=[
    combo_subplots(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: GUS — dane za 2018–2024",
        x=m.DIMS["TODO_DIM"].values(_df),
        panels=[
            {
                "title": "TODO: Panel 1 label (units)",
                "type":  "bar",
                "series": [
                    {"name": "TODO: label", "y": _df["TODO_col_1"].tolist()},
                ],
            },
            {
                "title": "TODO: Panel 2 label (pp)",
                "type":  "line",
                "diverging": True,   # marker colour per value around zero
                "series": [
                    {"name": "TODO: label", "y": _df["TODO_col_2"].tolist()},
                ],
            },
        ],
    )
])
```

## Rules
- Use only when measures have **different** scales or units — for same-scale pairs use `line_clustered_column`
- Max 4 panels per chart — more becomes unreadable at dashboard density
- Each panel's title must include units (e.g. `"Saldo (mld zł)"`, `"Dynamika (pp)"`)
- `y_measure` is not supported — configure per-panel labels via the `title` key
- Panels share the X axis — do not use for unrelated time ranges
- `diverging: True` is for series that naturally cross zero (variance, growth rate, balance)
- No legend — each panel self-labels via its Y-axis title
