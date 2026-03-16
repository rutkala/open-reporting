"""
GPW Stock Market Dashboard — Warsaw Stock Exchange.
Charts: WIG20 indexed performance · sector YTD · top movers · stock detail
Interactive: ticker selector, date range, sector filter
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import json
from lib.db import query
from lib.theme import C, AXIS, PALETTE, apply, page, kpi_card

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "charts")

WIG20 = ["PKO","PEO","CDR","PKN","PZU","LPP","KGH","ALE","ALR","MBK",
         "DNP","OPL","KRU","SPL","PGE","XTB","CPS","CCC","JSW","TPE"]


def build():
    # ── Raw data ───────────────────────────────────────────────────────────────
    prices = query("""
        SELECT s.date, s.ticker, s.close, s.volume, c.name, c.sector
        FROM stock_prices s JOIN companies c USING (ticker)
        WHERE s.date >= '2020-01-01'
        ORDER BY ticker, date
    """)
    prices["date"] = prices["date"].astype(str)

    all_prices = query("""
        SELECT s.date, s.ticker, s.close, c.name, c.sector
        FROM stock_prices s JOIN companies c USING (ticker)
        WHERE s.ticker = ANY(%(t)s)
        ORDER BY ticker, date
    """, {"t": WIG20})
    all_prices["date"] = all_prices["date"].astype(str)

    movers = query("""
        WITH s AS (
            SELECT ticker, close AS start_close
            FROM stock_prices
            WHERE date = (SELECT MIN(date) FROM stock_prices
                          WHERE date >= CURRENT_DATE - INTERVAL '30 days')
        ), e AS (
            SELECT ticker, close AS end_close
            FROM stock_prices
            WHERE date = (SELECT MAX(date) FROM stock_prices)
        )
        SELECT c.name, p.ticker, c.sector,
               ROUND((e.end_close - p.start_close) / p.start_close * 100, 1) AS ret
        FROM s p JOIN e ON e.ticker = p.ticker JOIN companies c ON c.ticker = p.ticker
        ORDER BY ret DESC
    """)

    ytd = query("""
        WITH s AS (
            SELECT ticker, close AS start_close
            FROM stock_prices
            WHERE date = (SELECT MIN(date) FROM stock_prices
                          WHERE date >= DATE_TRUNC('year', CURRENT_DATE))
        ), e AS (
            SELECT ticker, close AS end_close
            FROM stock_prices WHERE date = (SELECT MAX(date) FROM stock_prices)
        )
        SELECT c.sector,
               ROUND(AVG((e.end_close - p.start_close) / p.start_close * 100), 1) AS ytd_pct,
               COUNT(*) AS n
        FROM s p JOIN e ON e.ticker = p.ticker JOIN companies c ON c.ticker = p.ticker
        GROUP BY c.sector ORDER BY ytd_pct DESC
    """)

    latest_date = prices["date"].max()

    # ── KPIs ───────────────────────────────────────────────────────────────────
    top_gainer = movers.iloc[0]
    top_loser  = movers.iloc[-1]
    avg_ytd    = ytd["ytd_pct"].mean()

    kpis = "".join([
        kpi_card("Data as of", latest_date, "GPW Warsaw", "neu"),
        kpi_card("Best 30d", f"{top_gainer.ticker} {top_gainer.ret:+.1f}%",
                 top_gainer["name"][:25], "pos"),
        kpi_card("Worst 30d", f"{top_loser.ticker} {top_loser.ret:+.1f}%",
                 top_loser["name"][:25], "neg"),
        kpi_card("Avg Market YTD", f"{avg_ytd:+.1f}%",
                 "All GPW sectors average", "pos" if avg_ytd >= 0 else "neg"),
    ])

    # ── Chart 1: WIG20 indexed performance (all history) ──────────────────────
    fig1 = go.Figure()
    palette = px.colors.qualitative.Plotly

    for i, ticker in enumerate(WIG20):
        sub = all_prices[all_prices["ticker"] == ticker].copy()
        if sub.empty:
            continue
        base = sub["close"].iloc[0]
        sub["idx"] = (sub["close"] / base * 100).round(1)
        name = sub["name"].iloc[0]
        fig1.add_trace(go.Scatter(
            x=sub["date"], y=sub["idx"],
            name=f"{ticker}",
            mode="lines", line=dict(width=1.5, color=palette[i % len(palette)]),
            hovertemplate=f"<b>{ticker} · {name}</b><br>%{{x}}<br>Index: %{{y:.1f}}<extra></extra>",
        ))

    fig1.add_hline(y=100, line_dash="dot", line_color=C["muted"],
                   annotation_text="base 100", annotation_font_color=C["muted"])
    apply(fig1, "WIG20 — Indexed Performance (base = 100 at first available date)",
          "All 20 large-cap stocks · Warsaw Stock Exchange", height=480)
    fig1.update_layout(
        xaxis=dict(**AXIS, rangeslider=dict(visible=False),
                   rangeselector=dict(
                       buttons=[
                           dict(count=1, label="1M", step="month", stepmode="backward"),
                           dict(count=6, label="6M", step="month", stepmode="backward"),
                           dict(count=1, label="1Y", step="year",  stepmode="backward"),
                           dict(count=3, label="3Y", step="year",  stepmode="backward"),
                           dict(count=5, label="5Y", step="year",  stepmode="backward"),
                           dict(step="all", label="All"),
                       ],
                       bgcolor=C["card"], activecolor=C["blue"],
                       font=dict(color=C["text"], size=11),
                   )),
        legend=dict(font=dict(size=10)),
    )

    # ── Chart 2: Sector YTD ────────────────────────────────────────────────────
    fig2 = go.Figure(go.Bar(
        x=ytd["ytd_pct"], y=ytd["sector"], orientation="h",
        marker_color=[C["green"] if v >= 0 else C["red"] for v in ytd["ytd_pct"]],
        text=ytd["ytd_pct"].astype(str) + "%", textposition="outside",
        textfont=dict(size=10),
        customdata=ytd["n"],
        hovertemplate="<b>%{y}</b><br>YTD: %{x:.1f}%<br>%{customdata} stocks<extra></extra>",
    ))
    apply(fig2, "Sector Performance — Year to Date", "", height=480, showlegend=False)
    fig2.update_xaxes(ticksuffix="%")

    # ── Chart 3: Top/Bottom movers ─────────────────────────────────────────────
    top15 = movers.head(15).iloc[::-1]
    bot15 = movers.tail(15)

    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        y=top15.ticker + " · " + top15["name"].str[:18],
        x=top15.ret, orientation="h",
        name="Top gainers", marker_color=C["green"],
        text=top15.ret.astype(str) + "%", textposition="outside",
        textfont=dict(size=10),
    ))
    apply(fig3, "Top 15 Gainers — Last 30 Days", "", height=440, showlegend=False)
    fig3.update_xaxes(ticksuffix="%")

    fig4 = go.Figure()
    fig4.add_trace(go.Bar(
        y=bot15.ticker + " · " + bot15["name"].str[:18],
        x=bot15.ret, orientation="h",
        name="Top losers", marker_color=C["red"],
        text=bot15.ret.astype(str) + "%", textposition="outside",
        textfont=dict(size=10),
    ))
    apply(fig4, "Top 15 Losers — Last 30 Days", "", height=440, showlegend=False)
    fig4.update_xaxes(ticksuffix="%")

    # ── Chart 5: Stock detail (interactive selector) ───────────────────────────
    tickers = sorted(prices["ticker"].unique().tolist())
    options = "\n".join(f'<option value="{t}">{t} — {prices[prices.ticker==t]["name"].iloc[0]}</option>'
                        for t in tickers)

    # Pre-serialize data for JS
    stock_data = {}
    for t in tickers:
        sub = prices[prices["ticker"] == t][["date", "close", "volume"]].copy()
        stock_data[t] = {
            "dates":  sub["date"].tolist(),
            "close":  sub["close"].round(2).tolist(),
            "volume": sub["volume"].tolist(),
            "name":   prices[prices.ticker == t]["name"].iloc[0],
            "sector": prices[prices.ticker == t]["sector"].iloc[0],
        }

    def div(fig):
        return pio.to_html(fig, include_plotlyjs=False, full_html=False,
                           config={"displayModeBar": True, "scrollZoom": False})

    body = f"""
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<div class="charts">
  <div class="chart-card full">{div(fig1)}</div>
  <div class="charts two-col" style="grid-column:1/-1">
    <div class="chart-card">{div(fig2)}</div>
    <div style="display:grid;gap:1rem">
      <div class="chart-card">{div(fig3)}</div>
      <div class="chart-card">{div(fig4)}</div>
    </div>
  </div>
  <div class="chart-card full">
    <div style="padding:0.75rem 0.75rem 0">
      <div class="controls">
        <label>Select stock:</label>
        <select id="ticker-select">{options}</select>
      </div>
    </div>
    <div id="stock-detail"></div>
  </div>
