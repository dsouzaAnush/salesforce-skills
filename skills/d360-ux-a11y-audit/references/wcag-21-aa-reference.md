# WCAG 2.1 Level AA Compliance Reference

> Comprehensive reference for building an AI-powered accessibility audit skill.
> Focused on criteria evaluable through static code analysis.

---

## 1. Complete WCAG 2.1 Level A + AA Success Criteria

### Principle 1: Perceivable

Information and UI components must be presentable in ways users can perceive.

#### Guideline 1.1 Text Alternatives

| # | Name | Level | Requirement | Static Analysis? |
|---|------|-------|-------------|-----------------|
| 1.1.1 | Non-text Content | A | All non-text content (images, icons, buttons) must have text alternatives | YES - check `alt` on `<img>`, `aria-label` on icon buttons, `<input type="image">` |

#### Guideline 1.2 Time-based Media

| # | Name | Level | Requirement | Static Analysis? |
|---|------|-------|-------------|-----------------|
| 1.2.1 | Audio-only and Video-only (Prerecorded) | A | Provide text transcript or audio description | PARTIAL - detect `<audio>`/`<video>` without `<track>` |
| 1.2.2 | Captions (Prerecorded) | A | Synchronized captions for all prerecorded audio in video | PARTIAL - detect `<video>` missing `<track kind="captions">` |
| 1.2.3 | Audio Description or Media Alternative (Prerecorded) | A | Audio description or text alternative for video | PARTIAL |
| 1.2.4 | Captions (Live) | AA | Captions for live audio content | NO - runtime |
| 1.2.5 | Audio Description (Prerecorded) | AA | Audio description for all prerecorded video | PARTIAL |

#### Guideline 1.3 Adaptable

| # | Name | Level | Requirement | Static Analysis? |
|---|------|-------|-------------|-----------------|
| 1.3.1 | Info and Relationships | A | Structure/relationships conveyed visually must be programmatically determinable | YES - semantic HTML, proper heading hierarchy, table headers, label associations |
| 1.3.2 | Meaningful Sequence | A | Reading order must be programmatically determinable | PARTIAL - check DOM order vs CSS visual order |
| 1.3.3 | Sensory Characteristics | A | Instructions must not rely solely on shape, color, size, location | PARTIAL - flag text like "click the red button" |
| 1.3.4 | Orientation | AA | Content not restricted to single display orientation | YES - check CSS for `orientation` lock in media queries |
| 1.3.5 | Identify Input Purpose | AA | Input fields have programmatically determinable purpose | YES - check `autocomplete` attributes on user-info inputs |

#### Guideline 1.4 Distinguishable

| # | Name | Level | Requirement | Static Analysis? |
|---|------|-------|-------------|-----------------|
| 1.4.1 | Use of Color | A | Color not sole means of conveying information | PARTIAL - flag color-only indicators |
| 1.4.2 | Audio Control | A | Auto-playing audio > 3s needs pause/stop controls | PARTIAL - detect `autoplay` on `<audio>`/`<video>` |
| 1.4.3 | Contrast (Minimum) | AA | 4.5:1 for normal text, 3:1 for large text (18pt+ or 14pt bold+) | YES - analyze CSS color/background-color pairs |
| 1.4.4 | Resize Text | AA | Text resizable to 200% without loss of function | YES - check `user-scalable=no` or `maximum-scale=1` in viewport meta |
| 1.4.5 | Images of Text | AA | Use real text instead of images of text | PARTIAL - flag `<img>` in contexts where text would suffice |
| 1.4.10 | Reflow | AA | No 2D scrolling at 320px width (horizontal) or 256px height (vertical) | PARTIAL - check for fixed-width containers, `overflow: hidden` |
| 1.4.11 | Non-text Contrast | AA | 3:1 contrast for UI components and graphical objects | PARTIAL - analyze border/background colors on inputs, icons |
| 1.4.12 | Text Spacing | AA | No content loss when text spacing is increased | PARTIAL - flag fixed-height containers with `overflow: hidden` |
| 1.4.13 | Content on Hover or Focus | AA | Hover/focus content must be dismissible, hoverable, persistent | PARTIAL - check tooltip/popover patterns for `Escape` handling |

### Principle 2: Operable

UI components and navigation must be operable.

#### Guideline 2.1 Keyboard Accessible

