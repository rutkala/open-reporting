# Heatmap Matrix

## When to use
Matrix of values coloured by intensity — correlation matrices, period × category grids,
cross-tabulations where the pattern across cells matters more than individual values.
E.g. correlation between economic indicators, seasonality pattern (month × year).
**Not:** precise value comparison (use Table); single dimension (use Bar/Line).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| X LABELS | Yes | column dimension values |
| Y LABELS | Yes | row dimension values |
| Z VALUES | Yes | `list[list[float]]` — z_values[row][col] |
| COLOR SCALE | No | `"diverging"` (default, for +/-) or `"sequential"` (for 0+) |

## Import
```python
from products.visuals.components.special_chart import heatmap_matrix
```

## Template
```python
_x_labels = _df_hmap["dim_col"].unique().tolist()
_y_labels = _df_hmap["dim_row"].unique().tolist()
_z_values = [
    _df_hmap.loc[_df_hmap["dim_row"] == row, "val_z"].tolist()
    for row in _y_labels
]

html.Div(style=S["card"], children=[
    heatmap_matrix(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: GUS — dane za 2024 r.",
        x_labels=_x_labels,
        y_labels=_y_labels,
        z_values=_z_values,
        color_scale="diverging",   # "diverging" for +/- values, "sequential" for 0+
    )
])
```

## Rules
- `"diverging"` for values that go positive and negative (correlations, changes)
- `"sequential"` for values that are always positive (counts, intensities)
- Max ~12×12 cells before labels overlap
