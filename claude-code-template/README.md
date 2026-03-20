# Claude Code Universal Template

A production-ready `.claude/` setup you can drop into **any project** to get subagents, session memory, hooks, a real-time activity dashboard, and slash commands working immediately.

Built from a battle-tested setup used daily on a multi-service warehouse management system (3 repos, 7 agents, 10+ skills, thousands of delegations).

---

## What This Gives You

| Feature | What It Does |
|---------|-------------|
| **Session Memory** | Claude remembers what happened last session — auto-injected, enforced on exit |
| **Subagents** | Specialized workers (backend, frontend, debug, etc.) that Claude delegates to in parallel |
| **Agent Activity Dashboard** | Real-time web UI at localhost:5555 showing live agent timers, results, and history |
| **Slash Commands** | `/commit`, `/review`, `/test`, `/plan`, `/deps`, `/batch-audit`, `/document`, `/scaffold`, `/mobile-audit`, `/status-check` |
| **Hooks** | 5 automated behaviors: memory injection, push detection, session enforcement, activity logging |
| **Agent Memory** | Each agent builds up its own persistent knowledge about your project over time |

---

## Prerequisites

- **Claude Code CLI** installed and working (`claude` command available)
- **Node.js** 18+ (hooks and dashboard are plain Node.js, zero dependencies)
- A **git repository** (hooks track git operations)

---

## First-Time Setup (10 minutes)

### Step 1 — Copy the template into your project

```bash
# From wherever you downloaded/cloned this template:
cp -r .claude/  /path/to/your-project/.claude/
cp CLAUDE.md    /path/to/your-project/CLAUDE.md
```

Or if you're already in your project:
```bash
# Windows
xcopy /E /I "C:\path\to\claude-code-template\.claude" ".claude"
copy "C:\path\to\claude-code-template\CLAUDE.md" "CLAUDE.md"

# macOS/Linux
cp -r /path/to/claude-code-template/.claude .claude
cp /path/to/claude-code-template/CLAUDE.md CLAUDE.md
```

### Step 2 — Customize CLAUDE.md

Open `CLAUDE.md` and fill in the sections marked with `{PLACEHOLDERS}` and `<!-- CUSTOMIZE -->` comments:

1. **Replace `{PROJECT_NAME}`** everywhere (find & replace)
2. **See `CLAUDE.example.md`** for a fully filled-in reference (a hypothetical "TaskFlow" project). Delete this file once you've filled in your own `CLAUDE.md`.
4. **System Architecture** — list your directories and services
5. **Custom Subagents table** — uncomment and fill in the agents you created
6. **Development Environment** — your `npm run dev`, `docker-compose up`, etc.
7. **Project-specific sections** at the bottom — DB, auth, API format, inter-service communication

These sections are what make Claude understand YOUR project. The more detail you put here, the better Claude's decisions will be.

### Step 3 — Create your domain agents

The template includes `_template-domain.md` and `_template-feature.md` as starting points. Copy and customize them for your project structure:

```bash
cd .claude/agents/

# Example: a backend agent for a Node.js API
cp _template-domain.md backend.md

# Example: a frontend agent for a React app
cp _template-domain.md frontend.md

# Example: a cross-cutting feature agent
cp _template-feature.md feature.md
```

For each agent file, edit the YAML frontmatter and body:

```yaml
---
name: backend                    # Must match the filename (without .md)
description: "Backend specialist for the Express.js API server."
tools: Read, Edit, Write, Bash, Grep, Glob   # What tools it can use
model: sonnet                    # sonnet (fast/cheap) or opus (smart/expensive)
memory: project                  # Always keep this — enables agent memory
maxTurns: 30                     # Max back-and-forth before agent stops
---
```

**Key decisions per agent:**
- `tools` — Remove `Edit, Write` to make it read-only. Remove `Bash` to prevent shell commands.
- `model` — Use `sonnet` for most agents, `opus` for complex reasoning, `haiku` for bulk/simple work
- `permissionMode: plan` — Makes the agent truly read-only (like the `debug` agent)
- `isolation: worktree` — Gives the agent its own git worktree so changes are isolated
- `maxTurns` — 30 is good for focused tasks, 50 for large features

