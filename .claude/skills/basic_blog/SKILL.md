---
name: basic_blog
description: "Blog platform product context. Loaded when working on www.open-reporting.dev — the Ghost CMS editorial platform. Defines the blog as a product: configuration, content strategy, publishing workflow."
user-invocable: true
---

# Blog

The blog is the editorial delivery channel at `www.open-reporting.dev`, powered by
Ghost CMS. It publishes data-driven articles about Polish public data.

This skill defines WHAT the blog platform is. For individual article work, use `/basic_blog_article`.

---

## Technology stack

| Layer | Technology |
|-------|-----------|
| CMS | Ghost (port 2368, internal) |
| Public URL | `www.open-reporting.dev` |
| Admin | Ghost admin panel (OR-78) |
| Delivery | nginx reverse proxy |

---

## Content strategy

- Domain focus: Polish public data — labour, finance, demographics, regional
- Audience: informed general public, journalists, policy analysts
- Cadence: data-driven — publish when data warrants it, not on a fixed schedule
- Language: Polish (formal, accessible)

---

## Publishing workflow

1. Article draft produced via `/basic_blog_article`
2. Passes `/composite_evaluate` (content-reviewer)
3. Published to Ghost via admin panel or Ghost API
4. Appears at `www.open-reporting.dev`

---

## Quality gates (platform level)

- [ ] Ghost service healthy: `docker compose ps ghost`
- [ ] Published article accessible at its URL
- [ ] Article appears in RSS feed
- [ ] Images load correctly

---

## Standards

- `team/standards/evaluation/content-review.md`
