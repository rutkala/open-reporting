# Component Catalogue

All reusable chart and UI components live in `products/visuals/components/`.
Always use these before building anything custom. Read the component file
itself only when you need to understand an edge-case parameter.

**Key pattern:** chart functions take `x=list`, `series=[Measure.to_series(...)]`,
`y_measure=Measure` — not DataFrames. Pre-aggregate first, then pass lists.

---

## Import paths

```python
from products.visuals.components.kpi_card        import kpi_row, kpi_standard, kpi_compact
from products.visuals.components.bar_chart        import (
    clustered_column, stacked_column, pct_stacked_column,
    clustered_bar, stacked_bar, pct_stacked_bar,
    clustered_stacked_column, clustered_stacked_bar,
)
from products.visuals.components.line_chart       import line, area, stacked_area, pct_stacked_area
from products.visuals.components.combo_chart      import (
    line_clustered_column, line_stacked_column, line_pct_stacked_column,
)
from products.visuals.components.waterfall_chart  import waterfall_contribution, waterfall_variance
from products.visuals.components.scatter_chart    import scatter_bubble
from products.visuals.components.distribution_chart import histogram, box_plot
from products.visuals.components.special_chart    import (
    funnel, treemap, gauge, bullet, ribbon, heatmap_matrix,
)
from products.visuals.components.map_chart        import choropleth_map, bubble_map
from products.visuals.components.financial_chart  import candlestick
from products.visuals.components.table_chart      import table_basic, table_matrix, data_list
from products.visuals.components.pie_chart        import pie_chart
from products.visuals.components.slicer           import (
    dropdown_slicer, list_slicer, range_slicer, date_range_slicer, tile_slicer,
)
import products.visuals.lib.theme as _theme  # registers 'teal' Plotly template
from products.visuals.lib.theme import BG_PAGE, BG_SURFACE, BORDER, TEXT, SUBTEXT, ...
from products.visuals.lib.db import query
```

---

## KPI Cards — `kpi_card.py`

```python
kpi_row(cards: list, min_width: str = "160px", gap: str = "16px") → html.Div
```
Flex row wrapping 2–5 KPI cards. `min_width` sets the card minimum width.

```python
kpi_standard(
    label: str,
    value: str,               # use Measure.kpi_value(v)
    unit: str = "",           # use Measure.plotly_ticksuffix
    subtitle: str = None,
    reference_value: str = None,  # use Measure.kpi_value(v)
    reference_label: str = None,
    trend: str = None,        # e.g. "▲ +0.8" or "▼ -1.2"
    trend_color: str = None,  # POSITIVE, NEGATIVE, or SUBTEXT
) → html.Div
```

```python
kpi_compact(
    label: str,
    value: str,
    unit: str = "",
    trend: str = None,
    trend_color: str = None,
) → html.Div
```

**Rules:**
- 3–5 cards per `kpi_row` (Cowan 4±1)
- Use `kpi_standard` for primary KPIs; `kpi_compact` for secondary / dense rows
- `trend_color`: `POSITIVE` (green up), `NEGATIVE` (red down), `SUBTEXT` (neutral)

**Example:**
```python
kpi_row([
    kpi_standard(
        label=m.MEASURES["rate"].label,
        value=m.MEASURES["rate"].kpi_value(_scalars["rate"]),
        unit=m.MEASURES["rate"].plotly_ticksuffix,
        reference_value=m.MEASURES["rate"].kpi_value(5.0),
        reference_label="Cel",
        trend="▼ -0.3", trend_color=POSITIVE,
    ),
    kpi_compact(
        label=m.MEASURES["employment"].label,
        value=m.MEASURES["employment"].kpi_value(_scalars["employment"]),
        unit=m.MEASURES["employment"].plotly_ticksuffix,
    ),
])
```

---

## Bar / Column Charts — `bar_chart.py`

All bar/column functions share the `series=` interface:
`series = [measure.to_series(df["col"].tolist()), ...]`

