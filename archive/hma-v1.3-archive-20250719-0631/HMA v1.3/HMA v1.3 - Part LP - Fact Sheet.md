---
id: hma_architecture_v1_3
type: HMA_Concept
label: Hexagonal Microkernel Architecture (HMA) v1.3
keywords: [architecture, hexagonal, microkernel, plugin, port, event, apmdd mandate]
summary: HMA v1.3 is APMDD's mandated architecture, synthesizing Hexagonal (Ports & Adapters), Microkernel (minimal Core, autonomous Plugins), and Event-Driven patterns to create modular, governable, and AI-friendly systems.
relationships:
  - type: mandatedBy
    target_id: apmdd_methodology
  - type: coreComponent
    target_ids: [hma_core_l2, hma_plugin_l3_capability, hma_plugin_l2_orchestrator]
  - type: usesPattern
    target_ids: [hma_hexagonal_pattern, hma_microkernel_pattern, hma_eda_pattern]
  - type: definesInterfaceMechanism
    target_ids: [hma_port, hma_adapter]
  - type: definesCommunicationMechanism
    target_id: hma_event_bus
---
**Disclaimer:** This document serves as a high-level introductory guide to HMA v1.3. While it aims to provide a comprehensive overview of the main principles, ideas, and background, the complete and definitive Single Source of Truth (SSoT) resides in the detailed `Part X` documents of the HMA v1.3 specification. For specific implementation details, normative rules, and exhaustive explanations, please refer to the main documentation set.
## Hexagonal Microkernel Architecture (HMA) v1.3

**Definition:** The mandated architectural pattern for systems developed under [[apmdd_methodology|APMDD v2.0]]. HMA v1.3 provides a framework for building AI-augmented platforms requiring rapid evolution, governability, observability, and component replaceability.

