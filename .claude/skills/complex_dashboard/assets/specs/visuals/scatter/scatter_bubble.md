# Scatter / Bubble

## When to use
Correlation between two continuous measures across observations (countries, sectors,
individuals). Bubble variant adds a third measure as bubble size.
E.g. "GDP per capita vs employment rate by country" (scatter) or
"education vs income vs population size" (bubble).
**Not:** time series (use Line); categorical comparison (use Bar).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| X AXIS | Yes | 1 numeric measure (horizontal) |
| Y AXIS | Yes | 1 numeric measure (vertical) |
| SIZE | No | 1 numeric measure as bubble size (omit for plain scatter) |
| LABELS | Yes | observation labels shown on hover / data labels |
| X MEASURE | Yes | measure object for x axis label + tick format |
| Y MEASURE | Yes | measure object for y axis label + tick format |

## Import
```python
from complex_dashboard.assets.components.scatter_chart import scatter_bubble
```

## Template
```python
# SIZE: pass None for plain scatter, list of values for bubble chart

html.Div(style=S["card"], children=[
    scatter_bubble(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: GUS / Eurostat — dane za 2024 r.",
        x=_df["TODO_x_col"].tolist(),
        y=_df["TODO_y_col"].tolist(),
        size=_df["TODO_size_col"].tolist(),   # remove for plain scatter
        labels=m.DIMS["TODO_LABEL_DIM"].values(_df),
        x_measure=m.MEASURES["TODO_X"],
        y_measure=m.MEASURES["TODO_Y"],
    )
])
```

## Rules
- Each observation = one point; avoid overplotting (max ~30 points readable)
- Bubble size: use absolute values, not rates
- Always label outliers; enable hover for all points
