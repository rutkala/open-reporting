"""card — Single-value card / KPI visual (Power BI's Card + KPI consolidated).

Mandatory encoding:
  value: { metric: <name> }       — the value to display

Optional:
  options.show_period:  show the period (e.g. "2024") below the value
  options.compact:      smaller inline layout (label + value on same line)
  options.threshold:    { rule: <name> }  — overlay a status badge from the metric's
                                            threshold metadata (e.g. SGP -3%)
"""
from dash import dcc, html
import plotly.graph_objects as go

from dbr.semantic import semantic_query, semantic_query_history
from dbr.theme import (
    BG_SURFACE, CARD_RADIUS, CARD_SHADOW, FONT_FAMILY,
    KPI_COMPACT_LABEL_SIZE, KPI_COMPACT_LABEL_VALUE_GAP, KPI_COMPACT_PADDING,
    KPI_COMPACT_VALUE_SIZE, KPI_COMPACT_VALUE_WEIGHT,
    KPI_LABEL_BOTTOM_GAP, KPI_LABEL_SIZE, KPI_PADDING, KPI_PERIOD_SIZE,
    KPI_PERIOD_TOP_GAP, KPI_VALUE_SIZE, KPI_VALUE_WEIGHT,
    NEGATIVE, POSITIVE, SUBTEXT, TEXT, WARNING,
)
from dbr.visuals._encoding import parse_encoding, _resolve_color
from dbr.visuals._render import format_value, _FORMAT_OPTION_SCHEMA

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
        "title":    {"type": "string"},
        "subtitle": {"type": "string"},
        "filter":  {"type": "object"},
        "options": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "show_period": {"type": "boolean"},
                "compact":     {"type": "boolean"},
                **_FORMAT_OPTION_SCHEMA,
                "threshold":   {
                    "type": "object",
                    "required": ["rule"],
                    "properties": {"rule": {"type": "string"}},
                },
                "delta": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "vs":           {"enum": ["prior_year", "target"]},
                        "target_value": {"type": "number"},
                        "format":       {"enum": ["icon-first", "textual"]},
                    },
                    "description": "Render a Δ indicator below the value. vs: prior_year computes against the previous observation; vs: target uses target_value. format: icon-first (▲/▼ + value) or textual (sentence).",
                },
                "sparkline": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "years":  {"type": "integer", "minimum": 2, "maximum": 30, "description": "Number of years to show in the spark line (default: 10)."},
                        "height": {"type": "integer", "minimum": 30, "maximum": 120, "description": "Sparkline height in px (default: 48)."},
                        "color":  {"type": "string", "description": "Line color (default: azure_1)."},
                        "filled": {"type": "boolean", "description": "Fill area under the line (default: false)."},
                    },
                    "description": "Render a tiny trend sparkline below the KPI value.",
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
        return _render_compact(r, opts)
    return _render_standard(r, opts, metric=enc.value.metric, filter=filter)


def _display_value(r, opts: dict) -> str:
    """The KPI's main value string. ``options.value_format`` overrides the
    semantic layer's built-in formatting; otherwise use ``r.formatted``."""
    fmt = opts.get("value_format")
    if fmt and r.value is not None:
        return format_value(r.value, fmt)
    return r.formatted


def _render_standard(r, opts: dict, *, metric: str, filter: dict | None) -> html.Div:
    show_period = opts.get("show_period", True)
    threshold = opts.get("threshold")
    badge = _badge(r, threshold) if threshold else None
    delta_opts = opts.get("delta")
    delta = _delta(r, metric, delta_opts, filter) if delta_opts else None

    style_card = {
        "background": BG_SURFACE, "borderRadius": CARD_RADIUS, "boxShadow": CARD_SHADOW,
        "padding": KPI_PADDING, "fontFamily": FONT_FAMILY,
        "height": "100%", "boxSizing": "border-box",
    }
    children = [
        html.Div(r.label, className="dbr-kpi-label", style={
            "fontSize": KPI_LABEL_SIZE, "color": SUBTEXT,
            "marginBottom": KPI_LABEL_BOTTOM_GAP,
        }),
        html.Div(_display_value(r, opts), className="dbr-kpi-value", style={
            "fontSize": KPI_VALUE_SIZE, "fontWeight": KPI_VALUE_WEIGHT,
            "color": TEXT, "lineHeight": "1.1",
        }),
    ]
    if delta:
        children.append(delta)
    if show_period and r.period is not None:
        children.append(html.Div(str(r.period), style={
            "fontSize": KPI_PERIOD_SIZE, "color": SUBTEXT, "marginTop": KPI_PERIOD_TOP_GAP,
        }))
    if badge:
        children.append(badge)
    sparkline_opts = opts.get("sparkline")
    if sparkline_opts is not None:
        spark = _sparkline(metric, filter, sparkline_opts)
        if spark:
            children.append(spark)
    return html.Div(children=children, className="dbr-kpi-card", style=style_card)


