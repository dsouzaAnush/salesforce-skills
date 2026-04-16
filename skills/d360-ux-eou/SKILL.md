---
name: d360-ux-eou
description: Use when evaluating UI/UX against Data 360 ease-of-use principles. Supports Figma designs, planning documents or ideas, and code. Triggers on 'ease of use', 'eou', 'simplicity', 'principles', 'L1', 'L2', 'L3', 'figma', 'plan', or 'idea'.
user-invocable: true
---

# Data 360 Ease of Use Evaluator

Evaluate **Figma designs**, **planning documents/ideas**, or **code** against the **Data 360 Experience Principles** (6 prioritized principles) and **Simplicity Scale** (L1/L2/L3). Produce an actionable report with copy-paste prompts for each issue. Report only — no automatic fixes.

---

## Usage

**Evaluate Figma design:**
```
/d360-ux-eou figma
/d360-ux-eou https://figma.com/file/abc123
```

**Evaluate planning document:**
```
/d360-ux-eou PLAN.md
/d360-ux-eou Can you check if my idea follows the principles?
```

**Evaluate code (specific feature):**
```
/d360-ux-eou identity resolution wizard
/d360-ux-eou src/components/dataMapping/
```

**Evaluate code (full project):**
```
/d360-ux-eou
```

**Cancel evaluation:**
- Respond with "cancel", "nevermind", "skip", or "no thanks" at any prompt

---

## When to Use

**Use this skill when:**
- Evaluating Figma designs before coding starts
- Checking if a feature idea or plan follows EOU principles
- Evaluating any Data 360 UI code for ease-of-use
- Assessing whether a design follows the prioritized experience principles
- Identifying the correct simplicity level (L1/L2/L3) for a feature
- Reviewing work at any stage: concept, planning, design, prototyping, production
- Any discipline: designers, developers, PMs, architects

**Do NOT use this skill for:**
- Salesforce architecture audits (Apex vs Flow, AXL maturity) — use `d360-ux-architectural-audit` instead
- SLDS compliance checks — separate skill
- Accessibility (WCAG) audits — use `d360-ux-a11y-audit` skill
- Performance or security reviews — separate concerns

---

## Evaluation Process

### Step 0: Determine Evaluation Mode

The skill supports three modes based on what artifact you're evaluating:

**Decision logic:**

1. **Check for Figma indicators** (case-insensitive):
   - User message or arguments contain "figma"
   - Arguments contain a Figma URL (figma.com/file/)
   - → Go to **FIGMA MODE**

2. **Check for Planning indicators**:
   - Arguments point to a planning file (PLAN.md, requirements.md, PRD.md, design-doc.md)
   - Message contains: "idea", "plan", "concept", "before we build"
   - → Go to **PLANNING MODE**

3. **Default to CODE MODE**:
   - Arguments specify feature name or file path → scope to that
   - No arguments → evaluate full project

4. **Unclear**:
   - Ask user: "What would you like me to evaluate? (Figma design / Feature idea or plan / Existing code)"
   - Check for cancellation keywords in response

**Cancellation handling:** At any clarifying question, if user responds with "cancel", "nevermind", "never mind", "skip", "exit", or "no thanks", gracefully exit:
```
Evaluation cancelled. Let me know if you'd like to run /d360-ux-eou later!
```

---

## Shared Evaluation Guidance

**The following guidance applies to all evaluation modes (Figma, Planning, Code).**

### Loading Reference Material

Before evaluating, read the evaluation criteria:
- `references/experience-principles.md` — The 6 principles in priority order with evaluation questions
- `references/simplicity-scale.md` — L1/L2/L3 levels with assessment criteria

### P2 Evaluation Nuance — When Technical Language is Appropriate

When evaluating **P2 (Lead with outcomes, abstract the system)**, distinguish between violations and appropriate technical language:

**Flag as P2 violation (system language leak):**
- ✅ Technical terms in L1/default UI (e.g., "Sync Entities" button on simple dashboard)
- ✅ Backend/API concepts in user-facing labels (e.g., "POST Request Status" instead of "Upload Progress")
- ✅ Implementation details users can't control (e.g., "Database Index" in UI settings)
- ✅ Error messages using system codes without context (e.g., "Error 500" with no explanation)