### Step 4 — Register agent colors (optional but nice)

Open `.claude/hooks/log-subagent.js` and add your agents to `DEFAULT_MODELS` and `AGENT_COLORS`:

```javascript
const DEFAULT_MODELS = {
  'backend':  'sonnet',
  'frontend': 'sonnet',
  'debug':    'sonnet',
  // Add your agents here
};

const AGENT_COLORS = {
  'backend':  '#3b82f6',  // blue
  'frontend': '#10b981',  // green
  'debug':    '#a855f7',  // purple
  // Add your agents here — these colors show in the dashboard
};
```

### Step 5 — Add permissions for your project's tools

Open `.claude/settings.local.json` and add permissions for your project's specific commands:

```json
{
  "permissions": {
    "allow": [
      // ... existing git/node permissions (already included) ...

      // ADD YOUR PROJECT-SPECIFIC PERMISSIONS:
      "Bash(docker-compose:*)",
      "Bash(python:*)",
      "Bash(cargo:*)",
      "Bash(go:*)",
      "Bash(make:*)",
      "Bash(pytest:*)"
    ]
  }
}
```

The template includes safe defaults for git, node, npm. Add whatever your project needs.

### Step 6 — Configure languages

Open `.claude/languages.json` and set your project's languages:

```json
{
  "agent_language": "English",
  "content_languages": ["English", "Polish"],
  "primary_content_language": "English",
  "documentation_language": "English",
  "style_notes": {
    "English": "Professional register. British English spelling.",
    "Polish": "Formal register (Pan/Pani). Proper diacritics."
  }
}
```

This controls:
- What language Claude responds in (`agent_language`)
- Which languages the translate agent generates (`content_languages`)
- What language `/document` writes docs in (`documentation_language`)
- Spelling and register rules per language (`style_notes`)

If your project is English-only, you can leave the defaults or delete the file entirely.

### Step 7 — Make the dashboard scripts executable (macOS/Linux only)

```bash
chmod +x .claude/watch-agents.sh
chmod +x .claude/watch-agents-ui.js
```

### Step 8 — Git: decide what to commit

**Recommended .gitignore additions:**
```gitignore
# Claude Code runtime files (don't commit)
.claude/agent-activity.log
.claude/agent-activity.jsonl
.claude/.agent-timers/
.claude/.session-pushed
.claude/.lead-last-log
.claude/.hook-errors.log
```

**DO commit:**
- `.claude/hooks/` — everyone on the team gets the same automation
- `.claude/agents/` — shared agent definitions
- `.claude/skills/` — shared slash commands
- `.claude/settings.local.json` — shared hook wiring and permissions
- `.claude/session-memory.md` — shared session context
- `.claude/watch-agents-ui.js` — shared dashboard
- `CLAUDE.md` — shared project instructions

### Step 9 — Test it

```bash
cd your-project

# Start Claude Code
claude

# Test session memory — you should see "Session Memory (auto-loaded)" in context
# Test a slash command:
> /status-check

# In a separate terminal, launch the dashboard:
# Windows:
.claude\watch-agents-ui.bat
# macOS/Linux:
node .claude/watch-agents-ui.js

# Now ask Claude to do something that triggers an agent delegation
# and watch it appear in the dashboard in real time
```

---

## How Everything Works Together

### The Session Memory Loop

```
┌─────────────────────────────────────────────────┐
│ 1. You start a conversation                     │
│    → SessionStart hook fires                    │
│    → inject-session-memory.js reads             │
│      .claude/session-memory.md                  │
│    → Content injected as additionalContext       │
│    → Claude starts with full context of          │
│      what happened in previous sessions          │
├─────────────────────────────────────────────────┤
│ 2. You work with Claude                         │
│    → Context gets long, auto-compaction fires   │
│    → PostCompact hook re-injects session memory │
│    → Claude never loses session context          │
├─────────────────────────────────────────────────┤
│ 3. You push code                                │
│    → detect-git-push.js sets .session-pushed    │
│      flag file                                   │
├─────────────────────────────────────────────────┤
│ 4. Conversation ends                            │
│    → Stop hook checks: was code pushed?         │
│    → If yes: was session-memory.md updated       │
│      in last 5 min?                              │
│    → If no: BLOCKS and reminds Claude to update  │
│    → If yes: clears flag, allows stop            │
│    → Prevents "amnesia" between sessions         │
└─────────────────────────────────────────────────┘
```

