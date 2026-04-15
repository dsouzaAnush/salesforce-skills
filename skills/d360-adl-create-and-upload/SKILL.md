---
name: adl-create-and-upload
description: Create a new Agentforce Data Library, wait for readiness, upload files, and trigger indexing — all in one step. Use when the user wants to create an ADL and upload files in one go.
user-invocable: true
allowed-tools: Bash(sf *) Bash(curl *) Bash(jq *) Bash(stat *) Read
argument-hint: "<library_name> <file_path> [--org <alias>]"
---

# Create Agentforce Data Library and Upload Files

End-to-end flow: create a new SFDRIVE library, wait for readiness, upload a file, and trigger indexing.

## Arguments

Parse the arguments from: $ARGUMENTS

- `library_name` (required) — the masterLabel for the library. Spaces are replaced with `_` for developerName.
- `file_path` (required) — absolute path to the file to upload. May also be a Slack file reference (see Step 0).
- `--org <alias>` (optional) — the sf CLI org alias to use. Overrides both `~/.claude/d360_org` and the sf CLI default.

## Steps

### 0. Resolve File (Slack files only)

Only use this step when the skill is being used from Slack and the user provides a Slack file reference (for example a `[Slack file: ...]` attachment, a Slack file ID like `F0AT38Y3B6J`, or a `files.slack.com` URL).

If `file_path` is already a normal local path, skip this step entirely. A Slack bot token is not required for non-Slack usage.

For Slack-originated files, download them using a Slack bot token that is configured outside this skill package (for example in `TOOLS.md` or another workspace secret store). Never store the actual token in this skill, this folder, or the repo.

Read the message metadata (via the `message` tool `read` action) to get `files[0].url_private_download`, `files[0].name`, and `files[0].size`.

Then download:

```bash
# Resolve your own Slack bot token from TOOLS.md or workspace secrets.
SLACK_BOT_TOKEN="<your Slack bot token>"

curl -s -L -o /tmp/<filename> \
  "<url_private_download>" \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}"

# Verify it's a real file, not an HTML redirect
file /tmp/<filename>   # should say "PDF document" not "HTML document"
ls -la /tmp/<filename> # size should match files[0].size
```

If the download returns HTML or the size is wrong, the token may be missing, expired, or lack permission to access the file. Tell the user and ask them to refresh the Slack token or provide a local file path instead.

Set `file_path` to `/tmp/<filename>` and proceed.

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

Extract `.result.accessToken` and `.result.instanceUrl`.
If this fails, tell the user to authenticate first:
```
sf org login web --instance-url <instance_url> --set-default --alias <alias>
```

### 2. Create the Library

Derive `developerName` from `library_name` by replacing spaces with `_`.

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

Extract `libraryId`. If error, show it and stop.

### 3. Poll Upload Readiness

Poll until ready (max 24 attempts, 5 seconds apart):

```bash
curl -s "<instanceUrl>/services/data/v66.0/einstein/data-libraries/<libraryId>/upload-readiness" \
  -H "Authorization: Bearer <accessToken>"
```

Check `.ready == true`. If it times out after 2 minutes, report and stop.

### 4. Get Presigned Upload URL

```bash
curl -s -X POST "<instanceUrl>/services/data/v66.0/einstein/data-libraries/<libraryId>/file-upload-urls" \
  -H "Authorization: Bearer <accessToken>" \
  -H "Content-Type: application/json" \
  -d '{
    "files": [
      { "fileName": "<basename>" }
    ]
  }'
```

Extract `.uploadUrls[0].uploadUrl`, `.uploadUrls[0].filePath`, and `.uploadUrls[0].headers`.

### 5. Upload File to S3

Build curl headers from the `.headers` object.

```bash
curl -s -X PUT "<uploadUrl>" \
  -H "<key>: <value>" \
  --data-binary @"<file_path>" \
  -w "\nHTTP_STATUS:%{http_code}"
```

Verify HTTP 200. If not, show error and stop.

### 6. Trigger Indexing

Get file size with `stat -f%z <file_path>` (macOS) or `stat -c%s <file_path>` (Linux).

