"""bullet — Bullet chart (IBCS-style: metric vs. target vs. ranges).

An IBCS-compliant alternative to the gauge. Renders a compact horizontal bar
with a target marker line and optional coloured performance ranges.

Mandatory encoding:
  value: { metric: <name> }   — the actual value

Optional:
  options.target:       float  — target / reference marker
  options.target_label: str    — label for the target line (default: "Cel")
  options.min:          float  — axis minimum (default: 0)
  options.max:          float  — axis maximum (default: auto from data + 20%)
  options.ranges:       list of {to, color} — background range bands
                        e.g. [{to: 60, color: "negative"}, {to: 80, color: "warning"}, {to: 100, color: "positive"}]
  options.bar_color:    str    — bar fill colour (default: azure_1)
  options.height:       int    — chart height (default: 120 — compact by design)
  options.show_number:  bool   — show numeric value label (default: true)

IBCS rules applied:
  - Thin horizontal bullet bar (not a semicircle like gauge)
  - Reference line (not a needle)
  - Bands from worst (left) to best (right) in ascending performance
"""
from dash import dcc, html
import plotly.graph_objects as go

from dbr.semantic import semantic_query
from dbr.theme import (
    AZURE_1, BG_SURFACE, CARD_RADIUS, CARD_SHADOW,
    NEGATIVE, POSITIVE, SLATE_3, TEXT, WARNING,
)
from dbr.visuals._encoding import parse_encoding, _resolve_color

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "encoding"],
    "properties": {
        "type": {"const": "bullet"},
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
                "target":       {"type": "number"},
                "target_label": {"type": "string"},
                "min":          {"type": "number"},
                "max":          {"type": "number"},
                "ranges": {
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
                "bar_color":   {"type": "string"},
                "height":      {"type": "integer", "minimum": 60, "maximum": 400},
                "show_number": {"type": "boolean"},
            },
        },
    },
}

_CARD_STYLE = {
    "background": BG_SURFACE, "borderRadius": CARD_RADIUS, "boxShadow": CARD_SHADOW,
    "padding": "16px", "height": "100%", "boxSizing": "border-box",
}


def bullet(*, encoding: dict, filter: dict | None = None, options: dict | None = None) -> html.Div:
    enc  = parse_encoding(encoding)
    opts = options or {}

    if not (enc.value and enc.value.metric):
        raise ValueError("bullet: encoding.value must bind a metric")

    r     = semantic_query(enc.value.metric, filter=filter)
    value = r.value if r.value is not None else 0

    g_min      = opts.get("min", 0)
    g_max      = opts.get("max", max(value * 1.2, 100) if value else 100)
    target     = opts.get("target")
    ranges     = opts.get("ranges") or []
    bar_color  = _resolve_color(opts.get("bar_color"), AZURE_1)
    height     = opts.get("height", 120)
    show_num   = opts.get("show_number", True)
    tgt_label  = opts.get("target_label", "Cel")

    mode = "number+gauge" if show_num else "gauge"
    if target is not None:
        mode = mode + "+delta"

    # Build range steps
    steps = []
    prev = g_min
    default_range_colors = [SLATE_3, "#D0D8DE", "#E8EDF0"]
    for i, rng in enumerate(ranges):
        steps.append(dict(
            range=[prev, rng["to"]],
            color=_resolve_color(rng.get("color"), default_range_colors[i % len(default_range_colors)]),
        ))
        prev = rng["to"]

    gauge_kwargs = dict(
        axis=dict(range=[g_min, g_max]),
        bar=dict(color=bar_color, thickness=0.4),
        steps=steps,
        shape="bullet",
    )
    if target is not None:
        gauge_kwargs["threshold"] = dict(
            line=dict(color=TEXT, width=3),
            thickness=0.75,
            value=target,
        )

    delta_kwargs = {}
    if target is not None and "delta" in mode:
        delta_kwargs = dict(
            delta=dict(reference=target, relative=False),
        )

    fig = go.Figure(go.Indicator(
        mode=mode,
        value=value,
        **delta_kwargs,
        gauge=gauge_kwargs,
        domain=dict(x=[0, 1], y=[0, 1]),
    ))
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=10, b=10))
    return html.Div(dcc.Graph(figure=fig, config={"displayModeBar": False}), style=_CARD_STYLE)
