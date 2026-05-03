# Bubble Map

## When to use
Geographic counts or volumes at point locations — bubble size encodes a measure at
coordinates. E.g. number of enterprises by city, export volume by port.
**Not:** rates/ratios (use Choropleth Map); when precise location matters less than
regional pattern (use Choropleth Map).

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| LAT | Yes | latitude values (`dim_lat`) |
| LON | Yes | longitude values (`dim_lon`) |
| SIZE | Yes | absolute count/volume values |
| LABELS | Yes | location names shown on hover |

## Import
```python
from products.visuals.components.map_chart import bubble_map
```

## Template
```python
html.Div(style=S["card"], children=[
    bubble_map(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: GUS — dane za 2024 r.",
        lat=_df_geo["dim_lat"].tolist(),
        lon=_df_geo["dim_lon"].tolist(),
        size=_df_geo["TODO_count_col"].tolist(),
        labels=m.DIMS["label"].values(_df_geo),
    )
])
```

## Rules
- Size must be absolute values (counts, volumes) — not rates
- Bubble size is proportional — component normalises to visible range
- Use `dim_lat` / `dim_lon` columns from the geo loader
