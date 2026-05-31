"""Shared rendering helpers — chart + optional companion table.

Multi-row visuals (line, bar, column, area, scatter) wrap their Plotly
figure in a card-style ``html.Div``. With ``options.table`` set, the
helper appends a paired precision table beneath the chart using the same
DataFrame the chart was rendered from. This closes the gap analysis
dimension 3 ("chart for pattern, table for precision (paired)") which
fails on every page of the current public_finance dashboard.

YAML shape:

  options:
    table: true                  # default row limit (TABLE_ROW_LIMIT)
    # or
    table:
      row_limit: 12
      labels:                    # optional Polish display names per column
        date_key__cal_year: "Rok"
        public_debt: "Dług publiczny (% PKB)"

When ``table`` is absent or falsy, the returned Div is unchanged from the
prior single-chart shape — fully backwards-compatible.

Column labels resolved by ``_label_for_column`` in this order:
  1. explicit ``labels`` dict from the YAML option
  2. ``metric_label`` from the semantic layer (if column is a metric with
     a different ``label:`` set in its semantic_model YAML)
  3. heuristic cleanup of the raw column name (strip ``<prefix>__``,
     strip trailing ``_pl``, replace ``_`` with space, capitalise)
"""
from __future__ import annotations

import pandas as pd
from dash import dcc, html

from dbr.semantic import metric_label
from dbr.theme import (
    BORDER, SUBTEXT, TEXT,
    TABLE_FONT_SIZE, TABLE_ROW_HEIGHT, TABLE_ROW_LIMIT,
)


def chart_with_graph_id(
    fig,
    df: pd.DataFrame,
    options: dict | None,
    card_style: dict,
    *,
    graph_id: str | None = None,
) -> html.Div:
    """Wrap a Plotly figure in a card; assign graph_id when cross_filter is active."""
    opts = options or {}
    graph_kwargs: dict = {"figure": fig, "config": {"displayModeBar": False}}
    if graph_id:
        graph_kwargs["id"] = graph_id
    children: list = [dcc.Graph(**graph_kwargs)]
    table_opt = opts.get("table")
    if table_opt and df is not None and not df.empty:
        children.append(_render_companion_table(df, table_opt))
    if opts.get("download") and df is not None and not df.empty:
        children.append(_render_download_button(df))
    return html.Div(children, style=card_style)


def chart_with_optional_table(fig, df: pd.DataFrame, options: dict | None, card_style: dict) -> html.Div:
    """Wrap a Plotly figure in a card Div; append a companion table and/or download button when requested.

    Each multi-row visual calls this in place of building the wrapping
    ``html.Div(dcc.Graph(...))`` itself.
    """
    opts = options or {}
    children: list = [dcc.Graph(figure=fig, config={"displayModeBar": False})]
    table_opt = opts.get("table")
    if table_opt and df is not None and not df.empty:
        children.append(_render_companion_table(df, table_opt))
    if opts.get("download") and df is not None and not df.empty:
        children.append(_render_download_button(df))
    return html.Div(children, style=card_style)


def _render_download_button(df: pd.DataFrame) -> html.Div:
    """Render a small CSV download link using a data-URI.

    Uses an anchor tag with a data-URI so no Dash callback is needed —
    the browser handles the download entirely client-side. The entire
    DataFrame is encoded as CSV in the href. For large DataFrames (>500
    rows) this is still fast because it runs once at page load, not on
    user interaction.
    """
    import base64
    csv_str  = df.to_csv(index=False)
    b64      = base64.b64encode(csv_str.encode()).decode()
    data_uri = f"data:text/csv;base64,{b64}"
    return html.Div(
        html.A(
            "↓ Pobierz CSV",
            href=data_uri,
            download="data.csv",
            style={
                "fontSize": "11px", "color": SUBTEXT, "textDecoration": "none",
                "padding": "4px 0", "display": "inline-block",
                "cursor": "pointer",
            },
        ),
        style={"textAlign": "right", "marginTop": "4px"},
    )


