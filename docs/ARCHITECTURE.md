# Architecture

Open Reporting is a one-person data media company turning Polish public data into dashboards, articles, and research. This document is the **single source of truth** for how the repo is organised, where work lives, and which AI models are allowed to touch which parts.

If anything in this document conflicts with code or other docs, **this document wins** — open a PR to update it.

---

## The two-plane model

Everything in the repo belongs to exactly one of two planes.

| Plane | Path prefixes | What lives here | Who edits it |
|---|---|---|---|
| 🟢 **Declarative** | `products/`, `docs/`, `team/` | YAML, SQL, dbt models, semantic definitions, dashboard specs, knowledge base | Radek + cheap AI (Sonnet, Haiku) |
| 🔴 **Engine** | `packages/`, `infra/`, `.claude/` | Python frameworks, nginx config, systemd units, AI agent + hook config | Expert AI (Opus) only |
| 🔵 **Runtime** | `data/` (gitignored) | DuckDB warehouse, landing files | Pipelines write; nothing else |

**Rule:** to add or change an analytical output (dashboard page, dbt model, KPI, ingestion config), you should only need to touch the declarative plane. If a change forces you into the engine plane, that's a signal that the framework's YAML-facing API is missing something — escalate to expert AI, don't reach across the boundary.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         🟢 DECLARATIVE PLANE                              │
│                  (Radek + Sonnet / Haiku work here)                       │
│                                                                            │
│  products/                                                                 │
│  ├── ingestion/         Python fetchers + dlt pipelines (per source)      │
│  ├── warehouse/         dbt project — models, tests, semantic layer       │
│  │   ├── dbt_project.yml                                                  │
│  │   ├── profiles.yml                                                     │
│  │   └── models/                                                          │
│  │       ├── staging/   raw.* → curated.stg_*  (one folder per source)    │
│  │       ├── intermediate/  consolidations, business-key resolution       │
│  │       ├── marts/<domain>/  star-schema facts                           │
│  │       ├── dim/       shared dimension tables                           │
│  │       └── semantic/  MetricFlow semantic_models + metric YAMLs         │
│  │                                                                         │
│  ├── database/          PostgreSQL operational schema (catalogue + ops)   │
│  │                                                                         │
│  ├── dashboards/        dbr YAML — one folder per dashboard               │
│  │   └── <domain>/                                                        │
│  │       ├── dashboard.yml                                                │
│  │       ├── app.py     (8-line bootstrap, never edit)                    │
│  │       └── pages/<page>/visuals/<visual>.yml                            │
│  │                                                                         │
│  ├── blog/  social/  research/  domain-briefs/                            │
│                                                                            │
│  docs/                  Architecture, contributing, data model            │
│  team/                  Knowledge base, standards, agent memory           │
│                                                                            │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│                            🔴 ENGINE PLANE                                │
│                       (Opus only; rare edits)                             │
│                                                                            │
│  packages/                                                                 │
│  ├── dbr/               Dashboard framework — Dash + Plotly + MetricFlow  │
│  └── screenshot/        Dashboard screenshot CLI                          │
│                                                                            │
│  infra/                                                                    │
│  ├── nginx/             Reverse proxy config + certs + static web root    │
│  └── systemd/           Service units (hand-written + dbr-generated)      │
│                                                                            │
│  .claude/               AI agent + hook + skill config                    │
│                                                                            │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│                       🔵 RUNTIME (gitignored)                             │
│                                                                            │
│  data/                                                                     │
│  ├── warehouse.duckdb   Analytical store — all dashboards query this      │
│  └── landing/           Raw files staged from external sources            │
│                                                                            │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Data flow

End-to-end pipeline from external source to rendered visual:

