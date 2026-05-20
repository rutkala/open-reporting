import os
from pathlib import Path

# Tell theme + layout loaders where this project lives so they pick up
# any local theme.yaml / layout.yaml overrides. Must be set BEFORE
# `or_dashboards` is imported.
os.environ.setdefault("OR_DASHBOARDS_PROJECT_ROOT", str(Path(__file__).resolve().parent))

from or_dashboards.compiler import run_dashboard

run_dashboard(__file__)
