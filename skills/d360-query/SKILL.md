---
name: CDP Query
description: Query Data Cloud using SQL, profile APIs, and calculated insights. Use when the user wants to run SQL queries against Data Cloud, look up profiles, query calculated insights, or explore data graph records. Requires the cdp MCP server to be configured.
---

# CDP Query Skill

Execute queries against Salesforce Data Cloud / CDP using the CDP MCP server tools.

## Query Decision Tree

```
What does the user want to query?
│
├─► "Run a SQL query" or "query data"
│   └─► Use d360_query_sql (V3 API - preferred)
│       → For large results: check status with d360_query_sql_status, paginate with d360_query_sql_rows
│       → To cancel: d360_query_sql_cancel
│
├─► "Look up a profile" or "find individual/contact"
│   └─► Use d360_profile_query with dataModelName (e.g., Individual__dlm)
│       → Use searchKey for text search
│       → Use id for specific record
│       → Use childDataModelName to navigate relationships
│
├─► "Query calculated insights" or "get metrics/KPIs"
│   └─► Use d360_insights_query with ciName, dimensions, measures
│
├─► "Query data graph"
│   └─► Use d360_datagraph_query (by ID) or d360_datagraph_lookup (by keys)
│
├─► "What entities/objects exist?"
│   └─► Use d360_metadata (all metadata) or d360_metadata_entities (paginated)
│
└─► "What fields does X have?"
    └─► Use d360_profile_metadata or d360_metadata with entityName filter
```

## SQL Query Workflow (V3 - Recommended)

### Step 1: Submit query
```
Tool: d360_query_sql
Args: { sql: "SELECT Id__c, FirstName__c FROM Individual__dlm LIMIT 100" }
```

The response includes:
- `status.queryId` - for pagination/status checks
- `status.completionStatus` - "Success", "Running", etc.
- `data` - first chunk of results
- `metadata` - column names and types

### Step 2: If more data needed (status shows more rows than returned)
```
Tool: d360_query_sql_rows
Args: { queryId: "<queryId>", offset: 100, rowLimit: 100 }
```

### Step 3: For long-running queries
```
Tool: d360_query_sql_status
Args: { queryId: "<queryId>", waitTimeMs: 5000 }
```
Wait until `completionStatus` is "Success", then fetch rows.

## Data Space Scoping

All query tools accept an optional `dataspace` parameter. When the user mentions a specific data space, always pass it:
```
{ sql: "SELECT ...", dataspace: "my_data_space" }
```

## Common DC SQL Patterns

### List all DMOs
```sql
SELECT EntityName, EntityCategory FROM metadata_entity__md
```

### Get fields for a DMO
```sql
SELECT FieldName, DataType FROM metadata_field__md WHERE EntityName = 'Individual__dlm'
```

### Count records
```sql
SELECT COUNT(*) FROM Individual__dlm
```

### Query with filters
```sql
SELECT Id__c, FirstName__c, LastName__c
FROM Individual__dlm
WHERE LastName__c = 'Smith'
LIMIT 50
```

### Join across DMOs
```sql
SELECT i.FirstName__c, e.EmailAddress__c
FROM Individual__dlm i
JOIN ContactPointEmail__dlm e ON i.Id__c = e.PartyId__c
LIMIT 100
```

### Parameterized queries (V3)
```
Tool: d360_query_sql
Args: {
  sql: "SELECT * FROM Individual__dlm WHERE LastName__c = ?",
  sqlParameters: [{ name: "p1", type: "Varchar", value: "Smith" }]
}
```

## Semantic Queries (SDM)

For business-friendly queries against Semantic Data Models:

```
Tool: d360_sdm_query
Args: {
  body: {
    semanticModelId: "<uuid from d360_sdm_list>",
    structuredSemanticQuery: {
      fields: [
        { expression: { tableField: { name: "Region", tableName: "Account" } }, alias: "Region", rowGrouping: true },
        { expression: { tableField: { name: "Revenue", tableName: "Financials" } }, alias: "TotalRevenue", semanticAggregationMethod: "SEMANTIC_AGGREGATION_METHOD_SUM" }
      ],
      options: { limitOptions: { limit: 100 } }
    }
  }
}
```

For calculated dimensions/measurements, use `semanticField` (not `tableField`):
```json
{ "expression": { "semanticField": { "name": "Revenue_Tier" } }, "alias": "Tier", "rowGrouping": true }
```

## Tips
- Always use `d360_query_sql` (V3) for new queries - it's faster and supports pagination
- Use `d360_metadata` first if you're unsure of entity/field names
- Use `d360_discover` to find the right tool for any Data Cloud task
- DMO names end in `__dlm` (data lake model)
- DLO names end in `__dll` (data lake lineage)
- Common DMOs: `Individual__dlm`, `ContactPointEmail__dlm`, `ContactPointPhone__dlm`, `ContactPointAddress__dlm`
- For semantic queries, use `semanticModelId` (UUID), NOT the API name
