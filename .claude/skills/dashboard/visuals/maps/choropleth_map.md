# Choropleth Map

## When to use
Geographic rates or ratios by region — colour intensity encodes a measure across
administrative boundaries. E.g. unemployment rate by voivodeship, GDP per capita by country.
**Not:** raw counts or absolute values (area bias — use Bubble Map); point locations.

## Field bindings
| Slot | Required | Accept |
|------|----------|--------|
| LOCATIONS | Yes | ISO-3 codes (`dim_iso3`) — e.g. "POL", "DEU" |
| VALUES | Yes | rate/ratio values (one per location) |
| HOVER LABELS | Yes | display names shown on hover (`dim_label`) |

## Import
```python
from products.visuals.components.map_chart import choropleth_map
```

## Template
```python
# LOCATIONS: ISO-3 codes — use dim_iso3 column
# VALUES:    rates/ratios only — NOT raw counts (area bias)
# scope="europe" for Polish/EU regional data (default)

html.Div(style=S["card"], children=[
    choropleth_map(
        "TODO: analytical conclusion as title",
        subtitle="TODO: Źródło: Eurostat — dane za 2024 r.",
        locations=m.DIMS["iso3"].values(_df_geo),
        values=_df_geo["TODO_rate_col"].tolist(),
        hover_labels=m.DIMS["label"].values(_df_geo),
    )
])
```

## Rules
- Rates/ratios only (unemployment %, GDP per capita) — never raw counts
- Use sequential colour scale for one-direction data; diverging for +/- data
- `scope="europe"` for Polish/EU data (set in component default)
- Always label the colour scale with units
