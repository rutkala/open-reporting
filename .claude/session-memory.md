# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-03-23 -->

## Current Focus
Reviewing and refining `.claude/` config file by file. Next: review `CLAUDE.md`.

## Last Session Summary
Full review and redesign of `.claude/` configuration:
- Removed all agents except `debug` — start lean, add back when codebase warrants it
- Removed `agent-memory/` empty folder
- Set Polish as primary content language (English for agent communication)
- Fixed hook model names (sonnet), updated agent colours for dashboard-dev/data-engineer
- Renamed `/linear` skill to `/kickoff` (tool-agnostic naming)
- Built complete skill workflow: `/kickoff` → `/research` → `/plan` → implement → `/review` → `/commit` → `/document`
- All gates now present in plain business language — product owner approves deliverables, not code
- `/commit` now prompts memory update + Linear issue close after each commit
- Moved `renew-certs.sh` to `nginx/`, removed empty `charts/` folder, deleted `AGENTS.md` and `claude-code-template/`

## Recent Changes
- 2026-03-23: Claude Code environment set up from scratch
- 2026-03-23: `.claude/` config reviewed and redesigned — skills, hooks, agents, languages

## Open Items
- Review and update `CLAUDE.md` (next step)
- Review `docs/` folder
- Add agent threshold note: create `dashboard-dev` + `data-engineer` agents when 3+ dashboards or pipelines exist and context fills up
- Choose first domain/dashboard from Linear backlog
- DB schemas not yet created
- Ghost CMS live but no articles published
