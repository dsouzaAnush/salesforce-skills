---
name: d360-ux-lwc-ui-checklist
description: Enforces the mandatory 5-step UI decision tree before writing any Lightning Web Component (LWC) markup, styling, or logic. Covers 25+ Lightning Base Components and 128+ SLDS Blueprints. Invoke this skill whenever someone asks you to build, add, style, or modify any UI element, component, page, layout, or visual feature. Also trigger when you hear: "add a button", "style this", "create a card", "make a table", "show this data", "build a form", "add a modal", "lay this out", or any variation of writing HTML/CSS/JS for UI. If there is even a 1% chance this involves UI markup or styling, invoke this skill first — before touching any file.
---

# LWC UI Code Checklist

Before writing ANY HTML, CSS, or component JavaScript in this repo, you must work through this checklist **in order**. Each step is a gate: only proceed to the next if the current step cannot satisfy the requirement.

The goal is to stay as close to the Salesforce platform as possible — native components first, custom code last. This keeps the UI consistent, accessible, theme-aware (SLDS 1 + SLDS 2 / dark mode), and maintainable.

---

## The 5-Step Decision Tree

### Step 1 — Does a Lightning Base Component (LBC) exist?

Lightning Base Components are pre-built LWCs from Salesforce that ship with this repo via `lightning-base-components`. They have built-in JavaScript APIs, events, accessibility, and SLDS styling.

**How to check:** Look at the common components below, or search the `node_modules/lightning-base-components/src/` directory.

**Common LBCs:**

| Need | Component |
|------|-----------|
| Button | `<lightning-button>` (variants: base, neutral, brand, destructive, success) |
| Text input | `<lightning-input>` (type: text, email, date, number, checkbox, toggle) |
| Textarea | `<lightning-textarea>` |
| Dropdown/select | `<lightning-combobox>` |
| Card container | `<lightning-card>` (slots: header, actions, footer) |
| Data table | `<lightning-datatable>` |
| Badge | `<lightning-badge>` |
| Icon | `<lightning-icon>` (use this — do not inline SVGs) |
| Spinner | `<lightning-spinner>` |
| Modal | Extend `LightningModal` from `lightning/modal` — see `src/modules/ui/demoModal/` for the reference pattern |
| Tab set | `<lightning-tabset>` / `<lightning-tab>` |
| Accordion | `<lightning-accordion>` / `<lightning-accordion-section>` |
| Avatar | `<lightning-avatar>` |
| Avatar group | `<lightning-avatar-group>` |
| Pill | `<lightning-pill>` |
| Progress bar | `<lightning-progress-bar>` |
| Vertical nav | `<lightning-vertical-navigation>` |
| Layout | `<lightning-layout>` / `<lightning-layout-item>` (use for grid-based layouts) |
| Alert/Banner | `<lightning-alert>` or `<lightning-banner>` (dismissible notifications) |
| Radio button | `<lightning-radio-group>` |
| Slider | `<lightning-slider>` (range input) |
| Breadcrumb | `<lightning-breadcrumb>` / `<lightning-breadcrumb-item>` |
| Help text | `<lightning-helptext>` (inline documentation/tooltips) |
| Color picker | `<lightning-color-picker>` |
| Dueling picklist | `<lightning-dueling-picklist>` |

**If YES → use it. Stop here.**

**If NO → proceed to Step 2.**

---

### Step 2 — Does an SLDS Component Blueprint exist?

Blueprints are HTML/CSS-only patterns from the Lightning Design System. Use the MCP tools to search for them — do not guess class names.

**How to check (use MCP tools in this order):**

1. Call `guide_slds_blueprints` for a full index of all ~128 available blueprints organized by category.
2. Call `explore_slds_blueprints` with a `search` keyword or `name` to retrieve the full spec for a candidate blueprint.

**Common SLDS Blueprints (reference — always verify with MCP tools):**

| Use Case | Blueprint Name | Notes |
|----------|---|---|
| Two-column resizable layout | Split View | See `src/modules/ui/splitView/` for reference implementation |
| Collapsible content | Expandable Section | Alternative to accordion for single sections |
| Temporary notifications | Toast, Notification, Scoped Notification | Use for feedback messages |
| Contextual overlays | Popover | For non-modal supplementary content |
| Page section headers | Page Header | Includes title, actions, breadcrumbs slot |
| Application chrome | Global Header, Global Navigation | For app-level shells |
| Navigation breadcrumbs | Breadcrumbs | Hierarchical navigation trail |
| Data visualization | Tree, Tree Grid | Hierarchical or tabular data display |
| Form container | Form Layout, Form Element | Structured form layout patterns |
| Rich text input | Rich Text Editor | WYSIWYG editor |
| Dismissible banners | Brand Band, Trial Bar | For promotions or alerts |
| Side panel | Docked Utility Bar, Docked Composer | Fixed side UI elements |
| List builder | List Builder | Reorderable list of items |
| Interactive menu | Dynamic Menu, Menus | Custom dropdown/context menus |
| Date/time selection | Datepicker, Datetime Picker, Timepicker | Calendar-based input |
| Visual selection | Visual Picker, Color Picker | Grid-based option selection |

