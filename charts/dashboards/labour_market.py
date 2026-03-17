"""
Labour Market Dashboard — 16 Polish voivodships.
Charts: unemployment rate trend · wage comparison · GDP per capita · region detail
Interactive: region selector for unemployment trend
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
from lib.db import query
from lib.theme import C, AXIS, PALETTE, apply, page, kpi_card

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "charts")


def build():
    # ── Load data ──────────────────────────────────────────────────────────────
    unemp = query("""
        SELECT unit_name, year, value AS unemp_rate
        FROM raw.bdl_labour
        WHERE variable_name = 'unemployment_rate'
        ORDER BY unit_name, year
    """)

    wages = query("""
        SELECT unit_name, year, value AS avg_wage
        FROM raw.bdl_labour
        WHERE variable_name = 'avg_wages'
        ORDER BY unit_name, year
    """)

    gdp = query("""
        SELECT unit_name, year, value / 1000.0 AS gdp_k
        FROM raw.bdl_labour
        WHERE variable_name = 'gdp_per_capita'
        ORDER BY unit_name, year
    """)

    latest_unemp_year = int(unemp.year.max())
    latest_wages_year = int(wages.year.max())
    latest_gdp_year   = int(gdp.year.max())

    unemp_latest = unemp[unemp.year == latest_unemp_year].sort_values("unemp_rate")
    wages_latest = wages[wages.year == latest_wages_year].sort_values("avg_wage")
    gdp_latest   = gdp[gdp.year == latest_gdp_year].sort_values("gdp_k")

    regions = sorted(unemp["unit_name"].unique().tolist())

    # National aggregates (simple mean across voivodships as proxy)
    nat_unemp = round(float(unemp_latest["unemp_rate"].mean()), 1)
    nat_wages = round(float(wages_latest["avg_wage"].mean()), 0)
    nat_gdp   = round(float(gdp_latest["gdp_k"].mean()), 1)

    min_unemp_region = unemp_latest.iloc[0]["unit_name"].title()
    max_unemp_region = unemp_latest.iloc[-1]["unit_name"].title()
    max_unemp_val    = round(float(unemp_latest.iloc[-1]["unemp_rate"]), 1)

    # Wage change YoY
    prev_wages_year = latest_wages_year - 1
    wages_prev = wages[wages.year == prev_wages_year]["avg_wage"].mean()
    wages_yoy  = round((nat_wages / wages_prev - 1) * 100, 1) if wages_prev else 0

    # ── KPIs ──────────────────────────────────────────────────────────────────
    kpis = "".join([
        kpi_card(f"Avg Unemployment {latest_unemp_year}", f"{nat_unemp}%",
                 f"Highest: {max_unemp_region} {max_unemp_val}%", "neu"),
        kpi_card(f"Avg Monthly Wage {latest_wages_year}", f"{int(nat_wages):,} PLN",
                 f"▲ {wages_yoy:+.1f}% YoY", "pos" if wages_yoy > 0 else "neg"),
        kpi_card(f"Avg GDP/capita {latest_gdp_year}", f"{nat_gdp:.1f}k PLN", "", "neu"),
        kpi_card("Lowest Unemployment", min_unemp_region.split()[0],
                 f"{round(float(unemp_latest.iloc[0]['unemp_rate']),1)}%", "pos"),
    ])

    # ── Chart 1: Unemployment comparison bar ──────────────────────────────────
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        y=unemp_latest.unit_name,
        x=unemp_latest.unemp_rate.round(1),
        orientation="h",
        marker_color=[
            C["green"] if v <= nat_unemp else (C["orange"] if v <= nat_unemp * 1.5 else C["red"])
            for v in unemp_latest.unemp_rate
        ],
        hovertemplate="<b>%{y}</b><br>Unemployment: %{x:.1f}%<extra></extra>",
    ))
    fig1.add_vline(x=nat_unemp, line_dash="dot", line_color=C["muted"],
                   annotation_text=f"avg {nat_unemp}%", annotation_font_color=C["muted"])
    apply(fig1, f"Registered Unemployment Rate {latest_unemp_year}",
          "By voivodship — green = below average, red = above 1.5× average", height=500)

    # ── Chart 2: Wages comparison bar ─────────────────────────────────────────
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        y=wages_latest.unit_name,
        x=wages_latest.avg_wage.round(0),
        orientation="h",
        marker_color=C["blue"],
        hovertemplate="<b>%{y}</b><br>Avg wage: %{x:,.0f} PLN<extra></extra>",
    ))
    fig2.add_vline(x=nat_wages, line_dash="dot", line_color=C["muted"],
                   annotation_text=f"avg {int(nat_wages):,} PLN", annotation_font_color=C["muted"])
    apply(fig2, f"Average Monthly Gross Wage {latest_wages_year}",
          "By voivodship (PLN)", height=500)

    # ── Chart 3: GDP per capita comparison ────────────────────────────────────
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        y=gdp_latest.unit_name,
        x=gdp_latest.gdp_k.round(1),
        orientation="h",
        marker_color=C["teal"],
        hovertemplate="<b>%{y}</b><br>GDP/capita: %{x:.1f}k PLN<extra></extra>",
    ))
    fig3.add_vline(x=nat_gdp, line_dash="dot", line_color=C["muted"],
                   annotation_text=f"avg {nat_gdp:.0f}k PLN", annotation_font_color=C["muted"])
    apply(fig3, f"GDP per Capita {latest_gdp_year}",
          "By voivodship (thousands PLN)", height=500)

    # ── Chart 4: Interactive region detail ────────────────────────────────────
    detail_data = {}
    for r in regions:
        u = unemp[unemp.unit_name == r].sort_values("year")
        w = wages[wages.unit_name == r].sort_values("year")
        g = gdp[gdp.unit_name == r].sort_values("year")
        detail_data[r] = {
            "u_years": u.year.tolist(),
            "u_vals":  u.unemp_rate.round(1).tolist(),
            "w_years": w.year.tolist(),
            "w_vals":  w.avg_wage.round(0).tolist(),
            "g_years": g.year.tolist(),
            "g_vals":  g.gdp_k.round(1).tolist(),
        }

    # ── Assemble HTML ──────────────────────────────────────────────────────────
    def div(fig):
        return pio.to_html(fig, include_plotlyjs=False, full_html=False,
                           config={"displayModeBar": True})

    options = "\n".join(f'<option value="{r}">{r}</option>' for r in regions)
    detail_js = f"const DETAIL = {json.dumps(detail_data)};"

    body = f"""
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<div class="charts">
  <div class="charts two-col" style="grid-column:1/-1">
    <div class="chart-card">{div(fig1)}</div>
    <div class="chart-card">{div(fig2)}</div>
  </div>
  <div class="chart-card full">{div(fig3)}</div>
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
const orange = "{C['orange']}";
const teal = "{C['teal']}";
const muted = "{C['muted']}";
const text = "{C['text']}";

