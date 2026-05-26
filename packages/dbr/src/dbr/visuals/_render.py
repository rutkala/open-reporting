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


def chart_with_optional_table(fig, df: pd.DataFrame, options: dict | None, card_style: dict) -> html.Div:
    """Wrap a Plotly figure in a card Div; append a companion table when requested.

    Each multi-row visual calls this in place of building the wrapping
    ``html.Div(dcc.Graph(...))`` itself.
    """
    children: list = [dcc.Graph(figure=fig, config={"displayModeBar": False})]
    table_opt = (options or {}).get("table")
    if table_opt and df is not None and not df.empty:
        children.append(_render_companion_table(df, table_opt))
    return html.Div(children, style=card_style)


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