def _render_companion_table(df: pd.DataFrame, table_opt: bool | dict) -> html.Table:
    """Render the paired precision table from the chart's DataFrame.

    The columns are the DataFrame's columns as-is — group_by dimensions
    first, metric values after. Row count is capped by ``row_limit``
    (default from theme) so very long series don't blow up the page;
    callers wanting full data should use the standalone ``table`` visual
    instead.
    """
    limit = TABLE_ROW_LIMIT
    labels: dict[str, str] = {}
    if isinstance(table_opt, dict):
        limit = table_opt.get("row_limit", TABLE_ROW_LIMIT)
        labels = table_opt.get("labels") or {}
    capped = df.head(limit)

    th_style = {
        "textAlign": "left", "padding": "6px 8px",
        "borderBottom": f"1px solid {BORDER}",
        "color": SUBTEXT, "fontWeight": 500, "fontSize": TABLE_FONT_SIZE,
    }
    td_style = {
        "padding": "6px 8px", "borderBottom": f"1px solid {BORDER}",
        "color": TEXT, "height": TABLE_ROW_HEIGHT, "fontSize": TABLE_FONT_SIZE,
    }

    return html.Table(
        style={"width": "100%", "borderCollapse": "collapse", "marginTop": "12px"},
        children=[
            html.Thead(html.Tr([
                html.Th(_label_for_column(c, labels), style=th_style)
                for c in capped.columns
            ])),
            html.Tbody([
                html.Tr([html.Td(_fmt(row[c]), style=td_style) for c in capped.columns])
                for _, row in capped.iterrows()
            ]),
        ],
    )


