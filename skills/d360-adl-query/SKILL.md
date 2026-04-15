---
name: adl-query
description: Query an Agentforce Data Library using hybrid search via the Data Cloud SQL API (d360_query_sql). Use when the user wants to search or query an ADL, data library, or retrieve chunks from an ADL.
user-invocable: true
argument-hint: "<library_developer_name> <search_query> [--top_k <number>] [--org <alias>]"
---

# Query Agentforce Data Library

Run a hybrid search against an Agentforce Data Library (ADL) using the Data Cloud SQL API (`d360_query_sql` tool).

## Arguments

Parse the arguments from: $ARGUMENTS

- `library_developer_name` (required) — the developerName of the ADL library (e.g., `My_Library`).
- `search_query` (required) — the natural-language search query to run against the library.
- `--top_k <number>` (optional, default: `5`) — the number of results to return from the hybrid search.
- `--org <alias>` (optional) — the sf CLI org alias to use (only needed if not using the cdp MCP server). Overrides both `~/.claude/d360_org` and the sf CLI default.

## Table Name Convention

ADL index and chunk table names are derived from the library's developer name:

- **Index table**: `ADL_<developerName>_index__dlm`
- **Chunk table**: `ADL_<developerName>_chunk__dlm`

For example, if the library developer name is `My_Library`:
- Index table: `ADL_My_Library_index__dlm`
- Chunk table: `ADL_My_Library_chunk__dlm`

## Query Template

Use the `d360_query_sql` tool with this SQL pattern:

```sql
SELECT chunk.Chunk__c
FROM hybrid_search(
  TABLE("ADL_<developerName>_index__dlm"),
  '<search_query>',
  '',
  <top_k>
) AS hs
JOIN "ADL_<developerName>_chunk__dlm" AS chunk
  ON hs.SourceRecordId__c = chunk.RecordId__c
ORDER BY hs."hybrid_score__c" DESC
```

## Steps

### 1. Build the SQL Query

Substitute the library developer name, search query, and top_k into the template above.

**Important:** Escape any single quotes in the search query by doubling them (`'` → `''`).

### 2. Execute via d360_query_sql

```
Tool: d360_query_sql
Args: {
  sql: "<constructed SQL query>"
}
```

### 3. Handle Results

- If the query succeeds, display the returned chunks to the user.
- If the query returns no results, let the user know and suggest checking:
  - The library developer name is correct
  - The library has been indexed (files uploaded and indexing triggered)
  - The search query is relevant to the uploaded content
- If the query fails with a table-not-found error, verify the library developer name and confirm the ADL exists and has been indexed.

### 4. Report Results

Do NOT dump raw chunk text. Instead, synthesize and format the results into a clear, human-friendly answer.

**Formatting rules:**
- **Analyze the chunks** and produce a well-structured answer to the user's question, not a list of raw chunks.
- Use **bold** for key values, names, and critical findings.
- Use **emoji indicators** for status/severity where appropriate (🔴 critical, 🟡 warning, ✅ normal).
- Include **clinical implications, reasoning, or context** when the data supports it — don't just list facts.
- If the query returns no useful results, say so clearly rather than showing empty or irrelevant chunks.
- **Cite the source library** at the end of the response.

**Platform-aware formatting:**
- **Slack / Discord / WhatsApp:** No markdown tables or `###` headers. Use **bold text** for section titles, bullet lists for structured data, and line breaks for readability.
- **Web chat / Markdown-supported surfaces:** Tables and headers are fine.
- When in doubt, default to the **Slack-friendly format** (bold + bullets) — it works everywhere.

**Example formatted output (Slack-friendly) for a lab values query:**

```
*Robert Caldwell — Critically Abnormal Lab Values*

🔴 *HbA1c:* 9.1% (normal: <7%) — HIGH
🔴 *Albumin:* 2.9 g/dL (normal: 3.5–5.0) — LOW
🔴 *ABI:* 0.37 (normal: >0.9) — Critical
🔴 *eGFR:* 44 mL/min (normal: 60–120) — LOW
🔴 *Fasting Glucose:* 194 mg/dL (normal: 70–100) — HIGH
🟡 *LDL:* 112 mg/dL (target: <70 for vascular) — Elevated
🟡 *WBC:* 11.4 (normal: <11.0) — Mildly elevated

*Clinical Implications*

The combination of poor perfusion (ABI 0.37), uncontrolled diabetes
(HbA1c 9.1%), and low albumin creates a hostile wound-healing
environment. Without revascularization and metabolic optimization,
estimated amputation risk is 30–40%.

_Source: MIMIT_Agentforc Data Library_
```

**Example formatted output (Markdown/web) for the same query:**

```
### Robert Caldwell — Critically Abnormal Lab Values

| Lab Value | Result | Normal Range | Status |
|-----------|--------|-------------|--------|
| **HbA1c** | 9.1% | <7% | 🔴 HIGH |
| **Albumin** | 2.9 g/dL | 3.5–5.0 | 🔴 LOW |
| **ABI** | 0.37 | >0.9 | 🔴 Critical |

### Clinical Implications

The combination of poor perfusion (ABI 0.37), uncontrolled diabetes (HbA1c 9.1%),
and low albumin creates a hostile wound-healing environment...

---
*Source: MIMIT_Agentforc Data Library*
```

## Examples

**Simple search:**
```
/adl-query My_Library "What is the return policy?"
```

Generates:
```sql
SELECT chunk.Chunk__c
FROM hybrid_search(
  TABLE("ADL_My_Library_index__dlm"),
  'What is the return policy?',
  '',
  5
) AS hs
JOIN "ADL_My_Library_chunk__dlm" AS chunk
  ON hs.SourceRecordId__c = chunk.RecordId__c
ORDER BY hs."hybrid_score__c" DESC
```

**With custom top_k:**
```
/adl-query My_Library "product specifications" --top_k 10
```

**Clinical data query (healthcare ADL):**
```
/adl-query MIMIT_Agentforc "Which of Robert Caldwell lab values are critically abnormal, and what are the clinical implications?"
```

Generates:
```sql
SELECT chunk.Chunk__c
FROM hybrid_search(
  TABLE("ADL_MIMIT_Agentforc_index__dlm"),
  'Which of Robert Caldwell lab values are critically abnormal, and what are the clinical implications?',
  '',
  5
) AS hs
JOIN "ADL_MIMIT_Agentforc_chunk__dlm" AS chunk
  ON hs.SourceRecordId__c = chunk.RecordId__c
ORDER BY hs."hybrid_score__c" DESC
```

**Note:** Salesforce may truncate long library developer names when creating search indexes. For example, `MIMIT_AgentforceDataLibrary_Demo_Package` becomes `MIMIT_Agentforc`. Use the truncated name (as shown in the search index) when querying, not the full library developer name.
