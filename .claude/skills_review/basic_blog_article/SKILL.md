---
name: basic_blog_article
description: "Blog article product context. Loaded when any work targets a written article for www.open-reporting.dev. Defines what an article is, its structure, tone, quality standards, and publication workflow."
user-invocable: true
---

# Blog Article

A blog article is a data-driven editorial piece published to `www.open-reporting.dev`
via Ghost CMS. Articles turn Polish public data into accessible analytical narratives
for a general but curious audience.

This skill defines WHAT an article is. The process for producing one lives in `/composite_develop`.
Load this skill first to provide article-specific context to the process skills.

---

## Technology stack

| Layer | Technology |
|-------|-----------|
| CMS | Ghost (port 2368, internal) |
| Publication URL | `www.open-reporting.dev` |
| Language | Polish (formal register, correct diacritics) |
| Format | Markdown → Ghost editor |

---

## Input

| Artifact | Location | Produced by |
|----------|----------|-------------|
| Requirements document | `products/domain-briefs/{domain}/basic_requirements.md` | `/composite_document` |
| Domain brief | `products/domain-briefs/{domain}/domain-brief.md` | `/basic_research` (via `/composite_document`) |

---

## Output

| Deliverable | Location | Required |
|-------------|----------|---------|
| Article draft | `products/blog/{slug}.md` | Yes |
| Published article | `www.open-reporting.dev/{slug}` | Yes (on release) |

---

## Structure

Every article must contain:
1. **Lead paragraph** — the key finding in plain language; answers "so what?" immediately
2. **Data section** — what the data shows, with supporting charts or statistics
3. **Context section** — why this matters, what it compares to, what experts say
4. **Conclusion** — one clear takeaway; what the reader should think or do with this
5. **Source attribution** — every data claim linked to its source

---

## Tone and language rules

- Formal Polish — no slang, no anglicisms
- Active voice preferred
- Numbers in Polish format (space separator, comma decimal, tys./mln/mld/zł)
- Every claim must be traceable to a cited source
- No unsupported conclusions — if causation cannot be shown, write "suggests", not "proves"

---

## Quality gates

Before handing to `/composite_evaluate`:
- [ ] Lead paragraph answers "so what?" without jargon
- [ ] Every data claim has a cited source
- [ ] Polish diacritics are correct throughout (ą ć ę ł ń ó ś ź ż)
- [ ] No anglicisms or informal register
- [ ] Conclusion is a single, defensible claim

---

## Standards

- `docs/content/reviewing.md`
- `docs/analytical-methods/principles.md`
