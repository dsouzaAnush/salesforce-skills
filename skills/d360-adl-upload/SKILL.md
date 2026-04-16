---
name: adl-upload
description: Upload files to an existing Agentforce Data Library and trigger indexing. Use when the user wants to upload files to an ADL or data library.
user-invocable: true
allowed-tools: Bash(sf *) Bash(curl *) Bash(jq *) Bash(stat *) Read
argument-hint: "<library_developer_name> <file_path> [--org <alias>]"
---

# Upload Files to Agentforce Data Library

Upload a file to an existing SFDRIVE-type Agentforce Data Library and trigger indexing.

## Arguments

Parse the arguments from: $ARGUMENTS

- `library_developer_name` (required) — the developerName of the existing library.
- `file_path` (required) — absolute path to the file to upload.
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

Extract `.result.accessToken` and `.result.instanceUrl`.

### 2. Find the Library ID

List all libraries and find the one matching the developer name:

```bash
curl -s "<instanceUrl>/services/data/v66.0/einstein/data-libraries" \
  -H "Authorization: Bearer <accessToken>"
```

Find the library where `.libraries[].developerName` matches the given name. Extract its `libraryId`.
If not found, list available libraries and stop.

### 3. Get Presigned Upload URL

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

### 4. Upload File to S3

Build curl headers from the `.headers` object (e.g. `Content-Type: application/pdf`).

```bash
curl -s -X PUT "<uploadUrl>" \
  -H "<key>: <value>" \
  --data-binary @"<file_path>" \
  -w "\nHTTP_STATUS:%{http_code}"
```

Verify HTTP status is 200. If not, show the error and stop.

### 5. Trigger Indexing

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

### 6. Report Results

When done, report:
- Library ID and Developer Name
- File name, size, and S3 path
- Indexing status from the response
- The org alias used
