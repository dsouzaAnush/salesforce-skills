from __future__ import annotations

import json
from pathlib import Path
import sys

import pytest

from scripts import validate_repo as validator
from scripts.validate_repo import collect_validation_errors


def test_validate_repo_reports_no_errors() -> None:
    assert collect_validation_errors() == []


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_validate_repo_collects_errors_for_missing_assets(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path
    plugin_manifest = root / ".codex-plugin" / "plugin.json"
    marketplace = root / ".agents" / "plugins" / "marketplace.json"
    root_agent = root / "agents" / "openai.yaml"
    skill_dir = root / "skills" / "sf-demo"

    write_file(
        plugin_manifest,
        json.dumps(
            {
                "name": "sf-skills",
                "skills": "./skills/",
                "interface": {
                    "composerIcon": "./assets/missing.png",
                    "logo": "./assets/missing.png",
                },
            }
        ),
    )
    write_file(
        marketplace,
        json.dumps(
            {
                "plugins": [
                    {
                        "name": "sf-skills",
                        "source": {"path": "./wrong"},
                    }
                ]
            }
        ),
    )
    write_file(
        root_agent,
        """interface:
  display_name: "Salesforce Skills"
  icon_small: "./assets/missing.png"
  icon_large: "./assets/missing.png"
""",
    )
    write_file(skill_dir / "SKILL.md", "---\nname: sf-demo\ndescription: Demo\n---\n")
    write_file(skill_dir / "agents" / "openai.yaml", "stale\n")

    monkeypatch.setattr(validator, "ROOT", root)
    monkeypatch.setattr(validator, "PLUGIN_MANIFEST", plugin_manifest)
    monkeypatch.setattr(validator, "MARKETPLACE", marketplace)
    monkeypatch.setattr(validator, "ROOT_AGENT_METADATA", root_agent)

    errors = validator.collect_validation_errors()

    assert any("missing" in error.lower() for error in errors)
    assert any("stale" in error.lower() for error in errors)


def test_validate_repo_main_success_and_failure(monkeypatch) -> None:
    monkeypatch.setattr(validator, "collect_validation_errors", lambda: [])
    monkeypatch.setattr(sys, "argv", ["validate_repo.py"])
    validator.main()

    monkeypatch.setattr(validator, "collect_validation_errors", lambda: ["bad state"])
    with pytest.raises(SystemExit):
        validator.main()
