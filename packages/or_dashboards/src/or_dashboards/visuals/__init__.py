"""`visuals` block — the pre-configured visualization library.

Each visual is a factory in its own file. The block exposes two registries:

  VISUAL_REGISTRY  — type name → factory function (used by the compiler)
  VISUAL_SCHEMAS   — type name → JSON Schema (used by `or-dashboard validate`)

To register a new visual:

1. Add ``visuals/<name>.py`` with:
   - a factory function with signature ``(metric, *, filter=None, **overrides)``
   - a ``SCHEMA`` dict describing the visual's full YAML shape
2. Import both below and add to the two registries.

Each factory takes ``metric`` (mandatory data binding), ``filter`` (optional
dict, default ``None``), and any number of behaviour overrides via
``**kwargs``. The factory reads its own defaults internally — the YAML
only declares opt-in overrides.
"""
from or_dashboards.visuals.kpi_compact  import kpi_compact,  SCHEMA as _KPI_COMPACT_SCHEMA
from or_dashboards.visuals.kpi_standard import kpi_standard, SCHEMA as _KPI_STANDARD_SCHEMA
from or_dashboards.visuals.line_chart   import line_chart,   SCHEMA as _LINE_CHART_SCHEMA

VISUAL_REGISTRY: dict = {
    "kpi_standard": kpi_standard,
    "kpi_compact":  kpi_compact,
    "line_chart":   line_chart,
}

VISUAL_SCHEMAS: dict = {
    "kpi_standard": _KPI_STANDARD_SCHEMA,
    "kpi_compact":  _KPI_COMPACT_SCHEMA,
    "line_chart":   _LINE_CHART_SCHEMA,
}

__all__ = [
    "VISUAL_REGISTRY",
    "VISUAL_SCHEMAS",
    "kpi_standard",
    "kpi_compact",
    "line_chart",
]
