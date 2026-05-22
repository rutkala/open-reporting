"""line — Line chart. Encoding-based, multi-series via `color` or multi-metric `y`.

Mandatory encoding:
  x:  { dimension: <name>, granularity: <grain> }   — time or category
  y:  { metric:    <name> }                          — single metric, or
  y:  { metric:    [<name>, <name>, ...] }          — list → one trace per metric

Optional:
  color: { dimension: <name> }                       — split single metric by category
  options.years:           limit history (when x is time)
  options.markers:         show point markers
  options.reference_lines: dashed horizontal lines at given y values

Multi-metric `y` (list) and multi-series `color` are mutually exclusive
— use one or the other, not both, on the same chart.
"""
from dash import dcc, html
import plotly.graph_objects as go

import pandas as pd

from dbr.semantic import metric_label, semantic_query_data
from dbr.theme import (
    BG_SURFACE, CARD_RADIUS, CARD_SHADOW, COLORWAY,
    LINE_CHART_HEIGHT, LINE_CHART_LINE_WIDTH, LINE_CHART_MARKER_SIZE,
)
from dbr.visuals._encoding import (
    apply_reference_lines, postprocess_time_columns,
    dimension_column_name, group_by_from_channels, parse_encoding,
)

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "encoding"],
    "properties": {
        "type": {"const": "line"},
        "encoding": {
            "type": "object",
            "required": ["x", "y"],
            "additionalProperties": False,
            "properties": {
                "x":     {"type": "object"},
                "y":     {"type": "object"},
                "color": {"type": "object"},
            },
        },
        "filter":  {"type": "object"},
        "options": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "years":   {"type": "integer", "minimum": 1, "maximum": 100},
                "markers": {"type": "boolean"},
                "reference_lines": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["value"],
                        "properties": {
                            "value": {"type": "number"},
                            "label": {"type": "string"},
                            "color": {"type": "string"},
                        },
                    },
                },
                "dash_when": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["dimension", "value"],
                    "properties": {
                        "dimension":      {"type": "string"},
                        "value":          {},
                        "label_suffix":   {"type": "string"},
                    },
                },
            },
        },
    },
}

_CARD_STYLE = {
    "background": BG_SURFACE, "borderRadius": CARD_RADIUS, "boxShadow": CARD_SHADOW,
    "padding": "16px", "height": "100%", "boxSizing": "border-box",
}


def line(*, encoding: dict, filter: dict | None = None, options: dict | None = None) -> html.Div:
    enc = parse_encoding(encoding)
    opts = options or {}

    if not (enc.x and enc.x.dimension):
        raise ValueError("line: encoding.x must bind a dimension")
    metrics = enc.y.metrics if enc.y else []
    if not metrics:
        raise ValueError("line: encoding.y must bind a metric")
    if enc.color and len(metrics) > 1:
        raise ValueError(
            "line: encoding.color cannot be combined with a list-valued y.metric "
            "(both produce multiple series). Use one or the other."
        )

    dash_when = opts.get("dash_when")
    extra_group = [dash_when["dimension"]] if dash_when else []

    group_by = group_by_from_channels(enc.x, enc.color) + extra_group
    x_col = dimension_column_name(enc.x)

    df = semantic_query_data(
        metrics if len(metrics) > 1 else metrics[0],
        group_by=group_by, filter=filter, order=x_col,
        limit=opts.get("years") * (df_series_count(enc.color) if enc.color else 1) if opts.get("years") else None,
    )
    if df.empty:
        return html.Div("No data", style=_CARD_STYLE)
    df = postprocess_time_columns(df, enc)
    if dash_when:
        df = df.sort_values(x_col)

    show_markers = opts.get("markers", True)
    mode = "lines+markers" if show_markers else "lines"

    fig = go.Figure()
    if enc.color:
        color_col = dimension_column_name(enc.color)
        metric = metrics[0]
        for series, sub in df.groupby(color_col):
            fig.add_trace(go.Scatter(
                x=sub[x_col], y=sub[metric], mode=mode, name=str(series),
                line=dict(width=LINE_CHART_LINE_WIDTH),
                marker=dict(size=LINE_CHART_MARKER_SIZE),
            ))
    elif dash_when:
        _add_dashed_traces(fig, df, x_col, metrics, dash_when, mode)
    elif len(metrics) > 1:
        for m in metrics:
            fig.add_trace(go.Scatter(
                x=df[x_col], y=df[m], mode=mode, name=metric_label(m),
                line=dict(width=LINE_CHART_LINE_WIDTH),
                marker=dict(size=LINE_CHART_MARKER_SIZE),
            ))
    else:
        metric = metrics[0]
        fig.add_trace(go.Scatter(
            x=df[x_col], y=df[metric], mode=mode,
            line=dict(width=LINE_CHART_LINE_WIDTH),
            marker=dict(size=LINE_CHART_MARKER_SIZE),
        ))
    fig.update_layout(
        height=int(str(LINE_CHART_HEIGHT).rstrip("px")),
        xaxis_title="", yaxis_title="",
    )
    apply_reference_lines(fig, opts, axis="y")
    return html.Div(dcc.Graph(figure=fig, config={"displayModeBar": False}), style=_CARD_STYLE)


