#!/usr/bin/env python3
"""
Open Reporting — Public Finance Dashboard
Updated to match Justinmind template design:
- Dark header bar (Personal finance style)
- 3 KPI cards at top with big numbers
- White card styling with shadows
- Grid layout for charts
- Clean typography

Run:
    PYTHONPATH=/opt/open-reporting \
    DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb \
    python3 products/dashboards/finance_test/app.py
"""
import logging

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, html, dcc

import complex_dashboard.assets.theme as _theme  # noqa: F401
from complex_dashboard.assets.theme import (
    AZURE_1, AZURE_3, BG_PAGE, BG_SURFACE, BORDER,
    COLORWAY, NEGATIVE, POSITIVE, SUBTEXT, TEXT, WARNING,
)
from complex_dashboard.assets.data.db import query

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

PORT = 8054

# ── Theme colors matching Justinmind templates ─────────────────────────────────
COLORS = {
    "bg_page": "#F0F2F5",
    "bg_card": "#FFFFFF",
    "header": "#1A1F36",
    "header_secondary": "#2D3748",
    "primary": "#4299E1",
    "primary_dark": "#3182CE",
    "success": "#48BB78",
    "danger": "#F56565",
    "warning": "#ED8936",
    "text_dark": "#1A202C",
    "text_medium": "#718096",
    "text_light": "#A0AEC0",
    "border": "#E2E8F0",
}

# ── Data loading ──────────────────────────────────────────────────────────────

log.info("Loading mart_finance data...")
_SQL_ALL = """
    SELECT
        source_id, detail_id, detail_name, geo, country_name,
        period_year, is_poland, is_eu_aggregate, is_v4,
        fiscal_category, dim_resources_uses,
        value, unit, is_projection, obs_status
    FROM curated.mart_finance
"""
_mart: pd.DataFrame = query(_SQL_ALL)

# ── Helper functions ────────────────────────────────────────────────────────────

def _ts(detail_id: str, geo: str, source_id: str, min_year: int = 1995) -> pd.DataFrame:
    return (
        _mart[
            (_mart["detail_id"] == detail_id) &
            (_mart["geo"] == geo) &
            (_mart["source_id"] == source_id) &
            (_mart["period_year"] >= min_year)
        ]
        .sort_values("period_year")
    )


def _get_kpi_data() -> dict:
    """Get KPI data for top cards."""
    kpis = {}
    
    # Revenue
    rev = _ts("pub.revenue_gdp", "PL", "eurostat", min_year=2010)
    if not rev.empty:
        current = rev.iloc[-1]["value"]
        prev = rev.iloc[-2]["value"] if len(rev) > 1 else current
        kpis["revenue"] = {"value": round(current, 1), "change": round(((current - prev) / abs(prev) * 100) if prev else 0, 1)}
    
    # Expenditure
    exp = _ts("pub.expenditure_gdp", "PL", "eurostat", min_year=2010)
    if not exp.empty:
        current = exp.iloc[-1]["value"]
        prev = exp.iloc[-2]["value"] if len(exp) > 1 else current
        kpis["expenditure"] = {"value": round(current, 1), "change": round(((current - prev) / abs(prev) * 100) if prev else 0, 1)}
    
    # Balance
    bal = _ts("pub.fiscal_balance_gdp", "PL", "eurostat", min_year=2010)
    if not bal.empty:
        current = bal.iloc[-1]["value"]
        prev = bal.iloc[-2]["value"] if len(bal) > 1 else current
        kpis["balance"] = {"value": round(current, 1), "change": round(((current - prev) / abs(prev) * 100) if prev else 0, 1)}
    
    # Debt
    debt = _ts("pub.public_debt_gdp", "PL", "eurostat", min_year=2010)
    if not debt.empty:
        current = debt.iloc[-1]["value"]
        prev = debt.iloc[-2]["value"] if len(debt) > 1 else current
        kpis["debt"] = {"value": round(current, 1), "change": round(((current - prev) / abs(prev) * 100) if prev else 0, 1)}
    
    return kpis


# ── KPI Card Component ─────────────────────────────────────────────────────────

