# dbr

Declarative YAML dashboard framework for Open Reporting.

Authors write YAML; the engine renders Dash apps. Theme, layout, and 18 visual types are
bundled. Connects to the MetricFlow semantic layer — no raw SQL in dashboard files.

## Visual library (21 types)

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

- [x] 21 visual types — matches PowerBI/Tableau/Qlik core feature sets
- [x] Slicers: dropdown, radio, multi, **date_range**, **slider** — declarative callback wiring
- [x] **Cross-filtering**: `cross_filter: true` on any chart → click emits filter signal
- [x] **Axis control**: y_min/y_max/log_y/normalize on all chart types
- [x] **Number format templates**: format_value() with Polish locale, named presets
- [x] **Reference bands**: shaded vertical regions (GFC, COVID, policy breaks)
- [x] **Sparklines** inside KPI cards
- [x] **Trendline** on scatter, **smooth** on line, **error bars** on bar/column
- [x] **Small multiples** (trellis/facet grid), **choropleth** (EU scope + custom GeoJSON)
- [x] **Tab groups** for sub-page navigation
- [x] Universal title/subtitle, height, format, download options
- [x] Table: conditional formatting, totals row, data bars
- [x] Compiler (YAML → Dash app)
- [x] Theme YAML + loader (Nordic teal palette)
- [x] Layout YAML + loader (sidebar position/enabled)
- [x] MetricFlow semantic-layer binding
- [x] CLI (init / run / serve / validate / compile)
- [x] Schema validation (jsonschema)
- [ ] Drill-through page navigation (OR-164)
- [ ] Ribbon chart / rank chart (OR-163)
- [ ] Export: print layout / PDF
