# Lessons Learned

A running log of process improvements, recurring mistakes, and things that worked well. Reviewed at the start of `/kickoff` for relevant context.

## Format

```
### YYYY-MM-DD — Short title
**What happened:** What went wrong or what insight emerged.
**Root cause:** Why it happened.
**Process change:** What rule or step was added/changed as a result.
**Applies to:** Which issue types or phases this affects.
```

---

## 2026-03-28 — MVP line drawn at commit 736ab606

**What happened:** MVP v0.1.0 declared complete. All work up to and including commit `736ab606` on `main` is MVP bootstrap — process setup, documentation, Linear issues, skills. This work went directly to `main` without PRs, which is a one-time justified exception.

**Root cause:** The PR process was being established during this work. It would be circular to require PRs for the commits that created the PR requirement.

**Process change:** From commit `736ab606` onwards, the full process is mandatory for all work — no exceptions except explicit agreement with the user:
1. Idea → Linear (Backlog + Idea label)
2. `/review-ideas` → convert to issue
3. `/kickoff` → feature branch → implement → PR → merge

**Applies to:** All future work without exception.

---

## 2026-03-28 — Documentation not tracked during post-MVP cleanup session

**What happened:** A full session of work (Linear docs archived, DOMAINS.md expanded, project description updated, README/ARCHITECTURE rewritten, MVP docs created) was completed without any entries in `RELEASE_NOTES.md` under "Unreleased". The work was invisible in the release history.

**Root cause:** The CONTRIBUTING.md step 8 (Merge) only mentioned updating RELEASE_NOTES.md but did not explicitly list which other docs to check, and did not make the documentation review a named step. It was easy to skip.

**Process change:** Added step 9 (Documentation update) and step 10 (Lessons learned) to CONTRIBUTING.md. Step 9 includes a table mapping change types to the docs that must be reviewed. Step 9 is now a required named step, not a bullet under Merge.

**Applies to:** All issue types — every merge requires a documentation review pass.

---

## 2026-03-28 — Instagram token was for wrong account

**What happened:** First Instagram publish attempt failed — the access token was for the personal account (radoslawutkala) not the business account (@otwarteraporty). Token had to be regenerated after switching the active profile in Meta Developer portal.

**Root cause:** Meta Developer portal defaults to the personal profile. The correct account must be explicitly selected when generating tokens.

**Process change:** Documented in `.claude/playbooks/social.md` — token generation step now specifies "ensure @otwarteraporty is the active profile in Meta Developer before generating".

**Applies to:** Instagram publishing, token refresh (next: ~May 2026).

---

## 2026-03-28 — Instagram image cached by URL

**What happened:** After regenerating the Instagram card with Nordic theme colors, republishing to the same URL (`post_test.png`) showed the old image. Instagram had cached the original.

**Root cause:** Instagram caches media container images by URL. Same filename = same URL = cached image, even if the file content changed.

**Process change:** Documented in `.claude/playbooks/social.md` — always use a unique filename per post. Timestamp or content-based naming recommended.

**Applies to:** Instagram publishing — every post.

---

## 2026-03-28 — Ghost title env var ignored on existing installation

**What happened:** Added `title: Otwarte Raporty` to Ghost environment in docker-compose.yml. After restart, the blog header still showed "Open Reporting".

**Root cause:** Ghost env vars for `title`, `description`, etc. only apply on first install (when the DB is initialised). An existing Ghost installation ignores them — the value is stored in the `settings` table in the Ghost database.

**Process change:** To rename Ghost on an existing install, use Node.js knex query directly against ghost.db:
```bash
docker exec ghost node -e "
  const knex = require('knex')({client:'sqlite3',connection:'/var/lib/ghost/content/data/ghost.db'});
  knex('settings').where({key:'title'}).update({value:'Otwarte Raporty'}).then(()=>process.exit(0));
"
```

**Applies to:** Ghost CMS configuration changes on existing installations.

---

## 2026-03-29 — Research step skipped: data inventory ≠ principles research

**What happened:** OR-97 required researching DW modelling approaches (Kimball, Inmon, Data Vault) before designing the schema. The research subagent catalogued data structure (column names, row counts, source shapes) but never researched DW principles. Implementation proceeded on a generic EAV-like dim1/dim2/dim3 pattern — a known anti-pattern in dimensional modelling — without the user being informed this was a shortcut, not a decision.

**Root cause:** The research prompt was written as "inventory what exists" rather than "evaluate which architectural approach is correct." The distinction between data research and principles research was not made explicit. The plan was approved by the user who lacked the context to know the proposed pattern was an anti-pattern.

**Process change:** When a research task is about architectural approach (not data availability), the prompt must explicitly ask the agent to research and compare industry-standard approaches, not just describe what currently exists. During plan review, if a proposed pattern is a known shortcut or anti-pattern, flag it explicitly to the user before proceeding — do not let it pass silently.

