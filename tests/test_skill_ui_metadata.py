"""Validate generated agents/openai.yaml metadata for all shipped skills."""
from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_every_skill_has_openai_yaml() -> None:
    skill_dirs = sorted(path for path in (ROOT / "skills").glob("sf-*") if path.is_dir())
    assert skill_dirs

    for skill_dir in skill_dirs:
        metadata_file = skill_dir / "agents" / "openai.yaml"
        assert metadata_file.is_file(), f"Missing metadata: {metadata_file}"


def test_openai_yaml_contains_expected_fields() -> None:
    for skill_dir in sorted(path for path in (ROOT / "skills").glob("sf-*") if path.is_dir()):
        metadata_file = skill_dir / "agents" / "openai.yaml"
        content = metadata_file.read_text(encoding="utf-8")
        skill_name = skill_dir.name

        assert re.search(r'^interface:\n', content, re.MULTILINE)
        assert re.search(r'^  display_name: ".+"\n', content, re.MULTILINE)
        assert re.search(r'^  short_description: ".+"\n', content, re.MULTILINE)
        assert re.search(r'^  icon_small: "\./assets/.+"\n', content, re.MULTILINE)
        assert re.search(r'^  icon_large: "\./assets/.+"\n', content, re.MULTILINE)
        assert re.search(r'^  brand_color: "#0176D3"\n', content, re.MULTILINE)
        assert re.search(rf'^  default_prompt: "Use \${re.escape(skill_name)} .+"\n', content, re.MULTILINE)
        assert "allow_implicit_invocation: true" in content


def test_openai_yaml_icon_paths_exist() -> None:
    for skill_dir in sorted(path for path in (ROOT / "skills").glob("sf-*") if path.is_dir()):
        metadata_file = skill_dir / "agents" / "openai.yaml"
        content = metadata_file.read_text(encoding="utf-8")

        for field in ("icon_small", "icon_large"):
            match = re.search(rf'^  {field}: "(.+)"\n', content, re.MULTILINE)
            assert match, f"Missing {field}: {metadata_file}"
            icon_path = skill_dir / match.group(1).removeprefix("./")
            assert icon_path.is_file(), f"Missing icon asset: {icon_path}"
