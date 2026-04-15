---
name: adl-create
description: Create a new Agentforce Data Library (SFDRIVE type) and wait until it is ready for file uploads. Use when the user wants to create an ADL or data library.
user-invocable: true
allowed-tools: Bash(sf *) Bash(curl *) Bash(jq *) Read
argument-hint: "<library_name> [--org <alias>]"
---

# Create Agentforce Data Library

Create a new SFDRIVE-type Agentforce Data Library and poll until it is ready for file uploads.

## Arguments

Parse the arguments from: $ARGUMENTS

- `library_name` (required) — the masterLabel AND developerName for the library. Spaces in the label are replaced with `_` for developerName.
- `--org <alias>` (optional) — the sf CLI org alias to use. Overrides both `~/.claude/d360_org` and the sf CLI default.

## Steps

### 1. Get Access Token

Resolve the org alias using this priority:
1. If `--org` was provided as an argument, use that.
2. Otherwise, check if `~/.claude/d360_org` exists and read the alias from it.
3. Otherwise, detect the sf CLI default org:
   ```bash
   sf config get target-org --json
   ```
   Extract `.result[0].value` as the org alias.

If none of the above yields an alias, tell the user to either:
- Run `/d360-set-org <alias>` to set a default for d360 skills
- Pass `--org <alias>` to this skill
- Or set the sf CLI default: `sf config set target-org <alias>`

Then get the access token:

```bash
sf org display --target-org <alias> --json
```

Extract `.result.accessToken` and `.result.instanceUrl` from the JSON output.
If this fails, tell the user to authenticate first:
```
sf org login web --instance-url <instance_url> --set-default --alias <alias>
```

### 2. Create the Library

```bash
curl -s -X POST "<instanceUrl>/services/data/v66.0/einstein/data-libraries" \
  -H "Authorization: Bearer <accessToken>" \
  -H "Content-Type: application/json" \
  -d '{
    "masterLabel": "<library_name>",
    "developerName": "<developer_name>",
    "groundingSource": {
      "sourceType": "SFDRIVE"
    }
  }'
```

Extract `libraryId` from the response. If the response contains an error, show it and stop.

### 3. Poll Upload Readiness

Poll until ready (max 24 attempts, 5 seconds apart):

```bash
curl -s "<instanceUrl>/services/data/v66.0/einstein/data-libraries/<libraryId>/upload-readiness" \
  -H "Authorization: Bearer <accessToken>"
```

Check `.ready == true` in the response.

### 4. Report Results

When done, report:
- Library ID
- Library Name / Developer Name
- Status: READY or TIMED OUT
- The org alias used

If readiness times out after 2 minutes, report the library was created but is not yet ready, and suggest the user retry or check status later.
