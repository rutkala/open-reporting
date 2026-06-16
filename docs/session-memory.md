# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-16 07:23 UTC (run #94 — SHIPPED uzp disk-full fix + filed OR-195) -->

## Run #94 (06-16 07:23 UTC) — SHIPPED. Root-caused + fixed the recurring uzp disk-full.
All 5 dashboards + www 200; daily 22 UTC ingest exit=0. No Telegram inbox; Linear 0 Strategic, 0
issues in 5d. Release sweep ran = no-op (20 already published, 1 blocked, 0 new drafts → nothing
pushed). FIXED uzp disk-full that #90–93 deferred: the errno 28 was the per-month notices STREAM, not
the output. `data/landing` is on the Drive mount (st_dev 39, ~5TB) but the stream went to
`tempfile.TemporaryDirectory()` defaulting to /tmp on the 38G root (st_dev 2049) — one full-scope
ContractNotice month exhausted root → OSError 28 at uzp_extractor.py:122. NOT full-history (orchestr
runs uzp "single"/no-args = default last-3-months). Fix (commit 2b2f7178, pushed): temp dir now under
LANDING (Drive) + 2 GiB free-space preflight as mount-down fallback. Verified temp at st_dev 39 not
/tmp; real fetch exits 0, no orphan. uzp_extractor was clean/committed (not in Antigravity's tree) so
editing stepped on nothing — explicit-path commit only.
NEW: BZP API enum drift — only `ContractNotice` returns 200; `ContractAwardNotice` +
`ContractModificationNotice` → HTTP 400 (out-of-range). 2 of 3 types silently empty since enum
changed; completeness overstated. Filed OR-195 (Bug/Data, Medium, Backlog) — did NOT guess enum
values (API-burn). Tonight's 01:00 nightly is the live test of the disk fix.

## Runs #86–#93 (06-14 → 06-16 07:00) — WATCHDOG. Prod healthy, no PO direction.
All dashboards + www 200, content real, TLS → Sep 12 2026, crons intact. No build/deploy/publish —
Antigravity's plane (tree holds uncommitted work; never `git add -A`; commit only my files, explicit
paths). #90–93 saw the uzp failure as transient/their-plane; #94 root-caused & fixed it (above).

## 2026-06-14 — INTERACTIVE w/ PO (condensed history)
- **Drive mount restored:** rclone token had expired (consent screen was in Testing). One-tap re-auth
  via nginx `/auth` capture endpoint (commit 933977ac); PO then published OAuth app to Production →
  token permanent. Procedure in memory `reference_gdrive_rclone_reauth.md`. `data/landing` is the
  Drive mount (~5TB) — relevant to #94's uzp fix.
- **Intl extractors (8bba3af5, 7109dc31):** 4 of 6 category-d sources now working via new kinds
  `sdmx_csv` (OECD/ILOSTAT), `unsd_sdg` (UN SDG), `un_wpp` (Bearer token in .env UN_WPP_TOKEN). Still
  blocked: imf_ifs (host decommissioned), faostat (403).
- **KRS (d5a69b68):** krs_extractor.py pulls OdpisAktualny register extracts (api-krs.ms.gov.pl,
  krs_targets.yaml). Financial statements SKIPPED per PO — RDF docs behind Imperva Incapsula (403 from
  datacenter IP). gpw_espi + opp_niw also parked.
- **TLS (Run #85):** cert lineage `open-reporting.dev-0003` valid → 2026-09-12; renewal host cron
  `20 3,15` certbot. Standing followups to PO: compose `certbot` service has wrong volume paths
  (dead); add cert-expiry alert.

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
