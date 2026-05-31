"""`visuals` block — the encoding-based visualization library.

Each visual is a factory in its own file with an encoding-based signature:

    factory(*, encoding: dict, filter: dict | None = None, options: dict | None = None)

The block exposes two registries:

  VISUAL_REGISTRY  — type name → factory function (used by the compiler)
  VISUAL_SCHEMAS   — type name → JSON Schema (used by `dbr validate`)

Seventeen visuals registered, modelled on Power BI's standard library:

  card      — KPI card (value + delta + threshold badge)
  column    — vertical bar chart (category x, metric y)
  bar       — horizontal bar chart (metric x, category y)
  line      — line chart (time series or category, multi-series)
  area      — filled area (single or stacked)
  pie       — pie / donut
  scatter   — scatter / bubble
  table     — multi-row + multi-column tabular display
  waterfall — bridge / waterfall chart (cumulative changes)
  gauge     — speedometer gauge (go.Indicator)
  histogram — distribution chart (metric values across categories)
  heatmap   — matrix heatmap (two dimensions × one metric)
  treemap   — hierarchical area chart (one or two-level)
  funnel    — funnel / conversion chart
  combo     — combination line + column (dual y-axis)
  bullet    — IBCS bullet chart (metric vs target vs ranges)
  box       — box-and-whisker distribution chart
  slicer         — interactive filter control (dropdown / radio / multi-select / date_range / slider)
  choropleth     — geographic map with colour-encoded metric values
  small_multiples — trellis / facet chart grid (same chart per dimension value)
"""
from dbr.visuals.area            import area,            SCHEMA as _AREA_SCHEMA
from dbr.visuals.bar             import bar,             SCHEMA as _BAR_SCHEMA
from dbr.visuals.box             import box,             SCHEMA as _BOX_SCHEMA
from dbr.visuals.bullet          import bullet,          SCHEMA as _BULLET_SCHEMA
from dbr.visuals.card            import card,            SCHEMA as _CARD_SCHEMA
from dbr.visuals.choropleth      import choropleth,      SCHEMA as _CHOROPLETH_SCHEMA
from dbr.visuals.column          import column,          SCHEMA as _COLUMN_SCHEMA
from dbr.visuals.combo           import combo,           SCHEMA as _COMBO_SCHEMA
from dbr.visuals.funnel          import funnel,          SCHEMA as _FUNNEL_SCHEMA
from dbr.visuals.gauge           import gauge,           SCHEMA as _GAUGE_SCHEMA
from dbr.visuals.heatmap         import heatmap,         SCHEMA as _HEATMAP_SCHEMA
from dbr.visuals.histogram       import histogram,       SCHEMA as _HISTOGRAM_SCHEMA
from dbr.visuals.line            import line,            SCHEMA as _LINE_SCHEMA
from dbr.visuals.pie             import pie,             SCHEMA as _PIE_SCHEMA
from dbr.visuals.scatter         import scatter,         SCHEMA as _SCATTER_SCHEMA
from dbr.visuals.small_multiples import small_multiples, SCHEMA as _SMALL_MULTIPLES_SCHEMA
from dbr.visuals.tab_group       import tab_group,       SCHEMA as _TAB_GROUP_SCHEMA
from dbr.visuals.table           import table,           SCHEMA as _TABLE_SCHEMA
from dbr.visuals.treemap   import treemap,   SCHEMA as _TREEMAP_SCHEMA
from dbr.visuals.slicer    import slicer,    SCHEMA as _SLICER_SCHEMA
from dbr.visuals.waterfall import waterfall, SCHEMA as _WATERFALL_SCHEMA

VISUAL_REGISTRY: dict = {
    "area":            area,
    "bar":             bar,
    "box":             box,
    "bullet":          bullet,
    "card":            card,
    "choropleth":      choropleth,
    "column":          column,
    "combo":           combo,
    "funnel":          funnel,
    "gauge":           gauge,
    "heatmap":         heatmap,
    "histogram":       histogram,
    "line":            line,
    "pie":             pie,
    "scatter":         scatter,
    "slicer":          slicer,
    "small_multiples": small_multiples,
    "tab_group":       tab_group,
    "table":           table,
    "treemap":         treemap,
    "waterfall":       waterfall,
}

VISUAL_SCHEMAS: dict = {
    "area":            _AREA_SCHEMA,
    "bar":             _BAR_SCHEMA,
    "box":             _BOX_SCHEMA,
    "bullet":          _BULLET_SCHEMA,
    "card":            _CARD_SCHEMA,
    "choropleth":      _CHOROPLETH_SCHEMA,
    "column":          _COLUMN_SCHEMA,
    "combo":           _COMBO_SCHEMA,
    "funnel":          _FUNNEL_SCHEMA,
    "gauge":           _GAUGE_SCHEMA,
    "heatmap":         _HEATMAP_SCHEMA,
    "histogram":       _HISTOGRAM_SCHEMA,
    "line":            _LINE_SCHEMA,
    "pie":             _PIE_SCHEMA,
    "scatter":         _SCATTER_SCHEMA,
    "slicer":          _SLICER_SCHEMA,
    "small_multiples": _SMALL_MULTIPLES_SCHEMA,
    "tab_group":       _TAB_GROUP_SCHEMA,
    "table":           _TABLE_SCHEMA,
    "treemap":         _TREEMAP_SCHEMA,
    "waterfall":       _WATERFALL_SCHEMA,
}

__all__ = [
    "VISUAL_REGISTRY", "VISUAL_SCHEMAS",
    "area", "bar", "box", "bullet", "card", "choropleth", "column", "combo",
    "funnel", "gauge", "heatmap", "histogram", "line", "pie",
    "scatter", "slicer", "small_multiples", "table", "treemap", "waterfall",
]
