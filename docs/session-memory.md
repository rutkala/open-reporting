# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-02 (run #50 — OR-165 footer auto-derive) -->

## Run #50 — OR-165: auto-derive footer "Dane: YYYY" fleet-wide. HEAD 8b2f620a

**Shipped the footer-freshness fix. The mobile-WIP blocker is GONE** — runs #47–#49
committed+shipped the responsive work, so the engine tree is clean and OR-165 (which
was blocked by the dirty tree) became actionable.

**What:** dashboard footers were hand-set literals (`"Dane: 2023"`) drifting stale
after each ingest. New engine helper `latest_actual_year(domains)` in `dbr.semantic`
derives the stamp at build time: `max(year(period_date))` from `curated.all_indicators`
for the dashboard's domain_id code(s) + PL, **strictly before the current calendar
year**. That single cutoff is the forecast-safety trick — it drops both partial
current-year months and forward projections (IMF WEO → 2029) at once, so the stamp is
always a complete observed year and never overstates. Compiler: `footer_updated: auto`
+ `footer_data_domain: <CODE>` triggers it; literal still wins (backward compatible).
All 16 YAMLs migrated; `production` = `[MAC, AGR]` (mixed-domain). architecture-critic
APPROVE. Commits `b86b2d63` + fix `8b2f620a`, PR #64 merged, OR-165 → Done.

**The bug I caught (lesson):** first cut opened a *second* in-process
`duckdb.connect()` — DuckDB rejects this once the MetricFlow engine holds the file
("different configuration than existing connections"). Footer derives *after*
`_load_pages` inits the engine, so every live service silently fell back to an EMPTY
footer. The standalone unit test passed (no engine open) — only the live
`_dash-layout` rendered-DOM check exposed it. Fix routes through the engine's existing
`_sql_client`. **SHA stamp + 200 prove code is live, not that the feature works** — the
rendered check is mandatory for behaviour, not just layout.

**Verified live (rendered footers, was→now):** demographics 2023→2025, health
2022→2024, living_conditions 2022→2025, national_accounts/science/trade/transport/
education/tourism/production 2023→2025, environment/energy 2023→2024, prices/
labour_market/financial_markets 2024→2025, public_finance 2025. All match warehouse
truth. Fleet SHA-verified: all 16 on HEAD `8b2f620a`.

**Known limitation (documented, accepted):** derives at *domain* granularity from
`all_indicators`, not from the exact metrics a page renders — a future metric lagging
its domain's max year could overstate by one year on that one card. Per-displayed-
metric resolution is the future enhancement if precision is ever needed.

## How the footer auto-derive works (for next maintainer)
- `footer_data_domain` in dashboard.yml = domain_id code(s): scalar `PUB` or list
  `[MAC, AGR]`. 16-dashboard slug→code map lives only in the YAMLs (declarative plane).
- Engine reads via `_get_engine()._sql_client.query(sql)` — the shared RO connection.
  Do NOT open a fresh `duckdb.connect()` (config-conflict → silent empty-footer fallback).
- Codes sanitised to uppercase-alpha before inlining (SQL client takes raw stmt, no
  bind params). Bad/empty/injection → None → literal fallback.

## Recent commits
- 8b2f620a fix(dbr): footer auto-derive must reuse engine's DuckDB connection (OR-165)
- b86b2d63 feat(dbr): auto-derive footer_updated from live warehouse data (OR-165)
- f7be910e docs: run #49 — mobile active-section pill + 2-up KPI grid
- 80ca7eb9 feat(dbr): mobile active-section label pill + 2-up KPI grid
- 10e36b7e docs: run #48 — mobile sidebar always-visible narrow rail

## What's next (unblocked, autonomous)
- **dbr feature backlog (all engine-plane, High/Med):** OR-159 choropleth/map (High),
  OR-160 cross-filtering (High), OR-162 number-format templates, OR-161 date-range
  slicer + time-intelligence. Each is a sizable engine feature → branch+PR+critic+
  redeploy; pick one per run, don't batch.
- OR-88 NUTS2 regional coverage expansion (Data, Med) — needs source check.

## Standing blockers (all PO-side)
- OR-153 Telegram inbound · OR-90 Instagram token → OR-89 · OR-86 BDL key → crime/agri/
  business dashboards · OR-79 Ghost nav.
- Known untracked PO/bot WIP in tree (do NOT commit): `infra/discord-bot/bot.py`,
  `infra/systemd/or-*-bot.service`, `logs/`, `.claude/scheduled_tasks.lock`.

## Lessons
- **Rendered-DOM verification is non-negotiable for behaviour changes.** SHA stamp
  proves which code is live; 200 proves a process answered; only the `_dash-layout`
  (or Playwright) check proves the feature actually produces output. The empty-footer
  bug passed SHA + 200 + standalone unit test and would have shipped silently.
- A second in-process `duckdb.connect()` to a file the MetricFlow engine already holds
  fails with a config-mismatch error → reuse `_get_engine()._sql_client.query()`.
