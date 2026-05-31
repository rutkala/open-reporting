"""gauge — Gauge / speedometer visual using go.Indicator.

Mandatory encoding:
  value: { metric: <name> }   — the needle value

Optional:
  options.min:          float — gauge minimum (default: 0)
  options.max:          float — gauge maximum (default: 100)
  options.target:       float — target marker line on the gauge arc
  options.steps:        list of {to, color} — coloured arc segments
                        e.g. [{to: 30, color: "positive"}, {to: 60, color: "warning"}, {to: 100, color: "negative"}]
  options.show_number:  bool  — show the numeric value (default: true)
  options.height:       int   — chart height override (default: 250)

Typical use: KPI against a range (utilisation, growth rate vs. target corridor,
compliance score). Prefer `card` with `delta` for simple above/below target; use
`gauge` when the position within a range communicates meaningful information.
"""
from dash import dcc, html
import plotly.graph_objects as go

from dbr.semantic import semantic_query
from dbr.theme import (
    AZURE_1, BG_SURFACE, CARD_RADIUS, CARD_SHADOW,
    NEGATIVE, POSITIVE, SLATE_2, WARNING,
)
from dbr.visuals._encoding import parse_encoding, _resolve_color

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "encoding"],
    "properties": {
        "type": {"const": "gauge"},
        "title":    {"type": "string"},
        "subtitle": {"type": "string"},
        "encoding": {
            "type": "object",
            "required": ["value"],
            "additionalProperties": False,
            "properties": {
                "value": {"type": "object"},
            },
        },
        "filter": {"type": "object"},
        "options": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "min":         {"type": "number"},
                "max":         {"type": "number"},
                "target":      {"type": "number"},
                "steps": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["to"],
                        "properties": {
                            "to":    {"type": "number"},
                            "color": {"type": "string"},
                        },
                    },
                },
                "show_number": {"type": "boolean"},
                "height":      {"type": "integer", "minimum": 100, "maximum": 800},
            },
        },
    },
}

_CARD_STYLE = {
    "background": BG_SURFACE, "borderRadius": CARD_RADIUS, "boxShadow": CARD_SHADOW,
    "padding": "16px", "height": "100%", "boxSizing": "border-box",
}


def gauge(*, encoding: dict, filter: dict | None = None, options: dict | None = None) -> html.Div:
    enc = parse_encoding(encoding)
    opts = options or {}

    if not (enc.value and enc.value.metric):
        raise ValueError("gauge: encoding.value must bind a metric")

    r = semantic_query(enc.value.metric, filter=filter)
    value = r.value if r.value is not None else 0

    g_min    = opts.get("min", 0)
    g_max    = opts.get("max", 100)
    target   = opts.get("target")
    steps    = opts.get("steps") or []
    height   = opts.get("height", 250)
    show_num = opts.get("show_number", True)

    mode = "gauge+number" if show_num else "gauge"

    # Build arc steps for go.Indicator
    bar_steps = []
    prev = g_min
    for step in steps:
        bar_steps.append(dict(
            range=[prev, step["to"]],
            color=_resolve_color(step.get("color"), SLATE_2),
        ))
        prev = step["to"]

    threshold_line = dict(color=AZURE_1, width=3, value=target) if target is not None else None

    fig = go.Figure(go.Indicator(
        mode=mode,
        value=value,
        number=dict(suffix=f" {r.unit}" if getattr(r, "unit", None) else ""),
        gauge=dict(
            axis=dict(range=[g_min, g_max]),
            bar=dict(color=AZURE_1),
            steps=bar_steps,
            threshold=dict(
                line=threshold_line,
                thickness=0.75,
                value=target,
            ) if target is not None else dict(line=None, thickness=0, value=0),
        ),
    ))
    fig.update_layout(height=height, margin=dict(l=20, r=20, t=20, b=20))
    return html.Div(dcc.Graph(figure=fig, config={"displayModeBar": False}), style=_CARD_STYLE)
