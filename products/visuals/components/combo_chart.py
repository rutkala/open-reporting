"""
Combo and subplot chart variants.
KB reference: team/analytics/visualization/charts/combo-subplots.md

Rules applied:
- combo_bar_line: only for same-scale data (KB: never force dual-axis)
- combo_subplots: stacked panels sharing x-axis — the IBCS fiscal pattern
- No dual-axis implementation (KB: dual-axis misleads unless scales truly identical)
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from products.visuals.lib.theme import COLORWAY, POSITIVE, NEGATIVE, SUBTEXT, TEXT, BORDER
from products.visuals.components import PLOT_H, PLOT_H_TALL, MARGIN_L, MARGIN_R, MARGIN_T, MARGIN_B, _chart
from products.visuals.lib.theme import FONT_FAMILY, GRID, ZERO_LINE


def _rgba(hex_color: str, alpha: float) -> str:
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    return f"rgba({r},{g},{b},{alpha})"


def combo_bar_line(title, x, bar_series, line_series, subtitle=""):
    """
    Bar + line overlay on a shared axis.
    Use only when both series share the same scale and units (KB rule).

    Args:
        bar_series:  list of {"name": str, "y": list, "color": str (optional)}
        line_series: list of {"name": str, "y": list, "color": str (optional)}
    """
    fig = go.Figure()

    for i, s in enumerate(bar_series):
        color = s.get("color", COLORWAY[i % len(COLORWAY)])
        fig.add_trace(go.Bar(
            x=x, y=s["y"], name=s["name"],
            marker_color=color,
        ))

    bar_count = len(bar_series)
    for i, s in enumerate(line_series):
        color = s.get("color", COLORWAY[(bar_count + i) % len(COLORWAY)])
        fig.add_trace(go.Scatter(
            x=x, y=s["y"], name=s["name"], mode="lines+markers",
            line=dict(color=color, width=2, shape="linear"),
            marker=dict(size=5, color=color),
        ))

    fig.update_layout({
        "template": "teal",
        "height": PLOT_H,
        "barmode": "group",
        "margin": dict(l=MARGIN_L, r=MARGIN_R, t=MARGIN_T, b=MARGIN_B),
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": dict(family=FONT_FAMILY, color=TEXT, size=12),
        "xaxis": dict(showgrid=False, showline=True, linecolor=BORDER,
                      tickfont=dict(size=11, color=SUBTEXT)),
        "yaxis": dict(gridcolor=GRID, zerolinecolor=ZERO_LINE, showgrid=True,
                      tickfont=dict(size=11, color=SUBTEXT), rangemode="tozero"),
        "showlegend": False,
        "hovermode": "x unified",
    })

    all_series = bar_series + line_series
    legend = [(s["name"], s.get("color", COLORWAY[i % len(COLORWAY)])) for i, s in enumerate(all_series)]
    return _chart(title=title, subtitle=subtitle, legend_items=legend, figure=fig)


def combo_subplots(title, x, panels, subtitle=""):
    """
    Stacked subplots sharing x-axis — the IBCS fiscal pattern.
    Use when panel metrics have incompatible scales or units.

    Args:
        panels: list of panel dicts:
            {
                "title":  str,             panel label shown as y-axis title
                "type":   "bar" | "line",
                "series": [{"name": str, "y": list, "color": str (optional)}],
                "diverging": bool (optional) — use POSITIVE/NEGATIVE colors per bar
            }

    Example (revenue / expenditure / balance):
        panels=[
            {"title": "Dochody", "type": "bar",  "series": [{"name": "mld zł", "y": [...]}]},
            {"title": "Wydatki", "type": "bar",  "series": [{"name": "mld zł", "y": [...]}]},
            {"title": "Saldo",   "type": "line", "series": [{"name": "mld zł", "y": [...]}], "diverging": True},
        ]
    """
    n = len(panels)
    panel_h = 120          # height per panel in px
    total_h = max(PLOT_H_TALL, n * panel_h + 60)
    row_heights = [1 / n] * n

    fig = make_subplots(
        rows=n, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.06,
        row_heights=row_heights,
    )

    for row_idx, panel in enumerate(panels, start=1):
        is_last = row_idx == n
        series_list = panel.get("series", [])
        diverging = panel.get("diverging", False)
        ptype = panel.get("type", "bar")

        for si, s in enumerate(series_list):
            color = s.get("color", COLORWAY[si % len(COLORWAY)])

            if ptype == "bar":
                if diverging:
                    bar_colors = [POSITIVE if v >= 0 else NEGATIVE for v in s["y"]]
                else:
                    bar_colors = color
                fig.add_trace(go.Bar(
                    x=x, y=s["y"], name=s["name"],
                    marker_color=bar_colors,
                    showlegend=False,
                ), row=row_idx, col=1)

            else:  # line
                fig.add_trace(go.Scatter(
                    x=x, y=s["y"], name=s["name"], mode="lines",
                    line=dict(
                        color=POSITIVE if diverging else color,
                        width=2, shape="linear",
                    ),
                    showlegend=False,
                ), row=row_idx, col=1)

        # Panel y-axis label
        fig.update_yaxes(
            title_text=panel.get("title", ""),
            title_font=dict(size=11, color=SUBTEXT),
            gridcolor=GRID,
            zerolinecolor=ZERO_LINE,
            tickfont=dict(size=10, color=SUBTEXT),
            row=row_idx, col=1,
        )
        # Show x-axis only on last panel
        fig.update_xaxes(
            showline=True, linecolor=BORDER,
            tickfont=dict(size=11, color=SUBTEXT),
            showticklabels=is_last,
            row=row_idx, col=1,
        )

    fig.update_layout(
        template="teal",
        height=total_h,
        margin=dict(l=MARGIN_L + 20, r=MARGIN_R, t=MARGIN_T, b=MARGIN_B),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT_FAMILY, color=TEXT, size=12),
        showlegend=False,
        hovermode="x unified",
        barmode="group",
    )

    return _chart(title=title, subtitle=subtitle, figure=fig, height=total_h)
