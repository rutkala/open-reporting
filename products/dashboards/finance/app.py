#!/usr/bin/env python3
"""
Open Reporting — Public Finance Dashboard
Visualises curated.mart_finance: fiscal balance, public debt, revenue/expenditure,
COFOG functional spending, IMF projections, EU comparisons, and source comparison.

Run:
    PYTHONPATH=/opt/open-reporting \
    DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb \
    python3 products/dashboards/finance/app.py
"""
import logging
import os

import pandas as pd
import plotly.graph_objects as go
from dash import Dash, Input, Output, callback, dcc, html, dash_table

import products.visuals.lib.theme as _theme  # noqa: F401 — registers nordic template
from products.visuals.lib.theme import (
    AZURE_1, AZURE_3, BG_PAGE, BG_SURFACE, BORDER,
    COLORWAY, NEGATIVE, POSITIVE, SUBTEXT, TEXT, WARNING,
)
from products.visuals.lib.db import query

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

PORT = int(os.environ.get("OR_PORT", 8053))

# ── EU-27 individual country codes (excludes aggregates and non-members) ─────
EU27 = {
    "AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "EL", "ES",
    "FI", "FR", "HR", "HU", "IE", "IT", "LT", "LU", "LV", "MT",
    "NL", "PL", "PT", "RO", "SE", "SI", "SK",
}

# V4 countries
V4 = {"PL", "CZ", "SK", "HU"}

# COFOG labels (Polish)
COFOG_LABELS = {
    "pub.cofog_01_gdp": "Usługi publiczne",
    "pub.cofog_02_gdp": "Obrona",
    "pub.cofog_03_gdp": "Porządek publiczny",
    "pub.cofog_04_gdp": "Gospodarka",
    "pub.cofog_05_gdp": "Środowisko",
    "pub.cofog_06_gdp": "Mieszkalnictwo",
    "pub.cofog_07_gdp": "Zdrowie",
    "pub.cofog_08_gdp": "Kultura i rekreacja",
    "pub.cofog_09_gdp": "Edukacja",
    "pub.cofog_10_gdp": "Ochrona socjalna",
}
COFOG_IDS = list(COFOG_LABELS.keys())

# Color palette for COFOG (10 distinct colors)
COFOG_COLORS = [
    "#4A7FB5", "#7BAFD4", "#5A7A6E", "#D4874A", "#C0503A",
    "#9BB5C4", "#A8C8E8", "#B5C4C1", "#6B8FA6", "#C5D8E3",
]

# ── Data loading (once at startup) ────────────────────────────────────────────

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

# Pre-slice commonly used subsets
_pl_eurostat = _mart[(_mart["geo"] == "PL") & (_mart["source_id"] == "eurostat")]
_pl_imf      = _mart[(_mart["geo"] == "PL") & (_mart["source_id"] == "imf")]
_pl_dbw      = _mart[(_mart["geo"] == "PL") & (_mart["source_id"] == "dbw")]
_eu27_mask   = _mart["geo"].isin(EU27)

log.info("mart_finance loaded: %d rows", len(_mart))


# ── Helper utilities ──────────────────────────────────────────────────────────

def _latest(df: pd.DataFrame, detail_id: str) -> tuple[float | None, int | None]:
    """Return (value, year) for the latest non-null row."""
    sub = df[df["detail_id"] == detail_id].dropna(subset=["value"])
    if sub.empty:
        return None, None
    row = sub.loc[sub["period_year"].idxmax()]
    return float(row["value"]), int(row["period_year"])


def _eu_rank(detail_id: str, source_id: str, year: int, pl_value: float) -> int | None:
    """Rank of Poland among EU-27 for a given indicator (1 = best/highest)."""
    sub = _mart[
        (_mart["detail_id"] == detail_id) &
        (_mart["source_id"] == source_id) &
        (_mart["period_year"] == year) &
        (_mart["geo"].isin(EU27))
    ].dropna(subset=["value"])
    if sub.empty:
        return None
    # For fiscal balance & debt: lower value = worse, so rank ascending (1=best)
    # We rank by value descending → position of PL
    sorted_vals = sub["value"].sort_values(ascending=False).values
    rank = int(list(sorted_vals).index(pl_value)) + 1 if pl_value in sorted_vals else None
    return rank


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


def _ref_line(fig: go.Figure, y: float, label: str, color: str = NEGATIVE,
              axis: str = "y", is_vertical: bool = False) -> go.Figure:
    """Add a horizontal (or vertical) dashed reference line."""
    if is_vertical:
        fig.add_vline(
            x=y, line_dash="dash", line_color=color, line_width=1.5,
            annotation_text=label, annotation_position="top right",
            annotation_font=dict(color=color, size=11),
        )
    else:
        fig.add_hline(
            y=y, line_dash="dash", line_color=color, line_width=1.5,
            annotation_text=label, annotation_position="top right",
            annotation_font=dict(color=color, size=11),
        )
    return fig


def _card(label: str, value_str: str, rank_str: str, color: str = TEXT,
          badge: tuple[str, str] | None = None,
          trend: tuple[str, str] | None = None) -> html.Div:
    """KPI card component.

    badge: (text, color) — e.g. ("✓ SGP", POSITIVE) or ("✗ SGP", NEGATIVE)
    trend: (arrow+delta, color) — e.g. ("▲ +1,2 pp", NEGATIVE)
    """
    children = [
        html.Div(label, style={"color": SUBTEXT, "fontSize": "13px", "marginBottom": "6px"}),
    ]
    # Value row with optional badge
    value_row = [
        html.Span(value_str, style={"color": color, "fontSize": "26px", "fontWeight": "700"}),
    ]
    if badge:
        badge_text, badge_color = badge
        value_row.append(html.Span(
            badge_text,
            style={
                "fontSize": "11px", "fontWeight": "600",
                "color": badge_color, "background": f"{badge_color}18",
                "border": f"1px solid {badge_color}40",
                "borderRadius": "4px", "padding": "2px 6px",
                "marginLeft": "8px", "verticalAlign": "middle",
            },
        ))
    children.append(html.Div(value_row, style={"display": "flex", "alignItems": "center"}))
    if trend:
        trend_text, trend_color = trend
        children.append(html.Div(
            trend_text,
            style={"color": trend_color, "fontSize": "12px", "marginTop": "3px", "fontWeight": "500"},
        ))
    children.append(html.Div(rank_str, style={"color": SUBTEXT, "fontSize": "12px", "marginTop": "4px"}))
    return html.Div(
        style={
            "background": BG_SURFACE,
            "border": f"1px solid {BORDER}",
            "borderRadius": "8px",
            "padding": "20px 24px",
            "flex": "1",
            "minWidth": "200px",
        },
        children=children,
    )


