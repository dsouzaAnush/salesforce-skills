<!-- Source: https://docs.google.com/presentation/d/1cQCPANXQ7jfX5AJ9kOXRingF4mRvFsl2L9EvLGjDFzE/edit?slide=id.g2f42db121f4_2_482#slide=id.g2f42db121f4_2_482 -->
<!-- Last synced: 2026-03-31 -->

# Data 360 Experience Principles — Evaluation Rubric

Principles listed in priority order. When principles conflict, higher priority wins.

---

## P1: Simple by default, power on demand

**Definition:** Less to decide upfront, more control when needed.

**Decision tests:**
- "Where does this setting go?" — If it isn't required for the 80% use case to succeed, it shouldn't be visible by default. Reveal only when the user engages with a specific related sub-task.
- "Should we offer a 'Basic' and 'Advanced' mode?" — No. The system should intelligently "grow" with the user's specific workflow, not force a binary choice.
- "How do we handle Power Users?" — Don't build a separate UI. Ensure their "power tools" are one logical step away from the standard flow.

**Red flags:**
- All settings visible by default
- Binary "Basic" vs "Advanced" mode toggle
- Separate power-user UI instead of progressive complexity
- Dead ends for complex tasks after oversimplification
- Every toggle upfront "so users have control"

---

## P2: Lead with outcomes, abstract the system

**Definition:** Design for user outcomes, not technical implementation.

**Decision tests:**
- "What do we call this field?" — If the backend calls it `API_Trigger_v2` but the user thinks of it as "Start Schedule," we use "Start Schedule."
- "Should we show the processing status of each microservice?" — No. The user wants to know if their data is ready to use, not which specific server is handling the load.
- "Does the user need to know about the underlying object model?" — Only if it directly impacts their business logic. Otherwise, keep the focus on the workflow.

**Red flags:**
- Backend-derived naming exposed in UI (API_Trigger_v2 instead of "Start Schedule")
- Processing status showing microservice or infrastructure details
- Object model or database schema exposed when unnecessary for business logic
- Field names that map directly to API property names

---

## P3: Predictable paths, easy pivots

**Definition:** Transparent results and seamless revision or reversal.

**Decision tests:**
- "How do we handle destructive actions?" — Show a clear preview of the impact (e.g., "This will update 50k records") and provide a clear "Back" or "Undo" path.
- "Can the user change their mind mid-workflow?" — Yes. Navigation should allow users to jump back to previous steps to tweak logic without losing their progress.

**Red flags:**
- Destructive actions without impact preview ("This will update 50k records")
- Linear wizards with no back navigation
- Loss of progress when changing earlier steps
- No clear "Back" or "Undo" path after making a change

---

## P4: Obvious by design

**Definition:** Eliminate guesswork. If it needs explaining, it needs rethinking.

**Decision tests:**
- "How would the customer know?" — Ask this at every decision point. If a user understands the concept but still struggles with the UI, the design has failed.
- **The "Post-Documentation" Test** — If a user reads a help article about "Identity Resolution" and returns to the app, is the "Identity Resolution" tab the most prominent thing they see? If they have to hunt for the feature they just read about, the information architecture is broken.
- **"Advanced" is not an excuse for unexplained** — Complexity in a feature doesn't justify ambiguity in the UI. Even a "Power User" shouldn't have to guess what a toggle does or when it is appropriate to use.

**Red flags:**
- Controls whose purpose requires reading documentation to understand
- Features hidden in unexpected locations (if user reads help about "Identity Resolution" but can't find the tab)
- Ambiguous icons or labels without accompanying text
- "Advanced" used as an excuse for unexplained UI

---

## P5: Learn once, use everywhere

**Definition:** Familiarity shouldn't reset with every new workflow.

Consistency is the foundation of user proficiency. We prioritize the Salesforce Lightning Design System (SLDS) and shared component libraries as our default to ensure Data 360 feels like a native part of the broader ecosystem.

**Decision tests:**
- "Which component should I use?" — Start with the standard design system. If you innovate beyond it, ensure the new pattern is used consistently across all modules, not just one.
- "Does this custom pattern solve a unique problem?" — If a standard component is functionally sufficient, the burden of proof is on the team wanting to build something custom. Innovation is allowed when solving domain-specific problems the standard design system wasn't built for, but it must be intentional and documented.

**Red flags:**
- Bespoke UI patterns for a single feature without documented rationale
- Inconsistent interaction patterns between modules
- Custom components where standard design system equivalents exist and are functional
- "Lone Ranger" pattern — modern/custom UI just for one feature
- Re-learning cost for a pattern that doesn't solve a unique domain-specific problem

---

## P6: Good at any scale

**Definition:** Simplicity must persist as data, users, and complexity grow.

**Decision tests:**
- "Is this screen too crowded?" — Design for the "full" state first. A screen that feels busy with 5 items will be paralyzed when an enterprise adds 5,000.
- "How do we handle long-running tasks?" — Don't just show a spinner. Provide progress transparency and "fire-and-forget" workflows so users stay productive while the system works in the background.
- "Does this work with 10,000 items?" — If a dropdown or list breaks at high item counts, it isn't "Good at any scale."

**Red flags:**
- Dropdowns or lists that break at high item counts
- Manual repetitive tasks without bulk alternatives (requiring users to do the same thing 100 times)
- Spinners without progress indicators for long operations
- UI designed only for "small data" demo state (5 items looks fine, 5,000 is paralyzed)
- Layouts that feel busy with 5 items and become unusable with 5,000

---

## Common Anti-Patterns to Check

When evaluating a design, check for these red flags:

- [ ] **Total Exposure** — All options visible at once instead of progressive disclosure
- [ ] **Oversimplification** — Necessary utility stripped away, creating dead ends for complex tasks
- [ ] **System-language leak** — API names, internal jargon, or backend concepts exposed in UI
- [ ] **Point-of-no-return** — Destructive actions without preview or undo path
- [ ] **Unexplained "advanced"** — Complexity used as excuse for ambiguous UI
- [ ] **Inconsistent patterns** — Custom UI where standard components would suffice
- [ ] **Small Data design** — UI that breaks at enterprise scale (10,000+ items)
- [ ] **Manual Overhead** — Repetitive tasks without bulk operations or automation