**Core Philosophy & Synthesized Patterns:**
1.  **[[HMA v1.3 - Part 3 - Internal Components and Interfaces#9.1 Defining Ports (Inbound/Outbound)|Hexagonal Architecture (Ports & Adapters)]]:** Fundamental for decoupling. All major HMA boundaries are defined by technology-agnostic [[HMA v1.3 - Part 3 - Internal Components and Interfaces#9.1 Defining Ports (Inbound/Outbound)|Ports]], with technology-specific concerns handled by [[HMA v1.3 - Part 3 - Internal Components and Interfaces#9.2 Implementing Adapters (Driving/Driven)|Adapters]].
2.  **[[HMA v1.3 - Part 2 - High-Level Structure#5. The HMA Microkernel Core Zone (L2): Role & Responsibilities|Microkernel Pattern]]:** Enforces a minimal, stable [[HMA v1.3 - Part 2 - High-Level Structure#5. The HMA Microkernel Core Zone (L2): Role & Responsibilities|Core]] focused on routing, Plugin lifecycle, and Control Plane services. Business logic resides in external, replaceable [[HMA v1.3 - Part 3 - Internal Components and Interfaces#9. Deeper Dive: Generic Plugin Components (L3 & L2 Orchestrator)|Plugins]].
3.  **[[HMA v1.3 - Part 3 - Internal Components and Interfaces#10.3 EventBusPort|Event-Driven Architecture (EDA)]]:** Recommended for asynchronous communication between [[HMA v1.3 - Part 3 - Internal Components and Interfaces#9. Deeper Dive: Generic Plugin Components (L3 & L2 Orchestrator)|Plugins]] via a central [[HMA v1.3 - Part 3 - Internal Components and Interfaces#10.3 EventBusPort|Event Bus]].

**Key Architectural Principles:**
*   Maximal Plugin Autonomy & Strict Separation of Concerns.
*   Explicit Boundaries via Ports & Events.
*   Minimal Core (Router/Lifecycle/Control Plane Focus).
*   Replaceable L2 Orchestration via Plugins.
*   Governed Extensibility (Technical & Contractual).
*   Architectural Support for Comprehensive Observability.
*   Security by Design through Boundaries & Mechanisms.

---
id: hma_layered_model
type: HMA_Concept
label: HMA Layered Reference Model (L0-L4)
keywords: [layers, L0, L1, L2, L2.5, L3, L4, actors, interfaces, core, plugins, infrastructure]
summary: HMA employs a strict layered architecture (L0-L4) to enforce separation of concerns, enable replaceability, and manage dependencies.
relationships:
  - type: partOfArchitecture
    target_id: hma_architecture_v1_3
---
## HMA Layered Reference Model (L0-L4)

**Definition:** HMA defines logical layers to structure the system and manage dependencies:
*   **L0: Actor Layer:** External entities (users, systems) interacting with HMA.
*   **L1: Interface Layer (Driving Adapters):** Outermost boundary for inbound requests. Technology-specific [[hma_driving_adapter|Driving Adapters]] translate requests for the L2 Core.
*   **L2: Microkernel Core Layer:** The architectural heart. Contains the [[hma_core_l2_logic|Core logic]] (Router, Lifecycle Mgr, Control Plane) and [[hma_plugin_l2_orchestrator|L2 Orchestrator Plugins]].
*   **L2.5: Instrumentation & Enforcement Sub-Layer:** Houses OTEL SDK and `HMA Compliance Validator`.
*   **L3: Capability Plugin Layer:** Contains independently deployable [[hma_plugin_l3_capability|L3 Capability Plugins]] encapsulating business logic.
*   **L4: Infrastructure Layer (Driven Adapters & External Systems):** Concrete implementations and external dependencies (databases, message brokers, external APIs) accessed via [[hma_driven_adapter|Driven Adapters]].

---
id: hma_core_l2
type: HMA_Component
label: HMA Microkernel Core (L2)
keywords: [core, L2, router, lifecycle manager, control plane, minimal]
summary: The minimal central hub of HMA, responsible for request routing, Plugin lifecycle management, and providing access to Control Plane Services. Contains no business logic.
relationships:
  - type: coreOfArchitecture
    target_id: hma_architecture_v1_3
  - type: residesInLayer
    target_id: hma_layer_L2
  - type: managesLifecycleOf
    target_id: hma_plugin
  - type: providesServiceViaPort
    target_ids: [hma_credential_broker_query_port, hma_event_bus_port, hma_observability_port]
  - type: invokesPluginViaPort
    target_id: hma_plugin_execution_port
---
## HMA Microkernel Core (L2)

**Definition:** The minimalist central component in HMA (L2 layer). Its primary responsibilities are Plugin lifecycle management, request routing/dispatching to Plugins, and providing access to shared Control Plane services.

**Key Internal Components:**
*   **Request Router/Dispatcher:** Routes incoming requests to the appropriate L3 Capability Plugin or L2 Orchestrator Plugin. Its routing is deterministic, based on configuration and registration, differing from the intelligent, adaptive coordination performed by L2 Orchestrator Plugins.
*   **Plugin Lifecycle Manager:** Manages discovery, registration, validation, activation, deactivation, and updates for all Plugins.
*   **Control Plane Services:**
    *   **[[hma_credential_broker|Credential Broker]]:** Vends short-lived, scoped credentials to Plugins via [[hma_credential_broker_query_port]].
    *   **Event Bus Access:** Provides access to the [[hma_event_bus|Event Bus]] via [[hma_event_bus_port]].
    *   **Observability Access:** Provides access for telemetry emission via [[hma_observability_port]].

**Minimalist Mandate:** The Core does NOT contain domain-specific business logic or orchestrate multi-Plugin business workflows itself (this is for [[hma_plugin_l2_orchestrator|L2 Orchestrator Plugins]]).

---
id: hma_plugin
type: HMA_Component_Concept
label: HMA Plugin (L2 Orchestrator / L3 Capability)
keywords: [plugin, L3, L2, capability, orchestrator, autonomous, modular, port-driven]
summary: An independently deployable, self-contained HMA functional unit. L3 Capability Plugins encapsulate business logic; L2 Orchestrator Plugins intelligently and adaptively coordinate complex workflows, typically leveraging LLM-driven logic for dynamic task distribution and sequence management.
relationships:
  - type: componentOfArchitecture
    target_id: hma_architecture_v1_3
  - type: managedBy
    target_id: hma_core_l2
  - type: invokedViaPort
    target_id: hma_plugin_execution_port
  - type: interactsVia
    target_ids: [hma_port, hma_event]
---
## HMA Plugin (L2 Orchestrator / L3 Capability)

**Definition:** An independently deployable, self-contained functional unit within HMA, extending Core functionality. All Plugins are managed by the Core's lifecycle system and interact via defined [[hma_port|Ports]] and [[hma_event|Events]].

**Types:**
*   **[[hma_plugin_l3_capability|L3 Capability Plugin]]:** Resides in L3, encapsulates a specific business capability or domain logic. Highly autonomous, manages its own state and L4 dependencies via internal Adapters.
*   **[[hma_plugin_l2_orchestrator|L2 Orchestrator Plugin]]:** Functionally in L2, managed as a Plugin. Intelligently and adaptively coordinates complex, multi-step workflows, typically leveraging LLM-driven logic or AI agent capabilities for dynamic task distribution and workflow management. This distinguishes it from simpler, rule-based workflow engines.

**Key Characteristics (L2 Orchestrator Plugins):**
*   **Intelligent Coordination:** Often powered by LLMs or AI agents for dynamic and adaptive workflow management.

**Generic Plugin Structure:**
*   Implements the contract defined by the Core's [[hma_plugin_execution_port|PluginExecutionPort]].
*   Contains its own core business/orchestration logic.
*   Defines Outbound [[hma_port|Ports]] for its dependencies (e.g., specific database access, external APIs).
*   Uses internal L4 [[hma_driven_adapter|Driven Adapters]] to implement these Outbound Ports.
*   Consumes Core Control Plane Ports (e.g., [[hma_credential_broker_query_port]], [[hma_event_bus_port]]).

---
id: hma_port
type: HMA_Interface_Concept
label: HMA Port
keywords: [port, interface, contract, technology-agnostic, inbound, outbound]
summary: A technology-agnostic interface defined by an HMA component (Core or Plugin) that specifies an interaction contract at its boundary.
relationships:
  - type: coreConceptOf
    target_id: hma_architecture_v1_3
  - type: implementedOrUsedBy
    target_id: hma_adapter
---
## HMA Port

**Definition:** A technology-agnostic interface defined by an HMA component (Core or Plugin) that specifies an interaction contract at its boundary. Ports enable decoupling and standardized interactions.

**Types:**
*   **Inbound Port:** Defines how a component *can be driven* by external callers (e.g., Core's `RequestPort` called by L1 Adapters).
*   **Outbound Port:** Defines *what a component needs from the outside world* (e.g., a Plugin's `UserRepositoryPort` to access user data, Core's `PluginExecutionPort` to call Plugins).

**Key Standard HMA Port Types:**
*   **[[hma_plugin_execution_port|PluginExecutionPort]]:** (Core Outbound) For Core to invoke Plugins. Implemented by all Plugins.
*   **[[hma_credential_broker_query_port|CredBrokerQueryPort]]:** (Core Outbound) For Plugins to get credentials.
*   **[[hma_event_bus_port|EventBusPort]]:** (Core Outbound) For Core/Plugins to interact with the Event Bus.
*   **[[hma_observability_port|ObservabilityPort]]:** (Core Outbound) For Core/Plugins to emit telemetry.

**Design Standards:** Must have explicit definitions, stable contracts, well-defined parameters/returns, clear error handling, and be versioned (SemVer recommended).

---
id: hma_adapter
type: HMA_Interface_Concept
label: HMA Adapter
keywords: [adapter, technology-specific, driving, driven, bridge]
summary: A technology-specific component implementing a Port (if Driven/Outbound) or using a Port (if Driving/Inbound), bridging HMA's abstract interfaces to concrete technologies.
relationships:
  - type: coreConceptOf
    target_id: hma_architecture_v1_3
  - type: implementsOrUses
    target_id: hma_port
---
## HMA Adapter

**Definition:** A technology-specific component that bridges HMA's abstract, technology-agnostic [[hma_port|Ports]] to concrete technologies or external systems. Adapters handle the specifics of communication protocols, data mapping, and interaction with external infrastructure.

**Types:**
*   **[[hma_driving_adapter|Driving Adapter (L1)]]:** Handles incoming requests/events from L0 Actors (e.g., REST API endpoint, Kafka listener) and invokes operations on the L2 Core's Inbound Ports.
*   **[[hma_driven_adapter|Driven Adapter (L4)]]:** Implements an Outbound Port defined by the L2 Core or an L3/L2-Orchestrator Plugin. It is called by the Core/Plugin to interact with L4 external systems or infrastructure (e.g., a `PostgresUserAdapter` implementing a `UserRepositoryPort`, a `CoreKafkaEventBusAdapter` implementing the `EventBusPort`).

**Location:** Driving Adapters are in L1; Driven Adapters are in L4 (conceptually, they are part of the Core's or Plugin's deployment unit but interact with L4 systems).

---
id: hma_event
type: HMA_Communication_Concept
label: HMA Event
keywords: [event, asynchronous, event bus, schema, metadata, decoupling]
summary: A record of a significant state change or occurrence, published to the Event Bus for asynchronous communication, adhering to versioned schemas and standard metadata.
relationships:
  - type: communicationMechanismIn
    target_id: hma_architecture_v1_3
  - type: transportedVia
    target_id: hma_event_bus
---
## HMA Event

**Definition:** A record of a significant state change or occurrence within the HMA system, typically published to the [[hma_event_bus|Event Bus]] for asynchronous communication between components (primarily Plugins).

**Design Standards:**
*   **Schema Definition:** All events MUST have a clearly defined, versioned schema (JSON Schema recommended).
*   **Standard Metadata:** Events SHOULD include standard metadata like `event_id`, `event_type` (versioned), `event_version`, `source_component_id`, `timestamp`, `trace_id`.
*   **Versioning:** Event schemas MUST be versioned to allow evolution without breaking consumers.
*   **Payload:** Should be focused and contain only relevant data.

**Purpose:** Promotes loose coupling, resilience, and scalability in inter-Plugin communication.

---
id: hma_router_l2
type: HMA_Core_SubComponent
label: HMA L2 Core Router/Dispatcher
keywords: [router, dispatcher, L2, core, deterministic, routing, plugin registration]
summary: The HMA Core component responsible for deterministic dispatch of tasks to L3 Plugins or L2 Orchestrators based on configuration and dynamic Plugin registration.
relationships:
  - type: partOfComponent
    target_id: hma_core_l2
  - type: dispatchesTo
    target_ids: [hma_plugin_l3_capability, hma_plugin_l2_orchestrator]
---
## HMA L2 Core Router/Dispatcher

**Definition:** The component within the [[hma_core_l2|HMA Microkernel Core]] responsible for deterministic dispatching of incoming requests or tasks. Based on request metadata and its dynamic routing configuration (updated via Plugin registration), it directs tasks to either a specific [[hma_plugin_l3_capability|L3 Capability Plugin]] or an [[hma_plugin_l2_orchestrator|L2 Orchestrator Plugin]]. It does not perform intelligent workflow coordination itself but rather acts as a preliminary distribution mechanism. The router must automatically integrate new plugins into its routing table upon their successful registration by the Plugin Lifecycle Manager, without requiring manual code modifications to the router itself.

---
*This Fact Sheet provides a structured overview of key HMA v1.3 concepts. More entries could be added for specific principles, layers, or cross-cutting concerns as needed.*
