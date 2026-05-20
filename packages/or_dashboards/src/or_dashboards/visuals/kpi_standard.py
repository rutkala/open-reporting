"""KPI standard — a single scalar value bound to a semantic metric.

Power BI parallel: a Card visual. The metric is the only mandatory binding;
everything else (visibility flags, formatting) inherits kit defaults from
``theme.yaml`` and the metric's own semantic-layer metadata (Polish label,
unit suffix, format).

YAML usage:

    type:   kpi_standard
    metric: fiscal_balance
    filter:
      geo: PL
    # optional behaviour overrides:
    # show_period: false
"""
from dash import html

from or_dashboards.semantic import semantic_query
from or_dashboards.theme import (
    BG_SURFACE,
    CARD_RADIUS,
    CARD_SHADOW,
    FONT_FAMILY,
    KPI_LABEL_BOTTOM_GAP,
    KPI_LABEL_SIZE,
    KPI_PADDING,
    KPI_PERIOD_SIZE,
    KPI_PERIOD_TOP_GAP,
    KPI_VALUE_SIZE,
    KPI_VALUE_WEIGHT,
    SUBTEXT,
    TEXT,
)

DEFAULTS = {
    "show_period": True,
}

_CARD_STYLE = {
    "background":   BG_SURFACE,
    "borderRadius": CARD_RADIUS,
    "boxShadow":    CARD_SHADOW,
    "padding":      KPI_PADDING,
    "fontFamily":   FONT_FAMILY,
    "height":       "100%",
    "boxSizing":    "border-box",
}

_LABEL_STYLE = {
    "fontSize":     KPI_LABEL_SIZE,
    "color":        SUBTEXT,
    "marginBottom": KPI_LABEL_BOTTOM_GAP,
}

_VALUE_STYLE = {
    "fontSize":   KPI_VALUE_SIZE,
    "fontWeight": KPI_VALUE_WEIGHT,
    "color":      TEXT,
    "lineHeight": "1.1",
}

_PERIOD_STYLE = {
    "fontSize":  KPI_PERIOD_SIZE,
    "color":     SUBTEXT,
    "marginTop": KPI_PERIOD_TOP_GAP,
}


def kpi_standard(metric: str, *, filter: dict | None = None, **overrides) -> html.Div:
    """Render a single-value KPI card bound to ``metric``.

    Reads label / value / unit / period from the semantic layer (the metric's
    YAML in ``platform/processing/dbt/`` defines all formatting). Only
    ``metric`` is mandatory; behaviour overrides default to ``DEFAULTS``.
    """
    cfg = {**DEFAULTS, **overrides}
    r = semantic_query(metric, filter=filter)

    children = [
        html.Div(r.label,     style=_LABEL_STYLE),
        html.Div(r.formatted, style=_VALUE_STYLE),
    ]
    if cfg["show_period"] and r.period is not None:
        children.append(html.Div(str(r.period), style=_PERIOD_STYLE))

    return html.Div(children=children, style=_CARD_STYLE)
