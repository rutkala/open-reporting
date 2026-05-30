#!/usr/bin/env python3
"""
Weekly Economy Snapshot — generates a 1080×1080 social card with 4 KPIs
from the warehouse and (optionally) publishes to Instagram.

Usage:
  python products/social/weekly_snapshot.py            # generate + publish
  python products/social/weekly_snapshot.py --dry-run  # generate only, save to /tmp/

Environment variables (from .env):
  DUCKDB_PATH           — path to warehouse.duckdb
  INSTAGRAM_ACCESS_TOKEN — Meta long-lived token (needed for --publish)

Linear: OR-89
"""
from __future__ import annotations

import argparse
import logging
import os
import sys
from datetime import date
from pathlib import Path

import duckdb
import plotly.graph_objects as go
import requests

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
CARD_W, CARD_H = 1080, 1080
OUTPUT_DIR = Path("/tmp/or-social")
INSTAGRAM_API = "https://graph.facebook.com/v19.0"

# Nordic / Open Reporting colour palette
TEAL = "#00796B"
WARM_GREY = "#F5F5F0"
DARK = "#1A1A1A"
MUTED = "#757575"
GREEN_GOOD = "#2E7D32"
RED_BAD = "#C62828"


def _load_env() -> None:
    path = Path(".env")
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
def fetch_kpis() -> list[dict]:
    """
    Returns a list of 4 KPI dicts: {label, value, unit, year, direction}.
    direction: "good" | "bad" | "neutral" — for colour coding.
    """
    db_path = os.environ.get("DUCKDB_PATH", "data/warehouse.duckdb")
    con = duckdb.connect(db_path, read_only=True)

    queries = [
        ("Bezrobocie", "% r/r", "neutral",
         "SELECT unemployment_rate_pct, period_year FROM curated.fact_labour_overview "
         "WHERE geo='PL' AND unemployment_rate_pct IS NOT NULL ORDER BY period_year DESC LIMIT 1"),
        ("Wzrost PKB", "% r/r", None,
         "SELECT gdp_real_growth_pct, period_year FROM curated.fact_macro_overview "
         "WHERE geo='PL' AND gdp_real_growth_pct IS NOT NULL ORDER BY period_year DESC LIMIT 1"),
        ("Inflacja (żywność)", "idx 2015=100", "neutral",
         "SELECT food_hicp_idx, period_year FROM curated.fact_prices_overview "
         "WHERE geo='PL' AND food_hicp_idx IS NOT NULL ORDER BY period_year DESC LIMIT 1"),
        ("Saldo handlowe", "mld EUR", None,
         "SELECT ROUND(trade_balance_mio_eur/1000.0,1), period_year "
         "FROM curated.fact_trade_overview "
         "WHERE geo='PL' AND trade_balance_mio_eur IS NOT NULL ORDER BY period_year DESC LIMIT 1"),
    ]
    rows = []
    for label, unit, fixed_dir, q in queries:
        r = con.execute(q).fetchone()
        if r:
            value, year = r
            direction = fixed_dir or ("good" if value >= 0 else "bad")
            rows.append((label, value, unit, year, direction))

    return [
        {"label": r[0], "value": r[1], "unit": r[2], "year": r[3], "direction": r[4]}
        for r in rows
    ]


