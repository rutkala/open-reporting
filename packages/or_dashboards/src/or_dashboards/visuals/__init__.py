"""`visuals` block — the pre-configured visualization library.

Each visual is a factory in its own file. The block exposes
``VISUAL_REGISTRY`` — a dict mapping the YAML ``type`` string to the
factory — so the compiler can build a visual from its declarative spec
without any per-visual code in the compiler.

To register a new visual:

1. Add ``visuals/<name>.py`` with the factory function.
2. Import it below and add it to ``VISUAL_REGISTRY``.

Each factory takes ``metric`` (mandatory data binding), ``filter``
(optional dict, default ``None``), and any number of behaviour overrides
via ``**kwargs``. The factory reads its own defaults internally — the
YAML only declares opt-in overrides.
"""
from or_dashboards.visuals.kpi_compact import kpi_compact
from or_dashboards.visuals.kpi_standard import kpi_standard
from or_dashboards.visuals.line_chart import line_chart

VISUAL_REGISTRY: dict = {
    "kpi_standard": kpi_standard,
    "kpi_compact":  kpi_compact,
    "line_chart":   line_chart,
}

__all__ = ["VISUAL_REGISTRY", "kpi_standard", "kpi_compact", "line_chart"]
