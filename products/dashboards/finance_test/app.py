#!/usr/bin/env python3
"""
Open Reporting — Public Finance Dashboard (TEST VERSION)
Designed from scratch following analytics knowledge base process:
1. Domain research (public-finance.md)
2. Identify analytical questions
3. Apply chart selection rules
4. Design with proper scales

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

import products.visuals.lib.theme as _theme  # noqa: F401
from products.visuals.lib.theme import (
    AZURE_1, AZURE_3, BG_PAGE, BG_SURFACE, BORDER,
    COLORWAY, NEGATIVE, POSITIVE, SUBTEXT, TEXT, WARNING,
)
from products.visuals.lib.db import query

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

PORT = 8054

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
    """Time series slice."""
    return (
        _mart[
            (_mart["detail_id"] == detail_id) &
            (_mart["geo"] == geo) &
            (_mart["source_id"] == source_id) &
            (_mart["period_year"] >= min_year)
        ]
        .sort_values("period_year")
    )

# ── Chart 1: Revenue vs Expenditure + Balance (Multi-panel) ──────────────────

def build_revenue_expenditure_chart() -> go.Figure:
    """
    Analytical question: "How do revenue and expenditure compare over time, and what's the balance?"
    Analysis type: Comparison + Trend
    Chart selection: Stacked subplots (different scales)
    
    Design:
    - Top panel: Balance (deficit) as columns - shows trajectory
    - Bottom panel: Revenue | Expenditure grouped bars - shows comparison
    """
    rev = _ts("pub.revenue_gdp", "PL", "eurostat", min_year=2000)
    exp = _ts("pub.expenditure_gdp", "PL", "eurostat", min_year=2000)
    bal = _ts("pub.fiscal_balance_gdp", "PL", "eurostat", min_year=2000)

    m = (
        rev[["period_year", "value"]].rename(columns={"value": "rev"})
        .merge(exp[["period_year", "value"]].rename(columns={"value": "exp"}), on="period_year")
        .merge(bal[["period_year", "value"]].rename(columns={"value": "bal"}), on="period_year")
        .sort_values("period_year")
    )

    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.35, 0.65],
        vertical_spacing=0.08,
        shared_xaxes=True,
        subplot_titles=("Saldo (deficyt)", "Dochody i wydatki"),
    )

    # Top: Balance columns
    fig.add_trace(go.Bar(
        x=m["period_year"], y=m["bal"],
        name="Saldo", marker_color="#C0503A",
    ), row=1, col=1)

    # SGP threshold reference
    fig.add_hline(y=-3, line_dash="dash", line_color="#6B7A8D", line_width=1,
                  annotation_text="-3% SGP", row=1, col=1)
    fig.add_hline(y=0, line_color="#C8CDD5", line_width=1, row=1, col=1)

    # Bottom: Revenue and Expenditure grouped bars
    fig.add_trace(go.Bar(
        x=m["period_year"], y=m["rev"],
        name="Dochody", marker_color="#4A4A4A",  # IBCS: dark grey for actual
    ), row=2, col=1)

    fig.add_trace(go.Bar(
        x=m["period_year"], y=m["exp"],
        name="Wydatki", marker_color="#A0A0A0",  # IBCS: light grey for comparison
    ), row=2, col=1)

    fig.update_layout(
        title=dict(
            text="Dochody, wydatki i saldo sektora finansów publicznych",
            subtitle=dict(text="Polska, 2000-2024, dane Eurostat, % PKB"),
        ),
        barmode="group",
        showlegend=True,
        legend=dict(orientation="h", y=-0.02),
        template="nordic",
        height=450,
    )

    fig.update_xaxes(dtick=2, row=2, col=1)
    fig.update_yaxes(title="% PKB", row=1, col=1)
    fig.update_yaxes(title="% PKB", showgrid=True, row=2, col=1)

    return fig


# ── Chart 2: Debt trajectory with Maastricht threshold ────────────────────────

def build_debt_chart() -> go.Figure:
    """
    Analytical question: "Is public debt sustainable? What's the trajectory vs 60% threshold?"
    Analysis type: Trend with benchmark
    Chart selection: Line chart with threshold band
    """
    debt = _ts("pub.public_debt_gdp", "PL", "eurostat", min_year=2000)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=debt["period_year"], y=debt["value"],
        mode="lines+markers",
        name="Dług publiczny",
        line=dict(color="#4A7FB5", width=2.5),
        marker=dict(size=5),
    ))

    # Maastricht 60% threshold
    fig.add_hline(y=60, line_dash="dash", line_color="#C0503A", line_width=1.5,
                  annotation_text="Próg Maastricht: 60%", annotation_position="bottom right")

    fig.update_layout(
        title=dict(
            text="Dług publiczny (% PKB)",
            subtitle=dict(text="Polska, 2000-2024, dane Eurostat"),
        ),
        yaxis=dict(title="% PKB", showgrid=True),
        xaxis=dict(title=None, dtick=2),
        legend=dict(orientation="h", y=-0.1),
        template="nordic",
        height=350,
    )

    return fig


# ── Chart 3: COFOG Expenditure breakdown ───────────────────────────────────────

def build_cofog_chart() -> go.Figure:
    """
    Analytical question: "Where is money spent? What are the major expenditure functions?"
    Analysis type: Composition
    Chart selection: Horizontal bar (ranked) - best for many categories with long labels
    """
    cofog_data = []
    for i in range(1, 11):
        detail_id = f"pub.cofog_0{i}_gdp"
        df = _ts(detail_id, "PL", "eurostat", min_year=2015)
        if not df.empty:
            latest = df.iloc[-1]
            cofog_data.append({
                "function": f"Funkcja {i}",
                "value": float(latest["value"]),
                "year": int(latest["period_year"]),
            })

    df_cofog = pd.DataFrame(cofog_data).sort_values("value", ascending=True)

    colors = COLORWAY[:len(df_cofog)]

    fig = go.Figure(go.Bar(
        x=df_cofog["value"], y=df_cofog["function"],
        orientation="h",
        marker_color=colors,
        text=df_cofog["value"].apply(lambda x: f"{x:.1f}%"),
        textposition="outside",
    ))

    fig.update_layout(
        title=dict(
            text="Wydatki według funkcji COFOG (% PKB)",
            subtitle=dict(text="Polska, 2024, dane Eurostat"),
        ),
        xaxis=dict(title="% PKB"),
        yaxis=dict(title=None),
        template="nordic",
        height=350,
    )

    return fig


# ── Chart 4: Poland vs EU comparison ──────────────────────────────────────────

def build_eu_comparison_chart() -> go.Figure:
    """
    Analytical question: "How does Poland compare to EU peers? Is Poland an outlier?"
    Analysis type: Ranking/Comparison
    Chart selection: Horizontal bar - direct comparison
    """
    eu27_codes = [
        "AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "EL", "ES",
        "FI", "FR", "HR", "HU", "IE", "IT", "LT", "LU", "LV", "MT",
        "NL", "PL", "PT", "RO", "SE", "SI", "SK",
    ]

    df = _mart[
        (_mart["detail_id"] == "pub.fiscal_balance_gdp") &
        (_mart["source_id"] == "eurostat") &
        (_mart["geo"].isin(eu27_codes)) &
        (_mart["period_year"] == 2023)
    ].dropna(subset=["value"]).sort_values("value")

    fig = go.Figure(go.Bar(
        x=df["value"], y=df["geo"],
        orientation="h",
        marker_color=[
            "#C0503A" if geo == "PL" else "#4A7FB5"
            for geo in df["geo"]
        ],
    ))

    fig.update_layout(
        title=dict(
            text="Saldo fiskalne — Polska vs EU-27 (% PKB)",
            subtitle=dict(text="2023, dane Eurostat"),
        ),
        xaxis=dict(title="% PKB"),
        yaxis=dict(title=None),
        template="nordic",
        height=400,
    )

    return fig


# ── Dashboard layout ────────────────────────────────────────────────────────────

# Build charts at startup with callback exception handling
import dash
app = Dash(
    __name__,
    title="Finanse publiczne — TEST",
    requests_pathname_prefix="/finance-test/",
    routes_pathname_prefix="/finance-test/",
)
app.config.suppress_callback_exceptions = True

# Build charts at startup
log.info("Building charts...")
_chart1 = build_revenue_expenditure_chart()
_chart2 = build_debt_chart()
_chart3 = build_cofog_chart()
_chart4 = build_eu_comparison_chart()
log.info("Charts built successfully")

app.layout = html.Div(
    style={"background": BG_PAGE, "padding": "20px", "minHeight": "100vh"},
    children=[
        html.H1("Finanse publiczne — Polska", style={"color": TEXT}),
        html.P("Analiza sektora finansów publicznych w oparciu o dane Eurostat, IMF, Ministerstwo Finansów",
               style={"color": SUBTEXT, "marginBottom": "30px"}),

        # Chart 1: Revenue, Expenditure, Balance
        html.Div(dcc.Graph(figure=_chart1), style={"marginBottom": "30px"}),

        # Chart 2: Debt trajectory
        html.Div(dcc.Graph(figure=_chart2), style={"marginBottom": "30px"}),

        # Chart 3: COFOG breakdown
        html.Div(dcc.Graph(figure=_chart3), style={"marginBottom": "30px"}),

        # Chart 4: EU comparison
        html.Div(dcc.Graph(figure=_chart4), style={"marginBottom": "30px"}),
    ],
)

if __name__ == "__main__":
    log.info("Starting Public Finance Dashboard (TEST) on port %d", PORT)
    app.run(host="0.0.0.0", port=PORT, debug=False)