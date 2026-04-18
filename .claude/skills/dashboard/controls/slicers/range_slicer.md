# Range Slicer

## When to use
Dual-handle numeric range slider — when users need to filter by a continuous numeric
range (value threshold, year range as numbers, age bracket).
**Not:** discrete categories (use List or Dropdown); date ranges (use Date Range Slicer).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| TITLE | Yes | filter label |
| MIN VAL | Yes | minimum value of the range |
| MAX VAL | Yes | maximum value of the range |
| VALUE | No | `[start, end]` pre-selected range (defaults to full range) |

## Import
```python
from products.visuals.components.slicer import range_slicer
```

## Template
```python
range_slicer(
    "TODO: Filter label (Polish)",
    min_val=TODO_MIN,           # e.g. 0, int(_df["val_col"].min())
    max_val=TODO_MAX,           # e.g. 100, int(_df["val_col"].max())
    value=[TODO_MIN, TODO_MAX], # default: full range
    subtitle="",
)
```

## Callback pattern
```python
@callback(
    Output("TODO-chart-id", "figure"),
    Input("TODO-slicer-id", "value"),
)
def update_chart(range_value):
    low, high = range_value
    filtered = _df[(_df["val_col"] >= low) & (_df["val_col"] <= high)]
    ...
```

## Rules
- Callback receives `[low, high]` list — always unpack both handles
- Handle edge case: low == high → show single-value result or empty state
- Wrap in `maxWidth: 480px` for readability