def _chart_wrapper(fig: go.Figure, h: int = 420) -> dcc.Graph:
    return dcc.Graph(figure=fig, config={"displayModeBar": False},
                     style={"height": f"{h}px"})


# ── Tab 1: Overview (GUS DBW-style) ──────────────────────────────────────────

def _yoy_trend(df: pd.DataFrame, detail_id: str, ascending_is_good: bool = True
               ) -> tuple[str, str] | None:
    """Compute YoY change arrow + delta string and colour for a KPI card."""
    sub = df[df["detail_id"] == detail_id].dropna(subset=["value"]).sort_values("period_year")
    if len(sub) < 2:
        return None
    cur = float(sub.iloc[-1]["value"])
    prev = float(sub.iloc[-2]["value"])
    delta = cur - prev
    if abs(delta) < 0.05:
        return f"→ bez zmian", SUBTEXT
    arrow = "▲" if delta > 0 else "▼"
    sign = "+" if delta > 0 else ""
    text = f"{arrow} {sign}{delta:.1f} pp r/r"
    improving = (delta > 0) == ascending_is_good
    color = POSITIVE if improving else NEGATIVE
    return text, color


def _build_overview_kpis() -> html.Div:
    fiscal_val, fiscal_yr   = _latest(_pl_eurostat, "pub.fiscal_balance_gdp")
    debt_val,   debt_yr     = _latest(_pl_eurostat, "pub.public_debt_gdp")
    revenue_val, revenue_yr = _latest(_pl_dbw,      "pub.govt_revenue")

    fiscal_color = NEGATIVE if (fiscal_val or 0) < -3 else (WARNING if (fiscal_val or 0) < 0 else POSITIVE)
    debt_color   = NEGATIVE if (debt_val or 0) > 60 else TEXT

    # SGP compliance badges
    fiscal_sgp = ("✓ SGP", POSITIVE) if (fiscal_val or 0) >= -3 else ("✗ SGP", NEGATIVE)
    debt_sgp   = ("✓ SGP", POSITIVE) if (debt_val or 0) <= 60 else ("✗ SGP", NEGATIVE)

    # YoY trends (higher fiscal balance = better; lower debt = better)
    fiscal_trend  = _yoy_trend(_pl_eurostat, "pub.fiscal_balance_gdp", ascending_is_good=True)
    debt_trend    = _yoy_trend(_pl_eurostat, "pub.public_debt_gdp",    ascending_is_good=False)
    revenue_trend = _yoy_trend(_pl_dbw,      "pub.govt_revenue",       ascending_is_good=True)

    def _fmt_mld(val: float | None) -> str:
        if val is None:
            return "—"
        return f"{val / 1000:,.1f} mld zł".replace(",", "\u00a0").replace(".", ",")

    return html.Div(
        style={"display": "flex", "gap": "16px", "flexWrap": "wrap", "marginBottom": "24px"},
        children=[
            _card(
                "Saldo finansów publicznych",
                f"{fiscal_val:.1f}% PKB" if fiscal_val is not None else "—",
                f"Eurostat ESA 2010, sektor rządowy ({fiscal_yr})",
                color=fiscal_color,
                badge=fiscal_sgp,
                trend=fiscal_trend,
            ),
            _card(
                "Dług publiczny",
                f"{debt_val:.1f}% PKB" if debt_val is not None else "—",
                f"Kryterium z Maastricht: 60% PKB ({debt_yr})",
                color=debt_color,
                badge=debt_sgp,
                trend=debt_trend,
            ),
            _card(
                "Dochody sektora finansów publ.",
                _fmt_mld(revenue_val),
                f"Dochody ogółem, sektor S13 ({revenue_yr})",
                trend=revenue_trend,
            ),
        ],
    )


def _build_budget_combo_chart() -> go.Figure:
    """Revenue + Expenditure grouped bars with Balance line — DBW HVD, PLN mn."""
    rev  = _ts("pub.govt_revenue",       "PL", "dbw", min_year=1995)
    exp  = _ts("pub.govt_expenditure",   "PL", "dbw", min_year=1995)
    bal  = _ts("pub.net_lending_borrowing", "PL", "dbw", min_year=1995)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=rev["period_year"], y=rev["value"],
        name="Dochody",
        marker_color=AZURE_1,
        offsetgroup=0,
    ))
    fig.add_trace(go.Bar(
        x=exp["period_year"], y=exp["value"],
        name="Wydatki",
        marker_color=AZURE_3,
        offsetgroup=1,
    ))
    fig.add_trace(go.Bar(
        x=bal["period_year"], y=bal["value"],
        name="Saldo",
        marker_color=[NEGATIVE if v < 0 else POSITIVE for v in bal["value"]],
        yaxis="y2",
    ))
    fig.update_layout(
        title="Budżet sektora finansów publicznych (mln zł)",
        barmode="group",
        yaxis=dict(title="mln zł"),
        yaxis2=dict(
            title="Saldo (mln zł)",
            overlaying="y",
            side="right",
            showgrid=False,
        ),
        legend=dict(orientation="h", y=-0.15),
        template="teal",
        height=440,
    )
    return fig


