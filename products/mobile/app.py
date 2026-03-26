#!/usr/bin/env python3
"""
Open Reporting — Mobile PWA
FastAPI + Jinja2. Port 8052, mounted at /app/.
Run: PYTHONPATH=/opt/open-reporting DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb \
     uvicorn products.mobile.app:app --host 0.0.0.0 --port 8052
"""
import os
import json
import logging
from pathlib import Path

import duckdb
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

BASE = Path(__file__).parent
app = FastAPI(root_path="/app")
app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")
templates = Jinja2Templates(directory=BASE / "templates")

# Polish month abbreviations
MONTH_PL = {
    1: "sty", 2: "lut", 3: "mar", 4: "kwi", 5: "maj", 6: "cze",
    7: "lip", 8: "sie", 9: "wrz", 10: "paź", 11: "lis", 12: "gru",
}


def _db():
    path = os.environ.get("DUCKDB_PATH", "/opt/open-reporting/data/warehouse.duckdb")
    return duckdb.connect(path, read_only=True)


def _format_period(d) -> str:
    """Format a date object into a human-readable Polish period string."""
    if d is None:
        return ""
    if d.day == 1 and d.month == 1:
        return str(d.year)
    if d.day == 1:
        return f"{MONTH_PL[d.month]} {d.year}"
    return f"{d.day} {MONTH_PL[d.month]} {d.year}"


def _format_value(v) -> str:
    """Format a numeric value for display."""
    if v is None:
        return "—"
    if abs(v) >= 1_000_000:
        return f"{v / 1_000_000:,.1f}M"
    if abs(v) >= 10_000:
        return f"{v:,.0f}"
    if abs(v) >= 100:
        return f"{v:,.1f}"
    return f"{v:,.2f}"


HOME_KPIS = [
    {"detail_id": "lab.unemployment_rate",     "label": "Stopa bezrobocia"},
    {"detail_id": "prc.cpi_total",             "label": "Inflacja CPI"},
    {"detail_id": "mac.gdp_real_growth",       "label": "Wzrost PKB"},
    {"detail_id": "fin.exchange_rate_eur_pln", "label": "Kurs EUR/PLN"},
    {"detail_id": "lab.wage_growth",           "label": "Wzrost wynagrodzeń"},
    {"detail_id": "mac.pmi_manufacturing",     "label": "PMI Przemysł"},
    {"detail_id": "pub.state_budget_balance",  "label": "Saldo budżetu"},
    {"detail_id": "pop.births",                "label": "Urodzenia"},
]

DOMAIN_NAMES_PL = {
    "AGR": "Rolnictwo i leśnictwo",
    "BUS": "Przedsiębiorczość",
    "CLT": "Kultura, turystyka i sport",
    "CRM": "Przestępczość i wymiar sprawiedliwości",
    "EDU": "Edukacja",
    "ENE": "Energia",
    "ENV": "Środowisko i klimat",
    "FIN": "Rynki finansowe",
    "HLT": "Zdrowie",
    "LAB": "Rynek pracy",
    "MAC": "Gospodarka i makroekonomia",
    "POP": "Ludność i demografia",
    "PRC": "Ceny i inflacja",
    "PUB": "Finanse publiczne",
    "SCI": "Nauka, technologia i cyfryzacja",
    "SOC": "Dochody i warunki życia",
    "TRD": "Handel zagraniczny",
    "TRP": "Transport",
}


def get_kpi_card(detail_id: str) -> dict:
    """Return KPI card data: latest value, period, unit, change, trend, sparkline."""
    try:
        con = _db()
        rows = con.execute(
            """
            SELECT f.period_date, f.value, d.detail_unit
            FROM curated.all_indicators f
            JOIN curated.dim_domain_detail d ON f.detail_id = d.detail_id
            WHERE f.detail_id = ?
              AND f.geo = 'PL'
              AND f.value IS NOT NULL
            ORDER BY f.period_date DESC
            LIMIT 25
            """,
            [detail_id],
        ).fetchall()
        con.close()
    except Exception as exc:
        log.warning("get_kpi_card(%s) failed: %s", detail_id, exc)
        return _empty_kpi(detail_id)

    if not rows:
        return _empty_kpi(detail_id)

    # rows are sorted newest first
    latest_date, latest_val, unit = rows[0]
    prev_val = rows[1][1] if len(rows) > 1 else None

    if prev_val is not None and prev_val != 0 and latest_val is not None:
        diff = latest_val - prev_val
        if abs(diff) < 0.0001:
            change_str = "→ bez zmian"
            trend = "flat"
        elif diff > 0:
            change_str = f"▲ +{_format_value(diff)}"
            trend = "up"
        else:
            change_str = f"▼ {_format_value(diff)}"
            trend = "down"
    else:
        change_str = ""
        trend = "flat"

    # sparkline: last 24 points, oldest first (reverse rows[1:25])
    spark_rows = rows[1:25] if len(rows) > 1 else []
    spark_rows = list(reversed(spark_rows))
    sparkline = [r[1] for r in spark_rows if r[1] is not None]

    return {
        "detail_id": detail_id,
        "latest_value": _format_value(latest_val),
        "latest_period": _format_period(latest_date),
        "unit": unit or "",
        "change": change_str,
        "trend": trend,
        "sparkline": json.dumps(sparkline),
    }


