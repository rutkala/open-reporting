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

## Runs #58–63 (condensed — superseded by #64's static conversion)
OR-168 OOM saga: 09:24 cull (#58) was a full reboot (global OOM), not a dbr bug —
16 `dbr serve` ≈ 2.9 GB cgroup on a 3.7 GB box overcommitted RAM. #60 shipped per-svc
MemoryHigh=256M/Max=384M guardrails (those `_render_systemd_unit` directives are now
moot — services retired #64, but harmless if units ever restart). #59/#63 lesson:
low avail-RAM was sometimes a concurrent PO VS Code session, not the fleet. **All of
this is now obsolete: the fleet is gone (#64).**

## Pipeline freshness note (still true)
`run_daily.sh` = raw refresh only (no dbt). Curated marts lag raw between manual dbt
runs — fine because all dashboards show annual/quarterly aggregates. To refresh
dashboard data: `dbt run` (DuckDB write lock now FREE — no live readers) then
`python3 infra/scheduler/redeploy_dashboards.py` (rebuilds static). No daily cron dbt.

## Engine-tree state
- Clean except known untracked PO/bot WIP (never commit): `infra/discord-bot/bot.py`,
  `infra/systemd/or-*-bot.service`, `logs/`, `.claude/scheduled_tasks.lock`,
  `products/blog/reviews/release-report.md`.
- 16 dashboards = static HTML in `infra/nginx/html/<domain>/` (gitignored), on stamp
  == HEAD (1d9973ee). `infra/systemd/or-<domain>.service` files retained but services
  stopped (PO to `disable` for reboot durability — OR-168 / outbox).

## Choropleth maintainer notes (from #57, unchanged)
- `packages/dbr/src/dbr/visuals/choropleth.py`. Renders as a fill-chart via
  `chart_with_optional_table` — do NOT bake `fig.layout.height` on a geo (overflows
  the row). `_BUNDLED_GEOJSON`: name → (path, featureidkey, view-or-None). Design
  rests on warehouse `geo` == GISCO `NUTS_ID`; YAML must filter EU27_2020/EA20.
  (Verified renders correctly in static export, #64.)

## Standing blockers (all PO-side)
- **OR-168** — root-fixed (#64, static conversion); only `systemctl disable or-{16}`
  remains (sudo gap, in outbox). Then closes.
- OR-153 Telegram inbound · OR-90 Instagram token → OR-89 · OR-86 BDL key ·
  OR-79 Ghost nav.

## Lessons
- **Verify the premise against the docs, but trust a sound engineering call** (#64).
  PO said "convert to static, PROJECT.md mandates it" — PROJECT.md actually mandated
  the *opposite* (interactive Dash). Surfaced the contradiction, but the call was right
  (dashboards had zero callbacks); shipped it + corrected the docs.
- **Measure the WHOLE box before re-diagnosing** (#59/#63): low avail-RAM was often a
  concurrent PO VS Code Remote-SSH session, not the fleet.