def make_kpi_card(title: str, value: float, change: float, icon: str, color: str = "primary") -> html.Div:
    change_color = COLORS["success"] if change > 0 else COLORS["danger"]
    if "debt" in title.lower() and change > 0:
        change_color = COLORS["danger"]  # Higher debt is bad
    elif "debt" in title.lower() and change < 0:
        change_color = COLORS["success"]  # Lower debt is good
    
    arrow = "↑" if change > 0 else "↓" if change < 0 else "→"
    
    return html.Div([
        html.Div([
            html.Span(icon, style={"marginRight": "8px", "fontSize": "18px"}),
            html.Span(title, style={"fontSize": "13px", "color": COLORS["text_medium"], "fontWeight": "500"})
        ], style={"display": "flex", "alignItems": "center", "marginBottom": "8px"}),
        html.Div(f"{value:.1f}%", style={
            "fontSize": "32px", 
            "fontWeight": "700", 
            "color": COLORS["text_dark"],
            "lineHeight": "1.2"
        }),
        html.Div([
            html.Span(f"{arrow} {abs(change):.1f}%", style={"color": change_color, "fontWeight": "600", "fontSize": "13px"}),
            html.Span(" vs zeszły rok", style={"color": COLORS["text_light"], "fontSize": "12px", "marginLeft": "4px"})
        ], style={"marginTop": "6px"})
    ], style={
        "background": COLORS["bg_card"],
        "borderRadius": "12px",
        "padding": "20px",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.08)",
        "border": f"1px solid {COLORS['border']}",
        "transition": "transform 0.2s, box-shadow 0.2s",
    })


# ── Chart 1: Revenue vs Expenditure ───────────────────────────────────────────

def build_revenue_chart() -> go.Figure:
    rev = _ts("pub.revenue_gdp", "PL", "eurostat", min_year=2010)
    exp = _ts("pub.expenditure_gdp", "PL", "eurostat", min_year=2010)
    
    df = rev[["period_year", "value"]].merge(exp[["period_year", "value"]], on="period_year", suffixes=("_rev", "_exp"))
    df = df.sort_values("period_year")
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df["period_year"], y=df["value_rev"],
        name="Dochody", marker_color=COLORS["primary"],
        hovertemplate="Dochody: %{y:.1f}% PKB<br>Rok: %{x}<extra></extra>"
    ))
    
    fig.add_trace(go.Bar(
        x=df["period_year"], y=df["value_exp"],
        name="Wydatki", marker_color=COLORS["text_medium"],
        hovertemplate="Wydatki: %{y:.1f}% PKB<br>Rok: %{x}<extra></extra>"
    ))
    
    fig.update_layout(
        title=dict(text="Dochody i wydatki (% PKB)", font=dict(size=14, weight="bold")),
        barmode="group",
        legend=dict(orientation="h", y=1.02, x=0.5, xanchor="center"),
        paper_bgcolor=COLORS["bg_card"],
        plot_bgcolor=COLORS["bg_card"],
        margin=dict(t=50, l=50, r=20, b=40),
        height=280,
    )
    
    fig.update_xaxes(showgrid=False, dtick=2, tickfont=dict(size=10))
    fig.update_yaxes(title="% PKB", gridcolor=COLORS["border"], tickfont=dict(size=10))
    
    return fig


# ── Chart 2: Fiscal Balance ───────────────────────────────────────────────────

def build_balance_chart() -> go.Figure:
    bal = _ts("pub.fiscal_balance_gdp", "PL", "eurostat", min_year=2010)
    
    colors = [COLORS["success"] if v >= 0 else COLORS["danger"] for v in bal["value"]]
    
    fig = go.Figure(go.Bar(
        x=bal["period_year"], y=bal["value"],
        marker_color=colors,
        hovertemplate="Saldo: %{y:.1f}% PKB<br>Rok: %{x}<extra></extra>"
    ))
    
    fig.add_hline(y=0, line_color=COLORS["border"], line_width=1)
    fig.add_hline(y=-3, line_dash="dash", line_color=COLORS["warning"], line_width=1,
                  annotation_text="Próg SGP", annotation_position="bottom right")
    
    fig.update_layout(
        title=dict(text="Saldo fiskalne (% PKB)", font=dict(size=14, weight="bold")),
        paper_bgcolor=COLORS["bg_card"],
        plot_bgcolor=COLORS["bg_card"],
        margin=dict(t=40, l=50, r=20, b=40),
        showlegend=False,
        height=220,
    )
    
    fig.update_xaxes(showgrid=False, dtick=2, tickfont=dict(size=10))
    fig.update_yaxes(title="% PKB", gridcolor=COLORS["border"], tickfont=dict(size=10))
    
    return fig


# ── Chart 3: Public Debt ─────────────────────────────────────────────────────

