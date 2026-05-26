# Multimodal capture recipe — visual design references

How to capture an external design-knowledge article (e.g. PencilAndPaper, FT Visual Vocabulary, Tableau showcase) in a form a vision-capable AI agent can later reason on.

Verified working as of 2026-05-25.

## The recipe

**Three steps:**

1. **WebFetch the article** with a prompt that asks for: section headings, image count, **full image URLs**, and the surrounding text for each central image.
2. **WebFetch each image URL individually.** The small model that processes the WebFetch response cannot describe images and will return a "binary content" message. Ignore that — the file is **silently saved to disk** in the session's `tool-results/` directory as a side-effect. That's the linchpin.
3. **`Read` each saved file path** with the main vision-capable model (Sonnet or Opus). Full multimodal vision is available. Pair the visual reading with the article context from step 1 to produce a paired text+image annotation.

## Why this works

WebFetch was built for text content but its underlying fetch happens before the model layer — so binary responses land on disk regardless of whether the small model can interpret them. The `Read` tool reads images natively for vision-capable models. Chaining the two gives multimodal capture without installing anything.

## Caveats

- **≈30% of CDN image URLs return HTTP 403** because the CDN checks the `Referer` header. For those, fall back to **Playwright** (available at `/home/radek/.local/bin/playwright`) — render the page in a real browser context and screenshot the relevant section.
- **GIF files yield only the first frame** via `Read`. Useful for static patterns; insufficient for interaction demos. Capture interactions as descriptive text instead.
- **`tool-results/` is session-scoped.** Files there vanish when the session ends. A pipeline that builds a persistent reference library must **copy the binaries to a stable path** (e.g. `.claude/skills/complex_dashboard/assets/references/<source>/`) before the session closes.
- **Vision works in subagents.** Sonnet subagents (default tier per `docs/process/model-delegation.md`) can run the whole loop end-to-end. Reserve Opus for picking which references to capture and for distilling the quality rubric from observed patterns.

## When to prefer Playwright instead

- Site renders content via JS so URLs aren't in the initial markdown
- Paywalled or auth-walled content
- 403 rate is high enough that per-image fetch becomes uneconomical
- Need the **full page in context** (rare — per-image is usually more useful for KB)

Playwright produces one large screenshot; per-image fetch produces N targeted images. The latter is almost always better for a reference library.
