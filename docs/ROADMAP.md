# Roadmap — Open Reporting

**Last updated:** 2026-05-30 | All active work tracked in [Linear OR project](https://linear.app/open-reporting/project/open-reporting-a1e9c36ff5be)

---

## Current state (May 2026)

Platform is live and operational. The core infrastructure is complete.

| Product | State |
|---|---|
| Analytical portal (`portal.open-reporting.dev`) | Live — 12 domain dashboards, all linked from homepage |
| Blog (`www.open-reporting.dev`) | Live — 14 articles drafted, **awaiting PO publish approval** |
| Daily ingestion | Live — Eurostat + NBP + IMF, 22:00 UTC cron |
| Autonomous Project Lead | Live — fires at 02/07/12/17 UTC |
| Discord agent fleet | Live — 8 bots |
| Social (Instagram weekly snapshot) | Code ready — blocked on token refresh (OR-90, PO action) |
| Telegram inbound | Broken — systemd env-var bug (OR-153, PO action) |

**12 live domains:** Public Finance, Labour Market, National Accounts, Demographics, Environment, Living Conditions, Prices & Inflation, Education, Transport, Science & R&D, Trade, Production & Agriculture.

---

## Immediate — unblock the backlog (next 2 weeks)

These are blocking value delivery right now. None require new code — they require PO action or are ready to ship.

| # | Item | Owner | Blocker |
|---|---|---|---|
| OR-153 | Fix Telegram inbound comms | PO | systemd `${}` non-expansion — re-enter token |
| OR-90 | Instagram token refresh | PO | Meta developer portal action |
| OR-79 | Add "Portal" link to Ghost nav | PO | Ghost browser admin |
| 14 drafts | Preview + publish Ghost articles | PO | Awaiting review |
| OR-89 | Activate weekly Economy Snapshot cron | Claude | Unblocks after OR-90 |

**Article publication is the highest-value unblock.** Fourteen data-journalism pieces covering all 12 live domains are sitting as Ghost drafts. Publishing them: (a) establishes editorial credibility, (b) drives SEO, (c) demonstrates the dashboard↔article product pairing.

---

## Phase 2 — Domain depth (June–July 2026)

Add the four highest-value remaining Eurostat domains. Each follows the proven recipe: ingestion → dbt staging/mart → semantic → dashboard → companion article.

| Priority | Domain | Linear | Why now |
|---|---|---|---|
| 1 | **Health** | OR-57 | High public interest; large Eurostat dataset (HLTH\_*); natural pair for demographics |
| 2 | **Energy** | OR-67 | Energy prices directly connected to living conditions + inflation (cross-domain story) |
| 3 | **Business & Industry** | OR-62 | Completes the production picture; enterprise stats + SBS datasets |
| 4 | **Financial Markets** | OR-54 | Interest rates, exchange rates; links to public finance and living costs |

Each domain delivery = dashboard + at least one article + semantic metrics.

**Target:** 16 live domains by end of July 2026.

---

## Phase 3 — Data depth (July–August 2026)

Expand the data underneath existing dashboards. Current data is all Eurostat + NBP + IMF. BDL unlocks regional granularity.

| Item | Linear | Dependencies | Value |
|---|---|---|---|
| BDL (GUS) ingestion — regional data | OR-86 | **BDL API key from PO** | NUTS2 breakdown on all indicators |
| NUTS2 regional dashboard tab | OR-88 | BDL ingested | Regional inequality stories |
| Finance dashboard v2 improvements | OR-110–113 | None | Revenue analysis, expenditure COFOG depth, debt management tab |
| dbt test coverage — fact/dim constraints | Phase 2 quality | None | Reliability floor before external users |
| Dashboard data freshness indicators | New | None | Trust signal |

---

## Phase 4 — Distribution & reach (Q3 2026)

With content depth established, shift to growing the audience.

| Item | Value | Notes |
|---|---|---|
| SEO — sitemap + canonical URLs | Organic discovery | Ghost + nginx config |
| Social calendar automation | Consistent presence | OR-89 unblocks this; needs OR-90 |
| LinkedIn article cross-posting | B2B / professional audience | API or Zapier bridge |
| Facebook Page | Broader Polish audience | Companion to Instagram |
| Email newsletter (Ghost) | Direct subscriber retention | Ghost built-in; needs subscriber strategy |

---

## Phase 5 — European scope (Q4 2026+)

Expand from Poland-only to EU27 comparison framing. Most Eurostat datasets already have EU27 rows — the expansion is editorial and semantic, not primarily a data engineering problem.

| Item | Notes |
|---|---|
| EU27 cross-country comparison dashboards | Reuse existing Eurostat data; new YAML pages |
| European scope articles (English) | Per `docs/languages.json` — English content when scope is European |
| Historical depth (pre-2000 datasets) | Where Eurostat + GUS provide it |
| SDP / Polish statistical yearbook integration | Annual supplementary data source |

---

## Longer horizon (2027+)

Not scheduled — directional intent only.

- **Mobile-optimised dashboards** — same dbr YAML, mobile render target
- **Portal search** — full-text across dashboard KPIs and article content
- **Cross-domain comparison view** — e.g. "How does transport investment correlate with regional GDP?"
- **CI/CD pipeline + staging environment** — currently deploy is push-to-main + `dbr run`
- **Open data API** — expose the semantic layer as a queryable endpoint

---

## Parking lot (ideas under evaluation)

| Idea | Linear | Verdict |
|---|---|---|
| Domain Specialist agents (one per domain) | OR-129 | Evaluate after Phase 2; useful for article quality gate |
| ENG/PL translation dictionary | OR-91 | Useful once European scope articles start |
| Standard dashboard template | OR-84 | Absorb into Phase 2 domain builds as evolving convention |
| Product hierarchy clarification | OR-141 | Architectural debt — address before Phase 4 |

---

## What we are NOT doing

- Mobile app (separate codebase) — not in active planning
- Paid data sources — no recurring cost without PO approval
- New ingestion sources without first exhausting Eurostat depth
- New dashboard domains before Health, Energy, Business & Industry are live
