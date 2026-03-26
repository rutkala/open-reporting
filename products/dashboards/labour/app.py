#!/usr/bin/env python3
"""
Open Reporting — Dash portal
Layout, chart titles, units, formatting and section grouping all derived
from the semantic model. Adding a measure to labour.yml automatically
reflects here — no code changes needed.
Run: python3 products/dashboards/labour/app.py
"""
import logging

import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback

import products.visuals.lib.theme as _theme  # noqa: F401 — registers nordic template
from products.visuals.lib.theme import AZURE_1, AZURE_3, BG_PAGE, BG_SURFACE, BORDER, COLORWAY, SUBTEXT, TEXT
from products import semantic
from products.semantic.models import Measure

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

# ── Semantic model ────────────────────────────────────────────────────────────

DOMAIN  = "labour"
domain  = semantic.get_domain(DOMAIN)

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

def _label(r: str) -> str:
    return REGION_LABELS.get(r.upper(), r.title())

def _raw_regions(display_regions: list[str]) -> list[str]:
    return [k for k, v in REGION_LABELS.items() if v in display_regions]

def _add_label(df):
    df = df.copy()
    df["region_label"] = df["region"].apply(_label)
    return df

# ── Reference data (loaded once at startup) ───────────────────────────────────

_ref      = semantic.query("unemployment_rate", domain=DOMAIN, group_by=["region", "year"])
all_regions = sorted([_label(r) for r in _ref["region"].unique()])
all_years   = sorted(_ref["year"].unique().tolist())
min_year, max_year = all_years[0], all_years[-1]

# ── Derive chart IDs from domain sections ─────────────────────────────────────
# For each measure in each section: one trend chart + one ranking chart.

def _trend_id(measure_id: str) -> str: return f"chart-{measure_id}-trend"
def _rank_id(measure_id: str)  -> str: return f"chart-{measure_id}-rank"

# Flat ordered list of measures across all sections (preserves section order)
section_measures: list[tuple[str, Measure]] = []   # (section_label, measure)
for section in domain.sections:
    for mid in section.measures:
        section_measures.append((section.label, domain.get_measure(mid)))

# ── App ───────────────────────────────────────────────────────────────────────

app = Dash(
    __name__,
    title=f"Open Reporting — {domain.label}",
    suppress_callback_exceptions=True,
    requests_pathname_prefix="/labour/",
    routes_pathname_prefix="/labour/",
)

# ── Styles ────────────────────────────────────────────────────────────────────

S = {
    "body": {
        "fontFamily": "Inter, 'Segoe UI', system-ui, sans-serif",
        "background": BG_PAGE, "color": TEXT,
        "minHeight": "100vh", "display": "flex", "flexDirection": "column", "margin": 0,
    },
    "header": {
        "background": BG_SURFACE, "borderBottom": f"1px solid {BORDER}",
        "padding": "16px 32px", "display": "flex", "alignItems": "baseline",
        "gap": "24px", "flexShrink": 0,
    },
    "page_header": {
        "background": BG_SURFACE, "borderBottom": f"1px solid {BORDER}",
        "padding": "24px 32px 20px",
    },
    "layout": {"display": "flex", "flex": 1},
    "filter_pane": {
        "width": "220px", "flexShrink": 0,
        "background": BG_SURFACE, "borderRight": f"1px solid {BORDER}",
        "padding": "20px 16px", "position": "sticky",
        "top": 0, "height": "100vh", "overflowY": "auto",
    },
    "main": {"flex": 1, "padding": "28px 24px 56px", "minWidth": 0},
    "filter_label": {
        "fontSize": "11px", "fontWeight": 600, "textTransform": "uppercase",
        "letterSpacing": "0.07em", "color": SUBTEXT, "marginBottom": "10px",
    },
    "section_label": {
        "fontSize": "11px", "fontWeight": 600, "textTransform": "uppercase",
        "letterSpacing": "0.08em", "color": SUBTEXT,
        "marginBottom": "14px", "paddingBottom": "8px",
        "borderBottom": f"1px solid {BORDER}",
    },
    "card": {
        "background": BG_SURFACE, "borderRadius": "6px",
        "boxShadow": "0 1px 4px rgba(0,0,0,0.07), 0 0 1px rgba(0,0,0,0.04)",
        "padding": "16px",
    },
    "grid2": {"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px", "marginBottom": "20px"},
    "grid1": {"display": "grid", "gridTemplateColumns": "1fr", "gap": "20px", "marginBottom": "20px"},
    "footer": {
        "background": BG_SURFACE, "borderTop": f"1px solid {BORDER}",
        "padding": "16px 32px", "fontSize": "12px", "color": SUBTEXT,
        "display": "flex", "justifyContent": "space-between", "flexShrink": 0,
    },
}