| # | Name | Level | Requirement | Static Analysis? |
|---|------|-------|-------------|-----------------|
| 2.1.1 | Keyboard | A | All functionality available via keyboard | YES - check `onClick` without `onKeyDown`/`onKeyPress`, non-focusable interactive elements |
| 2.1.2 | No Keyboard Trap | A | Focus can always be moved away from any component | PARTIAL - detect focus trap patterns without escape |
| 2.1.4 | Character Key Shortcuts | A | Single-character shortcuts can be disabled/remapped | PARTIAL - detect single-key event listeners |

#### Guideline 2.2 Enough Time

| # | Name | Level | Requirement | Static Analysis? |
|---|------|-------|-------------|-----------------|
| 2.2.1 | Timing Adjustable | A | Time limits can be turned off/adjusted/extended | PARTIAL - detect `setTimeout`/`setInterval` for UI state |
| 2.2.2 | Pause, Stop, Hide | A | Moving/auto-updating content can be paused | PARTIAL - detect auto-play, carousels, marquee |

#### Guideline 2.3 Seizures and Physical Reactions

| # | Name | Level | Requirement | Static Analysis? |
|---|------|-------|-------------|-----------------|
| 2.3.1 | Three Flashes or Below Threshold | A | No content flashes > 3 times/second | PARTIAL - detect CSS animations with rapid state changes |

#### Guideline 2.4 Navigable

| # | Name | Level | Requirement | Static Analysis? |
|---|------|-------|-------------|-----------------|
| 2.4.1 | Bypass Blocks | A | Skip navigation mechanism available | YES - check for skip links, landmark regions |
| 2.4.2 | Page Titled | A | Pages have descriptive titles | YES - check `<title>` element presence and content |
| 2.4.3 | Focus Order | A | Focus order preserves meaning and operability | PARTIAL - check `tabindex` values > 0 |
| 2.4.4 | Link Purpose (In Context) | A | Link purpose determinable from text or context | YES - flag empty `<a>` tags, generic "click here" links |
| 2.4.5 | Multiple Ways | AA | Multiple methods to locate pages in a set | PARTIAL - check for nav, search, sitemap |
| 2.4.6 | Headings and Labels | AA | Headings and labels describe topic/purpose | YES - flag empty headings, generic labels |
| 2.4.7 | Focus Visible | AA | Visible focus indicator for keyboard navigation | YES - check CSS `outline: none`/`outline: 0` without replacement `:focus` styles |

#### Guideline 2.5 Input Modalities

| # | Name | Level | Requirement | Static Analysis? |
|---|------|-------|-------------|-----------------|
| 2.5.1 | Pointer Gestures | A | Complex gestures have single-pointer alternatives | PARTIAL |
| 2.5.2 | Pointer Cancellation | A | Actions not triggered on down-event alone | YES - check `onMouseDown`/`onTouchStart` as sole action triggers |
| 2.5.3 | Label in Name | A | Accessible name includes visible label text | YES - compare `aria-label` with visible text content |
| 2.5.4 | Motion Actuation | A | Motion-triggered features have UI alternatives | PARTIAL |
| 2.5.7 | Dragging Movements | AA | Drag operations have non-drag alternatives | PARTIAL - detect drag handlers without alternatives |
| 2.5.8 | Target Size (Minimum) | AA | Interactive targets at least 24x24 CSS pixels | PARTIAL - check explicit width/height on buttons/links |

### Principle 3: Understandable

Information and UI operation must be understandable.

#### Guideline 3.1 Readable

| # | Name | Level | Requirement | Static Analysis? |
|---|------|-------|-------------|-----------------|
| 3.1.1 | Language of Page | A | Page language identified with `lang` attribute | YES - check `<html lang="...">` |
| 3.1.2 | Language of Parts | AA | Language changes marked with `lang` attribute | PARTIAL - detect mixed-language content |

#### Guideline 3.2 Predictable

| # | Name | Level | Requirement | Static Analysis? |
|---|------|-------|-------------|-----------------|
| 3.2.1 | On Focus | A | No context change on focus | YES - check `onFocus` handlers that trigger navigation/submission |
| 3.2.2 | On Input | A | No unexpected context change on input | YES - check `onChange` that triggers navigation without warning |
| 3.2.3 | Consistent Navigation | AA | Navigation order consistent across pages | PARTIAL - compare nav structures across files |
| 3.2.4 | Consistent Identification | AA | Same-function components identified consistently | PARTIAL |

