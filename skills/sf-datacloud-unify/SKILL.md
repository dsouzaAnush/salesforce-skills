---
name: sf-datacloud-unify
description: Plan and execute Salesforce Data Cloud customer-data unification work. Use when Codex needs to connect Marketing Cloud, Salesforce CRM, Snowflake, Amazon S3, or custom application data into Data Cloud, build unified customer profiles, define mappings and identity resolution, create audience segments, or activate unified data downstream. Trigger for customer 360, profile unification, segmentation, and Data Cloud onboarding requests that assume a Data Cloud-enabled Salesforce org with admin access.
---

# sf-datacloud-unify

## Overview

Use this skill when the user is trying to turn disconnected customer data into a usable Data Cloud pipeline that ends in unified profiles and segments.

## Prerequisites

Confirm these before doing mutation-heavy work:
- Salesforce org with Data Cloud enabled
- admin access
- target org alias or login context
- source systems in scope: Marketing Cloud, CRM, Snowflake, S3, or custom apps
- desired business outcome: unified profiles, segments, activations, or all three

If Data Cloud is not enabled or admin access is missing, stop early and report the blocker instead of guessing around it.

## What Success Looks Like

Aim to produce:
- connected data sources
- unified customer profiles
- actionable segments

If the user also wants downstream execution, include the activation target and verify the audience can be pushed or exposed where needed.

## Workflow

### 1. Confirm the unification scope

Gather:
- which source systems are authoritative for profile, engagement, and transaction data
- which identifiers can be used for matching: email, CRM ID, loyalty ID, phone, device ID, or external IDs
- whether the user wants a new implementation, an inspection of existing Data Cloud setup, or a fix for a broken pipeline

### 2. Break the request into Data Cloud phases

Route the work using the existing sf-skills family:
- connection setup and source discovery: [sf-datacloud-connect](../sf-datacloud-connect/SKILL.md)
- ingestion, data streams, and landing objects: [sf-datacloud-prepare](../sf-datacloud-prepare/SKILL.md)
- mappings, DMOs, and identity resolution: [sf-datacloud-harmonize](../sf-datacloud-harmonize/SKILL.md)
- segment definition and calculated insights: [sf-datacloud-segment](../sf-datacloud-segment/SKILL.md)
- activation targets and downstream actions: [sf-datacloud-act](../sf-datacloud-act/SKILL.md)
- cross-phase orchestration or unclear ownership: [sf-datacloud](../sf-datacloud/SKILL.md)

Use this skill as the customer-360 orchestrator. Delegate execution details to the phase-specific skill as soon as the work becomes localized.

### 3. Build the customer unification plan

Structure the plan in this order:
1. sources to connect
2. ingestion objects or streams to create
3. canonical profile entities to unify
4. identity resolution rules
5. segments to publish
6. activation destinations

Prefer a simple source-to-profile mapping first. Do not over-design identity resolution before confirming what keys actually exist in the source data.

### 4. Verify each outcome before moving on

Check:
- the source connection exists and authenticates
- data lands in the expected stream or object
- mappings and unified profiles resolve as expected
- segment counts are believable
- activation targets are ready if activation is in scope

Do not claim success after connector setup alone. The user asked for customer unification, so verify progress all the way through profiles and segments.

## Common Request Patterns

Use this skill when the user says things like:
- "Connect Marketing Cloud and CRM data in Data Cloud."
- "Unify customer records from Snowflake and Salesforce."
- "Build unified profiles and create activation-ready segments."
- "Set up a customer 360 flow from S3 into Salesforce Data Cloud."

## Output Format

Respond in this order:
1. prerequisites status
2. sources in scope
3. Data Cloud phases involved
4. current state or gaps
5. plan of action
6. verification status
7. next recommended step

Suggested shape:

```text
Prerequisites: <ready / blocked>
Sources: <CRM, Marketing Cloud, Snowflake, S3, custom app>
Phases: <connect, prepare, harmonize, segment, act>
Current state: <new implementation / partial setup / troubleshooting>
Plan: <ordered actions>
Verification: <what is confirmed so far>
Next step: <highest-value next action>
```
