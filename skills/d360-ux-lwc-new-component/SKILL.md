---
name: d360-ux-lwc-new-component
description: Step-by-step workflow for creating new Lightning Web Components in the data360-vibe-foundation repo. Invoke this skill whenever someone asks to create a new component, add a page, build a new view, add a route, scaffold a new LWC, or set up a new UI module. Trigger on: "create a component", "add a new page", "new LWC", "add a route", "scaffold", "make a page for X", "build a reusable component", "add to the nav", or any variation of "I need a new [thing] in the app". Always invoke before creating any new files so the correct namespace and registration steps are followed.
---

# LWC New Component Workflow

This repo has a strict structure for new components. Getting the namespace wrong or skipping registration steps causes import errors or missing nav entries that are hard to debug. Follow the steps in order.

---

## Step 1 — Choose the Right Namespace

There are exactly 3 namespaces for new components. Pick based on what the component does:

| Namespace | Path | Tag prefix | Use for |
|-----------|------|------------|---------|
| `page` | `src/modules/page/<name>/` | `page-<name>` | Full-page route views. One per route. |
| `ui` | `src/modules/ui/<name>/` | `ui-<name>` | Reusable building blocks used inside pages or other components. |
| `shell` | `src/modules/shell/<name>/` | `shell-<name>` | App chrome only (header, nav, panel). Do not put feature UI here. |

**When in doubt:** if it's a page the router navigates to → `page/`. If it's a component that appears inside a page → `ui/`. Never add to `shell/` for feature work.

**Do NOT create components under:**
- `src/modules/lightning/` — reserved for LBC overrides
- `src/build/lightning-icon/shims/` — reserved for icon overrides

---

## Step 2 — Create the Component Files

Every LWC is a folder containing at minimum 2 files. Create them now.

### For a `ui/*` component (reusable):

```
src/modules/ui/<name>/
├── <name>.html      ← template
├── <name>.js        ← controller
└── <name>.css       ← styles (optional but recommended)
```

**`<name>.html` starter:**
```html
<template>
    <!-- component markup here -->
</template>
```

**`<name>.js` starter:**
```javascript
import { LightningElement } from 'lwc';

export default class <PascalCaseName> extends LightningElement {}
```

**`<name>.css` starter:**
```css
:host {
    display: block;
}
```

### For a `page/*` component (route view):

Same file structure as `ui/*`, but the JS also needs to import the router if it uses path params:

```javascript
import { LightningElement } from 'lwc';
import { getCurrentRoute } from '../../router/router';  // only if using route params

export default class <PascalCaseName> extends LightningElement {
    // connectedCallback() { const route = getCurrentRoute(); }
}
```

---

## Step 3 — Register in routes.config.js (pages only)

If the new component is a `page/*`, open `src/routes.config.js` and add a route entry. Skip this step for `ui/*` components.

**Route entry shape:**

```javascript
{
    path: '/your-path',           // URL path (use :param for dynamic segments)
    component: 'page-your-name', // kebab-case tag name
    title: 'Page Title',          // string, or function: (route) => `Detail: ${route.params.id}`
    navPage: 'your-name',        // creates a nav tab — omit if this is a child route
    // navHighlight: 'parent-name'  // use instead of navPage for child routes (e.g. /contacts/:id)
}
```

**navPage vs navHighlight:**
- `navPage: 'name'` → creates a tab in global navigation
- `navHighlight: 'parent-name'` → highlights an existing parent tab (no new tab created); use for detail/child routes like `/contacts/:id`

**Example — top-level page with nav tab:**
```javascript
{ path: '/reports', component: 'page-reports', title: 'Reports', navPage: 'reports' }
```

**Example — child route (no new tab):**
```javascript
{ path: '/reports/:id', component: 'page-report-detail', title: (r) => `Report ${r.params.id}`, navHighlight: 'reports' }
```

---

## Step 4 — Register in shell/app/app.js (pages only)

Open `src/modules/shell/app/app.js`. Find the `ROUTE_COMPONENTS` map and add your page component.

```javascript
import PageYourName from 'page/yourName';

const ROUTE_COMPONENTS = {
    // ... existing entries
    'page-your-name': PageYourName,
};
```

The key must match the `component` value in `routes.config.js` exactly.

---

## Step 5 — Use the Component

### Using a `ui/*` component inside a page or another component:

```html
<!-- in some-page.html -->
<template>
    <ui-your-name></ui-your-name>
</template>
```

```javascript
// in some-page.js — no import needed, LWC resolves by tag name
```

### Navigating to a `page/*` route:

```javascript
import { navigate } from '../../router/router';
// ...
navigate('/your-path');
```

Or use an anchor/button that calls `navigate()`.

---

## Step 6 — Run the Dev Server

After creating files, if the dev server isn't running:

```bash
npm run dev
```

If icons are broken after adding new components, re-run `npm run dev` (the icon prebuild step runs automatically).

---

## Checklist Summary

```
[ ] 1. Chose correct namespace: page/ ui/ shell/
[ ] 2. Created <name>.html, <name>.js, <name>.css
[ ] 3. Added route to src/routes.config.js        (pages only)
[ ] 4. Imported + registered in shell/app/app.js  (pages only)
[ ] 5. Dev server running / restarted
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Component renders blank | Check `app.js` ROUTE_COMPONENTS — import missing |
| Route 404 | Check `routes.config.js` — path typo or not added |
| Nav tab not showing | Make sure `navPage` is set (not just `navHighlight`) |
| Nav tab always highlighted | Check `navHighlight` on child routes — should match parent's `navPage` value |
| Import error `Cannot resolve module` | Verify folder name matches tag name exactly (kebab-case) |