def build_debt_chart() -> go.Figure:
    debt = _ts("pub.public_debt_gdp", "PL", "eurostat", min_year=2010)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=debt["period_year"], y=debt["value"],
        mode="lines+markers",
        name="Dług publiczny",
        line=dict(color=COLORS["danger"], width=2.5),
        marker=dict(size=6, color=COLORS["danger"]),
        fill='tozeroy',
        fillcolor=f"rgba(245, 101, 101, 0.15)",
        hovertemplate="Dług: %{y:.1f}% PKB<br>Rok: %{x}<extra></extra>"
    ))
    
    fig.add_hline(y=60, line_dash="dash", line_color=COLORS["danger"], line_width=1.5,
                  annotation_text="Próg Maastricht (60%)")
    
    fig.update_layout(
        title=dict(text="Dług publiczny (% PKB)", font=dict(size=14, weight="bold")),
        paper_bgcolor=COLORS["bg_card"],
        plot_bgcolor=COLORS["bg_card"],
        margin=dict(t=40, l=50, r=20, b=40),
        showlegend=False,
        height=220,
    )
    
    fig.update_xaxes(showgrid=False, dtick=2, tickfont=dict(size=10))
    fig.update_yaxes(title="% PKB", gridcolor=COLORS["border"], tickfont=dict(size=10), range=[0, None])
    
    return fig


# ── Chart 4: EU Comparison ───────────────────────────────────────────────────

def build_eu_chart() -> go.Figure:
    eu27_codes = ["AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "EL", "ES",
                  "FI", "FR", "HR", "HU", "IE", "IT", "LT", "LU", "LV", "MT",
                  "NL", "PL", "PT", "RO", "SE", "SI", "SK"]
    
    df = _mart[
        (_mart["detail_id"] == "pub.fiscal_balance_gdp") &
        (_mart["source_id"] == "eurostat") &
        (_mart["geo"].isin(eu27_codes)) &
        (_mart["period_year"] == 2023)
    ].dropna(subset=["value"]).sort_values("value")
    
    colors = [COLORS["primary"] if geo != "PL" else COLORS["danger"] for geo in df["geo"]]
    
    fig = go.Figure(go.Bar(
        x=df["value"], y=df["geo"],
        orientation="h",
        marker_color=colors,
        text=df["value"].apply(lambda x: f"{x:+.1f}%"),
        textposition="outside",
        textfont=dict(size=9),
    ))
    
    fig.update_layout(
        title=dict(text="Saldo fiskalne — Polska vs UE-27 (2023)", font=dict(size=14, weight="bold")),
        paper_bgcolor=COLORS["bg_card"],
        plot_bgcolor=COLORS["bg_card"],
        margin=dict(t=40, l=40, r=40, b=40),
        height=350,
    )
    
    fig.update_xaxes(title="% PKB", gridcolor=COLORS["border"], tickfont=dict(size=10))
    fig.update_yaxes(title=None, tickfont=dict(size=10))
    
    return fig


# ── Chart 5: COFOG Breakdown (Pie/Donut) ──────────────────────────────────────

def build_cofog_chart() -> go.Figure:
    cofog_data = []
    labels = {
        "pub.cofog_01_gdp": "Usługi ogólne", "pub.cofog_07_gdp": "Zdrowie",
        "pub.cofog_09_gdp": "Edukacja", "pub.cofog_10_gdp": "Ochrona społ.",
        "pub.cofog_04_gdp": "Gospodarka", "pub.cofog_03_gdp": "Bezpieczeństwo",
    }
    for i in [1, 7, 9, 10, 4, 3]:
        detail_id = f"pub.cofog_0{i}_gdp"
        df = _ts(detail_id, "PL", "eurostat", min_year=2020)
        if not df.empty:
            cofog_data.append({"label": labels.get(detail_id, f"F{i}"), "value": float(df.iloc[-1]["value"])})
    
    df_cofog = pd.DataFrame(cofog_data).sort_values("value", ascending=False)
    
    colors = ["#4299E1", "#48BB78", "#ED8936", "#9F7AEA", "#F56565", "#718096"]
    
    fig = go.Figure(go.Pie(
        labels=df_cofog["label"], values=df_cofog["value"],
        hole=0.5, marker_colors=colors,
        textinfo="label+percent", textposition="outside",
        hovertemplate="%{label}: %{value:.1f}% PKB<br>%{percent}<extra></extra>"
    ))
    
    fig.update_layout(
        title=dict(text="Wydatki według funkcji (%)", font=dict(size=14, weight="bold")),
        paper_bgcolor=COLORS["bg_card"],
        plot_bgcolor=COLORS["bg_card"],
        margin=dict(t=40, l=40, r=40, b=40),
        height=280,
        showlegend=False,
    )
    
    return fig


# ── Dashboard Layout ─────────────────────────────────────────────────────────

