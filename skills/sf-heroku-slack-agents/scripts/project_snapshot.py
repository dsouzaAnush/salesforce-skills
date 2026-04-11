#!/usr/bin/env python3
"""Read-only local readiness snapshot for Slack agents deployed to Heroku."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


ENV_MARKERS = [
    "SLACK_SIGNING_SECRET",
    "SLACK_BOT_TOKEN",
    "SLACK_APP_TOKEN",
]

MANIFEST_CANDIDATES = [
    "manifest.json",
    "manifest.yaml",
    "manifest.yml",
    "manifest.ts",
    "slack-manifest.json",
    "slack-manifest.yaml",
    "slack-manifest.yml",
    ".slack/manifest.json",
    ".slack/manifest.yaml",
    ".slack/manifest.yml",
    ".slack/manifest.ts",
]

SEARCH_EXTENSIONS = {".js", ".cjs", ".mjs", ".ts", ".cts", ".mts"}
SKIP_DIRS = {"node_modules", ".git", ".next", "dist", "build", ".turbo", "coverage"}


def run(cmd: list[str]) -> dict:
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return {
        "command": cmd,
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def load_text(path: Path) -> str:
    try:
        return path.read_text()
    except (UnicodeDecodeError, OSError):
        return ""


def iter_search_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in {"Procfile", "README.md", ".env", ".env.example", ".env.local"}:
            files.append(path)
            continue
        if path.suffix in SEARCH_EXTENSIONS:
            files.append(path)
    return files


def collect_procfile(root: Path) -> dict:
    procfile = root / "Procfile"
    if not procfile.exists():
        return {"exists": False, "process_types": {}, "raw": ""}

    process_types: dict[str, str] = {}
    for line in procfile.read_text().splitlines():
        if ":" not in line:
            continue
        process_type, command = line.split(":", 1)
        process_types[process_type.strip()] = command.strip()

    return {
        "exists": True,
        "process_types": process_types,
        "raw": procfile.read_text(),
    }


def collect_package_json(root: Path) -> dict:
    package_json = root / "package.json"
    if not package_json.exists():
        return {"exists": False}

    try:
        payload = json.loads(package_json.read_text())
    except json.JSONDecodeError:
        return {"exists": True, "valid_json": False}

    deps = payload.get("dependencies", {}) | payload.get("devDependencies", {})
    scripts = payload.get("scripts", {})
    return {
        "exists": True,
        "valid_json": True,
        "dependencies": sorted(deps.keys()),
        "scripts": scripts,
        "bolt_detected": "@slack/bolt" in deps,
        "typescript_detected": "typescript" in deps,
    }


def collect_repo_hints(root: Path) -> dict:
    search_files = iter_search_files(root)
    combined = "\n".join(load_text(path) for path in search_files)

    manifests = [name for name in MANIFEST_CANDIDATES if (root / name).exists()]

    env_mentions = {
        key: (key in combined)
        for key in ENV_MARKERS
    }

    return {
        "manifest_files": manifests,
        "scanned_files": [str(path.relative_to(root)) for path in search_files[:50]],
        "scanned_file_count": len(search_files),
        "mentions_slack_events_path": "/slack/events" in combined,
        "mentions_port_env": "process.env.PORT" in combined or "PORT" in combined,
        "env_var_mentions": env_mentions,
        "mentions_socket_mode": (
            "socketMode" in combined
            or "SocketModeReceiver" in combined
            or "SLACK_APP_TOKEN" in combined
        ),
        "mentions_signing_secret": "signingSecret" in combined or "SLACK_SIGNING_SECRET" in combined,
        "mentions_bolt_app": "@slack/bolt" in combined or "new App(" in combined,
    }


def guess_transport(procfile: dict, repo_hints: dict) -> str:
    process_types = procfile.get("process_types", {})
    if "web" in process_types and "worker" not in process_types:
        return "http"
    if "worker" in process_types and "web" not in process_types:
        return "socket-mode"
    if repo_hints["mentions_socket_mode"] and not repo_hints["mentions_slack_events_path"]:
        return "socket-mode"
    if repo_hints["mentions_slack_events_path"] or repo_hints["mentions_signing_secret"]:
        return "http"
    return "unknown"


def build_recommendations(procfile: dict, repo_hints: dict, package_json: dict, mode: str) -> list[str]:
    recommendations: list[str] = []
    if not package_json.get("exists"):
        recommendations.append("No package.json found; confirm this is a Node-based Slack app before using this skill.")
    elif not package_json.get("bolt_detected") and not repo_hints.get("mentions_bolt_app"):
        recommendations.append("Bolt for JavaScript was not detected; verify whether this repo uses another Slack framework and stop if it is not a Bolt JS or TS app.")

    if mode == "http" and not procfile.get("process_types", {}).get("web"):
        recommendations.append("HTTP mode usually needs a Procfile with a web process.")
    if mode == "socket-mode" and not procfile.get("process_types", {}).get("worker"):
        recommendations.append("Socket Mode on Heroku usually needs a worker process in Procfile.")
    if mode == "http" and not repo_hints["mentions_port_env"]:
        recommendations.append("HTTP mode should bind the server to process.env.PORT for Heroku.")
    if mode == "http" and not repo_hints["env_var_mentions"]["SLACK_SIGNING_SECRET"]:
        recommendations.append("HTTP mode should verify Slack requests with SLACK_SIGNING_SECRET.")
    if mode == "socket-mode" and not repo_hints["env_var_mentions"]["SLACK_APP_TOKEN"]:
        recommendations.append("Socket Mode usually requires SLACK_APP_TOKEN.")
    if repo_hints["manifest_files"] == []:
        recommendations.append("No Slack manifest file was found; be ready to update app settings manually.")
    return recommendations


def main() -> None:
    root = Path.cwd()
    heroku_path = shutil.which("heroku")
    procfile = collect_procfile(root)
    package_json = collect_package_json(root)
    repo_hints = collect_repo_hints(root)
    deployment_mode_guess = guess_transport(procfile, repo_hints)

    payload = {
        "cwd": str(root),
        "heroku_cli_installed": bool(heroku_path),
        "auth_check": run(["heroku", "auth:whoami"]) if heroku_path else None,
        "package_json": package_json,
        "procfile": procfile,
        "repo_hints": repo_hints,
        "deployment_mode_guess": deployment_mode_guess,
        "recommendations": build_recommendations(
            procfile,
            repo_hints,
            package_json,
            deployment_mode_guess,
        ),
        "notes": [
            "This helper is read-only.",
            "Use it from the target project root to inspect Procfile, package.json, TypeScript or JavaScript Slack files, and common Bolt deployment hints.",
        ],
    }

    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
