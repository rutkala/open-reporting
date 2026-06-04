# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-04 (run #61 — quiet run, OR-168 guardrails verified holding) -->

## Run #61 — [QUIET RUN] fleet healthy, OR-168 guardrails holding. HEAD pending

Smoke all green: 5 probed dashboards + www 200; ingest exit=0 (Eurostat fresh
2026-06-03, 98,091 obs); inbox empty; no Strategic / In-Progress / Todo. Open
Urgents (OR-168, OR-153, OR-90) all PO-side. Release sweep: **18/18 published, 0
drafts** → no reviewer spawns. **Verified run #60's guardrails live & holding:**
`systemctl show` confirms MemoryHigh=256M / MemoryMax=384M; per-svc usage 145–190
MiB, all under MemoryHigh. Exactly 16 `dbr serve` (apparent "17th" = transient
grep cwd helper). No failed units.

**Memory unchanged:** 527 MiB available, swap 75% used (1523/2047). OR-168 still
binding → deliberately NO heavy build (OR-160/161/162 redeploy + NUTS2 dbt build
both spike memory, risk re-cull at 527 MiB). 0 builds, 0 subagent spawns.

**Doc drift noted (NOT fixed — CLAUDE.md is protected):** Development Commands
example `from dbr.semantic import query` is stale; API is now `semantic_query` /
`semantic_query_data` (MetricFlow-only, not raw SQL). For raw SQL use
`duckdb.connect(path, read_only=True)` — concurrent reads work fine alongside the
live fleet (no lock contention). Flagged to PO in outbox.

**Audit note:** run #60's decisions.md entry was missing (its commit touched
session-memory + units only); reconstructed #60 into decisions.md this run.

## Run #60 — [OR-168] dbr memory guardrails shipped. HEAD 987744b1 / 51c34ea8

Diagnosed: NOT a dbr bug — 09:24 cull was a full reboot (global OOM killer).
Structural overcommit: 16 svc ≈ 2,942 MB cgroup on 3.7 GB box; swap (2 GiB
`/swapfile`) exists since 2026-03-16. **Shipped (987744b1):** `MemoryAccounting=yes`
/ `MemoryHigh=256M` / `MemoryMax=384M` on all 16 units + `_render_systemd_unit`
template (survives `dbr run`). Whole-box OOM reboots → bounded per-svc
cgroup-kill+autorestart. All 16 under MemoryHigh in normal op. Infra-only, zero
render-path change → did NOT force a stamp-bumping restart. **Still PO-side:**
guardrails harden failure, add no capacity. Need swap grow 2→6 GiB or RAM.

## OOM diagnostics cheat-sheet (runs #58–61)
- Fleet check: `systemctl list-units 'or-*.service' --state=active`, `free -m`,
  `ps -eo pid,rss,etime,args | grep '[d]br serve'` (expect 16: demographics,
  education, energy, environment, financial_markets, health, labour_market,
  living_conditions, national_accounts, prices, production, public_finance,
  science, tourism, trade, transport). A "17th" is usually this session's own
  grep cwd helper (`/tmp/claude-*-cwd`), not an orphan — check the args.
- Guardrails check: `systemctl show or-<d>.service -p MemoryHigh -p MemoryMax
  -p MemoryCurrent --value` (NB systemd may print MemoryCurrent first; the two
  constants 268435456=256M=High, 402653184=384M=Max).
- Find non-fleet RAM hogs: `ps -eo pid,rss,etime,stat,args --sort=-rss | head`.
  `Sl+` = foreground/terminal-attached (= PO manual session, don't kill).
- Raw SQL on warehouse: `duckdb.connect(path, read_only=True)` (read concurrent
  with fleet OK). `dbr.semantic.semantic_query_data` is MetricFlow-only.
- My NOPASSWD sudo = ONLY `systemctl <restart|start|stop|status|enable> or-*`,
  `daemon-reload`, `cp .../infra/systemd/*.service /etc/systemd/system/`. No swap.
- Recovery tool: `python3 infra/scheduler/redeploy_dashboards.py` (restart 16 +
  verify each `<meta dbr-build>` == HEAD; non-zero exit = NOT resolved).

## What's next (autonomous, ONLY once memory is safe — OR-168)
- **Until OR-168 resolved, avoid heavy builds** (dbt/dbr/subagents) — they can
  re-cull the fleet at ~500 MiB available. Prefer light/no-mutation runs; if the
  fleet 502s, re-run redeploy_dashboards.py and re-note OR-168.
- dbr feature backlog (engine, branch+PR+critic+redeploy, one/run, don't batch):
  **OR-160 cross-filter (High)**, OR-161 date slicer, OR-162 number-format.
- More NUTS2 metrics: only gdp_per_capita_regional reaches full 17-NUTS2 cleanly;
  others need a by-domain intermediate change first (data-plane, safe when RAM ok).

## Engine-tree state
- Clean except known untracked PO/bot WIP (never commit): `infra/discord-bot/bot.py`,
  `infra/systemd/or-*-bot.service`, `logs/`, `.claude/scheduled_tasks.lock`,
  `products/blog/reviews/release-report.md` (regenerated each release sweep).
- All 16 dashboards on stamp `2b09320a` (run #60 infra-only change didn't bump
  stamps; next natural `dbr run`/redeploy will sync to HEAD).

## Choropleth maintainer notes (from #57, unchanged)
- `packages/dbr/src/dbr/visuals/choropleth.py`. Renders as a fill-chart via
  `chart_with_optional_table` — do NOT bake `fig.layout.height` on a geo (overflows
  the row). `_BUNDLED_GEOJSON`: name → (path, featureidkey, view-or-None). Design
  rests on warehouse `geo` == GISCO `NUTS_ID`; YAML must filter EU27_2020/EA20.

## Prod-build-with-lock pattern (#54/#57) — use sparingly under OR-168
dbt build needing the DuckDB write lock: build on /tmp COPY → stop 16 → dbt run+test
on prod → restart 16 → verify rows + stamp. NB stop-16 + restart spikes memory;
risky while the box is at ~500 MiB available.

## Standing blockers (all PO-side)
- **OR-168 VPS memory overcommit (Urgent)** — guardrails shipped (#60), holding
  (#61). Still needs swap grow 2→6 GiB (PO 3 cmds or NOPASSWD extension) or RAM.
- OR-153 Telegram inbound · OR-90 Instagram token → OR-89 · OR-86 BDL key ·
  OR-79 Ghost nav.

## Lessons
- **Verify guardrails actually hold, don't assume.** #61 confirmed #60's
  MemoryHigh/Max are live via `systemctl show` + per-svc usage under cap — cheap
  light check that proves the prior run's fix is durable, not just committed.
- **Measure the whole box, not just the fleet** (#59). Fleet ≈ 2.2–2.75 GiB; the
  swing factor is concurrent non-fleet load (manual opencode, claude run, bots).
- When the same P0 recurs, measure before re-guessing (#58).
