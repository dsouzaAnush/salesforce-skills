---
name: set-org
description: Set or view the default Salesforce org alias used by all d360 ADL skills. Supports setting by existing alias or logging in via instance URL with OAuth. Persists to ~/.claude/d360_org so it carries across conversations.
user-invocable: true
allowed-tools: Bash(sf *) Bash(rm *) Read Write
argument-hint: "<org_alias_or_instance_url> [--alias <name>] | --show | --clear"
---

# Set Default Org for d360 Skills

Set, view, or clear the default Salesforce org alias that all d360 ADL skills use. Supports both existing org aliases and new OAuth login via instance URL.

## Arguments

Parse the arguments from: $ARGUMENTS

- `org_alias` — an existing sf CLI org alias to set as default.
- `instance_url` — a Salesforce instance URL (starts with `https://`). Triggers OAuth web login flow.
- `--alias <name>` (optional, used with instance URL) — the alias to assign to the newly authenticated org. If omitted, prompt the user to provide one.
- `--show` — display the currently configured org (if any).
- `--clear` — remove the saved org so skills fall back to `sf config get target-org`.

If no arguments are provided, treat as `--show`.

## Steps

### If `--show` or no arguments

1. Check if `~/.claude/d360_org` exists. If it does, read and display the saved alias.
2. Also show the sf CLI default org for comparison:
   ```bash
   sf config get target-org --json
   ```
3. Report both values so the user can see what's active.

### If `--clear`

1. Delete `~/.claude/d360_org` if it exists.
2. Confirm that d360 skills will now fall back to the sf CLI default org.

### If an instance URL is provided (starts with `https://`)

This triggers an OAuth web login flow to authenticate a new org.

1. Determine the alias:
   - If `--alias <name>` was provided, use that.
   - Otherwise, ask the user what alias they'd like to use.

2. Run the OAuth web login. Tell the user a browser window will open for them to log in:
   ```bash
   sf org login web --instance-url <instance_url> --alias <alias>
   ```
   This opens a browser for the user to authenticate. Wait for the command to complete.

3. If the login succeeds, verify the org is accessible:
   ```bash
   sf org display --target-org <alias> --json
   ```
   Extract the instance URL and username from the output.

4. Write the alias to `~/.claude/d360_org`:
   ```
   <alias>
   ```

5. Confirm the org was authenticated and set as the d360 default.

### If an org alias is provided (does not start with `https://`)

1. Validate the alias exists by running:
   ```bash
   sf org display --target-org <org_alias> --json
   ```
   If this fails, tell the user the alias is not recognized and suggest either:
   - Passing an instance URL to trigger OAuth login: `/d360-set-org https://your-instance.salesforce.com --alias my_org`
   - Or authenticating manually: `sf org login web --instance-url <url> --alias <alias>`

2. Write the alias to `~/.claude/d360_org`:
   ```
   <org_alias>
   ```

3. Confirm the org was set and show the instance URL from the display output.

## Report

Show:
- The saved d360 org alias (or "not set" if cleared/absent)
- The sf CLI default org (for reference)
- Instance URL and username of the saved org (if set)
- A reminder that `--org <alias>` on any skill overrides both

## Examples

**Set by existing alias:**
```
/d360-set-org my_sandbox
```

**Login via instance URL and set as default:**
```
/d360-set-org https://mycompany.my.salesforce.com --alias my_prod
```

**View current config:**
```
/d360-set-org --show
```

**Clear saved org:**
```
/d360-set-org --clear
```