```
External source (Eurostat API, GUS DBW, IMF WEO, NBP, ...)
    │
    │   products/ingestion/to_landing/<source>.py
    ↓
data/landing/<source>/                                 — gitignored
    │
    │   products/ingestion/to_raw/<source>.py  (dlt pipeline)
    ↓
warehouse.duckdb : raw.<source>_<entity>               — raw schema
    │
    │   products/warehouse/  (dbt run)
    ↓
warehouse.duckdb : curated.{stg_*, int_*, fact_*, dim_*}
    │
    │   products/warehouse/models/semantic/*.yml       — MetricFlow defs
    ↓
MetricFlow semantic layer                              — process boundary
    │
    │   packages/dbr/.../semantic.py  (in-process engine)
    ↓
dbr visual factories (line, column, bar, card, ...)
    │
    │   products/dashboards/<domain>/pages/<page>/visuals/<v>.yml
    ↓
Dash app rendered as HTML + Plotly JSON
    │
    │   nginx reverse proxy
    ↓
https://portal.open-reporting.dev/<domain>/
```

**Rule:** dashboards and visuals query MetricFlow only — never `curated.*` directly, never `raw.*` ever. Direct SQL access skips the semantic layer's business logic.

---

## Storage

Two databases, two roles:

| Database | Path | Schema | Role |
|---|---|---|---|
| **DuckDB analytical warehouse** | `data/warehouse.duckdb` | `raw.*`, `curated.*` | All dashboards, all analysis. Opened **read-only** by dashboards via the `dashboard` dbt target. |
| **PostgreSQL operational DB** | `localhost:5432` (Docker) | Ghost CMS, catalogue.* | Blog CMS + operational metadata (sources/domains registry). Not queried by dashboards. |

**Why two databases:** DuckDB is the right shape for analytical queries (column store, fast scans, no concurrent writers needed). PostgreSQL handles Ghost's transactional needs and a small catalogue that classifies sources and domains.

**DuckDB concurrency model:**
- `dbt run` writes the warehouse — uses the `dev` profile target (read-write).
- Every dashboard reads the warehouse — uses the `dashboard` profile target (`config_options.access_mode: READ_ONLY`). Many concurrent dashboards can hold open MetricFlow engines this way; only one writer at a time.

---

## Layer-by-layer

### 1. Ingestion (`products/ingestion/`)

Two phases per source:

| Phase | Folder | Job |
|---|---|---|
| **to_landing** | `products/ingestion/to_landing/<source>.py` | Fetch from external API / portal, save raw file(s) to `data/landing/<source>/` |
| **to_raw** | `products/ingestion/to_raw/<source>.py` | dlt pipeline that reads landed files and writes typed rows into `raw.<source>_<entity>` |

**Why Python is acceptable here:** each new external source has unique extraction quirks (auth, pagination, file formats, rate limits). This is the one place where "first contact with a messy source" justifies engineer-tier code. Once a source is wired, the YAML→pipeline path becomes more uniform; future work may migrate config to declarative YAML templates.

### 2. Warehouse (`products/warehouse/`)

The dbt project. Standard dbt convention for `models/`:

| Folder | Layer | Examples | Materialisation |
|---|---|---|---|
| `staging/<source>/` | One model per raw source table; light typing + renames | `stg_eurostat_observations.sql` | view |
| `intermediate/` | Business-key resolution, joins across sources | `int_finance_consolidated.sql` | view/table |
| `marts/<domain>/` | Star-schema facts ready for the semantic layer | `fact_finance_overview.sql` | table |
| `dim/` | Shared dimension tables | `dim_geo.sql`, `dim_calendar.sql`, `dim_cofog.sql` | table |
| `semantic/` | MetricFlow `semantic_models:` + `metrics:` YAMLs | `finance_overview.yml` | n/a (definitions) |

**Why standard dbt layout** (and not by-domain): any AI model recognises `staging/intermediate/marts/` immediately. Each dashboard's data is also a layer cake — domain-grouping forces facts and stagings to live next to unrelated source files.

### 3. Semantic layer (`products/warehouse/models/semantic/`)

