<!-- Source: https://docs.google.com/presentation/d/1oWuMrwlamlTBedNsUbBj-q6Xn4Ie1Y4_2Zou8VdE7eQ/edit?slide=id.g38e250adfd8_16_539#slide=id.g38e250adfd8_16_539 -->
<!-- Last synced: 2026-03-31 -->

# Data 360 Simplicity Scale — Assessment Criteria

## L1 Express

**Theme:** Speed and confidence with very few options.

**User POV:** My use case is straightforward. The system should handle this for me.

**Product criteria:** Minimum understanding needed to achieve goal. Simple tasks should start here.

**Design rules:**
- Single primary action
- 0-3 input fields maximum
- Smart defaults do the heavy lifting
- Clear success state with outcome preview
- Seamless path to L2 if defaults don't fit

**Appropriate when:**
- Task is common, low-risk, low-variability
- User wants immediate results without configuration
- The "happy path" covers 80%+ of use cases

---

## L2 Progressive Reveal

**Theme:** Progressive reveal of options supported by recommendations.

**User POV:** My use case requires some options. The system should help me through this.

**Product criteria:** Most common options/configurations surfaced progressively based on user's goals.

**Design rules:**
- System recommendations with ability to adjust
- Progressive disclosure (collapsible sections, expandable panels)
- "Preset + Customize" model
- Options appear in context, not all at once
- Preview/impact of choices shown before committing

**Appropriate when:**
- Task has moderate complexity requiring decisions
- Users benefit from guided choices with recommendations
- Options exist but shouldn't overwhelm upfront
- Context determines which controls to show

---

## L3 Full Control

**Theme:** Every option for every use case.

**User POV:** I want this done my way but don't make me work for it. The system is here to support my needs.

**Product criteria:** Power users get every option with guidance and guardrails for efficiency. Note: this is not the cluttered experience of today — even full control should have guardrails and smart defaults.

**Design rules:**
- Full control available but still intuitive (NOT today's cluttered experience)
- Guided empty states, tooltips, inline help even at full control
- Inline validation and warnings to prevent errors
- Users can return to L1/L2 recommendations at any time

**Appropriate when:**
- Task is highly specialized, sensitive, or nuanced
- Power users need access to edge-case configurations
- Risk or compliance requires explicit control over all parameters

---

## Critical Constraints

**Not all jobs fit all levels.** Some workflows are too sensitive or nuanced for L1 or L2. That's expected.

**All levels must be intuitive.** Even L3 must meet foundational usability heuristics. Complexity in a feature doesn't justify poor usability.

**ONE path that evolves.** Never create separate "Simple" and "Advanced" modes. Design one path that starts simple (L1) and can evolve (L2/L3) as the user's needs grow. Users should move seamlessly between levels.

**Smart vs. Agentic are separate concepts:**
- **Smart Experience**: AI-recommended actions, default configs, auto-applied standards. No chat required.
- **Agentic Experience**: Chat interface for open-ended tasks/questions. Can be available at ANY level.

---

## Common Mistakes

1. **Exposing all options upfront** — Instead of hiding behind smart defaults
2. **Creating separate simple/advanced modes** — Instead of one evolving path
3. **Revealing more fields in L2 without guidance** — Missing recommendations or context
4. **L3 with no guardrails** — Missing validation, help, or warnings
5. **Confusing Smart with Agentic** — Smart = auto-applied (no chat), Agentic = chat-based assistance
6. **Skipping L1** — When 80%+ of users share the same goal, start simple

---

## Assessment Guidelines

- **When evaluating:** Determine the level the design or implementation currently targets, then assess whether that level is appropriate for the use case and user goals.

- **Consider task characteristics:** Common + low-risk = L1, moderate complexity = L2, specialized/sensitive = L3.

- **Check for seamless transitions:** Users should be able to move between levels without context loss or mode switching.