### The Agent Delegation Flow

```
┌──────────────────────────────────────────────────┐
│ 1. Claude decides to delegate a task             │
│    → PreToolUse:Agent hook fires                 │
│    → log-subagent.js writes DELEGATE entry       │
│      to .log (terminal) + .jsonl (dashboard)     │
│    → Starts timer for the agent                  │
│                                                  │
│ 2. Agent works (may spawn in parallel)           │
│    → Dashboard shows live timer + task desc      │
│    → Terminal log shows "▶ DELEGATE"             │
│                                                  │
│ 3. Agent completes                               │
│    → SubagentStop hook fires                     │
│    → log-subagent.js writes REPORT entry         │
│      with duration + result summary              │
│    → Dashboard updates: ✓ done, shows result     │
│    → Terminal log shows "✓ REPORT"               │
└──────────────────────────────────────────────────┘
```

### The Lead Activity Bar

While Claude (the orchestrator) is working solo (not delegating), the `log-lead.js` hook tracks what tools it's using — Reading files, Editing, Running commands, Searching. This shows up as a thin amber bar in the dashboard so you always know what Claude is doing.

Throttled to max 1 entry per 2 seconds to avoid flooding.

---

## Daily Usage

### Starting a session
Just open Claude Code in your project. Session memory loads automatically. You'll see the previous session's context without doing anything.

### Watching agents work
Open the dashboard in a separate terminal before starting work:
```bash
# Windows — double-click or run:
.claude\watch-agents-ui.bat

# macOS/Linux:
node .claude/watch-agents-ui.js
```
Leave it open in a browser tab. It auto-updates via SSE (no polling, no refresh needed).

### Using slash commands

```
/commit                    — Analyze changes, generate conventional commit message
/commit fix auth bug       — Same but with a hint for the message
/review                    — Code review all uncommitted changes
/review server             — Code review only server/ changes
/test                      — Run tests for recently changed files
/test all                  — Run the full test suite
/test auth                 — Run tests matching "auth" pattern
/test --coverage           — Run with coverage reporting
/plan add user avatars     — Design implementation plan before coding
/deps                      — Full dependency audit (outdated + security + unused)
/deps security             — Check for known vulnerabilities only
/batch-audit security      — Spawn 3-8 parallel agents to audit security
/batch-audit missing auth  — Audit all routes for missing auth middleware
/document                  — Full codebase scan → generates 17+ docs in docs/
/document update           — Re-scan changed files, update existing docs only
/document api              — Regenerate just the API documentation
/scaffold route users      — Scaffold a new API route file matching project patterns
/scaffold page Settings    — Scaffold a new frontend page component
/scaffold service billing  — Scaffold a new service/business logic class
/mobile-audit              — Audit all pages for mobile responsiveness issues
/mobile-audit LoginPage    — Audit just one component
/status-check              — Quick diagnostic of git state + running processes
```

### How Claude uses agents

You don't need to tell Claude which agent to use. The orchestrator (CLAUDE.md) contains delegation rules that tell Claude:
- Backend-only changes → `backend` agent
- Frontend-only changes → `frontend` agent
- Bug investigation → `debug` agent (safe, read-only)
- Cross-cutting features → `feature` agent
- etc.

Claude reads the task, picks the right agent, and delegates. You see it happen in real time on the dashboard.

### Ending a session
If you pushed code during the session, Claude will automatically update session memory before stopping. If you didn't push, it stops normally. Either way, next session starts with full context.

---

## The `/document` Command

The most powerful skill in the template. Run `/document` and Claude will:

1. Scan every file in the repo (parallelised with agents on large codebases)
2. Produce a complete `docs/` folder with 17+ standardised documents
3. Keep a `docs/CHANGELOG.md` and `docs/INDEX.md` up to date

### What it generates

