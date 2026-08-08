"""Compatibility entry point: K3C supersedes K3A's direct-font prototype."""

import runpy
from pathlib import Path


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[3]
    runpy.run_path(
        str(root / "tools/thai/tests/test_thai_naming_keyboard_k3c.py"),
        run_name="__main__",
    )