**Technical language is appropriate (NOT a P2 violation):**
- ⛔ L2/L3 advanced features where users need system understanding to make informed choices
- ⛔ Progressive disclosure contexts (e.g., "Advanced: Configure API Endpoint" revealed under "Show Advanced")
- ⛔ Technical configuration UI explicitly for experts (e.g., API settings, webhook config, developer tools)
- ⛔ Learning moments with clear "Learn more" paths that teach system concepts progressively

**Ask yourself before flagging P2:**
- Does hiding this term make L2/L3 users less effective at their task?
- Is this in a progressively disclosed area (not default view)?
- Would a power user need to understand this system concept to use the feature correctly?

### Including Anti-Pattern Names in Findings

When describing principle violations, include the anti-pattern name if applicable:
- P1 violations often relate to: **Total Exposure** or **Oversimplification**
- P2 violations often relate to: **System-language leak**
- P3 violations often relate to: **Point-of-no-return**
- P4 violations often relate to: **Unexplained "advanced"**
- P5 violations often relate to: **Inconsistent patterns**
- P6 violations often relate to: **Small Data design** or **Manual Overhead**

**Example finding format:**
> **Issue 1 (Total Exposure pattern):** All settings visible at once instead of progressive disclosure...

---

## FIGMA MODE

**When:** User mentions "figma" or provides Figma URL

### Step 1: Check Figma MCP Availability

Before proceeding, verify Figma MCP server is available:
- Check if Figma MCP tools exist (look for tools with `figma` in the name)
- If **NOT available**:
  ```
  **Figma MCP is not currently available.** To evaluate Figma designs, you need to enable the Figma MCP server.

  To set up Figma MCP, see the official documentation: https://developers.figma.com/docs/figma-mcp-server/
  
  Alternatively:
  - If you have a detailed feature description or plan, use Planning Mode instead: describe your design and I'll evaluate the concept
  - If you've already implemented code, use Code Mode: /d360-ux-eou [feature name]
  ```
  - Exit gracefully - user needs to set up MCP first

### Step 2: Fetch Figma Design Data (when MCP available)

**If Figma URL provided:**
- Extract node ID from URL (convert "node-id=1-2" to "1:2" format)
- Use Figma MCP to fetch file/frame data:
  - Try `get_design_context` with the node ID
  - Try `get_screenshot` for visual reference
  - Try `get_metadata` if design context is too large

**If no URL (user said "figma" only):**
- Try Figma MCP's "get selected frames" capability (pass empty/no node ID)
- If no frames selected: "Please select frames in Figma or provide a Figma URL"

**Handle MCP Failures:**

If MCP tools timeout or fail (even though MCP is installed), provide clear troubleshooting:

```
**Unable to fetch Figma design data.** The Figma MCP server is installed but couldn't retrieve the design.

**Troubleshooting steps:**

1. **Ensure Figma Desktop is running** - The Figma Desktop app must be open
2. **Open the file in Figma** - Navigate to the file/frame in the Figma Desktop app
3. **Check your connection** - Figma MCP requires an active connection to Figma's servers
4. **Try refreshing** - Close and reopen the Figma file, then try again

**Alternative options:**

- **Share a screenshot:** Upload a screenshot of your design and I'll evaluate based on the visual
- **Describe your design:** Tell me about the UI elements, flows, and interactions - I'll evaluate using Planning Mode
- **Evaluate after implementation:** If you've already built the feature, use Code Mode: /d360-ux-eou [feature name]

Would you like to try one of the alternatives, or troubleshoot the Figma connection?
```

Check for cancellation keywords in user response. If user wants to proceed with alternatives, switch modes accordingly.

**Successfully fetched data - Extract:**
- Frame structure and hierarchy
- Layer names and organization
- Text content and labels
- Component usage
- Visual grouping and spacing
- Interactive elements (buttons, inputs, dropdowns)

### Step 3: Load Reference Material

See "Shared Evaluation Guidance" section above for reference materials.

### Step 4: Evaluate Design Against Principles

