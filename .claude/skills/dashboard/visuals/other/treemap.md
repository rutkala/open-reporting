# Treemap

## When to use
Hierarchical part-to-whole — rectangle size encodes value within a nested structure.
E.g. GDP composition by sector → sub-sector; budget by ministry → department.
**Not:** flat (non-hierarchical) composition (use Stacked Bar); time trends (use Line).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| LABELS | Yes | unique node names (all levels) |
| PARENTS | Yes | parent node name per node ("" for root) |
| VALUES | Yes | node values (leaf values; parent = sum of children) |

## Import
```python
from products.visuals.components.special_chart import treemap
```

## Data structure
```python
# Each node needs a unique label and a parent label.
# Root node has parent = "".
# Parent values must equal sum of their children (branchvalues="total").

_df_tree = pd.DataFrame({
    "dim_node":   ["Total", "Group A", "Group B", "A1",    "A2",    "B1",    "B2"],
    "dim_parent": ["",       "Total",   "Total",   "Group A","Group A","Group B","Group B"],
    "val_size":   [1000.0,   400.0,     600.0,     250.0,   150.0,   350.0,   250.0],
})
```

## Template
```python
html.Div(style=S["card"], children=[
    treemap(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: GUS — dane za 2024 r.",
        labels=_df_tree["dim_node"].tolist(),
        parents=_df_tree["dim_parent"].tolist(),
        values=_df_tree["val_size"].tolist(),
    )
])
```

## Rules
- Parent values must equal sum of children — enforced by `branchvalues="total"`
- Max 2–3 hierarchy levels before readability drops
- Root node always has `dim_parent = ""`