def _render_compact(r, opts: dict | None = None) -> html.Div:
    return html.Div(
        children=[
            html.Span(r.label, style={"fontSize": KPI_COMPACT_LABEL_SIZE, "color": SUBTEXT}),
            html.Span(_display_value(r, opts or {}), style={
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


def _delta(r, metric: str, delta_opts: dict, filter: dict | None) -> html.Div | None:
    """Render a Δ indicator below the value.

    YAML:
      delta:
        vs: prior_year     # or 'target' (requires target_value)
        target_value: -3   # only when vs: target
        format: icon-first # or 'textual'

    Color semantics derive from the metric's ``ascending_is_good`` meta:
    a movement in the "good" direction renders POSITIVE; otherwise NEGATIVE.
    Format defaults to icon-first.
    """
    if r.value is None:
        return None

    vs = delta_opts.get("vs", "prior_year")
    if vs == "prior_year":
        history = semantic_query_history(metric, filter=filter, n=2)
        if len(history) < 2 or history[1].value is None:
            return None
        prior_value  = history[1].value
        prior_label  = f"vs {history[1].period}"
    elif vs == "target":
        prior_value = delta_opts.get("target_value")
        if prior_value is None:
            return None
        prior_label = f"vs cel ({_fmt_short(prior_value)})"
    else:
        return None

    delta_value = r.value - prior_value
    ascending_good = r.meta.get("ascending_is_good", True)
    if delta_value == 0:
        color = SUBTEXT
        icon = "▬"
    else:
        improved = (delta_value > 0) if ascending_good else (delta_value < 0)
        color = POSITIVE if improved else NEGATIVE
        icon = "▲" if delta_value > 0 else "▼"

    sign = "+" if delta_value > 0 else ""
    delta_str = f"{sign}{delta_value:.1f}".replace(".", ",")
    fmt = delta_opts.get("format", "icon-first")
    if fmt == "textual":
        verb = "wzrost" if delta_value > 0 else ("spadek" if delta_value < 0 else "bez zmian")
        text = f"{verb} o {abs(delta_value):.1f}".replace(".", ",")
        return html.Div(
            [html.Span(text, style={"color": color, "fontWeight": 500}),
             html.Span(f" {prior_label}", style={"color": SUBTEXT})],
            style={"fontSize": "12px", "marginTop": "6px"},
        )
    # icon-first (default)
    return html.Div(
        [html.Span(f"{icon} {delta_str}", style={"color": color, "fontWeight": 600, "marginRight": "8px"}),
         html.Span(prior_label, style={"color": SUBTEXT})],
        style={"fontSize": "12px", "marginTop": "6px"},
    )


def _fmt_short(v: float) -> str:
    """Compact PL-decimal formatter for target labels."""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return f"{v:.1f}".replace(".", ",")


def _sparkline(metric: str, filter: dict | None, spark_opts: dict) -> html.Div | None:
    """Render a tiny trend sparkline using the metric's history."""
    from dbr.semantic import semantic_query_data
    from dbr.theme import AZURE_1, AZURE_PALE

    years  = spark_opts.get("years", 10)
    height = spark_opts.get("height", 48)
    color  = _resolve_color(spark_opts.get("color"), AZURE_1)
    filled = spark_opts.get("filled", False)

    df = semantic_query_data(
        metric, group_by=["metric_time__year"],
        filter=filter, order="metric_time__year", limit=years,
    )
    if df.empty or metric not in df.columns:
        return None

    import pandas as pd
    x_col = "metric_time__year"
    if x_col not in df.columns:
        return None
    x = pd.to_datetime(df[x_col]).dt.year.tolist()
    y = df[metric].tolist()

    trace = go.Scatter(
        x=x, y=y, mode="lines",
        line=dict(color=color, width=1.5),
        fill="tozeroy" if filled else "none",
        fillcolor=AZURE_PALE if filled else None,
        hoverinfo="skip",
    )
    fig = go.Figure(trace)
    fig.update_layout(
        height=height, margin=dict(l=0, r=0, t=4, b=4),
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return html.Div(
        dcc.Graph(figure=fig, config={"displayModeBar": False, "staticPlot": True}),
        style={"marginTop": "8px"},
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
