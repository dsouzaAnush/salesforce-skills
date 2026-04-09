#!/usr/bin/env python3
"""Sync sf-* skills from the upstream Jaganpro/sf-skills repository.

This script intentionally replaces local upstream-owned skill content with the
canonical source tree, then regenerates the local Codex metadata layer.
Compatibility additions such as agents/openai.yaml are allowed; edits to the
shared upstream files are not.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.generate_openai_yaml import main as generate_openai_yaml
else:
    from .generate_openai_yaml import main as generate_openai_yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
DEFAULT_UPSTREAM = Path(
    os.getenv("SALESFORCE_SKILLS_SOURCE", "/tmp/jaganpro-sf-skills")
).resolve()
DEFAULT_UPSTREAM_REPOSITORY = "https://github.com/Jaganpro/sf-skills"


def discover_upstream_skills(upstream_root: Path) -> list[Path]:
    upstream_skills_dir = upstream_root / "skills"
    return sorted(path for path in upstream_skills_dir.glob("sf-*") if path.is_dir())


def sync_skill(upstream_skill_dir: Path) -> None:
    destination = SKILLS_DIR / upstream_skill_dir.name
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(upstream_skill_dir, destination)


def remove_stale_skills(expected_skill_names: set[str]) -> None:
    for skill_dir in sorted(path for path in SKILLS_DIR.glob("sf-*") if path.is_dir()):
        if skill_dir.name not in expected_skill_names:
            shutil.rmtree(skill_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync sf-* skills from the upstream skills repo")
    parser.add_argument(
        "--upstream",
        default=str(DEFAULT_UPSTREAM),
        help="Path to the upstream Jaganpro/sf-skills repo",
    )
    parser.add_argument(
        "--upstream-repository",
        default=DEFAULT_UPSTREAM_REPOSITORY,
        help="Public repository URL for the upstream skills repo",
    )
    args = parser.parse_args()

    upstream_root = Path(args.upstream).resolve()
    if not upstream_root.is_dir():
        raise SystemExit(f"Upstream repo not found: {upstream_root}")

    skill_dirs = discover_upstream_skills(upstream_root)
    if not skill_dirs:
        raise SystemExit(f"No sf-* skills found in: {upstream_root / 'skills'}")

    SKILLS_DIR.mkdir(exist_ok=True)
    remove_stale_skills({path.name for path in skill_dirs})
    for skill_dir in skill_dirs:
        sync_skill(skill_dir)

    # Rebuild the additive Codex metadata layer after restoring upstream skill content.
    generate_openai_yaml()
    print(
        f"Synced {len(skill_dirs)} skills from {upstream_root} "
        f"using source-of-truth {args.upstream_repository}"
    )


if __name__ == "__main__":
    main()
