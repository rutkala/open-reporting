# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-04 (run #64 — OR-168 ROOT FIX: dashboards → static HTML, Dash fleet retired) -->

## Run #64 — [OR-168 ROOT FIX] dashboards converted to static HTML; 16 Dash servers retired

PO directive: stop masking OR-168 with swap — remove the always-on Dash servers.
**Done.** Available RAM **884 MiB → 2.5 GiB**, swap **2.0 G → 0.3 G**. The 16-server
overcommit (~2.9 GB) that caused the global-OOM reboots is eliminated.

**Diagnosis that unlocked it:** the 16 dashboards use ZERO server callbacks (only
line/card/bar/column/choropleth; no slicers/cross-filter/tabs/Interval;
`Location(refresh=False)`). Every chart is a pre-computed Plotly figure; only
client-side hover/zoom interactivity, which survives static export. The Dash backend
was pure overhead. NB: PROJECT.md had *mandated* "Interactive dashboards, Dash+Plotly+
MetricFlow" — the static premise contradicted the doc, but the call was right; docs now updated.

**Shipped (engine):** `packages/dbr/src/dbr/static_export/` + `dbr build`. Walks the
same compiled tree → self-contained static HTML (Plotly `to_html`, ONE shared
`infra/nginx/html/assets/plotly.min.js`, reuses exact `_CSS`/scrollspy/sidebar JS +
`<meta dbr-build>` stamp = byte-identical layout). `UnsupportedComponentError` hard-fails
if a dashboard ever adds interactivity (guards both `ctx.has_bindings()` and the dcc tree).
architecture-critic CONDITIONAL → all fixes applied (shared asset, strict guard, atomic
write, freshness verify).

**Cutover:** 16 pre-rendered to `infra/nginx/html/<domain>/`; nginx `try_files` static
(no proxy); `dbr run` rewritten (build → static route → reload, no systemd/port);
`_render_nginx_block` static; `redeploy_dashboards.py` rebuilds+verifies file stamps
(hard-fail on build error); `run_daily.sh` no longer stops/restarts fleet (no DuckDB
lock holder). 16 `or-<domain>.service` STOPPED. Verified 16/16 200 + stamp==HEAD + SVG.

