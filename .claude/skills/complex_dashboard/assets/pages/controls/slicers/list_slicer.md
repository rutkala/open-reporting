# List Slicer

## When to use
Visible checklist (multi-select) or radio list (single-select) — when users need to
see all available options simultaneously and select one or many.
**Not:** many options >10 (use Dropdown); when space is very limited (use Dropdown).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| TITLE | Yes | filter label |
| OPTIONS | Yes | list of strings or `{"label": str, "value": str}` dicts |
| VALUE | No | pre-selected value(s) — list for multi, scalar for single |
| MULTI | No | `True` (checklist, default) or `False` (radio) |

## Import
```python
from products.visuals.components.slicer import list_slicer
```

## Template
```python
# Multi-select (checklist):
list_slicer(
    "TODO: Filter label (Polish)",
    options=m.DIMS["TODO_DIM"].values(_df),
    value=m.DIMS["TODO_DIM"].values(_df)[:2],  # pre-select first 2
    multi=True,
)

# Single-select (radio):
list_slicer(
    "TODO: Filter label (Polish)",
    options=m.DIMS["TODO_DIM"].values(_df),
    value=m.DIMS["TODO_DIM"].values(_df)[0],
    multi=False,
)
```

## Rules
- Multi-select: callback receives a list; handle empty selection (default to all)
- Single-select: callback receives a scalar
- Max ~10 options before list becomes too long — switch to Dropdown
- Use Polish labels for options
