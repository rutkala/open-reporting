# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-03-23 -->

## Current Focus
Setting up Claude Code environment with Linear workflow integration. Setup complete — ready to start first dashboard.

## Last Session Summary
Implemented full Claude Code setup from template:
- Removed OpenCode artifacts (`.opencode/`)
- Copied and customised `.claude/` (minimal subset: no watch-agents-ui, no stop-hook enforcement)
- Created `CLAUDE.md` (lead architect instructions, Linear workflow, subagents table)
- Created domain agents: `dashboard-dev.md` (DDF stages) and `data-engineer.md` (ETL patterns)
- Created `docs/` folder: PROJECT.md, DOMAINS.md, DATA_SOURCES.md, WORKFLOW.md, ARCHITECTURE.md
- Slimmed `AGENTS.md` to code standards only (removed OpenCode refs, DDF, agent definitions)
- Configured `settings.local.json`: added `docker compose` and `python3` permissions, removed deleted hooks

## Recent Changes
- 2026-03-23: Claude Code environment set up from scratch

## Open Items
- Choose first domain/dashboard from Linear backlog
- DB schemas not yet created (no ingestion pipelines built yet)
- Ghost CMS live but no articles published
