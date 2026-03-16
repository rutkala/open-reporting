#!/usr/bin/env python3
"""
Generate standalone Plotly HTML charts from PostgreSQL.
Outputs to /opt/open-reporting/charts/

Usage:
    POSTGRES_PASSWORD=xxx python3 scripts/generate_charts.py
    or with .env:
    python3 scripts/generate_charts.py
"""

import os
import psycopg2
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from dotenv import load_dotenv

load_dotenv()

DB = dict(
    host=os.environ.get("POSTGRES_HOST", "localhost"),
    port=int(os.environ.get("POSTGRES_PORT", "5432")),
    dbname=os.environ.get("POSTGRES_DB", "reporting"),
    user=os.environ.get("POSTGRES_USER", "reporting"),
    password=os.environ["POSTGRES_PASSWORD"],
)

OUT = "/opt/open-reporting/charts"
os.makedirs(OUT, exist_ok=True)

COLORS = {
    "blue":   "#3B82F6",
    "red":    "#EF4444",
    "green":  "#22C55E",
    "yellow": "#EAB308",
    "purple": "#A855F7",
    "gray":   "#6B7280",
    "orange": "#F97316",
    "teal":   "#14B8A6",
    "bg":     "#0F172A",
    "surface":"#1E293B",
    "border": "#334155",
    "text":   "#F1F5F9",
    "muted":  "#94A3B8",
}

LAYOUT_BASE = dict(
    paper_bgcolor=COLORS["bg"],
    plot_bgcolor=COLORS["surface"],
    font=dict(family="Inter, system-ui, sans-serif", color=COLORS["text"], size=13),
    margin=dict(l=60, r=40, t=70, b=60),
    legend=dict(
        bgcolor=COLORS["surface"],
        bordercolor=COLORS["border"],
        borderwidth=1,
    ),
    xaxis=dict(gridcolor=COLORS["border"], linecolor=COLORS["border"], zerolinecolor=COLORS["border"]),
    yaxis=dict(gridcolor=COLORS["border"], linecolor=COLORS["border"], zerolinecolor=COLORS["border"]),
)


def conn():
    return psycopg2.connect(**DB)


def save(fig, filename, title):
    path = os.path.join(OUT, filename)
    fig.write_html(path, include_plotlyjs="cdn", full_html=True)
    print(f"  ✓ {filename}")


def apply_layout(fig, title, subtitle=None, **kwargs):
    full_title = f"<b>{title}</b>"
    if subtitle:
        full_title += f"<br><span style='font-size:12px;color:{COLORS['muted']}'>{subtitle}</span>"
    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(text=full_title, font=dict(size=18), x=0.02),
        **kwargs,
    )
    return fig


# ─────────────────────────────────────────────────────────────
# 1. STATE BUDGET: Revenues vs Expenditures
# ─────────────────────────────────────────────────────────────
def chart_national_budget_overview():
    with conn() as c:
        df = pd.read_sql("SELECT * FROM national_budget ORDER BY year", c)

    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.65, 0.35],
        shared_xaxes=True,
        vertical_spacing=0.08,
        subplot_titles=["Revenues & Expenditures (bn PLN)", "Deficit (bn PLN)"],
    )

    fig.add_trace(go.Scatter(
        x=df["year"], y=df["revenues_bn"],
        name="Revenues", mode="lines+markers",
        line=dict(color=COLORS["blue"], width=2.5),
        marker=dict(size=6),
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=df["year"], y=df["expenditures_bn"],
        name="Expenditures", mode="lines+markers",
        line=dict(color=COLORS["red"], width=2.5),
        marker=dict(size=6),
    ), row=1, col=1)

    fig.add_trace(go.Bar(
        x=df["year"], y=df["deficit_bn"].abs(),
        name="Deficit",
        marker_color=[COLORS["yellow"] if v < 50 else COLORS["red"] for v in df["deficit_bn"].abs()],
        text=df["deficit_bn"].abs().round(1),
        textposition="outside",
    ), row=2, col=1)

    apply_layout(fig,
        "Polish State Budget 2008–2024",
        "Central government revenues, expenditures and deficit · Source: NIK / MF",
    )
    fig.update_layout(height=620, hovermode="x unified")
    for i in [1, 2]:
        fig.update_xaxes(row=i, col=1, **LAYOUT_BASE["xaxis"])
        fig.update_yaxes(row=i, col=1, **LAYOUT_BASE["yaxis"])

    save(fig, "national_budget_overview.html", "State Budget Overview")