function renderDetail(region) {{
  const d = DETAIL[region];
  const traces = [
    {{
      x: d.u_years, y: d.u_vals, name: 'Unemployment (%)',
      mode: 'lines+markers', line: {{ color: orange, width: 2 }}, marker: {{ size: 5 }},
      yaxis: 'y'
    }},
    {{
      x: d.w_years, y: d.w_vals, name: 'Avg Wage (PLN)',
      mode: 'lines+markers', line: {{ color: blue, width: 2 }}, marker: {{ size: 5 }},
      yaxis: 'y2'
    }},
    {{
      x: d.g_years, y: d.g_vals, name: 'GDP/capita (k PLN)',
      mode: 'lines+markers', line: {{ color: teal, width: 2, dash: 'dot' }}, marker: {{ size: 5 }},
      yaxis: 'y3'
    }},
  ];
  const layout = {{
    paper_bgcolor: bg, plot_bgcolor: surface,
    font: {{ family: 'Inter, system-ui, sans-serif', color: text, size: 12 }},
    height: 400, hovermode: 'x unified',
    legend: {{ bgcolor: surface, bordercolor: border, borderwidth: 1, font: {{ size: 11 }} }},
    margin: {{ l: 70, r: 120, t: 45, b: 40 }},
    title: {{ text: '<b>' + region + '</b> — Labour Market Trends', font: {{ size: 15 }}, x: 0.01 }},
    xaxis: {{ gridcolor: border, linecolor: border, tickfont: {{ color: muted }} }},
    yaxis: {{ gridcolor: border, linecolor: border, tickfont: {{ color: muted }},
              title: {{ text: 'Unemployment (%)', font: {{ color: orange, size: 11 }} }} }},
    yaxis2: {{ overlaying: 'y', side: 'right', gridcolor: 'transparent',
               linecolor: border, tickfont: {{ color: muted }},
               title: {{ text: 'Avg Wage (PLN)', font: {{ color: blue, size: 11 }} }} }},
    yaxis3: {{ overlaying: 'y', side: 'right', position: 0.97, gridcolor: 'transparent',
               linecolor: border, tickfont: {{ color: muted }},
               title: {{ text: 'GDP/capita (k PLN)', font: {{ color: teal, size: 11 }} }} }},
  }};
  Plotly.react('region-detail', traces, layout, {{ displayModeBar: false, responsive: true }});
}}

document.getElementById('region-select').addEventListener('change', function() {{
  renderDetail(this.value);
}});

renderDetail(document.getElementById('region-select').value);
</script>"""

    html = page(
        title="Polish Labour Market by Region",
        subtitle=f"16 voivodships — unemployment rate, wages, GDP per capita · Source: GUS BDL API",
        active="Labour Market",
        kpis=f'<div class="kpis">{kpis}</div>',
        body=body,
        source="GUS Bank Danych Lokalnych",
    )

    out = os.path.join(OUT, "labour_market.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓ labour_market.html")


if __name__ == "__main__":
    build()
