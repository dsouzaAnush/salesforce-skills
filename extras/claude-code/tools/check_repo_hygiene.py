#!/usr/bin/env python3
"""Repository hygiene checks for sf-skills.

Checks tracked Markdown files for:
- broken local Markdown links / anchors
- forbidden placeholder patterns
- stale install instructions / legacy path references

By default, excludes docs/ because whitepaper/export content is managed separately.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[3]

FORBIDDEN_PATTERNS = {
    "placeholder_github_username": r"your-github-username",
    "placeholder_email": r"YOUR_EMAIL",
    "legacy_plugin_install": r"(?:^|\s)(?:claude\s+)?/plugin install\b",
    "legacy_marketplace_path": r"~/.claude/plugins/marketplaces/sf-skills",
}

EXCLUDE_PREFIXES = ("docs/", ".clinerules/")

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
ANCHOR_RE = re.compile(r'<a id="([^"]+)"></a>')


def git_ls_files(*patterns: str) -> list[str]:
    cmd = ["git", "ls-files", *patterns]
    return subprocess.check_output(cmd, cwd=ROOT, text=True).splitlines()


def included_markdown_files(include_docs: bool) -> list[str]:
    files = git_ls_files("*.md")
    if include_docs:
        return files
    return [f for f in files if not f.startswith(EXCLUDE_PREFIXES)]


def normalize_heading_to_slug(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = "".join(
        ch for ch in text if not unicodedata.category(ch).startswith(("P", "S"))
    )
    text = text.replace(" ", "-").strip("-")
    return text


def collect_anchors(files: Iterable[str]) -> dict[str, set[str]]:
    anchors: dict[str, set[str]] = {}
    for rel in files:
        path = ROOT / rel
        aset: set[str] = set()
        for line in path.read_text(errors="ignore").splitlines():
            m = ANCHOR_RE.search(line)
            if m:
                aset.add(m.group(1))
            h = HEADING_RE.match(line)
            if h:
                slug = normalize_heading_to_slug(h.group(2))
                if slug:
                    aset.add(slug)
        anchors[rel] = aset
    return anchors


def strip_fenced_code_blocks(text: str) -> str:
    out: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(line)
    return "\n".join(out)


def check_forbidden_patterns(files: Iterable[str]) -> list[str]:
    issues: list[str] = []
    for rel in files:
        text = (ROOT / rel).read_text(errors="ignore")
        for name, pattern in FORBIDDEN_PATTERNS.items():
            regex = re.compile(pattern)
            for i, line in enumerate(text.splitlines(), 1):
                if regex.search(line):
                    issues.append(f"FORBIDDEN\t{name}\t{rel}:{i}\t{line.strip()}")
    return issues


def check_local_links(files: list[str], anchors: dict[str, set[str]]) -> list[str]:
    issues: list[str] = []
    for rel in files:
        path = ROOT / rel
        text = strip_fenced_code_blocks(path.read_text(errors="ignore"))
        base = path.parent
        for i, line in enumerate(text.splitlines(), 1):
            for raw in LINK_RE.findall(line):
                raw = raw.strip().strip("<>")
                if raw.startswith(("http://", "https://", "mailto:", "tel:", "data:")):
                    continue
                if raw.startswith("#"):
                    anchor = raw[1:]
                    if anchor and anchor not in anchors.get(rel, set()):
                        issues.append(f"ANCHOR\t{rel}:{i}\t{raw}\t-> {rel}")
                    continue
                token = raw.split()[0]
                if "#" in token:
                    rel_target, anchor = token.split("#", 1)
                else:
                    rel_target, anchor = token, None
                if not rel_target:
                    continue
                target = (base / rel_target).resolve()
                if not target.exists():
                    issues.append(
                        f"MISSING\t{rel}:{i}\t{raw}\t-> {target.relative_to(ROOT) if str(target).startswith(str(ROOT)) else target}"
                    )
                    continue
                if anchor:
                    target_rel = None
                    for candidate in files:
                        if (ROOT / candidate).resolve() == target:
                            target_rel = candidate
                            break
                    if target_rel and anchor not in anchors.get(target_rel, set()):
                        issues.append(f"ANCHOR\t{rel}:{i}\t{raw}\t-> {target_rel}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Run sf-skills repository hygiene checks")
    parser.add_argument(
        "--include-docs",
        action="store_true",
        help="Include docs/ in checks (excluded by default)",
    )
    args = parser.parse_args()

    files = included_markdown_files(include_docs=args.include_docs)
    anchors = collect_anchors(files)

    issues = []
    issues.extend(check_forbidden_patterns(files))
    issues.extend(check_local_links(files, anchors))

    if issues:
        print(f"Found {len(issues)} hygiene issue(s):")
        for issue in issues:
            print(issue)
        return 1

    print(f"Hygiene checks passed for {len(files)} Markdown files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
