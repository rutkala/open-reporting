---
name: batch-audit
description: "Run a parallel read-only audit across the codebase using multiple simultaneous agents. Each agent analyzes a scoped subset of files and returns findings. Results are combined into a single report. Use for broad codebase analysis: missing patterns, security gaps, code quality, etc."
user-invocable: true
argument-hint: "<what to audit>"
disable-model-invocation: true
---

# Batch Audit

You are orchestrating a **parallel read-only audit** of the codebase. You will spawn multiple debug agents simultaneously, each scoped to a different part of the codebase, then combine their findings into one report.

## Audit Task

**What to find:** $ARGUMENTS

## Step 1 — Determine Scope

Based on the audit task, decide which directories/files to split across agents. Common patterns:

| Audit Type | Split By |
|------------|----------|
| Route/API patterns | One agent per route file |
| Component patterns | One agent per subdirectory |
| Job/worker patterns | One agent per job file |
| Cross-service pattern | One agent per top-level service |

Aim for **3-8 agents** — enough to parallelize meaningfully without excessive overhead.

## Step 2 — Spawn Parallel Agents

Spawn ALL agents in a **single message** (parallel execution). Each agent must be:
- **Read-only** — Glob, Grep, Read, Bash(grep:*) only. NO Edit, Write, or any mutating tools.
- **Scoped** — given a specific list of files or directories to check
- **Structured output** — instructed to return findings in a consistent format

### Agent Prompt Template

Give each agent this prompt (customized for its scope):

```
You are a READ-ONLY audit agent. DO NOT edit any files.

Audit task: [WHAT TO FIND]
Your scope: [SPECIFIC FILES OR DIRECTORY]

For each file in your scope:
1. Read the file
2. Check for: [SPECIFIC PATTERN OR CONDITION]
3. Report findings

Return your findings in this exact format:

## [Agent Scope Name]

### Files Checked
- file/path.js — [PASS / ISSUE FOUND]

### Issues Found
- **[file:line]** — [description of issue]
  ```
  [relevant code snippet]
  ```

### Summary
X files checked, Y issues found.
```

## Step 3 — Combine Results

After ALL agents complete, compile their findings into one report:

```
# Batch Audit Report
**Task:** [what was audited]
**Date:** [today]
**Agents run:** [N]

## Executive Summary
- Total files checked: X
- Total issues found: Y
- Directories affected: [list]

## Findings by Agent

[paste each agent's output here]

## Priority Issues
List the top issues that need immediate attention, sorted by severity:
1. CRITICAL — [file:line] description
2. WARNING  — [file:line] description
3. INFO     — [file:line] description

## Recommended Next Steps
- [ ] [specific action 1]
- [ ] [specific action 2]
```

## Rules

- **Never edit files.** This is analysis only.
- **Always spawn agents in parallel** (single message, multiple Agent tool calls).
- **Scope each agent tightly** — overlapping scopes waste tokens.
- **If $ARGUMENTS is vague**, ask one clarifying question before spawning agents.
- If a finding is critical (security, data leak, broken auth), highlight it prominently.