# ─────────────────────────────────────────────────────────────
# 2. STATE BUDGET: Deficit % of Revenues
# ─────────────────────────────────────────────────────────────
def chart_national_budget_deficit_pct():
    with conn() as c:
        df = pd.read_sql("SELECT * FROM national_budget ORDER BY year", c)

    df["deficit_pct"] = (df["deficit_bn"].abs() / df["revenues_bn"] * 100).round(1)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["year"],
        y=df["deficit_pct"],
        marker_color=[COLORS["green"] if v < 10 else COLORS["yellow"] if v < 20 else COLORS["red"] for v in df["deficit_pct"]],
        text=df["deficit_pct"].astype(str) + "%",
        textposition="outside",
    ))
    fig.add_hline(y=10, line_dash="dot", line_color=COLORS["muted"],
                  annotation_text="10% threshold", annotation_position="top right")

    apply_layout(fig,
        "Deficit as % of Revenues 2008–2024",
        "Fiscal pressure ratio — deficit divided by total revenues · Source: NIK / MF",
    )
    fig.update_layout(height=480, showlegend=False)
    fig.update_yaxes(ticksuffix="%", **LAYOUT_BASE["yaxis"])

    save(fig, "national_budget_deficit_pct.html", "Deficit % of Revenues")


# ─────────────────────────────────────────────────────────────
# 3. VOIVODSHIP BUDGETS: National aggregate trend
# ─────────────────────────────────────────────────────────────
def chart_voivodship_aggregate():
    with conn() as c:
        df = pd.read_sql("""
            SELECT
                year,
                variable_name,
                SUM(value) / 1e9 AS total_bn
            FROM raw.bdl_budget
            WHERE variable_name IN ('revenues', 'expenditures')
            GROUP BY year, variable_name
            ORDER BY year
        """, c)

    rev = df[df["variable_name"] == "revenues"]
    exp = df[df["variable_name"] == "expenditures"]
    bal = rev.set_index("year")["total_bn"] - exp.set_index("year")["total_bn"]

    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.65, 0.35],
        shared_xaxes=True,
        vertical_spacing=0.08,
        subplot_titles=["Total Revenues & Expenditures (bn PLN)", "Budget Balance (bn PLN)"],
    )

    fig.add_trace(go.Scatter(
        x=rev["year"], y=rev["total_bn"].round(2),
        name="Revenues", mode="lines+markers",
        line=dict(color=COLORS["blue"], width=2.5),
        marker=dict(size=6),
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=exp["year"], y=exp["total_bn"].round(2),
        name="Expenditures", mode="lines+markers",
        line=dict(color=COLORS["red"], width=2.5),
        marker=dict(size=6),
    ), row=1, col=1)

    fig.add_trace(go.Bar(
        x=bal.index,
        y=bal.round(2),
        name="Balance",
        marker_color=[COLORS["green"] if v >= 0 else COLORS["red"] for v in bal],
    ), row=2, col=1)

    apply_layout(fig,
        "Polish Voivodship Budgets 1999–2024",
        "Aggregate of all 16 regional budgets · Source: GUS BDL",
    )
    fig.update_layout(height=620, hovermode="x unified")
    for i in [1, 2]:
        fig.update_xaxes(row=i, col=1, **LAYOUT_BASE["xaxis"])
        fig.update_yaxes(row=i, col=1, **LAYOUT_BASE["yaxis"])

    save(fig, "voivodship_aggregate.html", "Voivodship Budget Aggregate")


