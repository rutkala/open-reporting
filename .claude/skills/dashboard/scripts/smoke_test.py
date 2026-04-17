#!/usr/bin/env python3
"""
Smoke test for Open Reporting Dash dashboards.

Starts the dashboard, waits for it to be ready, makes one HTTP request,
reports pass or fail, then shuts down cleanly.

Usage:
    PYTHONPATH=/opt/open-reporting \
    DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb \
    python3 .claude/skills/build-dashboard/scripts/smoke_test.py \
        products/dashboards/{domain}/app.py {port}

Exit codes:
    0 — dashboard started and responded HTTP 200
    1 — dashboard failed to start or returned non-200
"""
import os
import signal
import subprocess
import sys
import time
import urllib.request
import urllib.error


def main():
    if len(sys.argv) < 3:
        print("Usage: smoke_test.py <app_path> <port>")
        sys.exit(1)

    app_path = sys.argv[1]
    port = int(sys.argv[2])
    url = f"http://localhost:{port}/"

    env = os.environ.copy()
    env.setdefault("PYTHONPATH", "/opt/open-reporting")
    env.setdefault("DUCKDB_PATH", "/opt/open-reporting/data/warehouse.duckdb")

    print(f"Starting: {app_path} on port {port}")
    proc = subprocess.Popen(
        [sys.executable, app_path],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Wait up to 15 seconds for the app to be ready
    ready = False
    deadline = time.time() + 15
    while time.time() < deadline:
        time.sleep(1)
        if proc.poll() is not None:
            # Process exited early — capture error output
            _, stderr = proc.communicate()
            print("FAIL — app exited before becoming ready")
            print("--- stderr ---")
            print(stderr.decode(errors="replace"))
            sys.exit(1)
        try:
            with urllib.request.urlopen(url, timeout=2) as resp:
                if resp.status == 200:
                    ready = True
                    break
        except (urllib.error.URLError, ConnectionRefusedError):
            pass  # still starting

    if not ready:
        proc.send_signal(signal.SIGTERM)
        _, stderr = proc.communicate(timeout=5)
        print("FAIL — app did not respond within 15 seconds")
        print("--- stderr ---")
        print(stderr.decode(errors="replace"))
        sys.exit(1)

    # One final request to confirm content is returned
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            body_len = len(resp.read())
    except Exception as e:
        proc.send_signal(signal.SIGTERM)
        proc.wait(timeout=5)
        print(f"FAIL — HTTP request failed: {e}")
        sys.exit(1)

    proc.send_signal(signal.SIGTERM)
    proc.wait(timeout=5)

    print(f"PASS — HTTP 200, {body_len} bytes received from {url}")
    sys.exit(0)


if __name__ == "__main__":
    main()