**Critical: Evidence-Based Evaluation Only**

**Scope Your Evaluation to What's Shown:**
- ✅ **Evaluate**: Design decisions visible in these frames (what IS shown)
- ✅ **Evaluate**: Whether shown elements follow the principles
- ❌ **Don't evaluate**: Features not shown in these frames (out of scope)
- ❌ **Don't evaluate**: Complete feature requirements (you're seeing a slice, not the whole product)

**Before flagging something as a problem:**

1. **"This feature is missing X"** → STOP. Is X shown anywhere in these frames?
   - No → It's out of scope. Don't flag it.
   - Yes → Proceed with evaluation.

2. **"This panel is always/persistently visible"** → STOP. Do these frames show multiple states?
   - No (only one state) → Don't claim "always" or "persistent"
   - Yes (multiple states shown) → Okay to comment on visibility patterns

3. **"This violates P3 (no undo/edit)"** → STOP. Is undo/edit functionality shown in ANY frame?
   - No → Out of scope. Principle doesn't apply to features not shown.
   - Yes → Evaluate how well the shown undo/edit works.

**Apply principles ONLY to what's visible:**
- If citations are shown but edit isn't → evaluate the citations design, not the missing edit feature
- If one workflow state is shown → evaluate that state, not other states you imagine
- If a panel appears in these frames → evaluate its design, not whether it should always be visible

**When evaluating Figma designs:**
- **Cite specific visual evidence**: "The button at [frame/layer name] shows X"
- **Use human-readable names**: Reference frames/sections/layers by their names (e.g., "the builder panel titled 'All Sources'"), NOT by node IDs (e.g., "node 4942:259927"). Node IDs are not useful to Figma users who can't easily navigate to them.
- **Flag uncertainty about out-of-scope features**: Designs may show one state of many. Say "No error state shown" rather than "Design lacks error handling"
- **Don't assume features**: Only evaluate what's visibly present in the frames
- **Don't invent workflows**: If a flow isn't shown, note "Not visible in current frames"
- **Verify visual details**: Before claiming an element lacks something (icon, color, etc.), double-check the screenshot/layer data

**Red flags - STOP if you catch yourself:**
- Saying "should have [feature]" when that feature isn't shown anywhere
- Using words like "always," "persistent," "never" when only seeing one state
- Describing features not shown in the frames
- Assuming workflows or states not designed yet
- Claiming elements lack details you didn't verify visually
- Applying principles to features not visible in the design

**Assess visual design patterns (for features shown in these frames):**
- **P1 - Simple by default, power on demand**: Is complexity hidden or exposed? Are defaults smart? Is progressive disclosure used?
- **P2 - Lead with outcomes, abstract the system**: Do labels focus on user outcomes or system concepts? See "P2 Evaluation Nuance" in Shared Evaluation Guidance
- **P3 - Predictable paths, easy pivots**: Are actions reversible? Can users preview impact? Clear navigation?
- **P4 - Obvious by design**: Are CTAs clear? Is information hierarchy obvious? Do labels self-explain?
- **P5 - Learn once, use everywhere**: Does design follow SLDS or established patterns?
- **P6 - Good at any scale**: Does design handle empty states, errors, 100+ items?

**Identify Simplicity Level (L1/L2/L3):**
- What level does this design target?
- Is it appropriate for the use case?
- Should it start simpler?

**Include anti-pattern names in findings** — See "Shared Evaluation Guidance" for pattern names and example format.

### Step 5: Produce Figma Report

Use the output format (see Output Format section), but:
- Reference Figma frames/layers instead of code files
- Include screenshots or frame links if possible
- Prompts should reference design changes (colors, layout, labels)

**Save to:** `docs/d360-ux-eou/figma_{frame-name}_{YYYY-MM-DD_HH-MM}.md`

---

## PLANNING MODE

**When:** User provides planning file, or message contains "idea", "plan", "concept", "before we build"

### Step 1: Identify What to Evaluate

**If planning file specified** (e.g., `/d360-ux-eou PLAN.md`):
- Read that specific file

