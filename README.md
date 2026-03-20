# Open Reporting

A one-person data media company turning Polish public data into accessible, beautiful, and useful products.

**Live:** [portal.open-reporting.dev](https://portal.open-reporting.dev) · [www.open-reporting.dev](https://www.open-reporting.dev)

## Quick Start

```bash
# Clone and setup
git clone https://github.com/rutkala/open-reporting.git
cd open-reporting
cp .env.example .env

# Start services
docker compose up -d

# Generate dashboards
POSTGRES_PASSWORD=xxx python3 charts/generate.py
```

## Documentation

All agent guidelines and project documentation: **[AGENTS.md](AGENTS.md)**

## Current Status

- ✅ 4 dashboards deployed (State Budget, Regional Budgets, GPW Market, Labour Market)
- ✅ Data ingestion for GPW stocks and GUS BDL budget data
- ⬜ 18 dashboard domains planned (see AGENTS.md for full list)

*Owner: Radek Utkala · Poland · 2026*