#### Guideline 3.3 Input Assistance

| # | Name | Level | Requirement | Static Analysis? |
|---|------|-------|-------------|-----------------|
| 3.3.1 | Error Identification | A | Input errors identified and described in text | PARTIAL - check form validation patterns |
| 3.3.2 | Labels or Instructions | A | Labels/instructions for user input | YES - check `<input>` has associated `<label>` or `aria-label` |
| 3.3.3 | Error Suggestion | AA | Suggestions provided for detected errors | PARTIAL |
| 3.3.4 | Error Prevention (Legal, Financial, Data) | AA | Submissions reversible, verified, or confirmed | PARTIAL |
| 3.3.7 | Redundant Entry | A | Previously entered info auto-populated or selectable | NO - runtime |
| 3.3.8 | Accessible Authentication (Minimum) | AA | Auth does not rely solely on cognitive function tests | PARTIAL |

### Principle 4: Robust

Content must be robust enough for assistive technologies.

#### Guideline 4.1 Compatible

| # | Name | Level | Requirement | Static Analysis? |
|---|------|-------|-------------|-----------------|
| 4.1.2 | Name, Role, Value | A | UI components have programmatic name, role, value | YES - check ARIA roles, custom elements with proper semantics |
| 4.1.3 | Status Messages | AA | Status messages announced without focus via live regions | YES - check `role="alert"`, `role="status"`, `aria-live` on dynamic messages |

---

## 2. Most Commonly Violated Criteria

Based on the WebAIM Million 2025 analysis of 1,000,000 home pages, **96% of all detected errors fall into just 6 categories**:

| Rank | Failure | % of Sites | WCAG Criterion | Level |
|------|---------|-----------|----------------|-------|
| 1 | Low contrast text | 79.1% | 1.4.3 Contrast (Minimum) | AA |
| 2 | Missing image alt text | 55.5% | 1.1.1 Non-text Content | A |
| 3 | Missing form input labels | 48.2% | 1.3.1 Info and Relationships | A |
| 4 | Empty links | 45.4% | 2.4.4 Link Purpose | A |
| 5 | Empty buttons | 29.6% | 4.1.2 Name, Role, Value | A |
| 6 | Missing document language | 15.8% | 3.1.1 Language of Page | A |

**All 6 of these are detectable via static code analysis.**

---

## 3. Level A vs. Level AA: Key Distinctions

### Level A (Minimum/Essential)
- **Baseline** accessibility: content is technically accessible but may be difficult to use
- Covers fundamental requirements: text alternatives, keyboard access, no traps, basic structure
- Without Level A, content is **effectively inaccessible** to many users
- Examples: alt text on images, keyboard operability, page titles, form labels

### Level AA (Standard/Recommended)
- **Recommended** conformance level for most organizations and legal requirements
- Adds **usability and quality** improvements beyond basic access
- Focuses on making content **comfortable** to use, not just technically possible
- Key additions over Level A:
  - **Color contrast minimums** (4.5:1 for text, 3:1 for large text and UI components)
  - **Visible focus indicators** for keyboard navigation
  - **Consistent navigation** and identification across pages
  - **Error suggestions** (not just error identification)
  - **Text reflow** at 320px width (responsive design)
  - **Text spacing** adjustability
  - **Orientation** flexibility
  - **Input purpose identification** via `autocomplete`
  - **Status messages** announced to assistive technology
  - **Hover/focus content** must be dismissible and persistent

### Legal Context
- **WCAG 2.1 AA** is the standard referenced by most accessibility laws (ADA, Section 508, EN 301 549, EAA)
- Level A alone is generally insufficient for legal compliance
- Level AAA is aspirational (not required for entire sites)

---

## 4. Common Code Patterns That Cause WCAG 2.1 AA Failures

### HTML Anti-Patterns

#### Missing or inadequate alt text (1.1.1)
```html
<!-- FAIL: No alt attribute -->
<img src="logo.png">

<!-- FAIL: Non-descriptive alt -->
<img src="chart.png" alt="image">
<img src="photo.jpg" alt="photo">

<!-- PASS -->
<img src="logo.png" alt="Acme Corporation logo">
<img src="decoration.png" alt="">  <!-- decorative: empty alt -->
```

