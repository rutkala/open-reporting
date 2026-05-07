#!/usr/bin/env python3
"""Open Reporting — Template Dashboard.

Visual-component showroom served on port 8055 under ``/template/``.
The full showroom (41 sections, sample data, sidebar nav, palette
reference) lives in the skill at
``.claude/skills/complex_dashboard/assets/example/showroom.py`` —
this file is the deployed entry point.

Copy this directory to start a real domain dashboard, then replace
``build_showroom_app(...)`` with your own layout.

Run:
    PYTHONPATH=/opt/open-reporting:/opt/open-reporting/.claude/skills \\
    DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb \\
    python3 products/dashboards/template/app.py
"""
import logging

from complex_dashboard.assets.example.showroom import build_showroom_app
from complex_dashboard.assets.runtime import register_healthcheck

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

PORT = 8055

app = build_showroom_app(domain="template", module_name=__name__)
register_healthcheck(app)


if __name__ == "__main__":
    log.info("Starting Template dashboard on port %d", PORT)
    app.run(host="0.0.0.0", port=PORT, debug=False)
