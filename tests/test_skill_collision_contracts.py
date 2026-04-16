from __future__ import annotations

from scripts.generate_openai_yaml import extract_frontmatter, parse_field
from scripts.validate_repo import canonicalize_skill_name
from tests.datacloud_test_utils import ROOT


def iter_skill_files() -> list[tuple[str, str]]:
    skill_pairs: list[tuple[str, str]] = []
    for skill_dir in sorted(path for path in (ROOT / "skills").iterdir() if path.is_dir() and (path / "SKILL.md").is_file()):
        frontmatter = extract_frontmatter((skill_dir / "SKILL.md").read_text(encoding="utf-8"))
        skill_pairs.append((skill_dir.name, parse_field(frontmatter, "name")))
    return skill_pairs


def test_skill_directory_names_do_not_collide_after_repo_normalization() -> None:
    collisions: dict[str, list[str]] = {}

    for directory_name, _ in iter_skill_files():
        canonical_name = canonicalize_skill_name(directory_name)
        collisions.setdefault(canonical_name, []).append(directory_name)

    collisions = {
        canonical_name: sorted(set(names))
        for canonical_name, names in collisions.items()
        if len(set(names)) > 1
    }

    assert not collisions, f"Normalized skill directory collisions detected: {collisions}"


def test_skill_frontmatter_names_do_not_collide_after_repo_normalization() -> None:
    collisions: dict[str, list[str]] = {}

    for _, frontmatter_name in iter_skill_files():
        canonical_name = canonicalize_skill_name(frontmatter_name)
        collisions.setdefault(canonical_name, []).append(frontmatter_name)

    collisions = {
        canonical_name: sorted(set(names))
        for canonical_name, names in collisions.items()
        if len(set(names)) > 1
    }

    assert not collisions, f"Normalized skill frontmatter collisions detected: {collisions}"
