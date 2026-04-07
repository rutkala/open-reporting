#!/usr/bin/env python3
"""
Screenshot utility for dashboard visual review.

Usage:
    python3 tools/screenshot.py <dashboard> [--port PORT] [--output PATH]

Arguments:
    dashboard   One of: labour, explorer, finance
    --port      Temp port to start the dashboard on (default: 19999)
    --output    Output PNG path (default: /tmp/or-screenshot-{dashboard}.png)

Starts the dashboard from current branch code on a temporary port,
waits for it to be ready, takes a full-page screenshot, then stops it.
Prints the output PNG path to stdout on success.
"""

import argparse
import os
import signal
import subprocess
import sys
import time

import requests
from playwright.sync_api import sync_playwright

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DASHBOARDS = {
    "labour":   ("products/dashboards/labour/app.py",   "/labour/"),
    "explorer": ("products/dashboards/explorer/app.py", "/explorer/"),
    "finance":  ("products/dashboards/finance/app.py",  "/finance/"),
}

STARTUP_TIMEOUT = 40   # seconds to wait for dashboard to become ready
RENDER_WAIT_MS  = 3000  # milliseconds to wait after page load for JS rendering


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
    entry = DASHBOARDS.get(dashboard)
    if not entry:
        print(f"ERROR: unknown dashboard '{dashboard}'. Choose from: {', '.join(DASHBOARDS)}", file=sys.stderr)
        return False

    app_path, url_path = entry
    full_app_path = os.path.join(REPO_ROOT, app_path)
    if not os.path.exists(full_app_path):
        print(f"ERROR: dashboard file not found: {full_app_path}", file=sys.stderr)
        return False

    # Check port availability; try fallback
    if not is_port_free(port):
        fallback = port - 1
        if not is_port_free(fallback):
            print(f"ERROR: ports {port} and {fallback} are both in use", file=sys.stderr)
            return False
        print(f"Port {port} in use, using {fallback}", file=sys.stderr)
        port = fallback

    env = os.environ.copy()
    env["PYTHONPATH"] = REPO_ROOT
    env["OR_PORT"] = str(port)

    proc = subprocess.Popen(
        [sys.executable, full_app_path],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid,
    )

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
    parser = argparse.ArgumentParser(description="Take a screenshot of a dashboard for visual review")
    parser.add_argument("dashboard", choices=list(DASHBOARDS), help="Dashboard to screenshot")
    parser.add_argument("--port", type=int, default=19999, help="Temp port (default: 19999)")
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
