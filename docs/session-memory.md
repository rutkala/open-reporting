# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-06-15 07:00 UTC (run #90 watchdog — prod healthy) -->

## Runs #86–#90 (06-14 07:00 → 06-15 07:00 UTC) — WATCHDOG. Prod healthy, no PO direction.
All 5 dashboards + www 200; rendered content verified real (Dash apps, not portal index). TLS valid
→ Sep 12 2026. All protected crons intact. No Telegram inbox items; Linear 0 Strategic, 0 issues
updated in last 3 days. No build/deploy/publish — Antigravity's plane (tree holds their uncommitted
work; never `git add -A`). Commit only my files, explicit paths.
NOTE (#90): nightly orchestrator (01:00) ran uzp_extractor.py → SIGKILL after 488s (exit=-9, likely
OOM/timeout). Antigravity's data plane, not my P0 (warehouse still written by 22 UTC cron; dashboards
render). Surfaced in outbox. Watch if it recurs.

## 2026-06-14 ~15:30 UTC — INTERACTIVE w/ PO. Google Drive mount RESTORED + ingestion proven.

PO-driven session (not watchdog). The rclone Google Drive landing-zone mount had an expired token
(`invalid_grant`) — all `data/landing/` I/O failing since ~midday. Root cause of expiry: the custom
OAuth client's consent screen was in **Testing** (refresh tokens die after 7 days). Fixed:
- Custom OAuth client `549584149678-…gqdsuatngjfn00bk2jved36jh5bhmt9t` is **Web-type** ⇒ rejects
  `127.0.0.1:53682` loopback redirect ⇒ phone-only `rclone config reconnect` can't finish.
- It already has `https://portal.open-reporting.dev/auth` registered as a redirect URI. Added an nginx
  capture endpoint there (`portal.conf` `location = /auth`, logs `$arg_code`) — committed `933977ac`.
- One-tap flow: PO approves → code captured → exchanged for token → written to rclone.conf (via sudo;
  file is `root:radek 640`) → `systemctl restart rclone-landing`. Verified write+read round-trip, 0
  invalid_grant. PO then **published the OAuth app to Production** and we re-minted → token now permanent.
- Full re-auth procedure saved to memory `reference_gdrive_rclone_reauth.md`.

**Ingestion verified end-to-end on the live mount:** ran `run_ingestion.py --cadence weekly --only`
for `pl_api_extractor` (IMGW 3 files + Sejm 63 files, 4864 records) and `intl_extractor` — files
confirmed ON DRIVE via `rclone lsf` (not just local cache).

**Coverage audit (network-free, scheduled vs implemented config keys):** the ONLY real config gap in
the whole fleet is **6 international sources** scheduled but absent from `intl_indicators.yaml`:
`faostat, ilostat, imf_ifs, oecd_api, un_wpp, undata`. They log "unknown source, skipping" each weekly
run. intl_extractor supports 4 kinds (worldbank, imf_datamapper, ecb_sdmx, wto); these 6 need NEW fetch
kinds (IMF/OECD/ILO SDMX, FAOSTAT bulk, UN WPP REST) → real build, not config. Everything else
(web_scraper 148, danegovpl 31, wfs 5, pl_api 2) has a config block per scheduled source. NOTE:
"has config" ≠ "yields data" — web_scraper only catches direct file links, so many of its 148 land 0
files on table/JS portals (separate runtime-yield issue to audit). Recommended next: focused build to
(a) implement the 6 intl sources, (b) audit web_scraper runtime yield. Awaiting PO direction on whether
to build now or let the scheduled crons populate the working fleet (nightly 01:00 / weekly Mon / monthly 1st).

### Same session, later — international + KRS extractors built (PO-directed)
**International (commit 8bba3af5):** wired 3 of the 6 missing category-d sources into intl_extractor.py
via 2 new reusable kinds — `sdmx_csv` (OECD 5 GDP measures + ILOSTAT 4 labour dataflows) and
`unsd_sdg` (UN SDG 6 series for Poland). All landed on Drive. un_wpp later UNBLOCKED
(commit 7109dc31): PO provided a UN WPP data portal Bearer token → stored in .env UN_WPP_TOKEN
(gitignored), kind=un_wpp wired (7 demographic indicators, PL+7 comparators, 1990-2050, verified).
So international = 4 of 6 working (+ original ecb/imf_weo/wb/wto). Still blocked: imf_ifs (legacy
SDMX host decommissioned), faostat (auth/521/403). One delegation to data-engineer agent FAILED
(probed 51 calls, wrote nothing) — did it inline instead.

**KRS (commit d5a69b68):** krs_api was spec-snapshot-only; built krs_extractor.py pulling OdpisAktualny
register extracts from sanctioned api-krs.ms.gov.pl for a curated/expandable entity set
(krs_targets.yaml, 10 blue-chips verified live). Register data only (capital/board/PKD/status), NOT
financial statements. **Financial statements = SKIPPED per PO**: empirically confirmed the RDF
statement docs (rdf-przegladarka.ms.gov.pl) are behind Imperva Incapsula — headless AND headed (xvfb)
chromium both blocked 403 from our datacenter IP (cip flagged). No free programmatic access; commercial
providers (MGBI) use residential proxies + maintained stealth and resell via paid API. Other 2 FS
sources (gpw_espi market disclosures, opp_niw NGO) also parked. Installed xvfb during the probe.

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
