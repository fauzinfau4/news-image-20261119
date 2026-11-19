"""Ship the rendered front page to the output folder.

Reads nothing but the PNG sitting next to this file and copies its
bytes to $MAKEFUN_OUTPUT_DIR (falling back to /output). Standard
library only: no network, no clock, no image work here.
"""

import os
import shutil

from pathlib import Path

HERE = Path(__file__).resolve().parent
PNG_NAME = "entry.png"
FALLBACK_DIR = Path("/output")


def pick_target():
    """Work out where the finished PNG has to land."""
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    base = Path(raw) if raw else FALLBACK_DIR
    return base / PNG_NAME


def ship_poster():
    """Copy entry.png byte-for-byte to the target folder."""
    source = HERE / PNG_NAME
    target = pick_target()
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    print("Wrote " + str(target) + " (" +
          str(target.stat().st_size) + " bytes)")


ship_poster()
