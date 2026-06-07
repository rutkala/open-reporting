# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-07 (run #73 — escalated Antigravity-pivot decision to Linear OR-172; Telegram channel is dead) -->

## Run #73 — Escalated the contested direction to Linear (OR-172) because Telegram is dead

QUIET RUN, blocked on PO direction. Production healthy (5 dashboards + www = 200; ingest
2026-06-06 exit=0, 98,091 obs, 56 datasets → 2026-S1). Inbox empty; no Strategic/In Progress/Todo.

**Key realisation:** run #72 flagged the "Antigravity V2" conflict only in the Telegram outbox —
but that channel is **dead**. Commit `00e7b85e` (authored `rutkala`, 2026-06-06 18:16Z) deleted
`infra/telegram-bot/bot.py` + `infra/discord-bot/bot.py` + all 8 `or-discord-*-bot.service` units
(946 deletions); `or-telegram-bot.service` inactive; no bot unit files remain. **#72's report never
reached the PO.** The PO reads Linear → that is now the ONLY working PO channel.

**Action:** created **OR-172** (Urgent/Infra, assigned to PO) — durable single anchor for the
decision: **A Sanction / B Revert / C Coexist** the Antigravity pivot. Full evidence inside (commit,
canceled OR-153, ROADMAP author "Antigravity Project Lead", untracked artifacts). Future runs point
at OR-172 instead of re-flagging into a void. Left all Antigravity artifacts UNTOUCHED.

Release sweep: no-op, no spawn (20/20 published, no drafts). Data-quality spot check clean
(21 fact tables populated). 0 subagent spawns, 0 code changes, 1 Linear issue, 1 post-mortem commit.

## THE GATING DECISION (OR-172) — read FIRST next run
A foreign "Antigravity" workstream (commits under PO git identity `rutkala`) is mutating this repo:
removed the Discord+Telegram bot fleet, canceled OR-153, rewrote `docs/ROADMAP.md` to "Open
Reporting V2 — AI-Native Media Company" (Author: Antigravity Project Lead), added untracked
`infra/nginx/html/team.html` + `infra/scheduler/team_workspace_feed.py`. **This contradicts
CLAUDE.md** (8-bot Discord fleet + Telegram comms). I cannot adjudicate — PO strategy call.
**Until OR-172 is answered: keep production healthy, do non-conflicting maintenance only, do NOT
build on either the old or the new ROADMAP, do NOT touch the Antigravity artifacts.**
If a future run sees a PO answer on OR-172: A → draft CLAUDE.md/charter+ROADMAP updates for approval;
B → `git revert 00e7b85e`, restore fleet, `git checkout docs/ROADMAP.md`, clean untracked artifacts;
C → implement the boundary split the PO specifies.

## COMMS MODEL (current reality)
- Telegram inbox/outbox is DEAD both ways (bot removed). Step-4 outbox files are still written per
  protocol but are NOT delivered. **Linear is the only channel that reaches the PO.** Surface
  everything that needs PO eyes as a Linear issue (Urgent + assigned to r.utkala@gmail.com).

## KEY OPS MODEL (current)
- Dashboards = **static HTML** in `infra/nginx/html/<domain>/index.html` (gitignored build artifacts).
  NO `dbr serve`, NO `or-<domain>.service` running, NO ports. 16 units inactive+disabled.
- YAML/data change → single: `dbr run products/dashboards/<domain>`; fleet / any `packages/dbr/`
  edit → commit FIRST, then `python3 infra/scheduler/redeploy_dashboards.py` (builds 16 → web root,
  verifies `<meta dbr-build>` == HEAD; non-zero exit = NOT resolved).
- Live verify: `curl -s .../<domain>/` → 200 + stamp + Plotly. Layout/visual → Playwright screenshot.
- **Page = fixed single-screen canvas `overflow:hidden`.** Don't stack full-height rows (clips).
- **Current dbr HEAD stamp: `19f6a4b2`** (#72 design refresh). All 16 on it.

## dbr design system (post-#72, OR-171)
- Theme tokens exposed as `:root` CSS custom properties via `get_css_vars()` in make_app.py; both
  static (`build.py`) and live Dash paths inject them. Edit colours/spacing in `theme.yaml` → rebuild.
- Palette: Slate/Tailwind (teal `#3B8B94`, azure `#3A6FA4`, canvas `#F8FAFC`, text `#1E293B`).
  16px radius, soft shadow, 24/32px spacing, glassmorphism (backdrop-blur) + hover-lift.

## dbr visual notes
- **bar = HORIZONTAL** (metric on x). Vertical categorical → use **column**. Bitten 3×.
- choropleth: warehouse `geo` == GISCO `NUTS_ID`; filter EU27_2020/EA20; don't bake height.
- Production visual types only: line, card, bar, column, choropleth.
- `value_format` fully wired (#65). Below-the-fold charts auto-resize on load (#67 `_RESIZE_JS`).

## public_finance dashboard pages
przeglad → dochody → wydatki → dlug → ue → prognozy.

## Content release (run EVERY run — Step 2b)
- `python3 products/blog/release_pipeline.py` → reviews unreviewed drafts through 3 reviewers,
  auto-publishes those with NO BLOCK. **20 articles published.** Sweep clean unless a new draft exists.
  Check cheaply first (drafts in `products/blog/*.md` vs `release-report.md`) before spawning.

## Engine-tree state (CAUTION — dirty with foreign Antigravity WIP, do NOT commit blindly)
- Untracked/modified foreign WIP NOT mine to commit: `docs/ROADMAP.md` (Antigravity rewrite),
  `infra/nginx/html/team.html`, `infra/scheduler/team_workspace_feed.py`, `ORIGINAL_REQUEST.md`,
  `PROJECT.md`, `fix_and_test.py`, `lin_finish.py`, `lin_reset.py`, `verify_mobile_layout.py`,
  `build_temp/`, `logs/`, `products/blog/reviews/release-report.md`, `.claude/scheduled_tasks.lock`.
  Fate decided by OR-172 (revert vs keep). Until then: leave untouched.

## Standing blockers (PO-side)
- **OR-172 Antigravity-pivot direction (Urgent — the gating decision).**
- OR-90 Instagram token · OR-86 BDL key · OR-79 Ghost nav.
- On hold under static model: OR-160 cross-filter, OR-161 date-picker (backend-only interactivity).
- OR-153 Telegram = Canceled by the Antigravity workstream; folded into OR-172.

## Followup (minor, deferred)
- CLAUDE.md Development Commands shows a stale DuckDB snippet (`from dbr.semantic import query`)
  — use `duckdb.connect(read_only=True)`. eurostat cols: dataset_code, geo, period, dimension_key,
  value, obs_status, fetched_at (period, NOT time_period). Too trivial to warrant a flagged edit alone.
- 16 leftover `or-<domain>.service` unit files on disk (disabled, zero risk) — `rm` needs sudo.
