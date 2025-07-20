---
id: apmdd_methodology
type: APMDD_Concept
label: AI-Powered Model-Driven Development (APMDD) v2.0
keywords: [methodology, architect-led, ai development, model-driven, hma, ssoT]
summary: An architect-led methodology for guiding AI teams in software development, using models, HMA, and comprehensive documentation to ensure quality, governability, and effective human-AI collaboration.
relationships:
  - type: mandatesArchitecture
    target_id: hma_architecture_v1_3
  - type: definesLifecycle
    target_id: apmdd_lifecycle
  - type: emphasizesRole
    target_id: apmdd_human_architect
  - type: utilizesTool
    target_id: apmdd_plantuml
  - type: reliesOnPrinciple
    target_id: apmdd_ssoT
---
**Disclaimer:** This document serves as a high-level introductory guide to APMDD v2.0. While it aims to provide a comprehensive overview of the main principles, ideas, and background, the complete and definitive Single Source of Truth (SSoT) resides in the detailed `Part X` documents of the APMDD v2.0 specification. For specific implementation details, normative rules, and exhaustive explanations, please refer to the main documentation set.

## AI-Powered Model-Driven Development (APMDD) v2.0

**Definition:** APMDD v2.0 is a comprehensive methodology designed for software development projects where AI agents serve as the primary development team, strategically guided and governed by a Human Architect. It aims to address challenges like AI context drift and communication gaps while empowering the architect.

**Core Purpose:** To provide a structured, model-centric lifecycle that enables effective human-AI collaboration, leveraging AI speed while ensuring governability, maintainability, and architectural efficacy for complex systems.

**Key Problems Solved:**
*   AI Context Drift & Loss of Focus
*   Human-AI Communication & Comprehension Gaps
*   Lack of Long-Term AI Memory & Adherence to Decisions
*   Managing System-Wide Complexity
*   Balancing Rigidity and Adaptability

