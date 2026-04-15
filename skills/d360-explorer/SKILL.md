---
name: CDP Explorer
description: Explore and discover Data Cloud org configuration - list all entities, understand the data model, check ingestion status, and get a full picture of the CDP setup. Use when the user wants to understand what's in their Data Cloud org, audit configuration, or get an overview. Requires the cdp MCP server.
---

# CDP Explorer Skill

Comprehensive discovery and exploration of a Data Cloud / CDP org.

## Quick Org Overview

Run these tools in sequence (or parallel where possible) to get a full picture:

### Step 1: Discover the data model
```
Tool: d360_metadata
Args: {}
```
This returns ALL entities - DMOs, DLOs, calculated insights, segments, etc.

### Step 2: List operational components
Run in parallel:
- `d360_dmo_list` - All Data Model Objects
- `d360_datastream_list` - All data streams
- `d360_connector_list` - Discover valid connector types first
- `d360_connection_list { connectorType: "<from connector_list>" }` - Connections (connectorType REQUIRED)
- `d360_segment_list` - All segments
- `d360_ci_list` - All calculated insights
- `d360_ir_list` - All identity resolution configs
- `d360_activation_list` - All activations
- `d360_dataspace_list` - All data spaces
- `d360_transform_list` - All data transforms

### Step 3: Deep dive into specific entities
```
Tool: d360_dmo_get
Args: { dmoName: "Individual__dlm" }
```

### Step 4: Sample data
```
Tool: d360_query_sql
Args: { sql: "SELECT * FROM Individual__dlm LIMIT 5" }
```

## Discovery Queries

### List all available tables/DMOs
```sql
SELECT EntityName, EntityCategory, EntityType FROM metadata_entity__md ORDER BY EntityCategory
```

### Get row counts for key entities
```sql
SELECT COUNT(*) as cnt FROM Individual__dlm
```

### Explore relationships
```sql
SELECT
  r.ParentEntityName, r.ChildEntityName, r.RelationshipType
FROM metadata_relationship__md r
```

### Check data freshness
```sql
SELECT MAX(DataSourceLastModifiedDate__c) as last_updated FROM Individual__dlm
```

## Typical Exploration Flow

1. **"What's in my org?"** → `d360_metadata` then summarize entities by category
2. **"Show me the schema for X"** → `d360_dmo_get { dmoName: "X__dlm" }` or `d360_profile_metadata { dataModelName: "X__dlm" }`
3. **"How much data do I have?"** → SQL COUNT queries per entity
4. **"What connections are set up?"** → First `d360_connector_list` to get valid types, then `d360_connection_list { connectorType: "..." }` — connectorType is REQUIRED
5. **"Is identity resolution configured?"** → `d360_ir_list` then `d360_ir_get`
6. **"What segments exist?"** → `d360_segment_list`
7. **"What's being activated?"** → `d360_activation_list` and `d360_activation_target_list`

## Data Cloud Entity Naming Conventions
- `__dlm` - Data Lake Model (DMO - unified model)
- `__dll` - Data Lake Lineage (DLO - source data)
- `__md` - Metadata tables (system catalog)
- Common DMOs: `Individual__dlm`, `ContactPointEmail__dlm`, `ContactPointPhone__dlm`, `ContactPointAddress__dlm`, `Account__dlm`

## Complete Tool Inventory (108+ tools across 14 families)

| Family | Prefix | Tool Count | Key Operations |
|--------|--------|------------|----------------|
| Query & Metadata | `d360_query_*`, `d360_metadata*`, `d360_profile_*`, `d360_insights_*`, `d360_datagraph_*` | 15 | SQL, profiles, insights, data graphs |
| DMO & Mappings | `d360_dmo_*`, `d360_dmo_mapping_*` | 10 | CRUD data model objects & mappings |
| Data Streams | `d360_datastream_*` | 6 | CRUD & run ingestion streams |
| Connections | `d360_connection_*`, `d360_connector_*` | 8 | Manage external connections (**connectorType required**) |
| Smart Tools | `d360_smart_*`, `d360_preview_*`, `d360_analyze_*` | 4 | Field matching, event date selection |
| Segments | `d360_segment_*` | 7 | CRUD, publish, wait-ready |
| Calculated Insights | `d360_ci_*` | 10 | CRUD, enable/disable, run, validate, wait-ready |
| Identity Resolution | `d360_ir_*` | 8 | CRUD, publish, run, full-update, delete |
| Activations | `d360_activation_*` | 10 | Manage activations & targets (incl. target update) |
| Data Spaces | `d360_dataspace_*` | 8 | Manage spaces & members |
| Data Transforms | `d360_transform_*` | 9 | CRUD, run, validate, schedule |
| SDM (Semantic) | `d360_sdm_*` | 25+ | Models, data objects, dims, measures, metrics, relationships, query |
| Data Kits | `d360_datakit_*` | 8 | Deploy/undeploy packages |
| Eventing | `d360_event_*` | 2 | Stream events (single & batch) |
| GDPR | `d360_gdpr_*` | 3 | Data subject rights |
| Data Actions | `d360_dataaction_*` | 8 | Actions & action targets |
| Orchestration | `d360_plan_execution` | 1 | Topological dependency ordering |

## Data Cloud Entity Categories
- **Profile**: Individual, Account - core customer entities
- **Engagement**: Events, interactions, touchpoints
- **Other**: Custom objects, reference data, enrichment
- **System**: Internal catalog, metadata tables

## Data Stream Types (23 connector types)
S3, Marketing Cloud, SFDC (CRM), SFDC_BUNDLE, FILEUPLOAD, EVENTS, INGESTAPI, COMMERCE, GOOGLE_CLOUD_STORAGE, SFTP, AZURE_BLOB, CONNECTORSFRAMEWORK, ACCOUNT_ENGAGEMENT, and more.

## Smart Tools (Intelligent Helpers)

### Auto-Map Fields
```
Tool: d360_smart_mapping
Args: { sourceDloName: "Account_00D...__dll", targetDmoName: "ssot__Account__dlm" }
```
Returns field matches with confidence scores plus a ready-to-use `mappingPayload` for `d360_dmo_mapping_create`.

### Analyze Event Date Candidates
```
Tool: d360_analyze_event_date
Args: { dataStreamName: "Task_00D..." }
```
Ranks date fields by suitability for event date column (immutable > mutable).

## Important: Connection Tools Require connectorType

The CDP `/ssot/connections` API requires `connectorType` as a URL parameter. Always:
1. Call `d360_connector_list` first to discover valid connector types
2. Pass the appropriate `connectorType` to `d360_connection_list`, `d360_connection_get`, etc.

## Tips
- Start broad (`d360_metadata`) then narrow down
- Use SQL queries for data exploration, REST tools for config exploration
- Data spaces partition data - query within a space using the `dataspace` parameter
- Run discovery tools in parallel for faster results
- Use `d360_datakit_list` to see what packages are deployed
- Use `d360_event_publish` for real-time streaming ingestion
- Use `d360_smart_mapping` instead of manually constructing field mappings
- Use `d360_plan_execution` before creating multi-component workflows to get dependency-ordered phases
- DMO field types: Text, Number, Date, DateTime, Boolean, LargeText
