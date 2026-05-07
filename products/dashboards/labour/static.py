#!/usr/bin/env python3
"""
Dashboard: Rynek pracy w Polsce — dane regionalne
Source:    GUS BDL, curated.labour_market_regional
Output:    public/labour/rynek-pracy.html
"""
import json as json_mod
import logging
import os
from datetime import date

import plotly.graph_objects as go
from plotly.io import to_html

import complex_dashboard.assets.theme as theme  # noqa: F401 — registers 'nordic' template
from complex_dashboard.assets.data.db import query
from complex_dashboard.assets.theme import (
    AZURE_1, AZURE_3, BG_PAGE, BG_SURFACE, BORDER, COLORWAY,
    SUBTEXT, TEXT,
)

log = logging.getLogger(__name__)

OUTPUT_PATH = "infra/nginx/html/labour/rynek-pracy.html"

REGION_LABELS = {
    "DOLNOŚLĄSKIE":        "Dolnośląskie",
    "KUJAWSKO-POMORSKIE":  "Kujawsko-Pomorskie",
    "LUBELSKIE":           "Lubelskie",
    "LUBUSKIE":            "Lubuskie",
    "ŁÓDZKIE":             "Łódzkie",
    "MAŁOPOLSKIE":         "Małopolskie",
    "MAZOWIECKIE":         "Mazowieckie",
    "OPOLSKIE":            "Opolskie",
    "PODKARPACKIE":        "Podkarpackie",
    "PODLASKIE":           "Podlaskie",
    "POMORSKIE":           "Pomorskie",
    "ŚLĄSKIE":             "Śląskie",
    "ŚWIĘTOKRZYSKIE":      "Świętokrzyskie",
    "WARMIŃSKO-MAZURSKIE": "Warmińsko-Mazurskie",
    "WIELKOPOLSKIE":       "Wielkopolskie",
    "ZACHODNIOPOMORSKIE":  "Zachodniopomorskie",
}


def _label(region: str) -> str:
    return REGION_LABELS.get(region.upper(), region.title())


# ── Data ──────────────────────────────────────────────────────────────────────

def load_data():
    df = query("""
        SELECT region, year, unemployment_rate, avg_wages, gdp_per_capita
        FROM curated.labour_market_regional
        ORDER BY region, year
    """)
    df["region_label"] = df["region"].apply(_label)
    return df


def latest_year(df, col: str) -> int:
    return int(df[df[col].notna()]["year"].max())


def build_ranking_data(df) -> dict:
    """
    Pre-compute ranking data for every (metric, year) combination.
    Embedded as JSON for client-side ranking chart updates.
    """
    data = {}
    for metric, higher_is_better in [
        ("unemployment_rate", False),
        ("avg_wages", True),
        ("gdp_per_capita", True),
    ]:
        for yr in sorted(df["year"].unique()):
            sub = df[(df["year"] == yr) & df[metric].notna()].sort_values(metric)
            if sub.empty:
                continue
            values = [float(v) for v in sub[metric]]
            avg = sum(values) / len(values)
            data[f"{metric}_{yr}"] = {
                "regions": sub["region_label"].tolist(),
                "values": values,
                "avg": avg,
                "higher_is_better": higher_is_better,
            }
    return data


# ── Figures ───────────────────────────────────────────────────────────────────

def fig_trend(df, metric: str, title: str, ytitle: str, fmt: str) -> go.Figure:
    """Generic trend line chart — one trace per region, sorted alphabetically."""
    regions = sorted(df["region_label"].unique())
    fig = go.Figure()
    for i, region in enumerate(regions):
        sub = df[df["region_label"] == region].dropna(subset=[metric])
        fig.add_trace(go.Scatter(
            x=sub["year"],
            y=sub[metric],
            name=region,
            mode="lines",
            line=dict(color=COLORWAY[i % len(COLORWAY)], width=1.5),
            hovertemplate=f"<b>{region}</b><br>%{{x}}: %{{y:{fmt}}}<extra></extra>",
        ))
    fig.update_layout(
        title=title,
        xaxis_title=None,
        yaxis_title=ytitle,
        legend=dict(
            orientation="v", yanchor="top", y=1.0,
            xanchor="left", x=1.01, font=dict(size=11),
        ),
        margin=dict(l=60, r=160, t=48, b=40),
        height=400,
    )
    return fig


