# Tile Slicer

## When to use
Clickable button tiles for single-select — when options are few (≤6), always visible,
and toggling between them is the primary interaction. Best for year/period selectors
placed inline above charts.
**Not:** many options (use Dropdown); multi-select (use List Slicer).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| TITLE | Yes | filter label |
| OPTIONS | Yes | list of strings (max 6) |
| VALUE | No | pre-selected value (defaults to first) |

## Import
```python
from products.visuals.components.slicer import tile_slicer
```

## Template
```python
tile_slicer(
    "TODO: Filter label (Polish)",
    options=m.DIMS["TODO_DIM"].values(_df),   # max 6 options
    value=m.DIMS["TODO_DIM"].values(_df)[0],  # default selection
    subtitle="",
)
```

## Rules
- Hard limit: max 6 tiles — more options → use Dropdown
- Use for period/year selectors placed inline above a chart
- Active tile highlighted in `TEAL_1` (enforced by component)
- Returns a single scalar value to callback
