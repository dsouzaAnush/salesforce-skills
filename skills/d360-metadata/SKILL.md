---
name: CDP Metadata Manager
description: Manage Data Cloud metadata - create, read, update, delete DMOs, DMO mappings, data streams, and connections. Use when the user wants to create or modify data model objects, set up data ingestion, or manage connections. Requires the cdp MCP server.
---

# CDP Metadata Manager Skill

Manage Data Cloud metadata entities using the CDP MCP server.

## Capabilities

| Operation | Tools |
|-----------|-------|
| **Data Model Objects** | `d360_dmo_list`, `d360_dmo_get`, `d360_dmo_create`, `d360_dmo_update`, `d360_dmo_delete` |
| **DMO Mappings** | `d360_dmo_mapping_list`, `d360_dmo_mapping_get`, `d360_dmo_mapping_create`, `d360_dmo_mapping_update`, `d360_dmo_mapping_delete`, `d360_dmo_field_mapping_add`, `d360_dmo_field_mapping_delete` |
| **Data Streams** | `d360_datastream_list`, `d360_datastream_get`, `d360_datastream_create`, `d360_datastream_update`, `d360_datastream_delete`, `d360_datastream_run` |
| **Connections** | `d360_connection_list`, `d360_connection_get`, `d360_connection_create`, `d360_connection_update`, `d360_connection_delete`, `d360_connection_test` (**all require `connectorType`**) |
| **Connectors** | `d360_connector_list`, `d360_connector_metadata` |
| **Connection Endpoints** | `d360_connection_endpoints` |
| **Smart Tools** | `d360_smart_mapping`, `d360_preview_field_matches`, `d360_smart_datastream`, `d360_analyze_event_date` |

## Workflows

### Discover what exists
1. `d360_dmo_list` - See all Data Model Objects
2. `d360_dmo_get { dmoName: "Individual__dlm" }` - Get field details
3. `d360_dmo_mapping_list { dmoDeveloperName: "ssot__Individual__dlm" }` - See all mappings for a DMO
4. `d360_datastream_list` - See all ingestion streams
5. `d360_connector_list` - **Always call first** to get valid connectorType values
6. `d360_connection_list { connectorType: "SalesforceCRM" }` - See connections (**connectorType required**)

### Set up data ingestion (end-to-end)
1. **Check available connectors**: `d360_connector_list`
2. **Get connector metadata**: `d360_connector_metadata { connectorType: "SalesforceCRM" }`
3. **Create connection**: `d360_connection_create { connectorType: "SalesforceCRM", body: { ... } }`
4. **Test connection**: `d360_connection_test { connectorType: "SalesforceCRM", body: { ... } }`
5. **Create data stream**: `d360_datastream_create { body: { connectionId: "...", sourceObjectName: "Contact", ... } }`
6. **Auto-map fields**: `d360_smart_mapping { sourceDloName: "Contact_00D...", targetDmoName: "ssot__Individual__dlm" }` — returns ready-to-use payload
7. **Create DMO mapping**: `d360_dmo_mapping_create` with the `mappingPayload` from step 6
8. **Run ingestion**: `d360_datastream_run { dataStreamId: "..." }`

### Auto-map DLO to DMO fields (smart mapping)
1. **Preview matches**: `d360_preview_field_matches { sourceDloName: "...", targetDmoName: "..." }` — dry run
2. **Generate mapping**: `d360_smart_mapping { sourceDloName: "...", targetDmoName: "..." }` — returns `mappingPayload`
3. **Apply**: `d360_dmo_mapping_create { body: <mappingPayload> }`

### Set up Engagement data stream (with event date)
1. **Prepare body**: Include field definitions in `dataLakeObjectInfo.dataLakeFieldInfoRepresentation`
2. **Auto-select event date**: `d360_smart_datastream { body: <stream_body> }` — auto-injects `eventDateColumn`
3. **Create stream**: `d360_datastream_create` with the `enhancedBody` from step 2

### Modify a DMO
1. **Get current state**: `d360_dmo_get { dmoName: "MyCustomObject__dlm" }`
2. **Update**: `d360_dmo_update { dmoName: "MyCustomObject__dlm", fields: [...] }`

## DMO Categories
- **Profile**: Individual, Account, etc.
- **Engagement**: Events, interactions
- **Other**: Custom objects, reference data

## Field Types
Common Data Cloud field types: `Text`, `Number`, `Date`, `DateTime`, `Boolean`, `LargeText`

## Important: connectorType is REQUIRED for Connections

All connection tools (`d360_connection_list`, `d360_connection_get`, `d360_connection_create`, `d360_connection_update`, `d360_connection_delete`, `d360_connection_test`) require a `connectorType` parameter. Valid values come from `d360_connector_list`. Common types: `SalesforceCRM`, `TenantBillingUsageConnector`, `S3`, `MarketingCloud`, etc.

## Tips
- Always `d360_dmo_get` before updating to understand the current structure
- Connection IDs are needed to create data streams
- DMO names follow the pattern `ObjectName__dlm`
- Mappings link source DLO fields to target DMO fields
- Use `d360_smart_mapping` instead of manually constructing field mappings — it matches by name/label similarity
- For Engagement streams, always use `d360_smart_datastream` to auto-select the event date column
- Never use `LastModifiedDate` as event date — it's mutable and breaks time-series partitioning