# ─────────────────────────────────────────────────────────────
# 4. VOIVODSHIP BUDGETS: Revenues by region (2024)
# ─────────────────────────────────────────────────────────────
def chart_voivodship_2024_comparison():
    with conn() as c:
        df = pd.read_sql("""
            SELECT
                unit_name,
                MAX(CASE WHEN variable_name = 'revenues'     THEN value / 1e9 END) AS revenues_bn,
                MAX(CASE WHEN variable_name = 'expenditures' THEN value / 1e9 END) AS expenditures_bn
            FROM raw.bdl_budget
            WHERE year = 2024
            GROUP BY unit_name
            ORDER BY revenues_bn DESC
        """, c)

    df["balance_bn"] = (df["revenues_bn"] - df["expenditures_bn"]).round(2)
    df = df.sort_values("revenues_bn")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df["unit_name"], x=df["revenues_bn"].round(2),
        name="Revenues", orientation="h",
        marker_color=COLORS["blue"],
    ))
    fig.add_trace(go.Bar(
        y=df["unit_name"], x=df["expenditures_bn"].round(2),
        name="Expenditures", orientation="h",
        marker_color=COLORS["red"], opacity=0.7,
    ))

    apply_layout(fig,
        "Voivodship Budget Revenues — 2024",
        "Total revenues and expenditures per region in bn PLN · Source: GUS BDL",
    )
    fig.update_layout(height=560, barmode="overlay")
    fig.update_xaxes(title_text="bn PLN", **LAYOUT_BASE["xaxis"])

    save(fig, "voivodship_2024_comparison.html", "Voivodship Comparison 2024")


# ─────────────────────────────────────────────────────────────
# 5. VOIVODSHIP: Budget balance heatmap by region & year
# ─────────────────────────────────────────────────────────────
def chart_voivodship_balance_heatmap():
    with conn() as c:
        df = pd.read_sql("""
            SELECT
                unit_name,
                year,
                SUM(CASE WHEN variable_name = 'revenues'     THEN value ELSE 0 END) -
                SUM(CASE WHEN variable_name = 'expenditures' THEN value ELSE 0 END) AS balance
            FROM raw.bdl_budget
            GROUP BY unit_name, year
            ORDER BY unit_name, year
        """, c)

    pivot = df.pivot(index="unit_name", columns="year", values="balance") / 1e6  # to millions PLN

    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale=[[0, COLORS["red"]], [0.5, COLORS["surface"]], [1, COLORS["green"]]],
        zmid=0,
        colorbar=dict(title="mn PLN", tickfont=dict(color=COLORS["text"])),
        hovertemplate="<b>%{y}</b><br>Year: %{x}<br>Balance: %{z:.0f} mn PLN<extra></extra>",
    ))

    apply_layout(fig,
        "Voivodship Budget Balance Heatmap 1999–2024",
        "Green = surplus, Red = deficit · Values in million PLN · Source: GUS BDL",
    )
    fig.update_layout(height=520)

    save(fig, "voivodship_balance_heatmap.html", "Voivodship Balance Heatmap")


