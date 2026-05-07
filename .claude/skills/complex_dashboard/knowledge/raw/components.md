# Component Catalogue

All reusable chart and UI components available in `products/visuals/components/`.
Always use these before building anything from scratch. Read the relevant component
file only if you need to understand a parameter — don't load all of them into context.

---

## Import path

```python
from complex_dashboard.assets.components.{module} import {function}
from complex_dashboard.assets.theme import BG_PAGE, BG_SURFACE, TEXT, SUBTEXT, ...
from complex_dashboard.assets.data.db import query
```

The `theme` import also registers the `nordic` Plotly template automatically.

---

## KPI Cards — `kpi_card.py`

```python
from complex_dashboard.assets.components.kpi_card import kpi_row, kpi_standard, kpi_compact
```

| Function | Returns | Use for |
|----------|---------|---------|
| `kpi_standard(label, value, unit, trend, trend_color, subtitle)` | `html.Div` | Main KPI — large value, optional trend arrow |
| `kpi_compact(label, value, unit)` | `html.Div` | Secondary KPI — smaller, no trend |
| `kpi_row(cards, min_width, gap)` | `html.Div` | Flex row wrapping 2–5 KPI cards |

Rules:
- 3–5 cards per row maximum (Cowan 4±1)
- One trend delta per card
- `trend_color`: use `POSITIVE` (green), `NEGATIVE` (red), or `SUBTEXT` (neutral)

---

## Bar / Column Charts — `bar_chart.py`

```python
from complex_dashboard.assets.components.bar_chart import (
    clustered_column, stacked_column, pct_stacked_column,
    clustered_bar, stacked_bar, pct_stacked_bar,
    clustered_stacked_column, clustered_stacked_bar,
)
```

| Function | Orientation | Use for |
|----------|-------------|---------|
| `clustered_column(title, df, x, y_cols, ...)` | Vertical | Comparing values across categories, few groups |
| `stacked_column(title, df, x, y_cols, ...)` | Vertical | Composition by category, showing totals |
| `pct_stacked_column(title, df, x, y_cols, ...)` | Vertical | Relative composition (100% bars) |
| `clustered_bar(title, df, x_col, y_cols, ...)` | Horizontal | Rankings, long category names |
| `stacked_bar(title, df, x_col, y_cols, ...)` | Horizontal | Composition, horizontal orientation |
| `pct_stacked_bar(title, df, x_col, y_cols, ...)` | Horizontal | Relative composition, horizontal |
| `clustered_stacked_column` | Vertical | Mixed grouped + stacked (advanced) |
| `clustered_stacked_bar` | Horizontal | Mixed grouped + stacked (advanced) |

Rules:
- Max 6 categories per chart
- Sort bars descending by value unless dimension has natural order (year, quarter)
- All column variants enforce `rangemode="tozero"` — y-axis always starts at zero

---

## Line / Area Charts — `line_chart.py`

```python
from complex_dashboard.assets.components.line_chart import (
    line, area, stacked_area, pct_stacked_area,
)
```

| Function | Use for |
|----------|---------|
| `line(title, df, x, y_cols, ...)` | Time series, trends — primary choice for temporal data |
| `area(title, df, x, y_cols, ...)` | Time series where volume matters, single series |
| `stacked_area(title, df, x, y_cols, ...)` | Composition over time, absolute values |
| `pct_stacked_area(title, df, x, y_cols, ...)` | Composition over time, relative (100% area) |

Rules:
- Max 4–5 visible series — direct-label if ≤4, group the rest as "Pozostałe" beyond that
- Line width minimum 2px (enforced)
- Area fill opacity 0.25 (enforced)
- No smoothing — `line_shape="linear"` (enforced)

---

## Combo Charts — `combo_chart.py`

```python
from complex_dashboard.assets.components.combo_chart import (
    line_clustered_column, line_stacked_column, line_pct_stacked_column,
)
```

| Function | Use for |
|----------|---------|
| `line_clustered_column(title, df, x, bar_cols, line_cols, ...)` | Two measures, same scale — e.g. employment + target |
| `line_stacked_column(...)` | Composition bars + trend line overlay |
| `line_pct_stacked_column(...)` | Relative composition + trend line |

