#!/usr/bin/env python3
"""Generate minimal agents/openai.yaml metadata for every sf-* skill."""

from __future__ import annotations

from pathlib import Path
import re
import shutil


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
ROOT_ICON = ROOT / "assets" / "salesforce-logo.png"
SKILL_ICON_NAME = "salesforce-logo.png"
BRAND_COLOR = "#0176D3"


def extract_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md is missing YAML frontmatter")
    _, frontmatter, _ = text.split("---\n", 2)
    return frontmatter


def parse_field(frontmatter: str, key: str) -> str:
    lines = frontmatter.splitlines()
    prefix = f"{key}:"
    for index, line in enumerate(lines):
        if not line.startswith(prefix):
            continue

        value = line[len(prefix):].strip()
        if value and value not in {">", "|"}:
            return value.strip("\"'")

        collected: list[str] = []
        for next_line in lines[index + 1 :]:
            if not next_line.startswith((" ", "\t")):
                break
            collected.append(next_line.strip())
        return " ".join(part for part in collected if part)

    raise ValueError(f"Missing frontmatter field: {key}")


def to_display_name(skill_name: str) -> str:
    parts = skill_name.split("-")
    replacements = {
        "sf": "Salesforce",
        "ai": "AI",
        "agentforce": "Agentforce",
        "agentscript": "Agent Script",
        "applink": "AppLink",
        "datacloud": "Data Cloud",
        "heroku": "Heroku",
        "lwc": "LWC",
        "soql": "SOQL",
        "slack": "Slack",
        "cme": "CME",
        "epc": "EPC",
        "omnistudio": "OmniStudio",
        "omniscript": "OmniScript",
        "commoncore": "CommonCore",
        "vlocity": "Vlocity",
        "nanobananapro": "Nano Banana Pro",
    }
    return " ".join(replacements.get(part, part.capitalize()) for part in parts)


def sanitize(text: str) -> str:
    text = text.replace("→", " to ")
    text = re.sub(r"\s+", " ", text).strip()
    return text.encode("ascii", "ignore").decode("ascii")


def collapse_description(description: str) -> str:
    description = sanitize(description)
    if len(description) <= 64:
        return description
    return description[:61].rstrip() + "..."


def default_prompt(skill_name: str, display_name: str) -> str:
    return f"Use ${skill_name} for help with {display_name} work."


def ensure_skill_icon(skill_dir: Path) -> None:
    assets_dir = skill_dir / "assets"
    assets_dir.mkdir(exist_ok=True)
    shutil.copy2(ROOT_ICON, assets_dir / SKILL_ICON_NAME)


def build_yaml(skill_name: str, description: str) -> str:
    display_name = to_display_name(skill_name)
    short_description = collapse_description(description)
    prompt = default_prompt(skill_name, display_name)
    return (
        "interface:\n"
        f'  display_name: "{display_name}"\n'
        f'  short_description: "{short_description}"\n'
        f'  icon_small: "./assets/{SKILL_ICON_NAME}"\n'
        f'  icon_large: "./assets/{SKILL_ICON_NAME}"\n'
        f'  brand_color: "{BRAND_COLOR}"\n'
        f'  default_prompt: "{prompt}"\n'
        "\n"
        "policy:\n"
        "  allow_implicit_invocation: true\n"
    )


def main() -> None:
    for skill_dir in sorted(SKILLS_DIR.glob("sf-*")):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        frontmatter = extract_frontmatter(skill_file.read_text(encoding="utf-8"))
        skill_name = parse_field(frontmatter, "name")
        description = parse_field(frontmatter, "description")
        ensure_skill_icon(skill_dir)

        agents_dir = skill_dir / "agents"
        agents_dir.mkdir(exist_ok=True)
        output = agents_dir / "openai.yaml"
        output.write_text(build_yaml(skill_name, description), encoding="utf-8")


if __name__ == "__main__":
    main()