def _build_debt_combo_chart() -> go.Figure:
    """Public debt: PLN mn bars (DBW) + % GDP line (Eurostat) — dual axis."""
    debt_pln = _ts("pub.public_debt_total", "PL", "dbw",      min_year=2000)
    debt_pct = _ts("pub.public_debt_gdp",   "PL", "eurostat", min_year=2000)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=debt_pln["period_year"], y=debt_pln["value"],
        name="Dług (mln zł)",
        marker_color=AZURE_1,
        yaxis="y",
    ))
    fig.add_trace(go.Scatter(
        x=debt_pct["period_year"], y=debt_pct["value"],
        name="Dług (% PKB)",
        line=dict(color=WARNING, width=2),
        mode="lines+markers",
        marker=dict(size=4),
        yaxis="y2",
    ))
    # Maastricht 60% reference on right axis
    fig.add_hline(
        y=60, line_dash="dash", line_color=NEGATIVE, line_width=1.5,
        annotation_text="60% PKB (Maastricht)",
        annotation_position="top right",
        annotation_font=dict(color=NEGATIVE, size=11),
        yref="y2",
    )
    fig.update_layout(
        title="Państwowy dług publiczny (mln zł; % PKB)",
        yaxis=dict(title="mln zł"),
        yaxis2=dict(
            title="% PKB",
            overlaying="y",
            side="right",
            showgrid=False,
        ),
        legend=dict(orientation="h", y=-0.15),
        template="teal",
        height=440,
    )
    return fig


def _rag(value: float | None, green_fn, amber_fn) -> str:
    """Return 'green', 'amber', or 'red' based on threshold functions."""
    if value is None:
        return "red"
    if green_fn(value):
        return "green"
    if amber_fn(value):
        return "amber"
    return "red"


_RAG_COLORS = {"green": POSITIVE, "amber": WARNING, "red": NEGATIVE}
_RAG_LABELS = {"green": "✓", "amber": "△", "red": "✗"}


def _scorecard_tile(label: str, value_str: str, rag: str, trend: tuple | None = None) -> html.Div:
    color = _RAG_COLORS[rag]
    signal = _RAG_LABELS[rag]
    children = [
        html.Div(label, style={"color": SUBTEXT, "fontSize": "12px", "marginBottom": "6px"}),
        html.Div(
            [
                html.Span(signal, style={
                    "fontSize": "16px", "fontWeight": "700", "color": color,
                    "marginRight": "6px",
                }),
                html.Span(value_str, style={
                    "fontSize": "20px", "fontWeight": "700", "color": color,
                }),
            ],
            style={"display": "flex", "alignItems": "baseline"},
        ),
    ]
    if trend:
        trend_text, trend_color = trend
        children.append(html.Div(
            trend_text,
            style={"color": trend_color, "fontSize": "11px", "marginTop": "4px"},
        ))
    return html.Div(
        style={
            "background": BG_SURFACE,
            "border": f"2px solid {color}40",
            "borderLeft": f"4px solid {color}",
            "borderRadius": "8px",
            "padding": "16px 20px",
            "flex": "1",
            "minWidth": "160px",
        },
        children=children,
    )


def _build_scorecard() -> html.Div:
    """4-tile RAG fiscal sustainability scorecard."""
    fiscal_val, fiscal_yr   = _latest(_pl_eurostat, "pub.fiscal_balance_gdp")
    debt_val,   _           = _latest(_pl_eurostat, "pub.public_debt_gdp")
    interest_val, _         = _latest(_pl_eurostat, "pub.interest_expenditure_gdp")
    structural_val, _       = _latest(_pl_imf,      "pub.structural_balance_imf")
    primary_val, _          = _latest(_pl_imf,      "pub.primary_balance_imf")

    fiscal_rag    = _rag(fiscal_val,    lambda v: v >= -3,   lambda v: v >= -5)
    debt_rag      = _rag(debt_val,      lambda v: v < 60,    lambda v: v < 80)
    interest_rag  = _rag(interest_val,  lambda v: v < 2.0,   lambda v: v < 3.0)
    structural_rag = _rag(structural_val, lambda v: v >= -3,  lambda v: v >= -5)

    return html.Div(
        style={"marginBottom": "24px"},
        children=[
            html.Div("Ocena stabilności fiskalnej", style={
                "color": SUBTEXT, "fontSize": "12px",
                "textTransform": "uppercase", "letterSpacing": "0.05em",
                "marginBottom": "10px",
            }),
            html.Div(
                style={"display": "flex", "gap": "12px", "flexWrap": "wrap"},
                children=[
                    _scorecard_tile(
                        "Saldo fiskalne",
                        f"{fiscal_val:.1f}% PKB" if fiscal_val else "—",
                        fiscal_rag,
                        _yoy_trend(_pl_eurostat, "pub.fiscal_balance_gdp", ascending_is_good=True),
                    ),
                    _scorecard_tile(
                        "Dług publiczny",
                        f"{debt_val:.1f}% PKB" if debt_val else "—",
                        debt_rag,
                        _yoy_trend(_pl_eurostat, "pub.public_debt_gdp", ascending_is_good=False),
                    ),
                    _scorecard_tile(
                        "Ciężar odsetkowy",
                        f"{interest_val:.1f}% PKB" if interest_val else "—",
                        interest_rag,
                        _yoy_trend(_pl_eurostat, "pub.interest_expenditure_gdp", ascending_is_good=False),
                    ),
                    _scorecard_tile(
                        "Saldo strukturalne",
                        f"{structural_val:.1f}% PKB" if structural_val else "—",
                        structural_rag,
                        _yoy_trend(_pl_imf, "pub.structural_balance_imf", ascending_is_good=True),
                    ),
                ],
            ),
        ],
    )


