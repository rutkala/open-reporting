#!/usr/bin/env python3
"""
Generic own-site file scraper (config-driven).

For sources whose data lives as downloadable files (XLSX/CSV/ZIP) linked from
an institution's own web page — the reports-only / own-portal tail that isn't
on dane.gov.pl. Fetches each configured page, extracts data-file links, and
downloads them.

Config: products/ingestion/registry/web_scraper_sources.yaml
Output: data/landing/{source_key}/{filename}
(OR_LANDING_DIR overrides base.)

Best-effort by design: pages vary, so it grabs whatever data files it finds and
logs how many. Sources that turn out to be pure-HTML (no files) surface as 0 —
a signal they need a bespoke handler.

Usage:
    python3 web_scraper_extractor.py
    python3 web_scraper_extractor.py --sources najwyzsza_izba_kontroli
    python3 web_scraper_extractor.py --sources nik --list   # list found links only
"""
import argparse
import logging
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
import yaml

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

REPO = Path("/opt/open-reporting")
CONFIG = REPO / "products/ingestion/registry/web_scraper_sources.yaml"
LANDING = Path(os.environ.get("OR_LANDING_DIR", str(REPO / "data/landing")))
HEADERS = {"User-Agent": "Mozilla/5.0 (OpenReporting-DataPipeline/1.0; open-reporting.dev)"}
DEFAULT_EXTS = ["xlsx", "xls", "csv", "zip", "ods", "json"]
LINK_RE = re.compile(r'href=["\']([^"\']+)["\']', re.I)


def find_files(session, page, exts) -> list[str]:
    try:
        r = session.get(page, headers=HEADERS, timeout=60)
        r.raise_for_status()
    except Exception as e:
        logger.warning(f"  page {page}: {e}")
        return []
    out = []
    for href in LINK_RE.findall(r.text):
        url = urljoin(page, href)
        path = urlparse(url).path.lower()
        if any(path.endswith("." + e) for e in exts):
            out.append(url)
    return sorted(set(out))


def download(session, url, dest: Path) -> bool:
    try:
        with session.get(url, headers=HEADERS, timeout=180, stream=True) as r:
            r.raise_for_status()
            dest.parent.mkdir(parents=True, exist_ok=True)
            tmp = dest.with_suffix(dest.suffix + ".tmp")
            with open(tmp, "wb") as fh:
                for chunk in r.iter_content(65536):
                    fh.write(chunk)
            tmp.replace(dest)
        return True
    except Exception as e:
        logger.warning(f"  {url}: {e}")
        return False


def main(sources, list_only) -> int:
    cfg = yaml.safe_load(CONFIG.read_text())["sources"]
    todo = sources or list(cfg)
    session = requests.Session()
    for key in todo:
        if key not in cfg:
            logger.warning(f"unknown source {key}")
            continue
        c = cfg[key]
        pages = c["pages"] if isinstance(c.get("pages"), list) else [c.get("pages") or c.get("url")]
        exts = c.get("exts", DEFAULT_EXTS)
        links = []
        for pg in pages:
            links += find_files(session, pg, exts)
        links = sorted(set(links))
        logger.info(f"[{key}] {len(links)} data-file links across {len(pages)} page(s)")
        if list_only:
            for l in links[:20]:
                logger.info(f"    {l}")
            continue
        land, n = LANDING / key, 0
        for url in links:
            fn = os.path.basename(urlparse(url).path) or f"file_{n}"
            if download(session, url, land / fn):
                n += 1
            time.sleep(0.2)
        logger.info(f"[{key}] done — {n} files → {land}")
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Generic own-site file scraper")
    p.add_argument("--sources", nargs="*", default=None)
    p.add_argument("--list", action="store_true", dest="list_only")
    a = p.parse_args()
    sys.exit(main(a.sources, a.list_only))
