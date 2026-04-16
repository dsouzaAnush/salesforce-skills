---
name: CDP Data Operations
description: Manage Data Cloud operational workflows - segments, calculated insights, identity resolution, activations, data transforms, and data spaces. Use when the user wants to create segments, run identity resolution, set up activations, manage computed metrics, or configure data spaces. Requires the cdp MCP server.
---

# CDP Data Operations Skill

Manage Data Cloud operational entities using the CDP MCP server.

## Capability Matrix

| Domain | List | Get | Create | Update | Delete | Actions |
|--------|------|-----|--------|--------|--------|---------|
| **Segments** | `d360_segment_list` | `d360_segment_get` | `d360_segment_create` | `d360_segment_update` | `d360_segment_delete` | `d360_segment_publish` |
| **Calculated Insights** | `d360_ci_list` | `d360_ci_get` | `d360_ci_create` | `d360_ci_update` | `d360_ci_delete` | `d360_ci_enable`, `d360_ci_disable`, `d360_ci_run`, `d360_ci_validate` |
| **Identity Resolution** | `d360_ir_list` | `d360_ir_get` | `d360_ir_create` | `d360_ir_update` | `d360_ir_delete` | `d360_ir_publish`, `d360_ir_run`, `d360_ir_full_update` |
| **Activations** | `d360_activation_list` | `d360_activation_get` | `d360_activation_create` | `d360_activation_update` | `d360_activation_delete` | — |
| **Activation Targets** | `d360_activation_target_list` | `d360_activation_target_get` | `d360_activation_target_create` | `d360_activation_target_update` | `d360_activation_target_delete` | — |
| **Data Transforms** | `d360_transform_list` | `d360_transform_get` | `d360_transform_create` | `d360_transform_update` | `d360_transform_delete` | `d360_transform_run`, `d360_transform_validate` |
| **Transform Schedules** | `d360_transform_schedule_get` | — | `d360_transform_schedule_set` | — | — | — |
| **Data Spaces** | `d360_dataspace_list` | `d360_dataspace_get` | `d360_dataspace_create` | `d360_dataspace_update` | `d360_dataspace_delete` | — |
| **Data Space Members** | `d360_dataspace_member_list` | — | `d360_dataspace_member_add` | — | `d360_dataspace_member_remove` | — |

## Common Workflows

### Create and publish a segment
1. `d360_segment_create { body: { name: "High Value Customers", segmentDefinition: "..." } }`
2. `d360_segment_publish { segmentId: "..." }`

### Set up activation pipeline
1. **Create target**: `d360_activation_target_create { body: { ... } }`
2. **Create activation**: `d360_activation_create { body: { activationTargetId: "...", segmentId: "..." } }`

### Configure identity resolution
1. `d360_ir_list` - See existing rulesets
2. `d360_ir_create { body: { label: "...", matchRules: {...}, reconciliationRules: {...} } }`
3. `d360_ir_publish { identityResolutionId: "..." }`
4. `d360_ir_run { identityResolutionId: "..." }`

### Create and schedule a data transform
1. `d360_transform_create { body: { name: "...", expression: "...", sourceObjectName: "..." } }`
2. `d360_transform_validate { transformId: "..." }`
3. `d360_transform_schedule_set { transformId: "...", body: { frequency: "Daily", cronExpression: "0 0 2 * * ?" } }`

### Manage data spaces
1. `d360_dataspace_list` - See all data spaces
2. `d360_dataspace_create { body: { name: "regional_space", displayName: "Regional Data" } }`
3. `d360_dataspace_member_add { dataSpaceName: "regional_space", body: { ... } }`

## Calculated Insight Lifecycle
1. **Create**: `d360_ci_create` - Define the CI with DCSQL expression
2. **Validate**: `d360_ci_validate` - Check for errors before enabling
3. **Enable**: `d360_ci_enable` - Make it active
4. **Run**: `d360_ci_run` - Trigger computation
5. **Query**: Use `d360_insights_query` (from Query skill) to see results

## Data Kit Operations (Package Management)
1. `d360_datakit_list` - See deployed packages
2. `d360_datakit_get` / `d360_datakit_manifest` - Inspect package contents
3. `d360_datakit_deploy` - Deploy a package
4. `d360_datakit_deploy_status` - Track deployment progress
5. `d360_datakit_undeploy` - Remove a package

## Event Streaming (Real-time Ingestion)
Single event:
```
d360_event_publish { schema: "MyEventSchema", payload: { field1: "value1" } }
```

Batch events:
```
d360_event_publish_batch { events: [...], schemas: [...] }
```

## GDPR / Data Subject Rights
- `d360_gdpr_read` - Read data for an individual
- `d360_gdpr_bulk_read` - Bulk read for multiple individuals
- `d360_gdpr_request` - Submit delete/portability request

## Data Actions
- `d360_dataaction_list` / `d360_dataaction_create` / `d360_dataaction_get` - Manage triggered actions
- `d360_dataaction_target_*` - Configure action destinations (webhooks, flows, etc.)

## Orchestration: Multi-Component Workflows

Use `d360_plan_execution` BEFORE creating multi-component workflows. Pass components with dependencies and get back a topologically-sorted execution plan with parallel phases:

```
Tool: d360_plan_execution
Args: {
  components: [
    { name: "Revenue_CI__cio", type: "CI", dependsOn: [] },
    { name: "HighValue_Segment", type: "Segment", dependsOn: ["Revenue_CI__cio"] },
    { name: "AccountModel", type: "SDM", dependsOn: [] }
  ]
}
```

Wait-ready helpers:
- `d360_ci_wait_ready { ciName: "..." }` — polls until CI is ACTIVE
- `d360_segment_wait_ready { segmentId: "..." }` — polls until segment is ACTIVE

## Tips
- Always validate before enabling (CIs) or publishing (segments, IR)
- Segments need to be published before they can be used in activations
- Identity resolution affects all downstream profile data — `d360_ir_delete` and `d360_ir_full_update` now available
- Activation targets can be updated with `d360_activation_target_update`
- Use `d360_ci_run_status` to check the outcome of a CI run
- Data transforms support DC SQL expressions for complex computations
- Data spaces provide multi-tenant data isolation within an org
- Use data kits for packaging and deploying bundles of DC components
- Event streaming requires a pre-registered schema in Data Cloud
- GDPR requests are async - check status after submission
- Use `d360_plan_execution` for complex multi-component creation with dependency ordering
