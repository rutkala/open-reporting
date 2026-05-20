"""KPI compact — smaller-footprint variant of `kpi_standard`.

Same data binding (one metric, one filter). Inline label-then-value layout
instead of stacked. Useful for dense KPI rows where space is tight.

YAML usage:

    type:   kpi_compact
    metric: fiscal_balance
    filter:
      geo: PL
"""
from dash import html

from or_dashboards.semantic import semantic_query
from or_dashboards.theme import (
    BG_SURFACE,
    CARD_RADIUS,
    CARD_SHADOW,
    FONT_FAMILY,
    KPI_COMPACT_LABEL_SIZE,
    KPI_COMPACT_LABEL_VALUE_GAP,
    KPI_COMPACT_PADDING,
    KPI_COMPACT_VALUE_SIZE,
    KPI_COMPACT_VALUE_WEIGHT,
    SUBTEXT,
    TEXT,
)

_CARD_STYLE = {
    "background":   BG_SURFACE,
    "borderRadius": CARD_RADIUS,
    "boxShadow":    CARD_SHADOW,
    "padding":      KPI_COMPACT_PADDING,
    "fontFamily":   FONT_FAMILY,
    "display":      "flex",
    "alignItems":   "baseline",
    "gap":          KPI_COMPACT_LABEL_VALUE_GAP,
    "height":       "100%",
    "boxSizing":    "border-box",
}

_LABEL_STYLE = {
    "fontSize": KPI_COMPACT_LABEL_SIZE,
    "color":    SUBTEXT,
}

_VALUE_STYLE = {
    "fontSize":   KPI_COMPACT_VALUE_SIZE,
    "fontWeight": KPI_COMPACT_VALUE_WEIGHT,
    "color":      TEXT,
}


def kpi_compact(metric: str, *, filter: dict | None = None, **overrides) -> html.Div:
    """Render a compact, inline KPI card bound to ``metric``."""
    r = semantic_query(metric, filter=filter)
    return html.Div(
        style=_CARD_STYLE,
        children=[
            html.Span(r.label,     style=_LABEL_STYLE),
            html.Span(r.formatted, style=_VALUE_STYLE),
        ],
    )