#### Missing form labels (1.3.1, 3.3.2)
```html
<!-- FAIL: No label association -->
<input type="text" placeholder="Email">

<!-- FAIL: Placeholder as only label -->
<input type="email" placeholder="Enter your email">

<!-- PASS: Explicit label -->
<label for="email">Email</label>
<input type="email" id="email">

<!-- PASS: aria-label -->
<input type="search" aria-label="Search products">
```

#### Empty interactive elements (2.4.4, 4.1.2)
```html
<!-- FAIL: Empty link -->
<a href="/profile"><i class="icon-user"></i></a>

<!-- FAIL: Empty button -->
<button><svg>...</svg></button>

<!-- PASS -->
<a href="/profile" aria-label="User profile"><i class="icon-user"></i></a>
<button aria-label="Close dialog"><svg>...</svg></button>
```

#### Missing document language (3.1.1)
```html
<!-- FAIL -->
<html>

<!-- PASS -->
<html lang="en">
```

#### Heading hierarchy violations (1.3.1, 2.4.6)
```html
<!-- FAIL: Skipped heading level -->
<h1>Page Title</h1>
<h3>Subsection</h3>  <!-- skipped h2 -->

<!-- FAIL: Empty heading -->
<h2></h2>

<!-- FAIL: Multiple h1 -->
<h1>Main Title</h1>
<h1>Another Title</h1>

<!-- PASS -->
<h1>Page Title</h1>
<h2>Section</h2>
<h3>Subsection</h3>
```

#### Missing table semantics (1.3.1)
```html
<!-- FAIL: No header cells -->
<table>
  <tr><td>Name</td><td>Email</td></tr>
  <tr><td>John</td><td>john@example.com</td></tr>
</table>

<!-- PASS -->
<table>
  <caption>User Directory</caption>
  <thead>
    <tr><th scope="col">Name</th><th scope="col">Email</th></tr>
  </thead>
  <tbody>
    <tr><td>John</td><td>john@example.com</td></tr>
  </tbody>
</table>
```

#### Viewport zoom disabled (1.4.4)
```html
<!-- FAIL -->
<meta name="viewport" content="width=device-width, user-scalable=no">
<meta name="viewport" content="width=device-width, maximum-scale=1.0">

<!-- PASS -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

#### Missing autocomplete on user inputs (1.3.5)
```html
<!-- FAIL: Personal info input without autocomplete -->
<input type="text" name="fname">
<input type="email" name="email">

<!-- PASS -->
<input type="text" name="fname" autocomplete="given-name">
<input type="email" name="email" autocomplete="email">
```

#### Missing skip navigation (2.4.1)
```html
<!-- FAIL: No skip link or landmarks -->
<body>
  <div class="nav">...</div>
  <div class="content">...</div>
</body>

<!-- PASS -->
<body>
  <a href="#main" class="skip-link">Skip to main content</a>
  <nav>...</nav>
  <main id="main">...</main>
</body>
```

### CSS Anti-Patterns

#### Removing focus indicators (2.4.7)
```css
/* FAIL: Removes focus indicator with no replacement */
*:focus { outline: none; }
a:focus { outline: 0; }
button:focus { outline: none; }

