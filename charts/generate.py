#!/usr/bin/env python3
"""
Generate all dashboards and the portal index.

Usage:
    cd /opt/open-reporting
    POSTGRES_PASSWORD=xxx python3 charts/generate.py

    # Single dashboard:
    POSTGRES_PASSWORD=xxx python3 charts/dashboards/state_budget.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from dashboards.state_budget import build as state_budget
from dashboards.voivodship   import build as voivodship
from dashboards.gpw_market   import build as gpw_market
from dashboards.portal       import build as portal

if __name__ == "__main__":
    print("Generating dashboards...")
    state_budget()
    voivodship()
    gpw_market()
    portal()
    print("\nDone. Open https://portal.open-reporting.dev")
