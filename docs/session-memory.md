# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-03 (run #60 — OR-168 memory guardrails shipped) -->

## Run #60 — [OR-168] dbr memory guardrails shipped. HEAD 987744b1

`/goal` urgent: "high memory, probably dbr serve." **Diagnosed: NOT a dbr bug** —
`dbr serve` is plain Dash `app.run` (single proc, no reloader; child python3 is
the 2 MB mp resource_tracker). Structural overcommit: 16 services = **2,942 MB
cgroup mem** (per-svc 127–214 M) on 3.7 GB box. Swap (`/swapfile`, 2 GiB) exists
since 2026-03-16 — NOT absent as OR-168 first said. 09:24 event was a **full
reboot** (global OOM killer), confirmed by uptime.

**Shipped (commit 987744b1, pushed):** `MemoryAccounting=yes` / `MemoryHigh=256M`
/ `MemoryMax=384M` on all 16 units + the `_render_systemd_unit` template (survives
`dbr run`). Converts whole-box OOM reboots → bounded per-svc cgroup-kill+autorestart.
All 16 sit under MemoryHigh in normal op (largest public_finance 214 M), so no
interference. Verified live (`systemctl show`), 16/16 active, stamp-verify PASS.

**Stamp note:** 16 dashboards serve `2b09320a`, HEAD is `987744b1`. The commit is
**infra-only (units + template fn), zero `dbr serve` render-path change** → output
identical. Did NOT re-restart to bump stamps (200 MiB available — the spike I'm
mitigating). Next natural `dbr run`/redeploy will sync stamps. **Do not let
redeploy --verify-only false-flag this into a needless full restart.**

**Still PO-side (OR-168 stays Urgent/open):** guardrails harden failure, add no
capacity (~200 MiB avail, swap 1.3/2.0 used). Need swap grow 2→6 GiB (PO runs it,
or add `fallocate`/`mkswap`/`swapon` to my NOPASSWD allowlist) OR RAM upgrade.

## Run #59 — [QUIET RUN] healthy fleet; OR-168 reframed. HEAD 16c39397

All 16 dashboards up, www up, ingest exit=0, inbox empty, no Strategic/Todo/
In-Progress. `free -h` = **306 MiB available, swap full** — same fragile ceiling
as #58, no new cull. Release sweep: 18/18 published, 0 drafts → skipped reviewer
spawns. No feature work (correct under OR-168 — a build at 306 MiB risks re-cull).

**Key finding (measured): the fleet is NOT the whole OOM story.** 16 `dbr serve`
= **~2.2 GiB RSS** (96–177 MB each — lower than #58's 205 MB/proc guess). The
cull trigger is **concurrent non-fleet load stacked on top**: two detached
`opencode` procs = **469 MB** (289+180), 6.7h old, `Sl+` foreground-attached,
non-systemd parents → **PO's manual interactive opencode sessions** (NOT the
`or-opencode-bot` service, cgroup 11.7 MB). + autonomous `claude -p` (~150–275 MB)
+ 13 bot listeners (~207 MB). Fleet+docker+bots fits; manual opencode + a claude
run on top is what pushes available→0. #58's 09:24 cull likely = this stacking.

