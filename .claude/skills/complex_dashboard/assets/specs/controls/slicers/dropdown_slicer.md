# Dropdown Slicer

## When to use
Single-select filter from a collapsed list — when options are numerous (>6) or screen
space is limited. Most common slicer type for dimension filters (year, region, sector).
**Not:** when all options should be visible at once (use List or Tile Slicer).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| TITLE | Yes | filter label shown above the dropdown |
| OPTIONS | Yes | list of strings or `{"label": str, "value": str}` dicts |
| VALUE | No | pre-selected value (defaults to first option) |

## Import
```python
from complex_dashboard.assets.components.slicer import dropdown_slicer
```

## Template
```python
# Connect to callback via the internal dcc.Dropdown id
# Default id format: set id= on the wrapping html.Div or use callback pattern below

dropdown_slicer(
    "TODO: Filter label (Polish)",
    options=m.DIMS["TODO_DIM"].values(_df),   # or hardcoded list
    value=m.DIMS["TODO_DIM"].values(_df)[0],  # default selection
    subtitle="",                               # optional helper text
)
```

## Callback pattern
```python
from dash import Input, Output, callback

@callback(
    Output("TODO-chart-id", "figure"),
    Input("TODO-slicer-id", "value"),
)
def update_chart(selected_value):
    filtered = _df[_df["dim_TODO"] == selected_value]
    return line("...", x=..., series=[...], y_measure=...)
```

## Rules
- Wrap in sidebar nav or inline above the chart section it controls
- Always set a sensible default (`value=` first option)
- Use Polish labels for options shown to users