def fig_ranking(df, metric: str, title: str, xtitle: str,
                fmt_text, higher_is_better: bool) -> go.Figure:
    """Generic ranking bar chart for the latest available year."""
    yr = latest_year(df, metric)
    sub = df[(df["year"] == yr) & df[metric].notna()].sort_values(metric)
    avg = float(sub[metric].mean())

    def _color(v):
        return AZURE_1 if (higher_is_better == (v >= avg)) else AZURE_3

    fig = go.Figure(go.Bar(
        x=sub[metric].tolist(),
        y=sub["region_label"].tolist(),
        orientation="h",
        marker_color=[_color(v) for v in sub[metric]],
        text=[fmt_text(v) for v in sub[metric]],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>" + xtitle + ": %{x}<extra></extra>",
    ))
    fig.add_vline(
        x=avg, line_dash="dot", line_color=SUBTEXT, line_width=1.5,
        annotation_text=f"Średnia: {fmt_text(avg)}",
        annotation_position="top right",
        annotation_font_color=SUBTEXT,
        annotation_font_size=11,
    )
    fig.update_layout(
        title=f"{title} ({yr} r.)",
        xaxis_title=xtitle,
        yaxis_title=None,
        height=500,
        margin=dict(l=180, r=80, t=48, b=40),
    )
    return fig


# ── HTML helpers ──────────────────────────────────────────────────────────────

def _div(fig: go.Figure, div_id: str) -> str:
    return to_html(
        fig, div_id=div_id,
        include_plotlyjs=False, full_html=False,
        config={"displayModeBar": False, "responsive": True},
    )


def _card(content: str) -> str:
    return f'<div class="card">{content}</div>'


# ── Filter pane HTML ──────────────────────────────────────────────────────────

def _filter_pane(df) -> str:
    regions = sorted(df["region_label"].unique())
    checkboxes = "\n".join(
        f'      <label class="cb-label">'
        f'<input type="checkbox" class="region-cb" value="{r}" checked> {r}'
        f'</label>'
        for r in regions
    )

    trend_years = sorted(df["year"].unique())
    year_options = "\n".join(f'<option value="{y}">{y}</option>' for y in trend_years)

    ur_years  = sorted(df[df["unemployment_rate"].notna()]["year"].unique())
    wg_years  = sorted(df[df["avg_wages"].notna()]["year"].unique())
    gdp_years = sorted(df[df["gdp_per_capita"].notna()]["year"].unique())

    def _year_opts(years, selected=None):
        sel = selected or years[-1]
        return "\n".join(
            f'<option value="{y}" {"selected" if y == sel else ""}>{y}</option>'
            for y in years
        )

    return f"""
    <aside class="filter-pane" id="filter-pane">
      <div class="filter-section">
        <div class="filter-label">Województwa</div>
        <div class="filter-actions">
          <button class="btn-link" id="select-all">Zaznacz wszystkie</button>
          <span class="separator">·</span>
          <button class="btn-link" id="deselect-all">Odznacz wszystkie</button>
        </div>
        <div class="checkbox-list">
{checkboxes}
        </div>
      </div>

      <div class="filter-section">
        <div class="filter-label">Zakres lat — trendy</div>
        <div class="year-range">
          <div class="year-field">
            <label for="year-from">Od</label>
            <select id="year-from">{_year_opts(trend_years, trend_years[0])}</select>
          </div>
          <div class="year-field">
            <label for="year-to">Do</label>
            <select id="year-to">{_year_opts(trend_years, trend_years[-1])}</select>
          </div>
        </div>
      </div>

      <div class="filter-section">
        <div class="filter-label">Rok — rankingi</div>
        <select id="ranking-year-ur"  class="ranking-year-select" data-metric="unemployment_rate">
          {_year_opts(ur_years)}
        </select>
        <select id="ranking-year-wg"  class="ranking-year-select" data-metric="avg_wages">
          {_year_opts(wg_years)}
        </select>
        <select id="ranking-year-gdp" class="ranking-year-select" data-metric="gdp_per_capita">
          {_year_opts(gdp_years)}
        </select>
        <div class="ranking-year-labels">
          <label for="ranking-year-ur">Bezrobocie</label>
          <label for="ranking-year-wg">Wynagrodzenia</label>
          <label for="ranking-year-gdp">PKB per capita</label>
        </div>
      </div>
    </aside>
    """


# ── JavaScript ────────────────────────────────────────────────────────────────

