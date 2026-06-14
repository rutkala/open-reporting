#!/usr/bin/env python3
"""
Allegro public REST API extractor.

OAuth client-credentials flow → public offer/product search. Requires a free
app registration at developer.allegro.pl; credentials in .env as
ALLEGRO_CLIENT_ID / ALLEGRO_CLIENT_SECRET (PO action — 3rd-party portal).

Pulls offer/price data for a configured category set (market-price signal).

Output: data/landing/allegro/{category}/{date}.json (OR_LANDING_DIR overrides).

Usage:
    python3 allegro_extractor.py --categories <id> <id>
    python3 allegro_extractor.py --phrase "rower" --max 500
"""
import argparse
import json
import logging
import os
import sys
import time
from datetime import date
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(override=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

REPO = Path("/opt/open-reporting")
LANDING = Path(os.environ.get("OR_LANDING_DIR", str(REPO / "data/landing"))) / "allegro"
TOKEN_URL = "https://allegro.pl/auth/oauth/token"
API = "https://api.allegro.pl"
HEADERS = {"Accept": "application/vnd.allegro.public.v1+json"}


def get_token() -> str:
    cid = os.environ.get("ALLEGRO_CLIENT_ID")
    secret = os.environ.get("ALLEGRO_CLIENT_SECRET")
    if not cid or not secret:
        raise RuntimeError("ALLEGRO_CLIENT_ID / ALLEGRO_CLIENT_SECRET not set in .env "
                           "(register a free app at developer.allegro.pl — PO action)")
    r = requests.post(TOKEN_URL, data={"grant_type": "client_credentials"},
                      auth=(cid, secret), timeout=30)
    r.raise_for_status()
    return r.json()["access_token"]


def search(session, token, phrase, category, limit) -> list:
    out, offset = [], 0
    h = {**HEADERS, "Authorization": f"Bearer {token}"}
    while offset < limit:
        params = {"limit": min(60, limit - offset), "offset": offset}
        if phrase:
            params["phrase"] = phrase
        if category:
            params["category.id"] = category
        r = session.get(f"{API}/offers/listing", params=params, headers=h, timeout=30)
        r.raise_for_status()
        items = r.json().get("items", {})
        batch = (items.get("promoted", []) or []) + (items.get("regular", []) or [])
        if not batch:
            break
        out.extend(batch)
        offset += 60
        time.sleep(0.3)
    return out


def main(categories, phrase, mx) -> int:
    try:
        token = get_token()
    except Exception as e:
        logger.error(str(e))
        return 2
    session = requests.Session()
    today = date.today().isoformat()
    targets = categories or ["_phrase"]
    for cat in targets:
        rows = search(session, token, phrase, None if cat == "_phrase" else cat, mx)
        dest = LANDING / (cat if cat != "_phrase" else "search") / f"{today}.json"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps({"fetched": today, "count": len(rows), "items": rows},
                                   ensure_ascii=False, indent=2))
        logger.info(f"[allegro] {cat}: {len(rows)} offers → {dest}")
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Allegro public API extractor")
    p.add_argument("--categories", nargs="*", default=None)
    p.add_argument("--phrase", default=None)
    p.add_argument("--max", type=int, default=300, dest="mx")
    a = p.parse_args()
    sys.exit(main(a.categories, a.phrase, a.mx))
