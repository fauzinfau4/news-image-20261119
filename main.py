#!/usr/bin/env python3
"""Copy the baked-in news poster to the grader's output location.

The poster (entry.png) was rendered at build time by draw.py. This
entrypoint only copies bytes, so both graded runs write identical
output with no network, no clock and no third-party packages.
"""

from os import environ
from pathlib import Path

SOURCE_NAME = "entry.png"
DEFAULT_OUTPUT = Path("/output") / SOURCE_NAME


def resolve_destination() -> Path:
    raw = environ.get("MAKEFUN_OUTPUT_DIR", "")
    if not raw:
        return DEFAULT_OUTPUT
    target = Path(raw)
    if target.suffix == ".png":
        return target
    return target / SOURCE_NAME


def main() -> None:
    here = Path(__file__).resolve().parent
    source = here / SOURCE_NAME
    destination = resolve_destination()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(source.read_bytes())


if __name__ == "__main__":
    main()
