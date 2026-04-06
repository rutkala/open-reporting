"""
Table chart variants using Plotly go.Table.
KB reference: team/analytics/visualization/charts/table.md

Rules applied:
- Numbers right-aligned, text left-aligned (KB)
- Header: bold, distinct background
- table_heatmap: colour encoding + values always shown (KB: never hide values behind colour)
- go.Table used (not DataTable) — consistent with component pattern, works inside card wrapper
"""
import plotly.graph_objects as go

from products.visuals.lib.theme import (
    AZURE_1, AZURE_PALE, BORDER, BG_SURFACE, GRID,
    POSITIVE, NEGATIVE, SLATE_4,
    SUBTEXT, TEXT,
)
from products.visuals.components import PLOT_H, MARGIN_L, MARGIN_R, MARGIN_T, MARGIN_B, _chart
from products.visuals.lib.theme import FONT_FAMILY


def _table_height(rows: int) -> int:
    """Estimate table height from number of rows."""
    return min(max(PLOT_H, 40 + len(rows) * 32), 480)


def table_basic(title, headers, rows, subtitle="", number_cols=None):
    """
    Plain table — right-aligns number columns, left-aligns text columns.

    Args:
        headers:     list of column header strings
        rows:        list of row lists (same length as headers)
        number_cols: set/list of column indices to right-align (auto-detected if None)
    """
    n_cols = len(headers)
    # Transpose rows → columns (Plotly expects column-major)
    columns = [[row[i] for row in rows] for i in range(n_cols)]

    # Auto-detect numeric columns
    if number_cols is None:
        number_cols = set()
        for ci, col in enumerate(columns):
            if all(isinstance(v, (int, float)) or str(v).replace(".", "").replace("-", "").replace(",", "").isnumeric() for v in col if v not in (None, "", "—")):
                number_cols.add(ci)

    align = ["right" if i in number_cols else "left" for i in range(n_cols)]

    # Alternating row colours
    fill_colors = []
    for ci in range(n_cols):
        col_fills = [BG_SURFACE if ri % 2 == 0 else "#F8FAFB" for ri in range(len(rows))]
        fill_colors.append(col_fills)

    h = _table_height(rows)
    fig = go.Figure(go.Table(
        header=dict(
            values=[f"<b>{h}</b>" for h in headers],
            fill_color=AZURE_PALE,
            align=align,
            font=dict(family=FONT_FAMILY, size=12, color=TEXT),
            line_color=BORDER,
            height=32,
        ),
        cells=dict(
            values=columns,
            fill_color=fill_colors,
            align=align,
            font=dict(family=FONT_FAMILY, size=12, color=TEXT),
            line_color=BORDER,
            height=30,
        ),
    ))

    fig.update_layout({
        "margin": dict(l=0, r=0, t=0, b=0),
        "paper_bgcolor": "rgba(0,0,0,0)",
        "height": h,
    })

    return _chart(title=title, subtitle=subtitle, figure=fig, height=h)


def table_heatmap(title, headers, rows, subtitle="", number_cols=None, diverging=False):
    """
    Heatmap table — colour-encodes numeric cells while keeping values visible.
    KB rule: always show numbers, never hide them behind colour.

    Args:
        headers:     list of column header strings
        rows:        list of row lists
        number_cols: column indices to colour-encode (auto-detected if None)
        diverging:   if True, use NEGATIVE→white→POSITIVE (for +/- data)
                     if False, use sequential white→AZURE_1
    """
    import numpy as np

    n_cols = len(headers)
    columns = [[row[i] for row in rows] for i in range(n_cols)]

    if number_cols is None:
        number_cols = set()
        for ci, col in enumerate(columns):
            if all(isinstance(v, (int, float)) for v in col if v is not None):
                number_cols.add(ci)

    def _cell_color(value, col_min, col_max, is_diverging):
        if value is None:
            return BG_SURFACE
        if col_max == col_min:
            return BG_SURFACE
        norm = (value - col_min) / (col_max - col_min)  # 0–1
        if is_diverging:
            mid = (0 - col_min) / (col_max - col_min) if col_min < 0 else 0.5
            if norm >= mid:
                t = (norm - mid) / (1 - mid) if mid < 1 else 0
                r, g, b = _lerp_color("#FFFFFF", POSITIVE, t)
            else:
                t = 1 - (norm / mid) if mid > 0 else 0
                r, g, b = _lerp_color("#FFFFFF", NEGATIVE, t)
            return f"rgb({r},{g},{b})"
        else:
            r, g, b = _lerp_color("#FFFFFF", AZURE_1, norm * 0.7)
            return f"rgb({r},{g},{b})"

    def _lerp_color(hex1, hex2, t):
        r1, g1, b1 = int(hex1[1:3], 16), int(hex1[3:5], 16), int(hex1[5:7], 16)
        r2, g2, b2 = int(hex2[1:3], 16), int(hex2[3:5], 16), int(hex2[5:7], 16)
        return (int(r1 + (r2 - r1) * t), int(g1 + (g2 - g1) * t), int(b1 + (b2 - b1) * t))

    # Build per-cell fill colours
    fill_colors = []
    for ci in range(n_cols):
        if ci in number_cols:
            numeric_vals = [v for v in columns[ci] if isinstance(v, (int, float))]
            col_min = min(numeric_vals) if numeric_vals else 0
            col_max = max(numeric_vals) if numeric_vals else 1
            if diverging:
                extreme = max(abs(col_min), abs(col_max))
                col_min, col_max = -extreme, extreme
            col_fills = [_cell_color(v, col_min, col_max, diverging) for v in columns[ci]]
        else:
            col_fills = [BG_SURFACE] * len(rows)
        fill_colors.append(col_fills)

    align = ["right" if i in number_cols else "left" for i in range(n_cols)]
    h = _table_height(rows)

    fig = go.Figure(go.Table(
        header=dict(
            values=[f"<b>{h}</b>" for h in headers],
            fill_color=AZURE_PALE,
            align=align,
            font=dict(family=FONT_FAMILY, size=12, color=TEXT),
            line_color=BORDER,
            height=32,
        ),
        cells=dict(
            values=columns,
            fill_color=fill_colors,
            align=align,
            font=dict(family=FONT_FAMILY, size=12, color=TEXT),
            line_color=BORDER,
            height=30,
        ),
    ))

    fig.update_layout({
        "margin": dict(l=0, r=0, t=0, b=0),
        "paper_bgcolor": "rgba(0,0,0,0)",
        "height": h,
    })

    return _chart(title=title, subtitle=subtitle, figure=fig, height=h)