# ── Layout — generated from domain sections ───────────────────────────────────

def _chart_card(chart_id: str) -> html.Div:
    return html.Div(style=S["card"], children=[
        dcc.Graph(id=chart_id, config={"displayModeBar": False}),
    ])


def _build_sections() -> list[html.Section]:
    """Build one HTML section per domain section, one row (trend + rank) per measure."""
    sections = []
    for section in domain.sections:
        rows = []
        for mid in section.measures:
            rows.append(html.Div(style=S["grid2"], children=[
                _chart_card(_trend_id(mid)),
                _chart_card(_rank_id(mid)),
            ]))
        sections.append(html.Section(style={"marginBottom": "36px"}, children=[
            html.H2(section.label, style=S["section_label"]),
            *rows,
        ]))
    return sections


app.layout = html.Div(style=S["body"], children=[

    html.Header(style=S["header"], children=[
        html.A("Open Reporting", href="/",
               style={"fontSize": "15px", "fontWeight": 600, "color": TEXT, "textDecoration": "none"}),
        html.Nav(children=[
            html.A(domain.label, href="#",
                   style={"fontSize": "13px", "color": SUBTEXT, "textDecoration": "none"}),
        ]),
    ]),

    html.Div(style=S["page_header"], children=[
        html.H1(domain.label,
                style={"fontSize": "24px", "fontWeight": 700, "color": TEXT, "marginBottom": "4px"}),
        html.P(domain.description, style={"fontSize": "13px", "color": SUBTEXT}),
    ]),

    html.Div(style=S["layout"], children=[

        html.Aside(style=S["filter_pane"], children=[
            html.Div(style={"marginBottom": "24px"}, children=[
                html.Div("Województwa", style=S["filter_label"]),
                dcc.Checklist(
                    id="filter-regions",
                    options=[{"label": r, "value": r} for r in all_regions],
                    value=all_regions,
                    inputStyle={"marginRight": "7px", "accentColor": AZURE_1},
                    labelStyle={"display": "block", "fontSize": "12px",
                                "color": TEXT, "marginBottom": "5px", "cursor": "pointer"},
                ),
            ]),
            html.Div(style={"marginBottom": "24px"}, children=[
                html.Div("Zakres lat — trendy", style=S["filter_label"]),
                html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "8px"}, children=[
                    html.Div([
                        html.Label("Od", style={"fontSize": "11px", "color": SUBTEXT,
                                                "display": "block", "marginBottom": "4px"}),
                        dcc.Dropdown(id="year-from",
                                     options=[{"label": y, "value": y} for y in all_years],
                                     value=min_year, clearable=False, style={"fontSize": "12px"}),
                    ]),
                    html.Div([
                        html.Label("Do", style={"fontSize": "11px", "color": SUBTEXT,
                                               "display": "block", "marginBottom": "4px"}),
                        dcc.Dropdown(id="year-to",
                                     options=[{"label": y, "value": y} for y in all_years],
                                     value=max_year, clearable=False, style={"fontSize": "12px"}),
                    ]),
                ]),
            ]),
            html.Div(style={"marginBottom": "24px"}, children=[
                html.Div("Rok — rankingi", style=S["filter_label"]),
                dcc.Dropdown(id="ranking-year",
                             options=[{"label": y, "value": y} for y in all_years],
                             value=max_year, clearable=False, style={"fontSize": "12px"}),
            ]),
        ]),

        html.Main(style=S["main"], children=_build_sections()),
    ]),

    html.Footer(style=S["footer"], children=[
        html.Span(f"Dane: {domain.description}"),
        html.A("bdl.stat.gov.pl", href="https://bdl.stat.gov.pl/", style={"color": SUBTEXT}),
    ]),
])

