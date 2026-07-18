#!/usr/bin/env python3
"""Install one generated candidate set with backup, rebuild, and validation."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

from generate_glyph_candidates import OUTPUT_DIR, TARGET_IDS, VERSIONS
from thai_font import MASTER_PATH, ROOT, load_registry, open_indexed, tile_box


BACKUP_DIR = ROOT / "tools/thai/font/recovery/candidate_installs"


def load_candidate(version: str, output_dir: Path = OUTPUT_DIR):
    if version not in VERSIONS:
        raise ValueError(f"candidate {version!r} does not exist; choose {', '.join(VERSIONS)}")
    master = open_indexed(MASTER_PATH)
    candidates = {}
    for glyph_id in TARGET_IDS:
        path = output_dir / version / f"{glyph_id:04x}.png"
        if not path.exists():
            raise ValueError(f"candidate file does not exist: {path}")
        image = open_indexed(path)
        if image.size != (16, 16):
            raise ValueError(f"{path}: expected 16x16, got {image.size}")
        if image.getpalette() != master.getpalette():
            raise ValueError(f"{path}: palette differs from thai_master.png")
        if not set(image.getdata()) <= {0, 1, 2, 3}:
            raise ValueError(f"{path}: unexpected palette index")
        if not any(image.getdata()):
            raise ValueError(f"{path}: candidate glyph is blank")
        candidates[glyph_id] = image
    return candidates


def install_cells(master, candidates):
    result = master.copy()
    for glyph_id in TARGET_IDS:
        result.paste(candidates[glyph_id], tile_box(glyph_id)[:2])
    return result


def install_candidate(version: str) -> Path:
    registry = {glyph.glyph_id: glyph for glyph in load_registry()}
    if any(registry[glyph_id].status != "draft" for glyph_id in TARGET_IDS):
        raise ValueError("target registry entries must remain draft during candidate installation")
    candidates = load_candidate(version)
    master = open_indexed(MASTER_PATH)
    updated = install_cells(master, candidates)
    for glyph_id in range(512):
        if glyph_id not in TARGET_IDS and list(master.crop(tile_box(glyph_id)).getdata()) != list(updated.crop(tile_box(glyph_id)).getdata()):
            raise ValueError(f"installer attempted to change non-target cell 0x{glyph_id:03X}")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = BACKUP_DIR / f"thai_master_before_{version}_{stamp}.png"
    shutil.copy2(MASTER_PATH, backup)
    with tempfile.NamedTemporaryFile(suffix=".png", dir=MASTER_PATH.parent, delete=False) as handle:
        temporary = Path(handle.name)
    try:
        updated.save(temporary, optimize=False)
        temporary.replace(MASTER_PATH)
        subprocess.run(["python3", "-B", "tools/thai/build_thai_font.py"], cwd=ROOT, check=True)
        subprocess.run(["python3", "-B", "tools/thai/validate_thai_font.py"], cwd=ROOT, check=True)
    except Exception:
        shutil.copy2(backup, MASTER_PATH)
        subprocess.run(["python3", "-B", "tools/thai/build_thai_font.py"], cwd=ROOT, check=False)
        raise
    finally:
        temporary.unlink(missing_ok=True)
    print(f"installed {version}; backup: {backup}")
    return backup


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", help="candidate label, for example V03")
    args = parser.parse_args()
    try:
        install_candidate(args.candidate.upper())
        return 0
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
