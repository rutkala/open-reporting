# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-14 (run #85 — P0: expired TLS cert fixed, HTTPS restored, renewal wired) -->

## Run #85 — 2026-06-14 02:00 UTC. [P0 FIXED] Expired TLS cert → HTTPS restored.

Smoke check returned 000 on all 6 hosts. Root cause: LE cert (`live/open-reporting.dev`,
SANs apex+www+portal) **expired Jun 13 19:27 UTC**. Fixed end-to-end:
- Reissued via webroot → new lineage `open-reporting.dev-0003`, valid through **2026-09-12**.
- Repointed 3 nginx confs (portal/apex/www) to `live/open-reporting.dev-0003/` (stable across renewals).
- Removed broken renewal configs (empty 0-byte + -0001/-0002 with no live dir); only `-0003.conf` left.
- **Wired renewal:** host cron `20 3,15 * * *` `certbot -q renew --config-dir infra/nginx/certs`
  with `--deploy-hook` nginx reload. `renew --dry-run` exit 0. Protected crons preserved (append-only).
- Verified: apex+www+portal + 5 dashboards 200 over HTTPS (full chain validation); public_finance
  renders real content, stamp `7e9e0496` (Antigravity in-flight, untouched). Commit `7605a4bc`, pushed.

### Why renewal had silently failed (so it doesn't recur surprise)
Host `certbot.timer` renews from default `/etc/letsencrypt` (empty); real certs live in
`infra/nginx/certs/`. That lineage's renewal conf was a 0-byte empty file. The compose `certbot`
service points at non-existent `./nginx/certs` paths and never ran. My new host cron is the live
renewal path now. **Certs are gitignored** — only the 3 nginx confs were committed.

### Followups flagged to PO (outbox + decisions #85)
1. compose `certbot` service has wrong volume paths (`./nginx/certs` vs `./infra/nginx/certs`) — dead, superseded by host cron; remove or fix to avoid confusion.
2. Renewal now depends on the host cron I added; reconcile if compose-certbot is meant to be canonical.
3. Add cert-expiry monitoring/alert so a future lapse pages BEFORE the cert dies.

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