# ── Chart builders — driven by Measure metadata ───────────────────────────────

def _trend_fig(df, measure: Measure) -> go.Figure:
    fig = go.Figure()
    for i, region in enumerate(sorted(df["region_label"].unique())):
        sub = df[df["region_label"] == region].dropna(subset=[measure.id]).sort_values("year")
        fig.add_trace(go.Scatter(
            x=sub["year"], y=sub[measure.id].astype(float),
            name=region, mode="lines",
            line=dict(color=COLORWAY[i % len(COLORWAY)], width=1.5),
            hovertemplate=f"<b>{region}</b><br>%{{x}}: %{{y:{measure.hover_fmt}}}<extra></extra>",
        ))
    fig.update_layout(
        title=f"{measure.label} według województw",
        xaxis_title=None,
        yaxis_title=measure.axis_label,
        legend=dict(orientation="v", yanchor="top", y=1.0,
                    xanchor="left", x=1.01, font=dict(size=11)),
        margin=dict(l=60, r=160, t=48, b=40), height=380,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def _rank_fig(df, measure: Measure, year: int) -> go.Figure:
    sub = df.dropna(subset=[measure.id]).sort_values(measure.id)
    if sub.empty:
        return go.Figure()
    values = sub[measure.id].astype(float).tolist()
    avg    = sum(values) / len(values)
    colors = [AZURE_1 if (measure.higher_is_better == (v >= avg)) else AZURE_3 for v in values]
    fig = go.Figure(go.Bar(
        x=values, y=sub["region_label"].tolist(), orientation="h",
        marker_color=colors,
        text=[measure.fmt(v) for v in values], textposition="outside",
        hovertemplate=f"<b>%{{y}}</b><br>{measure.axis_label}: %{{x}}<extra></extra>",
    ))
    fig.add_vline(
        x=avg, line_dash="dot", line_color=SUBTEXT, line_width=1.5,
        annotation_text=f"Średnia: {measure.fmt(avg)}",
        annotation_position="top right",
        annotation_font_color=SUBTEXT, annotation_font_size=11,
    )
    fig.update_layout(
        title=f"Ranking — {measure.label.lower()} ({year} r.)",
        xaxis_title=measure.axis_label,
        yaxis_title=None,
        height=480, margin=dict(l=180, r=80, t=48, b=40),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig

# ── Callback — outputs derived from domain sections ───────────────────────────

_outputs = []
for _, m in section_measures:
    _outputs.append(Output(_trend_id(m.id), "figure"))
    _outputs.append(Output(_rank_id(m.id),  "figure"))


@callback(
    *_outputs,
    Input("filter-regions", "value"),
    Input("year-from",       "value"),
    Input("year-to",         "value"),
    Input("ranking-year",    "value"),
)
def update_charts(regions, year_from, year_to, ranking_year):
    empty = go.Figure()
    if not regions:
        return [empty] * len(_outputs)

    raw = _raw_regions(regions)
    results = []

    for _, measure in section_measures:
        trend_df = _add_label(semantic.query(
            measure.id, domain=DOMAIN, regions=raw,
            year_range=(year_from, year_to),
        ))
        rank_df = _add_label(semantic.query(
            measure.id, domain=DOMAIN, regions=raw,
            year=ranking_year,
        ))
        results.append(_trend_fig(trend_df, measure))
        results.append(_rank_fig(rank_df,   measure, ranking_year))

    return results


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    log.info("Starting Dash app — domain: %s, measures: %s",
             domain.label, [m.id for _, m in section_measures])
    app.run(host="0.0.0.0", port=8050, debug=False)
