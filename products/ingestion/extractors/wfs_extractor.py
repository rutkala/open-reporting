#!/usr/bin/env python3
"""
Generic OGC WFS extractor (config-driven).

Pulls vector spatial data from any WFS service defined in
products/ingestion/registry/wfs_sources.yaml. For each source:
  1. GetCapabilities → discover feature types (or use the configured layer list).
  2. GetFeature per layer as GeoJSON, paginated (count + startIndex).
  3. Save one GeoJSON file per layer.

Covers the spatial fleet (Lasy/GDOŚ/Wody Polskie/GUGiK/PIG) with one engine.

Output: data/landing/{source_key}/{layer}.geojson
(OR_LANDING_DIR env overrides base; OGC services are public, no key.)

Usage:
    python3 wfs_extractor.py                       # all configured WFS sources
    python3 wfs_extractor.py --sources lasy_bdl
    python3 wfs_extractor.py --list                # just list layers per source
"""
import argparse
import json
import logging
import os
import re
import sys
import time
from pathlib import Path
from xml.etree import ElementTree as ET

import requests
import yaml

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

REPO = Path("/opt/open-reporting")
CONFIG = REPO / "products/ingestion/registry/wfs_sources.yaml"
LANDING = Path(os.environ.get("OR_LANDING_DIR", str(REPO / "data/landing")))
HEADERS = {"User-Agent": "OpenReporting-DataPipeline/1.0"}
PAGE = 5000
TIMEOUT = 120


def discover_layers(session, wfs) -> list[str]:
    r = session.get(wfs, params={"service": "WFS", "version": "2.0.0",
                                 "request": "GetCapabilities"},
                    headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    names = re.findall(r"<(?:[\w]+:)?Name>([^<]+)</(?:[\w]+:)?Name>", r.text)
    # keep typeName-looking entries (with a prefix or not), drop service-level Names
    return [n for n in names if n and not n.startswith("http")]


def fetch_layer(session, wfs, layer) -> dict | None:
    feats, start = [], 0
    while True:
        params = {"service": "WFS", "version": "2.0.0", "request": "GetFeature",
                  "typeNames": layer, "count": PAGE, "startIndex": start,
                  "outputFormat": "application/json", "srsName": "EPSG:4326"}
        r = session.get(wfs, params=params, headers=HEADERS, timeout=TIMEOUT)
        if r.status_code != 200 or r.text.lstrip().startswith("<"):
            # try GML fallback marker / exception → skip layer
            if start == 0:
                logger.warning(f"  {layer}: non-JSON response, skipping")
            break
        gj = r.json()
        batch = gj.get("features", [])
        feats.extend(batch)
        if len(batch) < PAGE:
            break
        start += PAGE
        time.sleep(0.3)
    if not feats:
        return None
    return {"type": "FeatureCollection", "features": feats}


def main(sources, list_only) -> int:
    cfg_all = yaml.safe_load(CONFIG.read_text())["sources"]
    todo = sources or list(cfg_all)
    session = requests.Session()
    worst = 0
    for key in todo:
        if key not in cfg_all:
            logger.warning(f"unknown source {key}")
            continue
        wfs = cfg_all[key]["wfs"]
        try:
            layers = cfg_all[key].get("layers") or discover_layers(session, wfs)
        except Exception as e:
            logger.error(f"[{key}] GetCapabilities failed: {e}")
            worst = 1
            continue
        logger.info(f"[{key}] {len(layers)} layers @ {wfs}")
        if list_only:
            for ly in layers[:40]:
                logger.info(f"    {ly}")
            continue
        total = 0
        for ly in layers:
            try:
                fc = fetch_layer(session, wfs, ly)
            except Exception as e:
                logger.warning(f"  {ly}: {e}")
                continue
            if fc:
                safe = ly.replace(":", "_").replace("/", "_")
                dest = LANDING / key / f"{safe}.geojson"
                dest.parent.mkdir(parents=True, exist_ok=True)
                tmp = dest.with_suffix(".tmp")
                tmp.write_text(json.dumps(fc, ensure_ascii=False))
                tmp.replace(dest)
                logger.info(f"  {ly}: {len(fc['features'])} features")
                total += len(fc["features"])
        logger.info(f"[{key}] done — {total} features → {LANDING / key}")
    return worst


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Generic OGC WFS extractor")
    p.add_argument("--sources", nargs="*", default=None)
    p.add_argument("--list", action="store_true", dest="list_only")
    a = p.parse_args()
    sys.exit(main(a.sources, a.list_only))
