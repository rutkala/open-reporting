#!/usr/bin/env python3
"""
gugik_geo WFS extractor.
Delegates to generic wfs_extractor.py for OGC WFS data.
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
WFS_EXTRACTOR_PATH = REPO_ROOT / "products/ingestion/extractors/wfs_extractor.py"

# Ensure wfs_extractor.py is in the Python path
sys.path.insert(0, str(WFS_EXTRACTOR_PATH.parent))

try:
    from wfs_extractor import main
except ImportError as e:
    print(f"Error importing wfs_extractor: {e}")
    print(f"Please ensure {WFS_EXTRACTOR_PATH} is accessible.")
    sys.exit(1)

if __name__ == "__main__":
    # Call the main function from wfs_extractor.py,
    # specifically for the 'gugik_geo' source.
    # The 'list_only' argument is passed through from sys.argv
    # or defaults to False if not present.
    # We need to adapt this to use argparse correctly,
    # replicating how wfs_extractor.py takes arguments.

    # This is a simplified approach, a more robust solution would
    # involve duplicating argparse setup or modifying wfs_extractor.py
    # to accept an explicit source list more easily.
    # For now, let's assume wfs_extractor.py is run directly.

    # This wrapper should call wfs_extractor.py as a subprocess.
    import subprocess
    cmd = [sys.executable, str(WFS_EXTRACTOR_PATH), "--sources", "gugik_geo"]
    if "--list" in sys.argv:
        cmd.append("--list")

    result = subprocess.run(cmd)
    sys.exit(result.returncode)
