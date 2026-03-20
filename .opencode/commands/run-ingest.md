---
description: Run data ingestion scripts
agent: build
---

Run data ingestion scripts. Options:
- GPW stock data: python3 ingestion/gpw_ingest.py
- Budget data: BDL_API_KEY=$BDL_API_KEY POSTGRES_PASSWORD=$POSTGRES_PASSWORD python3 ingestion/budget_ingest.py

Run incrementally (today only) unless --backfill is specified.

Which ingestion script to run?
