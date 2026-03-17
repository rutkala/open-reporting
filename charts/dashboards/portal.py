"""Portal landing page — links to all dashboards."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.theme import C, PAGE_CSS, NAV_LINKS

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "charts")

DASHBOARDS = [
    {
        "href": "state_budget.html",
        "icon": "📊",
        "title": "Polish State Budget",
        "subtitle": "2008–2024",
        "desc": "Revenues, expenditures, deficit and fiscal pressure ratio. Annual central government budget execution data.",
        "tags": ["Fiscal", "NIK / MF"],
    },
    {
        "href": "voivodship.html",
        "icon": "🗺️",
        "title": "Regional Budgets",
        "subtitle": "1999–2024",
        "desc": "All 16 Polish voivodships. Budget trends, regional comparison, surplus/deficit heatmap and interactive region selector.",
        "tags": ["Regional", "GUS BDL"],
    },
    {
        "href": "labour_market.html",
        "icon": "👷",
        "title": "Labour Market",
        "subtitle": "2002–2025",
        "desc": "Unemployment rate, average wages, and GDP per capita across all 16 voivodships. Regional comparison and historical trends.",
        "tags": ["Labour", "GUS BDL"],
    },
    {
        "href": "gpw_market.html",
        "icon": "📈",
        "title": "GPW Stock Market",
        "subtitle": "1992–today",
        "desc": "WIG20, mWIG40, sWIG80 — indexed performance, sector YTD returns, top movers and interactive stock detail charts.",
        "tags": ["Equities", "stooq.com"],
    },
]


def build():
    cards = "\n".join(f"""
    <a href="{d['href']}" class="dash-card">
      <div class="dash-icon">{d['icon']}</div>
      <div class="dash-body">
        <div class="dash-header">
          <h3>{d['title']}</h3>
          <span class="dash-period">{d['subtitle']}</span>
        </div>
        <p>{d['desc']}</p>
        <div class="dash-tags">{''.join(f'<span class="tag">{t}</span>' for t in d['tags'])}</div>
      </div>
    </a>""" for d in DASHBOARDS)

    nav_links = "\n".join(
        f'<a href="{href}">{label}</a>'
        for href, label in NAV_LINKS[1:]
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Open Reporting — Analytics Portal</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
{PAGE_CSS}
<style>
.hero {{ padding: 3.5rem 2rem 2.5rem; border-bottom: 1px solid var(--border); }}
.hero h1 {{ font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem; }}
.hero h1 span {{ color: var(--blue); }}
.hero p {{ color: var(--muted); font-size: 0.95rem; max-width: 560px; line-height: 1.6; }}
.dashboards {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
               gap: 1rem; padding: 2rem; max-width: 1400px; margin: 0 auto; }}
.dash-card {{
  display: flex; gap: 1.25rem; align-items: flex-start;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 12px; padding: 1.5rem;
  text-decoration: none; color: inherit;
  transition: border-color 0.15s, transform 0.1s, box-shadow 0.15s;
}}
.dash-card:hover {{
  border-color: var(--blue); transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}}
.dash-icon {{ font-size: 2rem; flex-shrink: 0; margin-top: 0.1rem; }}
.dash-body {{ flex: 1; }}
.dash-header {{ display: flex; align-items: baseline; gap: 0.75rem; margin-bottom: 0.5rem; }}
.dash-header h3 {{ font-size: 1rem; font-weight: 700; }}
.dash-period {{ font-size: 0.75rem; color: var(--muted); }}
.dash-body p {{ font-size: 0.83rem; color: var(--muted); line-height: 1.5; margin-bottom: 0.75rem; }}
.dash-tags {{ display: flex; gap: 0.4rem; flex-wrap: wrap; }}
.tag {{ font-size: 0.7rem; padding: 0.2rem 0.5rem; background: var(--card);
         border: 1px solid var(--border); border-radius: 4px; color: var(--muted); }}
footer {{ text-align: center; color: var(--muted); font-size: 0.75rem;
           padding: 2rem; border-top: 1px solid var(--border); }}
</style>
</head>
<body>
<nav>
  <a class="logo" href="/"><b>Open <span>Reporting</span></b></a>
  {nav_links}
</nav>
<div class="hero">
  <div style="max-width:1400px;margin:0 auto">
    <h1>Open <span>Reporting</span></h1>
    <p>Polish economic and market data — interactive analytics dashboards covering public finances and the Warsaw Stock Exchange.</p>
  </div>
</div>
<div class="dashboards">
  {cards}
</div>
<footer>Data sources: GUS BDL · NIK · Ministerstwo Finansów · stooq.com · Charts built with Python + Plotly</footer>
</body>
</html>"""

    out = os.path.join(OUT, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("  ✓ index.html")


if __name__ == "__main__":
    build()