</div>

<script>
const STOCKS = {json.dumps(stock_data)};
const bg="{C['bg']}",surface="{C['surface']}",border="{C['border']}",
      blue="{C['blue']}",red="{C['red']}",green="{C['green']}",
      muted="{C['muted']}",text="{C['text']}",card="{C['card']}";

function renderStock(ticker) {{
  const d = STOCKS[ticker];
  const closeColors = d.close.map((v,i) => i===0 ? blue : v >= d.close[i-1] ? green : red);
  const traces = [
    {{
      x: d.dates, y: d.close, name: 'Close', type: 'scatter', mode: 'lines',
      line: {{ color: blue, width: 2 }},
      hovertemplate: '%{{x}}<br><b>Close: %{{y:.2f}} PLN</b><extra></extra>',
    }},
    {{
      x: d.dates, y: d.volume, name: 'Volume', type: 'bar',
      yaxis: 'y2', marker: {{ color: muted, opacity: 0.4 }},
      hovertemplate: '%{{x}}<br>Volume: %{{y:,.0f}}<extra></extra>',
    }},
  ];
  const layout = {{
    paper_bgcolor: bg, plot_bgcolor: surface,
    font: {{ family: 'Inter, system-ui, sans-serif', color: text, size: 12 }},
    height: 400, hovermode: 'x unified',
    legend: {{ bgcolor: surface, bordercolor: border, borderwidth: 1, font: {{ size: 11 }} }},
    margin: {{ l: 60, r: 70, t: 50, b: 40 }},
    title: {{ text: '<b>' + ticker + ' · ' + d.name + '</b>  <span style="font-size:12px;color:' + muted + '">' + d.sector + '</span>',
              font: {{ size: 15 }}, x: 0.01 }},
    xaxis: {{
      gridcolor: border, linecolor: border, tickfont: {{ color: muted }},
      rangeselector: {{
        buttons: [
          {{ count:3,  label:'3M', step:'month', stepmode:'backward' }},
          {{ count:1,  label:'1Y', step:'year',  stepmode:'backward' }},
          {{ count:3,  label:'3Y', step:'year',  stepmode:'backward' }},
          {{ step:'all', label:'All' }},
        ],
        bgcolor: card, activecolor: blue,
        font: {{ color: text, size: 11 }},
      }},
    }},
    yaxis:  {{ gridcolor: border, linecolor: border, tickfont: {{ color: muted }},
               title: {{ text: 'Price (PLN)', font: {{ color: muted }} }} }},
    yaxis2: {{ overlaying: 'y', side: 'right', gridcolor: 'transparent',
               linecolor: border, tickfont: {{ color: muted }},
               title: {{ text: 'Volume', font: {{ color: muted }} }} }},
  }};
  Plotly.react('stock-detail', traces, layout, {{ displayModeBar: true, responsive: true }});
}}

document.getElementById('ticker-select').addEventListener('change', function() {{
  renderStock(this.value);
}});
renderStock(document.getElementById('ticker-select').value);
</script>"""

    html = page(
        title="GPW Warsaw Stock Exchange",
        subtitle="WIG20 · mWIG40 · sWIG80 · Daily prices since 1992 · Source: stooq.com",
        active="GPW Market",
        kpis=f'<div class="kpis">{kpis}</div>',
        body=body,
        source="stooq.com",
    )

    out = os.path.join(OUT, "gpw_market.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓ gpw_market.html")


if __name__ == "__main__":
    build()
