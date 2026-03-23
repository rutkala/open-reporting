---
name: scaffold
description: "Scaffold a new file following project conventions. Creates route/endpoint, page/component, service, model, job, or test file with proper boilerplate, imports, and registration. Reads existing code to match patterns."
disable-model-invocation: true
user-invocable: true
argument-hint: "<type> <name> [description]"
---

# Scaffold New File

Create a new file following this project's conventions. Reads existing code to match patterns exactly.

## Arguments
`$ARGUMENTS`

**Supported types** (first word of arguments):
- `route` or `endpoint` — API route/controller file
- `page` — Frontend page component
- `component` — Reusable UI component
- `service` — Business logic service class
- `model` — Database model/schema
- `job` — Background job/worker
- `test` — Test file for an existing module
- `middleware` — Request middleware
- `hook` — React hook (frontend)
- `util` — Utility/helper module

If the type is ambiguous or missing, ask the user.

## Method

### Step 1 — Identify the pattern
1. Determine which directory the new file belongs in based on type
2. Find an existing file of the same type to use as a pattern reference
3. Read that reference file to extract:
   - Import style (CommonJS `require` vs ES `import`)
   - Export pattern (default export, named exports, class instance)
   - Error handling pattern
   - Auth/middleware usage
   - Naming conventions (camelCase, PascalCase, kebab-case)

### Step 2 — Generate the scaffold
1. Create the new file matching the discovered patterns exactly
2. Include appropriate boilerplate:
   - Imports matching project style
   - Proper module structure
   - Error handling matching project patterns
   - TODO comments where business logic needs to be added
   - Type annotations if the project uses TypeScript

### Step 3 — Register it
Depending on the type, check if registration is needed:
- **Routes**: Register in the main app file (e.g., `app.use('/api/...', router)`)
- **Pages**: Add to router config (e.g., React Router, Next.js pages, Vue Router)
- **Models**: Register in model index if one exists
- **Jobs**: Register in job scheduler if one exists
- **Components**: No registration needed usually

### Step 4 — Present for approval
Show the user:
1. The new file content
2. Any registration changes needed
3. Any other files that need updating

**NEVER create files without user approval.**

## Rules
- Match existing code patterns exactly — don't introduce new conventions
- Use the project's actual import paths (read existing files to find them)
- If the project uses TypeScript, generate `.ts`/`.tsx` files
- **i18n awareness**: Read `.claude/languages.json` — if `content_languages` has 2+ entries, include i18n imports and `t()` calls for all user-facing strings in scaffolded components
- Include standard error handling matching the project's pattern
- Don't over-scaffold — keep it minimal, the user will add business logic
