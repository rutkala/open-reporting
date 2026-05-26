# Model Delegation Policy

## Why

Opus is the most capable Claude model and also the most expensive. Running all subagent work on Opus burns the token budget on tasks that do not require it — bulk file edits, code formatting checks, data lookups, and mechanical generation are all Sonnet-class work. Reserving Opus for judgment-heavy tasks (architectural critique, statistical soundness review, domain correctness) keeps costs proportionate to the actual cognitive demands of each task. This policy encodes that split as a persistent, enforced default rather than a per-session intention.

## Mechanism A — Per-agent default model

Each subagent file in `.claude/agents/` carries a `model:` field in its YAML frontmatter. When a skill or the lead analyst spawns that agent, it runs at the specified tier without requiring a per-call override.

Current assignments:

| Tier | Agents | Rationale |
|------|--------|-----------|
| `opus` | `architecture-critic`, `analytical-validator`, `domain-specialist` | Judgment-heavy evaluation — catching silent errors in architecture, statistical methods, or domain framing requires the model to hold nuanced trade-offs and detect subtle violations |
| `sonnet` | All other 19 agents (see full list below) | Builders, reviewers, and researchers whose work is directed by explicit KB rules and structured checklists — capable on Sonnet given good prompts |

Full Sonnet roster: `brief-reviewer`, `business-analyst`, `code-reviewer`, `content-reviewer`, `content-writer`, `cost-estimator`, `dashboard-dev`, `data-architect`, `data-engineer`, `data-engineer-reviewer`, `data-researcher`, `data-research-reviewer`, `debug`, `measures-reviewer`, `ops-engineer`, `ops-reviewer`, `researcher`, `research-reviewer`, `visual-screenshot-reviewer`.

To change an agent's tier, edit the `model:` line in `.claude/agents/<agent-name>.md`. Valid values: `opus`, `sonnet`, `haiku`.

## Mechanism B — Skill-level delegation pattern

Lifecycle skills (`plan`, `review`, `develop`, etc.) should explicitly name the model when spawning execution subagents. The pattern:

```
Spawn the data-engineer subagent (model: sonnet) to implement the ingestion script.
```

This makes the cost intent visible in the skill definition rather than implicit. It also decouples the spawned agent's tier from whatever model the parent orchestrator happens to be running on. Any skill step that is mechanical, bulk, or fully specified by a checklist is a candidate for explicit Sonnet delegation.

## Mechanism C — Execution heuristic

When deciding whether to delegate a task to a subagent and at what tier, apply these three rules:

- **Delegate to a Sonnet subagent** when: the task is mechanical or rule-following, the output is bulk (more than ~2K tokens), the task can be fully specified without access to the full conversation context, and subagent boot overhead is worth the savings.
- **Do inline with direct tool use, no subagent** when: the task is a quick lookup or small edit (under ~1K tokens), the overhead of spawning a subagent exceeds the cost savings, and the result feeds immediately into the next step.
- **Stay in the Opus orchestrator** when: the task is architectural or judgment-laden, it requires the full conversation context, it involves design decisions the PO will challenge, or it is short enough that delegation overhead dominates.

These heuristics are not rules — apply judgment. The goal is to avoid running Opus on tasks a cheaper model can handle given a clear spec.

## Tier table with rationale

| Tier | Agents | Why this tier |
|------|--------|---------------|
| `opus` | `architecture-critic` | Must evaluate layer contracts, coupling risks, and schema design trade-offs without being led by the plan's framing. Requires independent structural reasoning. |
| `opus` | `analytical-validator` | Must detect misleading aggregations, spurious causality, and statistical framing errors that look correct on the surface. Silent errors here corrupt every downstream chart. |
| `opus` | `domain-specialist` | Must evaluate whether KPIs, benchmarks, and framing are appropriate for a specific economic domain — requires deep contextual knowledge of Polish fiscal/labour/demographic data. |
| `sonnet` | Builder agents (`data-engineer`, `dashboard-dev`, `content-writer`, `data-architect`, `ops-engineer`, `researcher`, `business-analyst`, `data-researcher`) | Work is directed by explicit KB rules and structured checklists. Produces deterministic outputs from clear specs. |
| `sonnet` | Reviewer agents (`code-reviewer`, `brief-reviewer`, `content-reviewer`, `data-engineer-reviewer`, `data-research-reviewer`, `measures-reviewer`, `ops-reviewer`, `research-reviewer`, `visual-screenshot-reviewer`) | Apply rule-based checklists from `reviewing.md` files. Findings are P1/P2/P3-classified against explicit criteria. |
| `sonnet` | Utility agents (`debug`, `cost-estimator`) | Diagnostic and estimation work guided by structured investigation steps — no open-ended judgment required. |
