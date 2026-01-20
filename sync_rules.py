#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


def copy_rules(source_dir: Path, dest_dir: Path) -> int:
    copied = 0
    for root, dirs, files in os.walk(source_dir):
        root_path = Path(root)
        rel_root = root_path.relative_to(source_dir)
        target_root = dest_dir / rel_root
        target_root.mkdir(parents=True, exist_ok=True)

        for name in files:
            src_file = root_path / name
            dst_file = target_root / name
            shutil.copy2(src_file, dst_file)
            copied += 1
    return copied


def main() -> int:
    repo_root = Path(__file__).resolve().parent
    targets_file = repo_root / ".targets"
    rules_dir = repo_root / "rules"

    targets = []
    for line in targets_file.read_text().splitlines():
        if line == "":
            continue
        targets.append(line)

    if not targets:
        print("No targets found in .targets file.", file=sys.stderr)
        return 1
    
    for raw_target in targets:
        target_path = Path(raw_target)

        if not target_path.is_dir():
            print(f"Warning: target folder not found, skipping {target_path}")
            continue

        dest_dir = (target_path / ".cursor" / "rules").resolve()
        if dest_dir.exists():
            if dest_dir.is_dir():
                shutil.rmtree(dest_dir)
            else:
                dest_dir.unlink()

        dest_dir.mkdir(parents=True, exist_ok=True)
        copied = copy_rules(rules_dir, dest_dir)
        print(f"Copied {copied} files from {rules_dir.resolve()} to {dest_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
