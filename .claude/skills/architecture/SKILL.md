---
name: architecture
description: "Produce an architecture design for a dashboard. Defines data model, data flow, dashboard components, and KPI calculation logic. Called from /dashboard Step 4."
user-invocable: false
---

# Architecture Design

Produces a system design that specifies how the dashboard will be built — data layer,
component structure, and calculation logic. This document drives both the data pipeline
work and the dashboard code in subsequent steps.

## Inputs

- Requirements document from Step 3
- Domain brief from Step 2

## Standards and knowledge

- Read `team/standards/build/storage.md` for schema naming and data model patterns
- Read `team/standards/build/measures.md` for KPI calculation conventions
- Read `team/knowledge-base/data-architecture/architecture.md` for medallion patterns

## Agents

- **data-engineer** — data model, warehouse schema, dbt model structure, KPI calculations
- **dashboard-dev** — dashboard component inventory, chart-to-data mapping

These can run in parallel once requirements are confirmed.

## Mandatory sections

### 1. Data Model
- Source tables required (raw schema)
- Curated tables to be built (schema, grain, key fields)
- Gold mart if needed: `curated.mart_{domain}` — columns, calculated fields
- Any new dbt models required

### 2. Data Flow
Diagram (text) showing: source → ingestion → raw → curated → gold → dashboard

### 3. KPI Calculation Logic
For each KPI from the requirements document:
- SQL expression or dbt metric definition
- Denominator/numerator if a ratio
- Aggregation method (sum, avg, last value, YoY delta)
- Any edge cases (division by zero, null handling)

### 4. Component Inventory
Complete list of every component in the dashboard:
- Charts: type, data source, x-axis, y-axis, series, filters applied
- KPI cards: metric, format, comparison reference
- Filters: field, type (dropdown/slider/date), scope (page or global)
- Pages: name, purpose, components on it

### 5. Dependencies
- Ingestion jobs that must exist or be created
- dbt models that must exist or be created
- Any external data sources not yet in warehouse

## Evaluator

Spawn **architecture-critic** with the design document as input.
- BLOCK → fix P1 issues before proceeding
- CONDITIONAL → note P2 findings, proceed with caveats
- PASS → proceed

## Output

Save as a markdown file on the feature branch. Present to PO for approval.