**Applies to:** Any kickoff where the issue involves "choose an approach" or "design the architecture" — `/research` must address principles, not just data inventory.

---

## 2026-03-29 — Issue scope creep: documentation task became full implementation

**What happened:** OR-97 was scoped as a documentation task (write layer contracts, update standards). During kickoff the user corrected: "the idea was not to document it but to find and implement the right approach." The full implementation (wide fact table, stg_dbw.sql, domain mapping for 85 variables) was what was needed.

**Root cause:** The issue was created with "Define DW layer contracts" as the title, which reads as documentation. The user's actual intent was always implementation — the document is an output, not the goal.

**Process change:** During kickoff feasibility assessment, explicitly ask "is the deliverable a working system or a document?" if the issue title could be read either way. Do not default to documentation when the parent epic is about architectural change.

**Applies to:** Kickoff — feasibility assessment step, especially for "Define", "Document", "Establish" issue titles.

---

## 2026-03-29 — DBW mixed periods in same cross-section cause misleading KPIs

**What happened:** The "Gross domestic product" variable (section 16) stores annual totals (period_id=282), quarterly totals (period_id=270-273), and quarterly growth indices (103.x) all in the same cross-section. Summing by year across all period types produces nonsensical KPI values (latest year shows index values only, prior year includes annual total → apparent -100% YoY change).

**Root cause:** DBW cross-sections are not always "one metric per section" — some contain multiple presentation modes (level + index) or multiple periodicities (annual + quarterly) stacked together. The `period_id` field distinguishes these but is not exposed in the dashboard yet.

**Process change:** When building dashboards over DBW data for variables with multiple period types, either: (a) add a `period_id` filter, or (b) record the recommended `period_id` for annual series in `raw.dbw_variables`. For OR-95 this is an accepted limitation; address in a future enhancement.

**Applies to:** Any DBW dashboard or analysis using variables with mixed periodicity (GDP, national accounts aggregates).

---

## 2026-03-29 — Dynamic Dash callbacks require pattern-matching IDs for variable-count inputs

**What happened:** OR-99 added a dynamic dimension filter panel where the number of dropdowns changes based on selected indicators. Needed to read all active dim filter values in the run callback. Used Dash pattern-matching IDs (`{"type": "dim-filter", "col": ALL}`) + a `dcc.Store` intermediary to avoid the `prevent_initial_call` complication of having ALL-pattern inputs directly in the run callback.

**Root cause:** Dash `ALL` pattern-matching inputs in a callback fire on every render including initial. Isolating the sync to a dedicated `sync_dim_filter_store` callback and reading from `State("store-dim-filters", "data")` in the run callback avoids spurious runs.

**Process change:** For dynamic Dash components where the count of inputs varies at runtime: use pattern-matching IDs + a Store intermediary. Do not try to put `Input({"type": ..., "col": ALL}, "value")` directly into the main run callback.

**Applies to:** Any Dash dashboard with dynamically rendered filter components.

---

## 2026-03-29 — EAV anti-pattern approved without being flagged

**What happened:** OR-97 plan proposed generic `dim1_name/dim1_value...dim4_name/dim4_value` EAV slots as the dimension model for `curated.all_indicators`. The user approved the plan without knowing this was an anti-pattern. When OR-99 kicked off, the user noticed that `dim_sex` could land in `dim1` for one indicator and `dim2` for another — consistent filtering was impossible. Required a full OR-100 to research DW principles and reimplement with 24 named semantic columns.

**Root cause:** The plan was presented as if the EAV design was a thoughtful tradeoff ("flexibility vs. complexity"). In reality it was the path of least resistance. The known downsides (query-breaking inconsistency, no semantic meaning per column) were not flagged.

**Process change:** When a design choice is a known shortcut or anti-pattern, explicitly label it as such in the plan — do not present it as an equivalent tradeoff. The user must be told "this is an anti-pattern; the correct approach is X" not left to discover it later.

**Applies to:** Any plan that proposes a generic/flexible schema over a semantically correct one — flag as anti-pattern explicitly.

---

## 2026-03-29 — OS file permissions block Edit/Write tools when repo owned by root

**What happened:** Entire `/opt/open-reporting` directory tree was owned by `root`. Edit and Write tools ran as `radek` and received EACCES. Required three separate `sudo chown` commands before files could be written.

**Root cause:** The repo was initially set up as root, leaving all files root-owned. Claude Code runs as the logged-in user (`radek`), not root.

**Process change:** At project setup, run `sudo chown -R radek:radek /opt/open-reporting` once. If Edit/Write tools return EACCES, the fix is always the same command.

**Applies to:** All file editing — environment setup step.
