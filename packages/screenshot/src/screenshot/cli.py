#!/usr/bin/env python3
"""
Screenshot utility for dashboard visual review.

Usage:
    screenshot <dashboard> [--port PORT] [--output PATH]

Arguments:
    dashboard   One of: labour, explorer, finance
    --port      Temp port to start the dashboard on (default: 19999)
    --output    Output PNG path (default: /tmp/or-screenshot-{dashboard}.png)

Starts the dashboard from current branch code on a temporary port,
waits for it to be ready, takes a full-page screenshot, then stops it.
Prints the output PNG path to stdout on success.

Installed as a CLI command via `pip install -e packages/screenshot`.
"""

import argparse
import os
import signal
import subprocess
import sys
import time

import requests
from playwright.sync_api import sync_playwright

REPO_ROOT = "/opt/open-reporting"
DASHBOARDS_DIR = os.path.join(REPO_ROOT, "products", "dashboards")

STARTUP_TIMEOUT = 60   # seconds to wait for dashboard to become ready (dbr boot)
RENDER_WAIT_MS  = 3000  # milliseconds to wait after page load for JS rendering


def discover_dashboards() -> dict:
    """Scan products/dashboards/ for valid dbr dashboards.

    Returns {name: dashboard_config_path}. A valid dashboard has a
    dashboard.yml at the top level (the dbr project root).
    """
    import yaml
    out = {}
    if not os.path.isdir(DASHBOARDS_DIR):
        return out
    for name in sorted(os.listdir(DASHBOARDS_DIR)):
        project = os.path.join(DASHBOARDS_DIR, name)
        cfg = os.path.join(project, "dashboard.yml")
        if os.path.isfile(cfg):
            try:
                config = yaml.safe_load(open(cfg)) or {}
                if config.get("domain") and config.get("port"):
                    out[name] = project
            except yaml.YAMLError:
                continue
    return out


def is_port_free(port: int) -> bool:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) != 0


def wait_for_ready(port: int, url_path: str, timeout: int) -> bool:
    url = f"http://localhost:{port}{url_path}"
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(url, timeout=2)
            if r.status_code < 500:
                return True
        except Exception:
            pass
        time.sleep(1)
    return False


def take_screenshot(dashboard: str, port: int, output: str) -> bool:
    """Start the dashboard via `dbr serve`, wait for ready, screenshot, then stop.

    `port` is informational only — dbr reads its port from dashboard.yml.
    """
    dashboards = discover_dashboards()
    project_root = dashboards.get(dashboard)
    if not project_root:
        print(
            f"ERROR: unknown dashboard '{dashboard}'. "
            f"Choose from: {', '.join(dashboards) or '<none discovered>'}",
            file=sys.stderr,
        )
        return False

    # Read the port from the project's dashboard.yml so we hit the right one
    import yaml
    config = yaml.safe_load(open(os.path.join(project_root, "dashboard.yml")))
    domain = config["domain"]
    actual_port = int(config["port"])
    url_path = f"/{domain}/"

    proc = subprocess.Popen(
        ["dbr", "serve", project_root],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid,
    )
    port = actual_port

    try:
        print(f"Starting {dashboard} dashboard on port {port}...", file=sys.stderr)
        if not wait_for_ready(port, url_path, STARTUP_TIMEOUT):
            print(f"ERROR: dashboard did not become ready within {STARTUP_TIMEOUT}s", file=sys.stderr)
            return False

        print(f"Dashboard ready. Taking screenshot...", file=sys.stderr)
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1440, "height": 900})
            page.goto(f"http://localhost:{port}{url_path}", wait_until="networkidle")
            page.wait_for_timeout(RENDER_WAIT_MS)
            page.screenshot(path=output, full_page=True)
            browser.close()

        print(f"Screenshot saved: {output}", file=sys.stderr)
        return True

    finally:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        except Exception:
            proc.terminate()


def main():
    dashboards = discover_dashboards()
    parser = argparse.ArgumentParser(description="Take a screenshot of a dbr dashboard for visual review")
    parser.add_argument(
        "dashboard",
        choices=list(dashboards) or None,
        help=f"Dashboard to screenshot (one of: {', '.join(dashboards) or '<none>'})",
    )
    parser.add_argument("--port", type=int, default=19999, help="Informational; port comes from dashboard.yml")
    parser.add_argument("--output", help="Output PNG path (default: /tmp/or-screenshot-{dashboard}.png)")
    args = parser.parse_args()

    output = args.output or f"/tmp/or-screenshot-{args.dashboard}.png"

    success = take_screenshot(args.dashboard, args.port, output)
    if success:
        print(output)
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