/* PASS: Custom focus style */
*:focus { outline: none; }
*:focus-visible {
  outline: 2px solid #0066cc;
  outline-offset: 2px;
}
```

#### Insufficient color contrast (1.4.3)
```css
/* FAIL: Low contrast (approximately 2.5:1) */
.text { color: #999999; background-color: #ffffff; }

/* FAIL: Placeholder too low contrast */
::placeholder { color: #cccccc; }

/* PASS: Meets 4.5:1 */
.text { color: #595959; background-color: #ffffff; }
```

#### Fixed containers that break text spacing (1.4.12)
```css
/* FAIL: Fixed height + hidden overflow clips enlarged text */
.card-title {
  height: 48px;
  overflow: hidden;
  line-height: 1.2;
}

/* PASS: Use min-height or no height constraint */
.card-title {
  min-height: 48px;
  line-height: 1.2;
}
```

#### Orientation lock (1.3.4)
```css
/* FAIL */
@media (orientation: portrait) {
  body { transform: rotate(90deg); }
}

/* FAIL: In viewport meta */
<!-- orientation=portrait -->
```

#### Not respecting motion preferences (2.3.1)
```css
/* FAIL: No reduced motion alternative */
.hero { animation: slide-in 1s ease-in-out; }

/* PASS */
.hero { animation: slide-in 1s ease-in-out; }
@media (prefers-reduced-motion: reduce) {
  .hero { animation: none; }
}
```

### JavaScript / Component Anti-Patterns

#### Click handlers on non-interactive elements (2.1.1, 4.1.2)
```jsx
/* FAIL: div with click but no keyboard support or role */
<div onClick={handleClick}>Click me</div>

/* FAIL: span as button without role or keyboard */
<span onClick={toggle}>Toggle</span>

/* PASS: Use semantic elements */
<button onClick={handleClick}>Click me</button>

/* PASS: If div is required, add role + keyboard */
<div role="button" tabIndex={0} onClick={handleClick} onKeyDown={handleKeyDown}>
  Click me
</div>
```

#### Missing ARIA on dynamic content (4.1.3)
```jsx
/* FAIL: Status message not announced */
{error && <div className="error">{error}</div>}

/* PASS: Live region announces the message */
{error && <div role="alert" className="error">{error}</div>}

/* PASS: For non-urgent status */
<div role="status" aria-live="polite">{statusMessage}</div>
```

#### Incorrect ARIA usage (4.1.2)
```jsx
/* FAIL: aria-label on non-interactive/non-landmark div */
<div aria-label="Info section">...</div>

/* FAIL: Conflicting role and element */
<button role="link">Go to page</button>

/* FAIL: aria-hidden on focusable element */
<button aria-hidden="true">Hidden but focusable</button>

/* FAIL: Missing required ARIA properties */
<div role="checkbox">Accept terms</div>
/* Should have: aria-checked="false" */

/* PASS */
<div role="checkbox" aria-checked="false" tabIndex={0}>Accept terms</div>
```

#### Focus management failures (2.4.3, 2.4.7)
```jsx
/* FAIL: Modal doesn't trap focus */
function Modal({ isOpen, children }) {
  if (!isOpen) return null;
  return <div className="modal">{children}</div>;
}

/* FAIL: Positive tabindex */
<input tabIndex={5} />
<button tabIndex={3} />

/* PASS: Modal with focus trap */
function Modal({ isOpen, children, onClose }) {
  const modalRef = useRef();
  useEffect(() => {
    if (isOpen) modalRef.current?.focus();
  }, [isOpen]);
  return isOpen ? (
    <div role="dialog" aria-modal="true" ref={modalRef} tabIndex={-1}
         onKeyDown={(e) => e.key === 'Escape' && onClose()}>
      {children}
    </div>
  ) : null;
}
```

#### onChange causing navigation (3.2.2)
```jsx
/* FAIL: Select change causes immediate navigation */
<select onChange={(e) => window.location = e.target.value}>
  <option value="/page1">Page 1</option>
  <option value="/page2">Page 2</option>
</select>

/* PASS: Separate submit action */
<select value={selected} onChange={(e) => setSelected(e.target.value)}>
  <option value="/page1">Page 1</option>
  <option value="/page2">Page 2</option>
</select>
<button onClick={() => navigate(selected)}>Go</button>
```

### LWC-Specific Anti-Patterns

#### Missing component accessibility in templates
```html
<!-- FAIL: Icon-only button in LWC -->
<template>
  <lightning-button-icon icon-name="utility:close"></lightning-button-icon>
</template>

<!-- PASS: Include alternative-text -->
<template>
  <lightning-button-icon
    icon-name="utility:close"
    alternative-text="Close dialog">
  </lightning-button-icon>
</template>
```

#### Custom components missing ARIA
```html
<!-- FAIL: Custom dropdown without ARIA -->
<template>
  <div class="dropdown" onclick={toggleMenu}>
    <span>{selectedValue}</span>
    <ul if:true={isOpen}>
      <template for:each={options} for:item="opt">
        <li key={opt.id} onclick={selectOption}>{opt.label}</li>
      </template>
    </ul>
  </div>
</template>

<!-- PASS: With proper ARIA -->
<template>
  <div class="dropdown">
    <button aria-haspopup="listbox" aria-expanded={isOpenString} onclick={toggleMenu}>
      {selectedValue}
    </button>
    <ul role="listbox" if:true={isOpen} aria-label="Options">
      <template for:each={options} for:item="opt">
        <li key={opt.id} role="option" onclick={selectOption}
            onkeydown={handleKeyDown} tabindex="0">{opt.label}</li>
      </template>
    </ul>
  </div>
</template>
```

---

## 5. Static Analysis Detection Rules Summary

These are the highest-value checks an AI code auditor should perform, ranked by impact and detection reliability:

### Tier 1: High Impact, High Confidence (Always Flag)

1. **Missing `alt` on `<img>`** - 1.1.1
2. **Missing `<label>` or `aria-label` on form inputs** - 1.3.1, 3.3.2
3. **Empty links** (no text content or `aria-label`) - 2.4.4
4. **Empty buttons** (no text content or `aria-label`) - 4.1.2
5. **Missing `lang` on `<html>`** - 3.1.1
6. **`outline: none`/`outline: 0` without replacement focus style** - 2.4.7
7. **`user-scalable=no` or `maximum-scale=1`** in viewport meta - 1.4.4
8. **Click handlers on `<div>`/`<span>` without `role` and keyboard handler** - 2.1.1, 4.1.2
9. **Missing `<title>` element** - 2.4.2
10. **Heading level skips** (h1 to h3, etc.) - 1.3.1

### Tier 2: High Impact, Moderate Confidence

11. **Low color contrast** (requires parsing CSS values) - 1.4.3
12. **Missing `autocomplete` on personal data inputs** - 1.3.5
13. **Missing skip navigation link or landmark regions** - 2.4.1
14. **Positive `tabindex` values** (> 0) - 2.4.3
15. **`aria-hidden="true"` on focusable elements** - 4.1.2
16. **Missing `role="alert"` or `aria-live` on dynamic error/status messages** - 4.1.3
17. **Tables without `<th>` or `scope` attributes** - 1.3.1
18. **Images with non-descriptive alt** ("image", "photo", "icon", etc.) - 1.1.1
19. **`<video>`/`<audio>` without `<track>`** - 1.2.2
20. **Fixed height + `overflow: hidden` on text containers** - 1.4.12

### Tier 3: Moderate Impact, Requires Context

21. **`onChange` on `<select>` triggering navigation** - 3.2.2
22. **`onFocus` handlers causing context changes** - 3.2.1
23. **CSS `animation` without `prefers-reduced-motion` media query** - 2.3.1
24. **Modal dialogs without `role="dialog"` and `aria-modal`** - 4.1.2
25. **Custom widgets (tabs, accordions, menus) missing required ARIA roles/states** - 4.1.2
26. **Missing `role="presentation"` or `alt=""` on decorative images** - 1.1.1
27. **Generic link text** ("click here", "read more", "learn more") without context - 2.4.4
28. **`<marquee>`, `<blink>` elements or CSS equivalents** - 2.2.2, 2.3.1
29. **`autoplay` on `<video>`/`<audio>` elements** - 1.4.2
30. **Missing `<caption>` on data tables** - 1.3.1

---

## 6. Required ARIA Role Properties (for Completeness Checks)

When custom widgets use ARIA roles, certain properties are **required**:

| Role | Required Properties |
|------|-------------------|
| `checkbox` | `aria-checked` |
| `combobox` | `aria-expanded`, `aria-controls` |
| `gridcell` | (must be within `row` within `grid`) |
| `menuitemcheckbox` | `aria-checked` |
| `menuitemradio` | `aria-checked` |
| `option` | (must be within `listbox`) |
| `radio` | `aria-checked` |
| `scrollbar` | `aria-controls`, `aria-valuenow`, `aria-valuemax`, `aria-valuemin`, `aria-orientation` |
| `slider` | `aria-valuenow`, `aria-valuemax`, `aria-valuemin` |
| `switch` | `aria-checked` |
| `tab` | (must be within `tablist`) |
| `tabpanel` | `aria-labelledby` (recommended) |
| `treeitem` | (must be within `tree` or `group` within `tree`) |

---

## 7. WCAG 2.1 vs 2.0: New Criteria (for Reference)

WCAG 2.1 added 17 new success criteria beyond 2.0. The following are Level A or AA additions:

- **1.3.4** Orientation (AA)
- **1.3.5** Identify Input Purpose (AA)
- **1.4.10** Reflow (AA)
- **1.4.11** Non-text Contrast (AA)
- **1.4.12** Text Spacing (AA)
- **1.4.13** Content on Hover or Focus (AA)
- **2.1.4** Character Key Shortcuts (A)
- **2.5.1** Pointer Gestures (A)
- **2.5.2** Pointer Cancellation (A)
- **2.5.3** Label in Name (A)
- **2.5.4** Motion Actuation (A)
