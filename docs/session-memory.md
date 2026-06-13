# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-13 (run #83 — WATCHDOG; coexist; Antigravity is the active lead) -->

## Run #83 — 2026-06-13 12:00 UTC. WATCHDOG. Prod healthy. Antigravity (Gemini swarm) owns everything.

Production verified: 6/6 dashboards 200 + public_finance renders real content (stamp `7e9e0496`,
`<title>Finanse publiczne Polski</title>`); www 200. No new PO direction (inbox empty, 0 Strategic
issues, no Linear instruction to the Claude cron; latest Linear activity unchanged at 06-09 — OR-192
bulk-mirroring In Progress — nothing in last 4 days). `warehouse.duckdb` written 06-13 08:24 =
ingestion ran normally. Live stamp `7e9e0496` trails HEAD `44e1b844` by design (Antigravity in-flight
work). No build, no redeploy, no publish, 0 spawns, 0 Linear writes, 1 post-mortem commit. Committed
only my 3 files (explicit paths).

## THE NEW REALITY (read FIRST next run) — Antigravity is the active Project Lead
The project reorganised around an **Antigravity (Gemini) Discord swarm** as Project Lead. OR-191 (Urgent,
Done) shows the PO building a Slack/Discord-style studio + live status + parallel autonomous Antigravity
worker sessions, all via the "[AI Project Lead]" Antigravity orchestrator. The whole data plane pivoted:
OR-183→192 (parallel GitHub-Actions ingestion, real extractors, **unbounded bulk mirroring** OR-192 In
Progress, Parquet offloader OR-188, deep catalog OR-189, GraphQL B2B API OR-181, dynamic footers OR-190).
Content moved to Antigravity too: OR-175 Ghost Bridge + OR-177 Newsroom Controller → `ghost_publisher.py`.

## OR-176 IS CLOSED → COEXIST BY DEFAULT (the gating decision is over)
OR-176 was marked **Done** (2026-06-08 11:34 UTC), no comment, cron NOT removed, no plane-split given.
Read: coexistence. I self-impose the watchdog boundary I offered in OR-176 — **production-health only**.
Do NOT re-open or re-ping (OR-191 explicitly rebukes approval-friction/noise). Long-term the PO should
retire this legacy `autonomous-lead.sh` cron; already flagged + closed; re-flagging = noise.

## MY POSTURE EVERY RUN NOW (until/unless PO directs otherwise)
1. Smoke-check prod (6 dashboards + www + admin pages). Fix only TRUE P0s that are MINE (not Antigravity's
   in-flight work). Antigravity owns ingestion/dashboards/content/`packages/dbr/`/admin — all of it.
2. Do NOT build on any roadmap, do NOT redeploy (`redeploy_dashboards.py`/`dbr run`), do NOT publish.
   Any of these would render/commit Antigravity's UNCOMMITTED in-flight work → destroys their progress.
3. Do NOT run `release_pipeline.py` — publishing is irreversible AND content is Antigravity's plane.
4. Commit ONLY my own 3 files (decisions.md, session-memory.md, outbox) with EXPLICIT paths. NEVER
   `git add -A` — the tree is full of untracked Antigravity V2 deliverables (data-loss risk).
5. Telegram dead → Linear is the only live PO channel. Write the outbox per protocol (undelivered).

## WHY THE LIVE STAMP TRAILS HEAD (do not "fix" it)
Live `<meta dbr-build>` = `7e9e0496`; repo HEAD = `c0c995bf`. The gap is Antigravity's committed +
uncommitted dashboard/`packages/dbr/` work. Redeploying would push its half-finished YAML (untracked
currency_composition/fixed_floating/maturity_profile/tax_buoyancy/tax_mix/expenditure_type.yml +
modified public_finance visuals) live. Leaving it stale is CORRECT non-interference.

## NEW INGESTION = AS DESIGNED (not a P0)
`warehouse.duckdb` last written 06-09 06:21. Daily `bdl-bulk`/`dbw-bulk` logs show HTTP 404 on missing
subjects + 429 "Budget stop — manifest saved, resume next run" = the designed resumable/rate-limited
behavior of the unbounded-mirroring pivot (OR-192). Old `ingest-daily-*.log` stops 06-07 — superseded by
OR-186 nightly GitHub-Actions pipeline. The Step-0 "yesterday ingest log" check is now stale; ignore.

## When a future run sees an explicit PO instruction TO me (the Claude cron)
Only then leave watchdog mode. If PO says retire → idle (can't remove own cron, hard floor). If PO names
a plane split → operate strictly inside it. Absent that, stay watchdog: verify prod, document, no build.

## KEY OPS MODEL (static architecture, for reference only — do not trigger while watchdog)
- Dashboards = static HTML in `infra/nginx/html/<domain>/index.html`. No `dbr serve`, no per-domain
  service/port. YAML/data change → `dbr run`; fleet/`packages/dbr/` → commit FIRST then
  `redeploy_dashboards.py` (verifies `<meta dbr-build>`==HEAD). Semantic API:
  `from dbr.semantic import semantic_query, semantic_query_data` (CLAUDE.md snippet is stale).
- Crons live (hard floor, do NOT disable): `0 22 * * *` ingestion · `0 2,7,12,17 * * *` autonomous-lead
  (me). Note: an OR-186 nightly GitHub-Actions ingestion also runs in the cloud now.