**Acted:** added measured comment to OR-168 with the RSS breakdown + a **zero-cost
operational mitigation** for PO (don't leave heavy interactive agents running for
hours alongside the full fleet until swap exists — those 2 sessions alone exceed
the swap deficit). Did NOT kill the opencode procs (PO's live work). Swap stays
the durable recommended fix.

## OOM diagnostics cheat-sheet (runs #58–59)
- Fleet check: `systemctl list-units 'or-*.service'`, `free -h`,
  `ps -eo pid,rss,etime,args | grep '[d]br serve'` (expect exactly 16:
  demographics, education, energy, environment, financial_markets, health,
  labour_market, living_conditions, national_accounts, prices, production,
  public_finance, science, tourism, trade, transport).
- Find non-fleet RAM hogs: `ps -eo pid,rss,etime,stat,args --sort=-rss | head`.
  `Sl+` = foreground/terminal-attached (= PO manual session, don't kill).
  Service cgroup mem: `systemctl show <svc> -p MemoryCurrent --value`.
- My NOPASSWD sudo = ONLY `systemctl <restart|start|stop|status|enable> or-*`,
  `daemon-reload`, `cp .../infra/systemd/*.service /etc/systemd/system/`. No swap.
- Recovery tool: `python3 infra/scheduler/redeploy_dashboards.py` (restart 16 +
  verify each `<meta dbr-build>` == HEAD; non-zero exit = NOT resolved).

## What's next (autonomous, ONLY once memory is safe — OR-168)
- **Until OR-168 resolved, avoid heavy builds** (dbt/dbr/subagents) — they can
  re-cull the fleet at ~300 MiB available. Prefer light/no-mutation runs; if the
  fleet 502s again, re-run redeploy_dashboards.py and re-note OR-168.
- dbr feature backlog (engine, branch+PR+critic+redeploy, one/run, don't batch):
  **OR-160 cross-filter (High)**, OR-161 date slicer, OR-162 number-format.
- More NUTS2 metrics: only gdp_per_capita_regional reaches full 17-NUTS2 cleanly;
  others need a by-domain intermediate change first (data-plane, safe when RAM ok).

## Recent commits
- 16c39397 docs: run #58 — P0 fleet OOM recovery + OR-168 (VPS memory overcommit)
- bd65761c docs: run #57 — OR-167 voivodeship GDP map live + outbox
- 70f8f0e4 feat(national_accounts): map + ranked bar side-by-side (OR-167)
- ddc2cd3b Merge OR-167: choropleth fills flex cell (Poland map overlap fix)
- f1de9c3e docs(dbr): correct choropleth options.height docstring
- 85569855 feat(warehouse): voivodeship GDP-per-capita NUTS2 regional map (OR-167)

## Engine-tree state
- Clean except known untracked PO/bot WIP (never commit): `infra/discord-bot/bot.py`,
  `infra/systemd/or-*-bot.service`, `logs/`, `.claude/scheduled_tasks.lock`,
  `products/blog/reviews/release-report.md` (regenerated each release sweep).
- All 16 dashboards on stamp `bd65761c` (= HEAD before this run's docs commit).

## Choropleth maintainer notes (from #57, unchanged)
- `packages/dbr/src/dbr/visuals/choropleth.py`. Renders as a fill-chart via
  `chart_with_optional_table` — do NOT bake `fig.layout.height` on a geo (overflows
  the row). `_BUNDLED_GEOJSON`: name → (path, featureidkey, view-or-None). Design
  rests on warehouse `geo` == GISCO `NUTS_ID`; YAML must filter EU27_2020/EA20.

## Prod-build-with-lock pattern (#54/#57) — use sparingly under OR-168
dbt build needing the DuckDB write lock: build on /tmp COPY → stop 16 → dbt run+test
on prod → restart 16 → verify rows + stamp. NB stop-16 + restart spikes memory;
risky while the box is at ~300 MiB available.

## Standing blockers (all PO-side)
- **OR-168 VPS memory overcommit (Urgent)** — fleet gets OOM-culled; needs swap
  (PO 3 cmds or sudoers extension) or RAM upgrade. Now also has a zero-cost interim
  mitigation documented (don't stack manual opencode/gemini sessions on the fleet).
- OR-153 Telegram inbound · OR-90 Instagram token → OR-89 · OR-86 BDL key ·
  OR-79 Ghost nav.

## Lessons
- **Measure the whole box, not just the fleet.** #58 blamed 16×205 MB dbr procs;
  #59 measured them at 96–177 MB (~2.2 GiB total) and found the real swing factor
  is concurrent non-fleet load (manual opencode 469 MB + claude run + bots). The
  fleet fits — it's the stacking that kills it.
- When the same P0 recurs, measure before re-guessing (#58).
- A "verified clean" wide map can mask a layout bug a tall map exposes (#57).
