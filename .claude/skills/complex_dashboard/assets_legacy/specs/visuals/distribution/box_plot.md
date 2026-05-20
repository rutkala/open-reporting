# Box Plot

## When to use
Comparing distributions across 2–6 groups — shows median, IQR, whiskers, and outliers.
E.g. wage distribution by sector, regional unemployment spread by year.
**Not:** single variable distribution (use Histogram); showing exact values (use Table).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| DATA | Yes | `dict[group_label, list[float]]` — observations per group |
| Y MEASURE | Yes | primary measure |

## Import
```python
from complex_dashboard.assets.components.distribution_chart import box_plot
```

## Template
```python
# DATA: {group_label: [raw observations]}
# Build from DataFrame grouped by dimension:

_box_data = {
    grp: _df.loc[_df["dim_TODO_DIM"] == grp, "val_TODO_col"].tolist()
    for grp in m.DIMS["TODO_DIM"].values(_df)
}

html.Div(style=S["card"], children=[
    box_plot(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: GUS — dane za 2024 r.",
        data=_box_data,
        y_measure=m.MEASURES["TODO_1"],
    )
])
```

## Rules
- Max 6 groups (more becomes unreadable)
- Minimum ~8 observations per group for box to be meaningful
- Outliers shown as points — do not suppress
