---
name: dashboard
description: "Build a complete domain dashboard. Orchestrates all mandatory components in sequence. Can be invoked directly or routed from /kickoff."
user-invocable: true
argument-hint: "<optional: OR-123 or domain name e.g. labour-market>"
---

# Dashboard Build

Full pipeline for a domain dashboard. **Mandatory steps in sequence — none can be skipped.**

Before each step: check if the component already exists. If it does, verify it is current. If it does not, produce it.

---

## Step 1 — Initial Request

**If $ARGUMENTS is an OR-XXX issue ID:**
- Fetch the Linear issue: title, description, acceptance criteria, comments
- Extract: domain name, problem statement, target audience, any constraints
- Summarise in plain language what is being requested

**If $ARGUMENTS is a domain name or empty:**
- Enter intake mode. Ask the PO these questions one at a time:
  1. What domain or topic is this dashboard about?
  2. What business problem or question should it answer?
  3. Who will use it — and what decisions will they make with it?
  4. Are there specific KPIs or metrics you know must be included?
  5. Are there any known constraints (data sources, timeline, scope)?
- Summarise the captured request back to PO for confirmation
- Create a Linear issue from the captured request (label: Feature, status: In Progress)

**Gate:** Cannot proceed until initial request is confirmed by PO.

---

## Step 2 — Domain Brief

Check `products/domain-briefs/{domain}.md`.

- **Exists and current:** read it, proceed to Step 3
- **Missing or insufficient:** run `/domain-brief {domain}`

**Gate:** Domain brief must exist before requirements are written.

---

## Step 3 — Requirements

Run `/requirements`.

**Gate:** Present requirements document to PO. Wait for explicit approval before proceeding.
PO may add, remove, or change KPIs, pages, or scope at this point.

---

## Step 4 — Architecture Design

Run `/architecture`.

**Gate:** Present architecture design to PO. Wait for explicit approval before proceeding.

---

## Step 5 — UX/UI Design

Run `/ux-ui`.

No hard gate — runs after Step 4 is approved. PO may review and give feedback
but the build does not wait unless PO explicitly requests changes.

---

## Step 6 — Dashboard Code

Run `/dashboard-code`.

Does not start until Steps 4 and 5 are both complete.

---

## Step 7 — QA

Run `/qa`.

**Gate:** QA must pass before release. Any failures return to Step 6 for fixes.

---

## Step 8 — Release

Run `/release`.

**Gate:** Present release document to PO. Confirm deployment. Close Linear issue → Done.
