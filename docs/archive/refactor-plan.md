> **ARCHIVED 2026-05-22** — the structural refactor (Phases 1–8.2 + verification) is complete. The end state described here is now the live repo. Kept for historical reference of how the transition was executed. Current architecture: [`../ARCHITECTURE.md`](../ARCHITECTURE.md).

# Refactor Plan — Repo Reorganisation to Two-Plane Architecture

**Purpose:** mechanically transform the current repo into the structure described in [`ARCHITECTURE.md`](./ARCHITECTURE.md).

**Audience:** a mid-tier AI model (Sonnet) or careful human executing one phase at a time. Each phase is a single commit. Phases are mostly independent — if you stop after phase N, the repo still works.

**Branch:** continue on `feat/or-dashboards-kit` (or branch from it).

**Prerequisites:**
- Working tree is clean (`git status` shows no changes)
- All services running (`systemctl is-active or-public_finance`, `or-test_dashboard` return `active`)
- dbt parses cleanly (`cd platform/processing/dbt && DUCKDB_PATH=... dbt parse --profiles-dir .`)

---

## Pre-flight read

Read [`ARCHITECTURE.md`](./ARCHITECTURE.md) first. The end state is described there. This document is purely the path from A to B.

When in doubt: **ARCHITECTURE.md wins**. If a step in this plan contradicts the architecture doc, fix the plan, not the architecture.

---

## Target end state

```
/opt/open-reporting/
├── products/
│   ├── ingestion/              (was platform/ingestion/)
│   ├── warehouse/              (was platform/processing/dbt/)
│   │   ├── dbt_project.yml
│   │   ├── profiles.yml
│   │   └── models/
│   │       ├── staging/
│   │       │   ├── dbw/
│   │       │   ├── eurostat/
│   │       │   ├── nbp/
│   │       │   └── imf/
│   │       ├── intermediate/
│   │       │   ├── int_finance_consolidated.sql
│   │       │   └── by_domain/<domain>_indicators.sql ×18
│   │       ├── marts/
│   │       │   └── finance/
│   │       │       ├── fact_finance_overview.sql
│   │       │       ├── fact_finance_cofog.sql
│   │       │       ├── fact_finance_imf.sql
│   │       │       └── fact_finance_revenue_expenditure.sql
│   │       ├── dim/
│   │       │   ├── dim_calendar.sql
│   │       │   ├── dim_cofog.sql
│   │       │   └── dim_geo.sql
│   │       └── semantic/
│   │           ├── finance_overview.yml
│   │           ├── finance_cofog.yml
│   │           ├── finance_imf.yml
│   │           └── finance_revenue_expenditure.yml
│   ├── database/               (was platform/database/)
│   │   ├── catalogue/
│   │   ├── data/
│   │   ├── deploy/
│   │   └── loader.py
│   ├── dashboards/             (keep — clean out legacy)
│   │   ├── public_finance/
│   │   ├── test_dashboard/
│   │   ├── labour/             (legacy, kept until parity)
│   │   ├── explorer/           (legacy)
│   │   └── finance/            (legacy)
│   ├── blog/  social/  research/  mobile/  domain-briefs/
│
├── packages/
│   ├── dbr/                    (unchanged location)
│   └── screenshot/             (was tools/screenshot.py)
│
├── docs/                       (unchanged location; refreshed content)
├── team/                       (unchanged location; path refs updated)
├── infra/                      (unchanged)
├── .claude/                    (path refs updated in agents)
├── data/                       (unchanged, gitignored)
│
└── (root files unchanged: CLAUDE.md, AGENTS.md, README.md, docker-compose.yml,
    .env, .env.example, .gitignore, requirements.txt, skills-lock.json)
```

**Deletions:**
- `platform/` directory removed entirely
- `tools/` directory removed entirely
- `package.json` + `node_modules/` removed (leftover OpenAI experiment)
- `products/semantic/` removed (legacy pre-MetricFlow — survives only as long as Labour uses it; deletion is **not** in this plan)
- `products/dashboards/{_template, template, pilot_template, finance_test}` removed
- `infra/systemd/or-template.service` and `or-finance-test.service` removed (services already stopped)

---

## Phase 0 — Adopt the architecture (already done)

Already in place by the commit that adds this file:
- `docs/ARCHITECTURE.md` rewritten as target state
- `docs/refactor-plan.md` (this file) written

No further action.

---

## Phase 1 — Pure deletions (low risk, no path changes)

**Goal:** remove confirmed-stale files. Nothing else moves yet.

### 1a. Root-level cleanup

```bash
rm /opt/open-reporting/package.json
rm -rf /opt/open-reporting/node_modules
```

Why: `package.json` declares one dep (`openai`) from an early experiment never used in code. `node_modules/` is its dependency tree.