**If conversational idea** (no file specified):
- Use conversation context: user's recent messages describing the feature
- Extract the feature description from their message

### Step 2: Load Reference Material

See "Shared Evaluation Guidance" section above for reference materials.

### Step 3: Extract Key Aspects from Plan/Idea

From the planning document or conversational description, identify:
- **User goal/outcome**: What are users trying to accomplish?
- **Controls/options exposed**: What choices are users given?
- **Interaction flow**: How do users progress through the task?
- **Target complexity level**: Does it aim for L1, L2, or L3?
- **Missing considerations**: What's not mentioned that should be?

### Step 4: Evaluate Plan Against Principles

For each principle, check if the plan/idea addresses EOU concerns:

- **P1**: Does plan specify simple defaults with opt-in complexity?
- **P2**: Does plan use outcome language or system language? See "P2 Evaluation Nuance" in Shared Evaluation Guidance (apply to planned UI, not current implementation)
- **P3**: Does plan describe clear paths, pivots, preview/undo?
- **P4**: Does plan specify obviousness criteria (labels, CTAs, error states)?
- **P5**: Does plan reference existing patterns or create new ones?
- **P6**: Does plan consider scale (empty states, 100+ items, bulk operations)?

**Identify missing EOU considerations:**
- What should be addressed in the plan before implementation?
- Where might the implementation go wrong without guidance?

**Include anti-pattern names in findings** — See "Shared Evaluation Guidance" for pattern names and example format.

### Step 5: Produce Planning Report

Use the output format (see Output Format section), but:
- Reference sections/features in the plan document
- Recommendations should shape the plan/spec itself
- Prompts should suggest additions to the planning document

**Save to:** `docs/d360-ux-eou/plan_{plan-name}_{YYYY-MM-DD_HH-MM}.md`

---

## CODE MODE

**When:** Code exists and no Figma/planning indicators, OR user explicitly requests code evaluation

### Step 1: Determine Scope

Check if the user specified a feature/component to evaluate via `$ARGUMENTS`:
- **If feature/path specified** (e.g., "identity resolution wizard" or "src/components/dataMapping/"): Focus evaluation on that specific feature, component, or file path
- **If no arguments:** Ask the user:
  - "Would you like to evaluate the entire project or a specific feature/component?"
  - If they choose specific feature: "Which feature or component would you like me to evaluate?"
  - Check for cancellation keywords
  - Use their response to scope the evaluation accordingly

### Step 2: Understand the Code (or Feature)

Read the codebase in the **current working directory** (not the skills repo). Identify:
- What the feature/code does (user goal)
- UI components, flows, and interaction patterns
- Technology stack (LWC, React, Aura, etc.)

Use Glob, Grep, and Read to explore. Focus on UI-facing code: components, templates, pages, configuration.

**Important:** You are evaluating the user's code repo, not the `data360-ux-skills` repo. If a specific feature was requested, limit your search to that feature's files.

### Step 3: Load Reference Material

See "Shared Evaluation Guidance" section above for reference materials.

### Step 4: Identify Simplicity Level

Determine which level (L1 Express, L2 Progressive Reveal, L3 Full Control) the code implements. Assess whether this is appropriate for the use case.

Consider:
- What level does the implementation achieve?
- Is this the right level for the task's complexity and user needs?
- Should it start simpler (L1) and grow to L2/L3?

### Step 5: Evaluate Code Against Principles (Priority Order)

Evaluate in order (P1 is highest priority). For each principle, identify specific issues in the code with file paths and line references. Higher-priority violations are more critical.

**The 6 principles (in priority order):**
1. Simple by default, power on demand
2. Lead with outcomes, abstract the system (see "P2 Evaluation Nuance" in Shared Evaluation Guidance)
3. Predictable paths, easy pivots
4. Obvious by design
5. Learn once, use everywhere
6. Good at any scale

**Include anti-pattern names in findings** — See "Shared Evaluation Guidance" for pattern names and example format.

For each principle, cite specific examples from the code. If no issues found, note "No issues identified" briefly.

### Step 6: Produce Code Report

Use the output format below. Do NOT fix anything — report only.

