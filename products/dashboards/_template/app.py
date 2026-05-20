import os
from pathlib import Path

# Tell theme + layout loaders where this project lives so they pick up
# any local theme.yaml / layout.yaml overrides. Must be set BEFORE
# `dbr` is imported.
os.environ.setdefault("DBR_PROJECT_ROOT", str(Path(__file__).resolve().parent))

from dbr.compiler import run_dashboard

run_dashboard(__file__)
