--- START OF FILE APMDD v2.1 - Lifecycle: Integrating MDA and Agile Practices.md ---
# APMDD v2.1 - Lifecycle: Integrating MDA and Agile Practices
#apmdd-lifecycle-phase #apmdd-agile-activity

## 3.1. Overall Lifecycle Phases (MDA Influence)
APMDD v2.1 adopts a macro-lifecycle structure inspired by [[APMDD v2.1 - Part 8 - Glossary#Model-Driven Architecture (MDA)|Model-Driven Architecture (MDA)]], organizing development into three primary phases:

1. **Computation Independent Model (CIM):**
   - Focuses on business/domain requirements, goals, and context, independent of technical implementation. (See [[APMDD v2.1 - Part 8 - Glossary#Computation Independent Model (CIM)]])
2. **Platform Independent Model (PIM):**
   - Defines the system's structure and behavior in a technology-agnostic way, with a strong emphasis on [[APMDD v2.1 - Part 5 - Architectural Mandate - HMA v1.3|HMA]] structure and [[APMDD v2.1 - Part 8 - Glossary#Plugin|Plugin]] decomposition. (See [[APMDD v2.1 - Part 8 - Glossary#Platform Independent Model (PIM)]])
3. **Platform Specific Model (PSM):**
   - Refines the PIM with details of specific implementation technologies and platforms. (See [[APMDD v2.1 - Part 8 - Glossary#Platform Specific Model (PSM)]])

Each phase produces models and documentation that become part of the [[APMDD v2.1 - Part 8 - Glossary#Single Source of Truth (SSoT)|Single Source of Truth]].

For detailed guidance on the specific visual models and modeling notations used in each phase, see [[APMDD v2.1 - Part 4A - Strategic & Detailed Visual Modeling]] and [[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]].

## 3.2. Iterative Activities Embedded Within Each Phase (Agile Influence)
Within each macro-phase, APMDD embeds agile loops to enable iterative, adaptive development. Key activities include:

- **Envisioning:** Collaborative sessions (architect, stakeholders, AI team) to clarify goals, requirements, and high-level models (especially CIM).
- **Sprint Modeling:** Short, focused modeling sessions to define or refine models for the current iteration (PIM/PSM focus).
- **Model Storming:** Rapid, just-in-time modeling to address emerging questions or design needs.
- **Test-Driven Development (TDD):** Writing tests before code, especially within [[APMDD v2.1 - Part 8 - Glossary#Plugin|Plugin]] boundaries. (See [[APMDD v2.1 - Part 8 - Glossary#Test-Driven Development (TDD)]])
- **Reviews:** Regular review cycles for models, code, and documentation, led by the architect.

This hybrid approach ensures both structure and flexibility, allowing the team to adapt to change while maintaining architectural integrity.

## 3.3. Lifecycle Artifacts and SSoT
Artifacts produced during the lifecycle include:
- Models (CIM, PIM, PSM) using the mandated modeling notations (see [[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]])
- Documentation (DITA-inspired, modular, managed in Obsidian)
- Code (generated/implemented by the AI team)
- Tests (TDD-driven)

All artifacts are maintained as part of the [[APMDD v2.1 - Part 8 - Glossary#Single Source of Truth (SSoT)|Single Source of Truth]].

## 3.4. HMA Integration in the Lifecycle
The [[APMDD v2.1 - Part 5 - Architectural Mandate - HMA v1.3|Hexagonal Microkernel Architecture (HMA) Specification v1.3]] is integrated throughout the lifecycle:
- **PIM Phase:** HMA structure and [[APMDD v2.1 - Part 8 - Glossary#Plugin|Plugin]] boundaries are defined.
- **PSM Phase:** Platform-specific details for each [[APMDD v2.1 - Part 8 - Glossary#Plugin|Plugin]] and [[APMDD v2.1 - Part 8 - Glossary#Port|Port]] are specified.
- **Implementation:** AI team develops each [[APMDD v2.1 - Part 8 - Glossary#Plugin|Plugin]] as an independent, testable unit, adhering to HMA rules.

## 3.5. Governance, Quality, and Testing in the Lifecycle
Governance and quality assurance are embedded in every phase:
- Automated checks for HMA compliance (see [[APMDD v2.1 - Part 7 - Governance, Quality & Testing#7.4. Automated Governance & Enforcement|Automated Governance & Enforcement]]).
- Test-driven development and review cycles (see [[APMDD v2.1 - Part 7 - Governance, Quality & Testing#7.3. Testing Strategy: Simplicity, Reliability, and AI-Driven Execution|Testing Strategy]]).
- Continuous documentation updates (see [[APMDD v2.1 - Part 6 - Documentation Strategy]]).

## 3.6. Summary
APMDD v2.1's lifecycle combines the rigor of MDA with the adaptability of agile, enforced by HMA structure and continuous governance, to enable effective, scalable AI-led development.

--- END OF FILE APMDD v2.1 - Lifecycle: Integrating MDA and Agile Practices.md ---