**After generating the evaluation:**
1. Save the output to a markdown file in the user's repository at: `docs/d360-ux-eou/{component-name}_{YYYY-MM-DD_HH-MM}.md`
2. Extract the component/page name from the evaluation scope:
   - Single component/feature: use component name (remove "page-" prefix if present)
   - Full project: use "full-project"
3. Use the current date/time for the timestamp
4. Ensure the directory exists (create it if needed)
5. Never overwrite existing files — each evaluation gets a unique timestamp
6. Present the file path to the user after saving

---

## Output Format

**The evaluation must be saved to a file with this header:**

**Important:** Provide actionable findings with specific examples, NOT pass/fail scores or grades.

```markdown
# Data 360 Ease of Use Evaluation — {Component/Feature Name or "Full Project" or "Figma: Frame Name" or "Plan: Feature Name"}

**Date:** YYYY-MM-DD HH:MM

**Scope:** `{file path to component or "Full Project Evaluation" or "Figma: URL" or "Plan: PLAN.md"}`

**Mode:** [Figma / Planning / Code]

**Skill:** d360-ux-eou

---

## Simplicity Level Assessment

**Current level:** [L1 Express / L2 Progressive Reveal / L3 Full Control]

**Appropriate for this use case:** [Yes / No + brief rationale]

[If mismatched, explain what level would be more appropriate and why]

---

## Experience Principles Evaluation

### [P1] Simple by default, power on demand

**Issue 1 (Total Exposure pattern):** [Specific finding with file/component/frame reference]

**Suggestion:** [Actionable recommendation]

**Prompt to address:**
```
[Copy-paste prompt the user can give to Claude to fix this issue. Make it specific with references to what to change.]
```

**Issue 2:** [If additional issues found for this principle - include anti-pattern name if applicable]

**Suggestion:** [Actionable recommendation]

**Prompt to address:**
```
[Copy-paste prompt for this specific issue]
```

[Continue with additional issues for this principle, or note "No additional issues" if principle has no issues]

[Repeat this format for each principle P2-P6. For principles with no issues, include a brief line: "**[PX] Principle Name:** No issues identified."]

---

## Summary

- **Critical issues (P1-P2):** [count]
- **Other issues (P3-P6):** [count]
- **Top recommendation:** [Single most impactful change to improve ease of use]

---

## ⚠️ Important: Human Review Required

**This evaluation was performed by an AI assistant and may contain:**
- Misinterpretations of visual design elements
- Assumptions about features not explicitly shown
- Missing context about user workflows or business requirements

**Before acting on these findings:**
- ✅ Verify each issue against the actual design/code
- ✅ Consider whether suggested changes align with your product strategy
- ✅ Prioritize based on your team's understanding of user needs
- ✅ Use your judgment - not all flagged issues may apply to your context

This evaluation is a starting point for discussion, not a definitive assessment.

---

**Feedback on the Experience Principles?** Share your thoughts in #feedback-eou-principles
```

---

## Scope Boundaries

- This skill evaluates **ONLY** against Data 360 Experience Principles and Simplicity Scale
- SLDS compliance, accessibility (WCAG), performance, and security are **separate concerns** for separate skills
- **Do not fix code/designs** — report only with copy-paste prompts

---

## Known Limitations

- **Figma MCP timeouts with complex designs**: Very large or complex Figma frames may cause MCP timeouts. If this happens, try evaluating smaller sections of the design or use Planning Mode with screenshots instead.
- **Non-deterministic evaluation results**: Running the same evaluation multiple times (in any mode) may yield different findings due to differences in agent session context and interpretation. This is inherent to LLM-based evaluation. Always review findings with your own judgment.
- **Over-aggressive P2 (system language) assessments**: The skill may flag standard business terminology as "technical" or "system language" when evaluating P2 (Lead with outcomes, abstract the system). For example, terms like "Account" (in B2B contexts), "Dashboard", or "Report" are widely understood domain terms, not technical jargon requiring abstraction. When reviewing P2 findings, distinguish between: (1) true system leaks (API terms, database concepts, implementation details) vs. (2) standard business terminology appropriate for the user audience. Not all domain-specific language violates P2.
