"""
Bar and column chart variants — Power BI naming convention.
KB reference: team/analytics/visualization/charts/bar.md

Naming:
  column = vertical bars   bar = horizontal bars
  clustered = grouped      stacked = stacked      pct_stacked = 100% normalised

Rules applied:
  - All column variants enforce rangemode="tozero"
  - bar_diverging uses POSITIVE/NEGATIVE semantic colours
  - Horizontal variants sort descending by default (KB: largest at top)
"""
import plotly.graph_objects as go

from products.visuals.lib.theme import COLORWAY, POSITIVE, NEGATIVE, SLATE_1, SUBTEXT, TEXT, BORDER, GRID, ZERO_LINE, AZURE_1
from products.visuals.components import PLOT_H, _plotly_layout, _chart


# ── Internal helpers ──────────────────────────────────────────────────────────

def _bar_layout_h(**kw):
    """Horizontal bar layout — swapped grid/line on axes."""
    return {
        "template": "teal",
        "height": PLOT_H,
        "margin": dict(l=8, r=40, t=4, b=40),
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "xaxis": dict(
            gridcolor=GRID, zerolinecolor=ZERO_LINE, showgrid=True,
            showline=False, tickfont=dict(size=11, color=SUBTEXT),
            rangemode="tozero",
        ),
        "yaxis": dict(
            gridcolor="rgba(0,0,0,0)", showgrid=False,
            showline=False, tickfont=dict(size=11, color=SUBTEXT),
            automargin=True,
        ),
        "showlegend": False,
        "hovermode": "y unified",
        **kw,
    }


def _legend(series):
    return [(s["name"], s.get("color", COLORWAY[i % len(COLORWAY)])) for i, s in enumerate(series)] if len(series) > 1 else None


# ── Column (vertical) variants ────────────────────────────────────────────────

def clustered_column(title, x, series, subtitle="", show_labels=False, reference=None):
    """Vertical grouped bars — compare multiple series side by side."""
    fig = go.Figure()
    for i, s in enumerate(series):
        color = s.get("color", COLORWAY[i % len(COLORWAY)])
        fig.add_trace(go.Bar(
            x=x, y=s["y"], name=s["name"], marker_color=color,
            text=[str(v) for v in s["y"]] if show_labels else None,
            textposition="outside" if show_labels else "none",
            textfont=dict(size=11, color=SUBTEXT),
        ))
    layout = _plotly_layout(barmode="group", yaxis={"rangemode": "tozero"})
    if reference:
        layout.setdefault("shapes", []).append(dict(
            type="line", x0=-0.5, x1=len(x) - 0.5,
            y0=reference["value"], y1=reference["value"],
            line=dict(color=SLATE_1, width=1.5, dash="dash"),
        ))
        layout.setdefault("annotations", []).append(dict(
            x=len(x) - 0.5, y=reference["value"],
            text=reference.get("label", ""), showarrow=False,
            font=dict(size=11, color=SLATE_1), xanchor="right", yanchor="bottom",
        ))
    fig.update_layout(layout)
    return _chart(title=title, subtitle=subtitle, legend_items=_legend(series), figure=fig)


def stacked_column(title, x, series, subtitle="", show_labels=False):
    """Vertical stacked bars — total AND composition."""
    fig = go.Figure()
    for i, s in enumerate(series):
        color = s.get("color", COLORWAY[i % len(COLORWAY)])
        fig.add_trace(go.Bar(
            x=x, y=s["y"], name=s["name"], marker_color=color,
            text=[str(v) for v in s["y"]] if show_labels else None,
            textposition="inside" if show_labels else "none",
            textfont=dict(size=11, color="white"),
        ))
    fig.update_layout(_plotly_layout(barmode="stack", yaxis={"rangemode": "tozero"}))
    return _chart(title=title, subtitle=subtitle, legend_items=_legend(series), figure=fig)


def pct_stacked_column(title, x, series, subtitle="", show_labels=False):
    """Vertical 100% normalised stacked bars — composition only."""
    # Normalise each category's values so they sum to 100
    n = len(x)
    totals = [sum(s["y"][i] for s in series if i < len(s["y"])) for i in range(n)]
    norm_series = []
    for s in series:
        norm_y = [
            round(v / totals[i] * 100, 1) if totals[i] else 0
            for i, v in enumerate(s["y"])
        ]
        norm_series.append({**s, "y": norm_y})

    fig = go.Figure()
    for i, s in enumerate(norm_series):
        color = s.get("color", COLORWAY[i % len(COLORWAY)])
        fig.add_trace(go.Bar(
            x=x, y=s["y"], name=s["name"], marker_color=color,
            text=[f"{v}%" for v in s["y"]] if show_labels else None,
            textposition="inside" if show_labels else "none",
            textfont=dict(size=11, color="white"),
        ))
    layout = _plotly_layout(barmode="relative", yaxis={"rangemode": "tozero", "ticksuffix": "%"})
    fig.update_layout(layout)
    return _chart(title=title, subtitle=subtitle, legend_items=_legend(series), figure=fig)


