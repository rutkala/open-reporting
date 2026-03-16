"""
Regional Budgets Dashboard — 16 Polish voivodships 1999–2024.
Charts: aggregate trend · 2024 comparison · balance heatmap · region detail
Interactive: region selector updates detail chart
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import json
from lib.db import query
from lib.theme import C, AXIS, PALETTE, apply, page, kpi_card

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "charts")


def build():
    agg = query("""
        SELECT year,
               SUM(CASE WHEN variable_name='revenues'     THEN value/1e9 END) AS revenues_bn,
               SUM(CASE WHEN variable_name='expenditures' THEN value/1e9 END) AS expenditures_bn
        FROM raw.bdl_budget
        GROUP BY year ORDER BY year
    """)
    agg["balance_bn"] = (agg["revenues_bn"] - agg["expenditures_bn"]).round(3)

    cmp24 = query("""
        SELECT unit_name,
               MAX(CASE WHEN variable_name='revenues'     THEN value/1e9 END) AS rev,
               MAX(CASE WHEN variable_name='expenditures' THEN value/1e9 END) AS exp
        FROM raw.bdl_budget WHERE year=2024
        GROUP BY unit_name ORDER BY rev DESC
    """)
    cmp24["balance"] = (cmp24["rev"] - cmp24["exp"]).round(2)

    detail = query("""
        SELECT unit_name, year,
               SUM(CASE WHEN variable_name='revenues'     THEN value/1e9 END) AS rev,
               SUM(CASE WHEN variable_name='expenditures' THEN value/1e9 END) AS exp
        FROM raw.bdl_budget
        GROUP BY unit_name, year ORDER BY unit_name, year
    """)
    detail["balance"] = (detail["rev"] - detail["exp"]).round(3)

    heatmap = query("""
        SELECT unit_name, year,
               ROUND((SUM(CASE WHEN variable_name='revenues'     THEN value END) -
                      SUM(CASE WHEN variable_name='expenditures' THEN value END)) / 1e6, 1) AS balance_mn
        FROM raw.bdl_budget
        GROUP BY unit_name, year
    """)
    pivot = heatmap.pivot(index="unit_name", columns="year", values="balance_mn")

    regions = sorted(detail["unit_name"].unique().tolist())

    # ── KPIs ──────────────────────────────────────────────────────────────────
    latest_agg = agg.iloc[-1]
    prev_agg   = agg.iloc[-2]
    surplus_regions = int((cmp24["balance"] > 0).sum())
    deficit_regions = int((cmp24["balance"] < 0).sum())

    kpis = "".join([
        kpi_card("Total Revenues 2024", f"{latest_agg.revenues_bn:.1f} bn PLN",
                 f"▲ {latest_agg.revenues_bn - prev_agg.revenues_bn:.1f} bn vs 2023", "pos"),
        kpi_card("Budget Balance 2024", f"{latest_agg.balance_bn:+.2f} bn PLN",
                 f"Surplus" if latest_agg.balance_bn > 0 else "Deficit",
                 "pos" if latest_agg.balance_bn > 0 else "neg"),
        kpi_card("Regions in Surplus", f"{surplus_regions} / 16", "", "neu"),
        kpi_card("Largest Region", "Mazowieckie",
                 f"{cmp24[cmp24.unit_name.str.contains('MAZOW')]['rev'].values[0]:.2f} bn PLN", "neu"),
    ])

    # ── Chart 1: Aggregate trend ───────────────────────────────────────────────
    fig1 = make_subplots(
        rows=2, cols=1, row_heights=[0.65, 0.35],
        shared_xaxes=True, vertical_spacing=0.06,
        subplot_titles=["Aggregate Revenues & Expenditures (bn PLN)", "Aggregate Balance (bn PLN)"],
    )
    fig1.add_trace(go.Scatter(
        x=agg.year, y=agg.revenues_bn.round(2), name="Revenues",
        mode="lines+markers", line=dict(color=C["blue"], width=2.5), marker=dict(size=6),
    ), row=1, col=1)
    fig1.add_trace(go.Scatter(
        x=agg.year, y=agg.expenditures_bn.round(2), name="Expenditures",
        mode="lines+markers", line=dict(color=C["red"], width=2.5), marker=dict(size=6),
    ), row=1, col=1)
    fig1.add_trace(go.Bar(
        x=agg.year, y=agg.balance_bn,
        name="Balance",
        marker_color=[C["green"] if v >= 0 else C["red"] for v in agg.balance_bn],
        hovertemplate="<b>Balance %{x}</b>: %{y:.3f} bn PLN<extra></extra>",
    ), row=2, col=1)
    fig1.update_layout(
        paper_bgcolor=C["bg"], plot_bgcolor=C["surface"],
        font=dict(family="Inter, system-ui, sans-serif", color=C["text"]),
        height=500, hovermode="x unified",
        legend=dict(bgcolor=C["surface"], bordercolor=C["border"], borderwidth=1),
        margin=dict(l=60, r=30, t=50, b=20),
    )
    for r in [1, 2]:
        fig1.update_xaxes(row=r, col=1, **AXIS)
        fig1.update_yaxes(row=r, col=1, **AXIS)

    # ── Chart 2: 2024 regional comparison ─────────────────────────────────────
    cmp_s = cmp24.sort_values("rev")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        y=cmp_s.unit_name, x=cmp_s.rev.round(2),
        name="Revenues", orientation="h", marker_color=C["blue"],
        hovertemplate="<b>%{y}</b><br>Revenue: %{x:.2f} bn PLN<extra></extra>",
    ))
    fig2.add_trace(go.Bar(
        y=cmp_s.unit_name, x=cmp_s.exp.round(2),
        name="Expenditures", orientation="h", marker_color=C["red"], opacity=0.7,
        hovertemplate="<b>%{y}</b><br>Expenditures: %{x:.2f} bn PLN<extra></extra>",
    ))
    apply(fig2, "Regional Budgets 2024", "Revenues vs expenditures per voivodship",
          height=500, barmode="overlay")
    fig2.update_xaxes(title_text="bn PLN")

    # ── Chart 3: Heatmap ──────────────────────────────────────────────────────
    fig3 = go.Figure(go.Heatmap(
        z=pivot.values,
        x=[str(c) for c in pivot.columns],
        y=pivot.index.tolist(),
        colorscale=[[0, C["red"]], [0.45, "#3B2A1A"], [0.5, C["surface"]], [0.55, "#1A2B1A"], [1, C["green"]]],
        zmid=0,
        colorbar=dict(title="mn PLN", tickfont=dict(color=C["text"], size=10)),
        hovertemplate="<b>%{y}</b> · %{x}<br>Balance: %{z:.0f} mn PLN<extra></extra>",
    ))
    apply(fig3, "Budget Balance Heatmap 1999–2024",
          "Green = surplus · Red = deficit · Values in million PLN", height=460)

    # ── Chart 4: Region detail (interactive) ──────────────────────────────────
    # Build one trace per region, show only the first by default
    # JS handles the selector to show/hide traces
    traces_rev, traces_exp, traces_bal = [], [], []
    for i, region in enumerate(regions):
        sub = detail[detail.unit_name == region]
        visible = True if i == 0 else False
        traces_rev.append(dict(
            x=sub.year.tolist(), y=sub.rev.round(3).tolist(),
            name="Revenues", mode="lines+markers",
            line=dict(color=C["blue"], width=2), marker=dict(size=5),
            visible=visible,
        ))
        traces_exp.append(dict(
            x=sub.year.tolist(), y=sub.exp.round(3).tolist(),
            name="Expenditures", mode="lines+markers",
            line=dict(color=C["red"], width=2), marker=dict(size=5),
            visible=visible,
        ))
        traces_bal.append(dict(
            x=sub.year.tolist(), y=sub.balance.tolist(),
            name="Balance",
            type="bar",
            marker=dict(color=[C["green"] if v >= 0 else C["red"] for v in sub.balance]),
            visible=visible,
        ))

    detail_data = {r: {
        "rev": detail[detail.unit_name == r].rev.round(3).tolist(),
        "exp": detail[detail.unit_name == r].exp.round(3).tolist(),
        "bal": detail[detail.unit_name == r].balance.tolist(),
        "years": detail[detail.unit_name == r].year.tolist(),
    } for r in regions}

    # ── Assemble HTML ──────────────────────────────────────────────────────────
    def div(fig):
        return pio.to_html(fig, include_plotlyjs=False, full_html=False,
                           config={"displayModeBar": True})

    # Build region selector options
    options = "\n".join(f'<option value="{r}">{r}</option>' for r in regions)

    detail_js = f"const DETAIL = {json.dumps(detail_data)};"

    body = f"""
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<div class="charts">
  <div class="chart-card full">{div(fig1)}</div>
  <div class="charts two-col" style="grid-column:1/-1">
    <div class="chart-card">{div(fig2)}</div>
    <div class="chart-card">{div(fig3)}</div>
  </div>
  <div class="chart-card full">
    <div style="padding:0.75rem 0.75rem 0">
      <div class="controls">
        <label>Select region:</label>
        <select id="region-select">{options}</select>
      </div>
    </div>
    <div id="region-detail"></div>
  </div>