app = Dash(__name__, title="Finanse publiczne", requests_pathname_prefix="/finance-test/", routes_pathname_prefix="/finance-test/")
app.config.suppress_callback_exceptions = True

# Get data
kpis = _get_kpi_data()
latest_year = _mart["period_year"].max()

# Build charts
fig1 = build_revenue_chart()
fig2 = build_balance_chart()
fig3 = build_debt_chart()
fig4 = build_eu_chart()
fig5 = build_cofog_chart()

# Card style for all charts
card_style = {
    "background": COLORS["bg_card"],
    "borderRadius": "12px",
    "boxShadow": "0 2px 8px rgba(0,0,0,0.08)",
    "border": f"1px solid {COLORS['border']}",
    "padding": "20px",
}

app.layout = html.Div([
    # ── Header ─────────────────────────────────────────────────────────────
    html.Div([
        html.Div([
            html.Span("📊", style={"fontSize": "24px", "marginRight": "12px"}),
            html.Div([
                html.Div("Finanse publiczne", style={"fontSize": "18px", "fontWeight": "600", "color": "#FFF"}),
                html.Div(f"Dane za rok {latest_year}", style={"fontSize": "12px", "color": COLORS["text_light"]}),
            ]),
        ], style={"display": "flex", "alignItems": "center"}),
        html.Div([
            html.Span("🔔", style={"fontSize": "18px", "color": COLORS["text_light"], "marginRight": "16px", "cursor": "pointer"}),
            html.Span("👤", style={"fontSize": "18px", "color": COLORS["text_light"], "cursor": "pointer"}),
        ], style={"display": "flex", "alignItems": "center"}),
    ], style={
        "background": COLORS["header"],
        "padding": "16px 32px",
        "display": "flex",
        "justifyContent": "space-between",
        "alignItems": "center",
    }),

    # ── Main Content ─────────────────────────────────────────────────────
    html.Div([
        # Filter bar
        html.Div([
            html.Div([
                html.Label("Rok:", style={"fontSize": "12px", "color": COLORS["text_medium"], "marginBottom": "4px", "display": "block"}),
                dcc.Dropdown(
                    id="year-filter", clearable=False, searchable=False,
                    options=[{"label": str(y), "value": y} for y in range(2015, 2025)],
                    value=latest_year, style={"width": "100px"},
                ),
            ]),
        ], style={"padding": "20px 0"}),

        # KPI Cards
        html.Div([
            make_kpi_card("Dochody", kpis.get("revenue", {}).get("value", 0), 
                         kpis.get("revenue", {}).get("change", 0), "💰"),
            make_kpi_card("Wydatki", kpis.get("expenditure", {}).get("value", 0), 
                         kpis.get("expenditure", {}).get("change", 0), "💳"),
            make_kpi_card("Saldo", kpis.get("balance", {}).get("value", 0), 
                         kpis.get("balance", {}).get("change", 0), "⚖️"),
            make_kpi_card("Dług", kpis.get("debt", {}).get("value", 0), 
                         kpis.get("debt", {}).get("change", 0), "📈"),
        ], style={
            "display": "grid", "gridTemplateColumns": "repeat(4, 1fr)", "gap": "20px",
            "marginBottom": "24px",
        }),

        # Charts Grid
        html.Div([
            # Row 1: Revenue + Balance
            html.Div(html.Div(dcc.Graph(figure=fig1), style={"height": "100%"}), style={**card_style, "gridColumn": "span 2"}),
            html.Div(html.Div(dcc.Graph(figure=fig2), style={"height": "100%"}), style={**card_style, "gridColumn": "span 1"}),
            html.Div(html.Div(dcc.Graph(figure=fig3), style={"height": "100%"}), style={**card_style, "gridColumn": "span 1"}),
            
            # Row 2: COFOG + EU
            html.Div(html.Div(dcc.Graph(figure=fig5), style={"height": "100%"}), style={**card_style, "gridColumn": "span 1"}),
            html.Div(html.Div(dcc.Graph(figure=fig4), style={"height": "100%"}), style={**card_style, "gridColumn": "span 3"}),
        ], style={
            "display": "grid",
            "gridTemplateColumns": "repeat(4, 1fr)",
            "gap": "20px",
        }),
    ], style={"padding": "24px", "maxWidth": "1400px", "margin": "0 auto"}),
], style={"background": COLORS["bg_page"], "minHeight": "100vh", "fontFamily": "'Inter', -apple-system, sans-serif"})


if __name__ == "__main__":
    log.info("Starting Public Finance Dashboard on port %d", PORT)
    app.run(host="0.0.0.0", port=PORT, debug=False)