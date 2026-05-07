# Clustered + Stacked Column

## When to use
Advanced: comparing groups side by side where each group itself is a stacked composition.
E.g. employment by sector (groups) broken down by contract type (stacks) across regions.
**Not:** for simple comparisons (use Clustered Column); use only when both the group
comparison AND the internal composition are analytically meaningful.

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| X AXIS | Yes | 1 dimension (categories on x axis) |
| GROUPS | Yes | list of group dicts — each group has stacked series |
| Y MEASURE | Yes | primary measure |

## Import
```python
from complex_dashboard.assets.components.bar_chart import clustered_stacked_column
```

## Template
```python
# GROUPS format: [{"name": "Group A", "series": [{"name": "Series 1", "y": [...]}, ...]}, ...]

_groups = [
    {"name": "TODO_GROUP_1", "series": [
        {"name": "TODO_SERIES_1", "y": _df.loc[_df["dim_group"] == "TODO_GROUP_1", "val_a"].tolist()},
        {"name": "TODO_SERIES_2", "y": _df.loc[_df["dim_group"] == "TODO_GROUP_1", "val_b"].tolist()},
    ]},
    {"name": "TODO_GROUP_2", "series": [
        {"name": "TODO_SERIES_1", "y": _df.loc[_df["dim_group"] == "TODO_GROUP_2", "val_a"].tolist()},
        {"name": "TODO_SERIES_2", "y": _df.loc[_df["dim_group"] == "TODO_GROUP_2", "val_b"].tolist()},
    ]},
]

html.Div(style=S["card"], children=[
    clustered_stacked_column(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: GUS — dane za 2024 r.",
        x=m.DIMS["TODO_DIM"].values(_df_by_TODO),
        groups=_groups,
        y_measure=m.MEASURES["TODO_1"],
    )
])
```

## Rules
- Use sparingly — high cognitive load
- Max 3 groups, max 4 stacked series per group
- Series names must be consistent across all groups