Verify: `grep -rln "openai\|node_modules" /opt/open-reporting --include="*.py"` returns nothing important (Ghost CMS uses node internally but it's in its Docker image, not the host).

### 1b. Stale warehouse DDL — careful, two files are actually used

**Discovered during execution:** two DDL files in `platform/warehouse/raw/` are loaded at runtime by ingestion scripts, NOT stale:

| DDL file | Used by | Action |
|---|---|---|
| `platform/warehouse/raw/dbw_observations.sql` | `platform/ingestion/to_raw/dbw_observations.py:48-53` (ensure_table) | **Co-locate** with its script |
| `platform/warehouse/raw/imf_weo.sql` | `platform/ingestion/to_raw/imf_weo.py:91-96` (ensure_table) | **Co-locate** with its script |
| `platform/warehouse/raw/eurostat_observations.sql` | nothing | Delete (orphaned) |
| `platform/warehouse/raw/nbp_exchange_rates.sql` | nothing | Delete (orphaned) |
| `platform/warehouse/curated/mart_finance.sql` | nothing (dbt has it) | Delete |
| `platform/warehouse/dimensions/*.sql` (7 files) | nothing (dbt has dim_geo/dim_calendar/dim_cofog with different shapes) | Delete |
| `platform/warehouse/deploy/` | empty | Delete |

```bash
# Step 1: co-locate the 2 live DDL files
git mv /opt/open-reporting/platform/warehouse/raw/dbw_observations.sql \
       /opt/open-reporting/platform/ingestion/to_raw/dbw_observations.sql
git mv /opt/open-reporting/platform/warehouse/raw/imf_weo.sql \
       /opt/open-reporting/platform/ingestion/to_raw/imf_weo.sql

# Step 2: update the python scripts to use the co-located path
# imf_weo.py — change ddl_path target from "../../warehouse/raw/imf_weo.sql" to "imf_weo.sql"
sed -i 's|"../../warehouse/raw/imf_weo.sql"|"imf_weo.sql"|' \
  /opt/open-reporting/platform/ingestion/to_raw/imf_weo.py

# dbw_observations.py — same idea, plus switch from REPO_ROOT-based to file-relative path
sed -i 's|"platform/warehouse/raw/dbw_observations.sql"|"dbw_observations.sql"|' \
  /opt/open-reporting/platform/ingestion/to_raw/dbw_observations.py
sed -i 's|os.environ.get("REPO_ROOT", "/opt/open-reporting"),|os.path.dirname(os.path.abspath(__file__)),|' \
  /opt/open-reporting/platform/ingestion/to_raw/dbw_observations.py

# Step 3: now safe to delete the rest of platform/warehouse/
rm -rf /opt/open-reporting/platform/warehouse/
```

Verify after each step:
```bash
python3 -m py_compile /opt/open-reporting/platform/ingestion/to_raw/imf_weo.py
python3 -m py_compile /opt/open-reporting/platform/ingestion/to_raw/dbw_observations.py
ls /opt/open-reporting/platform/ingestion/to_raw/*.sql  # should show 2 files
```

**Why co-locate (not just move to a new ddl/ subfolder):** survives Phase 3 (move ingestion to products/) automatically — the SQL travels alongside its script. After this step, when the ingestion script moves, its DDL moves with it.

### 1c. Stale dashboards

```bash
# Stop their services first so we can safely remove unit files later
sudo -n /usr/bin/systemctl stop or-template.service or-test_dashboard.service 2>/dev/null
sudo -n /usr/bin/systemctl disable or-template.service 2>/dev/null
sudo -n rm -f /etc/systemd/system/or-template.service
sudo -n /usr/bin/systemctl daemon-reload

# Remove the directories
rm -rf /opt/open-reporting/products/dashboards/_template
rm -rf /opt/open-reporting/products/dashboards/template
rm -rf /opt/open-reporting/products/dashboards/pilot_template
rm -rf /opt/open-reporting/products/dashboards/finance_test

# Remove their systemd units
rm -f /opt/open-reporting/infra/systemd/or-template.service
rm -f /opt/open-reporting/infra/systemd/or-finance-test.service

# Remove any nginx routes pointing to them (only template might have one)
rm -f /opt/open-reporting/infra/nginx/conf.d/dbr-routes/template.conf
```

Keep: `public_finance`, `test_dashboard`, `labour`, `explorer`, `finance`.

### 1d. Commit

```
git add -A
git commit -m "chore: remove stale leftovers (package.json, warehouse DDL, scaffold dashboards)

- package.json + node_modules: leftover from an early OpenAI experiment;
  no code references the openai package.
- platform/warehouse/{raw,curated,dimensions,deploy}/*.sql: hand-written
  DDL predating dbt. The dbt project is the source of truth.
- products/dashboards/{_template, template, pilot_template, finance_test}:
  three abandoned scaffold attempts plus a temporary test directory.
- infra/systemd/or-{template,finance-test}.service: associated units."
```

**Verify before next phase:**
```bash
dbr run /opt/open-reporting/products/dashboards/public_finance   # should still succeed
dbr run /opt/open-reporting/products/dashboards/test_dashboard
curl -sf http://localhost:8057/public_finance/_dash-layout | head -c 100
curl -sf http://localhost:8056/test_dashboard/_dash-layout | head -c 100
```

**Rollback:** `git revert HEAD`

---

## Phase 2 — Package `screenshot` as a first-class package

**Goal:** unify `tools/` into `packages/` so all executable Python is a package.

### 2a. Create the package skeleton

```bash
mkdir -p /opt/open-reporting/packages/screenshot/src/screenshot
```

Write `packages/screenshot/pyproject.toml`:
```toml
[project]
name = "screenshot"
version = "0.1.0"
description = "Dashboard screenshot utility for Open Reporting"
requires-python = ">=3.10"
dependencies = [
  "playwright>=1.40",
]

[project.scripts]
screenshot = "screenshot.cli:main"

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]
```

Write `packages/screenshot/src/screenshot/__init__.py`:
```python
"""Dashboard screenshot CLI."""
__version__ = "0.1.0"
```

Move `tools/screenshot.py` into the package as `cli.py`:
```bash
git mv /opt/open-reporting/tools/screenshot.py \
       /opt/open-reporting/packages/screenshot/src/screenshot/cli.py
```

Update the file's `if __name__ == "__main__"` block to define a `main()` function and call it (so the entry point in pyproject.toml resolves). At the bottom of `cli.py`:
```python
def main() -> int:
    """Entry point for the `screenshot` CLI command."""
    # existing argument parsing / main logic — wrap whatever was at module level
    ...
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

The exact wrap depends on the current file shape. Open it; the top-level `if __name__ == "__main__"` block becomes `main()`.

### 2b. Install editable

```bash
pip install --break-system-packages -e /opt/open-reporting/packages/screenshot
```

### 2c. Update references

Files referencing `tools/screenshot.py`:
- `.claude/agents/visual-screenshot-reviewer.md` — change `python3 tools/screenshot.py` to `screenshot`
- `docs/RELEASE_NOTES.md` — find/replace once

```bash
# Find any remaining references
grep -rln "tools/screenshot\|tools.screenshot" /opt/open-reporting --include="*.md" --include="*.py" | grep -v __pycache__
```

### 2d. Remove `tools/`

```bash
rmdir /opt/open-reporting/tools
```

### 2e. Commit

```
git add -A
git commit -m "refactor: move tools/screenshot.py to packages/screenshot/ as proper package

Unifies all engine-plane Python under packages/. Provides a 'screenshot'
CLI entry point installed via pip install -e. Removes the tools/ directory.

Updated references:
- .claude/agents/visual-screenshot-reviewer.md: invocation changed to
  'screenshot <dashboard>' from 'python3 tools/screenshot.py <dashboard>'"
```

**Verify:**
```bash
which screenshot && screenshot --help
```

**Rollback:** `git revert HEAD` + `pip uninstall screenshot`.

---

## Phase 3 — Move ingestion

**Goal:** `platform/ingestion/` → `products/ingestion/`.

### 3a. The move

```bash
mkdir -p /opt/open-reporting/products
git mv /opt/open-reporting/platform/ingestion /opt/open-reporting/products/ingestion
```

### 3b. Find/replace path references

This is the find/replace map. Apply each:

| Old path | New path | Files affected |
|---|---|---|
| `platform/ingestion/` | `products/ingestion/` | docs/, team/, .claude/agents/, ingestion scripts internal docstrings |

```bash
# Generate the list of files that reference the old path
grep -rln "platform/ingestion" /opt/open-reporting \
  --include="*.py" --include="*.md" --include="*.yml" \
  | grep -v __pycache__ | grep -v node_modules | grep -v ".git/"
```

Expected files (verify each):
- `.claude/skills_review/composite_review/SKILL.md`
- `.claude/agents/data-engineer.md`
- `.claude/agents/data-architect.md`
- `.claude/agents/architecture-critic.md`
- `.claude/agents/data-engineer-reviewer.md`
- `products/ingestion/to_raw/imf_weo.py` (now-moved, may have self-references in docstrings)
- `products/ingestion/to_raw/eurostat_observations.py`
- `products/ingestion/to_raw/nbp_exchange_rates.py`
- `products/ingestion/to_raw/dbw_observations.py`
- `products/ingestion/to_landing/dbw_hvd.py`
- `team/PLATFORM.md`
- `team/knowledge-base/data-architecture/architecture.md`
- `team/knowledge-base/data-engineering/engineering.md`
- `docs/CONTRIBUTING.md`
- `docs/DATA_SOURCES.md`
- `team/standards/INDEX.md`
- `team/standards/evaluation/data-engineering-review.md`
- `team/standards/evaluation/architecture-review.md`
- `team/standards/evaluation/code-review.md`
- `team/standards/build/requirements.md`
- `CLAUDE.md`
- `AGENTS.md`

For each file, do a literal text replacement: `platform/ingestion/` → `products/ingestion/`.

A safe one-liner if you trust your tools:
```bash
grep -rl "platform/ingestion" /opt/open-reporting \
  --include="*.py" --include="*.md" --include="*.yml" \
  --exclude-dir=__pycache__ --exclude-dir=node_modules --exclude-dir=.git \
  | xargs sed -i 's|platform/ingestion|products/ingestion|g'
```

### 3c. Update .gitignore — caught during execution

The move breaks any `.gitignore` rule that referenced the old path. Specifically:

```
# Before:
platform/ingestion/to_raw/.dlt/secrets.toml

# After:
products/ingestion/to_raw/.dlt/secrets.toml
```

When the gitignore rule stops matching, `git add` picks up the previously-ignored file. Even if its content is template-only, the precedent is bad. Check `.gitignore` before committing:

```bash
grep "platform/" /opt/open-reporting/.gitignore
# Update any rules to use products/ paths instead.

# Also untrack anything that slipped in:
git diff --cached --name-only | xargs -I{} git check-ignore -v {} || true
# If a path appears in `git status` that should be ignored, run:
#   git rm --cached <path>
```

### 3d. Commit

```
git add -A
git commit -m "refactor: move platform/ingestion → products/ingestion

Step 3 of the two-plane refactor (see docs/refactor-plan.md):
ingestion is declarative work product, not engine code. All scripts
and references updated to the new path. No code-behaviour changes."
```

**Verify:**
```bash
# Ingestion scripts should still resolve as Python imports
python3 -c "import sys; sys.path.insert(0, '/opt/open-reporting'); from products.ingestion.to_raw import imf_weo"
# Or just spot-check that scripts still execute their --help
PYTHONPATH=/opt/open-reporting python3 /opt/open-reporting/products/ingestion/to_raw/eurostat_observations.py --help 2>&1 | head -5
# Dashboards unaffected by ingestion move — should still serve
curl -sf -o /dev/null -w '%{http_code}\n' http://localhost:8057/public_finance/
curl -sf -o /dev/null -w '%{http_code}\n' http://localhost:8056/test_dashboard/
```

**Rollback:** `git revert HEAD`.

---

## Phase 4 — Move + reorganise warehouse (load-bearing)

**Goal:** `platform/processing/dbt/` → `products/warehouse/` AND reorganise models into the dbt-standard `staging/intermediate/marts/dim/semantic` layout.

This is the **hardest phase**. Two commits — first the move, then the reorganisation — so each is independently revertable.

### 4a. The move (no internal reshape yet)

```bash
git mv /opt/open-reporting/platform/processing/dbt \
       /opt/open-reporting/products/warehouse
```

### 4b. Update all path references — dbr engine, profiles, docs, agents

The DBT_PROJECT_ROOT constant lives in:

| File | Line shape | Change |
|---|---|---|
| `packages/dbr/src/dbr/semantic/semantic.py` | `DBT_PROJECT_ROOT = Path("/opt/open-reporting/platform/processing/dbt")` | `Path("/opt/open-reporting/products/warehouse")` |
| `packages/dbr/src/dbr/compiler/compiler.py` | (verify — may not reference the path) | (skip if absent) |
| `.claude/skills/complex_dashboard/assets_legacy/runtime/semantic.py` | same constant | same change (or skip if legacy unused) |

Then text replacements across docs + agents + standards:

```bash
grep -rl "platform/processing/dbt" /opt/open-reporting \
  --include="*.py" --include="*.md" --include="*.yml" \
  --exclude-dir=__pycache__ --exclude-dir=node_modules --exclude-dir=.git \
  | xargs sed -i 's|platform/processing/dbt|products/warehouse|g'
```

Expected files (verify):
- `CLAUDE.md`
- `AGENTS.md`
- `.claude/skills_review/basic_semantic_model/SKILL.md`
- `.claude/agents/data-architect.md`
- `.claude/agents/measures-reviewer.md`
- `.claude/skills/complex_dashboard/SKILL.md`
- `.claude/skills_review/composite_review/SKILL.md`
- `.claude/agents/data-engineer.md`
- `packages/dbr/src/dbr/semantic/semantic.py`
- `packages/dbr/src/dbr/compiler/compiler.py`
- `team/PLATFORM.md`
- `docs/RELEASE_NOTES.md`
- `docs/DATA_MODEL.md`
- `team/standards/build/processing.md`
- `team/standards/build/storage.md`
- `team/standards/evaluation/measures-review.md`
- `team/standards/build/measures.md`

### 4c. Verify dbt still works at the new path

```bash
cd /opt/open-reporting/products/warehouse
DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb dbt parse --profiles-dir .
```

Expected: clean parse, no errors.

### 4d. Verify dashboards still work

```bash
dbr run /opt/open-reporting/products/dashboards/public_finance
dbr run /opt/open-reporting/products/dashboards/test_dashboard
curl -sf http://localhost:8057/public_finance/_dash-layout -o /dev/null -w "HTTP %{http_code}\n"
```

### 4e. Commit (the path move)

```
git add -A
git commit -m "refactor: move platform/processing/dbt → products/warehouse

Step 4a of the two-plane refactor. dbt project relocated; internal
folder structure unchanged in this commit (phase 4f handles reshape).

Updated path references in:
- packages/dbr (DBT_PROJECT_ROOT constant)
- all .claude/agents/* and skills referencing the old path
- all docs and standards
- CLAUDE.md, AGENTS.md

Verified: dbt parse clean; both dashboards (public_finance,
test_dashboard) boot and serve."
```

### 4f. Reorganise models inside `products/warehouse/models/`

Now the internal reshape. Target structure:

```
products/warehouse/models/
├── staging/
│   ├── dbw/
│   │   ├── stg_dbw.sql              (was dbw/stg_dbw.sql)
│   │   └── sources.yml              (was dbw/sources.yml)
│   ├── eurostat/
│   │   ├── stg_eurostat.sql         (was eurostat/stg_eurostat.sql)
│   │   ├── stg_eurostat_finance.sql (was pub/stg_eurostat_finance.sql)
│   │   ├── all_indicators.sql       (was eurostat/all_indicators.sql — keep here, it's a wide-staging consolidation)
│   │   └── sources.yml              (was eurostat/sources.yml)
│   ├── nbp/
│   │   └── stg_nbp.sql              (was finance/stg_nbp.sql)
│   └── imf/
│       └── stg_imf_finance.sql      (was pub/stg_imf_finance.sql)
│
├── intermediate/
│   ├── int_finance_consolidated.sql (was mart/mart_finance.sql — RENAMED)
│   └── by_domain/
│       ├── agr_indicators.sql       (was agr/agr_indicators.sql)
│       ├── bus_indicators.sql       (was bus/bus_indicators.sql)
│       ├── clt_indicators.sql       (was clt/clt_indicators.sql)
│       ├── crm_indicators.sql       (was crm/crm_indicators.sql)
│       ├── edu_indicators.sql       (was edu/edu_indicators.sql)
│       ├── ene_indicators.sql       (was ene/ene_indicators.sql)
│       ├── env_indicators.sql       (was env/env_indicators.sql)
│       ├── fin_indicators.sql       (was finance/fin_indicators.sql)
│       ├── hlt_indicators.sql       (was hlt/hlt_indicators.sql)
│       ├── lab_indicators.sql       (was lab/lab_indicators.sql)
│       ├── mac_indicators.sql       (was mac/mac_indicators.sql)
│       ├── pop_indicators.sql       (was pop/pop_indicators.sql)
│       ├── prc_indicators.sql       (was prc/prc_indicators.sql)
│       ├── pub_indicators.sql       (was pub/pub_indicators.sql)
│       ├── sci_indicators.sql       (was sci/sci_indicators.sql)
│       ├── soc_indicators.sql       (was soc/soc_indicators.sql)
│       ├── trd_indicators.sql       (was trd/trd_indicators.sql)
│       └── trp_indicators.sql       (was trp/trp_indicators.sql)
│
├── marts/
│   └── finance/
│       ├── fact_finance_overview.sql              (was finance/fact_finance_overview.sql)
│       ├── fact_finance_overview.yml
│       ├── fact_finance_cofog.sql
│       ├── fact_finance_cofog.yml
│       ├── fact_finance_imf.sql
│       ├── fact_finance_imf.yml
│       ├── fact_finance_revenue_expenditure.sql
│       ├── fact_finance_revenue_expenditure.yml
│       └── schema.yml                              (was finance/schema.yml)
│
├── dim/
│   ├── dim_calendar.sql
│   ├── dim_calendar.yml
│   ├── dim_cofog.sql
│   ├── dim_cofog.yml
│   ├── dim_geo.sql
│   └── dim_geo.yml
│
└── semantic/
    ├── finance_overview.yml         (was finance/semantic_models/finance_overview.yml)
    ├── finance_cofog.yml
    ├── finance_imf.yml
    └── finance_revenue_expenditure.yml
```

**Execution:** below is the full set of `git mv` commands.

```bash
cd /opt/open-reporting/products/warehouse/models

# staging/
mkdir -p staging/dbw staging/eurostat staging/nbp staging/imf
git mv dbw/stg_dbw.sql                  staging/dbw/stg_dbw.sql
git mv dbw/sources.yml                  staging/dbw/sources.yml
git mv eurostat/stg_eurostat.sql        staging/eurostat/stg_eurostat.sql
git mv eurostat/all_indicators.sql      staging/eurostat/all_indicators.sql
git mv eurostat/sources.yml             staging/eurostat/sources.yml
git mv pub/stg_eurostat_finance.sql     staging/eurostat/stg_eurostat_finance.sql
git mv finance/stg_nbp.sql              staging/nbp/stg_nbp.sql
git mv pub/stg_imf_finance.sql          staging/imf/stg_imf_finance.sql

# intermediate/
mkdir -p intermediate/by_domain
git mv mart/mart_finance.sql            intermediate/int_finance_consolidated.sql
git mv agr/agr_indicators.sql           intermediate/by_domain/agr_indicators.sql
git mv bus/bus_indicators.sql           intermediate/by_domain/bus_indicators.sql
git mv clt/clt_indicators.sql           intermediate/by_domain/clt_indicators.sql
git mv crm/crm_indicators.sql           intermediate/by_domain/crm_indicators.sql
git mv edu/edu_indicators.sql           intermediate/by_domain/edu_indicators.sql
git mv ene/ene_indicators.sql           intermediate/by_domain/ene_indicators.sql
git mv env/env_indicators.sql           intermediate/by_domain/env_indicators.sql
git mv finance/fin_indicators.sql       intermediate/by_domain/fin_indicators.sql
git mv hlt/hlt_indicators.sql           intermediate/by_domain/hlt_indicators.sql
git mv lab/lab_indicators.sql           intermediate/by_domain/lab_indicators.sql
git mv mac/mac_indicators.sql           intermediate/by_domain/mac_indicators.sql
git mv pop/pop_indicators.sql           intermediate/by_domain/pop_indicators.sql
git mv prc/prc_indicators.sql           intermediate/by_domain/prc_indicators.sql
git mv pub/pub_indicators.sql           intermediate/by_domain/pub_indicators.sql
git mv sci/sci_indicators.sql           intermediate/by_domain/sci_indicators.sql
git mv soc/soc_indicators.sql           intermediate/by_domain/soc_indicators.sql
git mv trd/trd_indicators.sql           intermediate/by_domain/trd_indicators.sql
git mv trp/trp_indicators.sql           intermediate/by_domain/trp_indicators.sql

# marts/
mkdir -p marts/finance
git mv finance/fact_finance_overview.sql              marts/finance/fact_finance_overview.sql
git mv finance/fact_finance_overview.yml              marts/finance/fact_finance_overview.yml
git mv finance/fact_finance_cofog.sql                 marts/finance/fact_finance_cofog.sql
git mv finance/fact_finance_cofog.yml                 marts/finance/fact_finance_cofog.yml
git mv finance/fact_finance_imf.sql                   marts/finance/fact_finance_imf.sql
git mv finance/fact_finance_imf.yml                   marts/finance/fact_finance_imf.yml
git mv finance/fact_finance_revenue_expenditure.sql   marts/finance/fact_finance_revenue_expenditure.sql
git mv finance/fact_finance_revenue_expenditure.yml   marts/finance/fact_finance_revenue_expenditure.yml
git mv finance/schema.yml                             marts/finance/schema.yml
git mv finance/sources.yml                            marts/finance/sources.yml      # if exists; check

# semantic/
mkdir -p semantic
git mv finance/semantic_models/finance_overview.yml             semantic/finance_overview.yml
git mv finance/semantic_models/finance_cofog.yml                semantic/finance_cofog.yml
git mv finance/semantic_models/finance_imf.yml                  semantic/finance_imf.yml
git mv finance/semantic_models/finance_revenue_expenditure.yml  semantic/finance_revenue_expenditure.yml

# dim/ — already in the right place, no move needed

# Clean up now-empty old folders
rmdir agr bus clt crm dbw edu ene env eurostat finance hlt lab mac mart pop prc pub sci soc trd trp 2>/dev/null
rmdir finance/semantic_models 2>/dev/null
```

### 4g. Update internal references

The rename `mart_finance` → `int_finance_consolidated` is **the only model name that changed**. Update all `{{ ref('mart_finance') }}` references in fact SQL files:

```bash
grep -rln "ref('mart_finance')" /opt/open-reporting/products/warehouse/models
# Expected: 4 fact files in marts/finance/
sed -i "s|ref('mart_finance')|ref('int_finance_consolidated')|g" \
  /opt/open-reporting/products/warehouse/models/marts/finance/fact_finance_*.sql
```

### 4h. Update `dbt_project.yml` model configs

Open `products/warehouse/dbt_project.yml`. Look for any model-path-specific configs (e.g., `models: open_reporting: finance: +materialized: table`). They reference the old folder names. Update to new structure:

```yaml
# Likely before:
models:
  open_reporting:
    finance:
      +materialized: table
    mart:
      +materialized: table
    dim:
      +materialized: table

# After:
models:
  open_reporting:
    staging:
      +materialized: view
    intermediate:
      +materialized: view
    marts:
      +materialized: table
    dim:
      +materialized: table
    semantic:
      +materialized: ephemeral   # (or omit — semantic_models are not SQL)
```

(Exact change depends on what's currently in `dbt_project.yml` — open and adapt.)

### 4i. Verify and rebuild

```bash
cd /opt/open-reporting/products/warehouse
DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb dbt parse --profiles-dir .
# Expected: clean parse

DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb dbt run --profiles-dir .
# Expected: all models rebuild successfully
```

If any model fails because it references a now-renamed model, fix the ref and re-run.

### 4j. Redeploy dashboards and verify

```bash
dbr run /opt/open-reporting/products/dashboards/public_finance
dbr run /opt/open-reporting/products/dashboards/test_dashboard

# Verify all 5 pages of public_finance still render
curl -sf http://localhost:8057/public_finance/_dash-layout | python3 -c "
import json, sys
d = json.load(sys.stdin)
def find(o, p, out=None):
    if out is None: out = []
    if isinstance(o, dict):
        if p(o): out.append(o)
        for v in o.values(): find(v, p, out)
    elif isinstance(o, list):
        for v in o: find(v, p, out)
    return out
print('graphs:', len(find(d, lambda x: x.get('type') == 'Graph')))
print('h2:', len(find(d, lambda x: x.get('type') == 'H2')))
print('no-data divs:', len(find(d, lambda x: x.get('type') == 'Div' and x.get('props', {}).get('children') == 'No data')))
"
# Expected: graphs=8, h2=5, no-data=0
```

### 4k. Commit (the reshape)

```
git add -A
git commit -m "refactor: reorganise dbt models into staging/intermediate/marts/dim/semantic

Step 4b of the two-plane refactor. Adopts standard dbt project layout:
- staging/<source>/ — light typing on raw tables (was dbw/, eurostat/, pub/)
- intermediate/ — consolidations (was mart/) + by_domain/<X>_indicators.sql ×18
- marts/<domain>/ — star-schema facts (was finance/fact_*.sql)
- dim/ — shared dimensions (unchanged)
- semantic/ — MetricFlow definitions (was finance/semantic_models/)

Internal renames:
- mart_finance → int_finance_consolidated (it's an intermediate, not a mart)

dbt_project.yml model configs updated to new top-level folder names.
Verified: dbt parse + dbt run clean; public_finance renders 8 graphs
across 5 pages; test_dashboard renders identically."
```

**Rollback:** `git revert HEAD` (and HEAD~1 if reverting the path move too).

---

## Phase 5 — Move operational database schema

**Goal:** `platform/database/` → `products/database/`.

```bash
git mv /opt/open-reporting/platform/database /opt/open-reporting/products/database
```

Update references:

```bash
grep -rln "platform/database" /opt/open-reporting \
  --include="*.py" --include="*.md" \
  --exclude-dir=__pycache__ --exclude-dir=node_modules --exclude-dir=.git \
  | xargs sed -i 's|platform/database|products/database|g'
```

Expected files:
- `.claude/agents/data-engineer.md`
- `products/database/loader.py` (internal docstrings)
- `team/standards/build/ingestion.md`
- `team/standards/build/storage.md`

Commit:
```
git add -A
git commit -m "refactor: move platform/database → products/database

PostgreSQL operational schema (catalogue + ops loaders) is declarative
work product, not engine code. Path references updated in 4 files."
```

---

## Phase 6 — Delete empty `platform/` and consolidate docs

**Goal:** remove the now-empty `platform/` directory and refresh docs that still describe the old structure.

### 6a. Remove platform/

```bash
# Should be empty by now
ls /opt/open-reporting/platform/
# Expected: empty
rmdir /opt/open-reporting/platform
```

### 6b. Archive stale docs

```bash
mkdir -p /opt/open-reporting/docs/archive
git mv /opt/open-reporting/docs/SITUATION.md            /opt/open-reporting/docs/archive/SITUATION.md
git mv /opt/open-reporting/docs/MVP.md                  /opt/open-reporting/docs/archive/MVP.md
git mv /opt/open-reporting/docs/or-142-chart-evaluation-findings.md \
       /opt/open-reporting/docs/archive/or-142-chart-evaluation-findings.md
```

Add a one-liner to top of each archived file (in commit, via sed or manual edit):

```
> **ARCHIVED 2026-05-22**: this document describes a prior state of the project.
> The current architecture is in [`../ARCHITECTURE.md`](../ARCHITECTURE.md).
```

### 6c. Update remaining docs

For each of the following, open and update sections that mention old paths or now-obsolete structure:

- `docs/DATA_MODEL.md` — refresh schema to reference new fact_finance_*, dim_geo, dim_cofog
- `docs/CONTRIBUTING.md` — paths to new structure
- `team/PLATFORM.md` — replace inline architecture with: "See [`../docs/ARCHITECTURE.md`](../docs/ARCHITECTURE.md) for the authoritative architecture document."
- `CLAUDE.md` — update the "Repo Structure" section to reference new tree
- `AGENTS.md` — update path examples

### 6d. Commit

```
git add -A
git commit -m "docs: archive stale docs, refresh remaining for new structure

- Removed empty platform/ directory (all moved in phases 3-5).
- Archived: SITUATION.md, MVP.md, or-142-chart-evaluation-findings.md
  to docs/archive/ — each describes a prior state.
- Updated DATA_MODEL.md, CONTRIBUTING.md, CLAUDE.md, AGENTS.md to
  reference the new declarative-plane / engine-plane layout.
- team/PLATFORM.md now points at docs/ARCHITECTURE.md instead of
  duplicating its content."
```

---

## Phase 7 — Final verification

After all phases, run this checklist:

```bash
# 1. dbt parse + run
cd /opt/open-reporting/products/warehouse
DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb dbt parse --profiles-dir .
DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb dbt run --profiles-dir .
DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb dbt test --profiles-dir .

# 2. dbr smoke test
cd /opt/open-reporting
dbr validate products/dashboards/public_finance
dbr validate products/dashboards/test_dashboard
dbr run products/dashboards/public_finance
dbr run products/dashboards/test_dashboard

# 3. HTTP health on all live dashboards
for url in \
  http://localhost:8050/labour/ \
  http://localhost:8051/explorer/ \
  http://localhost:8052/app/ \
  http://localhost:8053/finance/ \
  http://localhost:8056/test_dashboard/ \
  http://localhost:8057/public_finance/; do
  echo "  $url → $(curl -sf -o /dev/null -w '%{http_code}' $url || echo FAILED)"
done

# 4. Screenshot package
screenshot --help

# 5. Visual: load public_finance, check graphs render
curl -sf http://localhost:8057/public_finance/_dash-layout | head -c 200
```

Expected:
- dbt parse + run: pass
- dbr validate: OK
- All HTTP: 200
- screenshot --help: shows usage
- public_finance layout: starts with `{"props":` and contains graph data

If anything fails, the offending phase can be reverted independently.

---

## Reference: full file/path map

The complete before/after for files that move:

### Engine-plane unification (Phase 2)

| Before | After |
|---|---|
| `tools/screenshot.py` | `packages/screenshot/src/screenshot/cli.py` |
| (none) | `packages/screenshot/pyproject.toml` |
| (none) | `packages/screenshot/src/screenshot/__init__.py` |

### Declarative-plane consolidation (Phases 3–5)

| Before | After |
|---|---|
| `platform/ingestion/` | `products/ingestion/` |
| `platform/processing/dbt/` | `products/warehouse/` |
| `platform/database/` | `products/database/` |
| `platform/` | (deleted) |

### Pure deletions (Phase 1)

- `package.json`
- `node_modules/`
- `platform/warehouse/{raw,curated,dimensions,deploy}/`
- `products/dashboards/{_template, template, pilot_template, finance_test}/`
- `infra/systemd/or-{template, finance-test}.service`

### dbt model layout (Phase 4f)

See full table inside Phase 4f.

### Path-reference updates (find/replace)

| Old | New | Phase |
|---|---|---|
| `tools/screenshot` | `screenshot` | 2 |
| `tools.screenshot` | `screenshot` | 2 |
| `platform/ingestion` | `products/ingestion` | 3 |
| `platform/processing/dbt` | `products/warehouse` | 4 |
| `platform/database` | `products/database` | 5 |
| `ref('mart_finance')` | `ref('int_finance_consolidated')` | 4 |

---

## What this plan does *not* do

These are out of scope — separate work, separate sessions:

- **Migrate Labour, Explorer, or Finance to dbr.** Legacy dashboards keep running. dbr migration is per-domain product work, not a refactor.
- **Delete `products/semantic/`.** This legacy module is still used by Labour. Delete after migration.
- **Implement declarative ingestion.** The `products/ingestion/` directory keeps Python scripts — moving them is enough for now. YAML templates are a separate initiative.
- **Process the `.claude/skills_review/` backlog.** 27 skills awaiting review; treat as its own session.
- **Add CI/CD.** Manual deploy remains the model.

---

## On stopping early

You can stop after any phase commit. The repo will be in a working intermediate state — not as clean as the final shape, but functional. Phases 1, 2, 3, 5, 6 are independent. Phases 4a and 4f are coupled (the move makes the reshape possible) but each is its own commit.

If a phase fails verification, **do not push forward**. Investigate, fix or revert that phase only.