def _insight_budget() -> html.Div:
    """Auto-generated Polish insight for the budget combo chart."""
    rev_val, rev_yr  = _latest(_pl_dbw, "pub.govt_revenue")
    exp_val, _       = _latest(_pl_dbw, "pub.govt_expenditure")
    bal_val, _       = _latest(_pl_dbw, "pub.net_lending_borrowing")
    if rev_val is None or exp_val is None or bal_val is None:
        return html.Div()

    bal_pct = (bal_val / rev_val) * 100
    direction = "Deficyt" if bal_val < 0 else "Nadwyżka"
    sign = "+" if bal_val >= 0 else ""
    text = (
        f"{direction} sektora finansów publicznych wyniósł {sign}{bal_val:,.0f} mln zł "
        f"({sign}{bal_pct:.1f}% dochodów) w {rev_yr}."
    )
    return html.Div(text, style={
        "color": SUBTEXT, "fontSize": "12px", "fontStyle": "italic",
        "marginTop": "6px", "paddingLeft": "4px",
        "borderLeft": f"3px solid {BORDER}",
    })


def _insight_debt() -> html.Div:
    """Auto-generated Polish insight for the debt combo chart."""
    debt_pct, yr   = _latest(_pl_eurostat, "pub.public_debt_gdp")
    debt_pln, _    = _latest(_pl_dbw,      "pub.public_debt_total")
    trend          = _yoy_trend(_pl_eurostat, "pub.public_debt_gdp", ascending_is_good=False)
    if debt_pct is None:
        return html.Div()

    gap = 60 - debt_pct
    if debt_pct > 60:
        threshold_note = f"przekracza unijny próg 60% PKB o {abs(gap):.1f} pp"
    elif gap < 5:
        threshold_note = f"jest {gap:.1f} pp poniżej unijnego progu 60% PKB"
    else:
        threshold_note = f"pozostaje poniżej unijnego progu 60% PKB"

    trend_note = ""
    if trend:
        trend_note = f" ({trend[0]})"

    text = f"Dług publiczny wynosi {debt_pct:.1f}% PKB w {yr} i {threshold_note}{trend_note}."
    return html.Div(text, style={
        "color": SUBTEXT, "fontSize": "12px", "fontStyle": "italic",
        "marginTop": "6px", "paddingLeft": "4px",
        "borderLeft": f"3px solid {BORDER}",
    })


def _layout_tab1() -> html.Div:
    return html.Div([
        _build_overview_kpis(),
        _build_scorecard(),
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "16px"},
            children=[
                html.Div([
                    _chart_wrapper(_build_budget_combo_chart(), h=440),
                    _insight_budget(),
                ]),
                html.Div([
                    _chart_wrapper(_build_debt_combo_chart(), h=440),
                    _insight_debt(),
                ]),
            ],
        ),
    ])


# ── Tab 2: EU Comparison ──────────────────────────────────────────────────────

def _build_eu_fiscal_bar(year: int) -> go.Figure:
    df = _mart[
        (_mart["detail_id"] == "pub.fiscal_balance_gdp") &
        (_mart["source_id"] == "eurostat") &
        (_mart["period_year"] == year) &
        (_mart["geo"].isin(EU27))
    ].dropna(subset=["value"]).copy()

    if df.empty:
        return go.Figure().update_layout(title=f"Brak danych dla {year}")

    df = df.sort_values("value", ascending=True)
    colors = [AZURE_1 if g == "PL" else AZURE_3 for g in df["geo"]]
    labels = df["country_name"].fillna(df["geo"])

    fig = go.Figure(go.Bar(
        x=df["value"], y=labels,
        orientation="h",
        marker_color=colors,
        text=df["value"].apply(lambda v: f"{v:.1f}%"),
        textposition="outside",
    ))
    _ref_line(fig, -3, "-3% PKB", is_vertical=True)
    fig.update_layout(
        title=f"Saldo fiskalne sektora rządowego (% PKB), {year}",
        xaxis_title="% PKB",
        template="teal",
        height=max(420, len(df) * 22),
        margin=dict(l=120, r=60, t=48, b=40),
    )
    return fig


def _build_eu_debt_bar(year: int) -> go.Figure:
    df = _mart[
        (_mart["detail_id"] == "pub.gross_debt_imf") &
        (_mart["source_id"] == "imf") &
        (_mart["period_year"] == year) &
        (_mart["geo"].isin(EU27)) &
        (_mart["is_projection"].ne(True))
    ].dropna(subset=["value"]).copy()

    if df.empty:
        return go.Figure().update_layout(title=f"Brak danych dla {year}")

    df = df.sort_values("value", ascending=False)
    colors = [AZURE_1 if g == "PL" else AZURE_3 for g in df["geo"]]
    labels = df["country_name"].fillna(df["geo"])

    fig = go.Figure(go.Bar(
        x=df["value"], y=labels,
        orientation="h",
        marker_color=colors,
        text=df["value"].apply(lambda v: f"{v:.1f}%"),
        textposition="outside",
    ))
    _ref_line(fig, 60, "60% PKB", is_vertical=True)
    fig.update_layout(
        title=f"Dług publiczny brutto (% PKB), {year}",
        xaxis_title="% PKB",
        template="teal",
        height=max(420, len(df) * 22),
        margin=dict(l=120, r=60, t=48, b=40),
    )
    return fig


def _layout_tab2() -> html.Div:
    # Available years for EU fiscal comparison (eurostat)
    avail_years = sorted(
        _mart[
            (_mart["detail_id"] == "pub.fiscal_balance_gdp") &
            (_mart["source_id"] == "eurostat") &
            (_mart["geo"].isin(EU27))
        ]["period_year"].dropna().unique().tolist(),
        reverse=True,
    )
    default_year = 2024 if 2024 in avail_years else avail_years[0] if avail_years else 2023

    return html.Div([
        html.Div(
            style={"marginBottom": "16px", "display": "flex", "alignItems": "center", "gap": "12px"},
            children=[
                html.Label("Rok:", style={"color": TEXT, "fontWeight": "600"}),
                dcc.Dropdown(
                    id="eu-year-selector",
                    options=[{"label": str(y), "value": y} for y in avail_years],
                    value=default_year,
                    clearable=False,
                    style={"width": "120px"},
                ),
            ],
        ),
        html.Div(id="eu-fiscal-bar-container"),
        html.Div(style={"height": "16px"}),
        html.Div(id="eu-debt-bar-container"),
    ])


