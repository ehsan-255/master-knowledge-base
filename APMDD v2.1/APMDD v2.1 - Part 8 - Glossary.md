--- START OF FILE APMDD v2.1 - Glossary.md ---
# APMDD v2.1 - Glossary
#apmdd-glossary

## 8.1. Glossary Overview
This glossary defines key terms used throughout APMDD v2.1. For detailed explanations and context, see the relevant documentation sections (e.g., [[APMDD v2.1 - Part 2 - Core Principles, Concepts & Roles]], [[APMDD v2.1 - Part 5 - Architectural Mandate - HMA v1.3]]).

## 8.2. Terms
#apmdd-glossary
- **AI-Powered Model-Driven Development (APMDD):** See [[APMDD v2.1 - Part 2 - Core Principles, Concepts & Roles#2.2. Core Concepts & Definitions]].
- **AI Team:** See [[APMDD v2.1 - Part 2 - Core Principles, Concepts & Roles#2.2. Core Concepts & Definitions]].
- **Architect (Human):** See [[APMDD v2.1 - Part 2 - Core Principles, Concepts & Roles#2.2. Core Concepts & Definitions]].
- **Computation Independent Model (CIM):** See [[APMDD v2.1 - Part 3 - Lifecycle - Integrating MDA and Agile Practices#3.1. Overall Lifecycle Phases (MDA Influence)]].
- **Context Drift:** See [[APMDD v2.1 - Part 1 - Master Guide & Introduction#1.1. The APMDD Paradigm: Solving Challenges in AI-Led Development]].
- **Hexagonal Microkernel Architecture (HMA):** See [[APMDD v2.1 - Part 5 - Architectural Mandate - HMA v1.3]].
- **Model:** An abstraction representing aspects of a system. In APMDD v2.1, this primarily refers to the C4-DSL architectural model and complementary behavioral/visual diagrams created with tools like PlantUML. (See [[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]]).
- **Model Transformation (APMDD Context):** See [[APMDD v2.1 - Part 2 - Core Principles, Concepts & Roles#2.2. Core Concepts & Definitions]].
- **Orchestrator Plugin:** See [[APMDD v2.1 - Part 5 - Architectural Mandate - HMA v1.3#5.3. HMA Structure]].
- **Platform Independent Model (PIM):** A model describing the system's structure and behavior without specifying implementation technologies. In APMDD v2.1, the PIM for architectural structure is primarily realized as the C4-DSL model. (See [[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]]).
- **Platform Specific Model (PSM):** A model that refines a PIM by incorporating technology-specific details. In APMDD v2.1, PSMs may include C4-DSL deployment views and technology-specific complementary diagrams (e.g., using PlantUML). (See [[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]]).
- **PlantUML:** A mandated complementary modeling language in APMDD v2.1 for behavioral diagrams (e.g., Sequence, Activity, State) and other non-C4 structural diagrams (e.g., Use Case, ERDs, DFDs). These diagrams are often embedded within or linked to the primary C4 architectural model. For full details on its role, see [[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]].
- **Plugin (HMA Context):** See [[APMDD v2.1 - Part 5 - Architectural Mandate - HMA v1.3#5.3. HMA Structure]].
- **Port (HMA Context):** See [[APMDD v2.1 - Part 5 - Architectural Mandate - HMA v1.3#5.3. HMA Structure]].
- **Single Source of Truth (SSoT):** See [[APMDD v2.1 - Part 6 - Documentation Strategy#6.2. Single Source of Truth: Models + Documentation + Code]].
- **Test-Driven Development (TDD):** See [[APMDD v2.1 - Part 3 - Lifecycle - Integrating MDA and Agile Practices#3.2. Iterative Activities Embedded Within Each Phase (Agile Influence)]].
- **Wardley Map (APMDD Context):** A strategic model used by the Architect for value chain analysis and component evolution assessment, informing HMA design. (See [[APMDD v2.1 - Part 4A - Strategic & Detailed Visual Modeling#1.1. Wardley Map]]).
- **C4-Model:** A lean approach to visualizing software architecture at different levels of abstraction (Context, Containers, Components, Code). In APMDD v2.1, the C4 model is defined using C4-DSL. (See [[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]]).
- **C4-DSL:** A domain-specific language provided by Structurizr for defining a C4 software architecture model as text. Mandated in APMDD v2.1 as the primary tool for defining the architectural model. (See [[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]]).
- **Structurizr:** A collection of tools (including C4-DSL) for creating software architecture diagrams and documentation based on the C4 model, using a 'model-first, diagrams as views' approach. Mandated in APMDD v2.1 as the primary ecosystem for architectural modeling. (See [[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]]).
- **HMA Component Diagram:** The master blueprint for HMA structure (Core, Plugins, Ports), defining decomposition for AI context management. (See [[APMDD v2.1 - Part 4A - Strategic & Detailed Visual Modeling#3.1. HMA Component Diagram (incorporating C4 Level 2/3)]]).
- **HMA Port & Event Definitions:** Precise contracts for HMA Ports and Event schemas, critical for AI implementation. (See [[APMDD v2.1 - Part 4A - Strategic & Detailed Visual Modeling#3.2. HMA Port & Event Definitions (using Class Diagram)]]).
- **Package Diagram (APMDD Context):** Organizes HMA components and artifacts into logical groups for complexity management. (See [[APMDD v2.1 - Part 4A - Strategic & Detailed Visual Modeling#3.3. Package Diagram]]).
- **Sequence Diagram (APMDD Context):** Illustrates message sequences between HMA components for specific scenarios. (See [[APMDD v2.1 - Part 4A - Strategic & Detailed Visual Modeling#4.1. Sequence Diagram]]).
- **State Machine Diagram (APMDD Context):** Models HMA Plugin lifecycle and complex entity behavior. (See [[APMDD v2.1 - Part 4A - Strategic & Detailed Visual Modeling#4.2. State Machine Diagram]]).
- **Data Flow Diagram (DFD) (APMDD Context):** Visualizes the movement and transformation of data, especially for complex event-driven choreographies. (See [[APMDD v2.1 - Part 4A - Strategic & Detailed Visual Modeling#7.1. Data Flow Diagram (DFD) for Complex Event Choreography or Data Pipelines]]).

## 8.3. Tagging Strategy
#apmdd-tagging
- #apmdd-principle: Principles and guiding rules
- #apmdd-concept: Core concepts and definitions
- #apmdd-role: Roles and responsibilities
- #apmdd-lifecycle-phase: Lifecycle phases and activities
- #apmdd-modeling: Modeling strategy and notations
- #apmdd-hma-alignment: HMA structure and compliance
- #apmdd-documentation: Documentation strategy and SSoT
- #apmdd-governance: Governance and quality
- #apmdd-testing: Testing and observability
- #apmdd-ssot: Single Source of Truth
- #apmdd-glossary: Glossary terms and definitions
- #apmdd-architect-focus: Architect empowerment, architect-led activities, and architect-focused modeling guidance

## 8.4. Summary
#apmdd-glossary
This glossary is a central reference for all APMDD v2.1 documentation. For further details, see the linked sections above.

A
---
*   **A2A (Agent-to-Agent Protocol)** <!-- #apmdd-glossary-term -->
    *   Definition: An external open standard protocol (e.g., from Google) intended for inter-AI agent communication.
    *   APMDD Context: [[Hexagonal Microkernel Architecture (HMA) Specification v1.2|HMA]] [[APMDD v2.1 - Glossary#Adapter|Adapters]] implementing [[APMDD v2.1 - Glossary#Port|Ports]] for interacting with *external* AI agents **SHOULD** consider A2A. Direct [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugin]]-to-[[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugin]] synchronous communication **MAY** use A2A via specific [[APMDD v2.1 - Glossary#Adapter|Adapters]] if unavoidable, but [[APMDD v2.1 - Glossary#Event-Driven Architecture (EDA)|EDA]] is preferred. (Ref: HMA Spec v1.2, Sec 2.5)
*   **Adapter (HMA Context)** <!-- #apmdd-glossary-term #apmdd-hma-concept -->
    *   Definition: A component that implements a [[APMDD v2.1 - Glossary#Port (HMA Context)|Port]], bridging the abstract interface defined by the [[APMDD v2.1 - Glossary#Port (HMA Context)|Port]] to concrete technology, protocols, or external systems.
    *   APMDD Context: Essential in [[Hexagonal Microkernel Architecture (HMA) Specification v1.2|HMA]] for decoupling application/business logic from infrastructure concerns. Includes [[APMDD v2.1 - Glossary#Driving Adapter|Driving Adapters]] (handling incoming requests) and [[APMDD v2.1 - Glossary#Driven Adapter|Driven Adapters]] (handling outgoing interactions). (Ref: HMA Spec v1.2, Sec 2.2)
*   **Agile Model-Driven Development (AMDD)** <!-- #apmdd-glossary-term -->
    *   Definition: A software development methodology that combines principles from agile development and model-driven development, emphasizing iterative modeling, just-enough detail, and close collaboration.
    *   APMDD Context: APMDD draws inspiration from AMDD for its iterative activities within macro-phases and its philosophy of creating "just-enough, just-in-time" [[APMDD v2.1 - Glossary#Model|models]]. (Ref: [[APMDD v2.1 - Master Guide & Introduction#1.4. Relationship to MDD, AMDD, and MDA|APMDD Introduction]])
*   **AI First Approach** <!-- #apmdd-glossary-term #apmdd-principle -->
    *   Definition: A guiding principle in APMDD where the [[APMDD v2.1 - Glossary#AI Team|AI team]] is considered an active collaborator throughout the development lifecycle, not just a passive code generator.
    *   APMDD Context: Involves leveraging AI capabilities for design assistance, research, [[APMDD v2.1 - Glossary#Model|model refinement]], test generation, documentation drafting, and QA, in addition to implementation, always under [[APMDD v2.1 - Glossary#Architect (Human)|architect]] guidance. (Ref: [[APMDD v2.1 - Core Principles, Concepts & Roles#2.1. Guiding Principles of APMDD v2.1|APMDD Principles]])
*   **Architectural Event Bus** <!-- #apmdd-glossary-term #apmdd-hma-concept -->
    *   Definition: A dedicated event stream within the [[Hexagonal Microkernel Architecture (HMA) Specification v1.2|HMA]] for publishing domain-level architecture events (e.g., [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugin]] lifecycle changes, policy violations, significant architectural state changes). Versioned as `hma.architecture.telemetry.v1`.
    *   APMDD Context: Enables real-time architectural monitoring, automated governance, and dynamic system adaptation. (Ref: HMA Spec v1.2, Sec 6.3, 10)

C
---
*   **Computation Independent Model (CIM)** <!-- #apmdd-glossary-term #apmdd-lifecycle-phase #apmdd-modeling -->
    *   Definition: A high-level model in [[APMDD v2.1 - Glossary#Model-Driven Architecture (MDA)|MDA]] and APMDD that focuses on the requirements, environment, and business context of a system, without detailing its structure or implementation technology. It answers "what" the system should do and "why."
    *   APMDD Context: The first major modeling phase in the APMDD lifecycle, involving stakeholders to define scope and high-level functionality. (Ref: [[APMDD v2.1 - Lifecycle: Integrating MDA and Agile Practices#3.1. Overall Lifecycle Phases (MDA Influence)|APMDD Lifecycle]])
*   **Context Drift** <!-- #apmdd-glossary-term -->
    *   Definition: The tendency for Large Language Models (LLMs) or AI agents to lose track of the overall goals, constraints, history, or specific details of a task or conversation, especially over long interactions or within large, complex codebases.
    *   APMDD Context: A primary challenge APMDD aims to mitigate through its structural (HMA) and documentation strategies. (Ref: [[APMDD v2.1 - Master Guide & Introduction#1.1. The APMDD Paradigm: Solving Challenges in AI-Led Development|APMDD Introduction]])
*   **Control Plane Services (HMA Context)** <!-- #apmdd-glossary-term #apmdd-hma-concept -->
    *   Definition: Core-provided, non-domain-specific services within the [[Hexagonal Microkernel Architecture (HMA) Specification v1.2|HMA]] L2 layer, essential for governance and operational support of [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugins]].
    *   APMDD Context: Examples include the [[APMDD v2.1 - Glossary#Credential Broker|Credential Broker]]. Accessed by [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugins]] via dedicated [[APMDD v2.1 - Glossary#Port (HMA Context)|Ports]]. (Ref: HMA Spec v1.2, Sec 4.1, 10)
*   **Core (HMA Context)** <!-- #apmdd-glossary-term #apmdd-hma-concept -->
    *   See: [[APMDD v2.1 - Glossary#Microkernel Core (HMA Context)|Microkernel Core (HMA Context)]]
*   **Credential Broker (HMA Context)** <!-- #apmdd-glossary-term #apmdd-hma-concept -->
    *   Definition: A mandatory [[APMDD v2.1 - Glossary#Control Plane Services (HMA Context)|Control Plane Service]] within the [[Hexagonal Microkernel Architecture (HMA) Specification v1.2|HMA]] L2 layer responsible for issuing short-lived, scoped credentials to [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugins]].
    *   APMDD Context: [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugins]] (both L2 Orchestrator and L3 Capability) **must** obtain credentials via the `CredBrokerQueryPort`. (Ref: HMA Spec v1.2, Sec 4.1, 9.2, 10)

D
---
*   **Darwin Information Typing Architecture (DITA)** <!-- #apmdd-glossary-term #apmdd-documentation -->
    *   Definition: An XML-based open standard for designing, writing, managing, and publishing technical documentation. It emphasizes topic-based authoring, content reuse, and semantic markup.
    *   APMDD Context: APMDD mandates DITA-inspired principles (topic-based, semantic structure, reuse via linking/transclusion) for its documentation strategy, using Obsidian as the tooling. (Ref: [[APMDD v2.1 - Documentation Strategy#6.3. Documentation Tooling: DITA-Inspired Principles with Obsidian (Mandatory)|APMDD Documentation Strategy]])
*   **Driving Adapter (HMA Context)** <!-- #apmdd-glossary-term #apmdd-hma-concept -->
    *   Definition: In Hexagonal Architecture, an [[APMDD v2.1 - Glossary#Adapter (HMA Context)|adapter]] that handles incoming requests or events from the external world (e.g., user interfaces, external systems, test harnesses) and invokes operations on the application's Inbound [[APMDD v2.1 - Glossary#Port (HMA Context)|Ports]].
    *   APMDD Context: Resides in the L1 Interface Layer of [[Hexagonal Microkernel Architecture (HMA) Specification v1.2|HMA]], translating external inputs into calls on the Core's Inbound [[APMDD v2.1 - Glossary#Port (HMA Context)|Ports]]. (Ref: HMA Spec v1.2, Sec 4.1, 10)
*   **Driven Adapter (HMA Context)** <!-- #apmdd-glossary-term #apmdd-hma-concept -->
    *   Definition: In Hexagonal Architecture, an [[APMDD v2.1 - Glossary#Adapter (HMA Context)|adapter]] that implements an Outbound [[APMDD v2.1 - Glossary#Port (HMA Context)|Port]] defined by the application core or a [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugin]]. It is called by the application/[[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugin]] to interact with external systems or infrastructure (e.g., databases, message brokers, third-party APIs).
    *   APMDD Context: Resides in the L4 Infrastructure Layer of [[Hexagonal Microkernel Architecture (HMA) Specification v1.2|HMA]], implementing [[APMDD v2.1 - Glossary#Port (HMA Context)|Ports]] defined by the Core or [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugins]] for their operational needs. (Ref: HMA Spec v1.2, Sec 4.1, 10)

E
---
*   **Event (HMA Context)** <!-- #apmdd-glossary-term #apmdd-hma-concept -->
    *   Definition: A record of a significant state change or occurrence within the system, typically published to an [[APMDD v2.1 - Glossary#Event Bus (HMA Context)|Event Bus]] for asynchronous communication.
    *   APMDD Context: Used for inter-[[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugin]] communication and for broadcasting Core state changes in [[Hexagonal Microkernel Architecture (HMA) Specification v1.2|HMA]]. Events **must** use versioned schemas. (Ref: HMA Spec v1.2, Sec 2.3, 7.3)
*   **Event Bus (HMA Context)** <!-- #apmdd-glossary-term #apmdd-hma-concept -->
    *   Definition: The messaging infrastructure (e.g., a message broker) that facilitates asynchronous, [[APMDD v2.1 - Glossary#Event (HMA Context)|event]]-based communication between components in [[Hexagonal Microkernel Architecture (HMA) Specification v1.2|HMA]].
    *   APMDD Context: Accessed by the Core and [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugins]] via a standardized `EventBusPort`. Recommended for asynchronous inter-[[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugin]] communication. (Ref: HMA Spec v1.2, Sec 2.3, 4.1)
*   **Event-Driven Architecture (EDA)** <!-- #apmdd-glossary-term #apmdd-hma-concept -->
    *   Definition: A software architecture paradigm that promotes the production, detection, consumption of, and reaction to [[APMDD v2.1 - Glossary#Event (HMA Context)|events]].
    *   APMDD Context: Recommended in [[Hexagonal Microkernel Architecture (HMA) Specification v1.2|HMA]] for asynchronous communication between [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugins]] or for Core state broadcasts. (Ref: HMA Spec v1.2, Sec 2.3)

H
---
*   **Hexagonal Architecture (Ports & Adapters)** <!-- #apmdd-glossary-term #apmdd-hma-concept -->
    *   Definition: An architectural pattern that isolates a component's core application/business logic from external concerns (UIs, databases, external APIs, test scripts) via explicit interfaces called [[APMDD v2.1 - Glossary#Port (HMA Context)|Ports]]. These [[APMDD v2.1 - Glossary#Port (HMA Context)|Ports]] are implemented by technology-specific [[APMDD v2.1 - Glossary#Adapter (HMA Context)|Adapters]].
    *   APMDD Context: A foundational pattern for [[Hexagonal Microkernel Architecture (HMA) Specification v1.2|HMA]], mandated for all major boundaries. (Ref: HMA Spec v1.2, Sec 2.2)
*   **Hexagonal Microkernel Architecture (HMA)** <!-- #apmdd-glossary-term #apmdd-hma-concept -->
    *   Definition: The specific architectural pattern mandated by APMDD v2.1, detailed in the [[Hexagonal Microkernel Architecture (HMA) Specification v1.2]]. It combines [[APMDD v2.1 - Glossary#Hexagonal Architecture (Ports & Adapters)|Hexagonal Architecture]] with a [[APMDD v2.1 - Glossary#Microkernel Core (HMA Context)|Microkernel]] pattern, enforcing a minimal Core and autonomous, replaceable [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugins]] (including [[APMDD v2.1 - Glossary#L2 Orchestrator Plugin|L2 Orchestrator Plugins]]).
    *   (Ref: [[APMDD v2.1 - Architectural Mandate: Hexagonal Microkernel Architecture (HMA) v1.2|APMDD Architectural Mandate]]; HMA Spec v1.2, Abstract)
*   **HMA Blueprinting** <!-- #apmdd-glossary-term #apmdd-lifecycle-phase -->
    *   Definition: An early activity in APMDD (Phase 0) where the [[APMDD v2.1 - Glossary#Architect (Human)|Architect]] creates an initial, high-level structural sketch of the [[Hexagonal Microkernel Architecture (HMA) Specification v1.2|HMA]], identifying the Core, conceptual [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugins]], and major interactions.
    *   (Ref: [[APMDD v2.1 - Lifecycle: Integrating MDA and Agile Practices#3.1. Overall Lifecycle Phases (MDA Influence)|APMDD Lifecycle]])

I
---
*   **Inbound Port (HMA Context)** <!-- #apmdd-glossary-term #apmdd-hma-concept -->
    *   Definition: An interface defined by an application's core logic (or an [[Hexagonal Microkernel Architecture (HMA) Specification v1.2|HMA]] Core/[[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugin]]) that exposes operations to be called by [[APMDD v2.1 - Glossary#Driving Adapter|Driving Adapters]]. It defines *how the application can be driven*.
    *   APMDD Context: Used by the [[Hexagonal Microkernel Architecture (HMA) Specification v1.2|HMA]] Core to receive requests from L1 [[APMDD v2.1 - Glossary#Adapter (HMA Context)|Adapters]], and potentially by [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugins]] if they expose direct external interfaces (though typically Core-mediated). (Ref: HMA Spec v1.2, Sec 4.1, 10)

L
---
*   **L2 Orchestrator Plugin (HMA Context)** <!-- #apmdd-glossary-term #apmdd-hma-concept #apmdd-role -->
    *   Definition: A specialized, replaceable [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugin]] within [[Hexagonal Microkernel Architecture (HMA) Specification v1.2|HMA]], residing functionally in the L2 (Core) layer but managed like any other [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugin]]. It is responsible for executing complex, multi-step workflows that coordinate multiple [[APMDD v2.1 - Glossary#L3 Capability Plugin|L3 Capability Plugins]].
    *   APMDD Context: Receives tasks from the Core Router and uses Core's `PluginExecutionPort` or the [[APMDD v2.1 - Glossary#Event Bus (HMA Context)|Event Bus]] to interact with L3 [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugins]]. (Ref: HMA Spec v1.2, Sec 4.1, 4.3, 10)
*   **L3 Capability Plugin (HMA Context)** <!-- #apmdd-glossary-term #apmdd-hma-concept -->
    *   Definition: An independently deployable [[Hexagonal Microkernel Architecture (HMA) Specification v1.2|HMA]] [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugin]] residing in the L3 layer, encapsulating a specific business capability or domain logic.
    *   APMDD Context: These are the primary autonomous, self-contained functional units developed by the [[APMDD v2.1 - Glossary#AI Team|AI team]]. (Ref: HMA Spec v1.2, Sec 4.1, 10)
*   **LLMFacadePort (HMA Context)** <!-- #apmdd-glossary-term #apmdd-hma-concept -->
    *   Definition: An Outbound [[APMDD v2.1 - Glossary#Port (HMA Context)|Port]] defined in [[Hexagonal Microkernel Architecture (HMA) Specification v1.2|HMA]] that Core or [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugin]] components can use to call external Large Language Model (LLM) services.
    *   APMDD Context: [[APMDD v2.1 - Glossary#Adapter (HMA Context)|Adapters]] implementing this [[APMDD v2.1 - Glossary#Port (HMA Context)|Port]] **MAY** use [[APMDD v2.1 - Glossary#Model Context Protocol (MCP)|MCP]]. (Ref: HMA Spec v1.2, Sec 2.4, 10)

M
---
*   **Model** <!-- #apmdd-glossary-term #apmdd-modeling #apmdd-artifact -->
    *   Definition: An abstraction, typically visual (e.g., using [[APMDD v2.1 - Glossary#PlantUML|PlantUML]]) or textual, that represents certain aspects of a system, such as its structure, behavior, requirements, or interactions.
    *   APMDD Context: A primary artifact for understanding, communication, and guiding the [[APMDD v2.1 - Glossary#AI Team|AI team]] in implementation. Part of the [[APMDD v2.1 - Glossary#Single Source of Truth (SSoT)|Single Source of Truth]]. (Ref: [[APMDD v2.1 - Modeling Types, Strategy & Notations#4.1. The Pervasive Role of Models in APMDD|APMDD Modeling Strategy]])
*   **Model Context Protocol (MCP)** <!-- #apmdd-glossary-term -->
    *   Definition: An external open standard protocol (e.g., from Anthropic) for structuring contextual information specifically for Large Language Models (LLMs).
    *   APMDD Context: An `LLM Adapter` implementing the `LLMFacadePort` in [[Hexagonal Microkernel Architecture (HMA) Specification v1.2|HMA]] **MAY** use MCP. It is one possible standard, not mandated for all communication. (Ref: HMA Spec v1.2, Sec 2.4)
*   **Model Storming** <!-- #apmdd-glossary-term #apmdd-agile-activity #apmdd-modeling -->
    *   Definition: A just-in-time, collaborative modeling activity in APMDD, typically time-boxed, aimed at quickly resolving specific design or implementation issues that arise during a sprint.
    *   APMDD Context: Involves the [[APMDD v2.1 - Glossary#Architect (Human)|Architect]] and relevant [[APMDD v2.1 - Glossary#AI Team|AI agents]] focusing on a particular problem within a [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugin's]] scope. (Ref: [[APMDD v2.1 - Lifecycle: Integrating MDA and Agile Practices#3.2. Iterative Activities Embedded Within Each Phase (Agile Influence)|APMDD Lifecycle]])
*   **Model Transformation (APMDD Context)** <!-- #apmdd-glossary-term #apmdd-modeling -->
    *   Definition: In APMDD, this refers to the process where the [[APMDD v2.1 - Glossary#AI Team|AI team]] acts as the "intelligent transformation engine," interpreting detailed [[APMDD v2.1 - Glossary#Model|models]] and specifications (primarily visual [[APMDD v2.1 - Glossary#PlantUML|PlantUML]] diagrams and textual contracts) to generate code and other artifacts like tests or documentation.
    *   APMDD Context: Differs from traditional [[APMDD v2.1 - Glossary#Model-Driven Architecture (MDA)|MDA]] by relying on AI interpretation rather than formal, automated M2M/M2T engines. [[APMDD v2.1 - Glossary#Model|Models]] must be precise and comprehensive enough for this AI-driven transformation. (Ref: [[APMDD v1.2 Clarifications.md|Clarifications Q11]])
*   **Model-Driven Architecture (MDA)** <!-- #apmdd-glossary-term -->
    *   Definition: A software design approach launched by the OMG that uses models as the primary artifacts of development, emphasizing separation of concerns through different model types (CIM, PIM, PSM) and model transformations.
    *   APMDD Context: APMDD adopts the CIM/PIM/PSM macro-phase structure from MDA but reinterprets model transformation through AI agency. (Ref: [[APMDD v2.1 - Master Guide & Introduction#1.4. Relationship to MDD, AMDD, and MDA|APMDD Introduction]])
*   **Model-Driven Development (MDD)** <!-- #apmdd-glossary-term -->
    *   Definition: A broader software development approach where models are primary artifacts guiding software creation, analysis, and evolution. [[APMDD v2.1 - Glossary#Model-Driven Architecture (MDA)|MDA]] is a specific type of MDD.
*   **Microkernel Core (HMA Context)** <!-- #apmdd-glossary-term #apmdd-hma-concept -->
    *   Definition: The minimal central component in the [[Hexagonal Microkernel Architecture (HMA) Specification v1.2|HMA]] (L2 layer). Its primary responsibilities are [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugin]] lifecycle management, request routing/dispatching to [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugins]], and providing access to shared [[APMDD v2.1 - Glossary#Control Plane Services (HMA Context)|Control Plane Services]].
    *   APMDD Context: The Core contains no domain-specific business logic itself. (Ref: HMA Spec v1.2, Sec 2.1, 4.1)

O
---
*   **Orchestrator Plugin (HMA Context)** <!-- #apmdd-glossary-term #apmdd-hma-concept -->
    *   See: [[APMDD v2.1 - Glossary#L2 Orchestrator Plugin (HMA Context)|L2 Orchestrator Plugin (HMA Context)]]
*   **Outbound Port (HMA Context)** <!-- #apmdd-glossary-term #apmdd-hma-concept -->
    *   Definition: An interface defined by an application's core logic (or an [[Hexagonal Microkernel Architecture (HMA) Specification v1.2|HMA]] Core/[[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugin]]) that specifies how it interacts with external systems or services (the "driven" side). It defines *what the application needs from the outside world*.
    *   APMDD Context: Implemented by [[APMDD v2.1 - Glossary#Driven Adapter|Driven Adapters]] in the L4 Infrastructure Layer. Used by the Core or [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugins]] to access databases, external APIs, message brokers, etc. (Ref: HMA Spec v1.2, Sec 4.1, 10)

P
---
*   **Platform Independent Model (PIM)** <!-- #apmdd-glossary-term #apmdd-lifecycle-phase #apmdd-modeling -->
    *   Definition: A model in [[APMDD v2.1 - Glossary#Model-Driven Architecture (MDA)|MDA]] and APMDD that describes a software system's structure and behavior without specifying the implementation technologies or platforms. It focuses on "how" the system is built logically, independent of platform specifics.
    *   APMDD Context: A critical phase where the [[Hexagonal Microkernel Architecture (HMA) Specification v1.2|HMA]] structure, [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugin]] boundaries, and [[APMDD v2.1 - Glossary#Port (HMA Context)|Port]] interfaces are precisely defined. (Ref: [[APMDD v2.1 - Lifecycle: Integrating MDA and Agile Practices#3.1. Overall Lifecycle Phases (MDA Influence)|APMDD Lifecycle]])
*   **Platform Specific Model (PSM)** <!-- #apmdd-glossary-term #apmdd-lifecycle-phase #apmdd-modeling -->
    *   Definition: A model in [[APMDD v2.1 - Glossary#Model-Driven Architecture (MDA)|MDA]] and APMDD that refines a PIM by incorporating details related to specific implementation technologies, platforms, and languages.
    *   APMDD Context: Guides the [[APMDD v2.1 - Glossary#AI Team|AI team]] in the concrete implementation of [[Hexagonal Microkernel Architecture (HMA) Specification v1.2|HMA Plugins]] using chosen technologies. (Ref: [[APMDD v2.1 - Lifecycle: Integrating MDA and Agile Practices#3.1. Overall Lifecycle Phases (MDA Influence)|APMDD Lifecycle]])
*   **Plugin (HMA Context)** <!-- #apmdd-glossary-term #apmdd-hma-concept -->
    *   Definition: An independently deployable, self-contained functional unit within the [[Hexagonal Microkernel Architecture (HMA) Specification v1.2|HMA]]. [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugins]] encapsulate specific business capabilities ([[APMDD v2.1 - Glossary#L3 Capability Plugin|L3 Capability Plugins]]) or complex workflow orchestration logic ([[APMDD v2.1 - Glossary#L2 Orchestrator Plugin|L2 Orchestrator Plugins]]). They interact with the Core and potentially each other via defined [[APMDD v2.1 - Glossary#Port (HMA Context)|Ports]] and [[APMDD v2.1 - Glossary#Event (HMA Context)|Events]].
    *   APMDD Context: The primary building blocks developed by the [[APMDD v2.1 - Glossary#AI Team|AI team]]. (Ref: HMA Spec v1.2, Sec 2.1, 10)
*   **PluginExecutionPort (HMA Context)** <!-- #apmdd-glossary-term #apmdd-hma-concept -->
    *   Definition: A standardized Outbound [[APMDD v2.1 - Glossary#Port (HMA Context)|Port]] defined by the [[Hexagonal Microkernel Architecture (HMA) Specification v1.2|HMA]] Core (L2).
    *   APMDD Context: Used by the Core's Router/Dispatcher to invoke operations on [[APMDD v2.1 - Glossary#L3 Capability Plugin|L3 Capability Plugins]] or to dispatch tasks to [[APMDD v2.1 - Glossary#L2 Orchestrator Plugin|L2 Orchestrator Plugins]]. [[APMDD v2.1 - Glossary#L2 Orchestrator Plugin|Orchestrator Plugins]] also use this (via the Core) to call L3 [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugins]]. (Ref: HMA Spec v1.2, Sec 4.1, 4.3)
*   **Port (HMA Context)** <!-- #apmdd-glossary-term #apmdd-hma-concept -->
    *   Definition: A technology-agnostic interface defined by an [[Hexagonal Microkernel Architecture (HMA) Specification v1.2|HMA]] component (Core or [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugin]]) that specifies an interaction contract at its boundary. [[APMDD v2.1 - Glossary#Port (HMA Context)|Ports]] can be Inbound (for receiving requests) or Outbound (for making requests or sending commands).
    *   APMDD Context: Fundamental to [[Hexagonal Microkernel Architecture (HMA) Specification v1.2|HMA]], enabling decoupling and standardized interactions. (Ref: HMA Spec v1.2, Sec 2.2, 10)

S
---
*   **Single Source of Truth (SSoT)** <!-- #apmdd-glossary-term #apmdd-documentation -->
    *   Definition: The principle and practice of structuring information [[APMDD v2.1 - Glossary#Model|models]], master data, and other artifacts such that every data element is stored, and editable, in only one authoritative place.
    *   APMDD Context: In APMDD v2.1, the SSoT comprises "[[APMDD v2.1 - Glossary#Model|models]] + documentation + code." This collective ensures consistency and provides a reliable foundation for both human and AI understanding and action. (Ref: [[APMDD v2.1 - Documentation Strategy#6.2. Single Source of Truth: Models + Documentation + Code|APMDD Documentation Strategy]])
*   **Sprint Modeling** <!-- #apmdd-glossary-term #apmdd-agile-activity #apmdd-modeling -->
    *   Definition: An agile activity in APMDD where the [[APMDD v2.1 - Glossary#Architect (Human)|Architect]] and [[APMDD v2.1 - Glossary#AI Team|AI team]] collaboratively plan the work for an upcoming iteration/sprint, focusing on specific [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugin]] development or refinement. It involves creating "just-enough" [[APMDD v2.1 - Glossary#Model|models]] and specifications.
    *   APMDD Context: Occurs within each macro-phase to detail tasks for the AI team. (Ref: [[APMDD v2.1 - Lifecycle: Integrating MDA and Agile Practices#3.2. Iterative Activities Embedded Within Each Phase (Agile Influence)|APMDD Lifecycle]])

T
---
*   **Test-Driven Development (TDD)** <!-- #apmdd-glossary-term #apmdd-testing #apmdd-agile-activity -->
    *   Definition: A software development process where developers write automated tests for a new function before writing the production code to fulfill that test. The process involves a short iterative cycle of writing a failing test, writing the minimum code to pass the test, and then refactoring the code.
    *   APMDD Context: The primary and mandatory method for developing [[Hexagonal Microkernel Architecture (HMA) Specification v1.2|HMA Plugin]] functionality by the [[APMDD v2.1 - Glossary#AI Team|AI team]]. (Ref: [[APMDD v2.1 - Governance, Quality & Testing#7.3. Testing Strategy: Simplicity, Reliability, and AI-Driven Execution|APMDD Testing Strategy]])

V
---
*   **Vector Store (HMA Context)** <!-- #apmdd-glossary-term #apmdd-hma-concept -->
    *   Definition: A specialized database designed for storing and querying vector embeddings, commonly used in AI/ML applications, particularly those involving semantic search or similarity matching with LLMs.
    *   APMDD Context: If needed by a specific [[Hexagonal Microkernel Architecture (HMA) Specification v1.2|HMA]] [[APMDD v2.1 - Glossary#L3 Capability Plugin|L3 Capability Plugin]], it is managed as part of that [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugin's]] internal L4 infrastructure. Access is via the [[APMDD v2.1 - Glossary#Plugin (HMA Context)|Plugin's]] own [[APMDD v2.1 - Glossary#Adapter (HMA Context)|Adapters]], potentially using credentials obtained from the Core's [[APMDD v2.1 - Glossary#Credential Broker|Credential Broker]]. (Ref: HMA Spec v1.2, Sec 4.1, 10)

W
---
*   **Workflow (AI Context)** <!-- #apmdd-glossary-term -->
    *   Definition: An AI system where LLMs and other tools are orchestrated through predefined code paths or sequences to accomplish a specific, often complex, task. The flow is generally fixed.
    *   APMDD Context: One form of [[APMDD v2.1 - Glossary#AI Team|AI agent]] that can be part of the development team. Contrast with more autonomous AI agents. (Ref: [[APMDD v1.2.md|APMDD v1.2, Sec 3]])

--- END OF FILE APMDD v2.1 - Glossary.md ---