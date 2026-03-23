---
name: {skill-name}
description: "{Description of what this skill provides. Include trigger keywords so Claude knows when to auto-load it. Example: Auto-loaded when creating or modifying API endpoints, routes, or middleware.}"
user-invocable: false
---

# {Skill Title} — Auto-Triggered Reference

<!--
  AUTO-TRIGGERED SKILLS
  =====================
  These are NOT slash commands. They are background knowledge that Claude
  automatically loads when it detects relevant work.

  Key setting: `user-invocable: false`

  Claude decides to load this based on the `description` field.
  Write the description to include trigger keywords, e.g.:
  - "Auto-loaded when working with database migrations, schema changes, or models"
  - "Auto-loaded when creating React components, pages, or hooks"
  - "Auto-loaded when working with authentication, JWT, or session handling"

  EXAMPLES OF GOOD AUTO-TRIGGERED SKILLS:
  - API conventions (response format, auth middleware, error handling)
  - Database patterns (query style, ORM usage, migration format)
  - Component conventions (file structure, prop patterns, state management)
  - Testing patterns (framework, mocking, fixture conventions)
  - Deployment patterns (CI/CD, environment variables, feature flags)
  - Real-time events (WebSocket/Socket.io event names and data shapes)
-->

## {Section 1: Core Pattern}

<!-- Document the mandatory pattern/convention here -->
<!-- Include code examples that can be copy-pasted -->

```
{code example}
```

## {Section 2: Variations}

<!-- Document variations of the pattern -->

## {Section 3: Common Mistakes}

<!-- Document what NOT to do -->

## {Section 4: Checklist}

<!-- Quick reference checklist for this convention -->
- [ ] {Check 1}
- [ ] {Check 2}
- [ ] {Check 3}
