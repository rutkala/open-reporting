"""`visuals` block — the encoding-based visualization library.

Each visual is a factory in its own file with an encoding-based signature:

    factory(*, encoding: dict, filter: dict | None = None, options: dict | None = None)

The block exposes two registries:

  VISUAL_REGISTRY  — type name → factory function (used by the compiler)
  VISUAL_SCHEMAS   — type name → JSON Schema (used by `dbr validate`)

Eight visuals registered today, modelled on Power BI's standard library:

  card     — Power BI Card + KPI (consolidated via options.threshold)
  column   — vertical bars (category x, metric y)
  bar      — horizontal bars (metric x, category y)
  line     — line chart (time series or category)
  area     — filled area (single or stacked)
  pie      — pie / donut (donut = options.hole_size > 0)
  scatter  — scatter / bubble (bubble = size encoding channel)
  table    — multi-row + multi-column tabular display
"""
from dbr.visuals.area     import area,     SCHEMA as _AREA_SCHEMA
from dbr.visuals.bar      import bar,      SCHEMA as _BAR_SCHEMA
from dbr.visuals.card     import card,     SCHEMA as _CARD_SCHEMA
from dbr.visuals.column   import column,   SCHEMA as _COLUMN_SCHEMA
from dbr.visuals.line     import line,     SCHEMA as _LINE_SCHEMA
from dbr.visuals.pie      import pie,      SCHEMA as _PIE_SCHEMA
from dbr.visuals.scatter  import scatter,  SCHEMA as _SCATTER_SCHEMA
from dbr.visuals.table    import table,    SCHEMA as _TABLE_SCHEMA

VISUAL_REGISTRY: dict = {
    "card":    card,
    "column":  column,
    "bar":     bar,
    "line":    line,
    "area":    area,
    "pie":     pie,
    "scatter": scatter,
    "table":   table,
}

VISUAL_SCHEMAS: dict = {
    "card":    _CARD_SCHEMA,
    "column":  _COLUMN_SCHEMA,
    "bar":     _BAR_SCHEMA,
    "line":    _LINE_SCHEMA,
    "area":    _AREA_SCHEMA,
    "pie":     _PIE_SCHEMA,
    "scatter": _SCATTER_SCHEMA,
    "table":   _TABLE_SCHEMA,
}

__all__ = ["VISUAL_REGISTRY", "VISUAL_SCHEMAS",
           "area", "bar", "card", "column", "line", "pie", "scatter", "table"]
