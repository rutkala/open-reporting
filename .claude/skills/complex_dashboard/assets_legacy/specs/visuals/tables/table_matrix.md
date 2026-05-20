# Matrix / Pivot Table

## When to use
Cross-tabulation of two dimensions with values at intersections — when both the row
and column dimensions are analytically meaningful. E.g. measures by year × region,
or indicators by country × year.
**Not:** simple list of rows (use Table); when one dimension is the primary axis (use Bar).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| ROW LABELS | Yes | list of row dimension values |
| COL LABELS | Yes | list of column dimension values |
| VALUES | Yes | `list[list[float]]` — values[row_index][col_index] |
| ROW DIM | Yes | label for the row dimension column header |

## Import
```python
from complex_dashboard.assets.components.table_chart import table_matrix
```

## Template
```python
# Build values matrix from DataFrame:
_row_labels = m.DIMS["TODO_ROW_DIM"].values(_df)
_col_labels = m.DIMS["TODO_COL_DIM"].values(_df)
_values = [
    [_df.loc[(_df["dim_row"] == r) & (_df["dim_col"] == c), "val_TODO"].iloc[0]
     for c in _col_labels]
    for r in _row_labels
]

html.Div(style=S["card"], children=[
    table_matrix(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: GUS — dane za 2024 r.",
        row_labels=_row_labels,
        col_labels=_col_labels,
        values=_values,
        row_dim="TODO: Row dimension label",
    )
])
```

## Rules
- Values must be pre-aggregated — one value per row/col intersection
- Max ~10 rows × ~10 columns before readability drops
