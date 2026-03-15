# open-reporting — Project Context for Claude Code

## Who I am
- Name: Radek
- Role: B2B contractor, Power BI/Fabric developer, analytics consultant
- Location: Poland
- Available time: ~5 hours/week for this project
- I have ADHD — keep tasks small, concrete, and deliverable-focused
  - Never give me theory walls — give me the next action
  - Every session should end with something committed or deployed
  - Use AI for boring/repetitive parts, I handle design decisions

## Project goal
Build a public-facing analytical web service showing Polish regional
economic indicators, hosted on this Hetzner VPS (CX22, 4GB RAM).

## Current stack (lean, fits on CX22)
- PostgreSQL — data warehouse
- Metabase — public dashboards
- Nginx — reverse proxy + SSL
- Python ingestion scripts — pull from GUS BDL API
- dbt — SQL transformations (future)
- All orchestrated via Docker Compose

## Data source
GUS BDL API (bdl.stat.gov.pl) — Polish regional statistics
- REST API, JSON, free API key
- Key indicators: unemployment rate, avg wage, population, GDP per capita
- All data by voivodship (16 Polish regions)

## Project phases
1. (NOW) Deploy lean Docker stack + first GUS BDL ingestion script
2. Public Metabase dashboard with regional indicators
3. Monetization + consulting positioning
4. Scale + academic path exploration

## How to work with me
- One task at a time, small and concrete
- Always tell me what the deliverable is before starting
- If something is repetitive or boring — just do it, don't ask
- If you need a decision from me — ask one question, not five
- Commit progress to git regularly so I can see what changed

## Repo
GitHub: open-reporting (to be connected)
VPS: /root/open-reporting

## Environment
- VPS IP: 91.98.118.153
- OS: Ubuntu, Docker installed
- Claude Code: v2.1.76 at ~/.local/bin/claude
