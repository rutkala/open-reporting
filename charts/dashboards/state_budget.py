"""
State Budget Dashboard — interactive fiscal overview 2008–2024.
Charts: revenues vs expenditures · deficit · deficit % · YoY growth
Interactive: year range slider, metric toggle
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
from lib.db import query
from lib.theme import C, AXIS, PALETTE, apply, page, kpi_card

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "charts")


def build():
    df = query("SELECT * FROM national_budget ORDER BY year")
    df["deficit_abs"] = df["deficit_bn"].abs()
    df["deficit_pct"] = (df["deficit_abs"] / df["revenues_bn"] * 100).round(1)
    df["rev_growth"]  = df["revenues_bn"].pct_change() * 100
    df["exp_growth"]  = df["expenditures_bn"].pct_change() * 100

    latest = df.iloc[-1]
    prev   = df.iloc[-2]

    # ── KPI cards ─────────────────────────────────────────────────────────────
    rev_delta  = latest.revenues_bn - prev.revenues_bn
    exp_delta  = latest.expenditures_bn - prev.expenditures_bn
    def_delta  = latest.deficit_abs - prev.deficit_abs

    kpis = "".join([
        kpi_card("Revenues 2024",      f"{latest.revenues_bn:.1f} bn PLN",
                 f"{'▲' if rev_delta > 0 else '▼'} {abs(rev_delta):.1f} bn vs 2023",
                 "pos" if rev_delta > 0 else "neg"),
        kpi_card("Expenditures 2024",  f"{latest.expenditures_bn:.1f} bn PLN",
                 f"{'▲' if exp_delta > 0 else '▼'} {abs(exp_delta):.1f} bn vs 2023",
                 "neg" if exp_delta > 0 else "pos"),
        kpi_card("Deficit 2024",       f"{latest.deficit_abs:.1f} bn PLN",
                 f"{'▲' if def_delta > 0 else '▼'} {abs(def_delta):.1f} bn vs 2023",
                 "neg" if def_delta > 0 else "pos"),
        kpi_card("Deficit / Revenues", f"{latest.deficit_pct:.1f}%",
                 f"{'▲' if latest.deficit_pct > prev.deficit_pct else '▼'} "
                 f"{abs(latest.deficit_pct - prev.deficit_pct):.1f}pp vs 2023",
                 "neg" if latest.deficit_pct > prev.deficit_pct else "pos"),
    ])

    # ── Chart 1: Revenues & Expenditures + Deficit (combined) ─────────────────
    fig1 = make_subplots(
        rows=2, cols=1, row_heights=[0.65, 0.35],
        shared_xaxes=True, vertical_spacing=0.06,
        subplot_titles=["Revenues & Expenditures (bn PLN)", "Annual Deficit (bn PLN)"],
    )
    fig1.add_trace(go.Scatter(
        x=df.year, y=df.revenues_bn, name="Revenues",
        mode="lines+markers", line=dict(color=C["blue"], width=2.5), marker=dict(size=7),
        hovertemplate="<b>Revenues</b>: %{y:.1f} bn PLN<extra></extra>",
    ), row=1, col=1)
    fig1.add_trace(go.Scatter(
        x=df.year, y=df.expenditures_bn, name="Expenditures",
        mode="lines+markers", line=dict(color=C["red"], width=2.5), marker=dict(size=7),
        hovertemplate="<b>Expenditures</b>: %{y:.1f} bn PLN<extra></extra>",
    ), row=1, col=1)
    bar_colors = [C["yellow"] if v < 50 else C["orange"] if v < 100 else C["red"]
                  for v in df.deficit_abs]
    fig1.add_trace(go.Bar(
        x=df.year, y=df.deficit_abs, name="Deficit",
        marker_color=bar_colors,
        text=df.deficit_abs.round(1), textposition="outside",
        textfont=dict(size=10),
        hovertemplate="<b>Deficit</b>: %{y:.1f} bn PLN<extra></extra>",
    ), row=2, col=1)
    fig1.update_layout(
        paper_bgcolor=C["bg"], plot_bgcolor=C["surface"],
        font=dict(family="Inter, system-ui, sans-serif", color=C["text"]),
        height=520, hovermode="x unified",
        legend=dict(bgcolor=C["surface"], bordercolor=C["border"], borderwidth=1),
        margin=dict(l=60, r=30, t=50, b=20),
        xaxis2=dict(
            rangeslider=dict(visible=True, bgcolor=C["card"], thickness=0.04),
            type="linear",
        ),
    )
    for r in [1, 2]:
        fig1.update_xaxes(row=r, col=1, **AXIS)
        fig1.update_yaxes(row=r, col=1, **AXIS)

    # ── Chart 2: Deficit % of revenues ────────────────────────────────────────
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=df.year, y=df.deficit_pct,
        marker_color=[C["green"] if v < 10 else C["yellow"] if v < 20 else C["red"]
                      for v in df.deficit_pct],
        text=df.deficit_pct.astype(str) + "%", textposition="outside",
        textfont=dict(size=10),
        hovertemplate="<b>%{x}</b>: %{y:.1f}% of revenues<extra></extra>",
    ))
    fig2.add_hline(y=10, line_dash="dot", line_color=C["muted"],
                   annotation_text="10%", annotation_font_color=C["muted"])
    fig2.add_hline(y=20, line_dash="dot", line_color=C["red"],
                   annotation_text="20%", annotation_font_color=C["red"])
    apply(fig2, "Deficit as % of Revenues",
          "Fiscal pressure ratio — lower is better", height=380, showlegend=False)
    fig2.update_yaxes(ticksuffix="%")

    # ── Chart 3: YoY growth rates ──────────────────────────────────────────────
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=df.year[1:], y=df.rev_growth[1:].round(1),
        name="Revenue growth",
        marker_color=[C["blue"] if v >= 0 else C["red"] for v in df.rev_growth[1:]],
        hovertemplate="<b>Revenue growth %{x}</b>: %{y:.1f}%<extra></extra>",
    ))
    fig3.add_trace(go.Scatter(
        x=df.year[1:], y=df.exp_growth[1:].round(1),
        name="Expenditure growth", mode="lines+markers",
        line=dict(color=C["orange"], width=2), marker=dict(size=6),
        hovertemplate="<b>Expenditure growth %{x}</b>: %{y:.1f}%<extra></extra>",
    ))
    apply(fig3, "Year-over-Year Growth", "Revenue growth (bars) vs expenditure growth (line)",
          height=360)
    fig3.update_yaxes(ticksuffix="%")

    # ── Assemble page ──────────────────────────────────────────────────────────
    def chart_div(fig):
        return pio.to_html(fig, include_plotlyjs=False, full_html=False,
                           config={"displayModeBar": True, "scrollZoom": False})

    body = f"""
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<div class="charts">
  <div class="chart-card full">{chart_div(fig1)}</div>
  <div class="charts two-col" style="grid-column:1/-1">
    <div class="chart-card">{chart_div(fig2)}</div>
    <div class="chart-card">{chart_div(fig3)}</div>
  </div>
</div>"""

    html = page(
        title="Polish State Budget 2008–2024",
        subtitle="Central government revenues, expenditures, deficit and fiscal pressure · Annual data",
        active="State Budget",
        kpis=f'<div class="kpis">{kpis}</div>',
        body=body,
        source="NIK · Ministerstwo Finansów",
    )

    out = os.path.join(OUT, "state_budget.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓ state_budget.html")


if __name__ == "__main__":
    build()
