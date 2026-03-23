# Open Reporting — Workflow

## The Three-Layer System

```
Claude.ai          →    Linear         →    Claude Code
(ideas, design,         (tasks, issues,      (implementation,
 concepts, research)     backlog, specs)       data, charts, infra)
```

### Claude.ai (Brainstorm & Design)
- Explore new domains and data sources
- Design dashboard layouts and stories
- Draft articles and social content
- Plan features and product direction
- Research data availability

Use Claude.ai project context: paste `docs/PROJECT.md`, `docs/DOMAINS.md`, and relevant `docs/DATA_SOURCES.md` sections.

### Linear (Task Management)
- All implementation tasks live in Linear (`ORE` project)
- Issues created from Claude.ai brainstorm output
- Priority and status managed in Linear
- NOT using GitHub Issues

**Issue format for implementation tasks:**
```
Title: [Domain] Short description
Description:
  - Data source: ...
  - Expected output: ...
  - Acceptance criteria: ...
```

### Claude Code (Implementation)
- Reads Linear issues via MCP (`get_issue ORE-xxx`)
- Implements dashboards, ingestion pipelines, infra changes
- Updates Linear status and adds comments during implementation
- Commits and pushes on completion

## Standard Implementation Flow

1. **Brainstorm** in Claude.ai → decide on a domain/dashboard
2. **Create Linear issue** with data source, expected output, acceptance criteria
3. In Claude Code: `"implement Linear issue ORE-xxx"` → Claude reads it, proposes plan
4. **Approve plan** → Claude implements using DDF (Dashboard Development Framework)
5. **Review output** → approve dashboard HTML
6. **Commit + push** → `/commit` skill

## Dashboard Development Framework (DDF)

All dashboard work follows four stages with approval gates:

1. **Source Research** — confirm data exists, document structure → Gate
2. **Metric Definition** — define KPIs and calculations → Gate
3. **Ingestion** (if needed) — build ETL, validate data → Gate
4. **UI/Presentation** — build chart, apply theme, test → Gate

Do not skip gates. Each gate is a natural checkpoint to course-correct.

## Git Conventions

- Branch: `main` (single-person workflow, no feature branches needed)
- Commit format: `feat:`, `fix:`, `refactor:`, `docs:`, `chore:`
- One logical change per commit
- Push after each completed Linear issue
