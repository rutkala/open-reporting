#!/usr/bin/env python3
"""
Ghost article publisher.

Reads a Markdown draft with YAML frontmatter from `data/drafts/<slug>.md`,
uploads any local image references it finds, converts MD→HTML, and posts
to Ghost via the Admin API as a draft (default) or published (--publish).

Usage:
  PYTHONPATH=/opt/open-reporting python3 products/blog/publish_to_ghost.py \\
      data/drafts/or-80-sgp-maastricht.md \\
      --images /tmp/article-images/debt-trend.png:wykres-1 \\
      --images /tmp/article-images/ue-deficit.png:wykres-2 \\
      --insert-after "## Jak doszło do deficytu":wykres-1 \\
      --insert-after "## Rosnące koszty obsługi długu":wykres-2 \\
      --publish

YAML frontmatter expected at the top of the draft:
  title:   "..."
  slug:    "..."
  excerpt: "..."
  tags:    ["...", ...]

Ghost Admin API auth uses the JWT integration key from .env:
  GHOST_KEY_ID, GHOST_KEY_SECRET

Linear: OR-80.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

import jwt
import requests
import yaml
from markdown_it import MarkdownIt

GHOST_URL = "https://www.open-reporting.dev/ghost/api/admin"


def _load_env(path: str = ".env") -> None:
    if not Path(path).exists():
        return
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k, v)


def _ghost_jwt() -> str:
    kid = os.environ["GHOST_KEY_ID"]
    secret = bytes.fromhex(os.environ["GHOST_KEY_SECRET"])
    iat = int(time.time())
    return jwt.encode(
        {"iat": iat, "exp": iat + 300, "aud": "/admin/"},
        secret, algorithm="HS256", headers={"kid": kid},
    )


def _headers(content_type: str | None = "application/json") -> dict:
    h = {"Authorization": f"Ghost {_ghost_jwt()}"}
    if content_type:
        h["Content-Type"] = content_type
    return h


def upload_image(local_path: str) -> str:
    """Upload an image to Ghost. Returns the public URL."""
    with open(local_path, "rb") as f:
        files = {"file": (Path(local_path).name, f, "image/png")}
        data = {"purpose": "image", "ref": Path(local_path).stem}
        # No Content-Type header — requests sets multipart boundary
        r = requests.post(
            f"{GHOST_URL}/images/upload/",
            headers={"Authorization": f"Ghost {_ghost_jwt()}"},
            files=files, data=data, timeout=30,
        )
    r.raise_for_status()
    return r.json()["images"][0]["url"]


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("---", 3)
    if end < 0:
        return {}, text
    fm = yaml.safe_load(text[3:end])
    body = text[end + 3:].lstrip("\n")
    return fm or {}, body


def strip_verification_comment(md: str) -> str:
    """Drop the internal <!-- WERYFIKACJA --> block before publishing."""
    return re.sub(r"<!-- WERYFIKACJA.*?-->", "", md, flags=re.DOTALL).rstrip()


def insert_image_figures(md: str, insertions: list[tuple[str, str, str]]) -> str:
    """For each (after_heading, image_url, alt) — insert a figure block right after the heading line."""
    out = md
    for after_heading, image_url, alt in insertions:
        # Find the heading line; insert a figure block on the next blank line
        pattern = re.escape(after_heading)
        # Look for the heading + the next paragraph break, then insert
        figure = f'\n\n<figure><img src="{image_url}" alt="{alt}" loading="lazy"><figcaption>{alt}</figcaption></figure>\n\n'
        replacement = after_heading + figure
        new = re.sub(pattern, replacement, out, count=1)
        if new == out:
            print(f"!! could not find heading: {after_heading!r}", file=sys.stderr)
        out = new
    return out


def get_post_by_slug(slug: str) -> dict | None:
    """Return the Ghost post record for slug, or None if not found."""
    r = requests.get(
        f"{GHOST_URL}/posts/",
        headers=_headers(),
        params={"filter": f"slug:{slug}", "fields": "id,slug,status,updated_at"},
        timeout=30,
    )
    r.raise_for_status()
    posts = r.json().get("posts", [])
    return posts[0] if posts else None


def publish_existing_post(post_id: str, updated_at: str) -> dict:
    """Change status of an existing Ghost post to published."""
    payload = {"posts": [{"status": "published", "updated_at": updated_at}]}
    r = requests.put(
        f"{GHOST_URL}/posts/{post_id}/?source=html",
        headers=_headers(), data=json.dumps(payload), timeout=30,
    )
    r.raise_for_status()
    return r.json()["posts"][0]


def update_and_publish_post(post_id: str, updated_at: str, fm: dict, html: str) -> dict:
    """Update content + set status=published in one PUT call."""
    payload = {"posts": [{
        "status":         "published",
        "updated_at":     updated_at,
        "title":          fm["title"],
        "custom_excerpt": fm.get("excerpt"),
        "html":           html,
        "tags":           [{"name": t} for t in (fm.get("tags") or [])],
    }]}
    r = requests.put(
        f"{GHOST_URL}/posts/{post_id}/?source=html",
        headers=_headers(), data=json.dumps(payload), timeout=30,
    )
    r.raise_for_status()
    return r.json()["posts"][0]


def create_post(fm: dict, html: str, status: str = "draft") -> dict:
    payload = {"posts": [{
        "title":       fm["title"],
        "slug":        fm.get("slug"),
        "custom_excerpt": fm.get("excerpt"),
        "html":        html,
        "status":      status,
        "tags":        [{"name": t} for t in (fm.get("tags") or [])],
    }]}
    r = requests.post(
        f"{GHOST_URL}/posts/?source=html",
        headers=_headers(), data=json.dumps(payload), timeout=30,
    )
    r.raise_for_status()
    return r.json()["posts"][0]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("draft", type=Path, help="Markdown draft with YAML frontmatter")
    ap.add_argument("--images", action="append", default=[],
                    help="Image to upload: 'local/path.png:alt-text'")
    ap.add_argument("--insert-after", action="append", default=[],
                    help="Insertion point: '## Heading text:alt-text'")
    ap.add_argument("--publish", action="store_true", help="Set status=published (default: draft)")
    args = ap.parse_args()

    _load_env()

    # Upload images first; build map alt -> url
    image_urls: dict[str, str] = {}
    for spec in args.images:
        local, alt = spec.rsplit("||", 1)
        url = upload_image(local)
        image_urls[alt] = url
        print(f"uploaded {local} → {url}")

    # Read + parse
    raw = args.draft.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(raw)
    body = strip_verification_comment(body)

    # Insert image figures by heading marker
    insertions: list[tuple[str, str, str]] = []
    for spec in args.insert_after:
        heading, alt = spec.rsplit("||", 1)
        if alt not in image_urls:
            print(f"!! no image uploaded for alt={alt!r}", file=sys.stderr)
            return 2
        insertions.append((heading, image_urls[alt], alt))
    body = insert_image_figures(body, insertions)

    # Convert MD → HTML
    md = MarkdownIt("commonmark", {"html": True}).enable("table")
    html = md.render(body)

    # Post
    status = "published" if args.publish else "draft"
    post = create_post(fm, html, status=status)
    print(f"\n{'PUBLISHED' if args.publish else 'DRAFT created'}")
    print(f"  id:     {post['id']}")
    print(f"  slug:   {post['slug']}")
    print(f"  status: {post['status']}")
    print(f"  url:    {post['url']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