# ─────────────────────────────────────────────────────────────
# 6. STOCK MARKET: WIG20 — normalized price performance
# ─────────────────────────────────────────────────────────────
def chart_wig20_performance():
    WIG20 = ["PKO", "PEO", "CDR", "PKN", "PZU", "LPP", "KGH", "ALE", "ALR", "MBK",
             "DNP", "OPL", "KRU", "SPL", "PGE", "XTB", "CPS", "CCC", "JSW", "TPE"]

    with conn() as c:
        df = pd.read_sql(f"""
            SELECT s.date, s.ticker, s.close, c.name
            FROM stock_prices s
            JOIN companies c USING (ticker)
            WHERE s.ticker = ANY(%(tickers)s)
              AND s.date >= '2020-01-01'
            ORDER BY ticker, date
        """, c, params={"tickers": WIG20})

    # Normalize to 100 at start date
    df["date"] = pd.to_datetime(df["date"])
    base = df.groupby("ticker").apply(lambda g: g.nsmallest(1, "date")["close"].values[0]).to_dict()
    df["indexed"] = df.apply(lambda r: r["close"] / base[r["ticker"]] * 100, axis=1)

    fig = go.Figure()
    palette = px.colors.qualitative.Plotly
    for i, ticker in enumerate(sorted(WIG20)):
        sub = df[df["ticker"] == ticker]
        if sub.empty:
            continue
        name = sub["name"].iloc[0]
        fig.add_trace(go.Scatter(
            x=sub["date"], y=sub["indexed"].round(1),
            name=f"{ticker} · {name}",
            mode="lines",
            line=dict(width=1.5, color=palette[i % len(palette)]),
            hovertemplate=f"<b>{ticker}</b><br>%{{x|%Y-%m-%d}}<br>Index: %{{y:.1f}}<extra></extra>",
        ))

    fig.add_hline(y=100, line_dash="dot", line_color=COLORS["muted"],
                  annotation_text="base = 100 (Jan 2020)")

    apply_layout(fig,
        "WIG20 — Price Performance (Indexed, Jan 2020 = 100)",
        "Warsaw Stock Exchange · 20 large-cap stocks · Source: stooq.com",
    )
    fig.update_layout(height=580, hovermode="x unified",
                      legend=dict(font=dict(size=10)))

    save(fig, "wig20_performance.html", "WIG20 Performance")


# ─────────────────────────────────────────────────────────────
# 7. STOCK MARKET: Sector YTD performance
# ─────────────────────────────────────────────────────────────
def chart_sector_ytd():
    with conn() as c:
        df = pd.read_sql("""
            WITH ytd_start AS (
                SELECT ticker, close AS start_close
                FROM stock_prices
                WHERE date = (
                    SELECT MIN(date) FROM stock_prices
                    WHERE date >= DATE_TRUNC('year', CURRENT_DATE)
                )
            ),
            latest AS (
                SELECT ticker, close AS end_close
                FROM stock_prices
                WHERE date = (SELECT MAX(date) FROM stock_prices)
            )
            SELECT
                c.sector,
                AVG((l.end_close - y.start_close) / y.start_close * 100) AS ytd_pct,
                COUNT(*) AS n_stocks
            FROM ytd_start y
            JOIN latest l USING (ticker)
            JOIN companies c USING (ticker)
            GROUP BY c.sector
            ORDER BY ytd_pct DESC
        """, c)

    df["ytd_pct"] = df["ytd_pct"].round(1)
    fig = go.Figure(go.Bar(
        x=df["ytd_pct"],
        y=df["sector"],
        orientation="h",
        marker_color=[COLORS["green"] if v >= 0 else COLORS["red"] for v in df["ytd_pct"]],
        text=df["ytd_pct"].astype(str) + "%",
        textposition="outside",
        customdata=df["n_stocks"],
        hovertemplate="<b>%{y}</b><br>YTD: %{x:.1f}%<br>Stocks: %{customdata}<extra></extra>",
    ))

    apply_layout(fig,
        "GPW Sector Performance — Year to Date",
        f"Average return per sector · Source: stooq.com",
    )
    fig.update_layout(height=560, showlegend=False)
    fig.update_xaxes(ticksuffix="%", **LAYOUT_BASE["xaxis"])

    save(fig, "sector_ytd.html", "Sector YTD Performance")


