"""bar — Horizontal bar chart.

Mandatory encoding:
  x:  { metric:    <name> }     — value on x-axis
  y:  { dimension: <name> }     — category on y-axis

Optional:
  color:     { dimension: <name> }  — splits into grouped or stacked bars
  options.stack:            bool    — stack (true) or group (false) when `color` is set
  options.sort:             "value-asc" | "value-desc" | "category"
  options.highlight:                — color one row distinctly (single-series only)
    value:   <category value>       — exact match against the y-dim column
    color:   <alias|hex>            — default azure_1
    other:   <alias|hex>            — default slate_2
  options.reference_lines:          — vertical dashed lines at given x values
    - { value: <number>, label: <str>, color: <alias|hex> }
"""
from dash import dcc, html
import plotly.graph_objects as go

from dbr.semantic import semantic_query_data
from dbr.theme import (
    AZURE_1, AZURE_PALE, BG_SURFACE, BAR_CHART_BARGAP, BAR_CHART_HEIGHT,
    CARD_RADIUS, CARD_SHADOW, SLATE_1, SLATE_3, SLATE_4,
)
from dbr.visuals._encoding import (
    apply_annotations, apply_reference_lines, _ANNOTATIONS_OPTION_SCHEMA, postprocess_time_columns,
    dimension_column_name, group_by_from_channels, parse_encoding,
    _resolve_color,
)
from dbr.visuals._render import (
    apply_axis_options, chart_with_optional_table,
    format_value, _AXIS_OPTIONS_SCHEMA, _FORMAT_OPTION_SCHEMA, _TABLE_OPTION_SCHEMA,
)

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "encoding"],
    "properties": {
        "type": {"const": "bar"},
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
        "title":    {"type": "string"},
        "subtitle": {"type": "string"},
        "filter":  {"type": "object"},
        "options": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "stack": {"type": "boolean"},
                "sort":  {"enum": ["value-asc", "value-desc", "category"]},
                "highlight": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["value"],
                    "properties": {
                        "value": {},
                        "color": {"type": "string"},
                        "other": {"type": "string"},
                    },
                },
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
                "data_labels": {
                    "type": "boolean",
                    "description": "Show value labels on each bar. Values formatted with 1 decimal place.",
                },
                "height": {"type": "integer", "minimum": 100, "maximum": 2000},
                "y_format": {"type": "string", "description": "Plotly tickformat for the x-axis (value axis)."},
                "download": {"type": "boolean", "description": "Render a CSV download link below the chart."},
                "error_bars": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["metric"],
                    "properties": {
                        "metric": {"type": "string"},
                        "type":   {"enum": ["data", "percent", "constant"]},
                    },
                },
                **_AXIS_OPTIONS_SCHEMA,
                **_FORMAT_OPTION_SCHEMA,
                "table": _TABLE_OPTION_SCHEMA,
                "annotations": _ANNOTATIONS_OPTION_SCHEMA,
                "dual_year": {
                    "oneOf": [
                        {"type": "boolean"},
                        {
                            "type": "object",
                            "additionalProperties": False,
                            "required": ["current", "prior"],
                            "properties": {
                                "current": {"type": "integer"},
                                "prior":   {"type": "integer"},
                            },
                        },
                    ],
                    "description": "Render side-by-side prior/current year bars per category. true = auto-detect latest 2 years; {current, prior} = explicit. Closes rubric dim 13 (dual-year grouped encoding > animated change).",
                },
            },
        },
    },
}

_CARD_STYLE = {
    "background": BG_SURFACE, "borderRadius": CARD_RADIUS, "boxShadow": CARD_SHADOW,
    "padding": "16px", "height": "100%", "boxSizing": "border-box",
}


