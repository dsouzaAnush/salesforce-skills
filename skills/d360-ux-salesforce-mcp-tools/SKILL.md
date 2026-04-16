---
name: d360-ux-salesforce-mcp-tools
description: Guide for using the Salesforce DX MCP server tools available in this repo (mcp.json). Invoke this skill when you need to look up SLDS blueprints, get Salesforce design guidance, convert a Figma design to LWC, or you're unsure which MCP tool to call. Trigger on: "use the MCP", "look up the blueprint", "check SLDS", "what component should I use", "find the design system pattern", "I have a Figma design", "how do I build this in Salesforce", or any time the d360-ux-lwc-ui-checklist skill directs you to call an MCP tool. Also invoke proactively when exploring unfamiliar UI patterns in this repo.
---

# Salesforce DX MCP Tools Guide

This repo's `mcp.json` wires up the `@salesforce/mcp` server with two toolsets and four specific tools. Each tool has a distinct purpose — calling the wrong one wastes context and gives worse results.

## The Four Tools

### `guide_slds_blueprints`
**When to use:** You need an overview of what blueprints exist, or you're not sure what to search for.

This tool returns a full index of all ~85 SLDS Component Blueprints organized by category. Call it first when starting Step 2 of the UI checklist and you don't already know the blueprint name.

**Good trigger phrases:**
- "What blueprints are available for navigation?"
- "Show me all data display blueprints"
- "I need a list to pick the right component"

---

### `explore_slds_blueprints`
**When to use:** You know (or suspect) a specific blueprint exists and need its full spec — markup, variants, CSS classes, and modifiers.

Supports multiple search modes — use whichever is most specific:
- `name` — exact blueprint name (e.g., `"data-table"`, `"card"`, `"path"`)
- `search` — keyword search across names and descriptions (e.g., `"progress"`, `"badge"`)
- `category` — filter by category (e.g., `"navigation"`, `"data-entry"`, `"feedback"`)
- `lightning_component` — find blueprints by their LBC counterpart (e.g., `"lightning-datatable"`)
- `slds_class` — find blueprints using a known CSS class (e.g., `"slds-badge"`)
- `styling_hook` — find blueprints that expose a specific CSS custom property

**Good trigger phrases:**
- "Get me the full spec for the path blueprint"
- "Search blueprints for 'spinner'"
- "What blueprint uses `slds-progress-ring`?"

**Typical workflow (Step 2 of UI checklist):**
1. Call `guide_slds_blueprints` → find the right category/name
2. Call `explore_slds_blueprints` with `name` → get the full markup and variants
3. Create a `ui-*` LWC that implements the blueprint

---

### `guide_design_general`
**When to use:** You need high-level Salesforce design guidance — principles, patterns, accessibility, or layout decisions — before committing to an approach.

This tool gives strategic direction: when to use which pattern, how to handle responsive layouts, accessibility requirements, and UX best practices within the Salesforce design language.

**Good trigger phrases:**
- "What's the recommended pattern for an empty state?"
- "How should I handle error messaging in LWC?"
- "What's the Salesforce approach for progressive disclosure?"
- "Is this layout accessible?"
- "Should I use a modal or a panel for this?"

---

### `guide_figma_to_lwc_conversion`
**When to use:** You have a Figma design (or a description of one) and need to map it to LWC components and SLDS classes.

This tool knows how Figma component names map to Lightning Base Components and SLDS patterns. It bridges the gap between what designers deliver and what developers implement.

**Good trigger phrases:**
- "I have this Figma design, what LWC components should I use?"
- "The designer gave me a comp with these elements — how do I build it?"
- "Convert this design to LWC"
- "What's the LWC equivalent of this Figma component?"

---

## Decision Flow

```
Starting UI work?
  │
  ├─ Have a Figma design? → guide_figma_to_lwc_conversion
  │
  ├─ Need design guidance / best practices? → guide_design_general
  │
  └─ Need a component blueprint?
       │
       ├─ Don't know what exists? → guide_slds_blueprints (index)
       │
       └─ Know what you need? → explore_slds_blueprints (full spec)
```

---

## Integration with the UI Checklist

The `d360-ux-lwc-ui-checklist` skill calls these tools at specific steps:

- **Step 2 (Blueprint search):** Call `guide_slds_blueprints` then `explore_slds_blueprints`
- **Any step (Design guidance):** Call `guide_design_general` if the right approach is unclear
- **Before Step 1 (Figma input):** Call `guide_figma_to_lwc_conversion` to map design → LBC first

---

## Notes on the MCP Server

The server runs via `npx @salesforce/mcp@latest` (see `mcp.json`). It requires network access to pull the latest component specs. If a tool call fails or returns stale data, the server may need to restart — run `claude mcp` or restart the Claude Code session.

The `--allow-non-ga-tools` flag is set, so tools in beta/preview may be available — treat their output as guidance, not spec.
