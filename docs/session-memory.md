# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-02 (run #47 — responsive mobile layout for all dashboards) -->

## Run #47 — responsive mobile layout (fleet-wide). HEAD abd9d912

**The dbr shell was desktop-only; added a mobile perspective without touching any
dashboard YAML.** Root problems: (1) **no viewport meta** → phones rendered the 980px
desktop canvas zoomed out; (2) the fixed-canvas model (outer `100vh`+`overflow:hidden`,
each section exactly one viewport, horizontal flex rows whose chart heights come from a
definite-height cascade) crushed charts to slivers and clipped the footer on narrow
screens. All inline-style based (Dash), so the only responsive lever is a `<style>`
`@media` block where **CSS `!important` overrides inline styles**.

Engine-plane fix in `packages/dbr/` (3 files), one commit `abd9d912`:
- `make_app.py`: added `meta_tags=[viewport width=device-width]` + a
  `@media (max-width:768px)` block — shell stacks vertically & BODY scrolls; sidebar →
  full-width top bar with wrap-nav; **sections `display:block`** (critical: as flex-column
  the body keeps `flex:1 1 0` basis-0 and collapses to ~0, overflowing/overlapping — block
  flow lets heading+rows stack naturally); rows stack one-visual-per-line full width.
- `page_shell.py`: className hooks on structural divs (`dbr-page-outer`, `dbr-right-col`,
  `dbr-page-section`, `dbr-page-body`, `dbr-row` + `dbr-row-grow`/`dbr-row-fixed`,
  `dbr-visual-item`) so the stylesheet can target them.
- `_render.py`: tag fill-mode charts `dbr-fill-graph`; mobile pins them to **320px**
  (their desktop height comes from the now-broken flex chain). Companion-table and
  baked-height visuals (choropleth/treemap/gauge/etc.) keep their figure height and just
  reflow to full width — untouched.

**Production visual vocabulary is only line/card/bar/column** (grepped all 17) — all
covered (line/bar/column = fill-mode tagged; card = KPI div sizing to text). Verified at
390×844 (iPhone) on education, labour_market (incl. 27-country EU ranking bars + CSV
download) & public_finance (side-by-side rows): no overlap, no h-scroll, readable. Fleet
redeployed + SHA-verified: **all 16 serving `abd9d912`**. Live systemd shot confirmed.

## Run #46 — P0 PRODUCTION RECOVERY. HEAD 02afe50d (no code commit)

**Three dashboards were dead at start — restored.** Smoke check caught `public_finance`
+ `labour_market` 502; fleet sweep also caught `education` 502. All three `or-*.service`
units were **inactive** — cleanly SIGTERM-stopped at **05:59 UTC** and never restarted
(the other 13 survived). Interrupted-redeploy / lock-stop signature, not a code fault.
`sudo systemctl start` the three → after ~15–25s boot all 200 + correct titles. Full
fleet re-swept: **all 16 + www HTTP 200.**

**Subtlety I own:** the tree carries uncommitted `packages/dbr/` WIP — the #41 interactive
layout session has evolved into a **mobile-responsive feature** (`@media (max-width:768px)`
block in make_app.py +130, className hooks in page_shell.py, `.dbr-fill-graph` in
_render.py, `width=device-width` viewport meta). dbr is editable-installed, so my P0
restart booted those **3 services on the uncommitted code; 13 run committed HEAD**. The
change is **provably desktop-noop** (media query only ≤768px; classNames are additive) →
desktop unchanged, which is why the 3 render correctly.

**Verified live (not assumed):** flagship desktop 1600×900 fully intact (sidebar, 4 KPI
cards −7,3/59,7/50,9/2,5 % PKB all 2025, 2 charts filling, footer Dane:2025, stamp
02afe50d=HEAD). Mobile 390×844: the WIP works well — wrapping top-bar nav, full-width
stacked cards, readable type, scrolls. `/tmp/pf_desktop.png`, `/tmp/pf_mobile.png`.

**Held the #41 line:** did NOT commit the WIP (unreviewed engine code — needs
architecture-critic + visual-screenshot-reviewer), did NOT revert it (PO's active work),
did NOT redeploy (would push WIP fleet-wide). Fleet stable: stamp-consistent, desktop-
identical.

## PO question raised this run (outbox)
The uncommitted dbr **mobile-responsive** WIP appears complete + verified-working.
Finalize (commit → dbr review gate → redeploy all 16) or stash? Until decided, no
autonomous run can safely redeploy dashboards (dirty engine tree).

## Lessons
- A subset of services can be left **dead** by an interrupted stop-all/redeploy; the
  daily-ingest "ensure running" only starts *stopped* units on its own schedule (22 UTC),
  so a 05:59 stop stays down until the next ensure or a manual start. **Always fleet-sweep
  all 16 on smoke check, not just the 6 protocol URLs** — education would have been missed.
- dbr-serve boot is slow (~15–25s); a fresh `systemctl start` can still 502 on the first
  curl. Re-poll before concluding failure.
- `build_sha()` reads git HEAD, not the dirty working tree → a service running uncommitted
  code still stamps HEAD. The stamp proves *which commit*, not *that the tree is clean*.

## Recent commits
- 02afe50d docs: run #45 — labour_market EU-27 data + ranking fix (OR-166)
- 05719c6e fix(dashboards): labour_market EU pages — correct ranking + fixed-canvas fill
- ce2dca37 fix(data): widen labour EU-comparison series to ALL_GEOS
- 401b9a35 style(dbr): lighten dashboard canvas background #E4EAF0 -> #EDF1F6
- 0a19fbdf docs: run #44 — no internal scroll + public_finance fill-restructure

## What's next
- **PO decision on the mobile WIP** (above) gates all dbr redeploys.
- **OR-165** (open): fleet-wide `footer_updated` auto-derive — engine-plane, blocked by the
  dirty tree until the mobile WIP is resolved.
- Phase-3 data depth (OR-86, BDL) blocked on PO `BDL_API_KEY`.

## Standing blockers (all PO-side)
- OR-153 Telegram inbound · OR-90 Instagram token → OR-89 · OR-86 BDL key · OR-79 Ghost nav
- Known untracked PO/bot WIP in tree (do not commit): `infra/discord-bot/bot.py`,
  `infra/systemd/or-*-bot.service`, `logs/`, `.claude/scheduled_tasks.lock`, and the
  uncommitted `packages/dbr/` mobile WIP (page_shell.py, make_app.py, _render.py).
