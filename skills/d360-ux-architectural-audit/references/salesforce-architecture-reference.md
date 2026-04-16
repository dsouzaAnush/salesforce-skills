# Salesforce Architecture Reference

Source: Norledge `Salesforce_Architecture_Reference`

---

## PART 1: SLDS 2.0 DESIGN PRINCIPLES

SLDS 2 (introduced in Spring '25) is a decoupled, styling-hook-based architecture designed to support both human and agentic interfaces.

- **Simplicity:** Prioritize clear, intuitive design and streamlined workflows to reduce friction and cognitive load.
- **Clarity:** Use the **Salesforce Cosmos** theme for high-contrast, scannable layouts with circular patterns, improved typography, and consistent iconography.
- **Adaptability:** A modular architecture built to flex across teams and platforms, supporting future innovations like Dark Mode and dynamic AI-generated UIs.
- **Decoupled Architecture:** Structure is separated from visual style using **Global Styling Hooks** (CSS Custom Properties). This allows for deep branding and theming without breaking core component logic.
- **Progressive Disclosure:** Information should be shown only when relevant. Use popovers, expandable sections, and hover states to provide "Evidence" (grounding) for AI insights without cluttering the primary view.
- **Efficiency:** Shift from custom blueprints to **Out-of-the-Box Base Components** to ensure future-proofing and AI-readiness.

---

## PART 2: AGENTIC EXPERIENCE LAYER (AXL) PATTERNS

AXL defines how agents operate within the Salesforce ecosystem, moving from request-response interactions to autonomous goal-seeking.

### Agent Maturity Scale

| Level | Name | Description |
|-------|------|-------------|
| L1 | Conversational | Reactive, request-response agents (Digital Front Doors) |
| L2 | Proactive | Event-driven agents triggered by data changes or specific conditions (Observers) |
| L3 | Ambient | Background agents that automate "work about work" without explicit prompts |
| L4 | Autonomous | Goal-oriented agents capable of independent planning and reasoning (Digital Employees) |
| L5 | Collaborative/Swarms | Specialized agents working together under an Orchestrator to solve complex, multi-domain problems |

### Agent Development Lifecycle (ADLC)

1. **Ideate & Plan:** Define Purpose, Persona, and specific Goals.
2. **Build:** Use Agent Builder (low-code) or pro-code tools to define Actions and Knowledge.
3. **Test:** Validate via Agent Simulator (manual) or Testing Center (automated) to ensure accuracy and minimize hallucinations.
4. **Deploy:** Package using Agentforce DX or Change Sets.
5. **Monitor & Tune:** Continuous observation of the "outer loop" to refine agent reasoning and instructions.

---

## PART 3: DATA 360 (D360) GROUNDING

All AI and Agentic interactions must be grounded in the **Data Cloud** layer to ensure trust and accuracy.

- **Unified Profile:** The "Golden Record" providing a 360-degree view of the customer.
- **Calculated Insights:** Real-time metrics (e.g., Churn Risk, LTV) used to trigger agents or inform UI components.
- **Atlas Reasoning Engine:** The "brain" that connects D360 data to agent actions, allowing the agent to adapt based on real-time context.
