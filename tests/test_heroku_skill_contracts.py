from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_HEROKU_SKILLS = {
    "sf-heroku-connect": {
        "references/connect-workflows.md",
        "scripts/plugin_status.py",
    },
    "sf-heroku-applink-connections": {
        "references/applink-connections.md",
        "scripts/plugin_status.py",
    },
    "sf-heroku-applink-publications": {
        "references/applink-publications.md",
    },
    "sf-heroku-slack-agents": {
        "references/slack-agent-workflows.md",
        "scripts/project_snapshot.py",
    },
}


def test_heroku_skills_have_expected_contract_files() -> None:
    for skill_name, expected_paths in EXPECTED_HEROKU_SKILLS.items():
        skill_dir = ROOT / "skills" / skill_name
        assert skill_dir.is_dir(), f"Missing skill directory: {skill_dir}"
        assert (skill_dir / "SKILL.md").is_file(), f"Missing SKILL.md: {skill_dir}"
        assert (skill_dir / "agents" / "openai.yaml").is_file(), f"Missing metadata: {skill_dir}"

        for relative_path in expected_paths:
            assert (skill_dir / relative_path).is_file(), f"Missing expected file: {skill_dir / relative_path}"


def test_heroku_skill_frontmatter_matches_directory_name() -> None:
    for skill_name in EXPECTED_HEROKU_SKILLS:
        content = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
        assert f"name: {skill_name}" in content
