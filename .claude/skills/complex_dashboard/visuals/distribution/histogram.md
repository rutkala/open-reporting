# Histogram

## When to use
Frequency distribution of a single numeric variable — how observations are spread
across value ranges. E.g. distribution of wages, age distribution, loan sizes.
**Not:** categorical counts (use Bar); comparing distributions across groups (use Box Plot).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| X AXIS | Yes | list of raw observations (not pre-binned) |
| X LABEL | Yes | axis label string — use `m.MEASURES["key"].axis_label` |
| Y MEASURE | Yes | primary measure (for tick format) |

## Import
```python
from products.visuals.components.distribution_chart import histogram
```

## Template
```python
html.Div(style=S["card"], children=[
    histogram(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: GUS — dane za 2024 r.",
        x=_df["TODO_obs_col"].tolist(),       # raw observations
        x_label=m.MEASURES["TODO_1"].axis_label,
        y_measure=m.MEASURES["TODO_1"],
    )
])
```

## Rules
- Pass raw observations — binning is handled by the component
- Minimum ~20 observations for histogram to be meaningful
- Use Box Plot instead when comparing groups
