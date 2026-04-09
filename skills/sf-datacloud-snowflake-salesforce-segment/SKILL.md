---
name: sf-datacloud-snowflake-salesforce-segment
description: Create Salesforce Data Cloud segments and calculated insights that combine Snowflake data and Salesforce-synced objects. Use when Codex needs to build or troubleshoot a segment or calculated insight that joins Snowflake customer or order data with Salesforce CRM data already synced into Data Cloud, validate object names and join keys, write SQL, and verify counts or publish status. Trigger for cross-source segmentation, Snowflake-plus-Salesforce audience creation, aggregate audience logic, and Data Cloud segment requests that assume data is already landed in Data Cloud.
---

# sf-datacloud-snowflake-salesforce-segment

## Overview

Use this skill when the user wants one audience built from data that already exists in Data Cloud across both Snowflake and Salesforce sources, with or without a calculated insight layer first.

## Prerequisites

Confirm these before doing mutation-heavy work:
- Salesforce org with Data Cloud enabled
- target org alias or login context
- Snowflake data already landed in Data Cloud
- Salesforce objects already synced into Data Cloud
- known or discoverable join path between the Snowflake objects and the Salesforce or unified profile objects

If the Snowflake objects are not visible in Data Cloud, stop and report that blocker instead of inventing table names.

## What Success Looks Like

Aim to produce:
- confirmed Data Cloud object names for Snowflake and Salesforce data
- a valid join path across those objects
- a reusable calculated insight when aggregated logic is needed
- a reusable segment definition
- verified segment count or publish status

## Workflow

### 1. Confirm the segment goal

Gather or infer:
- the business rule for the audience
- which Snowflake objects are in scope, usually customer and order
- which Salesforce-synced objects matter, such as Account, Contact, or unified profile objects
- whether the user wants create, inspect, publish, or troubleshoot
- whether the audience depends on aggregated measures like total spend, order count, average order value, or recency

### 2. Discover the actual Data Cloud objects first

Use the existing sf-skills family:
- object discovery and SQL inspection: [sf-datacloud-retrieve](../sf-datacloud-retrieve/SKILL.md)
- mappings and identity-resolution checks: [sf-datacloud-harmonize](../sf-datacloud-harmonize/SKILL.md)
- segment asset creation and publish flow: [sf-datacloud-segment](../sf-datacloud-segment/SKILL.md)

Before writing segment SQL:
- list or describe the relevant DLOs and DMOs
- verify the Snowflake objects are actually present
- verify the Salesforce objects or unified profile objects are actually present
- identify the field that ties them together: email, customer ID, account ID, CRM ID, or Data Cloud individual ID

Do not assume object API names from business labels alone.

### 3. Choose the correct segment base

Prefer this order:
1. unified profile entity, if identity resolution is complete
2. a segmentable canonical DMO
3. a source-backed DMO only if no better unified object exists

The selected SQL should return the identifier for the segment base entity, not a transaction or order row.

### 4. Build the cross-source SQL

Decide whether the logic should be:
1. direct segment SQL, for row-level filters and straightforward joins
2. calculated insight first, then segment, for aggregated logic like counts, sums, averages, rankings, or rolling windows

Prefer a calculated insight first when the user asks for things like:
- customers with at least `N` orders
- customers with spend above a threshold
- customers whose most recent order falls inside a time window
- customers ranked by value, frequency, or recency

Use direct segment SQL when the rule is mostly attribute filtering and simple existence logic.

Structure the SQL in this order:
1. base person or account entity
2. join to Snowflake customer object
3. join to Snowflake order object
4. optionally join Salesforce Account or Contact data
5. filter on the business rule
6. group at the base entity level if transactions are involved

Typical pattern:

```sql
SELECT base.<segment_id>
FROM "<base_entity>" base
JOIN "<snowflake_customer>" c
  ON c.<customer_join_key> = base.<base_join_key>
JOIN "<snowflake_order>" o
  ON o.<order_customer_key> = c.<customer_key>
LEFT JOIN "<salesforce_entity>" s
  ON s.<salesforce_join_key> = base.<base_salesforce_key>
WHERE <business_filters>
GROUP BY base.<segment_id>
```

Typical calculated insight pattern:

```sql
SELECT c.<customer_key> AS customer_id,
       COUNT(o.<order_id>) AS order_count,
       SUM(o.<order_amount>) AS total_spend
FROM "<snowflake_customer>" c
JOIN "<snowflake_order>" o
  ON o.<order_customer_key> = c.<customer_key>
GROUP BY c.<customer_key>
```

Then build the segment from the calculated insight plus the selected profile base.

### 5. Create and verify the asset

Use a reusable JSON definition when creating the calculated insight or segment.

If a calculated insight is used:
- create it first
- run it
- verify the aggregates look believable
- then create the segment that filters on the calculated insight output

Verify:
- the SQL compiles
- the calculated insight runs if used
- the member count is believable
- publish succeeds if the user asked for publishing

If the count is zero or unexpectedly high, inspect the joins before changing business filters.

## High-Signal Gotchas

- Data Cloud SQL is not SOQL.
- Snowflake business labels like `Order` and `customer` often do not match the Data Cloud API names.
- Calculated insights are optional, but they are usually the cleaner path for aggregate order logic.
- Segment creation is less reliable when the join path depends on incomplete identity resolution.
- If the Snowflake objects are only raw DLOs and not mapped into usable DMOs, segmentation may need harmonization work first.
- A segment should return one row per intended audience member, not one row per order.

## Common Request Patterns

Use this skill when the user says things like:
- "Create a segment from Snowflake orders and Salesforce contacts."
- "Build a Data Cloud audience using Snowflake customer data plus synced CRM data."
- "Segment customers with recent orders and Salesforce account context."
- "Create a calculated insight for total spend, then segment high-value customers."
- "Troubleshoot why my Snowflake plus Salesforce Data Cloud segment returns zero members."

## Output Format

Respond in this order:
1. prerequisites status
2. objects in scope
3. join path
4. asset type
5. current state or blockers
6. plan or SQL shape
7. verification status
8. next recommended step

Suggested shape:

```text
Prerequisites: <ready / blocked>
Objects: <Snowflake customer, Snowflake order, Salesforce objects, unified objects>
Join path: <keys and entities>
Asset type: <segment / calculated insight + segment>
Current state: <create / inspect / troubleshoot>
Plan: <ordered actions or SQL shape>
Verification: <object checks, insight run status, counts, publish status>
Next step: <highest-value next action>
```