# ─────────────────────────────────────────────────────────────
# 8. STOCK MARKET: Top movers (last 30 days)
# ─────────────────────────────────────────────────────────────
def chart_top_movers():
    with conn() as c:
        df = pd.read_sql("""
            WITH period_start AS (
                SELECT ticker, close AS start_close
                FROM stock_prices
                WHERE date = (
                    SELECT MIN(date) FROM stock_prices
                    WHERE date >= CURRENT_DATE - INTERVAL '30 days'
                )
            ),
            latest AS (
                SELECT ticker, close AS end_close
                FROM stock_prices
                WHERE date = (SELECT MAX(date) FROM stock_prices)
            )
            SELECT
                c.name,
                p.ticker,
                c.sector,
                ROUND((l.end_close - p.start_close) / p.start_close * 100, 1) AS return_pct
            FROM period_start p
            JOIN latest l ON l.ticker = p.ticker
            JOIN companies c ON c.ticker = p.ticker
            ORDER BY return_pct DESC
        """, c)

    top_n = 15
    top = df.head(top_n).iloc[::-1]
    bot = df.tail(top_n)

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=["Top 15 Gainers (30d)", "Top 15 Losers (30d)"],
        horizontal_spacing=0.12,
    )

    fig.add_trace(go.Bar(
        y=top["ticker"] + " · " + top["name"].str[:20],
        x=top["return_pct"],
        orientation="h",
        marker_color=COLORS["green"],
        text=top["return_pct"].astype(str) + "%",
        textposition="outside",
    ), row=1, col=1)

    fig.add_trace(go.Bar(
        y=bot["ticker"] + " · " + bot["name"].str[:20],
        x=bot["return_pct"],
        orientation="h",
        marker_color=COLORS["red"],
        text=bot["return_pct"].astype(str) + "%",
        textposition="outside",
    ), row=1, col=2)

    apply_layout(fig,
        "GPW Top Movers — Last 30 Days",
        "All listed stocks (WIG20 + mWIG40 + sWIG80) · Source: stooq.com",
    )
    fig.update_layout(height=540, showlegend=False)
    for col in [1, 2]:
        fig.update_xaxes(row=1, col=col, ticksuffix="%", **LAYOUT_BASE["xaxis"])
        fig.update_yaxes(row=1, col=col, **LAYOUT_BASE["yaxis"])

    save(fig, "top_movers.html", "Top Movers 30d")


# ─────────────────────────────────────────────────────────────
# 9. STOCK MARKET: Long-term WIG20 blue chips (all history)
# ─────────────────────────────────────────────────────────────
def chart_bluechips_longterm():
    BLUECHIPS = ["PKO", "PEO", "PKN", "PZU", "KGH", "LPP", "CDR"]

    with conn() as c:
        df = pd.read_sql(f"""
            SELECT s.date, s.ticker, s.close, c.name
            FROM stock_prices s
            JOIN companies c USING (ticker)
            WHERE s.ticker = ANY(%(tickers)s)
            ORDER BY ticker, date
        """, c, params={"tickers": BLUECHIPS})

    df["date"] = pd.to_datetime(df["date"])

    fig = go.Figure()
    palette = [COLORS["blue"], COLORS["green"], COLORS["yellow"],
               COLORS["purple"], COLORS["orange"], COLORS["teal"], COLORS["red"]]

    for i, ticker in enumerate(BLUECHIPS):
        sub = df[df["ticker"] == ticker]
        if sub.empty:
            continue
        fig.add_trace(go.Scatter(
            x=sub["date"], y=sub["close"].round(2),
            name=f"{ticker} · {sub['name'].iloc[0]}",
            mode="lines",
            line=dict(width=1.8, color=palette[i]),
            hovertemplate=f"<b>{ticker}</b><br>%{{x|%Y-%m-%d}}<br>Close: %{{y:.2f}} PLN<extra></extra>",
        ))

    apply_layout(fig,
        "GPW Blue Chips — Full History",
        "Nominal close prices · PKO, PEO, PKN, PZU, KGH, LPP, CDR · Source: stooq.com",
    )
    fig.update_layout(height=520, hovermode="x unified")
    fig.update_yaxes(title_text="Close Price (PLN)")

    save(fig, "bluechips_longterm.html", "Blue Chips Long-term")


