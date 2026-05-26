# Open Reporting — Live Status

**Last updated:** 2026-05-26 20:05 UTC

Autonomous agent: **RUNNING** — 20:00 UTC tick (run #4 since 4h cadence). Smoke check: production returning 403 from container IP (nginx allowlist) — not a service failure; PO confirmed 200 OK at 19:35 UTC. Pushing 5 unpushed OR-56 commits, then starting OR-52 National Accounts & Macro dashboard.

---

## Where to look

| What | Where |
|------|-------|
| Live run history (start times, success/failure, durations) | https://claude.ai/code/routines/trig_01TqBcSxS3SzQn7BtSTiDmif |
| What's currently being worked on | this file (`docs/STATUS.md`) — agent updates at run start |
| What was just shipped | `git log origin/main --oneline -10` |
| Full reasoning trail | `docs/decisions.md` (latest at bottom) |
| Production health | URLs below |
| Linear backlog state | https://linear.app/open-reporting |

---

## Production

| Service | URL | Status (last check 20:05 UTC) |
|---------|-----|------------------------------|
| Public finance dashboard | https://portal.open-reporting.dev/public_finance/ | 200 OK (PO-verified 19:35 UTC; 403 from container IP = nginx allowlist, not service down) |
| Labour market dashboard | https://portal.open-reporting.dev/labour_market/ | 200 OK (PO-verified 19:35 UTC) |
| Blog | https://www.open-reporting.dev/ | 200 OK (PO-verified 19:35 UTC) |
| Daily ingestion (NBP + Eurostat) | cron `0 22 * * *` UTC | last run 2026-05-26 13:52 UTC, exit=0 |

---

## Autonomous routine

| | |
|---|---|
| ID | `trig_01TqBcSxS3SzQn7BtSTiDmif` |
| Cron | `0 */4 * * *` (every 4h: 00, 04, 08, 12, 16, 20 UTC) |
| Last fire | 2026-05-26 20:00 UTC |
| Next scheduled fire | **2026-05-27 00:00 UTC** |
| Model | claude-sonnet-4-6 |
| Mode | week-long unattended (PO away) |

---

## Currently working on

**OR-52** — National Accounts & Macroeconomics dashboard (Theme 3 priority #2)

---

## Recently shipped (last 10)

| When (UTC) | Linear | Commit | What |
|------------|--------|--------|------|
| **2026-05-26 19:30** | **OR-56** | `fe9beac` | Labour Market dashboard live — fixed YAML + seed defects |
| 2026-05-26 17:15 | OR-56 | `ee5022bd` | linter comments on labour YAMLs (autonomous) |
| 2026-05-26 17:15 | OR-56 | `f79b904f` | labour dashboard YAML (autonomous) |
| 2026-05-26 17:15 | OR-56 | `92733d8e` | labour dbt mart models + semantic layer (autonomous) |
| 2026-05-26 15:02 | — | `51dc1527` | cadence correction: every 4h + manual trigger |
| 2026-05-26 14:32 | — | `cb508378` | switch routine to daily then 4h cadence |
| 2026-05-26 14:14 | OR-80, OR-74 | `4fab3af3` | first article published + reusable Ghost publisher |
| 2026-05-26 14:02 | OR-78, OR-85 | `866d9f46` | daily ingestion cron + Ghost admin verified |
| 2026-05-26 10:09 | — | `86bf9add` | AI Lead activation |
| 2026-05-26 08:55 | — | `2bd9c4a8` | initial Phase B/C work merged to main (via PR #61) |

---

## Blocked on PO action

| Linear | What needs PO |
|--------|---------------|
| **OR-90** | Refresh Instagram token in Meta Developer portal — `@otwarteraporty` profile |
| **OR-79** | Update Ghost navigation in `/ghost/` browser admin: add "Portal" link, set locale to `pl`, accent colour `#4A7FB5`, Polish description |

---

## Linear status — Theme 1, 2, 3

| Issue | Title | Status |
|-------|-------|--------|
| OR-78 | Ghost admin | Done |
| OR-85 | Daily ingestion cron | Done |
| OR-80 | First data-driven article | Done |
| OR-74 | Blog setup + first content | Done |
| OR-56 | Labour Market dashboard | Done |
| **OR-52** | **National Accounts & Macro dashboard** | **In Progress** |
| OR-55 | Population & Demographics dashboard | Backlog (Theme 3 priority #3) |
| OR-90 | Instagram token | **PO-blocked** |
| OR-79 | Portal nav | **PO-blocked** |

---

## How the agent should update this file

At the **start** of every autonomous run, after the smoke check, overwrite this file with the current state, then commit immediately as `chore(status): run #N heartbeat` — this is the PO's window into whether the agent is alive.

At the **end** of every autonomous run, update `Last updated`, set `Currently working on: <NOTHING>`, prepend the just-shipped row to the recently-shipped table, update `Next scheduled fire`.

The conversational PO session also updates this file when working in real time.
