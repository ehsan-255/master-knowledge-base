--- START OF FILE APMDD v2.1 - Modeling Types, Strategy & Notations.md ---
# APMDD v2.1 - Modeling Types, Strategy & Notations
#apmdd-modeling #apmdd-documentation #apmdd-architect-focus

> **For a comprehensive guide to specific visual models recommended within APMDD, including those for strategic architect-focused planning and detailed AI consumption, refer to [[APMDD v2.1 - Part 4A - Strategic & Detailed Visual Modeling]].**

In APMDD v2.1, models are the Human Architect's primary instruments for strategic thinking, architectural design, precise communication, and effective governance. This document details the role of models, the mandated modeling languages and tools, types of models used per lifecycle phase, and the overall modeling strategy designed to empower the architect while guiding the AI.

## 4.1. Modeling in APMDD v2.1
Modeling is a central pillar of APMDD v2.1. Models serve a dual, critical purpose:
1.  **For the Human Architect:** Tools for exploring design alternatives, making strategic architectural decisions (especially regarding HMA decomposition), defining precise contracts, and maintaining a coherent vision of the system.
2.  **For the AI Team:** The primary medium for receiving unambiguous specifications, understanding context, and guiding implementation, testing, and documentation efforts.
All models are considered first-class documentation artifacts and are maintained as part of the [[APMDD v2.1 - Part 8 - Glossary#Single Source of Truth (SSoT)|Single Source of Truth]], ensuring consistency for all participants.

## 4.2. Types of Models
APMDD v2.1 mandates several model types, each serving a specific purpose in the lifecycle:

- **Computation Independent Model (CIM):** Business/domain models, use case diagrams, conceptual overviews. (See [[APMDD v2.1 - Part 8 - Glossary#Computation Independent Model (CIM)]], and [[APMDD v2.1 - Part 4A - Strategic & Detailed Visual Modeling#2. Requirements & Domain Understanding (CIM Phase)]])
- **Platform Independent Model (PIM):** HMA structure, plugin decomposition, logical interfaces. (See [[APMDD v2.1 - Part 8 - Glossary#Platform Independent Model (PIM)]], [[APMDD v2.1 - Part 5 - Architectural Mandate - HMA v1.3]], and [[APMDD v2.1 - Part 4A - Strategic & Detailed Visual Modeling#3. HMA Structural Design (PIM Phase)]])
- **Platform Specific Model (PSM):** Technology-specific refinements, deployment diagrams, concrete API/interface definitions. (See [[APMDD v2.1 - Part 8 - Glossary#Platform Specific Model (PSM)]], and [[APMDD v2.1 - Part 4A - Strategic & Detailed Visual Modeling#5. Platform-Specific & Deployment (PSM/Deployment Phase)]])

## 4.3. Mandated Modeling Notations & Tools
**C4-DSL (Structurizr ecosystem) is the mandatory primary notation and tooling for defining the system's C4 architectural model (Levels 1-4: Context, Containers, Components, Code).**
- The C4-DSL model is the authoritative source for architectural structure. Diagrams are generated as views from this model.
- This approach enables model-first, diagrams-as-views, and SSoT benefits, and is well-suited for AI parsing and version control.

**PlantUML is retained as a mandated complementary tool** for behavioral diagrams (Sequence, Activity, State) and other non-C4 structural diagrams (Use Case, ERDs, DFDs). These can be embedded and linked to C4 model elements using Structurizr's capabilities.

## 4.4. Modeling Strategy
- **Just-Enough, Just-in-Time Modeling:** Only model what is needed for the current phase/iteration, focusing on the plugin/component under development.
- **Persistent, Versioned Models:** All models are stored, versioned, and maintained as part of the documentation set.
- **Architect-Led, AI-Assisted:** The architect leads modeling, with the AI team assisting in drafting, updating, and interpreting models.
- **Model-Driven Implementation:** Models directly inform code and test generation by the AI team.

## 4.5. Modeling Best Practices
- Use clear, unambiguous names and structures.
- Link models to relevant documentation sections using Obsidian links (e.g., [[APMDD v2.1 - Part 2 - Core Principles, Concepts & Roles]]).
- Reference glossary terms on first use (see [[APMDD v2.1 - Part 8 - Glossary]]).
- For detailed model guidance, see [[APMDD v2.1 - Part 4A - Strategic & Detailed Visual Modeling]].
- Maintain model consistency with code and documentation (see [[APMDD v2.1 - Part 6 - Documentation Strategy]]).

## 4.6. Example: HMA Plugin Modeling
- Define each Plugin as a C4 Component within a C4 Container in the C4-DSL model. (See [[APMDD v2.1 - Part 4A - Strategic & Detailed Visual Modeling#3.1. HMA Component Diagram (incorporating C4 Level 2/3)]])
- Specify Ports and Events explicitly as part of the C4 model, with behavioral details modeled in PlantUML as needed.
- Use sequence diagrams (PlantUML) to show interactions between plugins and the HMA core, linked to C4 model elements.
- Link each model to its corresponding documentation and code artifacts.

## 4.7. Summary
Modeling in APMDD v2.1 is rigorous, persistent, and central to the methodology, ensuring clarity, consistency, and effective human-AI collaboration.

## 4.8. Model Types Categorized per Phase (as Deliverables)
| Phase | Primary Model Types (C4-DSL/Structurizr & PlantUML) | Purpose |
| :--- | :--- | :--- |
| **Phase 0: System Conception & HMA Blueprinting** | Initial HMA Structure Sketch (C4 Context/Container), High-Level Use Cases (PlantUML) | Define overall architectural approach (HMA), initial decomposition into Core/Plugins, core capabilities, and initial project scope. |
| **Phase 1: CIM Development** | Use Case Diagrams (PlantUML), Activity Diagrams (PlantUML), Conceptual Domain Model (PlantUML) | Understand the problem domain, user needs, business processes, and high-level system interactions from a technology-agnostic viewpoint. |
| **Phase 2: PIM Development** | C4 Container/Component Diagrams (generated from C4-DSL), Port/Event Specifications (C4-DSL), Sequence Diagrams (PlantUML), State Diagrams (PlantUML) | Define the technology-agnostic structure, precise interfaces, interactions, and behavior of all HMA components. |
| **Phase 3: PSM & Code Development** | C4 Deployment Diagrams (generated from C4-DSL), Detailed Plugin Internal Design (PlantUML if complex), Sequence Diagrams (PlantUML) | Guide the AI team in implementing Plugin internals, refine interactions based on chosen technologies. |
| **Phase 4 & 5: Deployment, Operation & Evolution** | Deployment Diagrams (C4-DSL), Updated C4/PlantUML models reflecting changes | Document the current deployed system state, guide ongoing maintenance, troubleshooting, and evolution of HMA Plugins. |

## 4.9. Other Model Types (Available as Needed)
While C4-DSL and PlantUML cover the primary modeling needs, other specialized model types or notations may be employed as needed for specific analytical or design tasks, especially within a Plugin's L4 infrastructure or for complex internal logic. These are supplementary and should be clearly referenced from the primary C4-DSL or PlantUML models or documentation.

## 4.10. Model Repository & Version Control
To ensure models are managed effectively as part of the SSoT, rigorous version control is mandatory.

*   **Mandated Tool:** **Git** is the mandated version control system for all model artifacts, particularly `.dsl` files for Structurizr/C4-DSL models and `.puml` files for PlantUML diagrams.
*   **Rationale:**
    *   C4-DSL and PlantUML files are text-based, making them ideally suited for Git's diffing and merging capabilities.
    *   Git provides robust version history, branching, and collaboration features essential for managing evolving models.
    *   Consistency with code version control practices.
*   **Repository Structure:** Models should be organized within the Git repository in a logical structure, potentially mirroring the HMA component structure or lifecycle phases.
*   **Commit Practices:** Clear commit messages describing changes to models are essential for traceability.
*   **Traceability:** Model versions should be traceable to requirements, design decisions, and corresponding code versions.

By treating models as version-controlled assets, APMDD ensures their integrity and supports the iterative and collaborative nature of the methodology.

--- END OF FILE APMDD v2.1 - Modeling Types, Strategy & Notations.md ---