**Core Guiding Principles:**
*   **Architect-Led, AI-Powered:** Human Architect leads vision, design, and validation; AI team executes and assists.
*   **HMA as Mandatory Architectural Backbone:** [[APMDD v2.0 - Part 5 - Architectural Mandate - HMA v1.3|Hexagonal Microkernel Architecture (HMA)]] is non-negotiable for modularity and context management.
*   **Models as Primary Communication & Specification:** [[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations|Formal architectural models (defined with C4-DSL) and complementary behavioral diagrams (e.g., using PlantUML)]] are key for precise architect-AI communication.
*   **Single Source of Truth (SSoT):** [[APMDD v2.0 - Part 8 - Glossary#Single Source of Truth (SSoT)]]
*   **Iterative Lifecycle:** [[APMDD v2.0 - Part 3 - Lifecycle - Integrating MDA and Agile Practices|MDA-influenced macro-phases (CIM, PIM, PSM) with embedded agile loops]].
*   **Continuous, Living, DITA-Inspired Documentation:** Documentation (in Obsidian) is an integral, evolving artifact.
*   **AI as Active Collaborators:** AI assists in design, research, modeling, testing, and documentation.
*   **Automated Governance & HMA Compliance:** Tooling enforces standards and HMA rules.
*   **Clarity & Precision for AI Comprehension:** All artifacts for AI must be unambiguous.

---
id: apmdd_human_architect
type: APMDD_Role
label: Human Architect (APMDD)
keywords: [architect, lead, design, governance, validation, hma]
summary: The central human leadership role in APMDD, responsible for vision, architectural design (HMA), modeling, governance, and validation of AI-generated work.
relationships:
  - type: leadsMethodology
    target_id: apmdd_methodology
  - type: designsUsing
    target_id: hma_architecture_v1_3
  - type: createsModelsWith
    target_id: apmdd_plantuml
  - type: guidesTeam
    target_id: apmdd_ai_team
---
## Human Architect (APMDD Role)

**Definition:** The lead human role in APMDD, responsible for the overall system vision, architectural design (specifically [[APMDD v2.0 - Part 5 - Architectural Mandate - HMA v1.3|HMA]]), modeling leadership, governance, complexity management, AI team guidance, and ultimate validation of all work.

**Key Responsibilities:**
*   Defining system vision, strategy, and non-functional requirements.
*   Designing the HMA structure, ensuring its integrity.
*   Leading the creation and maintenance of the [[apmdd_c4_dsl_model|C4-DSL architectural model]] and [[apmdd_plantuml_behavioral_models|complementary behavioral/visual artifacts (using tools like PlantUML)]], as detailed in `[[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]]`.
*   Enforcing adherence to architectural standards and APMDD principles.
*   Validating all AI-generated work (code, tests, documentation, models).
*   Decomposing work, assigning tasks, and providing ongoing direction to the [[apmdd_ai_team|AI Team]].
*   Acting as the primary technical interface with stakeholders.

---
id: apmdd_ai_team
type: APMDD_Role
label: AI Team / Agents (APMDD)
keywords: [ai, agents, implementation, testing, documentation, modeling assistance]
summary: The collective of AI agents and workflows in APMDD responsible for development tasks like implementation, testing, documentation, and modeling assistance, under architect guidance.
relationships:
  - type: guidedBy
    target_id: apmdd_human_architect
  - type: implementsArchitecture
    target_id: hma_architecture_v1_3
  - type: consumesModels
    target_id: apmdd_plantuml_models
---
## AI Team / Agents (APMDD Role)

**Definition:** The collective of AI agents, LLM-based workflows, and autonomous systems responsible for performing development tasks within APMDD, functioning as active collaborators under the Human Architect's guidance.

**Key Responsibilities:**
*   **Implementation:** Developing HMA Plugins based on architect's models and specifications.
*   **Testing:** Performing Test-Driven Development (TDD), writing unit, integration, and contract tests.
*   **Documentation & Artifact Generation:** Generating and updating technical documentation, code comments.
*   **Modeling Assistance:** Assisting the architect in refining models (e.g., drafting PlantUML).
*   **Design & Research Assistance:** Conducting research and assisting in design exploration as directed.

---
id: apmdd_lifecycle
type: APMDD_Concept
label: APMDD Lifecycle
keywords: [lifecycle, cim, pim, psm, agile, mda]
summary: A hybrid lifecycle combining MDA-influenced macro-phases (CIM, PIM, PSM) for structure with embedded agile loops for iterative development and flexibility.
relationships:
  - type: partOfMethodology
    target_id: apmdd_methodology
  - type: hasPhase
    target_ids: [apmdd_cim_phase, apmdd_pim_phase, apmdd_psm_phase, apmdd_deployment_phase]
  - type: incorporates
    target_id: apmdd_agile_activities
---
## APMDD Lifecycle

**Definition:** APMDD employs a hybrid lifecycle combining structured macro-phases influenced by Model-Driven Architecture (MDA) with embedded agile loops for iterative development and rapid feedback.

**Overall Lifecycle Phases (MDA Influence):**
1.  **Phase 0: System Conception & HMA Blueprinting:** Architect-led strategic planning and initial HMA structural sketching.
2.  **[[apmdd_cim_phase|Phase 1: Computation Independent Model (CIM) Development]]:** Focus on business/domain requirements, technology-agnostic. Produces Use Case Diagrams, Conceptual Domain Models, Activity Diagrams (business process).
3.  **[[apmdd_pim_phase|Phase 2: Platform Independent Model (PIM) Development]]:** Defines the HMA structure, Plugin decomposition, Port interfaces, and Event schemas in a technology-agnostic way. Produces HMA Component Diagrams, Port/Event Definitions, Sequence Diagrams.
4.  **[[apmdd_psm_phase|Phase 3: Platform Specific Model (PSM) & Code Development]]:** Refines PIM with technology specifics; AI team implements HMA Plugins. Produces detailed Plugin designs, code, tests.
5.  **Phase 4 & 5: Deployment, Operation & Evolution:** Deploying, monitoring, and evolving the HMA system. Produces Deployment Diagrams, updated models.

**Iterative Activities Embedded Within Each Phase (Agile Influence):**
*   Envisioning, Sprint Modeling, Model Storming, Test-Driven Development (TDD), Reviews.

---
id: apmdd_modeling_approach
type: APMDD_Concept
label: APMDD Modeling Approach
keywords: [c4-dsl, structurizr, plantuml, architectural models, behavioral models, modeling, specification, architect tool]
summary: APMDD uses C4-DSL/Structurizr for primary architectural modeling, with PlantUML as a complementary tool for behavioral and other diagrams, all detailed in Part 4.
relationships:
  - type: usedInMethodology
    target_id: apmdd_methodology
  - type: notationStandard
    target_ids: [apmdd_c4_dsl, apmdd_plantuml]
  - type: componentOf
    target_id: apmdd_ssoT_concept
---
## APMDD Modeling Approach

**Definition:** In APMDD v2.1, models are primary instruments for the Human Architect and the AI Team. A 'model-first' approach is used for architecture, where the C4-DSL model is the authoritative source, and diagrams are views.

**Mandated Notations & Tools:** (See `[[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]]` for full details)
*   **Architectural Modeling:** C4-DSL with Structurizr (Primary).
*   **Behavioral & Other Non-C4 Structural Modeling:** PlantUML (Complementary).

**Role per Lifecycle Phase:**
*   **CIM:** Use Case Diagrams, Conceptual Domain Models, Activity Diagrams (business process).
*   **PIM:** Detailed HMA Component Diagrams, Port & Event Definitions (Class Diagrams), Package Diagrams, Sequence Diagrams, State Machine Diagrams.
*   **PSM:** Detailed Plugin internal designs, technology-specific Sequence Diagrams.
*   **Deployment:** Deployment Diagrams.

**Modeling Strategy:** Just-enough, just-in-time modeling; persistent, versioned models; architect-led, AI-assisted; model-driven implementation.

---
id: apmdd_ssoT_concept
type: APMDD_Principle_Concept
label: Single Source of Truth (SSoT - APMDD)
keywords: [ssoT, models, documentation, code, consistency, external memory]
summary: The SSoT in APMDD comprises Models + Documentation + Code, ensuring a unified, authoritative, and consistent reference for human architects and AI teams.
relationships:
  - type: corePrincipleOf
    target_id: apmdd_methodology
  - type: includes
    target_ids: [apmdd_plantuml_models, apmdd_documentation, apmdd_code]
---
## Single Source of Truth (SSoT - APMDD)

**Definition:** A core principle in APMDD ensuring that critical information is authoritatively defined and maintained in one place to minimize ambiguity and ensure consistency for all participants (human and AI).

**Components of APMDD SSoT:**
1.  **Models (C4-DSL for architecture, PlantUML for behavior, etc.):** The formal C4-DSL architectural model and complementary behavioral/visual diagrams. (See `[[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]]`).
2.  **Documentation (Obsidian, DITA-inspired):** Textual explanations, specifications (Port contracts, Event schemas), design rationale, user guides.
3.  **Code:** AI-generated source code implementing the designs.

**Purpose:** Provides a reliable "external memory," reduces context drift for AI, facilitates governance, and ensures all team members work from the same understanding. All SSoT components are version-controlled (Git).

---
id: apmdd_documentation
type: APMDD_Artifact_Concept
label: APMDD Documentation Strategy
keywords: [documentation, obsidian, dita, living document, ai-readable]
summary: Documentation in APMDD is a continuous, living, DITA-inspired artifact managed in Obsidian, forming part of the SSoT and crucial for AI context.
relationships:
  - type: partOfMethodology
    target_id: apmdd_methodology
  - type: componentOf
    target_id: apmdd_ssoT_concept
  - type: tooling
    target_id: apmdd_obsidian
---
## APMDD Documentation Strategy

**Philosophy:** Documentation is a first-class, mandatory, and living artifact, created and consumed throughout the lifecycle. It must be structured, clear, precise, and accessible to both humans and AI.

**Tooling & Principles:**
*   **Obsidian:** Mandatory tool for creating and managing documentation.
*   **DITA-Inspired Principles:** Topic-based authoring, semantic markup, content reuse (via linking/transclusion), information typing.

**Key Characteristics:**
*   **AI-Readable:** Unambiguous language, explicit links, consistent structure.
*   **Continuous & Living:** Updated in parallel with models and code.
*   **Version Controlled:** Managed in Git alongside models and code.
*   **Part of SSoT:** Ensures consistency with models and code.

---
*This Fact Sheet provides a structured overview of key APMDD v2.0 concepts. More entries could be added for specific principles, roles, or artifacts as needed.*

## Modeling in APMDD v2.1
Modeling is a central activity in APMDD v2.1, serving as the primary means for the architect to communicate structure, behavior, and requirements to the AI team. For details on modeling notations and strategy, see [[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]].