```python
clustered_column(
    title: str, subtitle: str = None,
    x: list,                             # category axis values
    series: list[dict],                  # [{"name": str, "y": list}, ...]
    y_measure: Measure,                  # controls axis label, tick format
    show_labels: bool = False,
) → dcc.Graph
```

```python
stacked_column(title, subtitle=None, x, series, y_measure, show_labels=False) → dcc.Graph
pct_stacked_column(title, subtitle=None, x, series, y_measure) → dcc.Graph
```

```python
clustered_bar(
    title: str, subtitle: str = None,
    categories: list,                    # note: param name is 'categories', not 'x'
    series: list[dict],
    y_measure: Measure,
    show_labels: bool = False,
) → dcc.Graph
```
Single series: auto-sorted descending (ranking chart).

```python
stacked_bar(title, subtitle=None, categories, series, y_measure, show_labels=False) → dcc.Graph
pct_stacked_bar(title, subtitle=None, categories, series) → dcc.Graph
```

```python
# Mixed grouped + stacked — advanced use only
clustered_stacked_column(
    title: str, subtitle: str = None,
    x: list,                             # category axis
    groups: list[dict],                  # [{"name": str, "series": [{"name": str, "y": list}, ...]}, ...]
    y_measure: Measure,
) → dcc.Graph

clustered_stacked_bar(title, subtitle=None, categories, groups, y_measure) → dcc.Graph
```

**Rules:**
- Max 6 categories / segments
- Column variants always start y-axis at zero (`rangemode="tozero"`)
- Sort bars descending unless dimension has natural order (year, quarter)

---

## Line / Area Charts — `line_chart.py`

```python
line(
    title: str, subtitle: str = None,
    x: list,
    series: list[dict],                  # [{"name": str, "y": list}, ...]
    y_measure: Measure,
    reference: dict = None,              # {"value": float, "label": str}
) → dcc.Graph
```

```python
area(title, subtitle=None, x, series, y_measure) → dcc.Graph
stacked_area(title, subtitle=None, x, series, y_measure) → dcc.Graph
pct_stacked_area(title, subtitle=None, x, series) → dcc.Graph
```

**Rules:**
- Max 4–5 visible series (direct-label if ≤4, group rest as "Pozostałe")
- Line width minimum 2px (enforced by component)
- Area fill opacity 0.25 (enforced)
- No smoothing — `line_shape="linear"` (enforced)

---

## Combo Charts — `combo_chart.py`

```python
line_clustered_column(
    title: str, subtitle: str = None,
    x: list,
    bar_series: list[dict],              # {"name": str, "y": list}
    line_series: list[dict],
    y_measure: Measure,
) → dcc.Graph

line_stacked_column(title, subtitle=None, x, bar_series, line_series, y_measure) → dcc.Graph
line_pct_stacked_column(title, subtitle=None, x, bar_series, line_series, y_measure) → dcc.Graph
```

**Rule:** Same-scale data only. No dual y-axis. If scales differ, use stacked subplots.

---

## Waterfall Charts — `waterfall_chart.py`

```python
waterfall_contribution(
    title: str, subtitle: str = None,
    categories: list,                    # stage/component labels
    values: list[float],                 # positive = adds, negative = subtracts
    total_label: str,                    # label of the final total bar
    y_measure: Measure,
) → dcc.Graph

waterfall_variance(
    title: str, subtitle: str = None,
    categories: list,
    values: list[float],
    y_measure: Measure,
) → dcc.Graph
```

Data must include `is_total` and `is_base` flags in the source DataFrame
(used to colour the bars correctly). See `data.py:load_waterfall()` for the
column structure.

---

## Scatter / Bubble — `scatter_chart.py`

```python
scatter_bubble(
    title: str, subtitle: str = None,
    x: list[float],
    y: list[float],
    size: list[float],                   # bubble size; pass None for plain scatter
    labels: list[str],                   # hover / data labels
    x_measure: Measure,
    y_measure: Measure,
) → dcc.Graph
```

---

## Distribution — `distribution_chart.py`

