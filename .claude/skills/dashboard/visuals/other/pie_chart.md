# Pie / Donut Chart

## When to use
Part-to-whole for exactly 2–3 categories where rough comparison is sufficient and
exact proportions are less important. E.g. employed vs unemployed vs inactive (3 slices).
**Not:** more than 3 categories (use Stacked Bar); when precise comparison matters (use Bar);
as a default composition chart — Bar is almost always better.

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| LABELS | Yes | category labels (2–3 only) |
| VALUES | Yes | values per category |
| DONUT | No | `True` (default) for donut, `False` for pie |

## Import
```python
from products.visuals.components.pie_chart import pie_chart
```

## Template
```python
html.Div(style={"maxWidth": "360px"}, children=[
    html.Div(style=S["card"], children=[
        pie_chart(
            "TODO: analytical conclusion as title",
            subtitle="TODO: Źródło: GUS — dane za 2024 r.",
            labels=_categories,         # max 3 labels
            values=_df["val_TODO"].tolist(),
            donut=True,
        )
    ])
])
```

## Rules
- **Hard limit: max 3 slices.** With 4+ slices, use `clustered_bar()` instead.
- Donut (`donut=True`) is the default — slightly better readability than full pie
- Wrap in `maxWidth: 360px` — pie is narrow by design
- Sort slices descending (largest first, clockwise from top)
