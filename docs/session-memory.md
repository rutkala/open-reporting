# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-14 (run #87 — watchdog, prod healthy, no PO direction) -->

## Run #87 — 2026-06-14 12:00 UTC. WATCHDOG. Prod healthy, no PO direction.

All 5 dashboards + www return 200. TLS valid through **Sep 12 2026** (lineage `open-reporting.dev-0003`,
fixed in #85). All protected crons intact. No Telegram inbox items. Linear: 0 Strategic, 0 issues
touched in last 5 days. Took no build/deploy/publish action — Antigravity's plane. Committed only my
files. Identical posture to #86.

### Run #85 carryover — TLS cert P0 fix (still the live setup)
Expired LE cert (Jun 13 19:27 UTC) reissued → lineage `open-reporting.dev-0003`, valid through
**2026-09-12**. 3 nginx confs (portal/apex/www) point at `live/open-reporting.dev-0003/`.
Renewal wired as host cron `20 3,15 * * *` `certbot -q renew --config-dir infra/nginx/certs`
+ nginx-reload deploy-hook (`renew --dry-run` exit 0). Certs gitignored; only nginx confs committed.
Open followups to PO (still standing): (1) compose `certbot` service has wrong volume paths
(`./nginx/certs` vs `./infra/nginx/certs`), dead/superseded — remove or fix; (2) renewal depends
on my host cron — reconcile if compose-certbot is meant canonical; (3) add cert-expiry alert.

## THE STANDING REALITY — Antigravity (Gemini swarm) is the active Project Lead
Project reorganised around an Antigravity Discord swarm as Project Lead (OR-191 Done). Data plane
pivoted: OR-183→192 (parallel GH-Actions ingestion, real extractors, unbounded bulk mirroring OR-192
In Progress, Parquet offloader OR-188, deep catalog OR-189, GraphQL API OR-181, dynamic footers OR-190).
Content moved to Antigravity too (OR-175 Ghost Bridge + OR-177 Newsroom → `ghost_publisher.py`).

## OR-176 CLOSED → COEXIST. My posture = production-health watchdog only.
OR-176 marked Done 2026-06-08, cron NOT removed, no plane-split → coexistence. I self-impose the
production-health boundary. P0 production breakage (like this run's expired cert) IS mine to fix —
TLS/nginx/infra health, not Antigravity's feature work. Do NOT re-open/re-ping OR-176 (= noise).

## MY POSTURE EVERY RUN (until/unless PO directs otherwise)
1. Smoke-check prod (6 dashboards + www + admin). Fix only TRUE P0s that are MINE (infra/TLS/nginx/
   service-down) — NOT Antigravity's in-flight ingestion/dashboard/content/`packages/dbr/` work.
2. Do NOT build roadmap, do NOT redeploy (`redeploy_dashboards.py`/`dbr run`), do NOT publish —
   these would render/commit Antigravity's UNCOMMITTED in-flight work and destroy their progress.
3. Do NOT run `release_pipeline.py` — publishing is irreversible AND content is Antigravity's plane.
4. Commit ONLY my own files (decisions.md, session-memory.md, outbox, and any P0 infra fix I make)
   with EXPLICIT paths. NEVER `git add -A` — tree is full of untracked Antigravity V2 deliverables.
5. Telegram likely dead → Linear is the live PO channel; still write the outbox per protocol.

## WHY THE LIVE DASHBOARD STAMP TRAILS HEAD (do not "fix")
Live `<meta dbr-build>` = `7e9e0496`; HEAD is ahead. The gap is Antigravity's committed + uncommitted
dashboard/`packages/dbr/` work (untracked currency_composition/fixed_floating/maturity_profile/
tax_buoyancy/tax_mix/expenditure_type.yml + modified public_finance visuals). Redeploying would push
its half-finished YAML live. Leaving it stale is CORRECT non-interference.

## INGESTION = AS DESIGNED (not a P0)
`warehouse.duckdb` written daily by 22 UTC cron. `bdl-bulk`/`dbw-bulk` HTTP 404 on missing subjects +
429 "Budget stop — manifest saved, resume next run" = designed resumable/rate-limited mirroring (OR-192).
Old `ingest-daily-*.log` superseded by OR-186 nightly GH-Actions pipeline; Step-0 yesterday-log check
is stale — ignore.

## When a future run sees an explicit PO instruction TO the Claude cron
Only then leave watchdog mode. PO says retire → idle (can't remove own cron, hard floor). PO names a
plane split → operate strictly inside it. Absent that, stay watchdog: verify prod, fix MY P0s, document.

## KEY OPS MODEL (reference — do not trigger while watchdog)
- Dashboards = static HTML in `infra/nginx/html/<domain>/index.html`. YAML/data change → `dbr run`;
  fleet/`packages/dbr/` → commit FIRST then `redeploy_dashboards.py` (verifies `<meta dbr-build>`==HEAD).
  Semantic API: `from dbr.semantic import semantic_query, semantic_query_data`.
- TLS: certs in `infra/nginx/certs/` (gitignored), lineage `open-reporting.dev-0003`, nginx confs point
  there. Renewal = host cron `20 3,15` certbot renew --config-dir infra/nginx/certs + nginx reload hook.
- Crons live (hard floor, do NOT disable): `0 22` ingestion · `0 2,7,12,17` autonomous-lead (me) ·
  `20 3,15` certbot-renew (new). OR-186 nightly GH-Actions ingestion also runs in the cloud.