# ── Tab 3: Revenue & Expenditure ──────────────────────────────────────────────

def _build_revenue_chart() -> go.Figure:
    INDICATORS = {
        "pub.revenue_gdp":            ("Dochody ogółem",           AZURE_1),
        "pub.taxes_prod_imports_gdp": ("Podatki od produkcji",     COLORWAY[1]),
        "pub.taxes_income_gdp":       ("Podatki dochodowe",        COLORWAY[3]),
        "pub.social_contributions_gdp": ("Składki społeczne",      COLORWAY[4]),
    }
    fig = go.Figure()
    for detail_id, (label, color) in INDICATORS.items():
        df = _ts(detail_id, "PL", "eurostat", min_year=1995)
        if not df.empty:
            fig.add_trace(go.Scatter(
                x=df["period_year"], y=df["value"],
                name=label, line=dict(color=color, width=2), mode="lines",
            ))
    fig.update_layout(
        title="Dochody podatkowe Polski (% PKB)",
        yaxis_title="% PKB",
        template="teal",
        height=420,
    )
    return fig


def _build_expenditure_chart() -> go.Figure:
    INDICATORS = {
        "pub.expenditure_gdp":           ("Wydatki ogółem",              AZURE_1),
        "pub.interest_expenditure_gdp":  ("Koszty obsługi długu",        COLORWAY[1]),
        "pub.govt_investment_gdp":       ("Inwestycje publiczne",        COLORWAY[2]),
        "pub.social_transfers_gdp":      ("Transfery społeczne",         COLORWAY[3]),
        "pub.compensation_employees_gdp": ("Wynagrodzenia pracowników",  COLORWAY[4]),
    }
    fig = go.Figure()
    for detail_id, (label, color) in INDICATORS.items():
        df = _ts(detail_id, "PL", "eurostat", min_year=1995)
        if not df.empty:
            fig.add_trace(go.Scatter(
                x=df["period_year"], y=df["value"],
                name=label, line=dict(color=color, width=2), mode="lines",
            ))
    fig.update_layout(
        title="Struktura wydatków publicznych Polski (% PKB)",
        yaxis_title="% PKB",
        template="teal",
        height=420,
    )
    return fig


def _layout_tab3() -> html.Div:
    return html.Div(
        style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "16px"},
        children=[
            _chart_wrapper(_build_revenue_chart()),
            _chart_wrapper(_build_expenditure_chart()),
        ],
    )


# ── Tab 4: COFOG Functional Spending ─────────────────────────────────────────

def _build_cofog_stacked_bar() -> go.Figure:
    fig = go.Figure()
    for idx, (detail_id, label) in enumerate(COFOG_LABELS.items()):
        df = _ts(detail_id, "PL", "eurostat", min_year=1995)
        if not df.empty:
            fig.add_trace(go.Bar(
                x=df["period_year"], y=df["value"],
                name=label, marker_color=COFOG_COLORS[idx],
            ))
    fig.update_layout(
        barmode="stack",
        title="Wydatki Polski wg funkcji COFOG (% PKB)",
        yaxis_title="% PKB",
        template="teal",
        height=420,
    )
    return fig


def _build_cofog_comparison_bar() -> go.Figure:
    """Horizontal grouped bar: Poland vs EU27 for each COFOG function (latest year)."""
    # Find latest year with COFOG data for both PL and EU27_2020
    df_all = _mart[
        (_mart["detail_id"].isin(COFOG_IDS)) &
        (_mart["source_id"] == "eurostat") &
        (_mart["geo"].isin(["PL", "EU27_2020"]))
    ].dropna(subset=["value"])

    if df_all.empty:
        return go.Figure().update_layout(title="Brak danych COFOG")

    latest_year = int(df_all["period_year"].max())

    df = df_all[df_all["period_year"] == latest_year].copy()
    pl_df  = df[df["geo"] == "PL"].set_index("detail_id")
    eu_df  = df[df["geo"] == "EU27_2020"].set_index("detail_id")

    # Sort by EU27 value descending
    eu_sorted = eu_df["value"].reindex(COFOG_IDS).sort_values(ascending=True)
    sorted_ids = eu_sorted.index.tolist()
    labels = [COFOG_LABELS[d] for d in sorted_ids]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=labels,
        x=[eu_df["value"].get(d, None) for d in sorted_ids],
        name="UE-27", orientation="h", marker_color=SUBTEXT,
    ))
    fig.add_trace(go.Bar(
        y=labels,
        x=[pl_df["value"].get(d, None) for d in sorted_ids],
        name="Polska", orientation="h", marker_color=AZURE_1,
    ))
    fig.update_layout(
        barmode="group",
        title=f"Porównanie struktury wydatków COFOG: Polska vs UE, {latest_year}",
        xaxis_title="% PKB",
        template="teal",
        height=500,
        margin=dict(l=140, r=40, t=48, b=40),
    )
    return fig


def _layout_tab4() -> html.Div:
    return html.Div([
        _chart_wrapper(_build_cofog_stacked_bar()),
        html.Div(style={"height": "16px"}),
        _chart_wrapper(_build_cofog_comparison_bar(), h=500),
    ])


# ── Tab 5: IMF Projections ────────────────────────────────────────────────────

