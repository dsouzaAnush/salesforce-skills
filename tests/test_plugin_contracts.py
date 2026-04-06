"""Contract tests for the repo-root Codex plugin packaging."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_MANIFEST = ROOT / ".codex-plugin" / "plugin.json"
MARKETPLACE_FILE = ROOT / ".agents" / "plugins" / "marketplace.json"


def test_plugin_manifest_points_at_repo_skills_dir() -> None:
    manifest = json.loads(PLUGIN_MANIFEST.read_text(encoding="utf-8"))

    assert manifest["name"] == "sf-skills"
    assert manifest["skills"] == "./skills/"
    assert (ROOT / manifest["skills"].removeprefix("./")).is_dir()


def test_marketplace_entry_resolves_back_to_plugin_root() -> None:
    marketplace = json.loads(MARKETPLACE_FILE.read_text(encoding="utf-8"))
    plugin_entry = marketplace["plugins"][0]

    assert plugin_entry["name"] == "sf-skills"

    plugin_root = (MARKETPLACE_FILE.parent / plugin_entry["source"]["path"]).resolve()
    assert plugin_root == ROOT.resolve()
    assert (plugin_root / ".codex-plugin" / "plugin.json").is_file()
