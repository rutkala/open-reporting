"""card — Single-value card / KPI visual (Power BI's Card + KPI consolidated).

Mandatory encoding:
  value: { metric: <name> }       — the value to display

Optional:
  options.show_period:  show the period (e.g. "2024") below the value
  options.compact:      smaller inline layout (label + value on same line)
  options.threshold:    { rule: <name> }  — overlay a status badge from the metric's
                                            threshold metadata (e.g. SGP -3%)
"""
from dash import html

from dbr.semantic import semantic_query
from dbr.theme import (
    BG_SURFACE, CARD_RADIUS, CARD_SHADOW, FONT_FAMILY,
    KPI_COMPACT_LABEL_SIZE, KPI_COMPACT_LABEL_VALUE_GAP, KPI_COMPACT_PADDING,
    KPI_COMPACT_VALUE_SIZE, KPI_COMPACT_VALUE_WEIGHT,
    KPI_LABEL_BOTTOM_GAP, KPI_LABEL_SIZE, KPI_PADDING, KPI_PERIOD_SIZE,
    KPI_PERIOD_TOP_GAP, KPI_VALUE_SIZE, KPI_VALUE_WEIGHT,
    NEGATIVE, POSITIVE, SUBTEXT, TEXT, WARNING,
)
from dbr.visuals._encoding import parse_encoding

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "encoding"],
    "properties": {
        "type": {"const": "card"},
        "encoding": {
            "type": "object",
            "required": ["value"],
            "additionalProperties": False,
            "properties": {
                "value": {"type": "object"},
            },
        },
        "filter":  {"type": "object"},
        "options": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "show_period": {"type": "boolean"},
                "compact":     {"type": "boolean"},
                "threshold":   {
                    "type": "object",
                    "required": ["rule"],
                    "properties": {"rule": {"type": "string"}},
                },
            },
        },
    },
}


def card(*, encoding: dict, filter: dict | None = None, options: dict | None = None) -> html.Div:
    enc = parse_encoding(encoding)
    opts = options or {}

    if not (enc.value and enc.value.metric):
        raise ValueError("card: encoding.value must bind a metric")

    r = semantic_query(enc.value.metric, filter=filter)
    compact = opts.get("compact", False)

    if compact:
        return _render_compact(r)
    return _render_standard(r, opts)


def _render_standard(r, opts: dict) -> html.Div:
    show_period = opts.get("show_period", True)
    threshold = opts.get("threshold")
    badge = _badge(r, threshold) if threshold else None

    style_card = {
        "background": BG_SURFACE, "borderRadius": CARD_RADIUS, "boxShadow": CARD_SHADOW,
        "padding": KPI_PADDING, "fontFamily": FONT_FAMILY,
        "height": "100%", "boxSizing": "border-box",
    }
    children = [
        html.Div(r.label, style={
            "fontSize": KPI_LABEL_SIZE, "color": SUBTEXT,
            "marginBottom": KPI_LABEL_BOTTOM_GAP,
        }),
        html.Div(r.formatted, style={
            "fontSize": KPI_VALUE_SIZE, "fontWeight": KPI_VALUE_WEIGHT,
            "color": TEXT, "lineHeight": "1.1",
        }),
    ]
    if show_period and r.period is not None:
        children.append(html.Div(str(r.period), style={
            "fontSize": KPI_PERIOD_SIZE, "color": SUBTEXT, "marginTop": KPI_PERIOD_TOP_GAP,
        }))
    if badge:
        children.append(badge)
    return html.Div(children=children, style=style_card)


def _render_compact(r) -> html.Div:
    return html.Div(
        children=[
            html.Span(r.label, style={"fontSize": KPI_COMPACT_LABEL_SIZE, "color": SUBTEXT}),
            html.Span(r.formatted, style={
                "fontSize": KPI_COMPACT_VALUE_SIZE,
                "fontWeight": KPI_COMPACT_VALUE_WEIGHT,
                "color": TEXT,
            }),
        ],
        style={
            "background": BG_SURFACE, "borderRadius": CARD_RADIUS, "boxShadow": CARD_SHADOW,
            "padding": KPI_COMPACT_PADDING, "fontFamily": FONT_FAMILY,
            "display": "flex", "alignItems": "baseline",
            "gap": KPI_COMPACT_LABEL_VALUE_GAP,
            "height": "100%", "boxSizing": "border-box",
        },
    )


def _badge(r, threshold: dict) -> html.Div | None:
    rule = threshold["rule"]
    threshold_value = (r.meta.get("thresholds") or {}).get(rule)
    if threshold_value is None:
        return None
    ascending_good = r.meta.get("ascending_is_good", True)
    value = r.value
    if value is None:
        return None
    breached = (value < threshold_value) if ascending_good else (value > threshold_value)
    color = NEGATIVE if breached else POSITIVE
    mark = "✗" if breached else "✓"
    return html.Div(
        f"{mark} {rule.replace('_', ' ').upper()}",
        style={
            "fontSize": "11px", "color": color, "fontWeight": 600,
            "marginTop": "8px",
        },
    )