# ── Bar (horizontal) variants ─────────────────────────────────────────────────

def clustered_bar(title, categories, series, subtitle="", show_labels=False, sort=True):
    """
    Horizontal grouped bars.
    Single series → ranked list (sorted descending).
    Multiple series → grouped horizontal comparison.

    Args:
        sort: sort by first series descending (applies to single-series only)
    """
    if sort and len(series) == 1:
        pairs = sorted(zip(series[0]["y"], categories), reverse=True)
        sorted_vals = [p[0] for p in pairs]
        sorted_cats = [p[1] for p in pairs]
        plot_series = [{**series[0], "y": sorted_vals}]
        plot_cats = sorted_cats
    else:
        plot_series = series
        plot_cats = categories

    fig = go.Figure()
    for i, s in enumerate(plot_series):
        color = s.get("color", COLORWAY[i % len(COLORWAY)])
        fig.add_trace(go.Bar(
            x=s["y"], y=plot_cats, name=s["name"], orientation="h",
            marker_color=color,
            text=[str(v) for v in s["y"]] if show_labels else None,
            textposition="outside" if show_labels else "none",
            textfont=dict(size=11, color=SUBTEXT),
        ))
    fig.update_layout(_bar_layout_h(barmode="group"))
    return _chart(title=title, subtitle=subtitle, legend_items=_legend(plot_series), figure=fig)


def stacked_bar(title, categories, series, subtitle="", show_labels=False, sort=False):
    """Horizontal stacked bars — total AND composition."""
    if sort and len(series) >= 1:
        totals = [sum(s["y"][i] for s in series) for i in range(len(categories))]
        order = sorted(range(len(categories)), key=lambda i: totals[i], reverse=True)
        sorted_cats = [categories[i] for i in order]
        plot_series = [{**s, "y": [s["y"][i] for i in order]} for s in series]
    else:
        sorted_cats = categories
        plot_series = series

    fig = go.Figure()
    for i, s in enumerate(plot_series):
        color = s.get("color", COLORWAY[i % len(COLORWAY)])
        fig.add_trace(go.Bar(
            x=s["y"], y=sorted_cats, name=s["name"], orientation="h",
            marker_color=color,
            text=[str(v) for v in s["y"]] if show_labels else None,
            textposition="inside" if show_labels else "none",
            textfont=dict(size=11, color="white"),
        ))
    fig.update_layout(_bar_layout_h(barmode="stack"))
    return _chart(title=title, subtitle=subtitle, legend_items=_legend(plot_series), figure=fig)


def pct_stacked_bar(title, categories, series, subtitle="", show_labels=False):
    """Horizontal 100% normalised stacked bars — composition only."""
    # Normalise each category's values so they sum to 100
    n = len(categories)
    totals = [sum(s["y"][i] for s in series if i < len(s["y"])) for i in range(n)]
    norm_series = []
    for s in series:
        norm_y = [
            round(v / totals[i] * 100, 1) if totals[i] else 0
            for i, v in enumerate(s["y"])
        ]
        norm_series.append({**s, "y": norm_y})

    fig = go.Figure()
    for i, s in enumerate(norm_series):
        color = s.get("color", COLORWAY[i % len(COLORWAY)])
        fig.add_trace(go.Bar(
            x=s["y"], y=categories, name=s["name"], orientation="h",
            marker_color=color,
            text=[f"{v}%" for v in s["y"]] if show_labels else None,
            textposition="inside" if show_labels else "none",
            textfont=dict(size=11, color="white"),
        ))
    layout = _bar_layout_h(barmode="relative")
    layout["xaxis"]["ticksuffix"] = "%"
    fig.update_layout(layout)
    return _chart(title=title, subtitle=subtitle, legend_items=_legend(series), figure=fig)


def bar_diverging(title, x, values, subtitle="", show_labels=False):
    """
    Vertical diverging bars — positive/negative from zero.
    POSITIVE (green) for gains, NEGATIVE (red) for losses.
    """
    colors = [POSITIVE if v >= 0 else NEGATIVE for v in values]
    fig = go.Figure(go.Bar(
        x=x, y=values, marker_color=colors,
        text=[str(v) for v in values] if show_labels else None,
        textposition="outside" if show_labels else "none",
        textfont=dict(size=11, color=SUBTEXT),
    ))
    fig.update_layout(_plotly_layout(
        yaxis={"zeroline": True, "zerolinewidth": 1.5, "zerolinecolor": "#C5D0D8"},
    ))
    return _chart(title=title, subtitle=subtitle, figure=fig)