# ---------------------------------------------------------------------------
# Card generation
# ---------------------------------------------------------------------------
def make_card(kpis: list[dict], output_path: Path) -> Path:
    """Render a 1080×1080 Plotly figure and export as PNG."""
    today = date.today().strftime("%-d %B %Y")
    fig = go.Figure()
    fig.update_layout(
        width=CARD_W, height=CARD_H,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor=WARM_GREY,
        plot_bgcolor=WARM_GREY,
        font=dict(family="Inter, Arial, sans-serif", color=DARK),
    )

    # Header bar
    fig.add_shape(type="rect", x0=0, x1=1, y0=0.88, y1=1,
                  xref="paper", yref="paper",
                  fillcolor=TEAL, line_width=0)
    fig.add_annotation(
        x=0.5, y=0.965, xref="paper", yref="paper",
        text="<b>Polska Gospodarka</b>",
        font=dict(size=36, color="white"), showarrow=False,
    )
    fig.add_annotation(
        x=0.5, y=0.915, xref="paper", yref="paper",
        text=f"Przegląd tygodniowy · {today}",
        font=dict(size=20, color="rgba(255,255,255,0.85)"), showarrow=False,
    )

    # 4 KPI tiles in 2×2 grid
    positions = [(0.25, 0.62), (0.75, 0.62), (0.25, 0.28), (0.75, 0.28)]
    for kpi, (cx, cy) in zip(kpis[:4], positions):
        colour = GREEN_GOOD if kpi["direction"] == "good" else (
            RED_BAD if kpi["direction"] == "bad" else TEAL
        )
        # Tile background
        fig.add_shape(type="rect",
                      x0=cx - 0.19, x1=cx + 0.19,
                      y0=cy - 0.15, y1=cy + 0.15,
                      xref="paper", yref="paper",
                      fillcolor="white",
                      line=dict(color="#E0E0E0", width=1))
        # Label
        fig.add_annotation(
            x=cx, y=cy + 0.10, xref="paper", yref="paper",
            text=kpi["label"],
            font=dict(size=22, color=MUTED), showarrow=False,
        )
        # Value
        val_str = f"{kpi['value']:.1f}" if kpi["value"] is not None else "—"
        fig.add_annotation(
            x=cx, y=cy + 0.01, xref="paper", yref="paper",
            text=f"<b>{val_str}</b>",
            font=dict(size=44, color=colour), showarrow=False,
        )
        # Unit + year
        fig.add_annotation(
            x=cx, y=cy - 0.09, xref="paper", yref="paper",
            text=f"{kpi['unit']}  ·  {kpi['year']}",
            font=dict(size=16, color=MUTED), showarrow=False,
        )

    # Footer
    fig.add_annotation(
        x=0.5, y=0.04, xref="paper", yref="paper",
        text="portal.open-reporting.dev  ·  Źródło: Eurostat",
        font=dict(size=16, color=MUTED), showarrow=False,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_image(str(output_path))
    log.info("card saved → %s", output_path)
    return output_path


# ---------------------------------------------------------------------------
# Instagram publish
# ---------------------------------------------------------------------------
def publish_to_instagram(image_path: Path, caption: str) -> str:
    """Upload image + post to Instagram. Returns media ID."""
    token = os.environ.get("INSTAGRAM_ACCESS_TOKEN", "")
    if not token:
        raise RuntimeError(
            "INSTAGRAM_ACCESS_TOKEN not set — refresh token via Meta portal (OR-90)"
        )

    # Step 1: create media container
    r = requests.post(
        f"{INSTAGRAM_API}/me/media",
        params={
            "image_url": image_path,  # must be public URL
            "caption": caption,
            "access_token": token,
        },
        timeout=30,
    )
    r.raise_for_status()
    container_id = r.json()["id"]

    # Step 2: publish
    r2 = requests.post(
        f"{INSTAGRAM_API}/me/media_publish",
        params={"creation_id": container_id, "access_token": token},
        timeout=30,
    )
    r2.raise_for_status()
    return r2.json()["id"]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Weekly Economy Snapshot card")
    parser.add_argument("--dry-run", action="store_true",
                        help="Generate card only, do not publish to Instagram")
    parser.add_argument("--output", type=Path,
                        default=OUTPUT_DIR / f"snapshot-{date.today()}.png",
                        help="Output PNG path (default: /tmp/or-social/snapshot-<date>.png)")
    args = parser.parse_args()

    _load_env()

    log.info("fetching KPIs from warehouse …")
    kpis = fetch_kpis()
    for k in kpis:
        log.info("  %-20s %s %s  (%s)", k["label"], k["value"], k["unit"], k["year"])

    log.info("rendering card …")
    card_path = make_card(kpis, args.output)

    if args.dry_run:
        log.info("--dry-run: skipping Instagram publish")
        log.info("card at: %s", card_path)
        return

    today = date.today().strftime("%-d %B %Y")
    caption = (
        f"📊 Tygodniowy przegląd polskiej gospodarki ({today})\n\n"
        + "\n".join(
            f"{'📈' if k['direction']=='good' else '📉' if k['direction']=='bad' else '📊'} "
            f"{k['label']}: {k['value']:.1f} {k['unit']} ({k['year']})"
            for k in kpis
        )
        + "\n\n🔗 portal.open-reporting.dev\n#Polska #gospodarka #Eurostat #opendata"
    )

    log.info("publishing to Instagram …")
    media_id = publish_to_instagram(card_path, caption)
    log.info("published — media ID: %s", media_id)


if __name__ == "__main__":
    main()
