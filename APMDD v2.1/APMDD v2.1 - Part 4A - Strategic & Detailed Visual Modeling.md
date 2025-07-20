# APMDD v2.1 - Part 4A - Strategic & Detailed Visual Modeling
#apmdd-modeling #apmdd-documentation #apmdd-architect-focus

> **Note:** The specific mandates for architectural vs. behavioral modeling tools and notations are detailed in [[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]].

Visual models are a cornerstone of the AI-Powered Model-Driven Development (APMDD) v2.1 methodology. They serve as the primary medium for communication, specification, and guidance for both the Human Architect and the AI Team. Critically, for the **Human Architect**, models are indispensable tools for strategic envisioning, architectural design, precise delegation, and effective governance. For the **AI Team**, models provide the clear, unambiguous context needed for implementation.

This document details recommended visual models, their purpose within APMDD, when to use them, specific considerations for an AI-led context, and guidance for their representation using the mandated modeling tools where applicable. The selection emphasizes models that:

1.  **Empower the Human Architect** in strategic decision-making, architectural design (especially for HMA), and efficient project orchestration.
2.  Provide clear, precise, and unambiguous specifications for the AI Team.
3.  Align with APMDD's lifecycle phases ([[APMDD v2.1 - Part 8 - Glossary#Computation Independent Model (CIM)|CIM]], [[APMDD v2.1 - Part 8 - Glossary#Platform Independent Model (PIM)|PIM]], [[APMDD v2.1 - Part 8 - Glossary#Platform Specific Model (PSM)|PSM]]) and agile activities.
4.  Can be effectively represented using the mandated modeling tools: **C4-DSL/Structurizr for architectural (C4) models** and **PlantUML for behavioral and non-C4 structural diagrams**.
5.  Contribute to the [[APMDD v2.1 - Part 8 - Glossary#Single Source of Truth (SSoT)|Single Source of Truth (SSoT)]].

## 1. Strategic Envisioning & Foundational Planning (Architect-Focused)
#apmdd-architect-focus

These models are primarily leveraged by the Human Architect for strategic planning, understanding the business and user context, making foundational architectural decisions, and defining the operational framework. This often occurs before or during the early stages of the CIM phase. While the direct output might not always be PlantUML consumed by AI, the *insights* derived are critical for shaping the HMA structure, subsequent detailed models, and even the AI team's operational context.

---
### 1.1. Wardley Map

*   **APMDD Phase(s):** Pre-CIM / Early Envisioning; Strategic Review cycles.
*   **Purpose in APMDD:**
    *   **Architect:** To understand the value chain, identify user needs, and analyze the evolutionary stages of system components (potential HMA Core services, Plugins). Aids in making strategic decisions about what to build (custom HMA Plugins), what to buy/leverage (SaaS via L4 Adapters), and where to focus development efforts. Crucial for identifying core vs. commodity components within the future HMA.
*   **APMDD Specific Considerations:**
    *   The map is a strategic thinking tool for the Architect. Its outputs (e.g., decisions on component sourcing) directly inform the HMA decomposition and resource allocation.
    *   AI Teams do not directly consume Wardley Maps but benefit from the clear strategic direction and component boundaries derived from them.
*   **PlantUML Guidance:**
    *   Not the primary tool. Specialized tools or manual drawing are common.
    *   Key strategic components identified *can* be summarized in a high-level PlantUML component diagram as an outcome, e.g., showing "Custom Build (HMA Plugin)" vs. "SaaS Service (L4 Adapter target)".

---
### 1.2. C4 Model (Conceptual Levels for HMA)

*   **APMDD Phase(s):**
    *   **Level 1 (System Context):** Pre-CIM / Early Envisioning, CIM.
    *   **Level 2 (Containers):** PIM (initial HMA decomposition).
    *   **Level 3 (Components):** PIM/PSM (detailing HMA Core/Plugin internals).
*   **Purpose in APMDD:**
    *   **Architect:** To progressively decompose the system, understand its structure at different levels of abstraction, and communicate this vision. Essential for designing the HMA and making early, high-impact architectural decisions.
    *   **AI Team:** C2 and C3 diagrams provide clear structural context for HMA Core, Plugins, and their interactions.
*   **APMDD Specific Considerations:**
    *   **C1 (System Context):** Defines the system boundary, users, and external system interactions. Essential for overall scope and for the architect to frame the problem.
    *   **C2 (Containers):** Maps directly to the HMA concept. "Containers" represent the HMA Core, L3 Capability Plugins, L2 Orchestrator Plugins, and key L1/L4 Adapters/external systems. This is a key diagram for defining HMA structure and is a primary input for AI.
    *   **C3 (Components):** Details internal components *within* the HMA Core or a specific HMA Plugin. Architect leads; AI can assist in detailing based on architect's C2 and HMA principles.
*   **C4-DSL/Structurizr Guidance:**
    *   **C4 diagrams are generated as views from the C4-DSL model using Structurizr.** The C4-DSL model is the authoritative source for architectural structure. Do not use PlantUML for C4 diagrams in APMDD v2.1.
    *   PlantUML and other diagram types may be embedded or linked to C4 model elements for behavioral or non-C4 structural views, using Structurizr's embedding/linking features.

---
### 1.3. Product Roadmap

*   **APMDD Phase(s):** Pre-CIM / Envisioning; Ongoing Strategic Planning.
*   **Purpose in APMDD:**
    *   **Architect:** To visualize the evolution of the product/system over time, aligning development efforts (including AI-led Plugin development) with strategic business goals and release milestones. Helps in prioritizing HMA Plugin development and feature rollouts.
*   **APMDD Specific Considerations:**
    *   Provides the "big picture" timeline that guides the architect in phasing the development of HMA Plugins.
    *   AI Teams don't directly consume the roadmap but are assigned tasks (Plugin development) that align with it.
*   **PlantUML Guidance:**
    *   PlantUML Gantt charts can represent a simplified roadmap.
    *   Specialized roadmap tools are more common.
    *   **Example (PlantUML Gantt for high-level phases):**
        ```plantuml
        @startgantt
        Project starts 2024-01-01
        [Phase 1: Core HMA & Auth Plugin] lasts 8 weeks
        [Phase 2: Order Orchestrator & Plugin] lasts 12 weeks
        [Phase 1: Core HMA & Auth Plugin] is colored in Blue
        [Phase 2: Order Orchestrator & Plugin] is colored in Navy
        @endgantt

        ```

---
### 1.4. Organization Chart (for AI Team & Stakeholder Structure)

*   **APMDD Phase(s):** Project Setup; Ongoing Reference.
*   **Purpose in APMDD:**
    *   **Architect:** To design and visualize the structure of the AI development team itself (if multiple specialized AI agents/workflows are used) and to map stakeholder roles and communication lines. Clarifies responsibilities and reporting for the overall APMDD project.
*   **APMDD Specific Considerations:**
    *   While APMDD focuses on a single Human Architect leading an "AI Team," this "team" might consist of different AI agents or workflows with specialized roles (e.g., "Code Generation Agent," "Test Generation Agent," "Documentation Agent"). An org chart can help the architect manage these AI assets.
    *   Also useful for mapping human stakeholders involved in requirements (CIM) and acceptance.
*   **PlantUML Guidance:**
    *   PlantUML class diagrams or component diagrams can be adapted to create org charts.
    *   Use nodes for roles/agents and arrows for reporting/collaboration lines.
    *   **Example (Conceptual AI Team Structure):**
        ```plantuml
        @startuml
        rectangle "Human Architect" as Arch
        package "AI Development Team" {
          rectangle "Lead Code-Gen AI" as LeadCodeGen
          rectangle "Specialist UI-Gen AI" as UIGen
          rectangle "Test Automation AI" as TestAI
          rectangle "Doc & Model Update AI" as DocAI
        }
        Arch --> LeadCodeGen : Manages & Directs
        LeadCodeGen --> UIGen : Coordinates
        LeadCodeGen --> TestAI : Coordinates
        Arch --> DocAI : Manages
        @enduml
        ```

---
## 2. Requirements & Domain Understanding (CIM Phase)
#apmdd-cim

These models help capture what the system should do and understand the business domain. They are key inputs for the CIM phase and inform subsequent PIM development. The architect uses these to solidify requirements before tasking the AI team.

---
### 2.1. Use Case Diagram

*   **APMDD Phase(s):** CIM.
*   **Purpose in APMDD:**
    *   **Architect & AI Team:** Identify system functionalities from actor perspectives, define scope, and provide a high-level overview of "what" the system does. Informs HMA Plugin identification.
*   **APMDD Specific Considerations:** Keep use cases at a business/domain level. Each significant use case might map to HMA Plugins or be orchestrated.
*   **PlantUML Guidance:** Standard syntax. (See previous example).

**Integration with C4 Model:** As per the modeling strategy detailed in `[[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]]`, Use Case Diagrams created with PlantUML should be linked to or embedded within relevant elements (e.g., C4 System Context or Container elements they describe) of the primary C4 architectural model to ensure a cohesive and interconnected system representation.

---
### 2.2. Conceptual Domain Model (using Class Diagram)

*   **APMDD Phase(s):** CIM.
*   **Purpose in APMDD:**
    *   **Architect & AI Team:** Model key business entities, attributes, and relationships. Establishes common vocabulary. Forms the basis for data structures in HMA Plugins and event schemas.
*   **APMDD Specific Considerations:** Focus on conceptual entities. Crucial for AI to understand data context.
*   **PlantUML Guidance:** Class diagram syntax. (See previous example).

**Integration with C4 Model:** As per the modeling strategy detailed in `[[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]]`, Conceptual Domain Models created with PlantUML should be linked to or embedded within relevant C4 model elements (such as Containers or Components) to maintain a unified architectural view.

---
### 2.3. Activity Diagram (for Business Process Modeling)

*   **APMDD Phase(s):** CIM.
*   **Purpose in APMDD:**
    *   **Architect & AI Team:** Model high-level business processes and workflows. Understand sequence, decisions. Helps identify areas for HMA Plugin automation, especially L2 Orchestrators.
*   **APMDD Specific Considerations:** Focus on business logic. Clear activities/decisions are important for AI.
*   **PlantUML Guidance:** Standard syntax. Swimlanes for roles. (See previous example).

**Integration with C4 Model:** As per the modeling strategy detailed in `[[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]]`, Activity Diagrams created with PlantUML should be linked to or embedded within the C4 model elements (such as relevant Containers or Plugins) they describe, ensuring behavioral flows are contextually anchored to the architecture.

---
### 2.4. Supporting Requirements Artifacts (Architect & Stakeholder Focused)

While not always directly modeled in PlantUML for AI consumption, these are vital for the architect during CIM and requirements gathering:

*   **System Use Cases (Textual):** Detailed descriptions elaborating on Use Case Diagrams. Provides narrative context for the architect and can be summarized for AI.
*   **User Stories & Epics:**
    *   **Architect:** To capture granular requirements and group related functionalities. Helps in prioritizing and decomposing work that will eventually become HMA Plugin features.
    *   **AI Team:** Well-defined user stories (especially acceptance criteria) can be direct inputs for TDD within a Plugin.
*   **Personas:**
    *   **Architect:** To maintain user-centricity in design and ensure HMA capabilities align with diverse user needs.
*   **Scenarios / Usage Scenarios (Textual):**
    *   **Architect:** To explore specific interaction paths and edge cases. Informs the design of robust HMA interactions and error handling. Can be translated into sequence diagrams for AI.

**PlantUML Note for Supporting Artifacts:** While these are often textual, key elements or summaries *can* be linked or briefly noted in related PlantUML diagrams (e.g., a Use Case Diagram referencing specific user stories).

---
## 3. HMA Structural Design (PIM Phase)
#apmdd-pim

These models define the technology-agnostic structure of the HMA system. They are critical PIM deliverables, primarily created by the architect and consumed by the AI team.

---
### 3.1. HMA Component Diagram (incorporating C4 Level 2/3)

*   **APMDD Phase(s):** PIM (primary), PSM (refinement).
*   **Purpose in APMDD:**
    *   **Architect & AI Team:** The **master blueprint** for HMA structure (Core, Plugins, Ports). Defines decomposition for AI context management.
*   **APMDD Specific Considerations:** Architect-led. Clearly delineates Plugin boundaries. Ports explicit.

#### C4-DSL/Structurizr Guidance
The HMA Component Diagram, representing C4 Levels 2 (Containers) and 3 (Components), is generated as a view from the C4-DSL model defined using the Structurizr ecosystem. This model is the authoritative source for the HMA structure. Refer to `[[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]]` for the tooling mandate.

---
### 3.2. HMA Port & Event Definitions (using Class Diagram)

*   **APMDD Phase(s):** PIM (primary), PSM (refinement).
*   **Purpose in APMDD:**
    *   **Architect & AI Team:** Precisely define contracts for HMA Ports and Event schemas. Critical specifications for AI implementation.
*   **APMDD Specific Considerations:** Clarity and precision paramount for AI. Align with HMA spec standards.
*   **PlantUML Guidance:** Class diagram syntax. Ports as interfaces, Events as classes. (See previous example).

**Integration with C4 Model:** As per the modeling strategy detailed in `[[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]]`, HMA Port & Event Definition diagrams created with PlantUML should be linked to or embedded within the corresponding C4 model elements (e.g., Ports, Components) to provide precise interface and event contract details in architectural context.

---
### 3.3. Package Diagram

*   **APMDD Phase(s):** PIM, PSM.
*   **Purpose in APMDD:**
    *   **Architect & AI Team:** Organize HMA components and artifacts into logical groups. Manage complexity.
*   **APMDD Specific Considerations:** Helps structure codebase and documentation.
*   **PlantUML Guidance:** Package diagram syntax. (See previous example).

**Integration with C4 Model:** As per the modeling strategy detailed in `[[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]]`, Package Diagrams created with PlantUML should be linked to or embedded within the relevant C4 model elements to clarify logical groupings and maintain architectural cohesion.

---
## 4. HMA Behavioral Design (PIM/PSM Phase)
#apmdd-pim #apmdd-psm

These models describe the dynamic behavior of the HMA system. The architect designs key patterns; the AI team implements and details them.

---
### 4.1. Sequence Diagram

*   **APMDD Phase(s):** PIM (logical), PSM (platform-specific).
*   **Purpose in APMDD:**
    *   **Architect & AI Team:** Illustrate message sequences between HMA components for specific scenarios. Detail Port usage and Event flows. Crucial for AI to implement interaction logic.
*   **APMDD Specific Considerations:** Focus on HMA boundaries. Keep diagrams scenario-focused for AI.
*   **PlantUML Guidance:** Standard syntax. (See previous example).

**Integration with C4 Model:** As per the modeling strategy detailed in `[[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]]`, Sequence Diagrams created with PlantUML should be linked to or embedded within the relevant C4 model elements (such as Ports, Components, or Plugins) to illustrate dynamic interactions in architectural context.

---
### 4.2. State Machine Diagram

*   **APMDD Phase(s):** PIM (logical), PSM (platform-specific).
*   **Purpose in APMDD:**
    *   **Architect & AI Team:** Model HMA Plugin lifecycle and complex entity behavior within Plugins.
*   **APMDD Specific Considerations:** HMA Plugin Lifecycle is key for Core. Entity states clarify Plugin logic for AI.
*   **PlantUML Guidance:** Standard syntax. (See previous example).

**Integration with C4 Model:** As per the modeling strategy detailed in `[[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]]`, State Machine Diagrams created with PlantUML should be linked to or embedded within the relevant C4 model elements (such as Plugins or Components) to provide lifecycle and state context within the architecture.

---
### 4.3. Activity Diagram (for System Logic)

*   **APMDD Phase(s):** PIM (logical), PSM (platform-specific).
*   **Purpose in APMDD:**
    *   **Architect & AI Team:** Model complex logic flows *within* HMA Plugins or L2 Orchestrators.
*   **APMDD Specific Considerations:** Useful for specifying complex business rules or orchestration steps for AI.
*   **PlantUML Guidance:** Similar to business process, but system-focused. (See previous example).

**Integration with C4 Model:** As per the modeling strategy detailed in `[[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]]`, Activity Diagrams for system logic created with PlantUML should be linked to or embedded within the relevant C4 model elements to ensure that detailed logic flows are contextually tied to the architecture.

---
### 4.4. Additional Interaction & Behavioral Models (Architect-Focused, Selective AI Input)

These UML diagrams can be valuable for the architect during detailed design exploration. While not always primary inputs for AI in their full complexity, their simplified outputs or key interaction points can be translated for AI.

*   **Communication Diagram (Collaboration Diagram):**
    *   **Architect:** To get an alternative view of object interactions, emphasizing relationships and message flow structure rather than strict time sequence. Useful for understanding the "wiring" between collaborating parts of a Plugin or between a few closely interacting Plugins.
    *   **AI Team:** Less common as a direct input than sequence diagrams. A complex communication diagram might be simplified or its key interactions shown in a sequence diagram for AI.
    *   **PlantUML:** Supported. `A -> B : message`.
*   **Interaction Overview Diagram:**
    *   **Architect:** To get a high-level view of control flow that involves multiple, complex interactions, where each interaction might be detailed in a separate sequence diagram. Good for orchestrating orchestrations.
    *   **AI Team:** The overview itself might be too high-level for direct AI coding tasks, but the referenced, more detailed sequence diagrams would be key.
    *   **PlantUML:** Activity diagram syntax where activities can be `ref` to other diagrams.
*   **Object Diagram:**
    *   **Architect:** To visualize concrete instances and their relationships at a specific point in time, useful for understanding complex data structures or specific runtime scenarios (e.g., debugging, illustrating test data).
    *   **AI Team:** Can be useful for AI to understand test setup data or expected state after an operation.
    *   **PlantUML:** Supported. `object "InstanceName" as Alias`.
*   **Composite Structure Diagram:**
    *   **Architect:** To detail the internal structure of a complex HMA Plugin or Core component, showing its internal parts (sub-components or classes) and how they are connected via ports or interfaces. Very useful for designing the "internals of the hexagon."
    *   **AI Team:** If a Plugin is sufficiently complex, this diagram can provide a clear blueprint of its internal modules and their wiring, guiding AI in structuring the Plugin's code.
    *   **PlantUML:** Supported. `component "Outer" { component "Inner" }`.
*   **Timing Diagram:**
    *   **Architect:** For systems with strict real-time constraints or time-sensitive interactions between HMA components (e.g., ensuring an L2 Orchestrator receives responses from L3 Plugins within specific deadlines).
    *   **AI Team:** If timing constraints are critical for a Plugin's logic, this diagram (or its specified constraints) would be an important input.
    *   **PlantUML:** Supported. `robust "User" as U; U is Idle; U is Waiting;`.
*   **Robustness Diagram (Boundary-Control-Entity):**
    *   **Architect:** As an intermediate step between Use Cases (CIM) and detailed PIM design (Sequence/Class diagrams). Helps identify candidate objects/responsibilities that will become parts of HMA Plugins or their interfaces.
    *   **AI Team:** The *outputs* of robustness analysis (identified entities, controllers, boundaries) inform the design of Plugin classes and interfaces, rather than the diagram itself being a direct AI input.

**Integration with C4 Model:** As per the modeling strategy detailed in `[[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]]`, all additional interaction and behavioral diagrams created with PlantUML (such as Communication, Interaction Overview, Object, Composite Structure, Timing, and Robustness diagrams) should be linked to or embedded within the relevant C4 model elements to maintain a cohesive and interconnected system representation.

---
## 5. Platform-Specific & Deployment (PSM/Deployment Phase)
#apmdd-psm

These models incorporate technology-specific details and describe the physical deployment. The architect leads, AI may assist with configurations.

---
### 5.1. Deployment Diagram

*   **APMDD Phase(s):** PSM, Deployment.
*   **Purpose in APMDD:**
    *   **Architect & AI Team (for config):** Visualize physical architecture, HMA artifact deployment. Essential for planning.
*   **APMDD Specific Considerations:** Maps HMA logical to physical.

#### C4-DSL/Structurizr Guidance
The Deployment Diagram, a C4 Level view, is generated from the C4-DSL model defined using the Structurizr ecosystem, illustrating the physical deployment of HMA artifacts. Refer to `[[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]]` for the tooling mandate.

---
### 5.2. Network Diagram (Contextual)

*   **APMDD Phase(s):** PSM, Deployment.
*   **Purpose in APMDD:**
    *   **Architect:** Depict technical infrastructure, network zones, communication paths.
*   **APMDD Specific Considerations:** Context for HMA component communication. Less direct AI consumption.
*   **PlantUML Guidance:** Basic network diagrams. (See previous example).

**Integration with C4 Model:** As per the modeling strategy detailed in `[[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]]`, Network Diagrams created with PlantUML should be linked to or embedded within the relevant C4 model elements (such as Deployment Nodes or Containers) to provide infrastructure context within the architectural model.

---
### 5.3. Additional Architectural Models (Architect-Focused)

*   **Milky Way Map & Change Cases:**
    *   **Architect:** Specialized architectural exploration tools for understanding the broader system landscape (Milky Way) and anticipating future architectural evolution (Change Cases). Insights feed into HMA design choices, particularly regarding Plugin boundaries and interface flexibility to accommodate future changes.
    *   **AI Team:** Not direct inputs, but the resulting robust HMA design benefits AI development.

---
## 6. User Experience (UX) - If Applicable

If the HMA system has a UI, these models define its structure and flow, providing context for backend HMA interactions.

---
### 6.1. User Interface (UI) Flow Diagram / Storyboard

*   **APMDD Phase(s):** CIM (high-level), PIM (refined), PSM (detailed).
*   **Purpose in APMDD:**
    *   **Architect & AI Team (for context):** Visualize UI navigation paths. Provides context for AI developing L1 Adapters or Plugins supporting UI interactions.
*   **APMDD Specific Considerations:** High-level flows inform AI about expected backend operation sequences.
*   **PlantUML Guidance:** Activity or state diagrams. (See previous example).

**Integration with C4 Model:** As per the modeling strategy detailed in `[[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]]`, UI Flow Diagrams or Storyboards created with PlantUML should be linked to or embedded within the relevant C4 model elements (such as Adapters or Containers) to ensure user experience flows are contextually represented in the architecture.

---
## 7. Specialized Models for Specific Concerns

---
### 7.1. Data Flow Diagram (DFD) for Complex Event Choreography or Data Pipelines

*   **APMDD Phase(s):** PIM, PSM.
*   **Purpose in APMDD:**
    *   **Architect:** To visualize the movement and transformation of data, especially for complex event-driven choreographies between multiple HMA Plugins or for data-intensive Plugins.
    *   **AI Team:** If a Plugin is part of a complex data flow or event chain, a DFD can clarify its inputs, outputs, and data transformation responsibilities.
*   **APMDD Specific Considerations:** Particularly useful when the Event Bus is heavily used for inter-Plugin communication involving significant data payloads or transformations.
*   **PlantUML Guidance:**
    *   PlantUML supports DFD-like diagrams using component/actor nodes and directed arrows for data flows.
    *   Clearly label data flows and processing steps (which could be HMA Plugins or their internal functions).
    *   **Example (Conceptual DFD for Event Flow):**
        ```plantuml
        @startuml
        actor "External Source" as Source
        component "Ingestion Plugin" <<L3 Capability Plugin>> as Ingest
        component "Processing Plugin" <<L3 Capability Plugin>> as Process
        component "Reporting Plugin" <<L3 Capability Plugin>> as Report
        database "Event Bus" as EB
        database "Data Lake" as DL

        Source --> Ingest : Raw Data
        Ingest --> EB : ProcessedEvent_V1
        EB --> Process : ProcessedEvent_V1
        Process --> EB : EnrichedEvent_V2
        Process --> DL : Store Transformed Data
        EB --> Report : EnrichedEvent_V2
        Report --> User : Generates Report
        @enduml
        ```

**Integration with C4 Model:** As per the modeling strategy detailed in `[[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]]`, Data Flow Diagrams (DFDs) created with PlantUML should be linked to or embedded within the relevant C4 model elements (such as Plugins, Event Buses, or Containers) to ensure data movement and transformation are contextually anchored to the architecture.

---
## Conclusion

The strategic use of these visual models, led by the Human Architect and leveraging mandated modeling tools (C4-DSL/Structurizr for architecture, PlantUML for complementary behavioral and other non-C4 diagrams as detailed in `[[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]]`), is fundamental to the success of APMDD v2.1. This expanded view recognizes that many models serve the architect's strategic and detailed design needs first, the outputs of which then become precise inputs for the AI Team. The emphasis remains on creating a clear, consistent, and evolving [[APMDD v2.1 - Part 8 - Glossary#Single Source of Truth (SSoT)|Single Source of Truth]] that effectively empowers the architect and guides the [[APMDD v2.1 - Part 8 - Glossary#AI Team|AI Team]] in developing robust systems based on the [[APMDD v2.1 - Part 5 - Architectural Mandate - HMA v1.3|Hexagonal Microkernel Architecture]].

---