def bar(*, encoding: dict, filter: dict | None = None, options: dict | None = None) -> html.Div:
    enc = parse_encoding(encoding)
    opts = options or {}

    if not (enc.x and enc.x.metric):
        raise ValueError("bar: encoding.x must bind a metric (use `column` for vertical bars)")
    if not (enc.y and enc.y.dimension):
        raise ValueError("bar: encoding.y must bind a dimension")

    y_col = dimension_column_name(enc.y)
    metric = enc.x.metric

    dual = opts.get("dual_year")
    if dual:
        # dual_year overrides the standard query path. We need both years of
        # data per category, so we drop any single-year filter the YAML had
        # and add date_key__cal_year to group_by.
        return _render_dual_year(
            metric=metric, y_col=y_col, enc=enc,
            filter=filter, opts=opts, dual=dual,
        )

    group_by = group_by_from_channels(enc.y, enc.color)

    df = semantic_query_data(metric, group_by=group_by, filter=filter, order=y_col)
    if df.empty:
        return html.Div("No data", style=_CARD_STYLE)
    df = postprocess_time_columns(df, enc)

    sort = opts.get("sort")
    if sort == "value-asc":
        df = df.sort_values(metric, ascending=True)
    elif sort == "value-desc":
        df = df.sort_values(metric, ascending=False)
    elif sort == "category":
        df = df.sort_values(y_col)

    data_labels = opts.get("data_labels", False)
    text_templ = "%{x:.1f}" if data_labels else None

    fig = go.Figure()
    if enc.color:
        color_col = dimension_column_name(enc.color)
        for series, sub in df.groupby(color_col):
            fig.add_trace(go.Bar(
                x=sub[metric], y=sub[y_col], orientation="h", name=str(series),
                text=[f"{v:.1f}" for v in sub[metric]] if data_labels else None,
                textposition="outside" if data_labels else None,
            ))
        fig.update_layout(barmode="stack" if opts.get("stack") else "group")
    else:
        marker_color = None
        hi = opts.get("highlight")
        if hi:
            target = hi["value"]
            color_hit = _resolve_color(hi.get("color"), AZURE_1)
            color_miss = _resolve_color(hi.get("other"), SLATE_1)
            marker_color = [color_hit if v == target else color_miss for v in df[y_col]]
        fig.add_trace(go.Bar(
            x=df[metric], y=df[y_col], orientation="h",
            marker=dict(color=marker_color) if marker_color else None,
            showlegend=False,
            text=[f"{v:.1f}" for v in df[metric]] if data_labels else None,
            textposition="outside" if data_labels else None,
        ))
    height = opts.get("height", int(str(BAR_CHART_HEIGHT).rstrip("px")))
    fig.update_layout(
        height=height,
        bargap=BAR_CHART_BARGAP, xaxis_title="", yaxis_title="",
    )
    if opts.get("y_format"):
        fig.update_layout(xaxis_tickformat=opts["y_format"])
    apply_reference_lines(fig, opts, axis="x")
    apply_annotations(fig, opts)
    return chart_with_optional_table(fig, df, opts, _CARD_STYLE)


def _render_dual_year(*, metric, y_col, enc, filter, opts, dual) -> html.Div:
    """Render a grouped bar chart with prior + current year per category.

    Prior year: muted slate-grey (azure-pale for the highlighted category).
    Current year: full accent (azure for the highlighted category).

    Side-by-side grouping puts both years adjacent per category — readable
    YoY comparison without a time slider or animation.
    """
    # Strip any single-year filter; we need both years of data
    yr_filter = (filter or {}).copy()
    yr_filter.pop("date_key__cal_year", None)

    group_by = group_by_from_channels(enc.y) + ["date_key__cal_year"]
    df = semantic_query_data(metric, group_by=group_by, filter=yr_filter, order=y_col)
    if df.empty:
        return html.Div("No data", style=_CARD_STYLE)
    df = postprocess_time_columns(df, enc)

    # Pick the two years
    if isinstance(dual, dict):
        current_year = dual["current"]
        prior_year = dual["prior"]
    else:
        years_in_data = sorted(df["date_key__cal_year"].unique())
        if len(years_in_data) < 2:
            return html.Div("Dual-year requires ≥2 years of data", style=_CARD_STYLE)
        current_year, prior_year = years_in_data[-1], years_in_data[-2]
    df = df[df["date_key__cal_year"].isin([current_year, prior_year])]

    # Sort categories by current-year value (most useful for "who's worst now")
    sort = opts.get("sort", "value-asc")
    current_df = df[df["date_key__cal_year"] == current_year]
    if sort == "value-asc":
        cat_order = current_df.sort_values(metric, ascending=True)[y_col].tolist()
    elif sort == "value-desc":
        cat_order = current_df.sort_values(metric, ascending=False)[y_col].tolist()
    else:
        cat_order = current_df.sort_values(y_col)[y_col].tolist()

    # Per-trace colour: highlight applied within each year's trace
    hi = opts.get("highlight") or {}
    target = hi.get("value")
    accent = _resolve_color(hi.get("color"), AZURE_1)
    grey   = _resolve_color(hi.get("other"), SLATE_3)
    accent_pale = AZURE_PALE
    grey_pale   = SLATE_4

    fig = go.Figure()
    # Prior year — muted shades
    prior_df = df[df["date_key__cal_year"] == prior_year].set_index(y_col).reindex(cat_order).reset_index()
    prior_colors = [
        (accent_pale if v == target else grey_pale) for v in prior_df[y_col]
    ] if target else [grey_pale] * len(prior_df)
    fig.add_trace(go.Bar(
        x=prior_df[metric], y=prior_df[y_col], orientation="h",
        marker=dict(color=prior_colors),
        name=str(prior_year),
    ))
    # Current year — full accent
    curr_df = df[df["date_key__cal_year"] == current_year].set_index(y_col).reindex(cat_order).reset_index()
    curr_colors = [
        (accent if v == target else grey) for v in curr_df[y_col]
    ] if target else [grey] * len(curr_df)
    fig.add_trace(go.Bar(
        x=curr_df[metric], y=curr_df[y_col], orientation="h",
        marker=dict(color=curr_colors),
        name=str(current_year),
    ))
    fig.update_layout(
        height=int(str(BAR_CHART_HEIGHT).rstrip("px")),
        bargap=BAR_CHART_BARGAP, xaxis_title="", yaxis_title="",
        barmode="group",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    apply_reference_lines(fig, opts, axis="x")
    apply_annotations(fig, opts)
    apply_axis_options(fig, opts)
    return chart_with_optional_table(fig, df, opts, _CARD_STYLE)
