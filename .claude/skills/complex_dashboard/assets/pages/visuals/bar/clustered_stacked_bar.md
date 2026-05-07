# Clustered + Stacked Bar (Horizontal)

## When to use
Horizontal variant of Clustered + Stacked Column — use when category names are long.
Same analytical use case: groups compared side by side, each group internally stacked.
**Not:** for simple comparisons; use only when both group comparison and internal
composition are analytically necessary.

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| CATEGORIES | Yes | 1 dimension — displayed on Y axis |
| GROUPS | Yes | list of group dicts — each group has stacked series |
| Y MEASURE | Yes | primary measure |

## Import
```python
from products.visuals.components.bar_chart import clustered_stacked_bar
```

## Template
```python
_groups = [
    {"name": "TODO_GROUP_1", "series": [
        {"name": "TODO_SERIES_1", "y": [...]},
        {"name": "TODO_SERIES_2", "y": [...]},
    ]},
    {"name": "TODO_GROUP_2", "series": [
        {"name": "TODO_SERIES_1", "y": [...]},
        {"name": "TODO_SERIES_2", "y": [...]},
    ]},
]

html.Div(style=S["card"], children=[
    clustered_stacked_bar(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: GUS — dane za 2024 r.",
        categories=m.DIMS["TODO_DIM"].values(_df_by_TODO),
        groups=_groups,
        y_measure=m.MEASURES["TODO_1"],
    )
])
```

## Rules
- Max 3 groups, max 4 stacked series per group
- Series names consistent across all groups
- Prefer over vertical variant when category labels exceed ~10 characters