MetricFlow YAMLs define **measures** (raw aggregations on a fact) and **metrics** (named, formatted business KPIs). Dashboards reference metrics by name only.

| Concept | Where | Example |
|---|---|---|
| `semantic_models:` | `products/warehouse/models/semantic/<name>.yml` | One semantic model per fact table |
| `metrics:` | Same file | `fiscal_balance`, `cofog_expenditure`, etc. |
| Polish labels & formatting | `metrics.config.meta.{format, source_label, ascending_is_good, thresholds}` | Read by dbr to render KPI cards |

**Polish vs English:** metric *names* are English snake_case (`fiscal_balance_weo`); user-facing labels are Polish (`Saldo fiskalne (MFW)`). dbr renders the label.

**Naming hygiene:** every fact with native dimensions gets a short `primary_entity` (e.g. `imf`, not `finance_imf_row`) so MetricFlow's `<entity>__<dim>` prefix stays readable in dashboard YAMLs.

### 4. Dashboards (`products/dashboards/`)

One folder per dashboard, dbr YAML format. Drop-in shape ([dbr docs](../packages/dbr/README.md)):

```
products/dashboards/<domain>/
├── app.py                       8-line bootstrap (never edit)
├── dashboard.yml                domain, port, title, footer
└── pages/
    ├── pages.yml                page order
    └── <page>/
        ├── page.yml             page title + anchor
        └── visuals/
            ├── visuals.yml      row layout
            └── <visual>.yml     one visual per file
```

**Visual types** (from `packages/dbr/src/dbr/visuals/`): `card`, `line`, `column`, `bar`, `area`, `pie`, `scatter`, `table`.

**Validation:** `dbr validate products/dashboards/<domain>` checks every YAML against JSON Schema before deploy. A cheaper AI authoring visuals can't ship broken specs — `dbr validate` will reject them.

### 5. Publishing (`infra/`)

