"""table — Tabular display with rows and columns.

Mandatory encoding:
  rows:    [ { dimension: <name> }, ... ]   — one or more dimensions (row keys)
  columns: [ { metric:    <name> }, ... ]   — one or more metrics (data columns)

Optional:
  options.row_limit:  cap row count (default from theme)
"""
from dash import html
import pandas as pd

from dbr.semantic import semantic_query_data
from dbr.theme import (
    BG_SURFACE, BORDER, CARD_RADIUS, CARD_SHADOW,
    SUBTEXT, TABLE_FONT_SIZE, TABLE_ROW_HEIGHT, TABLE_ROW_LIMIT, TEXT,
)
from dbr.visuals._encoding import (
    postprocess_time_columns,
    dimension_column_name, parse_encoding,
)

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "encoding"],
    "properties": {
        "type": {"const": "table"},
        "encoding": {
            "type": "object",
            "required": ["rows", "columns"],
            "additionalProperties": False,
            "properties": {
                "rows":    {"type": "array", "minItems": 1, "items": {"type": "object"}},
                "columns": {"type": "array", "minItems": 1, "items": {"type": "object"}},
            },
        },
        "filter":  {"type": "object"},
        "options": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "row_limit": {"type": "integer", "minimum": 1, "maximum": 1000},
            },
        },
    },
}

_CARD_STYLE = {
    "background": BG_SURFACE, "borderRadius": CARD_RADIUS, "boxShadow": CARD_SHADOW,
    "padding": "16px", "height": "100%", "boxSizing": "border-box",
    "fontSize": TABLE_FONT_SIZE,
}
_TH = {
    "textAlign": "left", "padding": "6px 8px",
    "borderBottom": f"1px solid {BORDER}",
    "color": SUBTEXT, "fontWeight": 500,
}
_TD = {
    "padding": "6px 8px", "borderBottom": f"1px solid {BORDER}",
    "color": TEXT, "height": TABLE_ROW_HEIGHT,
}


def table(*, encoding: dict, filter: dict | None = None, options: dict | None = None) -> html.Div:
    enc = parse_encoding(encoding)
    opts = options or {}
    limit = opts.get("row_limit", TABLE_ROW_LIMIT)

    if not enc.rows or not all(c.dimension for c in enc.rows):
        raise ValueError("table: encoding.rows must be a list of dimensions")
    if not enc.columns or not all(c.metric for c in enc.columns):
        raise ValueError("table: encoding.columns must be a list of metrics")

    group_by = [dimension_column_name(c) for c in enc.rows]
    metrics  = [c.metric for c in enc.columns]

    df = None
    for m in metrics:
        sub = semantic_query_data(m, group_by=group_by, filter=filter, order=group_by[0])
        if sub.empty:
            continue
        df = sub if df is None else df.merge(sub, on=group_by, how="outer")
    if df is None or df.empty:
        return html.Div("No data", style=_CARD_STYLE)
    df = postprocess_time_columns(df, enc)

    df = df.head(limit)
    header = group_by + metrics
    return html.Div(
        style=_CARD_STYLE,
        children=html.Table(
            style={"width": "100%", "borderCollapse": "collapse"},
            children=[
                html.Thead(html.Tr([html.Th(h, style=_TH) for h in header])),
                html.Tbody([
                    html.Tr([html.Td(_fmt(row[h]), style=_TD) for h in header])
                    for _, row in df.iterrows()
                ]),
            ],
        ),
    )


def _fmt(v) -> str:
    if pd.isna(v):
        return "—"
    if isinstance(v, float):
        return f"{v:.2f}".replace(".", ",")
    return str(v)