def _label_for_column(col: str, labels: dict[str, str] | None = None) -> str:
    """Resolve a Polish display label for a DataFrame column.

    Priority:
      1. Explicit override from ``labels`` dict (per-table YAML config)
      2. ``metric_label`` if the column is a defined metric with a label
         that differs from the raw name
      3. Heuristic cleanup of the raw column name:
         - strip ``<prefix>__`` (dim/source qualifier, e.g. ``date_key__``,
           ``cofog_function__``)
         - strip trailing ``_pl`` (language suffix from dim_geo etc.)
         - replace remaining ``_`` with space; capitalise first letter
    """
    if labels and col in labels:
        return labels[col]
    # Try metric_label — returns col unchanged if not a defined metric or
    # if its label equals the name. Use it only when it actually changes.
    via_metric = metric_label(col)
    if via_metric and via_metric != col:
        return via_metric
    cleaned = col
    if "__" in cleaned:
        cleaned = cleaned.split("__", 1)[1]
    if cleaned.endswith("_pl"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.replace("_", " ").strip()
    return cleaned[:1].upper() + cleaned[1:] if cleaned else col


def _fmt(v) -> str:
    """Same number formatting as the standalone table visual (PL decimal comma)."""
    if pd.isna(v):
        return "—"
    if isinstance(v, float):
        return f"{v:.2f}".replace(".", ",")
    return str(v)


# ── Shared title/subtitle schema fields ───────────────────────────────────────
# Import and spread into any per-visual SCHEMA's `properties` dict to enable
# per-visual title/subtitle headers (handled centrally in compiler._build_visual).
_TITLE_SCHEMA_PROPS: dict = {
    "title":    {"type": "string", "description": "Visual header shown at top of the card."},
    "subtitle": {"type": "string", "description": "Smaller caption below the title."},
}

# ── Shared axis/format schema fields ──────────────────────────────────────────
_AXIS_FORMAT_PROPS: dict = {
    "y_format": {
        "type": "string",
        "description": "Plotly tickformat string for the y-axis (e.g. '.1f', ',.0f', '.1%').",
    },
    "x_format": {
        "type": "string",
        "description": "Plotly tickformat string for the x-axis.",
    },
}

_HEIGHT_PROP: dict = {
    "height": {
        "type": "integer", "minimum": 100, "maximum": 2000,
        "description": "Chart height in pixels. Overrides the theme default.",
    },
}

# ── Axis customization schema + helper ───────────────────────────────────────
_AXIS_OPTIONS_SCHEMA: dict = {
    "y_min":     {"type": "number", "description": "Y-axis minimum value."},
    "y_max":     {"type": "number", "description": "Y-axis maximum value."},
    "x_min":     {"type": "number", "description": "X-axis minimum value."},
    "x_max":     {"type": "number", "description": "X-axis maximum value."},
    "log_y":     {"type": "boolean", "description": "Logarithmic y-axis."},
    "log_x":     {"type": "boolean", "description": "Logarithmic x-axis."},
    "y_title":   {"type": "string",  "description": "Y-axis label text."},
    "x_title":   {"type": "string",  "description": "X-axis label text."},
    "zero_line": {"type": "boolean", "description": "Show/hide the y=0 reference line (default: true)."},
    "normalize": {"type": "boolean", "description": "Normalize stacked bars/areas to 100%."},
}


def apply_axis_options(fig, opts: dict) -> None:
    """Apply axis min/max/log/title/normalize from the options dict to a Plotly figure."""
    if opts.get("y_min") is not None or opts.get("y_max") is not None:
        fig.update_yaxes(range=[opts.get("y_min"), opts.get("y_max")])
    if opts.get("x_min") is not None or opts.get("x_max") is not None:
        fig.update_xaxes(range=[opts.get("x_min"), opts.get("x_max")])
    if opts.get("log_y"):
        fig.update_yaxes(type="log")
    if opts.get("log_x"):
        fig.update_xaxes(type="log")
    if opts.get("y_title"):
        fig.update_layout(yaxis_title=opts["y_title"])
    if opts.get("x_title"):
        fig.update_layout(xaxis_title=opts["x_title"])
    if opts.get("zero_line") is False:
        fig.update_yaxes(zeroline=False)
    if opts.get("normalize"):
        fig.update_layout(barnorm="percent")


# ── Number format ─────────────────────────────────────────────────────────────
_FORMAT_OPTION_SCHEMA: dict = {
    "value_format": {
        "type": "string",
        "description": (
            "Format spec for value labels and hover tooltips. "
            "Accepts a Python format spec ('.1f', ',.0f', '.1%') or a named template: "
            "percent_1dp | percent_0dp | thousands | thousands_1dp | index_100."
        ),
    },
}

_FORMAT_TEMPLATES: dict[str, str] = {
    "percent_1dp":   ".1f",
    "percent_0dp":   ".0f",
    "thousands":     ",.0f",
    "thousands_1dp": ",.1f",
    "index_100":     ".1f",
    "currency_bln":  ",.2f",
}


def format_value(v, fmt: str | None) -> str:
    """Format a numeric value with a Python format spec (Polish decimal comma).

    Accepts a format spec string (e.g. '.1f', ',.0f') or a named template
    from _FORMAT_TEMPLATES. Falls back to 1-decimal Polish format if fmt is
    None or the value is not numeric.

    Polish convention: decimal separator = comma, thousands separator = NBSP (thin space).
    """
    try:
        f = float(v)
    except (TypeError, ValueError):
        return str(v) if v is not None else "—"
    if fmt is None:
        return f"{f:.1f}".replace(".", ",")
    spec = _FORMAT_TEMPLATES.get(fmt, fmt)
    try:
        raw = format(f, spec)
        # Swap: ',' thousands → ' ' (narrow no-break space), '.' decimal → ','
        result = raw.replace(" ", " ").replace(",", " ").replace(".", ",")
        return result
    except (ValueError, TypeError):
        return f"{f:.1f}".replace(".", ",")


_TABLE_OPTION_SCHEMA = {
    "oneOf": [
        {"type": "boolean"},
        {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "row_limit": {"type": "integer", "minimum": 1, "maximum": 1000},
                "labels": {
                    "type": "object",
                    "additionalProperties": {"type": "string"},
                    "description": "Map raw column names to Polish display labels (overrides metric_label and the heuristic). Keys are DataFrame column names (e.g. date_key__cal_year); values are display strings.",
                },
            },
        },
    ],
    "description": "Render a precision table beneath the chart using the same data. true = default row limit; {row_limit, labels} = configured.",
}
