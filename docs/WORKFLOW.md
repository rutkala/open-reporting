# Open Reporting — Workflow

> For the full post-MVP project management process including Git workflow, PR reviews, and release process, see `docs/CONTRIBUTING.md`.

---

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
- 2-week sprint cycles

**Issue must meet Definition of Ready** (see `.claude/standards/requirements.md`) before work starts.

### Claude Code (Implementation)
- Reads Linear issues via MCP (`/kickoff ORE-XXX`)
- Creates feature branch, implements, runs `/review`
- Updates Linear status and adds comments during implementation
- Opens PR on GitHub — never pushes directly to `main`

---

## Standard Implementation Flow

1. **Brainstorm** in Claude.ai → decide on a feature/domain
2. **Create Linear issue** meeting Definition of Ready
3. In Claude Code: `/kickoff ORE-XXX` → Claude reads it, proposes plan
4. **Approve plan** → Claude creates feature branch and implements
5. **Review**: `/review` → Claude checks standards compliance
6. **PR** → open on GitHub, paste review output, get approval
7. **Merge to main** → Linear issue → Done → update `RELEASE_NOTES.md`

---

## Git Conventions

- **Branching**: feature branches required for all work (see `CONTRIBUTING.md`)
- Branch format: `feat/ORE-XXX-description`, `fix/ORE-XXX-description`, etc.
- Commit format: `feat: ORE-123 description` / `fix:` / `refactor:` / `docs:` / `chore:`
- One logical change per commit
- `main` is always deployable — no direct pushes
