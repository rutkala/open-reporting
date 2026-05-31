#!/usr/bin/env python3
"""
Article release pipeline.

For each draft article, runs three independent reviewers:
  1. content-reviewer (Sonnet) — editorial/factual standards (P1/P2/P3)
  2. analytical-validator (Opus) — statistical correctness (MISLEADING/QUESTIONABLE/NOTED)
  3. domain-specialist (Opus) — domain KPI/framing (BLOCK/CONDITIONAL/APPROVE)

If NO reviewer returns BLOCK → publish the existing Ghost draft (update status to published).
If any reviewer BLOCKs → leave as Ghost draft, log findings.

Outputs:
  products/blog/reviews/<slug>-review.md  — per-article review
  products/blog/reviews/release-report.md — full run summary

Usage:
  # Review + publish all drafts
  python3 products/blog/release_pipeline.py

  # Review + publish specific file(s)
  python3 products/blog/release_pipeline.py products/blog/drafts/or-145-labour.md

  # Review only, no publish (safe to run any time)
  python3 products/blog/release_pipeline.py --dry-run

  # Force re-review even if review already exists
  python3 products/blog/release_pipeline.py --force
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml

# ─── Paths ────────────────────────────────────────────────────────────────────

REPO = Path("/opt/open-reporting")
DRAFTS_DIRS = [REPO / "products/blog/drafts", REPO / "products/blog"]
REVIEWS_DIR = REPO / "products/blog/reviews"
CLAUDE_BIN = shutil.which("claude") or "/home/radek/.local/bin/claude"
REVIEW_MODEL = "claude-sonnet-4-6"

# ─── Logging ──────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ─── Review criteria (loaded once from docs/) ─────────────────────────────────


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


CONTENT_CRITERIA = _read(REPO / "docs/content/reviewing.md")
ANALYTICAL_CRITERIA = _read(REPO / "docs/analytical-methods/reviewing.md")

# ─── Review prompts ───────────────────────────────────────────────────────────

# System prompts (criteria only) — passed via --system-prompt to bypass CLAUDE.md

CONTENT_SYSTEM_PROMPT = """You are a senior editorial reviewer for Open Reporting, a Polish data-journalism outlet.
Apply the review standards below to any article the user sends you. Return ONLY a structured verdict — no preamble.
Only flag what the rules explicitly cover. Do not offer suggestions beyond the rules.

===== REVIEW STANDARDS =====
{criteria}
===== END STANDARDS =====

Output ONLY this exact structure:

## Content Review

### P1 — Blocks Publication
<list findings as: "- Rule name: quote → explanation" or "None">

### P2 — Should Fix Before Publication
<list findings or "None">

### P3 — Noted
<list findings or "None">

### Verdict
<exactly one of: BLOCK | CONDITIONAL | PASS>

### Reasoning
<1-2 sentences: most critical finding, or confirmation of quality>

Verdict rules: BLOCK if any P1. CONDITIONAL if P2 only. PASS if P3 only or clean."""

ANALYTICAL_SYSTEM_PROMPT = """You are a senior statistician reviewing Polish data-journalism articles for statistical correctness.
Apply the analytical review standards below. You are in PLAN-PHASE mode — evaluate narrative claims, numbers, and framing (not code).
Only flag what the rules explicitly cover.

===== ANALYTICAL REVIEW STANDARDS =====
{criteria}
===== END STANDARDS =====

Evaluate only plan-phase rules: causal claims, CAGR across structural breaks, pp vs % errors, non-comparable populations.

Output ONLY this exact structure:

## Analytical Validation

### MISLEADING — Blocks Publication
<list findings as: "- Rule: quote → explanation" or "None">

### QUESTIONABLE — Should Fix
<list findings or "None">

### NOTED — Minor
<list findings or "None">

### Verdict
<exactly one of: BLOCK | CONDITIONAL | PASS>

### Reasoning
<1-2 sentences>

Verdict rules: BLOCK if any MISLEADING. CONDITIONAL if QUESTIONABLE only. PASS if NOTED only or clean."""

DOMAIN_SYSTEM_PROMPT = """You are a domain specialist reviewer evaluating Polish data-journalism articles.
Assess whether the domain-specific framing, indicator selection, and benchmarks are appropriate.

