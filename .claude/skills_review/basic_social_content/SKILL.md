---
name: basic_social_content
description: "Social media content product context. Loaded when producing content for Instagram (@otwarteraporty). Defines what social content is, its format, visual requirements, and publication workflow."
user-invocable: true
---

# Social Media Content

Social content is a data visualisation post for Instagram (@otwarteraporty).
It turns a single analytical insight into a visually compelling, self-contained post
that works without any accompanying text article.

This skill defines WHAT social content is. The process lives in `/composite_develop`.

---

## Platform

| Platform | Account | Token expiry |
|----------|---------|-------------|
| Instagram | @otwarteraporty | ~2026-05-20 (OR-90) |

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
| Visual asset | `products/social/{slug}/visual.png` | Yes |
| Caption (Polish) | `products/social/{slug}/caption.md` | Yes |
| Hashtags | Included in caption | Yes |

---

## Format rules

**Visual:**
- Square format (1080×1080px) or portrait (1080×1350px)
- Nordic colour palette — use theme tokens from `products/visuals/lib/theme.py`
- One key number or chart per post — no data overload
- Title states the insight, not the chart type

**Caption:**
- Polish, conversational but informed register
- Lead with the key number or finding
- 2–3 sentences of context
- Source attribution in final line
- 5–10 relevant hashtags

---

## Quality gates

- [ ] Single clear insight — viewer understands the point in 3 seconds
- [ ] Source visible on the visual itself (not just in caption)
- [ ] Caption reads naturally in Polish (correct diacritics, natural phrasing)
- [ ] Visual uses Nordic palette only — no off-palette colours

---

## Standards

- `team/standards/build/visualisation.md` (visual design)
- `team/standards/evaluation/content-review.md`