```
docs/
├── INDEX.md            ← Master index + "how to keep docs in sync" checklist
├── CHANGELOG.md        ← Change log for all doc updates
├── INVENTORY.md        ← Full file inventory: path, purpose, exports, consumers
├── ARCHITECTURE.md     ← Modules, layers, dependencies, Mermaid diagrams
├── SETUP.md            ← Local setup, tools, env vars, migrations, pitfalls
├── BUILD_DEPLOY.md     ← CI/CD, build commands, environments, smoke tests
├── DEPENDENCIES.md     ← Runtime deps with purpose, security notes
├── API.md              ← Every route: method, path, auth, body, response, examples
├── DATA_MODEL.md       ← DB schema, relations, indexes, ERD diagrams
├── CONFIG.md           ← Env vars, config files, feature flags, precedence
├── ERRORS_LOGGING.md   ← Error classes, logging formats, retry logic
├── TESTING.md          ← How to run tests, coverage, mocking, fixtures
├── SECURITY.md         ← AuthN/AuthZ, secrets, validation, XSS/CSRF/SQLi
├── PERFORMANCE.md      ← Bottlenecks, caching, pagination, optimisations
├── FRONTEND_GUIDE.md   ← Routing, state, API consumption (if frontend exists)
├── OPERATIONS.md       ← Runbooks: outages, backups, key rotations
├── CONTRIBUTING.md     ← Branching, commit style, PR checklist, code style
└── GLOSSARY.md         ← Domain-specific terminology
```

### Three modes

| Command | What it does |
|---------|-------------|
| `/document` | Full scan — reads every file, generates all 17+ docs from scratch |
| `/document update` | Incremental — re-scans changed files, updates affected docs only |
| `/document api` | Single section — regenerates just that one document |

### Rules it follows
- **No hallucination** — only documents what's confirmed in code
- **Secrets redacted** — only variable names, never values
- **Cross-linked** — docs reference each other and point to source files
- **Mermaid diagrams** — architecture flows, ERDs, request lifecycles
- **Backend first** — if both exist, documents APIs before frontend
- **Parallel scanning** — delegates to multiple agents on large codebases

---

## What's Included (Full Reference)

### Hooks (100% universal — zero changes needed)

| Hook | Event | Purpose |
|------|-------|---------|
| `inject-session-memory.js` | SessionStart, PostCompact | Auto-loads session memory into every conversation |
| `check-session-memory.js` | Stop | Blocks ending if you pushed code but didn't update memory |
| `detect-git-push.js` | PostToolUse:Bash | Sets flag when `git push` happens |
| `log-subagent.js` | PreToolUse:Agent, SubagentStop | Logs agent spawn/complete to `.log` + `.jsonl` |
| `log-lead.js` | PreToolUse:* | Logs lead orchestrator tool usage (throttled) |

### Agent Activity Dashboard

Zero-dependency Node.js web server. Features:
- Real-time SSE updates (no polling)
- "Currently Working" panel with live per-agent timers
- Full timeline with date filtering (Today / Yesterday / All)
- Stat filtering (All / Active / Completed)
- Auto-expire stale agents after 10 minutes
- Click-to-expand result text
- Lead agent activity bar (shows what the orchestrator is doing solo)

### Skills (Slash Commands)

| Skill | Universal? | Description |
|-------|-----------|-------------|
| `/commit` | 100% | Smart conventional commit with diff analysis |
| `/test` | 100% | Detect test framework, run tests, analyse failures |
| `/plan` | 100% | Design implementation plan before coding, get approval |
| `/deps` | 100% | Audit dependencies: outdated, vulnerabilities, unused |
| `/batch-audit` | 100% | Parallel read-only audit with multiple agents |
| `/document` | 100% | Full codebase documentation generator — 17+ docs in `docs/` |
| `/scaffold` | 100% | Scaffold new files (route, page, component, service, model, job, test) |
| `/mobile-audit` | 100% | Mobile/PWA responsiveness audit with fix suggestions |
| `/review` | Template | Code review — customize the checklist section |
| `/status-check` | Template | System diagnostic — customize the commands |
| `_template-auto-triggered` | Template | Pattern for auto-triggered background knowledge skills |

### Agents

