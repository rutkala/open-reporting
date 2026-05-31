# dbr

Declarative YAML dashboard framework for Open Reporting.

Authors write YAML; the engine renders Dash apps. Theme, layout, and 18 visual types are
bundled. Connects to the MetricFlow semantic layer — no raw SQL in dashboard files.

## Visual library (22 types)

| Type | Description | PowerBI equivalent |
|------|-------------|-------------------|
| `card` | KPI card with value, delta, threshold badge | Card / KPI |
| `column` | Vertical bar chart (grouped/stacked) | Clustered/Stacked Column |
| `bar` | Horizontal bar chart (grouped/stacked, dual-year) | Bar chart |
| `line` | Line chart (multi-series, projections, endpoint labels) | Line chart |
| `area` | Filled area (single or stacked) | Area chart |
| `pie` | Pie / donut | Pie / Donut |
| `scatter` | Scatter / bubble | Scatter |
| `table` | Table with conditional formatting, totals, data bars | Table / Matrix |
| `waterfall` | Bridge / waterfall chart (budget decomposition) | Waterfall |
| `gauge` | Speedometer gauge (go.Indicator) | Gauge |
| `bullet` | IBCS bullet chart (metric vs target vs ranges) | — |
| `histogram` | Distribution of metric values across categories | — |
| `heatmap` | Matrix heatmap (two dimensions × one metric) | Matrix |
| `treemap` | Hierarchical area chart (one or two-level) | Treemap |
| `funnel` | Funnel / conversion chart | Funnel |
| `combo` | Combination line + column (dual y-axis) | Line and stacked column |
| `box` | Box-and-whisker distribution | — |
| `slicer` | Interactive filter (dropdown / radio / multi / date_range / slider) | Slicer |
| `choropleth` | Geographic map — EU country or custom GeoJSON regions | Map |
| `small_multiples` | Trellis / facet grid (same chart per dimension value) | Small multiples |
| `tab_group` | Sub-page tab navigation within a section | Tabs |
| `ribbon` | Bump / rank chart — rank positions change over time | Ribbon chart |

## Universal visual options

All visual types accept:

```yaml
title:    "Chart title"          # rendered inside the card header
subtitle: "Supporting caption"  # smaller text below the title
```

Chart visuals also accept:

```yaml
options:
  height:    400          # px, overrides theme default
  y_format:  ".1%"        # Plotly tickformat for y-axis
  x_format:  ""           # Plotly tickformat for x-axis
  y_min:     0            # y-axis minimum
  y_max:     100          # y-axis maximum
  log_y:     true         # logarithmic y-axis
  y_title:   "% PKB"      # y-axis label text
  normalize: true         # 100% normalized stacked bars/area
  value_format: "percent_1dp"  # data label format (named template or spec)
  download:  true         # CSV download link below chart
  data_labels: true       # show value labels on bars (bar/column)
  error_bars:             # error bars (bar/column only)
    metric: error_metric
  trendline: true         # OLS trendline (scatter)
  smooth:    true         # spline smoothing (line)
  reference_bands:        # shaded vertical regions (line/area)
    - { from: 2008, to: 2009, color: "negative", label: "GFC" }
  table:     true         # append a precision table below the chart
```

**Card visual extras:**
```yaml
options:
  sparkline:             # mini trend line inside KPI card
    years:  10
    height: 48
    filled: false
```

## Interactive slicers

Wire a `slicer` visual to any chart on the same page via `filter_from`:

```yaml
# slicer.yml
type: slicer
slicer_id: country_filter
encoding:
  value:
    dimension: geo
options:
  metric: fiscal_balance
  kind: dropdown
  label: "Kraj"
  default: PL

# trend_chart.yml — filtered by the slicer above
type: line
filter_from:
  country_filter: geo       # slicer_id → filter dimension key
encoding:
  x: { dimension: metric_time, granularity: year }
  y: { metric: fiscal_balance }
```

No Python callback code is needed — the compiler wires everything declaratively.

## Drill-through navigation

Click a data point to scroll to a detail page with pre-applied filter:

```yaml
# overview_bar.yml — source visual
type: bar
drill_through:
  target_page: kraj_detail     # page anchor to scroll to
  pass_filter:
    geo: geo                   # filter key → dimension column from clickData

# detail_trend.yml — destination visual (on the kraj_detail page section)
type: line
filter_from:
  __dt_przeglad_overview_bar: geo   # auto-assigned slicer_id
encoding:
  x: { dimension: metric_time, granularity: year }
  y: { metric: unemployment_rate }
```

## Cross-filtering

Click a chart element to filter all linked visuals on the same page:

```yaml
# source: emits filter signal when clicked
type: bar
cross_filter: true
cross_filter_dimension: geo

# receiver: updates when source is clicked
type: line
filter_from:
  __cf_przeglad_country_bar: geo
```

## Project shape

```
<domain>/
├── app.py               ← run_dashboard(__file__)
├── dashboard.yml        ← domain, port, title
└── pages/
    ├── pages.yml        ← page order
    └── <page>/
        ├── page.yml     ← title + anchor
        └── visuals/
            ├── visuals.yml          ← row layout
            └── <visual>.yml        ← type + encoding + filter + options
```

## Override layering

1. Tool defaults (shipped in this package)
2. Project-root `theme.yaml` / `layout.yaml` (optional overrides)
3. Per-visual `options:` in YAML

## CLI

```bash
dbr init <name>       # scaffold a new dashboard project
dbr run <path>        # deploy via systemd + nginx
dbr serve <path>      # run Dash server in foreground
dbr validate <path>   # schema-check all YAMLs
dbr compile <path>    # print resolved layout tree (debug)
```

## Status

- [x] **22 visual types** — full feature parity with PowerBI / Tableau / Qlik core library
- [x] **Slicers**: dropdown, radio, multi, date_range, slider — declarative Dash callback wiring
- [x] **Cross-filtering**: `cross_filter: true` on any chart → click emits filter signal to linked visuals
- [x] **Drill-through**: `drill_through: {target_page, pass_filter}` → click navigates + pre-filters destination
- [x] **Axis control**: y_min/y_max/x_min/x_max, log_y/log_x, y_title, normalize (100% stacked)
- [x] **Number format templates**: format_value() with Polish locale; named presets (percent_1dp, thousands…)
- [x] **Reference bands**: shaded vertical regions on line/area (recession periods, structural breaks)
- [x] **Sparklines** inside KPI cards — embedded mini trend line
- [x] **Trendline** (OLS) on scatter, **smooth** (spline) on line, **error bars** on bar/column
- [x] **Ribbon/bump chart**: rank positions change over time with crossing lines
- [x] **Small multiples**: trellis/facet grid — same chart repeated per dimension value
- [x] **Choropleth**: EU country map (Plotly built-in) + custom GeoJSON for regional maps
- [x] **Tab groups**: sub-page tab navigation (dcc.Tabs) without page change
- [x] Universal title/subtitle, height, download (CSV), data_labels options on all visuals
- [x] Table: conditional_format, totals row, data bars per column
- [x] Compiler (YAML → Dash app), Theme YAML, Layout YAML, MetricFlow binding
- [x] CLI (init / run / serve / validate / compile), JSON Schema validation
- [ ] Export: print layout / PDF (browser print media CSS workaround available)
