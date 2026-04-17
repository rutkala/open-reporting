---
name: architecture
description: "Architecture artifact. Defines what a design document's backend architecture section is — data model, semantic layer, API contracts, and data flow from source to product."
user-invocable: false
---

# Architecture

The architecture artifact is the backend section of the design document. It specifies
the complete data layer: warehouse schema, dbt models, semantic layer, API endpoints,
and data flow. The build step implements this exactly.

Produced by: `/design` (backend section)
Consumed by: `/build` (`data-engineer` agent)

---

## Location

Embedded in: `products/domain-briefs/{domain}/design.md` (backend section)
Or standalone: `products/domain-briefs/{domain}/architecture.md`

---

## Structure

**Dashboard products (DuckDB + dbt + MetricFlow):**
1. **Data flow** — source → raw → curated → gold mart → semantic layer → dashboard
2. **Gold mart schema** — `curated.mart_{domain}`: tables, columns, types, grain
3. **dbt models** — new models required: name, purpose, source tables, grain
4. **MetricFlow semantic model** — entities, dimensions, measures
   - Each measure: name (English), Polish label, aggregation type, SQL, edge cases
   - Measures on fact tables only
5. **Data gaps** — indicators required but not yet in warehouse (flag for ingestion)
6. **Dependencies** — ingestion jobs or models that must exist first

**Portal / mobile products (PostgreSQL + API):**
1. **Schema** — tables, columns, types, constraints, indexes
2. **API endpoints** — route, method, request/response shape, auth
3. **Data flow** — client → API → PostgreSQL

---

## Quality criteria

- Every table and column has a clear purpose
- Grain documented for every fact table
- No measures on dimension tables
- All source tables referenced exist in the warehouse
- Data gaps explicitly flagged — never assumed to exist

---

## Standards

- `team/standards/build/storage.md`
- `team/standards/build/measures.md`
- `team/standards/build/processing.md`
- `team/knowledge-base/data-architecture/architecture.md`
- Reviewed by: `architecture-critic` agent