def _build_imf_fiscal_chart(geos: list[str]) -> go.Figure:
    fig = go.Figure()

    COLORS = [AZURE_1, WARNING, POSITIVE, COLORWAY[3]]
    NAMES  = {"PL": "Polska", "CZ": "Czechy", "SK": "Słowacja", "HU": "Węgry"}

    for i, geo in enumerate(geos):
        df = _ts("pub.fiscal_balance_imf", geo, "imf", min_year=2000)
        if df.empty:
            continue
        actual = df[df["is_projection"].ne(True)]
        proj   = df[df["is_projection"] == True]  # noqa: E712
        color  = COLORS[i % len(COLORS)]
        name   = NAMES.get(geo, geo)

        if not actual.empty:
            fig.add_trace(go.Scatter(
                x=actual["period_year"], y=actual["value"],
                name=f"{name} (historia)", line=dict(color=color, width=2),
                mode="lines",
            ))
        if not proj.empty:
            if not actual.empty:
                proj = pd.concat([actual.iloc[[-1]], proj])
            fig.add_trace(go.Scatter(
                x=proj["period_year"], y=proj["value"],
                name=f"{name} (prognoza)", line=dict(color=color, width=2, dash="dash"),
                mode="lines", showlegend=(geo == "PL"),
            ))

    # Primary and structural balance for Poland (first selected)
    if "PL" in geos:
        for detail_id, label in [
            ("pub.primary_balance_imf",    "Saldo pierwotne PL"),
            ("pub.structural_balance_imf", "Saldo strukturalne PL"),
        ]:
            df = _ts(detail_id, "PL", "imf", min_year=2000)
            if not df.empty:
                fig.add_trace(go.Scatter(
                    x=df["period_year"], y=df["value"],
                    name=label, line=dict(width=1.5, dash="dot"),
                    mode="lines",
                ))

    _ref_line(fig, -3, "-3% PKB (Maastricht)")
    fig.update_layout(
        title="Saldo fiskalne Polski — historia i prognozy MFW (% PKB)",
        yaxis_title="% PKB",
        template="teal",
        height=420,
    )
    return fig


def _build_imf_debt_chart(geos: list[str]) -> go.Figure:
    fig = go.Figure()

    COLORS = [AZURE_1, WARNING, POSITIVE, COLORWAY[3]]
    NAMES  = {"PL": "Polska", "CZ": "Czechy", "SK": "Słowacja", "HU": "Węgry"}

    for i, geo in enumerate(geos):
        df = _ts("pub.gross_debt_imf", geo, "imf", min_year=2000)
        if df.empty:
            continue
        actual = df[df["is_projection"].ne(True)]
        proj   = df[df["is_projection"] == True]  # noqa: E712
        color  = COLORS[i % len(COLORS)]
        name   = NAMES.get(geo, geo)

        if not actual.empty:
            fig.add_trace(go.Scatter(
                x=actual["period_year"], y=actual["value"],
                name=f"{name} (historia)", line=dict(color=color, width=2),
                mode="lines",
            ))
        if not proj.empty:
            if not actual.empty:
                proj = pd.concat([actual.iloc[[-1]], proj])
            fig.add_trace(go.Scatter(
                x=proj["period_year"], y=proj["value"],
                name=f"{name} (prognoza)", line=dict(color=color, width=2, dash="dash"),
                mode="lines", showlegend=(geo == "PL"),
            ))

    _ref_line(fig, 60, "60% PKB (Maastricht)")
    fig.update_layout(
        title="Dług publiczny — historia i prognozy MFW (% PKB)",
        yaxis_title="% PKB",
        template="teal",
        height=420,
    )
    return fig


def _layout_tab5() -> html.Div:
    country_options = [
        {"label": "Polska (PL)",        "value": "PL"},
        {"label": "Czechy (CZ)",        "value": "CZ"},
        {"label": "Słowacja (SK)",      "value": "SK"},
        {"label": "Węgry (HU)",         "value": "HU"},
    ]
    return html.Div([
        html.Div(
            style={"marginBottom": "16px", "display": "flex", "alignItems": "center", "gap": "12px"},
            children=[
                html.Label("Porównaj kraje:", style={"color": TEXT, "fontWeight": "600"}),
                dcc.Dropdown(
                    id="imf-country-selector",
                    options=country_options,
                    value=["PL"],
                    multi=True,
                    style={"width": "400px"},
                ),
            ],
        ),
        html.Div(id="imf-fiscal-chart-container"),
        html.Div(style={"height": "16px"}),
        html.Div(id="imf-debt-chart-container"),
    ])


# ── Tab 6: Explorer ───────────────────────────────────────────────────────────

def _layout_tab6() -> html.Div:
    # Load distinct indicators from all_indicators for domain PUB
    try:
        ind_df = query(
            "SELECT DISTINCT detail_id, detail_name FROM curated.all_indicators "
            "WHERE domain_id = 'PUB' ORDER BY detail_id"
        )
        indicator_opts = [
            {"label": f"{r.detail_id} — {r.detail_name}", "value": r.detail_id}
            for r in ind_df.itertuples()
        ]
    except Exception:
        log.exception("Could not load indicator list for Explorer")
        indicator_opts = []

    # Country options from mart_finance
    country_opts = sorted(
        [
            {"label": f"{row.country_name} ({row.geo})", "value": row.geo}
            for _, row in _mart[["geo", "country_name"]].drop_duplicates().iterrows()
            if row.country_name
        ],
        key=lambda x: x["label"],
    )

    return html.Div([
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "2fr 1fr 1fr", "gap": "12px",
                   "marginBottom": "16px"},
            children=[
                html.Div([
                    html.Label("Wskaźnik:", style={"color": TEXT, "fontWeight": "600",
                                                   "display": "block", "marginBottom": "6px"}),
                    dcc.Dropdown(
                        id="explorer-indicator",
                        options=indicator_opts,
                        value=indicator_opts[0]["value"] if indicator_opts else None,
                        clearable=False,
                    ),
                ]),
                html.Div([
                    html.Label("Kraj/kraje:", style={"color": TEXT, "fontWeight": "600",
                                                     "display": "block", "marginBottom": "6px"}),
                    dcc.Dropdown(
                        id="explorer-countries",
                        options=country_opts,
                        value=["PL"],
                        multi=True,
                    ),
                ]),
                html.Div([
                    html.Label("Zakres lat:", style={"color": TEXT, "fontWeight": "600",
                                                     "display": "block", "marginBottom": "6px"}),
                    dcc.RangeSlider(
                        id="explorer-year-range",
                        min=1980, max=2029, step=1,
                        value=[1995, 2024],
                        marks={y: str(y) for y in range(1980, 2030, 5)},
                        tooltip={"placement": "bottom", "always_visible": False},
                    ),
                ]),
            ],
        ),
        html.Div(id="explorer-chart-container"),
    ])


