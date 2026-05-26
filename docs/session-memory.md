# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-05-26 -->

## Current Focus

AI Lead operating model **active** (see `docs/process/lead-protocol.md`). Strategic direction, editorial picks, and execution are autonomous within cost ceiling. Themes 1+2 of the 4-6 week roadmap are essentially complete; Theme 3 (3 more domain dashboards) is next.

## What shipped (2026-05-26 session)

Direct-to-main commits since merge of PR #61:

| Commit | What | Linear |
|---|---|---|
| `57de7ba1` | YAML gap closures (Poland labels, COVID/breach annotations) | — |
| `cc4c34c3` | Codex P2: line.py post-fetch slice (fix silent truncation for >4 series) | — |
| `e5afdd09` | Table column labels resolver (`labels:` config) | — |
| `ee1a1e77` | Phase D agent slim 22→6 (over-cut, corrected next) | — |
| `519110d5` | Phase D reshape: 10 agents, 8 skills, Opus orchestrates | — |
| `463863b7` | C.8 `dual_year` grouped bar primitive | — |
| `9608e806` | Delete archived public_finance_phase_b | — |
| `828186aa` / `6eb67976` | Wrap-up: session memory + drop `composite_` skill prefix | — |
| `86bf9add` | **AI Lead activation:** lead-protocol.md, roadmap.md, decisions.md | — |
| `866d9f46` | OR-78 + OR-85: Ghost admin verified + daily ingestion cron live | OR-78, OR-85 |
| `4fab3af3` | OR-80: first article published + reusable Ghost publisher | OR-80, OR-74 |

## Linear status — Theme 1 + 2

| Issue | Title | Status |
|---|---|---|
| OR-78 | Ghost admin | **Done** |
| OR-85 | Daily ingestion cron | **Done** (22:00 UTC, stops dashboard ~9min, restarts) |
| OR-80 | First data-driven article | **Done** (live at /sgp-maastricht-1995-2024/) |
| OR-74 | Blog setup + first content | **Done** |
| **OR-90** | Instagram token refresh | **BLOCKED on PO** (Meta Developer portal) |
| **OR-79** | Portal nav link | **BLOCKED on PO** (Ghost browser admin session needed) |

## Live production state

- **Dashboards:** `portal.open-reporting.dev/public_finance/` — 71%+ rubric pass rate after Phase B/C work
- **Blog:** `www.open-reporting.dev` — 3 articles + Coming Soon placeholder (1 newly authored by AI Lead, 2 pre-existing)
- **Daily ingestion:** cron at `0 22 * * *` UTC → NBP rates + Eurostat observations → upsert into DuckDB warehouse
- **Autonomous loop:** scheduled remote agent fires Mondays 09:07 Warsaw (`trig_01TqBcSxS3SzQn7BtSTiDmif`)

## Next pending — Theme 3 (3 more domain dashboards)

| # | Linear | What |
|---|---|---|
| 7 | **OR-56** | Labour Market dashboard (Polish public-data flagship topic) |
| 8 | **OR-52** | National Accounts & Macroeconomics (pairs with public_finance for full macro picture) |
| 9 | **OR-55** | Population & Demographics (long-arc public interest) |

Pattern to follow: `products/dashboards/public_finance/` is the canonical example. Each new domain = dbt staging models + semantic layer + dbr YAML pages.

## Architecture (current)

**Opus orchestrates, agents execute.** Per `docs/process/model-delegation.md`:
- Opus (me) = analyse, plan, orchestrate, integrate
- Sonnet builders = `dashboard-dev`, `data-engineer`, `content-writer`, `researcher`
- Mixed evaluators = `code-reviewer` (Sonnet), `architecture-critic`, `analytical-validator`, `domain-specialist` (Opus), `visual-screenshot-reviewer` (Sonnet)
- Utility = `debug` (Sonnet)

**Skills (7):** `kickoff`, `plan`, `develop`, `review`, `review_ideas`, `knowledge`, `experience` (no `composite_` prefix).

## Key Technical Facts

- DuckDB: `data/warehouse.duckdb` (exclusive lock during writes — daily cron stops + restarts dashboard)
- PostgreSQL: `localhost:5432 db=reporting`
- Ghost: `ghost:5-alpine` container, SQLite backend, JWT-based Admin API at `GHOST_KEY_ID`/`GHOST_KEY_SECRET` in .env
- Production deploy: `dbr run products/dashboards/<name>` → systemd `or-<name>.service` + nginx
- Article publishing: `python3 products/blog/publish_to_ghost.py <draft.md> --publish` (reusable)
- Visual reviewer is **multimodal** — compares rendered screenshots against `docs/visualization/references/` using `docs/visualization/quality.md` rubric

## Deferred (low-priority, not blocking)

- Ghost settings updates via API require browser session (501 on Integration JWT) — OR-79 PO action
- DuckDB read-only mode in `dbr serve` would eliminate the 9-min daily downtime — file a Linear issue when next touching dbr
- Bar annotation y-axis can't take categorical string (schema relaxation needed)
- Grey-history primitive (needs design decision)
- Wave 3 reference captures (Tableau / IMF PDF / GUS detail)
- complex_dashboard skill recreation (retired in feat branch; recreate when needed)
- `data/drafts/` is gitignored — future article drafts should go under `products/blog/drafts/`
