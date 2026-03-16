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

## Working style
- I am Product Owner, you are Developer/Engineer/Analyst
- One task at a time, small and concrete
- Always tell me what the deliverable is before starting
- If something is repetitive or boring — just do it, don't ask
- If you need a decision from me — ask one question, not five
- Commit progress to git regularly

## At session start — always read these files
- **PRODUCT.md** — full product vision, domains, audience, business model
- **ROADMAP.md** — phased plan, what's done, what's next
- **DATA_CATALOG.md** — all data sources, tables, columns, ingestion scripts, and dashboard usage

These are the source of truth for what to build and why.

## Current stack
- PostgreSQL 16 — data warehouse
- Nginx — reverse proxy + SSL (Let's Encrypt)
- Ghost CMS — blog (www.open-reporting.dev)
- Python + Plotly — interactive dashboards (portal.open-reporting.dev)
- Python ingestion scripts — GUS BDL API, stooq.com
- All orchestrated via Docker Compose on Hetzner CX22

## Environment
- VPS: 91.98.118.153 (Hetzner CX22, 4GB RAM, Ubuntu)
- Repo: /opt/open-reporting
- GitHub: github.com/rutkala/open-reporting (SSH auth configured)
- Claude Code: ~/.local/bin/claude
