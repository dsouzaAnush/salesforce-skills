---
name: d360-ux-add-nav-item
description: Use when adding a new real page to the vertical sidebar nav in data360-vibe-foundation — triggered by "add a nav item", "wire up a page", "create a page for X group", "scaffold a nav page", or any request to turn a stub nav entry into a real route with an LWC component.
---

# Add Nav Item

Guided workflow that collects four inputs, then scaffolds an LWC page component, a route entry, and a wired nav item in one pass. Wraps and extends `d360-ux-lwc-new-component`.

---

## Step 1 — Gather Inputs (ask in sequence)

### Q1 — Nav Group

Read `src/apps.config.js`. Show the developer the current nav groups:

| id | label |
|----|-------|
| connect-unify | Connect & Unify |
| govern-secure | Govern & Secure |
| process-enrich | Process & Enrich |
| explore-optimize | Explore & Optimize |
| analyze-predict | Analyze & Predict |
| segment-act | Segment & Act |

Ask: **"Which nav group does this item belong to?"** (accept the id or label)

### Q2 — Nav Item Label

Ask: **"What is the nav item label?"** (e.g., `Data Streams`)

### Q3 — Route / Slug

Ask: **"What is the page route? (e.g. /connect-unify/data-streams)"**

Derive names from the **last path segment** of the route:

| Derived value | Rule | Example |
|---------------|------|---------|
| `pageName` (folder) | kebab-to-camelCase | `data-streams` → `dataStreams` |
| `className` (JS class) | PascalCase | `DataStreams` |
| `componentTag` | `page-` + last segment | `page-data-streams` |
| `navPageId` | last segment as-is | `data-streams` |
| `navItemId` | group-prefix + `-` + navPageId | `cu-data-streams` |

Use a short group prefix (first two letters of each word, e.g., `cu` for connect-unify, `gs` for govern-secure, `pe` for process-enrich, `eo` for explore-optimize, `ap` for analyze-predict, `sa` for segment-act).

### Q4 — Mockup / Screenshot

Ask: **"Do you have a mockup or screenshot for this page? If yes, provide the image path; otherwise press Enter to skip."**

If an image path is provided:
- Read the image with the Read tool
- Identify which Lightning Base Components and SLDS patterns are visible (cards, data tables, badges, charts, filters, modals, etc.)
- Use these findings to generate a richer HTML stub (see Step 3b below)

---

## Step 2 — Create the LWC Page Component

Create the folder and files at `src/modules/page/<pageName>/`.

### `<pageName>.html` — minimal stub (no mockup):

```html
<template>
    <div class="slds-p-around_large">
        <h1 class="slds-text-heading_large"><NAV_LABEL></h1>
        <p class="slds-text-body_regular slds-m-top_medium slds-text-color_weak">
            <!-- TODO: implement <NAV_LABEL> page -->
        </p>
    </div>
</template>
```

### `<pageName>.html` — richer stub (mockup provided):

Use `lightning-layout` / `lightning-layout-item` as the outer shell. For each identified component add a commented placeholder:

```html
<template>
    <div class="slds-p-around_large">
        <h1 class="slds-text-heading_large slds-m-bottom_medium"><NAV_LABEL></h1>
        <lightning-layout multiple-rows="true">
            <!-- TODO: <lightning-card title="..."> — identified from mockup -->
            <!-- TODO: <lightning-datatable ...> — identified from mockup -->
            <!-- Add one comment block per identified component -->
        </lightning-layout>
    </div>
</template>
```

### `<pageName>.js`:

```javascript
import { LightningElement } from 'lwc';

export default class <ClassName> extends LightningElement {}
```

---

## Step 3 — Register the Route in `src/routes.config.js`

Add a new entry to the `routes` array. Follow the existing ordering (group pages together near related entries if possible):

```javascript
{
    path: '<ROUTE>',
    component: '<componentTag>',
    title: '<Nav Label>',
    navPage: '<navPageId>',
    navLabel: '<Nav Label>',
},
```

---

## Step 4 — Register the Component in `src/modules/shell/app/app.js`

Add the import and the ROUTE_COMPONENTS entry:

```javascript
// At the top with other page imports:
import <ClassName> from 'page/<pageName>';

// In ROUTE_COMPONENTS:
'<componentTag>': <ClassName>,
```

---

## Step 5 — Wire the Nav Item in `src/apps.config.js`

Find the target nav group's `children` array. **Add a new child** (do not overwrite existing stubs unless one is clearly a placeholder with an auto-generated label like "Item 1"):

```javascript
{ id: '<navItemId>', label: '<Nav Label>', path: '<ROUTE>' },
```

If an obvious stub (`label: 'Item 1'`, `path: '/'`) exists in the correct group and the developer confirms they want to replace it, update that entry instead of appending.

---

## Step 6 — Confirm the Scaffold

After all files are written, print a summary table:

| What | Where |
|------|-------|
| Page component | `src/modules/page/<pageName>/<pageName>.html` + `.js` |
| Route entry | `src/routes.config.js` — `path: '<ROUTE>'` |
| ROUTE_COMPONENTS | `src/modules/shell/app/app.js` |
| Nav item | `src/apps.config.js` → `<group>.children` |

Then remind the developer: **if the dev server is already running, a hard-refresh is enough; otherwise run `npm run dev`**.

---

## Naming Quick Reference

```
route slug:       /connect-unify/data-streams
last segment:     data-streams
pageName folder:  dataStreams
class name:       DataStreams
component tag:    page-data-streams
navPage id:       data-streams
navItem id:       cu-data-streams   (cu = connect-unify prefix)
```

Group prefixes: `cu` · `gs` · `pe` · `eo` · `ap` · `sa`

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Blank page renders | `ROUTE_COMPONENTS` import missing or key doesn't match `component` in routes.config |
| Nav item doesn't highlight | `navPage` in routes.config must match the `id` used in nav active-state logic |
| Route 404 | Path in routes.config doesn't match what was entered in apps.config |
| Import error | Folder name must be camelCase and match the import path exactly |
| Added to wrong app | Vertical nav items live under the `data360` app entry in apps.config, not `template` |
