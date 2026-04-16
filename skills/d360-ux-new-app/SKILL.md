---
name: d360-ux-new-app
description: Use when adding a new app to the data360-vibe-foundation prototype — triggered by "new app", "add an app", "scaffold an app", "create a [Name] app", or any request to wire up a new top-level app with its own nav, pages, and routes.
---

# New App

Guided workflow that collects five inputs, then scaffolds all files needed to wire a new app into data360-vibe-foundation: an app entry in `apps.config.js`, stub page components under `src/modules/page/`, route entries in `routes.config.js`, and imports + ROUTE_COMPONENTS entries in `shell/app/app.js`.

---

## Step 1 — Gather Inputs (ask in sequence, wait for each answer)

### Q1 — App Name

Ask: **"What is the app name/label?"** (e.g., `Data Management`)

Derive the app id automatically:
- Lowercase, replace spaces with hyphens, strip non-alphanumeric (except hyphens)
- Example: `Data Management` → `data-management`

Show the derived id and ask: **"App id will be `<id>` — confirm or enter a different id."**

### Q2 — Nav Type

Ask: **"Horizontal nav (tab bar) or vertical nav (sidebar with groups)?"**

- **horizontal** → `contextBarItems` tab array, no `navItems`
- **vertical** → `navItems` groups with children, single Home `contextBarItem`

### Q3 — Default App

Ask: **"Should this be the default app? (y/n)"**

If yes: note which existing app has `isDefault: true` — you will set it to `false` when editing `apps.config.js`.

### Q4 — Screenshot

Ask: **"Do you have a screenshot or mockup of the app? Provide the image path, or press Enter to skip."**

If a path is provided:
- Read the image with the Read tool
- Identify tab/group names, page names, and recognizable Lightning Base Components or SLDS patterns (cards, data tables, badges, charts, filters, panels, etc.)
- Use findings to name the tabs/groups/items and generate richer page stubs

If skipped:
- **Horizontal**: create 3 default tabs: `Dashboard` (`/<app-id>/dashboard`), `List` (`/<app-id>/list`), `Settings` (`/<app-id>/settings`)
- **Vertical**: create 2 groups with 2 children each using generic labels (`Group 1`, `Group 2` / `Item 1`, `Item 2`)

### Q5 — App Icon

Ask: **"What utility icon should represent this app in the app switcher? (e.g., utility:apps) — press Enter to use the default `utility:apps`."**

---

## Step 2 — Derive All Names

For each tab (horizontal) or group child (vertical), derive from the label or route slug:

| Derived value | Rule | Example input: `data-streams` |
|---|---|---|
| `pageName` (folder) | kebab → camelCase | `dataStreams` |
| `className` (JS class) | PascalCase | `DataStreams` |
| `componentTag` | `page-` + slug | `page-data-streams` |
| `navPageId` | slug as-is | `data-streams` |

For vertical nav group children, prefix the navItemId: `<group-prefix>-<navPageId>` (e.g., `dm-data-streams` where `dm` = data-management first-letters).

---

## Step 3 — Create Page Components

For each tab/item create `src/modules/page/<pageName>/<pageName>.html` and `.js`.

### Minimal stub (no screenshot):

```html
<template>
    <div class="slds-p-around_large">
        <h1 class="slds-text-heading_large"><PAGE_LABEL></h1>
        <p class="slds-text-body_regular slds-m-top_medium slds-text-color_weak">
            <!-- TODO: implement <PAGE_LABEL> page -->
        </p>
    </div>
</template>
```

### Richer stub (screenshot provided — use identified components):

```html
<template>
    <div class="slds-p-around_large">
        <h1 class="slds-text-heading_large slds-m-bottom_medium"><PAGE_LABEL></h1>
        <lightning-layout multiple-rows="true">
            <!-- TODO: <lightning-card title="..."> — identified from mockup -->
            <!-- TODO: <lightning-datatable ...> — identified from mockup -->
            <!-- Add one comment block per identified component/section -->
        </lightning-layout>
    </div>
</template>
```

### `.js` for all stubs:

```javascript
import { LightningElement } from 'lwc';
export default class <ClassName> extends LightningElement {}
```

---

## Step 4 — Add Routes to `src/routes.config.js`

Append one entry per page to the `routes` array.

**Horizontal (each tab gets `navPage` + `navLabel`):**

```javascript
{
    path: '/<app-id>/<tab-slug>',
    component: '<componentTag>',
    title: '<Tab Label>',
    navPage: '<tab-slug>',
    navLabel: '<Tab Label>',
},
```

**Vertical (nav items don't need `navPage`/`navLabel` — paths drive the sidebar):**

```javascript
{
    path: '/<group-slug>/<item-slug>',
    component: '<componentTag>',
    title: '<Group Label> — <Item Label>',
},
```

---

## Step 5 — Register in `src/modules/shell/app/app.js`

Add one import per page at the top (keep alphabetical by label):

```javascript
import <ClassName> from 'page/<pageName>';
```

Add one entry per page to `ROUTE_COMPONENTS`:

```javascript
'<componentTag>': <ClassName>,
```

---

## Step 6 — Add App Entry to `src/apps.config.js`

### Horizontal app entry:

```javascript
{
    id: '<app-id>',
    label: '<App Label>',
    isDefault: false,            // or true if Q3 was yes
    icon: '<utility:icon>',
    navType: 'horizontal',
    contextBarItems: [
        { page: '<tab-slug>', label: '<Tab Label>', path: '/<app-id>/<tab-slug>' },
        // ... one per tab
    ],
    navItems: [],
},
```

### Vertical app entry:

```javascript
{
    id: '<app-id>',
    label: '<App Label>',
    isDefault: false,            // or true if Q3 was yes
    icon: '<utility:icon>',
    navType: 'vertical',
    contextBarItems: [
        { page: 'home', label: 'Home', path: '/' },
    ],
    navItems: [
        {
            id: '<group-slug>',
            label: '<Group Label>',
            icon: 'utility:list',    // pick a fitting utility icon per group
            children: [
                { id: '<group-prefix>-<item-slug>', label: '<Item Label>', path: '/<group-slug>/<item-slug>', component: '<componentTag>' },
            ],
        },
    ],
},
```

If Q3 was yes (new app is default): also update the previous default app entry — change its `isDefault: true` to `isDefault: false`.

---

## Step 7 — Confirm the Scaffold

Print a summary table:

| What | Where |
|------|-------|
| App entry | `src/apps.config.js` — `id: '<app-id>'` |
| Page components | `src/modules/page/<pageName>/` (one per tab/item) |
| Routes | `src/routes.config.js` — `<N>` entries added |
| ROUTE_COMPONENTS | `src/modules/shell/app/app.js` |

Remind: **if the dev server is already running, a hard-refresh is enough; otherwise run `npm run dev`.**

---

## Naming Quick Reference

```
app label:        Data Management
app id:           data-management
tab/item slug:    data-streams
pageName folder:  dataStreams
class name:       DataStreams
component tag:    page-data-streams
navPage id:       data-streams        (horizontal only)
navItem id:       dm-data-streams     (vertical; dm = data-management prefix)
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Blank page renders | `ROUTE_COMPONENTS` key doesn't match `component` in routes.config |
| App not in switcher | `icon` field missing or not a valid `utility:` icon name |
| Vertical nav items invisible | `navItems[].children` must include `component` field matching ROUTE_COMPONENTS key |
| Two default apps | When setting `isDefault: true`, always unset previous default |
| Import error | Folder name must be camelCase and exactly match import path |
| App id collision | Check existing `apps.config.js` ids before adding |
