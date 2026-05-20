"""Table — last N periods of a metric, one row per period.

Uses ``semantic_query_history`` and renders an HTML table. The metric's
unit and label come from the semantic-layer metadata; values use the
Polish-formatted ``value_str`` (NBSP thousands, comma decimal).

YAML usage:

    type:   table
    metric: fiscal_balance
    filter:
      geo: PL
    # Optional behaviour overrides:
    # rows: 5            # how many periods to show (default: TABLE_ROW_LIMIT)
"""
from dash import html

from dbr.semantic import semantic_query_history
from dbr.theme import (
    BG_SURFACE,
    BORDER,
    CARD_RADIUS,
    CARD_SHADOW,
    SUBTEXT,
    TABLE_FONT_SIZE,
    TABLE_ROW_HEIGHT,
    TABLE_ROW_LIMIT,
    TEXT,
)

DEFAULTS = {
    "rows": TABLE_ROW_LIMIT,
}

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "metric"],
    "properties": {
        "type":   {"const": "table"},
        "metric": {"type": "string"},
        "filter": {"type": "object"},
        "rows":   {"type": "integer", "minimum": 1, "maximum": 200},
    },
}

_CARD_STYLE = {
    "background":   BG_SURFACE,
    "borderRadius": CARD_RADIUS,
    "boxShadow":    CARD_SHADOW,
    "padding":      "16px",
    "height":       "100%",
    "boxSizing":    "border-box",
    "fontSize":     TABLE_FONT_SIZE,
}

_TITLE_STYLE = {
    "fontSize":     "16px",
    "fontWeight":   600,
    "color":        TEXT,
    "marginBottom": "12px",
}

_TABLE_STYLE = {
    "width": "100%",
    "borderCollapse": "collapse",
}

_TH_STYLE = {
    "textAlign":   "left",
    "padding":     "6px 8px",
    "borderBottom": f"1px solid {BORDER}",
    "color":       SUBTEXT,
    "fontWeight":  500,
}

_TD_STYLE = {
    "padding":     "6px 8px",
    "borderBottom": f"1px solid {BORDER}",
    "color":       TEXT,
    "height":      TABLE_ROW_HEIGHT,
}


def table(metric: str, *, filter: dict | None = None, **overrides) -> html.Div:
    """Render ``metric`` as an HTML table — one row per period."""
    cfg = {**DEFAULTS, **overrides}
    history = semantic_query_history(metric, filter=filter, n=cfg["rows"])

    if not history:
        return html.Div("No data", style=_CARD_STYLE)

    label = history[0].label
    unit  = history[0].unit_str or "Wartość"

    return html.Div(
        style=_CARD_STYLE,
        children=[
            html.Div(label, style=_TITLE_STYLE),
            html.Table(
                style=_TABLE_STYLE,
                children=[
                    html.Thead(html.Tr([
                        html.Th("Rok", style=_TH_STYLE),
                        html.Th(unit,  style={**_TH_STYLE, "textAlign": "right"}),
                    ])),
                    html.Tbody([
                        html.Tr([
                            html.Td(str(r.period), style=_TD_STYLE),
                            html.Td(r.value_str,   style={**_TD_STYLE, "textAlign": "right"}),
                        ])
                        for r in history
                    ]),
                ],
            ),
        ],
    )