| Agent | Universal? | Description |
|-------|-----------|-------------|
| `debug` | 100% | Read-only diagnostic agent (plan mode, cannot edit files) |
| `_template-domain` | Template | Copy and customize for each domain (backend, frontend, etc.) |
| `_template-feature` | Template | Copy for cross-cutting features spanning multiple directories |
| `_template-translate` | Template | Copy for i18n/translation work (scan, add keys, wire calls) |
| `_template-mobile` | Template | Copy for mobile/PWA optimization (responsive, touch, viewport) |

### Session Memory

- `.claude/session-memory.md` — shared across all agents, persists across conversations
- Auto-injected at conversation start + after context compaction
- Enforced on stop (after git push)
- 100-line limit with rolling history

### Agent Memory

- `.claude/agent-memory/<name>/` — per-agent persistent memory
- Each agent with `memory: project` auto-creates and maintains its own knowledge base
- Learns patterns, shortcuts, and domain knowledge over time

---

## File Structure

```
your-project/
├── CLAUDE.md                          ← Project instructions (customize)
├── CLAUDE.example.md                  ← Filled-in example (delete after setup)
└── .claude/
    ├── settings.local.json            ← Permissions + hook wiring
    ├── languages.json                 ← Language config (agent output + content languages)
    ├── session-memory.md              ← Cross-session memory (auto-populated)
    │
    ├── hooks/                         ← All universal, no changes needed
    │   ├── inject-session-memory.js   ← SessionStart + PostCompact
    │   ├── check-session-memory.js    ← Stop (enforces memory update)
    │   ├── detect-git-push.js         ← PostToolUse:Bash (tracks pushes)
    │   ├── log-subagent.js            ← PreToolUse:Agent + SubagentStop
    │   └── log-lead.js               ← PreToolUse:* (lead activity)
    │
    ├── .gitignore                     ← Ignores runtime files (logs, timers)
    │
    ├── agents/                        ← Templates + debug
    │   ├── debug.md                   ← Universal read-only diagnostics
    │   ├── _template-domain.md        ← Copy for each domain agent
    │   ├── _template-feature.md       ← Copy for cross-cutting agent
    │   ├── _template-translate.md     ← Copy for i18n/translation agent
    │   └── _template-mobile.md        ← Copy for mobile/PWA agent
    │
    ├── skills/
    │   ├── commit/SKILL.md            ← /commit — universal
    │   ├── test/SKILL.md              ← /test — universal (auto-detects framework)
    │   ├── plan/SKILL.md              ← /plan — universal (design before code)
    │   ├── deps/SKILL.md              ← /deps — universal (outdated/security/unused)
    │   ├── batch-audit/SKILL.md       ← /batch-audit — universal
    │   ├── document/SKILL.md          ← /document — universal (17+ docs)
    │   ├── scaffold/SKILL.md          ← /scaffold — universal file scaffolding
    │   ├── mobile-audit/SKILL.md      ← /mobile-audit — universal PWA audit
    │   ├── review/SKILL.md            ← /review — customize checklist
    │   ├── status-check/SKILL.md      ← /status-check — customize commands
    │   └── _template-auto-triggered/  ← Pattern for background knowledge skills
    │
    ├── agent-memory/                  ← Auto-populated by agents
    │
    ├── watch-agents-ui.js             ← Web dashboard server
    ├── watch-agents-ui.bat            ← Windows launcher (double-click)
    ├── watch-agents.bat               ← Terminal watcher (Windows)
    └── watch-agents.sh                ← Terminal watcher (macOS/Linux)
```

---

## Project Type Examples

### Monorepo (backend + frontend + jobs)
```
.claude/agents/
├── backend.md    → scope: server/, tools: all, model: sonnet
├── frontend.md   → scope: client/, tools: all, model: sonnet
├── data.md       → scope: jobs/, tools: all, model: sonnet
├── feature.md    → scope: all, isolation: worktree, maxTurns: 50
└── debug.md      → scope: all, read-only
```

### Single app (e.g., a Django or Rails project)
```
.claude/agents/
├── models.md     → scope: app/models/, tools: all
├── views.md      → scope: app/views/ + templates/, tools: all
├── api.md        → scope: api/, tools: all
└── debug.md      → scope: all, read-only
```

