# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-04 (run #65 — OR-162 value_format wired across visuals) -->

## Run #65 — OR-162 shipped: value_format honored in card/column/bar/table

Picked the one actionable backlog item (build-time, static-safe, no PO blocker).
**Found half-done:** a prior run added the `value_format` *schema + import* across
~14 visuals but never wired the rendering — silently ignored except choropleth/heatmap
(a documented-but-dead option = footgun). Completed it.

**Shipped (PR #65, squash-merged, HEAD `f8f64776`):**
- **card** — `options.value_format` overrides the semantic-layer KPI format (standard + compact)
- **column / bar** — `data_labels` via `format_value`; **exact no-op** (`f"{v:.1f}"`) when unset
- **table + companion table** — per-column `formats: {col: spec}` option
- **theme.yaml** — named templates moved to a `formats:` block (percent_1dp, percent_0dp,
  thousands, thousands_1dp, index_100, currency_bln), exposed as `dbr.theme.FORMATS`,
  deep-mergeable per project; `format_value` resolves theme over built-in fallback,
  applies Polish locale (space thousands, decimal comma).

**Verified:** 16/16 `dbr validate`; format_value unit-checked (`1234567 → "1 234 567"`);
`redeploy_dashboards.py` rebuilt all 16 static on HEAD (exit 0, every stamp == f8f64776);
live 200 + stamp==HEAD + Plotly content. No production YAML uses the new options yet →
rendered output unchanged (latent-correctness fix, unblocks authors). code-reviewer
CONDITIONAL → P2 backward-compat fixed (bar/column no-op preserved).

**Deferred (OR-162 comment):** gauge/bullet (Plotly Indicator `valueformat`, unused),
line hover (65 charts, own change), `currency_pln` (no need yet).

## Run #64 — [OR-168 ROOT FIX] dashboards → static HTML; 16 Dash servers retired

Available RAM 884 MiB → **2.5 GiB**, swap 2.0 G → 0.3 G. The 16 dashboards use ZERO
server callbacks (only line/card/bar/column/choropleth pre-computed figures) — the Dash
backend was pure overhead. Shipped `dbr build` static export → self-contained HTML
(Plotly `to_html`, ONE shared `assets/plotly.min.js`, byte-identical layout +
`<meta dbr-build>` stamp). nginx `try_files` static; `dbr run`/`redeploy_dashboards.py`
rebuild+verify file stamps; `run_daily.sh` no longer touches the fleet. 16
`or-<domain>.service` STOPPED.

**KEY OPS MODEL (current):**
- Dashboards = **static files** in `infra/nginx/html/<domain>/index.html` (gitignored build
  artifacts). NO `dbr serve`, NO `or-<domain>.service`, NO ports. Old OOM/fleet-502 recovery
  is obsolete.
- A dashboard change OR a data refresh (dbt) needs a **REBUILD** (not restart) to show:
  `python3 infra/scheduler/redeploy_dashboards.py` (builds 16 → web root, verifies each built
  `<meta dbr-build>` == HEAD; hard-fails on build error). `--verify-only` reads stamps.
- After ANY `packages/dbr/` edit: commit FIRST, then `redeploy_dashboards.py` (stamp target
  is HEAD). Non-zero exit = NOT resolved.
- Live verify: `curl -sk --resolve portal.open-reporting.dev:443:127.0.0.1 https://portal.open-reporting.dev/<domain>/`.
- **ONE PO ACTION (sudo gap):** 16 units stopped but still `enabled` — reboot restarts them
  (benign: 2.5 GiB headroom). PO runs `systemctl disable or-{16}` + `daemon-reload` (sudoers
  gap), then OR-168 closes.

## Pipeline freshness note (still true)
`run_daily.sh` = raw refresh only (no dbt). Curated marts lag raw between manual dbt runs —
fine because all dashboards show annual/quarterly aggregates. To refresh dashboard data:
`dbt run` (DuckDB write lock now FREE — no live readers) then `redeploy_dashboards.py`. No
daily cron dbt (would re-spike memory). NB `run_daily.sh` still logs "ensuring
or-<domain>.service is running…" for the retired fleet — stale/benign, clean up next infra touch.

## Engine-tree state
- Clean except known untracked PO/bot WIP (never commit): `infra/discord-bot/bot.py`,
  `infra/systemd/or-*-bot.service`, `logs/`, `.claude/scheduled_tasks.lock`,
  `products/blog/reviews/release-report.md`, stray `open-reporting-full.tar.gz` (root).
- 16 dashboards = static HTML on stamp == HEAD (f8f64776).
- dbr `value_format` now fully wired (OR-162). Authors can use `options.value_format` on
  card/column/bar/table + table `formats:` + theme `formats:` presets.

## dbr visual notes
- **bar = HORIZONTAL** (metric on x). Vertical categorical → use **column**. Bitten 3×.
- **choropleth** (`packages/dbr/src/dbr/visuals/choropleth.py`): renders via
  `chart_with_optional_table`; do NOT bake `fig.layout.height` on a geo. Warehouse `geo` ==
  GISCO `NUTS_ID`; YAML must filter EU27_2020/EA20.
- Production visual types only: line (65), card (57), bar (8), column (4), choropleth (2).
  No data_labels set in any production YAML; no slicers/cross-filter/tabs/Interval.

## Standing blockers (all PO-side)
- **OR-168** — root-fixed (#64); only `systemctl disable or-{16}` remains (sudo gap).
- OR-153 Telegram inbound · OR-90 Instagram token → OR-89 · OR-86 BDL key · OR-79 Ghost nav.
- On hold under static model: OR-160 cross-filter, OR-161 date-picker (backend-only).

## Lessons
- **Check whether a backlog item is already half-done before building** (#65): OR-162's schema
  was wired but the rendering was a silent no-op. Audit call-sites, not just imports.
- **A "no-op" must be byte-exact** (#65): `format_value(v, None)` returns comma-decimal, but the
  prior bar/column label was dot-decimal — preserve the exact prior path when the option is unset.
- **Measure the WHOLE box before re-diagnosing RAM** (#59/#63): low avail-RAM was often a
  concurrent PO VS Code Remote-SSH session, not the fleet. (Now moot — fleet retired.)
- **Trust a sound engineering call but verify the premise against docs** (#64).
