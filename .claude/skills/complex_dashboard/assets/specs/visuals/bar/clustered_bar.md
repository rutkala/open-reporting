# Clustered Bar (Horizontal)

## When to use
Ranking or comparing values when category names are long, or when a single series
should be sorted descending (ranking chart). Default choice for geographic/regional
comparisons with country/voivodeship names.
**Not:** time series (use Line); composition (use Stacked Bar).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| CATEGORIES | Yes | 1 dimension (region, country, sector) — displayed on Y axis |
| VALUES | Yes | 1–6 measures |
| Y MEASURE | Yes | primary measure — controls axis label + tick format |

## Import
```python
from complex_dashboard.assets.components.bar_chart import clustered_bar
```

## Template
```python
# CATEGORIES: [dimension] — displayed on Y axis (horizontal)
# VALUES:     [measure_1, …] — single series auto-sorts descending (ranking)
# Y MEASURE:  [primary measure]

html.Div(style=S["card"], children=[
    clustered_bar(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: GUS — dane za 2024 r.",
        categories=m.DIMS["TODO_DIM"].values(_df_by_TODO),
        series=[
            m.MEASURES["TODO_1"].to_series(_df["TODO_col_1"].tolist()),
        ],
        y_measure=m.MEASURES["TODO_1"],
    )
])
```

## Rules
- Single series: auto-sorted descending — largest bar at top
- Multi-series: sort by primary series descending
- Max 6 series; max ~15 categories before chart becomes unreadable
- Prefer over Clustered Column when category labels exceed ~10 characters
