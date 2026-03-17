#!/usr/bin/env python3
"""
Explore the DBW (GUS) API and inventory available datasets.

Fetches all subject areas and their variables, identifies potential HVD
(High Value Datasets) by name matching, prints a readable summary, and
saves full output to ingestion/dbw_areas.json.

API docs: https://api-dbw.stat.gov.pl/apidocs/
HVD catalog: https://dbw.stat.gov.pl/katalog/hvd

Usage:
    python3 ingestion/dbw_explore.py
"""

import json
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE = "https://api-dbw.stat.gov.pl/api/1.1.0"
API_KEY = os.environ.get("DBW_API_KEY", "")
PAUSE = 0.4

OUT_FILE = Path(__file__).parent / "dbw_areas.json"

# EU HVD regulation categories relevant to statistical data (Regulation 2023/138)
# GUS datasets in these domains are likely HVD candidates
HVD_KEYWORDS = [
    "population", "demographic", "birth", "death", "migration",
    "employment", "unemployment", "labour", "wages", "earnings",
    "gdp", "national accounts", "regional accounts",
    "prices", "inflation", "cpi",
    "education", "health", "crime", "environment", "energy",
    "agriculture", "transport", "tourism",
    "enterprise", "business", "trade",
    # Polish equivalents
    "ludno", "demograf", "urodzen", "zgon", "migracja",
    "zatrudni", "bezrobot", "rynek pracy", "wynagrodzeni",
    "pkb", "rachunki narodowe", "rachunki regionalne",
    "ceny", "inflacja",
    "edukacja", "zdrowie", "przestępczo", "środowisko", "energia",
    "rolnictwo", "transport", "turystyka",
    "przedsiębiorstwo", "handel",
    "budżet",
]


def get(path: str, params: dict = None) -> list | dict:
    headers = {"X-ClientId": API_KEY} if API_KEY else {}
    r = requests.get(f"{API_BASE}{path}", headers=headers, params=params or {}, timeout=30)
    r.raise_for_status()
    return r.json()


def fetch_areas() -> list[dict]:
    data = get("/area/area-area", {"lang": "pl"})
    return data if isinstance(data, list) else []


def fetch_variables(area_id: int) -> list[dict]:
    try:
        data = get("/area/area-variable", {"lang": "pl", "id-obszaru": area_id})
        return data if isinstance(data, list) else []
    except requests.HTTPError:
        return []


def is_hvd_candidate(name: str) -> bool:
    name_lower = name.lower()
    return any(kw in name_lower for kw in HVD_KEYWORDS)


def main():
    if not API_KEY:
        print("WARNING: DBW_API_KEY not set — requests may be rate-limited or rejected")

    print("Fetching subject areas...")
    areas = fetch_areas()
    leaf_areas = [a for a in areas if a.get("czy-zmienne")]
    parent_areas = [a for a in areas if not a.get("czy-zmienne")]

    print(f"Total areas: {len(areas)} ({len(leaf_areas)} with variables, {len(parent_areas)} parent/grouping)")
    print()

    result = []
    total_variables = 0
    hvd_candidates = []

    for area in areas:
        area_id = area["id"]
        area_name = area.get("nazwa", "")
        has_vars = area.get("czy-zmienne", False)
        level = area.get("nazwa-poziom", "")
        parent_id = area.get("id-nadrzedny-element")

        variables = []
        if has_vars:
            variables = fetch_variables(area_id)
            time.sleep(PAUSE)

        hvd_flag = is_hvd_candidate(area_name)
        hvd_var_names = [v["nazwa-zmienna"] for v in variables if is_hvd_candidate(v.get("nazwa-zmienna", ""))]

        if has_vars:
            marker = "  *** HVD?" if hvd_flag else ""
            print(f"  [{area_id:4}] [{level:30}] {area_name}  ({len(variables)} vars){marker}")
        else:
            print(f"  [{area_id:4}] [{level:30}] {area_name}  (group)")

        total_variables += len(variables)

        entry = {
            "id": area_id,
            "name": area_name,
            "level": level,
            "parent_id": parent_id,
            "has_variables": has_vars,
            "hvd_candidate": hvd_flag or bool(hvd_var_names),
            "variables_count": len(variables),
            "variables": [
                {
                    "id": v.get("id"),
                    "area_name": v.get("nazwa"),
                    "variable_id": v.get("id-zmienna"),
                    "variable_name": v.get("nazwa-zmienna"),
                    "hvd_candidate": is_hvd_candidate(v.get("nazwa-zmienna", "")),
                }
                for v in variables
            ],
        }
        result.append(entry)

        if entry["hvd_candidate"] and has_vars:
            hvd_candidates.append(entry)

    OUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print()
    print("=" * 70)
    print(f"SUMMARY")
    print("=" * 70)
    print(f"  Total areas:              {len(areas)}")
    print(f"  Areas with variables:     {len(leaf_areas)}")
    print(f"  Total variables indexed:  {total_variables}")
    print(f"  HVD candidate areas:      {len(hvd_candidates)}")
    print()
    print("HVD CANDIDATE AREAS (keyword match on EU HVD regulation categories):")
    for a in hvd_candidates:
        print(f"  [{a['id']:4}] {a['name']}  ({a['variables_count']} vars)")
    print()
    print(f"Full output saved to: {OUT_FILE}")
    print()
    print("NOTE: HVD identification above is by keyword matching.")
    print("For authoritative HVD list see: https://dbw.stat.gov.pl/katalog/hvd")


if __name__ == "__main__":
    main()
