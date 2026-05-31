#!/usr/bin/env python3
"""Redeploy every dbr dashboard and *verify* each is running current code.

Why this exists
---------------
``packages/dbr/`` is editable-installed. A running ``or-<domain>.service``
loads the framework code as it was on disk at process-start; editing dbr
source does NOT change a live service until that service is restarted.

The recurring failure this kills: a run edits dbr code, commits, restarts
some-or-no services, then "verifies" with a ``curl`` that returns 200 — but
200 only proves *a* process answered, not that it is running the *new* code.
Stale services pass the check, the run reports "resolved", and the dashboards
visibly do not change.

This script closes the loop. Every dashboard page now advertises the git SHA
it booted from via ``<meta name="dbr-build">`` (see ``dbr.make_app``). Here we:

  1. read repo HEAD,
  2. restart every ``or-<domain>.service`` (NOPASSWD-allowlisted),
  3. poll each live page until its ``dbr-build`` stamp == HEAD,
  4. print an honest per-dashboard PASS / STALE / DOWN table,
  5. exit non-zero if ANY dashboard is not on HEAD.

"resolved" is then provable: the live page literally names its commit, and a
non-zero exit means do not report success.

Usage
-----
    python3 infra/scheduler/redeploy_dashboards.py            # all dashboards
    python3 infra/scheduler/redeploy_dashboards.py finance    # one (by domain)
    python3 infra/scheduler/redeploy_dashboards.py --verify-only   # no restart
"""
from __future__ import annotations

import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
DASHBOARDS_DIR = REPO / "products" / "dashboards"
HEALTH_BUDGET_S = 140           # per-dashboard boot budget; heaviest (demographics) boots ~105s
POLL_INTERVAL_S = 2
_BUILD_RE = re.compile(r'<meta name="dbr-build" content="([^"]*)">')


def head_sha() -> str:
    out = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=REPO, capture_output=True, text=True, timeout=5,
    )
    out.check_returncode()
    return out.stdout.strip()


def discover() -> list[tuple[str, int]]:
    """Return [(domain, port), ...] for every dashboard with a dashboard.yml."""
    found: list[tuple[str, int]] = []
    for d in sorted(DASHBOARDS_DIR.iterdir()):
        yml = d / "dashboard.yml"
        if not yml.is_file():
            continue
        cfg = yaml.safe_load(yml.read_text()) or {}
        domain, port = cfg.get("domain"), cfg.get("port")
        if domain and port:
            found.append((domain, int(port)))
    return found


def live_sha(domain: str, port: int, timeout: float = 3.0) -> str | None:
    """Fetch the dashboard's index HTML and return its dbr-build stamp.

    None  → could not connect / no 200 (service down or still booting).
    ""    → page served but carries no stamp (pre-stamp / old code).
    """
    url = f"http://127.0.0.1:{port}/{domain}/"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            if resp.status != 200:
                return None
            html = resp.read().decode("utf-8", "replace")
    except Exception:
        return None
    m = _BUILD_RE.search(html)
    return m.group(1) if m else ""


def restart(domain: str) -> tuple[bool, str]:
    """Restart one unit via the NOPASSWD-allowlisted systemctl form."""
    r = subprocess.run(
        ["sudo", "-n", "/usr/bin/systemctl", "restart", f"or-{domain}.service"],
        capture_output=True, text=True,
    )
    return r.returncode == 0, (r.stderr or r.stdout).strip()


def wait_for_sha(domain: str, port: int, want: str) -> tuple[str, str]:
    """Poll until the live stamp == want, or the budget expires.

    Returns (status, detail) where status ∈ {PASS, STALE, DOWN}.
    """
    deadline = time.time() + HEALTH_BUDGET_S
    last: str | None = None
    while time.time() < deadline:
        last = live_sha(domain, port)
        if last == want:
            return "PASS", want
        time.sleep(POLL_INTERVAL_S)
    if last is None:
        return "DOWN", "no 200 within budget"
    if last == "":
        return "STALE", "page has no dbr-build stamp (pre-stamp code)"
    return "STALE", f"serving {last or '?'}, want {want}"


def main(argv: list[str]) -> int:
    verify_only = "--verify-only" in argv
    targets = [a for a in argv if not a.startswith("--")]

    want = head_sha()
    dashboards = discover()
    if targets:
        dashboards = [(d, p) for d, p in dashboards if d in targets]
        if not dashboards:
            print(f"No matching dashboards for {targets}", file=sys.stderr)
            return 2

    action = "Verifying" if verify_only else "Redeploying"
    print(f"{action} {len(dashboards)} dashboard(s) against HEAD {want}\n")

    if not verify_only:
        for domain, _ in dashboards:
            ok, detail = restart(domain)
            mark = "✓" if ok else "✗"
            print(f"  {mark} restart or-{domain}.service" + ("" if ok else f" — {detail}"))
        print()

    results: list[tuple[str, str, str]] = []
    for domain, port in dashboards:
        status, detail = wait_for_sha(domain, port, want)
        results.append((domain, status, detail))
        glyph = {"PASS": "✓", "STALE": "✗", "DOWN": "✗"}[status]
        print(f"  {glyph} {domain:<20} {status:<6} {detail}")

    stale = [d for d, s, _ in results if s != "PASS"]
    print()
    if stale:
        print(f"FAIL — {len(stale)}/{len(results)} not on HEAD: {', '.join(stale)}")
        print("Do NOT report this as resolved.")
        return 1
    print(f"OK — all {len(results)} dashboards serving HEAD {want}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
