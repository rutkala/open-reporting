# Date Range Slicer

## When to use
Start and end date picker — when users need to filter data by a date range with
calendar precision. Use for dashboards with daily/monthly granularity.
**Not:** year-only filters (use Dropdown or Tile Slicer); numeric ranges (use Range Slicer).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| TITLE | Yes | filter label |
| START DATE | Yes | default start date string "YYYY-MM-DD" |
| END DATE | Yes | default end date string "YYYY-MM-DD" |

## Import
```python
from complex_dashboard.assets.components.slicer import date_range_slicer
```

## Template
```python
date_range_slicer(
    "TODO: Filter label (Polish)",
    start_date="TODO-YYYY-MM-DD",   # e.g. "2024-01-01"
    end_date="TODO-YYYY-MM-DD",     # e.g. "2024-12-31"
    subtitle="",
)
```

## Callback pattern
```python
@callback(
    Output("TODO-chart-id", "figure"),
    Input("TODO-slicer-id", "start_date"),
    Input("TODO-slicer-id", "end_date"),
)
def update_chart(start_date, end_date):
    filtered = _df[(_df["dim_date"] >= start_date) & (_df["dim_date"] <= end_date)]
    ...
```

## Rules
- Callback receives ISO date strings — compare directly with string date columns
- Always set sensible defaults covering the most recent complete period
- Wrap in `maxWidth: 480px`
