# Data List

## When to use
Scrollable ranked list of labelled items with optional values — for top-N rankings,
recent events, or reference lists where a full table is too heavy.
E.g. top 10 voivodeships by employment, top companies by revenue.
**Not:** when numeric comparison matters (use Bar); when multiple measures per row needed (use Table).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| ITEMS | Yes | `list[{"label": str, "value": str}]` |

## Import
```python
from products.visuals.components.table_chart import data_list
```

## Template
```python
# ITEMS: pre-formatted label + value pairs
# Format values using Measure.format_value() for consistency

_items = [
    {"label": row["dim_TODO_label"], "value": m.MEASURES["TODO"].format_value(row["val_TODO"])}
    for _, row in _df_ranked.sort_values("val_TODO", ascending=False).head(10).iterrows()
]

html.Div(style={"maxWidth": "360px"}, children=[
    data_list(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: GUS — dane za 2024 r.",
        items=_items,
    )
])
```

## Rules
- Pre-sort by value before passing to component
- Limit to top 10–15 items
- Format values with `Measure.format_value()` for consistency
- Wrap in `maxWidth` div to control width in grid layouts