# ── Tab 7: Source Comparison ──────────────────────────────────────────────────

# Indicators available in both eurostat and imf
_MULTI_SOURCE_INDICATORS = {
    "pub.fiscal_balance_gdp / pub.fiscal_balance_imf": ("Saldo fiskalne (% PKB)",
                                                          "pub.fiscal_balance_gdp",
                                                          "pub.fiscal_balance_imf"),
    "pub.revenue_gdp / pub.revenue_imf":               ("Dochody publiczne (% PKB)",
                                                         "pub.revenue_gdp",
                                                         "pub.revenue_imf"),
    "pub.expenditure_gdp / pub.expenditure_imf":       ("Wydatki publiczne (% PKB)",
                                                         "pub.expenditure_gdp",
                                                         "pub.expenditure_imf"),
}


def _layout_tab7() -> html.Div:
    ind_opts = [
        {"label": v[0], "value": k}
        for k, v in _MULTI_SOURCE_INDICATORS.items()
    ]
    country_opts = sorted(
        [
            {"label": f"{row.country_name} ({row.geo})", "value": row.geo}
            for _, row in _mart[_mart["geo"].isin(EU27)][["geo", "country_name"]]
                .drop_duplicates().iterrows()
            if row.country_name
        ],
        key=lambda x: x["label"],
    )
    return html.Div([
        html.Div(
            style={"display": "flex", "gap": "16px", "marginBottom": "16px", "flexWrap": "wrap"},
            children=[
                html.Div([
                    html.Label("Wskaźnik:", style={"color": TEXT, "fontWeight": "600",
                                                   "display": "block", "marginBottom": "6px"}),
                    dcc.Dropdown(
                        id="src-indicator",
                        options=ind_opts,
                        value=ind_opts[0]["value"] if ind_opts else None,
                        clearable=False,
                        style={"width": "340px"},
                    ),
                ]),
                html.Div([
                    html.Label("Kraj:", style={"color": TEXT, "fontWeight": "600",
                                              "display": "block", "marginBottom": "6px"}),
                    dcc.Dropdown(
                        id="src-country",
                        options=country_opts,
                        value="PL",
                        clearable=False,
                        style={"width": "220px"},
                    ),
                ]),
            ],
        ),
        html.Div(id="src-chart-container"),
        html.Div(style={"height": "16px"}),
        html.Div(id="src-table-container"),
    ])


# ── App layout ─────────────────────────────────────────────────────────────────

_TAB_STYLE = {
    "padding": "10px 20px",
    "color": SUBTEXT,
    "borderBottom": f"2px solid {BORDER}",
    "fontFamily": "Inter, 'Segoe UI', system-ui, sans-serif",
}
_TAB_SELECTED_STYLE = {
    **_TAB_STYLE,
    "color": AZURE_1,
    "borderBottom": f"2px solid {AZURE_1}",
    "fontWeight": "600",
}


def _build_layout() -> html.Div:
    return html.Div(
        style={"backgroundColor": BG_PAGE, "minHeight": "100vh",
               "fontFamily": "Inter, 'Segoe UI', system-ui, sans-serif"},
        children=[
            # Header
            html.Div(
                style={"backgroundColor": BG_SURFACE, "borderBottom": f"1px solid {BORDER}",
                       "padding": "16px 32px"},
                children=[
                    html.H1("Finanse publiczne", style={"color": TEXT, "margin": 0,
                                                        "fontSize": "22px", "fontWeight": "700"}),
                    html.Span("Open Reporting · Źródło: Eurostat, MFW",
                              style={"color": SUBTEXT, "fontSize": "12px"}),
                ],
            ),
            # Tabs
            html.Div(
                style={"padding": "24px 32px"},
                children=[
                    dcc.Tabs(
                        id="main-tabs",
                        value="tab-overview",
                        style={"marginBottom": "24px"},
                        children=[
                            dcc.Tab(label="Przegląd",            value="tab-overview",
                                    style=_TAB_STYLE, selected_style=_TAB_SELECTED_STYLE),
                            dcc.Tab(label="Porównanie UE",        value="tab-eu",
                                    style=_TAB_STYLE, selected_style=_TAB_SELECTED_STYLE),
                            dcc.Tab(label="Dochody i Wydatki",    value="tab-rev-exp",
                                    style=_TAB_STYLE, selected_style=_TAB_SELECTED_STYLE),
                            dcc.Tab(label="Funkcje COFOG",        value="tab-cofog",
                                    style=_TAB_STYLE, selected_style=_TAB_SELECTED_STYLE),
                            dcc.Tab(label="Prognozy MFW",         value="tab-imf",
                                    style=_TAB_STYLE, selected_style=_TAB_SELECTED_STYLE),
                            dcc.Tab(label="Explorer",             value="tab-explorer",
                                    style=_TAB_STYLE, selected_style=_TAB_SELECTED_STYLE),
                            dcc.Tab(label="Porównanie źródeł",    value="tab-sources",
                                    style=_TAB_STYLE, selected_style=_TAB_SELECTED_STYLE),
                        ],
                    ),
                    html.Div(id="tab-content"),
                ],
            ),
        ],
    )


# ── App instantiation ──────────────────────────────────────────────────────────

app = Dash(
    __name__,
    title="Finanse publiczne — Open Reporting",
    suppress_callback_exceptions=True,
    requests_pathname_prefix="/finance/",
    routes_pathname_prefix="/finance/",
)
app.layout = _build_layout()
server = app.server  # expose for production WSGI


# ── Callbacks ─────────────────────────────────────────────────────────────────

