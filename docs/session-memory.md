# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-04 (run #62 — quiet run, data-quality audit, OR-168 holding) -->

## Run #62 — [QUIET RUN] clean smoke + read-only data-quality audit. HEAD pending

Smoke all green: 5 probed dashboards + www 200; daily ingest 2026-06-03 exit=0
(confirmed in full log, not just the trap's service-ensure tail); inbox empty; no
Strategic / In-Progress / Todo; 0 failed units; 16/16 `dbr serve`. Release sweep:
**18/18 published, 0 drafts** (pipeline ran 02:01 UTC) → no reviewer spawns.

**Memory healthier than #61:** 1122 MiB available (vs 527), fleet RSS 2167 MiB —
but **swap 100% used (2047/2047)**, ceiling unchanged. OR-168 still binding → NO
heavy build (0 builds, 0 subagent spawns, fleet untouched).

**Data-quality audit (read-only):**
- **Curated marts lag raw ~6 days** (last_fetch ~2026-05-29). Root cause:
  `run_daily.sh` refreshes **raw only** (NBP+Eurostat) + restarts fleet — does NOT
  run dbt. **No product impact:** every dashboard shows annual/quarterly aggregates
  (financial_markets = annual-avg FX 2002–2025, not daily NBP), so a 6-day curated
  lag is immaterial. A daily cron `dbt` would add the very memory spike OR-168
  fights → deliberately NOT added. Ad-hoc stop-16→dbt→restart during builds is fine.
- **PUB latest=2029** = legitimate fiscal forecasts (2026–29 all obs_status='p',
  Stability Programme/AWG), not a data error.

## Run #61 — [QUIET RUN] fleet healthy, OR-168 guardrails holding. HEAD 1b1a5add

18/18 published, 0 drafts. Verified #60's MemoryHigh=256M/MemoryMax=384M live via
`systemctl show` + per-svc usage 145–190 MiB (under cap). 527 MiB avail, swap 75%.
Doc drift flagged (CLAUDE.md `from dbr.semantic import query` stale → now
`semantic_query`/`semantic_query_data`). Reconstructed missing #60 decisions entry.

## Run #60 — [OR-168] dbr memory guardrails shipped. HEAD 987744b1 / 51c34ea8

09:24 cull was a full reboot (global OOM), not a dbr bug. 16 svc ≈ 2,942 MB cgroup
on 3.7 GB box; 2 GiB `/swapfile` since 2026-03-16. Shipped (987744b1):
`MemoryAccounting=yes`/`MemoryHigh=256M`/`MemoryMax=384M` on all 16 units +
`_render_systemd_unit` template (survives `dbr run`). Whole-box OOM reboots →
bounded per-svc cgroup-kill+autorestart. Still PO-side: harden ≠ capacity; need
swap grow 2→6 GiB or RAM.

## OOM diagnostics cheat-sheet (runs #58–62)
- Fleet check: `systemctl list-units 'or-*.service' --state=active`, `free -m`,
  `ps -eo pid,rss,etime,args | grep '[d]br serve'` (expect 16: demographics,
  education, energy, environment, financial_markets, health, labour_market,
  living_conditions, national_accounts, prices, production, public_finance,
  science, tourism, trade, transport). A "17th" is usually this session's own
  grep cwd helper (`/tmp/claude-*-cwd`), not an orphan — check the args.
- Guardrails check: `systemctl show or-<d>.service -p MemoryHigh -p MemoryMax
  -p MemoryCurrent --value` (268435456=256M=High, 402653184=384M=Max).
- Find non-fleet RAM hogs: `ps -eo pid,rss,etime,stat,args --sort=-rss | head`.
  `Sl+` = foreground/terminal-attached (= PO manual session, don't kill).
- Raw SQL on warehouse: `duckdb.connect(path, read_only=True)` (read concurrent
  with fleet OK). `dbr.semantic.semantic_query_data` is MetricFlow-only.
- My NOPASSWD sudo = ONLY `systemctl <restart|start|stop|status|enable> or-*`,
  `daemon-reload`, `cp .../infra/systemd/*.service /etc/systemd/system/`. No swap.
- Recovery tool: `python3 infra/scheduler/redeploy_dashboards.py` (restart 16 +
  verify each `<meta dbr-build>` == HEAD; non-zero exit = NOT resolved).

## Pipeline freshness note (from #62)
- `run_daily.sh` = raw refresh + fleet restart ONLY (no dbt). Curated lags raw
  between manual dbt runs. Fine because all dashboards are annual/quarterly. Don't
  "fix" with a daily cron dbt — it spikes memory (OR-168). Rebuild curated only
  inside a deliberate build using the stop-16→dbt→restart pattern.

## What's next (autonomous, ONLY once memory is safe — OR-168)
- **Until OR-168 resolved, avoid heavy builds** (dbt/dbr/subagents) — they can
  re-cull the fleet at low available RAM. Prefer light/no-mutation runs; if the
  fleet 502s, re-run redeploy_dashboards.py and re-note OR-168.
- dbr feature backlog (engine, branch+PR+critic+redeploy, one/run, don't batch):
  **OR-160 cross-filter (High)**, OR-161 date slicer, OR-162 number-format.
- More NUTS2 metrics: only gdp_per_capita_regional reaches full 17-NUTS2 cleanly;
  others need a by-domain intermediate change first (data-plane, safe when RAM ok).

## Engine-tree state
- Clean except known untracked PO/bot WIP (never commit): `infra/discord-bot/bot.py`,
  `infra/systemd/or-*-bot.service`, `logs/`, `.claude/scheduled_tasks.lock`,
  `products/blog/reviews/release-report.md` (regenerated each release sweep).
- All 16 dashboards on stamp `2b09320a` (#60 infra-only change didn't bump stamps;
  next natural `dbr run`/redeploy will sync to HEAD).

## Choropleth maintainer notes (from #57, unchanged)
- `packages/dbr/src/dbr/visuals/choropleth.py`. Renders as a fill-chart via
  `chart_with_optional_table` — do NOT bake `fig.layout.height` on a geo (overflows
  the row). `_BUNDLED_GEOJSON`: name → (path, featureidkey, view-or-None). Design
  rests on warehouse `geo` == GISCO `NUTS_ID`; YAML must filter EU27_2020/EA20.

## Prod-build-with-lock pattern (#54/#57) — use sparingly under OR-168
dbt build needing the DuckDB write lock: build on /tmp COPY → stop 16 → dbt run+test
on prod → restart 16 → verify rows + stamp. NB stop-16 + restart spikes memory;
risky while the box is low on available RAM.

## Standing blockers (all PO-side)
- **OR-168 VPS memory overcommit (Urgent)** — guardrails shipped (#60), holding
  (#61–62). Still needs swap grow 2→6 GiB (PO 3 cmds or NOPASSWD extension) or RAM.
- OR-153 Telegram inbound · OR-90 Instagram token → OR-89 · OR-86 BDL key ·
  OR-79 Ghost nav.

## Lessons
- **Audit the pipeline before "fixing" apparent staleness** (#62). Curated lagging
  raw looked like a bug; checking what the dashboards actually display (annual
  aggregates) proved it immaterial — and the obvious fix (daily cron dbt) would
  worsen OR-168. Cheap read-only checks beat a risky reflexive rebuild.
- **Verify guardrails actually hold, don't assume** (#61). `systemctl show` +
  per-svc usage under cap proves a prior fix is durable, not just committed.
- **Measure the whole box, not just the fleet** (#59); swing factor is concurrent
  non-fleet load. When the same P0 recurs, measure before re-guessing (#58).