def _js(regions_sorted: list, ranking_data: dict) -> str:
    regions_json   = json_mod.dumps(regions_sorted)
    ranking_json   = json_mod.dumps(ranking_data)
    azure1         = AZURE_1
    azure3         = AZURE_3
    subtext_color  = SUBTEXT

    return f"""
<script>
(function () {{
  const REGIONS       = {regions_json};
  const RANKING_DATA  = {ranking_json};
  const AZURE_1       = "{azure1}";
  const AZURE_3       = "{azure3}";
  const SUBTEXT       = "{subtext_color}";

  const TREND_CHARTS   = ["chart-ur-trend", "chart-wg-trend"];
  const RANKING_CONFIG = [
    {{ divId: "chart-ur-rank",  selectId: "ranking-year-ur",  metric: "unemployment_rate" }},
    {{ divId: "chart-wg-rank",  selectId: "ranking-year-wg",  metric: "avg_wages" }},
    {{ divId: "chart-gdp-rank", selectId: "ranking-year-gdp", metric: "gdp_per_capita" }},
  ];

  // ── Helpers ────────────────────────────────────────────────────────────────

  function selectedRegions() {{
    return Array.from(document.querySelectorAll(".region-cb:checked")).map(cb => cb.value);
  }}

  function fmtValue(metric, v) {{
    if (metric === "unemployment_rate") return v.toFixed(1) + "%";
    return v.toLocaleString("pl-PL", {{maximumFractionDigits: 0}}) + " zł";
  }}

  // ── Trend charts ───────────────────────────────────────────────────────────

  function applyTrendFilters() {{
    const selected = selectedRegions();
    const fromY = parseInt(document.getElementById("year-from").value);
    const toY   = parseInt(document.getElementById("year-to").value);

    // Show/hide traces by region (traces are in sorted REGIONS order)
    const visibility = REGIONS.map(r => selected.includes(r) ? true : "legendonly");

    TREND_CHARTS.forEach(id => {{
      Plotly.restyle(id, {{ visible: visibility }});
      Plotly.relayout(id, {{ "xaxis.range": [fromY - 0.5, toY + 0.5] }});
    }});
  }}

  // ── Ranking charts ─────────────────────────────────────────────────────────

  function applyRankingFilter(cfg) {{
    const yr       = parseInt(document.getElementById(cfg.selectId).value);
    const selected = selectedRegions();
    const key      = cfg.metric + "_" + yr;
    const src      = RANKING_DATA[key];
    if (!src) return;

    // Filter to selected regions, keep sorted order
    const rows = src.regions
      .map((r, i) => ({{ r, v: src.values[i] }}))
      .filter(x => selected.includes(x.r));

    if (rows.length === 0) return;

    const regions = rows.map(x => x.r);
    const values  = rows.map(x => x.v);
    const avg     = values.reduce((a, b) => a + b, 0) / values.length;
    const colors  = values.map(v =>
      src.higher_is_better === (v >= avg) ? AZURE_1 : AZURE_3
    );
    const texts = values.map(v => fmtValue(cfg.metric, v));

    const chartDiv = document.getElementById(cfg.divId);
    const layout   = chartDiv.layout;

    // Update trace data
    Plotly.restyle(cfg.divId, {{
      x: [values],
      y: [regions],
      "marker.color": [colors],
      text: [texts],
    }}, [0]);

    // Update average line + annotation + title
    const newTitle = layout.title.text.replace(/\\(\\d{{4}} r\\.\\)/, "(" + yr + " r.)");
    const fmtAvg   = fmtValue(cfg.metric, avg);
    Plotly.relayout(cfg.divId, {{
      "title.text": newTitle,
      shapes: [{{
        type: "line",
        x0: avg, x1: avg,
        y0: -0.5, y1: regions.length - 0.5,
        xref: "x", yref: "y",
        line: {{ color: SUBTEXT, width: 1.5, dash: "dot" }},
      }}],
      annotations: [{{
        x: avg, y: regions.length - 0.5,
        xref: "x", yref: "y",
        text: "Średnia: " + fmtAvg,
        showarrow: false,
        xanchor: "left",
        font: {{ color: SUBTEXT, size: 11 }},
      }}],
    }});
  }}

  function applyAllRankings() {{
    RANKING_CONFIG.forEach(applyRankingFilter);
  }}

  // ── Event wiring ───────────────────────────────────────────────────────────

  document.getElementById("select-all").addEventListener("click", () => {{
    document.querySelectorAll(".region-cb").forEach(cb => cb.checked = true);
    applyTrendFilters();
    applyAllRankings();
  }});

  document.getElementById("deselect-all").addEventListener("click", () => {{
    document.querySelectorAll(".region-cb").forEach(cb => cb.checked = false);
    applyTrendFilters();
    applyAllRankings();
  }});

  document.querySelectorAll(".region-cb").forEach(cb => {{
    cb.addEventListener("change", () => {{
      applyTrendFilters();
      applyAllRankings();
    }});
  }});

  document.getElementById("year-from").addEventListener("change", applyTrendFilters);
  document.getElementById("year-to").addEventListener("change",   applyTrendFilters);

  RANKING_CONFIG.forEach(cfg => {{
    document.getElementById(cfg.selectId).addEventListener("change", () => applyRankingFilter(cfg));
  }});
}})();
</script>
"""