def _empty_kpi(detail_id: str) -> dict:
    return {
        "detail_id": detail_id,
        "latest_value": "—",
        "latest_period": "",
        "unit": "",
        "change": "",
        "trend": "flat",
        "sparkline": "[]",
    }


def get_domains() -> list[dict]:
    """Return domain list with indicator counts sorted by domain_id."""
    try:
        con = _db()
        rows = con.execute(
            """
            SELECT domain_id, COUNT(*) AS cnt
            FROM curated.dim_domain_detail
            GROUP BY domain_id
            ORDER BY domain_id
            """
        ).fetchall()
        con.close()
    except Exception as exc:
        log.warning("get_domains() failed: %s", exc)
        return []

    result = []
    for domain_id, cnt in rows:
        result.append({
            "domain_id": domain_id,
            "name_pl": DOMAIN_NAMES_PL.get(domain_id, domain_id),
            "count": cnt,
        })
    return result


def get_domain_indicators(domain_id: str) -> list[dict]:
    """Return indicators for a domain with latest value using window function."""
    try:
        con = _db()
        rows = con.execute(
            """
            WITH ranked AS (
                SELECT
                    f.detail_id,
                    f.period_date,
                    f.value,
                    d.detail_name,
                    d.detail_unit,
                    ROW_NUMBER() OVER (
                        PARTITION BY f.detail_id
                        ORDER BY f.period_date DESC
                    ) AS rn
                FROM curated.all_indicators f
                JOIN curated.dim_domain_detail d ON f.detail_id = d.detail_id
                WHERE d.domain_id = ?
                  AND f.geo = 'PL'
                  AND f.value IS NOT NULL
            )
            SELECT detail_id, period_date, value, detail_name, detail_unit
            FROM ranked
            WHERE rn = 1
            ORDER BY detail_name
            """,
            [domain_id.upper()],
        ).fetchall()
        con.close()
    except Exception as exc:
        log.warning("get_domain_indicators(%s) failed: %s", domain_id, exc)
        return []

    result = []
    for detail_id, period_date, value, detail_name, detail_unit in rows:
        result.append({
            "detail_id": detail_id,
            "detail_name": detail_name,
            "detail_unit": detail_unit or "",
            "latest_value": _format_value(value),
            "latest_period": _format_period(period_date),
        })
    return result


def get_indicator(detail_id: str) -> dict | None:
    """Return indicator metadata + last 60 data points for geo='PL'."""
    try:
        con = _db()
        meta = con.execute(
            """
            SELECT detail_name, detail_unit, domain_id
            FROM curated.dim_domain_detail
            WHERE detail_id = ?
            """,
            [detail_id],
        ).fetchone()

        if not meta:
            con.close()
            return None

        rows = con.execute(
            """
            SELECT period_date, value
            FROM curated.all_indicators
            WHERE detail_id = ?
              AND geo = 'PL'
              AND value IS NOT NULL
            ORDER BY period_date DESC
            LIMIT 60
            """,
            [detail_id],
        ).fetchall()
        con.close()
    except Exception as exc:
        log.warning("get_indicator(%s) failed: %s", detail_id, exc)
        return None

    if not meta:
        return None

    detail_name, detail_unit, domain_id = meta

    # Reverse so oldest first for chart
    rows_asc = list(reversed(rows))
    chart_labels = [_format_period(r[0]) for r in rows_asc]
    chart_values = [r[1] for r in rows_asc]

    latest_date = rows[0][0] if rows else None
    latest_val = rows[0][1] if rows else None

    return {
        "detail_id": detail_id,
        "detail_name": detail_name,
        "detail_unit": detail_unit or "",
        "domain_id": domain_id,
        "domain_name_pl": DOMAIN_NAMES_PL.get(domain_id, domain_id),
        "latest_value": _format_value(latest_val),
        "latest_period": _format_period(latest_date),
        "chart_labels": json.dumps(chart_labels),
        "chart_values": json.dumps(chart_values),
    }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    cards = [get_kpi_card(kpi["detail_id"]) for kpi in HOME_KPIS]
    # Merge label from HOME_KPIS into card dicts
    for i, card in enumerate(cards):
        card["label"] = HOME_KPIS[i]["label"]
    return templates.TemplateResponse(
        request,
        "home.html",
        {"cards": cards, "active_tab": "home"},
    )


@app.get("/domeny/", response_class=HTMLResponse)
async def domains(request: Request):
    domain_list = get_domains()
    return templates.TemplateResponse(
        request,
        "domains.html",
        {"domains": domain_list, "active_tab": "domains"},
    )


@app.get("/domeny/{domain_id}/", response_class=HTMLResponse)
async def domain_detail(request: Request, domain_id: str):
    indicators = get_domain_indicators(domain_id)
    domain_name = DOMAIN_NAMES_PL.get(domain_id.upper(), domain_id)
    return templates.TemplateResponse(
        request,
        "domain.html",
        {
            "domain_id": domain_id.upper(),
            "domain_name": domain_name,
            "indicators": indicators,
            "active_tab": "domains",
        },
    )


@app.get("/wskaznik/{detail_id:path}/", response_class=HTMLResponse)
async def indicator_detail(request: Request, detail_id: str):
    data = get_indicator(detail_id)
    if data is None:
        return HTMLResponse("<h1>Nie znaleziono wskaźnika</h1>", status_code=404)
    return templates.TemplateResponse(
        request,
        "indicator.html",
        {"ind": data, "active_tab": "domains"},
    )