```python
histogram(
    title: str, subtitle: str = None,
    x: list[float],                      # raw observations (not pre-binned)
    x_label: str,                        # axis label string (use Measure.axis_label)
    y_measure: Measure,
) → dcc.Graph

box_plot(
    title: str, subtitle: str = None,
    data: dict[str, list[float]],        # {"Group A": [1.2, 3.4, ...], "Group B": [...]}
    y_measure: Measure,
) → dcc.Graph
```

---

## Special Charts — `special_chart.py`

```python
funnel(
    title: str, subtitle: str = None,
    stages: list[str],
    values: list[float],
) → dcc.Graph

treemap(
    title: str, subtitle: str = None,
    labels: list[str],                   # unique node names
    parents: list[str],                  # parent node name ("" for root)
    values: list[float],
) → dcc.Graph

gauge(
    title: str, subtitle: str = None,
    value: float,
    min_val: float, max_val: float,
    reference: float,                    # target / threshold
    y_measure: Measure,
) → dcc.Graph

bullet(
    title: str, subtitle: str = None,
    value: float,
    target: float,
    max_val: float,
    y_measure: Measure,
) → dcc.Graph

ribbon(
    title: str, subtitle: str = None,
    x: list,                             # time periods (sorted)
    series: list[dict],                  # [{"name": str, "ranks": list[int]}, ...]
) → dcc.Graph

heatmap_matrix(
    title: str, subtitle: str = None,
    x_labels: list[str],
    y_labels: list[str],
    z_values: list[list[float]],         # outer = rows, inner = cols
    color_scale: str = "diverging",      # "diverging" | "sequential"
) → dcc.Graph
```

---

## Map Charts — `map_chart.py`

```python
choropleth_map(
    title: str, subtitle: str = None,
    locations: list[str],                # ISO-3 codes (dim_iso3)
    values: list[float],
    hover_labels: list[str],             # display names shown on hover
) → dcc.Graph

bubble_map(
    title: str, subtitle: str = None,
    lat: list[float],
    lon: list[float],
    size: list[float],
    labels: list[str],
) → dcc.Graph
```

**Rules:**
- Choropleth: rates/ratios only (unemployment %, GDP per capita) — not raw counts
- `scope="europe"` for Polish regional data (default)

---

## Financial Chart — `financial_chart.py`

```python
candlestick(
    title: str, subtitle: str = None,
    dates: list[str],                    # "YYYY-MM" or "YYYY-MM-DD"
    open_: list[float],
    high: list[float],
    low: list[float],
    close: list[float],
    y_measure: Measure,
) → dcc.Graph
```

---

## Table Charts — `table_chart.py`

```python
table_basic(
    title: str, subtitle: str = None,
    headers: list[str],
    rows: list[list],                    # one list per row
    number_cols: set[int],               # column indices (0-based) to right-align
) → html.Div

table_matrix(
    title: str, subtitle: str = None,
    row_labels: list[str],
    col_labels: list[str],
    values: list[list[float]],           # values[row][col]
    row_dim: str,                        # label for the row dimension column
) → html.Div

data_list(
    title: str, subtitle: str = None,
    items: list[dict],                   # [{"label": str, "value": str}, ...]
) → html.Div
```

---

## Pie Chart — `pie_chart.py`

```python
pie_chart(
    title: str, subtitle: str = None,
    labels: list[str],
    values: list[float],
    donut: bool = True,
) → dcc.Graph
```

**Avoid.** Use `clustered_bar` or `stacked_column` instead.
Acceptable only for ≤3 categories where rough comparison is enough.

---

## Slicers (Filters) — `slicer.py`

```python
dropdown_slicer(label: str, options: list, value, multi: bool = False) → html.Div
list_slicer(label: str, options: list, value, multi: bool = True) → html.Div
range_slicer(label: str, min_val: float, max_val: float, value: list) → html.Div
date_range_slicer(label: str, start_date: str, end_date: str) → html.Div
tile_slicer(label: str, options: list, value) → html.Div
```

All slicers return a `html.Div` wrapper containing a labelled Dash Core Component.
Wire them to chart callbacks via their internal IDs. Slicers go in the sidebar nav
or inline above charts (tile_slicer only for ≤6 options).
