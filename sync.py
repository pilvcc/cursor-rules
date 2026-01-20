#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


def main():
    repo_root = Path(__file__).resolve().parent
    targets_file = repo_root / ".targets"
    rules_dir = repo_root / "rules"

    targets = []
    for line in targets_file.read_text().splitlines():
        if line == "" or line.startswith("#"):
            continue
        targets.append(line)

    for raw_target in targets:
        target_path = Path(raw_target)

        dest_dir = (target_path / ".cursor" / "rules").resolve()
        if dest_dir.exists():
            if dest_dir.is_dir():
                shutil.rmtree(dest_dir)
            else:
                dest_dir.unlink()

        dest_dir.mkdir(parents=True, exist_ok=True)

        copied = 0
        for root, dirs, files in os.walk(rules_dir):
            root_path = Path(root)
            rel_root = root_path.relative_to(rules_dir)
            target_root = dest_dir / rel_root
            target_root.mkdir(parents=True, exist_ok=True)

            for name in files:
                src_file = root_path / name
                dst_file = target_root / name
                shutil.copy2(src_file, dst_file)
                copied += 1

        print(f"Copied {copied} files from {rules_dir.resolve()} to {dest_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
