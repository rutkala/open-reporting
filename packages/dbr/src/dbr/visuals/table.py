"""table — Tabular display with rows and columns.

Mandatory encoding:
  rows:    [ { dimension: <name> }, ... ]   — one or more dimensions (row keys)
  columns: [ { metric:    <name> }, ... ]   — one or more metrics (data columns)

Optional:
  options.row_limit:   cap row count (default from theme)
  options.labels:      { col_name: "Display Label" } — override column header text
  options.totals:      bool — append a totals row summing all metric columns
  options.conditional_format:
    list of { column, min?, max?, color, background? }
    — colour cells where the metric falls within [min, max].
    color/background accept hex or palette aliases.
    example:
      conditional_format:
        - { column: public_debt, min: 60, color: "negative" }   # ≥ 60% → orange text
        - { column: fiscal_balance, max: -3, color: "negative" } # < -3% → orange text
  options.data_bars:
    list of column names (metrics) to render with an inline bar behind the value.
    The bar width scales to the column max.
    example:  data_bars: [unemployment_rate, employment_rate]
"""
from __future__ import annotations

from dash import html
import pandas as pd

from dbr.semantic import semantic_query_data
from dbr.theme import (
    AZURE_1, AZURE_PALE, BG_SURFACE, BORDER, CARD_RADIUS, CARD_SHADOW,
    NEGATIVE, POSITIVE, SUBTEXT, TABLE_FONT_SIZE, TABLE_ROW_HEIGHT, TABLE_ROW_LIMIT, TEXT,
)
from dbr.visuals._encoding import (
    postprocess_time_columns,
    dimension_column_name, parse_encoding, _resolve_color,
)
from dbr.visuals._render import _label_for_column

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "encoding"],
    "properties": {
        "type": {"const": "table"},
        "title":    {"type": "string"},
        "subtitle": {"type": "string"},
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
                "labels": {
                    "type": "object",
                    "additionalProperties": {"type": "string"},
                },
                "totals": {"type": "boolean"},
                "conditional_format": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["column"],
                        "additionalProperties": False,
                        "properties": {
                            "column":     {"type": "string"},
                            "min":        {"type": "number"},
                            "max":        {"type": "number"},
                            "color":      {"type": "string"},
                            "background": {"type": "string"},
                        },
                    },
                },
                "data_bars": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Metric column names to render with an inline data bar.",
                },
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
_TD_BASE = {
    "padding": "6px 8px", "borderBottom": f"1px solid {BORDER}",
    "color": TEXT, "height": TABLE_ROW_HEIGHT,
}
_TD_TOTAL = {
    **_TD_BASE,
    "fontWeight": 600,
    "borderTop": f"2px solid {BORDER}",
    "borderBottom": "none",
    "color": TEXT,
}


def table(*, encoding: dict, filter: dict | None = None, options: dict | None = None) -> html.Div:
    enc  = parse_encoding(encoding)
    opts = options or {}
    limit  = opts.get("row_limit", TABLE_ROW_LIMIT)
    labels = opts.get("labels") or {}

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

    header    = group_by + metrics
    cond_fmts = opts.get("conditional_format") or []
    data_bars = set(opts.get("data_bars") or [])
    show_totals = opts.get("totals", False)

    # Pre-compute column max for data_bars scaling
    col_max: dict[str, float] = {}
    for col in data_bars:
        if col in df.columns:
            m_val = df[col].max()
            col_max[col] = m_val if pd.notna(m_val) and m_val != 0 else 1.0

    def _cell(col: str, val, is_total: bool = False) -> html.Td:
        base_style = dict(_TD_TOTAL if is_total else _TD_BASE)
        text = _fmt(val)

        # Conditional formatting
        for rule in cond_fmts:
            if rule.get("column") != col:
                continue
            if not isinstance(val, (int, float)) or pd.isna(val):
                continue
            r_min = rule.get("min")
            r_max = rule.get("max")
            match = True
            if r_min is not None and val < r_min:
                match = False
            if r_max is not None and val > r_max:
                match = False
            if match:
                if rule.get("color"):
                    base_style["color"] = _resolve_color(rule["color"], NEGATIVE)
                if rule.get("background"):
                    base_style["background"] = _resolve_color(rule["background"], AZURE_PALE)

        # Data bar — inline bar behind the value
        if col in data_bars and isinstance(val, (int, float)) and pd.notna(val):
            pct = max(0, min(100, val / col_max[col] * 100))
            bar_div = html.Div(style={
                "position": "absolute", "left": 0, "top": "25%",
                "height": "50%", "width": f"{pct:.0f}%",
                "background": AZURE_PALE, "zIndex": 0, "borderRadius": "2px",
            })
            text_span = html.Span(text, style={"position": "relative", "zIndex": 1})
            return html.Td(
                [bar_div, text_span],
                style={**base_style, "position": "relative", "overflow": "hidden"},
            )

        return html.Td(text, style=base_style)

    body_rows = [
        html.Tr([_cell(h, row[h]) for h in header])
        for _, row in df.iterrows()
    ]

    # Totals row
    if show_totals:
        total_cells = []
        for i, h in enumerate(header):
            if h in metrics:
                numeric = pd.to_numeric(df[h], errors="coerce")
                total = numeric.sum()
                total_cells.append(_cell(h, total, is_total=True))
            else:
                label = "Razem" if i == 0 else ""
                total_cells.append(html.Td(label, style=_TD_TOTAL))
        body_rows.append(html.Tr(total_cells))

    return html.Div(
        style=_CARD_STYLE,
        children=html.Table(
            style={"width": "100%", "borderCollapse": "collapse"},
            children=[
                html.Thead(html.Tr([
                    html.Th(_label_for_column(h, labels), style=_TH) for h in header
                ])),
                html.Tbody(body_rows),
            ],
        ),
    )


def _fmt(v) -> str:
    if pd.isna(v):
        return "—"
    if isinstance(v, float):
        return f"{v:.2f}".replace(".", ",")
    return str(v)
