---
name: sf-datacloud-mce-unify
description: Connect Marketing Cloud Engagement to Salesforce Data Cloud and unify email engagement data with customer profiles. Use when Codex needs to bring email sends, opens, clicks, and related engagement history into Data Cloud, connect that data to existing customer identities, and support smarter segmentation and personalization. Trigger for Marketing Cloud Engagement to Data Cloud onboarding, email-engagement unification, profile enrichment, and engagement-driven audience design requests that assume a Data Cloud-enabled Salesforce org, a Marketing Cloud Engagement account, and admin access to both.
---

# sf-datacloud-mce-unify

## Overview

Use this skill when the user wants Marketing Cloud Engagement behavior to show up inside the unified customer view in Data Cloud.

## Prerequisites

Confirm these before doing mutation-heavy work:
- Salesforce org with Data Cloud enabled
- Marketing Cloud Engagement account
- admin access to both systems
- target org alias or login context
- clarity on which engagement events matter most: sends, opens, clicks, bounces, or unsubscribes

If either admin access or the MCE account is missing, stop and report the blocker early.

## What Success Looks Like

Aim to produce:
- an MCE connection in Data Cloud
- email engagement data streams
- unified profiles with engagement history

If the user also wants marketing outcomes, include the segment or activation target that will consume this engagement data.

## Workflow

### 1. Confirm the MCE unification goal

Gather:
- which business units or MCE data sources are in scope
- which engagement events must be available in Data Cloud
- which customer identifiers exist across MCE and CRM: subscriber key, contact key, email, CRM ID, or external profile IDs
- whether the user needs a new setup, a health check, or troubleshooting on an existing implementation

### 2. Route the request into Data Cloud phases

Use the existing sf-skills family:
- source connection and connector setup: [sf-datacloud-connect](../sf-datacloud-connect/SKILL.md)
- data streams and landing objects: [sf-datacloud-prepare](../sf-datacloud-prepare/SKILL.md)
- mappings, DMOs, and identity resolution: [sf-datacloud-harmonize](../sf-datacloud-harmonize/SKILL.md)
- segmentation built from engagement history: [sf-datacloud-segment](../sf-datacloud-segment/SKILL.md)
- downstream activation if the audience must be pushed out: [sf-datacloud-act](../sf-datacloud-act/SKILL.md)
- broader customer-360 orchestration: [sf-datacloud-unify](../sf-datacloud-unify/SKILL.md)

Use this skill as the specialized entry point for email engagement unification. Hand off to the phase-specific skill once the work narrows.

### 3. Build the MCE-to-profile plan

Structure the plan in this order:
1. establish the MCE connection
2. identify the engagement datasets to ingest
3. create or inspect engagement data streams
4. map engagement records to profile entities
5. define identity resolution inputs
6. expose engagement history for segmentation and personalization

Prefer explicit matching keys over inferred identity rules. If subscriber identity cannot be tied back to CRM identity, call that out before promising unified profiles.

### 4. Verify each milestone

Check:
- the MCE connection exists and authenticates
- send, open, and click data lands in the expected Data Cloud stream or object
- profile matching keys are present and usable
- unified profiles actually show engagement history
- segment logic can target engaged or unengaged audiences as intended

Do not stop at "connection created." The core value is unified engagement history on the customer profile.

## Common Request Patterns

Use this skill when the user says things like:
- "Connect Marketing Cloud Engagement to Data Cloud."
- "Bring email opens and clicks into unified customer profiles."
- "Use MCE engagement for segmentation and personalization."
- "Map subscriber activity into Data Cloud so we can build smarter audiences."

## Output Format

Respond in this order:
1. prerequisites status
2. MCE and CRM identity inputs
3. Data Cloud phases involved
4. current setup or gaps
5. plan of action
6. verification status
7. next recommended step

Suggested shape:

```text
Prerequisites: <ready / blocked>
MCE scope: <business units, events, identifiers>
Phases: <connect, prepare, harmonize, segment, act>
Current state: <new implementation / partial setup / troubleshooting>
Plan: <ordered actions>
Verification: <what is confirmed so far>
Next step: <highest-value next action>
```
