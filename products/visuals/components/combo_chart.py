"""
Combo and subplot chart variants — Power BI naming convention.
KB reference: team/analytics/visualization/charts/combo-subplots.md

Rules applied:
  - line_clustered_column / line_stacked_column: same-scale data only (KB rule)
  - combo_subplots: stacked panels sharing x-axis — the IBCS fiscal pattern
  - No dual-axis implementation (KB: dual-axis misleads unless scales truly identical)

y_measure (optional Measure):
  When provided on line_* variants, sets y-axis title, tickformat and ticksuffix.
  combo_subplots uses per-panel "title" string instead (multiple y-axes).
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from products.visuals.lib.theme import (
    COLORWAY, POSITIVE, NEGATIVE, SUBTEXT, TEXT, BORDER, GRID, ZERO_LINE, FONT_FAMILY,
)
from products.visuals.components import (
    PLOT_H, PLOT_H_TALL, MARGIN_L, MARGIN_R, MARGIN_T, MARGIN_B, _chart,
)


def _legend(series):
    return (
        [(s["name"], s.get("color", COLORWAY[i % len(COLORWAY)])) for i, s in enumerate(series)]
        if len(series) > 1 else None
    )


def _combo_base_layout(barmode="group"):
    return {
        "template": "teal",
        "height": PLOT_H,
        "barmode": barmode,
        "margin": dict(l=MARGIN_L, r=MARGIN_R, t=MARGIN_T, b=MARGIN_B),
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "xaxis": dict(showgrid=False, showline=True, linecolor=BORDER,
                      tickfont=dict(size=11, color=SUBTEXT)),
        "yaxis": dict(gridcolor=GRID, zerolinecolor=ZERO_LINE, showgrid=True,
                      tickfont=dict(size=11, color=SUBTEXT), rangemode="tozero"),
        "showlegend": False,
        "hovermode": "x unified",
    }


def line_clustered_column(title, x, bar_series, line_series, subtitle="", y_measure=None):
    """
    Line + clustered columns on a shared axis.
    Use only when both series share the same scale and units (KB rule).

    Args:
        bar_series:  list of {"name": str, "y": list, "color": str (optional)}
        line_series: list of {"name": str, "y": list, "color": str (optional)}
        y_measure:   when provided, sets y-axis title, tickformat and ticksuffix
    """
    fig = go.Figure()
    for i, s in enumerate(bar_series):
        fig.add_trace(go.Bar(
            x=x, y=s["y"], name=s["name"],
            marker_color=s.get("color", COLORWAY[i % len(COLORWAY)]),
        ))
    for i, s in enumerate(line_series):
        color = s.get("color", COLORWAY[(len(bar_series) + i) % len(COLORWAY)])
        fig.add_trace(go.Scatter(
            x=x, y=s["y"], name=s["name"], mode="lines+markers",
            line=dict(color=color, width=2, shape="linear"),
            marker=dict(size=5, color=color),
        ))
    layout = _combo_base_layout(barmode="group")
    if y_measure is not None:
        y_measure.apply_to_yaxis(layout["yaxis"])
    fig.update_layout(layout)
    all_series = bar_series + line_series
    legend = [
        (s["name"], s.get("color", COLORWAY[i % len(COLORWAY)]))
        for i, s in enumerate(all_series)
    ]
    return _chart(title=title, subtitle=subtitle, legend_items=legend, figure=fig)


def line_stacked_column(title, x, bar_series, line_series, subtitle="", y_measure=None):
    """
    Line + stacked columns on a shared axis.
    Columns show composition; line shows a related aggregate metric.

    Args:
        bar_series:  list of {"name": str, "y": list, "color": str (optional)}
        line_series: list of {"name": str, "y": list, "color": str (optional)}
        y_measure:   when provided, sets y-axis title, tickformat and ticksuffix
    """
    fig = go.Figure()
    for i, s in enumerate(bar_series):
        fig.add_trace(go.Bar(
            x=x, y=s["y"], name=s["name"],
            marker_color=s.get("color", COLORWAY[i % len(COLORWAY)]),
        ))
    for i, s in enumerate(line_series):
        color = s.get("color", COLORWAY[(len(bar_series) + i) % len(COLORWAY)])
        fig.add_trace(go.Scatter(
            x=x, y=s["y"], name=s["name"], mode="lines+markers",
            line=dict(color=color, width=2, shape="linear"),
            marker=dict(size=5, color=color),
        ))
    layout = _combo_base_layout(barmode="stack")
    if y_measure is not None:
        y_measure.apply_to_yaxis(layout["yaxis"])
    fig.update_layout(layout)
    all_series = bar_series + line_series
    legend = [
        (s["name"], s.get("color", COLORWAY[i % len(COLORWAY)]))
        for i, s in enumerate(all_series)
    ]
    return _chart(title=title, subtitle=subtitle, legend_items=legend, figure=fig)


def line_pct_stacked_column(title, x, bar_series, line_series, subtitle="", y_measure=None):
    """
    Line + 100% stacked columns on a shared axis.
    Columns are normalised to 100%; line shows a rate or % measure.

    Args:
        bar_series:  list of {"name": str, "y": list, "color": str (optional)}
        line_series: list of {"name": str, "y": list, "color": str (optional)}
        y_measure:   when provided, sets y-axis title, tickformat and ticksuffix
                     (overrides the default "%" ticksuffix on the normalised axis)
    """
    n = len(x)
    totals = [sum(s["y"][i] for s in bar_series if i < len(s["y"])) for i in range(n)]
    norm_series = []
    for s in bar_series:
        norm_y = [
            round(s["y"][i] / totals[i] * 100, 1) if totals[i] else 0
            for i in range(min(len(s["y"]), n))
        ]
        norm_series.append({**s, "y": norm_y})

    fig = go.Figure()
    for i, s in enumerate(norm_series):
        fig.add_trace(go.Bar(
            x=x, y=s["y"], name=s["name"],
            marker_color=s.get("color", COLORWAY[i % len(COLORWAY)]),
        ))
    for i, s in enumerate(line_series):
        color = s.get("color", COLORWAY[(len(bar_series) + i) % len(COLORWAY)])
        fig.add_trace(go.Scatter(
            x=x, y=s["y"], name=s["name"], mode="lines+markers",
            line=dict(color=color, width=2, shape="linear"),
            marker=dict(size=5, color=color),
        ))
    layout = _combo_base_layout(barmode="relative")
    layout["yaxis"]["ticksuffix"] = "%"
    if y_measure is not None:
        y_measure.apply_to_yaxis(layout["yaxis"])
    fig.update_layout(layout)
    all_series = bar_series + line_series
    legend = [
        (s["name"], s.get("color", COLORWAY[i % len(COLORWAY)]))
        for i, s in enumerate(all_series)
    ]
    return _chart(title=title, subtitle=subtitle, legend_items=legend, figure=fig)


def combo_subplots(title, x, panels, subtitle=""):
    """
    Stacked subplots sharing x-axis — the IBCS fiscal pattern.
    Use when panel metrics have incompatible scales or units.

    Args:
        panels: list of panel dicts:
            {
                "title":     str — y-axis label
                "type":      "bar" | "line"
                "series":    [{"name": str, "y": list, "color": str (optional)}]
                "diverging": bool (optional) — POSITIVE/NEGATIVE colours per value
            }

    Note: each panel has its own y-axis; use panel["title"] for per-panel labels.
    y_measure is not supported here — configure per panel via the "title" key.
    """
    n = len(panels)
    total_h = max(PLOT_H_TALL, n * 130 + 60)

    fig = make_subplots(
        rows=n, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.06,
        row_heights=[1 / n] * n,
    )

    for row_idx, panel in enumerate(panels, start=1):
        diverging = panel.get("diverging", False)
        ptype = panel.get("type", "bar")

        for si, s in enumerate(panel.get("series", [])):
            color = s.get("color", COLORWAY[si % len(COLORWAY)])

            if ptype == "bar":
                fig.add_trace(go.Bar(
                    x=x, y=s["y"], name=s["name"],
                    marker_color=[POSITIVE if v >= 0 else NEGATIVE for v in s["y"]] if diverging else color,
                    showlegend=False,
                ), row=row_idx, col=1)
            else:
                fig.add_trace(go.Scatter(
                    x=x, y=s["y"], name=s["name"], mode="lines",
                    line=dict(color=POSITIVE if diverging else color, width=2, shape="linear"),
                    showlegend=False,
                ), row=row_idx, col=1)

        fig.update_yaxes(
            title_text=panel.get("title", ""),
            title_font=dict(size=11, color=SUBTEXT),
            gridcolor=GRID, zerolinecolor=ZERO_LINE,
            tickfont=dict(size=10, color=SUBTEXT),
            row=row_idx, col=1,
        )
        fig.update_xaxes(
            showline=True, linecolor=BORDER,
            tickfont=dict(size=11, color=SUBTEXT),
            showticklabels=(row_idx == n),
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
