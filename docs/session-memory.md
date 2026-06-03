# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-03 (run #58 — P0 fleet OOM recovery + OR-168) -->

## Run #58 — [P0 RECOVERY] whole dashboard fleet was OOM-culled. HEAD bd65761c

**At start: all 16 dashboards 502** (only www up). Every `or-<domain>.service`
SIGTERM-dead at 09:24:31 UTC (between 07 and 12 runs), never restarted. Portal
dark ~2.5h.

**Fixed:** no lock/stuck proc → `redeploy_dashboards.py` → 16/16 PASS on HEAD
`bd65761c`, live-verified (200 + Dash app served, not portal index).

**ROOT CAUSE (measured, not the old "interrupted redeploy" guess): VPS memory
overcommit.** `free -h`: 3.7 GiB box, swap full, ~222 MiB available. RSS: 16
`dbr serve` = **3,276 MB (~205 MB each) = 88% of RAM** before docker + 13 bot
listeners (168 MB) + autonomous `claude -p` (152 MB). Kernel/OOM culls the fleet.
After restart: still only **256 MiB available — fragile, will recur.** Run #46's
3-dashboard P0 was almost certainly the same mechanism, mis-diagnosed.

**Escalated:** filed **OR-168 (Infra, Urgent)** — recommend **add 4 GiB swap**
(zero-cost, reversible, 9.9 GiB disk free). I CANNOT do it: NOPASSWD allowlist has
no swap/fallocate tooling; RAM upgrade = recurring cost (hard floor). PO must run
3 cmds OR extend my sudoers. Durable fallback = RAM 3.7→8 GiB. Flagged in outbox.

**Deliberately no feature work** — a build/subagent at 256 MiB available would
re-trigger the cull. Did NOT remove any live dashboard (silent 502s worse than
bounded recovery). Release sweep: 18/18 published, 0 drafts → skipped spawns.

## Memory ops cheat-sheet (run #58)
- Diagnose a 502 fleet: `systemctl list-units 'or-*.service'`, `free -h`,
  `ps -eo rss,args --sort=-rss | head`, `fuser data/warehouse.duckdb`.
- Each `dbr serve` ≈ 205 MB RSS (MetricFlow/duckdb resident). 16 of them don't
  fit in 3.7 GiB alongside bots + docker + a claude run. This is the ceiling.
- My NOPASSWD sudo = ONLY `systemctl <restart|start|stop|status|enable> or-*`,
  `daemon-reload`, `cp .../infra/systemd/*.service /etc/systemd/system/`. No swap.
- Recovery tool: `python3 infra/scheduler/redeploy_dashboards.py` (restart 16 +
  verify each `<meta dbr-build>` == HEAD; non-zero exit = not resolved).

## Recent commits
- bd65761c docs: run #57 — OR-167 voivodeship GDP map live + outbox
- 70f8f0e4 feat(national_accounts): map + ranked bar side-by-side (OR-167)
- ddc2cd3b Merge OR-167: choropleth fills flex cell (Poland map overlap fix)
- f1de9c3e docs(dbr): correct choropleth options.height docstring
- 7291111d fix(dbr): choropleth fills its flex cell instead of fixed height (OR-167)
- 85569855 feat(warehouse): voivodeship GDP-per-capita NUTS2 regional map (OR-167)

## What's next (autonomous, ONLY once memory is safe — OR-168)
- **Until OR-168 is resolved, avoid heavy builds** (dbt/dbr/subagents) — they can
  re-cull the fleet at 256 MiB available. Prefer light/no-mutation runs; if the
  fleet is 502 again, just re-run redeploy_dashboards.py and re-flag OR-168.
- dbr feature backlog (engine, branch+PR+critic+redeploy, one/run, don't batch):
  **OR-160 cross-filter (High)**, OR-161 date slicer, OR-162 number-format.
- More NUTS2 metrics: only gdp_per_capita_regional reaches full 17-NUTS2 cleanly;
  others need a by-domain intermediate change first (data-plane, safe when RAM ok).

## Engine-tree state
- Clean except known untracked PO/bot WIP (never commit): `infra/discord-bot/bot.py`,
  `infra/systemd/or-*-bot.service`, `logs/`, `.claude/scheduled_tasks.lock`,
  `products/blog/reviews/release-report.md` (regenerated each release sweep).
- All 16 dashboards on stamp `bd65761c` (= HEAD) after this run's recovery redeploy.

## Choropleth maintainer notes (from #57, unchanged)
- `packages/dbr/src/dbr/visuals/choropleth.py`. Renders as a fill-chart via
  `chart_with_optional_table` — do NOT bake `fig.layout.height` on a geo (overflows
  the row). `_BUNDLED_GEOJSON`: name → (path, featureidkey, view-or-None). Design
  rests on warehouse `geo` == GISCO `NUTS_ID`; YAML must filter EU27_2020/EA20.

## Prod-build-with-lock pattern (#54/#57) — use sparingly under OR-168
dbt build needing the DuckDB write lock: build on /tmp COPY → stop 16 → dbt run+test
on prod → restart 16 → verify rows + stamp. NB stop-16 + restart spikes memory;
risky while the box is at ~256 MiB available.

## Standing blockers (all PO-side)
- **OR-168 VPS memory overcommit (Urgent, NEW)** — fleet gets OOM-culled; needs
  swap (PO 3 cmds or sudoers extension) or RAM upgrade.
- OR-153 Telegram inbound · OR-90 Instagram token → OR-89 · OR-86 BDL key ·
  OR-79 Ghost nav.

## Lessons
- **When the same P0 recurs, measure before re-guessing.** Run #46 called the
  dead-fleet "interrupted redeploy"; `free -h` + per-proc RSS this run proved it's
  a capacity ceiling (16×205 MB > 3.7 GiB). A restart at 256 MiB available is a
  reprieve, not a fix.
- A "verified clean" wide map can mask a layout bug a tall map exposes (#57).
