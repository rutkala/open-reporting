# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-02 (run #46 — P0 recovery: 3 dead dashboards restored) -->

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