### Microservices
```
.claude/agents/
├── auth-service.md    → scope: services/auth/
├── billing-service.md → scope: services/billing/
├── gateway.md         → scope: services/gateway/
├── feature.md         → scope: all, isolation: worktree
└── debug.md           → scope: all, read-only
```

### Simple project (no subagents needed)
Just use `CLAUDE.md` + hooks + skills. No agents required. The hooks and slash commands work standalone:
```
.claude/
├── hooks/          ← Session memory + logging still works
├── skills/         ← /commit, /review still work
└── session-memory.md
```

---

## Customization Guide

### Adding a new domain agent

1. Copy `.claude/agents/_template-domain.md` → `.claude/agents/{name}.md`
2. Fill in the YAML frontmatter: `name`, `description`, `tools`, `model`
3. Fill in the body: scope, patterns, domain knowledge
4. Add the agent to the table in `CLAUDE.md`
5. Optionally add a color in `log-subagent.js` → `AGENT_COLORS` (for dashboard)

### Adding a translate agent

1. Copy `.claude/agents/_template-translate.md` → `.claude/agents/translate.md`
2. Fill in the `## i18n Setup` section (library, locale file paths, key naming)
3. Fill in `## Supported Languages` and `## Dictionary Location`
4. If your project has lots of files to scan, set `model: haiku` for speed/cost

### Adding a mobile agent

1. Copy `.claude/agents/_template-mobile.md` → `.claude/agents/mobile.md`
2. Update the breakpoint values to match your CSS framework
3. Add any project-specific CSS utility classes to reference

### Adding an auto-triggered skill

Auto-triggered skills are background knowledge that Claude loads automatically when it detects relevant work (NOT slash commands).

1. Copy `.claude/skills/_template-auto-triggered/SKILL.md` → `.claude/skills/{name}/SKILL.md`
2. Set `user-invocable: false` in frontmatter
3. Write the `description:` with trigger keywords so Claude knows when to load it
4. Fill in conventions, patterns, and code examples
5. Add it to the auto-triggered table in `CLAUDE.md`

Examples of useful auto-triggered skills:
- **API conventions** — response format, error handling, auth patterns
- **Database patterns** — query style, ORM conventions, migration format
- **Testing patterns** — framework, mocking strategy, fixture conventions
- **Component conventions** — file structure, prop patterns, state management

### Adding a new slash command

1. Create `.claude/skills/{name}/SKILL.md`
2. Add YAML frontmatter with `user-invocable: true`
3. Use `$ARGUMENTS` to accept user input
4. Optionally set `agent: {name}` to fork to a specific agent
5. Optionally set `context: fork` to run in a separate context
6. Add the skill to the slash commands table in `CLAUDE.md`

### Customizing the review checklist

Edit `.claude/skills/review/SKILL.md` — find the `{PROJECT-SPECIFIC CHECKLIST}` section and add your project's specific checks (e.g., translation keys, migration files, socket event names).

---

## Troubleshooting

### Session memory not loading
- Check that `.claude/session-memory.md` exists and has content
- Check that `settings.local.json` has the `SessionStart` hook configured
- Run `node .claude/hooks/inject-session-memory.js < /dev/null` to test — should output JSON or exit silently

### Dashboard not showing agents
- Check that `.claude/agent-activity.jsonl` exists (created on first agent delegation)
- Check that `settings.local.json` has both `PreToolUse:Agent` and `SubagentStop` hooks
- Check port 5555 is not in use: `netstat -an | grep 5555`

### Agent not delegating
- Check the agent `.md` file has valid YAML frontmatter (the `---` fences must be exact)
- Check the `name:` in frontmatter matches what Claude is trying to delegate to
- Check `tools:` lists the tools the agent needs (e.g., `Edit` for making changes)

### Stop hook blocking unexpectedly
- The stop hook only blocks if `.claude/.session-pushed` exists AND `session-memory.md` wasn't updated in the last 5 minutes
- To unblock: update session-memory.md, or delete `.claude/.session-pushed`
- The hook has infinite-loop prevention — it only blocks once

### Hooks not firing
- Hooks require Node.js in your PATH
- Hooks read JSON from stdin — they fail silently if stdin is invalid
- Check `.claude/.hook-errors.log` for any logged errors