# ─────────────────────────────────────────────────────────────
# INDEX PAGE
# ─────────────────────────────────────────────────────────────
def generate_index():
    charts = [
        ("national_budget_overview.html",      "State Budget Overview",          "Revenues, expenditures & deficit 2008–2024", "📊"),
        ("national_budget_deficit_pct.html",   "Deficit as % of Revenues",       "Fiscal pressure ratio 2008–2024", "📉"),
        ("voivodship_aggregate.html",          "Voivodship Budgets — Aggregate", "All 16 regions combined 1999–2024", "🗺️"),
        ("voivodship_2024_comparison.html",    "Voivodship Comparison 2024",     "Revenues & expenditures per region", "📋"),
        ("voivodship_balance_heatmap.html",    "Regional Balance Heatmap",       "Surplus/deficit matrix by region & year", "🔥"),
        ("wig20_performance.html",             "WIG20 Performance",              "20 large-cap stocks indexed since Jan 2020", "📈"),
        ("sector_ytd.html",                    "Sector YTD Performance",         "Average sector return year-to-date", "🏭"),
        ("top_movers.html",                    "Top Movers — 30 Days",           "Biggest gainers & losers on GPW", "🚀"),
        ("bluechips_longterm.html",            "Blue Chips — Full History",      "Long-term nominal prices for top stocks", "💼"),
    ]

    cards = "\n".join(f"""
        <a href="{fname}" class="card">
          <div class="icon">{icon}</div>
          <div class="card-body">
            <h3>{title}</h3>
            <p>{desc}</p>
          </div>
        </a>""" for fname, title, desc, icon in charts)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Open Reporting — Analytics Portal</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  :root {{
    --bg: #0F172A; --surface: #1E293B; --border: #334155;
    --text: #F1F5F9; --muted: #94A3B8; --accent: #3B82F6;
  }}
  body {{ background: var(--bg); color: var(--text); font-family: Inter, system-ui, sans-serif; }}
  header {{ padding: 3rem 2rem 2rem; border-bottom: 1px solid var(--border); }}
  header h1 {{ font-size: 1.8rem; font-weight: 700; }}
  header h1 span {{ color: var(--accent); }}
  header p {{ color: var(--muted); margin-top: 0.5rem; font-size: 0.95rem; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1rem; padding: 2rem; }}
  .card {{
    display: flex; align-items: flex-start; gap: 1rem;
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 10px; padding: 1.25rem;
    text-decoration: none; color: inherit;
    transition: border-color 0.15s, transform 0.1s;
  }}
  .card:hover {{ border-color: var(--accent); transform: translateY(-2px); }}
  .icon {{ font-size: 1.6rem; flex-shrink: 0; }}
  .card-body h3 {{ font-size: 0.95rem; font-weight: 600; margin-bottom: 0.3rem; }}
  .card-body p {{ font-size: 0.82rem; color: var(--muted); line-height: 1.4; }}
  footer {{ padding: 2rem; text-align: center; color: var(--muted); font-size: 0.8rem; border-top: 1px solid var(--border); }}
</style>
</head>
<body>
<header>
  <h1>Open <span>Reporting</span></h1>
  <p>Polish economic indicators — interactive charts · Fiscal data 1999–2024 · GPW stock market since 1992</p>
</header>
<div class="grid">{cards}
</div>
<footer>Data sources: GUS BDL API · Ministerstwo Finansów · NIK · stooq.com · Generated by open-reporting.dev</footer>
</body>
</html>"""

    path = os.path.join(OUT, "index.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓ index.html")


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating charts...")
    chart_national_budget_overview()
    chart_national_budget_deficit_pct()
    chart_voivodship_aggregate()
    chart_voivodship_2024_comparison()
    chart_voivodship_balance_heatmap()
    chart_wig20_performance()
    chart_sector_ytd()
    chart_top_movers()
    chart_bluechips_longterm()
    generate_index()
    print(f"\nDone. Charts saved to {OUT}/")
