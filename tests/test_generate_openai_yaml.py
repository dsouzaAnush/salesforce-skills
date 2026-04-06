from __future__ import annotations

from pathlib import Path
import sys

import pytest

from scripts import generate_openai_yaml as generator
from scripts.generate_openai_yaml import build_yaml, collapse_description, extract_frontmatter, parse_field


def test_build_yaml_includes_branding_fields() -> None:
    output = build_yaml("sf-apex", "Generates and reviews Salesforce Apex code.")

    assert 'icon_small: "./assets/salesforce-logo.png"' in output
    assert 'icon_large: "./assets/salesforce-logo.png"' in output
    assert 'brand_color: "#0176D3"' in output
    assert 'default_prompt: "Use $sf-apex for help with Salesforce Apex work."' in output


def test_collapse_description_truncates_long_text() -> None:
    description = "A" * 90
    assert collapse_description(description).endswith("...")
    assert len(collapse_description(description)) == 64


def test_extract_frontmatter_and_parse_field_handle_multiline_descriptions() -> None:
    text = """---\nname: sf-demo\ndescription: >\n  Demo skill.\n  Trigger on demo work.\n---\n\n# Demo\n"""
    frontmatter = extract_frontmatter(text)

    assert parse_field(frontmatter, "name") == "sf-demo"
    assert parse_field(frontmatter, "description") == "Demo skill. Trigger on demo work."


def test_extract_frontmatter_raises_without_frontmatter() -> None:
    with pytest.raises(ValueError):
        extract_frontmatter("# Demo\n")


def test_main_writes_metadata_and_copies_logo(tmp_path: Path, monkeypatch) -> None:
    skills_dir = tmp_path / "skills"
    skill_dir = skills_dir / "sf-demo"
    icon_file = tmp_path / "assets" / "salesforce-logo.png"

    icon_file.parent.mkdir(parents=True, exist_ok=True)
    icon_file.write_bytes(b"logo")
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        """---
name: sf-demo
description: >
  Demo skill for generation tests.
---

# Demo
""",
        encoding="utf-8",
    )

    monkeypatch.setattr(generator, "SKILLS_DIR", skills_dir)
    monkeypatch.setattr(generator, "ROOT_ICON", icon_file)
    monkeypatch.setattr(sys, "argv", ["generate_openai_yaml.py"])

    generator.main()

    metadata = (skill_dir / "agents" / "openai.yaml").read_text(encoding="utf-8")
    assert 'display_name: "Salesforce Demo"' in metadata
    assert (skill_dir / "assets" / "salesforce-logo.png").is_file()
