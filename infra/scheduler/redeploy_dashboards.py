#!/usr/bin/env python3
"""Rebuild every dbr dashboard to static HTML and *verify* each is on current code.

Why this exists
---------------
As of OR-168 the dashboards are pre-rendered STATIC HTML (``dbr build``) served
directly by nginx from ``infra/nginx/html/<domain>/index.html`` — there is no
always-on Dash server and no port. Editing dbr source or refreshing the warehouse
does NOT change what nginx serves until the pages are rebuilt.

The recurring failure this kills: a run edits dbr code or refreshes data, then
"verifies" with a ``curl`` that returns 200 — but 200 only proves a file exists,
not that it was rebuilt from current code/data. This script closes the loop:

  1. read repo HEAD,
  2. (unless --verify-only) publish the shared plotly.min.js, then ``dbr build``
     every dashboard into the nginx web root — hard-failing if ANY build errors
     (e.g. UnsupportedComponentError = a dashboard grew runtime interactivity),
  3. read each built page's ``<meta name="dbr-build">`` stamp and confirm == HEAD,
  4. print an honest per-dashboard PASS / STALE / MISSING table,
  5. exit non-zero if ANY dashboard is not freshly built on HEAD.

"resolved" is then provable: the built page literally names its commit, and a
non-zero exit means do not report success.

Usage
-----
    python3 infra/scheduler/redeploy_dashboards.py            # rebuild + verify all
    python3 infra/scheduler/redeploy_dashboards.py finance    # one (by domain)
    python3 infra/scheduler/redeploy_dashboards.py --verify-only   # no rebuild
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
DASHBOARDS_DIR = REPO / "products" / "dashboards"
WEB_ROOT = REPO / "infra" / "nginx" / "html"
PLOTLY_SRC = "/assets/plotly.min.js"
_BUILD_RE = re.compile(r'<meta name="dbr-build" content="([^"]*)">')


def head_sha() -> str:
    out = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=REPO, capture_output=True, text=True, timeout=5,
    )
    out.check_returncode()
    return out.stdout.strip()


def discover() -> list[str]:
    """Return [domain, ...] for every dashboard with a dashboard.yml."""
    found: list[str] = []
    for d in sorted(DASHBOARDS_DIR.iterdir()):
        yml = d / "dashboard.yml"
        if not yml.is_file():
            continue
        cfg = yaml.safe_load(yml.read_text()) or {}
        if cfg.get("domain"):
            found.append(cfg["domain"])
    return found


def built_sha(domain: str) -> str | None:
    """Read the built page's dbr-build stamp.

    None → no index.html (never built / wrong path).
    ""   → built but carries no stamp (shouldn't happen with current dbr).
    """
    index = WEB_ROOT / domain / "index.html"
    if not index.is_file():
        return None
    m = _BUILD_RE.search(index.read_text(encoding="utf-8", errors="replace"))
    return m.group(1) if m else ""


def _build_env() -> dict:
    env = dict(os.environ)
    env.setdefault("DUCKDB_PATH", str(REPO / "data" / "warehouse.duckdb"))
    env.setdefault("PYTHONPATH", str(REPO))
    return env


def build(domain: str) -> tuple[bool, str]:
    """Render one dashboard to static HTML in the web root. Returns (ok, detail)."""
    r = subprocess.run(
        ["dbr", "build", str(DASHBOARDS_DIR / domain),
         "--out", str(WEB_ROOT),
         "--plotly-src", PLOTLY_SRC, "--no-vendor-plotly"],
        capture_output=True, text=True, env=_build_env(),
    )
    out = (r.stderr or r.stdout).strip()
    detail = out.splitlines()[-1] if out else ""
    return r.returncode == 0, detail


def publish_shared_assets() -> None:
    """Write the single shared plotly.min.js under the web root (idempotent)."""
    sys.path.insert(0, str(REPO / "packages" / "dbr" / "src"))
    from dbr.static_export import write_plotlyjs
    write_plotlyjs(WEB_ROOT / "assets")


def main(argv: list[str]) -> int:
    verify_only = "--verify-only" in argv
    targets = [a for a in argv if not a.startswith("--")]

    want = head_sha()
    domains = discover()
    if targets:
        domains = [d for d in domains if d in targets]
        if not domains:
            print(f"No matching dashboards for {targets}", file=sys.stderr)
            return 2

    action = "Verifying" if verify_only else "Rebuilding"
    print(f"{action} {len(domains)} static dashboard(s) against HEAD {want}\n")

    if not verify_only:
        publish_shared_assets()
        build_failed = False
        for domain in domains:
            ok, detail = build(domain)
            mark = "✓" if ok else "✗"
            print(f"  {mark} build {domain}" + ("" if ok else f" — {detail}"))
            build_failed = build_failed or not ok
        print()
        if build_failed:
            print("FAIL — one or more dashboards failed to build. Do NOT report resolved.")
            return 1

    results: list[tuple[str, str, str]] = []
    for domain in domains:
        sha = built_sha(domain)
        if sha is None:
            status, detail = "MISSING", "no index.html in web root"
        elif sha == want:
            status, detail = "PASS", want
        else:
            status, detail = "STALE", f"built {sha or '?'}, want {want}"
        results.append((domain, status, detail))
        glyph = {"PASS": "✓", "STALE": "✗", "MISSING": "✗"}[status]
        print(f"  {glyph} {domain:<20} {status:<7} {detail}")

    stale = [d for d, s, _ in results if s != "PASS"]
    print()
    if stale:
        print(f"FAIL — {len(stale)}/{len(results)} not freshly built on HEAD: {', '.join(stale)}")
        print("Do NOT report this as resolved.")
        return 1
    print(f"OK — all {len(results)} dashboards built static on HEAD {want}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