</div>

<script>
{detail_js}

const bg = "{C['bg']}";
const surface = "{C['surface']}";
const border = "{C['border']}";
const blue = "{C['blue']}";
const red = "{C['red']}";
const green = "{C['green']}";
const muted = "{C['muted']}";
const text = "{C['text']}";

function renderDetail(region) {{
  const d = DETAIL[region];
  const balColors = d.bal.map(v => v >= 0 ? green : red);
  const traces = [
    {{ x: d.years, y: d.rev, name: 'Revenues', mode: 'lines+markers',
       yaxis: 'y', line: {{ color: blue, width: 2 }}, marker: {{ size: 5 }} }},
    {{ x: d.years, y: d.exp, name: 'Expenditures', mode: 'lines+markers',
       yaxis: 'y', line: {{ color: red, width: 2 }}, marker: {{ size: 5 }} }},
    {{ x: d.years, y: d.bal, name: 'Balance', type: 'bar',
       yaxis: 'y2', marker: {{ color: balColors }}, opacity: 0.85 }},
  ];
  const layout = {{
    paper_bgcolor: bg, plot_bgcolor: surface,
    font: {{ family: 'Inter, system-ui, sans-serif', color: text, size: 12 }},
    height: 380, hovermode: 'x unified',
    legend: {{ bgcolor: surface, bordercolor: border, borderwidth: 1, font: {{ size: 11 }} }},
    margin: {{ l: 60, r: 60, t: 40, b: 40 }},
    title: {{ text: '<b>' + region + '</b> — Budget 1999–2024', font: {{ size: 15 }}, x: 0.01 }},
    xaxis: {{ gridcolor: border, linecolor: border, tickfont: {{ color: muted }} }},
    yaxis: {{ gridcolor: border, linecolor: border, tickfont: {{ color: muted }},
              title: {{ text: 'bn PLN', font: {{ color: muted }} }} }},
    yaxis2: {{ overlaying: 'y', side: 'right', gridcolor: 'transparent',
               linecolor: border, tickfont: {{ color: muted }},
               title: {{ text: 'Balance (bn PLN)', font: {{ color: muted }} }} }},
  }};
  Plotly.react('region-detail', traces, layout, {{ displayModeBar: false, responsive: true }});
}}

document.getElementById('region-select').addEventListener('change', function() {{
  renderDetail(this.value);
}});

renderDetail(document.getElementById('region-select').value);
</script>"""

    html = page(
        title="Polish Regional Budgets 1999–2024",
        subtitle="16 voivodships — revenues, expenditures, fiscal balance · Source: GUS BDL API",
        active="Regional Budgets",
        kpis=f'<div class="kpis">{kpis}</div>',
        body=body,
        source="GUS Bank Danych Lokalnych",
    )

    out = os.path.join(OUT, "voivodship.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓ voivodship.html")


if __name__ == "__main__":
    build()