Rules:
- Same-scale data only — no dual y-axis (IBCS rule: dual axis misleads)
- If scales differ, use `combo_subplots` (stacked panels sharing x-axis)

---

## Waterfall Charts — `waterfall_chart.py`

```python
from complex_dashboard.assets.components.waterfall_chart import waterfall_contribution, waterfall_variance
```

| Function | Use for |
|----------|---------|
| `waterfall_contribution(title, df, labels, values, ...)` | Bridge chart — showing contribution of parts to total |
| `waterfall_variance(title, df, labels, values, ...)` | Variance chart — actual vs plan, year-over-year delta |

---

## Scatter / Bubble — `scatter_chart.py`

```python
from complex_dashboard.assets.components.scatter_chart import scatter_bubble
```

| Function | Use for |
|----------|---------|
| `scatter_bubble(title, df, x, y, size, color, ...)` | Correlation between two measures, optional 3rd dimension as bubble size |

---

## Distribution — `distribution_chart.py`

```python
from complex_dashboard.assets.components.distribution_chart import histogram, box_plot
```

| Function | Use for |
|----------|---------|
| `histogram(title, df, x, ...)` | Frequency distribution of a single variable |
| `box_plot(title, df, x, y, ...)` | Distribution across groups, showing median/IQR/outliers |

---

## Special Charts — `special_chart.py`

```python
from complex_dashboard.assets.components.special_chart import (
    funnel, treemap, gauge, bullet, ribbon, heatmap_matrix,
)
```

| Function | Use for |
|----------|---------|
| `funnel(title, df, stages, values, ...)` | Sequential conversion / drop-off |
| `treemap(title, df, labels, parents, values, ...)` | Hierarchical part-to-whole |
| `gauge(title, value, min, max, ...)` | Single KPI progress toward target (use sparingly) |
| `bullet(title, value, target, ...)` | KPI vs target — IBCS-preferred over gauge |
| `ribbon(title, df, ...)` | Flow between categories over time (Sankey-like) |
| `heatmap_matrix(title, df, ...)` | Correlation matrix, period × category grid |

---

## Map Charts — `map_chart.py`

```python
from complex_dashboard.assets.components.map_chart import choropleth_map, bubble_map
```

| Function | Use for |
|----------|---------|
| `choropleth_map(title, locations, values, scope, ...)` | Geographic rates/ratios by region — do NOT use for counts (area bias) |
| `bubble_map(title, df, lat, lon, size, ...)` | Geographic counts/volumes at points |

Rules:
- Choropleth: use rates/ratios only (unemployment rate, GDP per capita), not raw counts
- `scope="europe"` for Polish regional data

---

## Table Charts — `table_chart.py`

```python
from complex_dashboard.assets.components.table_chart import table_basic, table_matrix, data_list
```

| Function | Use for |
|----------|---------|
| `table_basic(title, df, ...)` | Standard data table with sorting |
| `table_matrix(title, df, ...)` | Cross-tab / pivot-style table |
| `data_list(title, items, ...)` | Simple ranked list display |

---

## Slicers (Filters) — `slicer.py`

```python
from complex_dashboard.assets.components.slicer import (
    dropdown_slicer, list_slicer, range_slicer, date_range_slicer, tile_slicer,
)
```

| Function | Use for |
|----------|---------|
| `dropdown_slicer(id, label, options, value, ...)` | Single or multi-select dropdown |
| `list_slicer(id, label, options, value, ...)` | Visible checkbox list |
| `range_slicer(id, label, min, max, ...)` | Numeric range slider |
| `date_range_slicer(id, label, ...)` | Date range picker |
| `tile_slicer(id, label, options, value, ...)` | Toggle buttons (few options, always visible) |

Slicers go in the left filter pane (220px wide). Tile slicers also allowed inline above charts.

---

## Pie Chart — `pie_chart.py`

```python
from complex_dashboard.assets.components.pie_chart import pie_chart
```

Avoid. Use `clustered_bar` or `stacked_column` instead. Pie charts are only acceptable
for ≤3 categories where exact proportions matter less than rough comparison.

---

## Financial Chart — `financial_chart.py`

```python
from complex_dashboard.assets.components.financial_chart import candlestick
```

Use only for time-series OHLC financial data (stock prices, bond yields with open/high/low/close).
