#!/usr/bin/env python3
"""Validate repo-root skill and plugin metadata contracts."""

from __future__ import annotations

import json
from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.generate_openai_yaml import build_yaml, extract_frontmatter, parse_field
else:
    from .generate_openai_yaml import build_yaml, extract_frontmatter, parse_field


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_MANIFEST = ROOT / ".codex-plugin" / "plugin.json"
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
ROOT_AGENT_METADATA = ROOT / "agents" / "openai.yaml"


def iter_skill_dirs() -> list[Path]:
    return sorted(path for path in (ROOT / "skills").iterdir() if path.is_dir() and (path / "SKILL.md").is_file())


def canonicalize_skill_name(skill_name: str) -> str:
    normalized = skill_name.strip().lower().replace("_", "-")
    if normalized.startswith("data360-"):
        return f"d360-{normalized.removeprefix('data360-')}"
    return normalized


def parse_openai_yaml(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    in_interface = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if not line:
            continue
        if line == "interface:":
            in_interface = True
            continue
        if in_interface and not raw_line.startswith("  "):
            break
        if not in_interface:
            continue
        key, _, value = line.strip().partition(":")
        if key and value:
            data[key] = value.strip().strip("\"'")
    return data


def validate_plugin_manifest() -> list[str]:
    errors: list[str] = []
    manifest = json.loads(PLUGIN_MANIFEST.read_text(encoding="utf-8"))

    if manifest.get("name") != "sf-skills":
        errors.append("Plugin manifest name must be sf-skills")
    if manifest.get("skills") != "./skills/":
        errors.append("Plugin manifest must point skills at ./skills/")

    interface = manifest.get("interface", {})
    for field in ("composerIcon", "logo"):
        asset = interface.get(field)
        if not asset:
            errors.append(f"Plugin manifest is missing interface.{field}")
            continue
        asset_path = ROOT / asset.removeprefix("./")
        if not asset_path.is_file():
            errors.append(f"Plugin manifest asset is missing: {asset_path}")

    return errors


def validate_marketplace() -> list[str]:
    errors: list[str] = []
    marketplace = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    plugins = marketplace.get("plugins", [])
    if not plugins:
        return ["Marketplace must contain at least one plugin entry"]

    plugin_entry = plugins[0]
    if plugin_entry.get("name") != "sf-skills":
        errors.append("Marketplace first plugin entry must be sf-skills")
    plugin_root = (MARKETPLACE.parent / plugin_entry["source"]["path"]).resolve()
    if plugin_root != ROOT.resolve():
        errors.append("Marketplace source path does not resolve back to the repo root")
    return errors


def validate_root_agent_metadata() -> list[str]:
    errors: list[str] = []
    metadata = parse_openai_yaml(ROOT_AGENT_METADATA)
    for field in ("icon_small", "icon_large"):
        asset = metadata.get(field)
        if not asset:
            errors.append(f"Root agent metadata is missing {field}")
            continue
        asset_path = ROOT / asset.removeprefix("./")
        if not asset_path.is_file():
            errors.append(f"Root agent metadata asset is missing: {asset_path}")
    return errors


def validate_skill_metadata() -> list[str]:
    errors: list[str] = []
    for skill_dir in sorted(path for path in (ROOT / "skills").glob("sf-*") if path.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        metadata_file = skill_dir / "agents" / "openai.yaml"
        if not skill_file.exists():
            errors.append(f"Missing SKILL.md: {skill_file}")
            continue
        if not metadata_file.exists():
            errors.append(f"Missing agents/openai.yaml: {metadata_file}")
            continue

        frontmatter = extract_frontmatter(skill_file.read_text(encoding="utf-8"))
        skill_name = parse_field(frontmatter, "name")
        description = parse_field(frontmatter, "description")
        expected_yaml = build_yaml(skill_name, description)
        current_yaml = metadata_file.read_text(encoding="utf-8")

        if skill_name != skill_dir.name:
            errors.append(f"Skill frontmatter name does not match directory: {skill_dir.name}")
        if current_yaml != expected_yaml:
            errors.append(f"Generated metadata is stale: {metadata_file}")

        metadata = parse_openai_yaml(metadata_file)
        for field in ("icon_small", "icon_large"):
            asset = metadata.get(field)
            if not asset:
                errors.append(f"Skill metadata is missing {field}: {metadata_file}")
                continue
            asset_path = skill_dir / asset.removeprefix("./")
            if not asset_path.is_file():
                errors.append(f"Skill icon asset is missing: {asset_path}")

    return errors


def validate_skill_name_collisions() -> list[str]:
    errors: list[str] = []
    raw_names_by_canonical: dict[str, set[str]] = {}
    owning_dirs_by_canonical: dict[str, set[str]] = {}

    for skill_dir in iter_skill_dirs():
        frontmatter = extract_frontmatter((skill_dir / "SKILL.md").read_text(encoding="utf-8"))
        skill_name = parse_field(frontmatter, "name")

        for raw_name in {skill_dir.name, skill_name}:
            canonical_name = canonicalize_skill_name(raw_name)
            raw_names_by_canonical.setdefault(canonical_name, set()).add(raw_name)
            owning_dirs_by_canonical.setdefault(canonical_name, set()).add(skill_dir.name)

    for canonical_name, owning_dirs in sorted(owning_dirs_by_canonical.items()):
        if len(owning_dirs) < 2:
            continue
        variants = ", ".join(sorted(raw_names_by_canonical[canonical_name]))
        errors.append(
            f"Skill naming collision after normalization for '{canonical_name}': {variants}"
        )

    return errors


def collect_validation_errors() -> list[str]:
    errors: list[str] = []
    errors.extend(validate_plugin_manifest())
    errors.extend(validate_marketplace())
    errors.extend(validate_root_agent_metadata())
    errors.extend(validate_skill_metadata())
    errors.extend(validate_skill_name_collisions())
    return errors


def main() -> None:
    errors = collect_validation_errors()
    if errors:
        raise SystemExit("\n".join(errors))
    print("Validated sf-skills")


if __name__ == "__main__":
    main()
