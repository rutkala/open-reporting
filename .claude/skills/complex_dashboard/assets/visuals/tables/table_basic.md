# Table

## When to use
Exact values that users need to read and compare precisely — when the numbers
themselves are the message, not a pattern. Use alongside charts, not instead of them.
**Not:** showing trends (use Line); showing distributions (use Histogram); as the
primary visual — always pair with a chart.

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| HEADERS | Yes | list of column header strings |
| ROWS | Yes | list of rows, each row is a list of values |
| NUMBER COLS | Yes | set of column indices (0-based) to right-align |

## Import
```python
from products.visuals.components.table_chart import table_basic
```

## Template
```python
html.Div(style=S["card"], children=[
    table_basic(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: GUS — dane za 2024 r.",
        headers=["TODO_DIM_LABEL", "TODO_MEASURE_1", "TODO_MEASURE_2"],
        rows=[
            [row["dim_TODO"], row["val_1"], row["val_2"]]
            for _, row in _df_table.iterrows()
        ],
        number_cols={1, 2},   # 0-based indices of numeric columns → right-aligned
    )
])
```

## Rules
- Numbers right-aligned (set via `number_cols`)
- Text/dimension columns left-aligned (default)
- Max ~15 rows before table needs pagination or filtering
- Format numbers consistently — use `Measure.format_value()` if needed