| Concern | Where | Notes |
|---|---|---|
| HTTP reverse proxy | `infra/nginx/conf.d/portal.conf` | Routes per dashboard |
| Auto-generated dashboard routes | `infra/nginx/conf.d/dbr-routes/<domain>.conf` | Written by `dbr run` |
| TLS certs | `infra/nginx/certs/` (Let's Encrypt) | Renewed via certbot |
| Static web root | `infra/nginx/html/` | Portal landing page + static dashboards |
| systemd units | `infra/systemd/or-<domain>.service` | Hand-written for legacy; `dbr run` writes new ones |

**Deploy command:** `dbr run products/dashboards/<domain>` — writes systemd unit, restarts service, waits for port health, writes nginx route, reloads nginx.

---

## URL structure

| URL | Serves | Stack |
|---|---|---|
| `www.open-reporting.dev` | Ghost blog | Docker container |
| `portal.open-reporting.dev` | Static portal landing | nginx |
| `portal.open-reporting.dev/public_finance/` | Public Finance dashboard | dbr / Dash (8057) |

**One dashboard, one stack.** All earlier dashboards (labour, explorer, finance, mobile PWA, test scaffold) were prototypes from different phases of the project and were retired together with the legacy `complex_dashboard` skill. New domain dashboards (labour, demography, health, …) will be authored on dbr following the public_finance pattern.

A mobile-responsive variant is a future direction — the intent is to extend dbr (or add a dbr-mobile package) so the same declarative YAML can target both desktop and mobile, rather than maintaining a separate FastAPI stack.

---

## AI delegation contract

This section is the **routing rule** for which model handles which task. Read this before delegating any work.

### Declarative plane (Sonnet / Haiku safe)

| Task | Path | Tool/check |
|---|---|---|
| Add or edit a dashboard visual | `products/dashboards/<domain>/pages/<page>/visuals/<v>.yml` | `dbr validate` |
| Reorder pages or rows | `products/dashboards/<domain>/pages/<page>/visuals/visuals.yml`, `pages/pages.yml` | `dbr validate` |
| Add a metric | `products/warehouse/models/semantic/<file>.yml` | `dbt parse` |
| Add a dbt model | `products/warehouse/models/<staging|intermediate|marts|dim>/<file>.sql` + `.yml` | `dbt run --select <model>`, `dbt test` |
| Tweak ingestion config (URL, schema, columns) | `products/ingestion/to_*/configs/<source>.yml` (when implemented) | run the script |
| Author a blog post / domain brief / social card | `products/blog/`, `products/domain-briefs/`, `products/social/` | content-reviewer agent |
| Update docs | `docs/*.md`, `team/**/*.md` | manual review |

### Engine plane (Opus only)

| Task | Path | Why expert-only |
|---|---|---|
| Add a new dbr visual type | `packages/dbr/src/dbr/visuals/<new>.py` | New Python module + schema + visual registry update |
| Change semantic-query behaviour | `packages/dbr/src/dbr/semantic/semantic.py` | Touches the in-process MetricFlow engine |
| Modify theme tokens | `packages/dbr/src/dbr/theme/theme.yaml` | Affects every dashboard; need design judgment |
| Edit deploy logic (`dbr run`) | `packages/dbr/src/dbr/cli.py` | systemd + nginx coordination |
| Change nginx server blocks | `infra/nginx/conf.d/portal.conf` | TLS + routing |
| New systemd unit (hand-written) | `infra/systemd/or-*.service` | (`dbr run` writes its own — those are declarative) |
| Modify AI agent definitions | `.claude/agents/<agent>.md` | Affects all sessions |
| Move the boundary itself | This document, repo structure | Architectural change |

### How a cheap AI should escalate

If a Sonnet/Haiku session needs something it can't do declaratively (e.g., "the column visual doesn't support a dual-axis option I need"), it must:

1. **Stop** — do not edit `packages/`.
2. **Log the request** as a Linear issue or `team/lessons-learned.md` entry describing the missing capability and the declarative shape it should have.
3. **Find a declarative workaround** for the immediate task if possible.

Expert AI consumes the queue and batches framework improvements.

---

## Conventions

### Naming

- **Folders, files, code identifiers**: English, snake_case
- **User-facing strings (chart titles, KPI labels, page names, portal copy)**: Polish, with proper diacritics
- **Branches**: `feat/OR-<issue>-<slug>` or `fix/...` / `refactor/...` / `docs/...`
- **Commits**: `feat:`, `fix:`, `refactor:`, `docs:`, `chore:` prefixes; one logical change per commit

### Polish content

- Always proper diacritics (ą, ć, ę, ł, ń, ó, ś, ź, ż)
- Formal register for analytical content
- No machine-translation artefacts

### Polish-specific data quirks (acknowledge before publishing)

- GUS methodology changes (LFS methodology break 2021 — labour data)
- EU-27 composition changes (UK exit; aggregates EA19 / EA20 / EA21 / EU27_2020 have different members in different years)
- Greece is `EL` in Eurostat coding, not ISO `GR`

---

## Working with the secrets

All secrets in `.env` (gitignored). See `.env.example` for the full list.

Key variables:
- `DUCKDB_PATH` — path to warehouse.duckdb (default: `/opt/open-reporting/data/warehouse.duckdb`)
- `POSTGRES_PASSWORD` — PostgreSQL password (Ghost only)
- `INSTAGRAM_APP_ID`, `INSTAGRAM_APP_SECRET`, `INSTAGRAM_ACCESS_TOKEN` — Meta API

`sudo NOPASSWD` is granted for `systemctl or-*` and `cp infra/systemd/*.service` so `dbr run` works without prompts.

---

## When this document is wrong

If you find this document conflicts with the code:

- **Code is the immediate truth**, but
- **this document is the intent** — the conflict is a bug in one or the other

Open a PR that either fixes the code or fixes the doc. Don't silently leave the conflict.

When the two planes need to shift (new declarative capability that didn't exist before), update this document **before** writing the code that implements it.
