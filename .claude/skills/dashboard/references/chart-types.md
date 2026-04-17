# Chart Type Decision Guide

Map what the design specification asks for to the correct component function.
Read this before building any chart — the wrong chart type is a P1 review finding.

---

## Decision table

| What you're showing | Correct chart | Component function | Avoid |
|--------------------|--------------|-------------------|-------|
| Trend over time, continuous | Line | `line()` | Bar (use only for ≤5 discrete periods) |
| Trend over time, volume matters | Area | `area()` | Line (area implies accumulation) |
| Composition over time (absolute) | Stacked area | `stacked_area()` | Pie |
| Composition over time (relative) | 100% area | `pct_stacked_area()` | |
| Comparison across categories | Vertical bar | `clustered_column()` | Pie, 3D |
| Ranking (long names) | Horizontal bar | `clustered_bar()` | Vertical bar |
| Part-to-whole (few categories) | Stacked bar | `stacked_column()` or `stacked_bar()` | Pie (>3 slices) |
| Relative shares | 100% bar | `pct_stacked_column()` | Donut |
| Contribution to change | Waterfall | `waterfall_contribution()` | Stacked bar |
| Variance vs plan / prior year | Waterfall | `waterfall_variance()` | Simple bar |
| Two measures, same scale | Combo | `line_clustered_column()` | Dual axis |
| Two measures, different scales | Subplots | `combo_subplots()` (special_chart) | Dual axis |
| Correlation (2 variables) | Scatter | `scatter_bubble()` (size=None) | Line |
| Correlation (3 variables) | Bubble | `scatter_bubble()` (with size) | |
| Distribution, single variable | Histogram | `histogram()` | Bar of counts |
| Distribution across groups | Box plot | `box_plot()` | Bar of averages |
| Geographic rate/ratio by region | Choropleth | `choropleth_map()` | Bubble map |
| Geographic count/volume by point | Bubble map | `bubble_map()` | Choropleth |
| KPI single value | KPI card | `kpi_standard()` | Gauge |
| KPI vs target | Bullet | `bullet()` | Gauge |
| KPI progress (exceptional case) | Gauge | `gauge()` | Default choice |
| Hierarchical composition | Treemap | `treemap()` | Nested pie |
| Sequential stages / funnel | Funnel | `funnel()` | Bar |
| Cross-tab / matrix | Heatmap | `heatmap_matrix()` | Table |
| Precise values alongside charts | Table | `table_basic()` | Chart |
| Ranked list | Data list | `data_list()` | Table |

---

## Hard rules

**Never use:**
- Pie chart with >3 categories — humans cannot compare angles; use `clustered_bar()`
- 3D charts — they distort perception and add no information; no component exists for this
- Dual y-axis — implies correlation that may not exist; use subplots instead
- Donut chart — same problem as pie; use bar

**Series count limits (Cowan 4±1 working memory):**
- Line chart: max 4–5 visible series. Beyond that: direct-label top series, group rest as "Pozostałe"
- Grouped bar: max 6 categories
- Stacked bar: max 6 segments
- Legend: if ≤4 series, prefer direct labels at line end

---

## Chart title rules

Chart titles state the analytical conclusion, not the chart type.

```
✓  "Zatrudnienie spada od 2023 r."
✗  "Wykres liniowy zatrudnienia"

✓  "Polska eksportuje głównie do Niemiec"
✗  "Wykres słupkowy eksportu według krajów"
```

Every chart must have a title. No untitled charts.

---

## Axis label rules

- Always include units in axis title: `Zatrudnienie (tys. osób)`, `Wartość (mld zł)`
- Polish axis labels — no English on any visible axis
- Percentage points: `Zmiana (pp)` — not `%` for differences of rates
- Never leave an axis without a label if the unit is not obvious from context

---

## Number formatting (Polish conventions)

| Type | Format | Example |
|------|--------|---------|
| Integers | space separator | `1 234 567` |
| Decimals | comma separator | `1 234,56` |
| Percentages | 1 decimal + % | `56,7%` |
| Percent point change | pp suffix | `+1,2 pp` |
| Thousands | tys. | `12,3 tys.` |
| Millions | mln | `1 234,5 mln` |
| Billions | mld | `1,2 mld` |
| Currency | zł | `123,45 zł` |

Use `Measure` objects from `products/visuals/lib/` for consistent formatting —
do not write format strings manually.