Focus ONLY on:
- Are the cited KPIs/indicators standard for this domain (Eurostat/ILO/IMF convention)?
- Is the framing accurate and the time-period context appropriate?
- Are benchmarks (EU average, peer group) correctly applied?
- Are any Polish-specific structural breaks or definitional notes missing where critical?

Do NOT flag issues covered by content-reviewer (language, attribution) or analytical-validator (causal claims, pp errors).

First identify the domain from the article. Then evaluate.

Output ONLY this exact structure:

## Domain Review: <identified domain>

### BLOCK — Must fix before publication
<list findings or "None">

### CONDITIONAL — Should address
<list findings or "None">

### NOTE — Good to address
<list findings or "None">

### Verdict
<exactly one of: BLOCK | CONDITIONAL | APPROVE>

### Reasoning
<1-2 sentences>

Verdict rules: BLOCK if critical domain error. CONDITIONAL if notable issues. APPROVE if domain framing is sound."""


# ─── Helpers ──────────────────────────────────────────────────────────────────


def _load_env() -> None:
    env_path = REPO / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k, v)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("---", 3)
    if end < 0:
        return {}, text
    fm = yaml.safe_load(text[3:end])
    body = text[end + 3:].lstrip("\n")
    return fm or {}, body


def extract_verdict(output: str, possible: list[str]) -> str | None:
    """Extract the verdict line from reviewer output."""
    for line in output.splitlines():
        stripped = line.strip()
        if stripped in possible:
            return stripped
        # Handle "### Verdict" section — next non-empty line
        if re.match(r"#{1,3}\s+Verdict", stripped, re.IGNORECASE):
            continue
    # Fallback: search for verdict word anywhere
    for word in possible:
        if re.search(rf"\b{word}\b", output, re.IGNORECASE):
            return word
    return None


def run_review(system_prompt: str, article_text: str, model: str = REVIEW_MODEL,
               max_retries: int = 3) -> str:
    """Run claude -p as a subprocess for a text-only review (no tools, custom system prompt).

    NOTE: Must be called from a standalone process (cron/autonomous lead), not from within
    an active Claude Code interactive session — nested sessions share the same rate-limit pool.
    """
    wrapped = f"Review the following article:\n\n{article_text}"
    for attempt in range(1, max_retries + 1):
        result = subprocess.run(
            [CLAUDE_BIN, "--model", model, "--tools", "", "--system-prompt", system_prompt,
             "-p", wrapped],
            capture_output=True,
            text=True,
            timeout=600,
            cwd=str(REPO),
            env={**os.environ},
        )
        if result.returncode == 0:
            return result.stdout
        detail = (result.stdout or result.stderr or "no output")[:300]
        if "credit" in detail.lower() or "rate" in detail.lower():
            wait = 30 * attempt
            log.warning("  rate-limit hit (attempt %d/%d), waiting %ds …", attempt, max_retries, wait)
            time.sleep(wait)
        else:
            raise RuntimeError(f"claude exited {result.returncode}: {detail}")
    raise RuntimeError(f"claude failed after {max_retries} retries (rate-limited)")


# ─── Per-article review ───────────────────────────────────────────────────────


def review_content(article_text: str) -> tuple[str, str]:
    """Returns (full_output, verdict: BLOCK|CONDITIONAL|PASS)."""
    system = CONTENT_SYSTEM_PROMPT.format(criteria=CONTENT_CRITERIA)
    output = run_review(system, article_text, model=REVIEW_MODEL)
    verdict = extract_verdict(output, ["BLOCK", "CONDITIONAL", "PASS"]) or "CONDITIONAL"
    return output, verdict


def review_analytical(article_text: str) -> tuple[str, str]:
    """Returns (full_output, verdict: BLOCK|CONDITIONAL|PASS)."""
    system = ANALYTICAL_SYSTEM_PROMPT.format(criteria=ANALYTICAL_CRITERIA)
    output = run_review(system, article_text, model=REVIEW_MODEL)
    verdict = extract_verdict(output, ["BLOCK", "CONDITIONAL", "PASS"]) or "CONDITIONAL"
    return output, verdict


def review_domain(article_text: str) -> tuple[str, str]:
    """Returns (full_output, verdict: BLOCK|CONDITIONAL|APPROVE)."""
    output = run_review(DOMAIN_SYSTEM_PROMPT, article_text, model=REVIEW_MODEL)
    # Domain specialist returns APPROVE (maps to PASS for gate logic)
    verdict = extract_verdict(output, ["BLOCK", "CONDITIONAL", "APPROVE"]) or "CONDITIONAL"
    return output, verdict


def run_all_reviews(article_text: str) -> dict:
    """Run three reviews sequentially to respect rate limits."""
    results = {}
    for name, fn in [
        ("content", review_content),
        ("analytical", review_analytical),
        ("domain", review_domain),
    ]:
        try:
            output, verdict = fn(article_text)
            results[name] = {"output": output, "verdict": verdict, "error": None}
        except Exception as exc:
            log.warning("  %s reviewer error: %s", name, exc)
            results[name] = {"output": "", "verdict": "ERROR", "error": str(exc)}
        time.sleep(2)  # brief pause between calls
    return results


def gate_passed(reviews: dict) -> bool:
    """True if no reviewer returned BLOCK (APPROVE counts as pass)."""
    for name, r in reviews.items():
        v = r["verdict"]
        if v in ("BLOCK", "ERROR"):
            return False
    return True


# ─── Ghost publish ────────────────────────────────────────────────────────────

# Import from sibling module (same directory)
sys.path.insert(0, str(REPO / "products/blog"))
from publish_to_ghost import (  # noqa: E402
    get_post_by_slug,
    publish_existing_post,
    create_post,
    parse_frontmatter as _parse_fm,
    strip_verification_comment,
)
from markdown_it import MarkdownIt  # noqa: E402


def publish_article(draft_path: Path, fm: dict, body: str) -> dict:
    """Publish article to Ghost. Updates existing draft or creates new published post."""
    slug = fm.get("slug", draft_path.stem)
    existing = get_post_by_slug(slug)
    if existing:
        log.info("  Ghost draft found (id=%s), updating to published …", existing["id"])
        return publish_existing_post(existing["id"], existing["updated_at"])
    # No existing draft — create and publish directly
    log.info("  No Ghost draft found for slug=%r, creating published post …", slug)
    md = MarkdownIt("commonmark", {"html": True}).enable("table")
    html = md.render(strip_verification_comment(body))
    return create_post(fm, html, status="published")


# ─── Review report ────────────────────────────────────────────────────────────


def write_review_report(slug: str, reviews: dict, published: bool, post_url: str | None) -> Path:
    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M")
    lines = [
        f"# Review: {slug}",
        f"*{ts} UTC*\n",
        f"**Gate result:** {'✅ PUBLISHED' if published else '🔴 BLOCKED — not published'}",
    ]
    if post_url:
        lines.append(f"**URL:** {post_url}\n")
    for name, r in reviews.items():
        lines.append(f"\n---\n\n## Reviewer: {name}")
        lines.append(f"**Verdict:** {r['verdict']}")
        if r["error"]:
            lines.append(f"**Error:** {r['error']}")
        else:
            lines.append("\n" + r["output"])

    report_path = REVIEWS_DIR / f"{slug}-review.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


# ─── Main ─────────────────────────────────────────────────────────────────────


def collect_drafts(paths: list[str]) -> list[Path]:
    if paths:
        return [Path(p).resolve() for p in paths if Path(p).suffix == ".md"]
    drafts: list[Path] = []
    for d in DRAFTS_DIRS:
        if d.is_dir():
            for f in sorted(d.glob("*.md")):
                if f.name != ".gitkeep":
                    drafts.append(f)
    return drafts


def process_article(draft: Path, dry_run: bool, force: bool) -> dict:
    """Review and optionally publish one article. Returns result summary."""
    text = draft.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    slug = fm.get("slug", draft.stem)
    title = fm.get("title", slug)

    log.info("── %s ──", slug)

    # Skip if already reviewed and not forced
    review_path = REVIEWS_DIR / f"{slug}-review.md"
    if review_path.exists() and not force:
        # Check if prior review resulted in publish
        prior = review_path.read_text()
        if "✅ PUBLISHED" in prior:
            log.info("  already published (skip). Use --force to re-review.")
            return {"slug": slug, "title": title, "status": "already_published", "url": None}

    log.info("  Running 3 reviewers in parallel …")
    t0 = time.monotonic()
    reviews = run_all_reviews(text)
    elapsed = time.monotonic() - t0
    log.info("  Reviews done in %.1fs", elapsed)

    for name, r in reviews.items():
        marker = "🔴 BLOCK" if r["verdict"] in ("BLOCK", "ERROR") else "✅"
        log.info("    %s → %s %s", name, r["verdict"], marker)

    passed = gate_passed(reviews)
    post_url = None

    if passed and not dry_run:
        log.info("  Gate PASSED — publishing to Ghost …")
        try:
            post = publish_article(draft, fm, body)
            post_url = post.get("url")
            log.info("  Published: %s", post_url)
            status = "published"
        except Exception as exc:
            log.error("  Ghost publish failed: %s", exc)
            status = "publish_error"
    elif passed and dry_run:
        log.info("  Gate PASSED — dry-run, skipping Ghost publish")
        status = "would_publish"
    else:
        log.info("  Gate BLOCKED — leaving as draft")
        status = "blocked"

    write_review_report(slug, reviews, passed and status == "published", post_url)
    return {"slug": slug, "title": title, "status": status, "url": post_url}


def write_summary(results: list[dict], dry_run: bool) -> Path:
    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M UTC")
    lines = [
        f"# Release Pipeline Report — {ts}",
        f"Mode: {'DRY RUN' if dry_run else 'LIVE'}\n",
        "| Article | Status |",
        "|---|---|",
    ]
    counts: dict[str, int] = {}
    for r in results:
        icon = {
            "published": "✅ Published",
            "would_publish": "🟡 Would publish",
            "blocked": "🔴 Blocked",
            "publish_error": "⚠️ Publish error",
            "already_published": "✅ Already published",
        }.get(r["status"], r["status"])
        url_cell = f" ([link]({r['url']}))" if r.get("url") else ""
        lines.append(f"| {r['title']} | {icon}{url_cell} |")
        counts[r["status"]] = counts.get(r["status"], 0) + 1

    lines.append("")
    lines.append("## Summary")
    for k, v in counts.items():
        lines.append(f"- {k}: {v}")

    path = REVIEWS_DIR / "release-report.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def main() -> int:
    ap = argparse.ArgumentParser(description="Article release pipeline")
    ap.add_argument("drafts", nargs="*", help="Specific draft file(s) to process (default: all)")
    ap.add_argument("--dry-run", action="store_true", help="Review only — do not publish to Ghost")
    ap.add_argument("--force", action="store_true", help="Re-review even if review already exists")
    args = ap.parse_args()

    _load_env()

    drafts = collect_drafts(args.drafts)
    if not drafts:
        log.error("No draft articles found.")
        return 1

    log.info("Found %d draft(s) to process.", len(drafts))
    if args.dry_run:
        log.info("DRY RUN — no Ghost publishes will be made.")

    results = []
    for draft in drafts:
        try:
            result = process_article(draft, dry_run=args.dry_run, force=args.force)
            results.append(result)
        except Exception as exc:
            log.error("Failed to process %s: %s", draft.name, exc)
            results.append({
                "slug": draft.stem,
                "title": draft.stem,
                "status": "error",
                "url": None,
            })

    summary_path = write_summary(results, dry_run=args.dry_run)
    log.info("Summary written to %s", summary_path.relative_to(REPO))

    # Print final tally
    published = sum(1 for r in results if r["status"] in ("published", "already_published"))
    blocked = sum(1 for r in results if r["status"] == "blocked")
    log.info("Done. Published: %d | Blocked: %d | Total: %d", published, blocked, len(results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
