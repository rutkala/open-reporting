"""Shared visual theme for all dashboards."""
import plotly.graph_objects as go

C = {
    "bg":      "#0F172A",
    "surface": "#1E293B",
    "card":    "#263148",
    "border":  "#334155",
    "text":    "#F1F5F9",
    "muted":   "#94A3B8",
    "blue":    "#3B82F6",
    "green":   "#22C55E",
    "red":     "#EF4444",
    "yellow":  "#EAB308",
    "orange":  "#F97316",
    "purple":  "#A855F7",
    "teal":    "#14B8A6",
}

AXIS = dict(
    gridcolor=C["border"],
    linecolor=C["border"],
    zerolinecolor=C["border"],
    tickfont=dict(color=C["muted"], size=11),
    title_font=dict(color=C["muted"], size=12),
)

LAYOUT = dict(
    paper_bgcolor=C["bg"],
    plot_bgcolor=C["surface"],
    font=dict(family="Inter, system-ui, sans-serif", color=C["text"], size=13),
    margin=dict(l=60, r=30, t=60, b=50),
    legend=dict(
        bgcolor=C["surface"],
        bordercolor=C["border"],
        borderwidth=1,
        font=dict(size=11),
    ),
    hovermode="x unified",
    hoverlabel=dict(bgcolor=C["card"], bordercolor=C["border"], font_size=12),
)

PALETTE = [C["blue"], C["green"], C["orange"], C["purple"],
           C["teal"], C["yellow"], C["red"], "#EC4899", "#6366F1", "#0EA5E9"]


def apply(fig: go.Figure, title: str, subtitle: str = "", height: int = 420, **kwargs):
    full = f"<b>{title}</b>"
    if subtitle:
        full += f"<br><span style='font-size:11px;color:{C['muted']}'>{subtitle}</span>"
    fig.update_layout(
        **LAYOUT,
        title=dict(text=full, font=dict(size=16), x=0.01, y=0.97),
        height=height,
        **kwargs,
    )
    fig.update_xaxes(**AXIS)
    fig.update_yaxes(**AXIS)
    return fig


def save(fig: go.Figure, path: str):
    fig.write_html(path, include_plotlyjs="cdn", full_html=False)


# ── HTML page wrapper ──────────────────────────────────────────────────────────
PAGE_CSS = f"""
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{
  --bg: {C['bg']}; --surface: {C['surface']}; --card: {C['card']};
  --border: {C['border']}; --text: {C['text']}; --muted: {C['muted']};
  --blue: {C['blue']}; --green: {C['green']}; --red: {C['red']};
}}
body {{ background: var(--bg); color: var(--text);
        font-family: Inter, system-ui, sans-serif; min-height: 100vh; }}
nav {{ display: flex; align-items: center; gap: 2rem; padding: 0.9rem 2rem;
       background: var(--surface); border-bottom: 1px solid var(--border);
       position: sticky; top: 0; z-index: 100; }}
nav .logo {{ font-size: 1rem; font-weight: 700; color: var(--text); text-decoration: none; }}
nav .logo span {{ color: var(--blue); }}
nav a {{ font-size: 0.82rem; color: var(--muted); text-decoration: none;
          padding: 0.3rem 0.7rem; border-radius: 5px; transition: all 0.15s; }}
nav a:hover, nav a.active {{ color: var(--text); background: var(--card); }}
.page {{ max-width: 1400px; margin: 0 auto; padding: 1.5rem 2rem 3rem; }}
h1 {{ font-size: 1.5rem; font-weight: 700; margin-bottom: 0.3rem; }}
.subtitle {{ color: var(--muted); font-size: 0.88rem; margin-bottom: 1.5rem; }}
.kpis {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
          gap: 0.75rem; margin-bottom: 1.5rem; }}
.kpi {{ background: var(--card); border: 1px solid var(--border);
         border-radius: 10px; padding: 1rem 1.25rem; }}
.kpi .label {{ font-size: 0.75rem; color: var(--muted); text-transform: uppercase;
                letter-spacing: 0.05em; margin-bottom: 0.35rem; }}
.kpi .value {{ font-size: 1.6rem; font-weight: 700; line-height: 1; }}
.kpi .delta {{ font-size: 0.78rem; margin-top: 0.3rem; }}
.kpi .delta.pos {{ color: var(--green); }}
.kpi .delta.neg {{ color: var(--red); }}
.kpi .delta.neu {{ color: var(--muted); }}
.charts {{ display: grid; gap: 1rem; }}
.chart-card {{ background: var(--surface); border: 1px solid var(--border);
               border-radius: 10px; padding: 0.5rem; overflow: hidden; }}
.chart-card.full {{ grid-column: 1 / -1; }}
.two-col {{ grid-template-columns: 1fr 1fr; }}
.controls {{ display: flex; gap: 0.75rem; align-items: center; flex-wrap: wrap;
              margin-bottom: 1rem; }}
.controls label {{ font-size: 0.8rem; color: var(--muted); }}
.controls select {{
  background: var(--card); color: var(--text); border: 1px solid var(--border);
  border-radius: 6px; padding: 0.35rem 0.6rem; font-size: 0.82rem; cursor: pointer;
}}
footer {{ text-align: center; color: var(--muted); font-size: 0.75rem;
           padding: 2rem; border-top: 1px solid var(--border); margin-top: 2rem; }}
@media (max-width: 768px) {{ .two-col {{ grid-template-columns: 1fr; }} nav {{ gap: 1rem; }} }}
</style>
"""

NAV_LINKS = [
    ("portal.open-reporting.dev/", "Portal"),
    ("state_budget.html", "State Budget"),
    ("voivodship.html", "Regional Budgets"),
    ("labour_market.html", "Labour Market"),
    ("gpw_market.html", "GPW Market"),
]


def nav(active: str = "") -> str:
    links = "\n".join(
        f'<a href="{href}" class="{"active" if label == active else ""}">{label}</a>'
        for href, label in NAV_LINKS
    )
    return f"""
<nav>
  <a class="logo" href="/"><Open <span>Reporting</span></a>
  {links}
</nav>"""


def page(title: str, subtitle: str, active: str, kpis: str, body: str,
         source: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · Open Reporting</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
{PAGE_CSS}
</head>
<body>
{nav(active)}
<div class="page">
  <h1>{title}</h1>
  <p class="subtitle">{subtitle}</p>
  {kpis}
  {body}
</div>
<footer>Sources: {source} · portal.open-reporting.dev</footer>
</body>
</html>"""


def kpi_card(label: str, value: str, delta: str = "", delta_class: str = "neu") -> str:
    delta_html = f'<div class="delta {delta_class}">{delta}</div>' if delta else ""
    return f"""
<div class="kpi">
  <div class="label">{label}</div>
  <div class="value">{value}</div>
  {delta_html}
</div>"""