# ── Page assembly ─────────────────────────────────────────────────────────────

def build_html(df) -> str:
    updated       = date.today().strftime("%-d %B %Y")
    regions_sorted = sorted(df["region_label"].unique().tolist())
    ranking_data  = build_ranking_data(df)

    # ── Figures ────────────────────────────────────────────────────────────────
    ur_trend  = _div(fig_trend(df, "unemployment_rate",
                               "Stopa bezrobocia rejestrowanego według województw (%)",
                               "Stopa bezrobocia (%)", ".1f%"),
                     "chart-ur-trend")
    wg_trend  = _div(fig_trend(df, "avg_wages",
                               "Przeciętne miesięczne wynagrodzenie brutto według województw",
                               "Wynagrodzenie brutto (zł)", ",.0f"),
                     "chart-wg-trend")
    ur_rank   = _div(fig_ranking(df, "unemployment_rate",
                                 "Ranking województw — stopa bezrobocia",
                                 "Stopa bezrobocia (%)",
                                 lambda v: f"{v:.1f}%", False),
                     "chart-ur-rank")
    wg_rank   = _div(fig_ranking(df, "avg_wages",
                                 "Ranking województw — przeciętne wynagrodzenie brutto",
                                 "Wynagrodzenie brutto (zł)",
                                 lambda v: f"{v:,.0f} zł", True),
                     "chart-wg-rank")
    gdp_rank  = _div(fig_ranking(df, "gdp_per_capita",
                                 "Ranking województw — PKB per capita",
                                 "PKB per capita (zł)",
                                 lambda v: f"{v:,.0f} zł", True),
                     "chart-gdp-rank")

    filter_pane = _filter_pane(df)
    js          = _js(regions_sorted, ranking_data)

    sections = f"""
      <section class="topic-group">
        <h2 class="group-label">Bezrobocie</h2>
        <div class="grid grid-2">
          {_card(ur_trend)}
          {_card(ur_rank)}
        </div>
      </section>

      <section class="topic-group">
        <h2 class="group-label">Wynagrodzenia</h2>
        <div class="grid grid-2">
          {_card(wg_trend)}
          {_card(wg_rank)}
        </div>
      </section>

      <section class="topic-group">
        <h2 class="group-label">Produkt Krajowy Brutto</h2>
        <div class="grid grid-1">
          {_card(gdp_rank)}
        </div>
      </section>
    """

    return f"""<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Rynek pracy w Polsce — Otwarte Raporty</title>
  <script src="https://cdn.plot.ly/plotly-3.0.0.min.js"></script>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: Inter, 'Segoe UI', system-ui, -apple-system, Helvetica, Arial, sans-serif;
      background: {BG_PAGE};
      color: {TEXT};
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}

    /* ── Header ── */
    header {{
      background: {BG_SURFACE};
      border-bottom: 1px solid {BORDER};
      padding: 16px 32px;
      display: flex;
      align-items: baseline;
      gap: 24px;
      flex-shrink: 0;
    }}
    .site-name {{
      font-size: 15px; font-weight: 600;
      color: {TEXT}; text-decoration: none;
    }}
    header nav a {{
      font-size: 13px; color: {SUBTEXT};
      text-decoration: none; margin-right: 16px;
    }}
    header nav a:hover {{ color: {TEXT}; }}

    /* ── Page title ── */
    .page-header {{
      background: {BG_SURFACE};
      border-bottom: 1px solid {BORDER};
      padding: 24px 32px 20px;
      flex-shrink: 0;
    }}
    .page-header h1 {{
      font-size: 24px; font-weight: 700; color: {TEXT}; margin-bottom: 4px;
    }}
    .page-header p {{ font-size: 13px; color: {SUBTEXT}; }}

    /* ── Body layout: filter pane + main ── */
    .body-layout {{
      display: flex;
      flex: 1;
      min-height: 0;
    }}

    /* ── Filter pane (220px, sticky) ── */
    .filter-pane {{
      width: 220px;
      flex-shrink: 0;
      background: {BG_SURFACE};
      border-right: 1px solid {BORDER};
      padding: 20px 16px;
      position: sticky;
      top: 0;
      height: 100vh;
      overflow-y: auto;
    }}
    .filter-section {{
      margin-bottom: 24px;
    }}
    .filter-label {{
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      color: {SUBTEXT};
      margin-bottom: 10px;
    }}
    .filter-actions {{
      display: flex;
      align-items: center;
      gap: 4px;
      margin-bottom: 8px;
    }}
    .btn-link {{
      background: none; border: none; padding: 0;
      font-size: 11px; color: {SUBTEXT};
      cursor: pointer; text-decoration: underline;
    }}
    .btn-link:hover {{ color: {TEXT}; }}
    .separator {{ font-size: 11px; color: {SUBTEXT}; }}

    .checkbox-list {{
      display: flex;
      flex-direction: column;
      gap: 5px;
      max-height: 340px;
      overflow-y: auto;
    }}
    .cb-label {{
      display: flex;
      align-items: center;
      gap: 7px;
      font-size: 12px;
      color: {TEXT};
      cursor: pointer;
      line-height: 1.3;
    }}
    .cb-label input {{ cursor: pointer; accent-color: {AZURE_1}; }}

    .year-range {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }}
    .year-field {{
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}
    .year-field label, .ranking-year-labels label {{
      font-size: 11px;
      color: {SUBTEXT};
    }}
    select {{
      width: 100%;
      font-size: 12px;
      color: {TEXT};
      background: {BG_PAGE};
      border: 1px solid {BORDER};
      border-radius: 4px;
      padding: 4px 6px;
      cursor: pointer;
    }}
    select:focus {{ outline: 2px solid {AZURE_1}; outline-offset: 1px; }}

    .ranking-year-select {{ margin-bottom: 4px; }}
    .ranking-year-labels {{
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}

    /* ── Main canvas ── */
    main {{
      flex: 1;
      padding: 28px 24px 56px;
      overflow-x: hidden;
      min-width: 0;
    }}

    /* ── Topic groups ── */
    .topic-group {{ margin-bottom: 36px; }}
    .group-label {{
      font-size: 11px; font-weight: 600;
      text-transform: uppercase; letter-spacing: 0.08em;
      color: {SUBTEXT};
      margin-bottom: 14px; padding-bottom: 8px;
      border-bottom: 1px solid {BORDER};
    }}

    /* ── Grid ── */
    .grid {{ display: grid; gap: 20px; }}
    .grid-2 {{ grid-template-columns: 1fr 1fr; }}
    .grid-1 {{ grid-template-columns: 1fr; }}
    @media (max-width: 1100px) {{
      .grid-2 {{ grid-template-columns: 1fr; }}
    }}

    /* ── Cards ── */
    .card {{
      background: {BG_SURFACE};
      border-radius: 6px;
      box-shadow: 0 1px 4px rgba(0,0,0,0.07), 0 0 1px rgba(0,0,0,0.04);
      padding: 16px;
      overflow: hidden;
    }}

    /* ── Footer ── */
    footer {{
      background: {BG_SURFACE};
      border-top: 1px solid {BORDER};
      padding: 16px 32px;
      font-size: 12px; color: {SUBTEXT};
      display: flex; justify-content: space-between;
      align-items: center; flex-wrap: wrap; gap: 8px;
      flex-shrink: 0;
    }}
    footer a {{ color: {SUBTEXT}; }}
  </style>
</head>
<body>

<header>
  <a class="site-name" href="/">Otwarte Raporty</a>
  <nav><a href="/labour/rynek-pracy.html">Rynek pracy</a></nav>
</header>

<div class="page-header">
  <h1>Rynek pracy w Polsce</h1>
  <p>Bezrobocie, wynagrodzenia i PKB per capita według województw · dane GUS BDL</p>
</div>

<div class="body-layout">
  {filter_pane}
  <main>{sections}</main>
</div>

<footer>
  <span>Dane: GUS BDL (Bank Danych Lokalnych) — aktualizacja: {updated}</span>
  <span>
    <a href="https://bdl.stat.gov.pl/">bdl.stat.gov.pl</a> ·
    <a href="/">portal.open-reporting.dev</a>
  </span>
</footer>

{js}
</body>
</html>"""


# ── Entry point ───────────────────────────────────────────────────────────────

def generate() -> None:
    log.info("Loading data...")
    df = load_data()
    log.info("Building HTML...")
    html = build_html(df)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    log.info("Written: %s (%d bytes)", OUTPUT_PATH, len(html))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    generate()
