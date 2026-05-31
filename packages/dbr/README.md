# dbr

Declarative YAML dashboard framework for Open Reporting.

Authors write YAML; the engine renders Dash apps. Theme, layout, and 18 visual types are
bundled. Connects to the MetricFlow semantic layer — no raw SQL in dashboard files.

## Visual library (18 types)

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
| `slicer` | Interactive filter (dropdown / radio / multi-select) | Slicer |

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
  download:  true         # CSV download link below chart
  data_labels: true       # show value labels on bars (bar/column)
  table:     true         # append a precision table below the chart
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

- [x] 18 visual types (card, column, bar, line, area, pie, scatter, table, waterfall, gauge, bullet, histogram, heatmap, treemap, funnel, combo, box, slicer)
- [x] Interactive slicers with declarative callback wiring
- [x] Universal title/subtitle, height, format, download options
- [x] Table: conditional formatting, totals row, data bars
- [x] Compiler (YAML → Dash app)
- [x] Theme YAML + loader (Nordic teal palette)
- [x] Layout YAML + loader (sidebar position/enabled)
- [x] MetricFlow semantic-layer binding
- [x] CLI (init / run / serve / validate / compile)
- [x] Schema validation (jsonschema)
- [ ] Choropleth / geographic map visual
- [ ] Cross-filtering (click chart → filter others)
- [ ] Drill-through pages
- [ ] Date-range picker slicer
- [ ] Export: print layout / PDF
