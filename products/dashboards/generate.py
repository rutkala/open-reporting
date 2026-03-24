#!/usr/bin/env python3
"""
Dashboard generator — runs all dashboard modules and writes HTML output.
Usage: python3 products/dashboards/generate.py
"""
import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

from products.dashboards.rynek_pracy.static import generate as gen_rynek_pracy

DASHBOARDS = [
    ("labour/rynek-pracy", gen_rynek_pracy),
]


def main() -> None:
    errors = []
    for name, fn in DASHBOARDS:
        try:
            log.info("Generating: %s", name)
            fn()
            log.info("OK: %s", name)
        except Exception as exc:
            log.error("FAILED: %s — %s", name, exc)
            errors.append(name)

    if errors:
        log.error("Failed dashboards: %s", errors)
        sys.exit(1)
    log.info("All dashboards generated successfully.")


if __name__ == "__main__":
    main()