@app.callback(Output("tab-content", "children"), Input("main-tabs", "value"))
def render_tab(tab: str):
    if tab == "tab-overview":
        return _layout_tab1()
    if tab == "tab-eu":
        return _layout_tab2()
    if tab == "tab-rev-exp":
        return _layout_tab3()
    if tab == "tab-cofog":
        return _layout_tab4()
    if tab == "tab-imf":
        return _layout_tab5()
    if tab == "tab-explorer":
        return _layout_tab6()
    if tab == "tab-sources":
        return _layout_tab7()
    return html.Div("Nieznana zakładka")


@app.callback(
    Output("eu-fiscal-bar-container", "children"),
    Output("eu-debt-bar-container",   "children"),
    Input("eu-year-selector", "value"),
)
def update_eu_charts(year):
    if year is None:
        return html.Div(), html.Div()
    return (
        _chart_wrapper(_build_eu_fiscal_bar(int(year)), h=max(420, 27 * 22)),
        _chart_wrapper(_build_eu_debt_bar(int(year)),   h=max(420, 27 * 22)),
    )


@app.callback(
    Output("imf-fiscal-chart-container", "children"),
    Output("imf-debt-chart-container",   "children"),
    Input("imf-country-selector", "value"),
)
def update_imf_charts(geos):
    if not geos:
        geos = ["PL"]
    return (
        _chart_wrapper(_build_imf_fiscal_chart(geos)),
        _chart_wrapper(_build_imf_debt_chart(geos)),
    )


@app.callback(
    Output("explorer-chart-container", "children"),
    Input("explorer-indicator",   "value"),
    Input("explorer-countries",   "value"),
    Input("explorer-year-range",  "value"),
)
def update_explorer(detail_id, geos, year_range):
    if not detail_id or not geos or not year_range:
        return html.Div("Wybierz wskaźnik i kraj.")

    try:
        df = query(
            "SELECT geo, period_year, value, country_name "
            "FROM curated.all_indicators "
            "WHERE detail_id = ? AND geo = ANY(?) "
            "  AND EXTRACT(YEAR FROM period_date) BETWEEN ? AND ? "
            "ORDER BY geo, period_year",
            (detail_id, geos, year_range[0], year_range[1]),
        )
    except Exception:
        log.exception("Explorer query failed")
        return html.Div("Błąd pobierania danych.")

    if df.empty:
        return html.Div("Brak danych dla wybranych parametrów.")

    fig = go.Figure()
    for geo in geos:
        sub = df[df["geo"] == geo]
        if sub.empty:
            continue
        name = sub["country_name"].iloc[0] if "country_name" in sub.columns else geo
        fig.add_trace(go.Scatter(
            x=sub["period_year"], y=sub["value"],
            name=str(name) if name else geo,
            mode="lines+markers" if len(sub) < 20 else "lines",
            line=dict(width=2),
        ))
    fig.update_layout(
        title=detail_id,
        template="teal",
        height=450,
    )
    return _chart_wrapper(fig, h=450)


@app.callback(
    Output("src-chart-container", "children"),
    Output("src-table-container", "children"),
    Input("src-indicator", "value"),
    Input("src-country",   "value"),
)
def update_source_comparison(indicator_key, geo):
    if not indicator_key or not geo:
        return html.Div(), html.Div()

    label, estat_id, imf_id = _MULTI_SOURCE_INDICATORS[indicator_key]

    df_estat = _ts(estat_id, geo, "eurostat", min_year=1995)
    df_imf   = _ts(imf_id,   geo, "imf",      min_year=1995)

    fig = go.Figure()
    if not df_estat.empty:
        fig.add_trace(go.Scatter(
            x=df_estat["period_year"], y=df_estat["value"],
            name="Eurostat", line=dict(color=AZURE_1, width=2), mode="lines",
        ))
    if not df_imf.empty:
        actual_imf = df_imf[df_imf["is_projection"].ne(True)]
        fig.add_trace(go.Scatter(
            x=actual_imf["period_year"], y=actual_imf["value"],
            name="MFW (historia)", line=dict(color=WARNING, width=2), mode="lines",
        ))

    fig.update_layout(
        title=f"{label} — Eurostat vs MFW",
        yaxis_title="% PKB",
        template="teal",
        height=420,
    )

    # Comparison table
    merged = pd.merge(
        df_estat[["period_year", "value"]].rename(columns={"value": "eurostat"}),
        df_imf[df_imf["is_projection"].ne(True)][["period_year", "value"]].rename(
            columns={"value": "imf"}),
        on="period_year", how="outer",
    ).sort_values("period_year", ascending=False)

    merged["różnica"] = (merged["eurostat"] - merged["imf"]).round(2)
    merged["eurostat"] = merged["eurostat"].apply(lambda v: f"{v:.2f}%" if pd.notna(v) else "—")
    merged["imf"]      = merged["imf"].apply(lambda v: f"{v:.2f}%" if pd.notna(v) else "—")
    merged["różnica"]  = merged["różnica"].apply(lambda v: f"{v:+.2f}%" if pd.notna(v) else "—")
    merged.rename(columns={"period_year": "Rok", "eurostat": "Eurostat",
                            "imf": "MFW", "różnica": "Różnica"}, inplace=True)

    table = dash_table.DataTable(
        data=merged.to_dict("records"),
        columns=[{"name": c, "id": c} for c in merged.columns],
        style_header={"backgroundColor": BG_SURFACE, "color": TEXT,
                      "fontWeight": "600", "borderBottom": f"2px solid {BORDER}"},
        style_data={"backgroundColor": BG_SURFACE, "color": TEXT,
                    "borderBottom": f"1px solid {BORDER}"},
        style_table={"overflowX": "auto"},
        page_size=20,
        style_cell={"fontFamily": "Inter, 'Segoe UI', sans-serif", "fontSize": "13px",
                    "padding": "8px 12px"},
    )

    return _chart_wrapper(fig), table


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    log.info("Starting Public Finance dashboard on port %d", PORT)
    app.run(host="0.0.0.0", port=PORT, debug=False)