**KEY OPS CHANGES (supersede #58–63 cheat-sheets):**
- Dashboards = static files in `infra/nginx/html/<domain>/index.html` (gitignored
  build artifacts; rebuilt by `dbr run`/`redeploy_dashboards.py`). NO `dbr serve`,
  NO `or-<domain>.service`, NO ports. Old OOM/fleet-502 recovery is obsolete.
- Rebuild+verify: `python3 infra/scheduler/redeploy_dashboards.py` (builds 16 → web
  root, checks each built `<meta dbr-build>` == HEAD). `--verify-only` reads stamps.
- A dashboard change OR data refresh (dbt) now needs a REBUILD (not restart) to show.
- Live verify: `curl -sk --resolve portal.open-reporting.dev:443:127.0.0.1 https://portal.open-reporting.dev/<domain>/`.

**ONE PO ACTION (sudo gap):** 16 units stopped but still `enabled` — reboot would
restart them (benign: 2.5 GiB headroom + #60 guardrails = no OOM, just wasted RAM).
`disable`/`mask`/`rm` NOT in my NOPASSWD allowlist. PO runs `systemctl disable or-{16}`
+ `daemon-reload` (in outbox + OR-168), or extends sudoers. Then OR-168 closes.

**Held (PO call):** OR-160 cross-filter + OR-161 date-picker = backend-only, on hold.
OR-162 number-format + OR-161 time-windows = build-time, still doable.

## Run #63 — [QUIET RUN] tight RAM = concurrent PO VS Code session, not fleet. HEAD pending

Smoke all green: 5 probed dashboards + www 200; daily ingest 2026-06-03 exit=0;
inbox empty; no Strategic / In-Progress / Todo; 0 failed units; 16/16 `dbr serve`.
Release sweep: **18/18 published, 0 drafts** → no reviewer spawns.

**Tightest available-RAM seen (347 MiB, swap 100% 2047/2047) — but benign + external.**
Measured the whole box (OR-168 lesson): fleet RSS **1780 MiB, LOWER than #62's 2167**;
guardrails live (High=256M/Max=384M, per-svc Cur ~111–132 MiB, under cap). Pressure =
**concurrent PO VS Code Remote-SSH session** (Pylance 407M + extensionHost 213M +
server-main 122M + helpers ≈ 900M+) plus this run's own `claude -p` (269M). The
"fleet + concurrent sessions" framing from #59 — NOT a fleet regression. Did not
touch PO's VS Code procs. → NO heavy build (0 builds, 0 spawns, fleet untouched).

Backlog reviewed (28 issues): everything actionable is PO/credential-blocked or a
memory-heavy engine build deferred under OR-168.

## Run #62 — [QUIET RUN] clean smoke + read-only data-quality audit. HEAD 02165649

18/18 published, 0 drafts. 1122 MiB avail, fleet RSS 2167, swap 100%. Data-quality
audit: curated marts lag raw ~6 days (run_daily.sh = raw refresh + fleet restart
only, no dbt) — immaterial because all dashboards show annual/quarterly aggregates;
a daily cron dbt would worsen OR-168, so NOT added. PUB latest=2029 = legit fiscal
forecasts (obs_status='p', Stability Programme/AWG), not a data error.

## Run #61 — [QUIET RUN] fleet healthy, OR-168 guardrails holding. HEAD 1b1a5add

18/18 published, 0 drafts. Verified #60's MemoryHigh=256M/MemoryMax=384M live via
`systemctl show` + per-svc 145–190 MiB (under cap). 527 MiB avail, swap 75%. Doc
drift flagged (CLAUDE.md `from dbr.semantic import query` stale → now
`semantic_query`/`semantic_query_data`).

## Run #60 — [OR-168] dbr memory guardrails shipped. HEAD 987744b1 / 51c34ea8

09:24 cull was a full reboot (global OOM), not a dbr bug. 16 svc ≈ 2,942 MB cgroup
on 3.7 GB box; 2 GiB `/swapfile` since 2026-03-16. Shipped: MemoryAccounting=yes/
MemoryHigh=256M/MemoryMax=384M on all 16 units + `_render_systemd_unit` template
(survives `dbr run`). Whole-box OOM reboots → bounded per-svc cgroup-kill+restart.
Still PO-side: harden ≠ capacity; need swap grow 2→6 GiB or RAM.

## OOM diagnostics cheat-sheet (runs #58–63)
- Fleet check: `systemctl list-units 'or-*.service' --state=active`, `free -m`,
  `ps -eo pid,rss,etime,args | grep '[d]br serve'` (expect 16: demographics,
  education, energy, environment, financial_markets, health, labour_market,
  living_conditions, national_accounts, prices, production, public_finance,
  science, tourism, trade, transport).
- **Measure the WHOLE box, not just the fleet** (#59, reconfirmed #63): when avail
  RAM is low but fleet RSS is flat/down, the swing factor is concurrent non-fleet
  load — a PO **VS Code Remote-SSH session** (`.vscode-server` node procs: Pylance,
  extensionHost, server-main ≈ 900M+) and/or this run's own `claude -p`. Don't kill
  PO's `.vscode-server` or `Sl+` terminal-attached procs.
- Guardrails check: `systemctl show or-<d>.service -p MemoryHigh -p MemoryMax
  -p MemoryCurrent --value` (268435456=256M=High, 402653184=384M=Max).
- Non-fleet hogs: `ps -eo pid,rss,etime,stat,args --sort=-rss | head`.
- Raw SQL on warehouse: `duckdb.connect(path, read_only=True)` (concurrent-safe).
  `dbr.semantic.semantic_query_data` is MetricFlow-only.
- NOPASSWD sudo = ONLY `systemctl <restart|start|stop|status|enable> or-*`,
  `daemon-reload`, `cp .../infra/systemd/*.service /etc/systemd/system/`. No swap.
- Recovery: `python3 infra/scheduler/redeploy_dashboards.py` (restart 16 + verify
  each `<meta dbr-build>` == HEAD; non-zero exit = NOT resolved).

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
  (#61–63). Still needs swap grow 2→6 GiB (PO 3 cmds or NOPASSWD extension) or RAM.
- OR-153 Telegram inbound · OR-90 Instagram token → OR-89 · OR-86 BDL key ·
  OR-79 Ghost nav.

## Lessons
- **Low avail-RAM ≠ fleet problem** (#63). Tightest available reading yet (347 MiB)
  but fleet RSS was actually down — root cause was a concurrent PO VS Code session.
  Measuring the whole box before re-diagnosing OR-168 avoided a false alarm and a
  needless fleet restart.
- **Audit the pipeline before "fixing" apparent staleness** (#62). Curated lagging
  raw looked like a bug; the dashboards display annual aggregates → immaterial, and
  the obvious fix (daily cron dbt) would worsen OR-168.
- **Verify guardrails actually hold, don't assume** (#61). `systemctl show` +
  per-svc usage under cap proves a prior fix is durable.
