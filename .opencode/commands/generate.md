---
description: Run the dashboard generation script
agent: build
---

Run the dashboard generation script to regenerate all dashboards.

Command: POSTGRES_PASSWORD=$POSTGRES_PASSWORD python3 charts/generate.py

Report which dashboards were generated and any errors.