**If a blueprint exists → create a new LWC in `src/modules/ui/<name>/` that implements the blueprint markup.** Do not copy blueprint HTML directly into a page component — wrap it in its own `ui-*` component.

**If NO → proceed to Step 3.**

---

### Step 3 — Does an SLDS Utility Class cover the styling need?

Utility classes handle the vast majority of spacing, layout, alignment, text, and sizing needs. Check before writing any CSS.

**Common utility categories:**

| Category | Examples |
|----------|---------|
| Spacing | `slds-m-around_small`, `slds-p-horizontal_medium`, `slds-p-vertical_large` |
| Layout / Grid | `slds-grid`, `slds-wrap`, `slds-col`, `slds-size_1-of-2`, `slds-medium-size_1-of-3` |
| Text | `slds-text-heading_large`, `slds-text-body_regular`, `slds-text-align_center` |
| Display | `slds-show`, `slds-hide`, `slds-is-relative` |
| Truncation | `slds-truncate` |
| Alignment | `slds-align_absolute-center` |

**If YES → apply the class in the HTML template. Stop here.**

**If NO → proceed to Step 4.**

---

### Step 4 — Does an SLDS Global Styling Hook cover the CSS need?

Styling hooks are CSS custom properties (variables) that respect the active theme (SLDS 1, SLDS 2, dark mode). Always prefer them over hard-coded values.

**Always provide a fallback value:** `background: var(--slds-g-color-surface-1, #fff);`

**Common hook categories:**

| Category | Examples |
|----------|---------|
| Surface backgrounds | `--slds-g-color-surface-1`, `--slds-g-color-surface-2` |
| Container backgrounds | `--slds-g-color-surface-container-1`, `--slds-g-color-surface-container-2` |
| Text / on-surface | `--slds-g-color-on-surface-1`, `--slds-g-color-on-surface-2` |
| Accent | `--slds-g-color-accent-1`, `--slds-g-color-accent-container-1` |
| Border | `--slds-g-color-border-1`, `--slds-g-color-border-accent-1` |
| Feedback | `--slds-g-color-error-1`, `--slds-g-color-success-1`, `--slds-g-color-warning-1` |

**Use hooks semantically — never repurpose a hook for an unintended CSS property:**
- ❌ `width: var(--slds-g-radius-border-circle)` — radius token used for width
- ✅ `background-color: var(--slds-g-color-surface-1, #fff)` — surface token used for background

**If YES → write the CSS rule using the hook with a fallback. Stop here.**

**If NO → proceed to Step 5.**

---

### Step 5 — Use a hard-coded CSS value

Only reach here when Steps 1–4 are exhausted. Acceptable cases: `height: 100%`, `z-index`, animation/transform values, percentages for custom geometry.

**Hard rules that apply at every step:**
- Never use `!important`
- Never override SLDS classes in your CSS
- Never use inline `style=""` attributes — always CSS files or utility classes

---

## Quick Reference Card

```
Need UI? → Step 1: LBC available?
              YES → use <lightning-*> or extend LightningModal
              NO  → Step 2: SLDS Blueprint?
                      YES → new ui-* LWC implementing blueprint
                      NO  → Step 3: SLDS Utility Class?
                              YES → add class to template HTML
                              NO  → Step 4: SLDS Styling Hook?
                                      YES → CSS var with fallback
                                      NO  → Step 5: hard-coded value
```

---

## Troubleshooting: "I don't see my component here"

**Did not find what you need?**

1. **For LBCs:** Search `node_modules/lightning-base-components/src/` for the component (e.g., `grep -r "color-picker" node_modules/lightning-base-components/src/`)
2. **For Blueprints:** Run `guide_slds_blueprints` to search the full ~128 blueprint catalog by keyword
3. **For any component:** Ask Claude to search `node_modules/lightning-base-components/` or use the MCP tools to verify availability

**Component not found?**

If the component truly doesn't exist:
- File an issue with the component name and requirement (e.g., "need a two-column layout, split-view pattern")
- Submit a PR to this skill if you implement a new custom component following Steps 2–5

**If you find an LBC or Blueprint that's missing from this skill's reference tables:**
- File an issue with the component name and whether it's an LBC or blueprint
- Submit a PR to update this skill's reference tables

---

## Special Cases

**Modals**: Always extend `LightningModal`. Use `src/modules/ui/demoModal/` as the reference. Never build modals from raw `slds-modal` markup.

**Icons**: Always use `<lightning-icon>`. Never inline SVGs or use `<img>` for icons. The icon names follow the pattern `category:name` (e.g., `utility:add`, `standard:contact`).

**Forms**: Prefer `<lightning-input>` for all form fields. Only fall back to blueprint-based inputs when the input type is unsupported.

**Tables**: Use `<lightning-datatable>` for sortable/selectable data. Only build a custom table LWC if datatable's column types don't fit the need.