```bash
curl -s -X POST "<instanceUrl>/services/data/v66.0/einstein/data-libraries/<libraryId>/indexing" \
  -H "Authorization: Bearer <accessToken>" \
  -H "Content-Type: application/json" \
  -d '{
    "uploadedFiles": [
      {
        "filePath": "<s3FilePath>",
        "fileSize": "<fileSize>"
      }
    ]
  }'
```

### 7. Poll Indexing Completion

Poll the search index endpoint until `runtimeStatus` is `READY` (max 60 attempts, 10 seconds apart = 10 minutes):

The index name follows the pattern `ADL_<developerName>` (the library's `developerName` prefixed with `ADL_`).

```bash
curl -s "<instanceUrl>/services/data/v66.0/ssot/search-index/ADL_<developerName>" \
  -H "Authorization: Bearer <accessToken>"
```

Check `.runtimeStatus`. Possible values:
- `READY` — indexing is complete, the library is ready to use.
- Other values (e.g., not yet available, or status is missing) — indexing is still in progress.

If it times out after 10 minutes, report the last known status and suggest the user check manually.

When `runtimeStatus` is `READY`, extract and report:
- `runtimeStatus`
- `label` (the index label)
- `searchType`
- `processingType`

### 8. Report Results

Do NOT dump raw JSON or API responses. Instead, present a clear, human-friendly summary.

Report:
- Library ID, Name, and Developer Name
- File name, size, and S3 path
- Indexing status (from Step 7: runtimeStatus, searchType, processingType)
- The org alias used

**Formatting rules:**
- Use **bold** for key values (library name, status, file name).
- Use **emoji indicators** for status: ✅ success/ready, ⏳ in progress, ❌ failed.
- Provide a **step-by-step progress summary** as each step completes (not just a final dump).
- If any step fails, clearly state what failed and suggest a fix.

**Platform-aware formatting:**
- **Slack / Discord / WhatsApp:** No markdown tables or `###` headers. Use **bold text** for section titles, bullet lists for structured data, and line breaks for readability.
- **Web chat / Markdown-supported surfaces:** Tables and headers are fine.
- When in doubt, default to the **Slack-friendly format** (bold + bullets) — it works everywhere.

**Example formatted output (Slack-friendly):**

```
✅ *Agentforce Data Library — Created & Indexed*

*Library:* MIMIT_AgentforceDataLibrary_Demo_Package
*Library ID:* 1JDSG000008F4Zl4AK
*Developer Name:* MIMIT_AgentforceDataLibrary_Demo_Package

*File:* MIMIT_AgentforceDataLibrary_Demo_Package.pdf
*File Size:* 73,786 bytes (~74 KB)

*Indexing Status:* ✅ READY
*Search Type:* HYBRID
*Processing Type:* NEAR_REALTIME

*Org:* adlorg
```

**Example formatted output (Markdown/web):**

```
### ✅ Agentforce Data Library — Created & Indexed

| Detail | Value |
|--------|-------|
| **Library Name** | MIMIT_AgentforceDataLibrary_Demo_Package |
| **Library ID** | 1JDSG000008F4Zl4AK |
| **File** | MIMIT_AgentforceDataLibrary_Demo_Package.pdf (74 KB) |
| **Indexing Status** | ✅ READY |
| **Search Type** | HYBRID |
| **Processing** | NEAR_REALTIME |
| **Org** | adlorg |
```

## Example Prompts

**"Ground my agent on data"** (with a file provided):
```
/adl-create-and-upload MIMIT_AgentforceDataLibrary_Demo_Package /Users/username/Downloads/MIMIT_AgentforceDataLibrary_Demo_Package.pdf --org adlorg
```

This will:
1. Get the access token and instance URL from the target org
2. Create a new Agentforce Data Library named `MIMIT_AgentforceDataLibrary_Demo_Package`
3. Poll until the library is ready for uploads
4. Get a presigned S3 upload URL
5. Upload the PDF file to S3
6. Trigger indexing
7. Poll until indexing is complete (`runtimeStatus: READY`)
8. Report the final status (library ID, file details, indexing status, org alias)