def df_series_count(_color_channel) -> int:
    return 4


def _add_dashed_traces(fig, df, x_col, metrics, dash_when, mode):
    """Split each metric into solid (non-matching) + dashed (matching) traces.

    Used for IMF-style history/projection charts: rows where the
    ``dash_when.dimension`` equals ``dash_when.value`` are drawn dashed,
    everything else solid. A bridge point (the last solid row) is
    prepended to the dashed series so the line appears continuous across
    the transition. Both segments share a color from the theme colorway;
    the dashed trace is hidden from the legend when there is only one
    metric, and labelled with ``label_suffix`` (default "(prognoza)")
    otherwise.
    """
    dim = dash_when["dimension"]
    target = dash_when["value"]
    suffix = dash_when.get("label_suffix", "(prognoza)")
    single_metric = len(metrics) == 1

    # Resolve target (often a Python bool/str) against the actual column dtype.
    # The mf CSV may render booleans as strings ("True"/"False"); accept both.
    target_norm = str(target).lower()

    def is_dashed(series):
        return series.astype(str).str.lower() == target_norm

    for i, m in enumerate(metrics):
        color = COLORWAY[i % len(COLORWAY)]
        label = metric_label(m)
        sub = df[[x_col, dim, m]].dropna(subset=[m])
        if sub.empty:
            continue
        dashed_mask = is_dashed(sub[dim])
        solid = sub[~dashed_mask]
        dashed = sub[dashed_mask]
        # Bridge point: prepend last solid row to dashed so the line is continuous.
        if not solid.empty and not dashed.empty:
            bridge = solid.iloc[[-1]]
            dashed = pd.concat([bridge, dashed])

        if not solid.empty:
            fig.add_trace(go.Scatter(
                x=solid[x_col], y=solid[m], mode=mode, name=label,
                line=dict(width=LINE_CHART_LINE_WIDTH, color=color),
                marker=dict(size=LINE_CHART_MARKER_SIZE),
                legendgroup=m,
            ))
        if not dashed.empty:
            # Hide the dashed trace from the legend — the dash style itself
            # signals "projected" and a second entry per metric would double
            # the legend size. The hover tooltip keeps the suffix so users
            # can confirm which segment they are reading.
            fig.add_trace(go.Scatter(
                x=dashed[x_col], y=dashed[m], mode=mode,
                name=f"{label} {suffix}",
                line=dict(width=LINE_CHART_LINE_WIDTH, color=color, dash="dash"),
                marker=dict(size=LINE_CHART_MARKER_SIZE),
                legendgroup=m,
                showlegend=False,
            ))
