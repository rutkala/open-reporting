---
name: architecture
description: "Produce an architecture design for a data product. Defines data model, data flow, component inventory, and KPI calculation logic."
user-invocable: false
---

# Architecture

Specifies how the product will be built — data layer, component structure, and calculation
logic. Drives both the data pipeline work and the code in subsequent steps.

Applies to: dashboard, portal (any product with a data layer).

## Input

- Requirements document
- Domain brief

## Output

- Architecture design document (markdown file on feature branch)
- Approved by PO before next step begins

## Components

| Role | Agent |
|------|-------|
| Data model + KPI logic | data-engineer |
| Component inventory | dashboard-dev |
| Reviewer | architecture-critic |

data-engineer and dashboard-dev work in parallel once requirements are confirmed.

## Steps

1. Read requirements document and domain brief
2. data-engineer: design data model and KPI calculation logic
3. dashboard-dev: compile complete component inventory
4. Merge into single architecture design document
5. Spawn **architecture-critic** — fix P1 findings before proceeding; note P2 as caveats
6. Present to PO and wait for explicit approval

## Instructions

**Data model**
- Source tables required (raw schema)
- Curated tables to build (schema, grain, key fields)
- Gold mart if needed: `curated.mart_{domain}` — columns, calculated fields
- New dbt models required (list with purpose)

**KPI calculation logic**
For each KPI from the requirements document:
- SQL expression or dbt metric definition
- Denominator/numerator if a ratio
- Aggregation method (sum, avg, last value, YoY delta)
- Edge cases (division by zero, null handling, partial periods)

**Component inventory**
Complete list of every component:
- Charts: type, data source, x-axis, y-axis, series, filters applied
- KPI cards: metric, format, comparison reference
- Filters: field, type (dropdown/slider/date range), scope (page or global)
- Pages: name, purpose, components on it

**Data flow**
Text diagram: source → ingestion → raw → curated → gold → dashboard

**Dependencies**
- Ingestion jobs that must exist or be created
- dbt models that must exist or be created
- Any data gaps from requirements that block the build

## Standards

- `team/standards/build/storage.md`
- `team/standards/build/measures.md`
- `team/knowledge-base/data-architecture/architecture.md`
