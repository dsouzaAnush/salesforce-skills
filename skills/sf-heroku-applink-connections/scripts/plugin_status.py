#!/usr/bin/env python3
"""Inspect local Heroku AppLink plugin availability without mutating state."""

from __future__ import annotations

import json
import shutil
import subprocess


def run(cmd: list[str]) -> dict:
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return {
        "command": cmd,
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def main() -> None:
    heroku_path = shutil.which("heroku")
    plugins = run(["heroku", "plugins", "--json"]) if heroku_path else None
    salesforce_help = run(["heroku", "help", "salesforce:connect"]) if heroku_path else None
    payload = {
        "heroku_cli_installed": bool(heroku_path),
        "heroku_path": heroku_path,
        "plugins": plugins,
        "salesforce_connect_help": salesforce_help,
        "notes": [
            "This helper is read-only.",
            "Install the AppLink plugin with `heroku plugins:install @heroku-cli/plugin-applink` when Salesforce or Data Cloud commands are unavailable.",
        ],
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
