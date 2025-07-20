# Hexagonal Microkernel Architecture (HMA) Specification

_Version 2.0 (Mandatory Dependencies Edition)_

**(Companion document to the AI-Powered Model-Driven Development (APMDD) Methodology v2.0)**

---

**Part 2: HMA High-Level Structure: Layers & Major Zones (Analogous to C4 Level 2 - Containers)**

This part describes the macro-architecture of HMA, focusing on its layered model and the major logical "zones" or "containers" within the system. It provides a high-level structural map, showing how different parts of an HMA system are organized and how they generally interact.

## 4. HMA Macro-Architecture: The Layered Reference Model
#hma-layer-L0 #hma-layer-L1 #hma-layer-L2 #hma-layer-L2-5 #hma-layer-L3 #hma-layer-L4 #c4-level-2

HMA employs a strict layered architecture to enforce separation of concerns, enable replaceability, and manage dependencies. Understanding these layers is fundamental to understanding HMA's structure and flow.

### 4.1 Overview of L0-L4 Layers
*(See [[HMA v2.0 - Part 6 - Supporting Information#19.2 Core HMA Terms (Enhanced for v2.0)|Glossary]] for layer definitions)*

HMA defines the following logical layers:

*   **L0: Actor Layer:** This layer represents all external entities that interact with the HMA system. These can be human users, other software systems, administrative tools, or even peer AI agents. Actors initiate requests or consume events from the system.
*   **L1: Interface Layer (Driving Adapters):** This is HMA's outermost boundary from an inbound perspective. It consists of **Driving Adapters** that receive requests or events from L0 Actors. These Adapters are technology-specific (e.g., REST API endpoints, gRPC services, message queue listeners, A2A listeners) and are responsible for translating incoming communication into calls on the L2 Microkernel Core's Inbound Ports.
*   **L2: Microkernel Core Layer & L2.5 Instrumentation Sub-Layer:** This is the architectural heart of HMA, though intentionally minimal in its logic.
    *   **L2 Core Logic:** Contains the non-domain-specific components:
        *   **Request Router/Dispatcher:** Routes incoming tasks from L1 to the appropriate L3 Capability Plugin or L2 Orchestrator Plugin.
        *   **Plugin Lifecycle Manager:** Manages the states and transitions of all Plugins.
        *   **Control Plane Services:** Provides essential, cross-cutting services like the `CredentialBroker`.
        *   **Core Inbound/Outbound Ports:** Defines the interfaces for interaction with L1, L3/L2-Orchestrators, and L4.
    *   **L2 Pluggable Orchestrators:** While functionally part of the application's control flow logic (thus L2), **Orchestrator Plugins** are architected as replaceable components managed by the Core's Lifecycle Manager. They handle complex multi-Plugin workflows, and these are typically LLM-powered agents or workflows responsible for intelligent, adaptive coordination of complex, multi-Plugin tasks.
    *   **L2.5 Instrumentation & Enforcement Sub-Layer:** A conceptual sub-layer within or tightly coupled with L2. It houses components like the OpenTelemetry (OTEL) SDK for emitting standardized telemetry and the `HMA Compliance Validator` for intercepting and validating telemetry or enforcing architectural rules.
*   **L3: Capability Plugin Layer:** This layer contains all the independently deployable **Capability Plugins**. Each Plugin encapsulates a specific, cohesive set of business capabilities, domain logic, or application features. They are self-contained, manage their own state (if any), and interact with the L2 Core (for control plane services or being invoked) and L4 Infrastructure (for their specific needs) via well-defined Ports and Adapters. They may also communicate with other L3 Plugins asynchronously via the Event Bus.
*   **L4: Infrastructure Layer (Driven Adapters & External Systems):** This layer contains the concrete implementations and external dependencies that HMA components interact with.
    *   **Core's Driven Adapters:** Implementations of the Core's Outbound Ports, allowing the Core to interact with its operational infrastructure (e.g., Event Bus Broker, Observability Backend, Plugin Invocation mechanisms, Credential Store).
    *   **Plugin's Driven Adapters:** Implementations of Outbound Ports defined *within* L3 Plugins (or L2 Orchestrator Plugins) for their specific infrastructure needs (e.g., database adapters, external API client adapters, vector store client adapters).
    *   **External Systems:** The actual external services and resources, such as databases, message brokers, LLM services, secret vaults, vector databases, third-party APIs, etc.

### 4.2 Diagram: HMA Layered Reference Model & Major Zones
#hma-diagram

The HMA layered structure is defined within a formal architectural model. Diagrams such as the one below (Diagram 4.2-A) are illustrative views derived from this model. For specific modeling notations and tooling, refer to `[[APMDD v2.1 - Part 4 - Modeling Types, Strategy & Notations]]`.

```mermaid
%%{ init: { 'theme': 'base', "flowchart": { "defaultRenderer": "elk" } } }%%
flowchart TD
    subgraph Zone_L0_Actors [L0: Actor Zone]
        direction TB
        User((User))
        ExtSystem((External System))
        PeerAgent((Peer AI Agent))
    end

    subgraph Zone_L1_Interfaces [L1: Interface Zone - Driving Adapters]
        direction TB
        RestAdapter["REST API Adapter"]
        EventAdapterIn["Event Listener Adapter"]
        A2AListener["A2A Listener Adapter"]
    end

    subgraph Zone_L2_Core_Orch_Instr [L2: Core & Orchestration Zone + L2.5]
        direction TB
        subgraph L2_Core_Kernel [L2 Microkernel Core]
            RouterDispatcher["Request Router/Dispatcher"]
            PluginLifecycleMgr["Plugin Lifecycle Mgr"]
            ControlPlaneSvcs["Control Plane Services e.g. CredentialBroker"]
        end
        subgraph L2_Orchestrators_SubZone [L2 Orchestrator Plugins]
             AgenticOrchestratorPluginZ["Agentic Orchestrator Z"]
        end
        subgraph L2_5_Instrumentation [L2.5 Instrumentation & Enforcement]
            OTEL_SDK["OTEL SDK"]
            HMA_Validator["HMA Compliance Validator"]
        end
        CoreInPorts["Core Inbound Ports e.g. RequestPort"]
        CoreOutPorts["Core Outbound Ports e.g. PluginExecPort, EventBusPort"]
    end

    subgraph Zone_L3_Plugins [L3: Capability Plugin Zone]
        direction TB
        CapabilityPluginA["Capability Plugin A"]
        CapabilityPluginB["Capability Plugin B"]
        PluginPortsOut["Plugin Outbound Ports to L4 or L2 Ctrl"]
    end

    subgraph Zone_L4_Infrastructure [L4: Infrastructure Zone - Driven Adapters & External Systems]
        direction TB
        CoreDrivenAdapters["Core's Driven Adapters to EventBus, Telemetry"]
        PluginDrivenAdapters["Plugins' Driven Adapters to DBs, Ext.APIs"]
        ExternalSystems["External Systems: Databases, LLMs, Event Broker"]
    end

    %% Connections between Zones/Layers
    User --> RestAdapter
    User --> EventAdapterIn
    ExtSystem --> EventAdapterIn
    PeerAgent --> A2AListener

    RestAdapter --> CoreInPorts
    EventAdapterIn --> CoreInPorts
    A2AListener --> CoreInPorts

    CoreInPorts --> RouterDispatcher
    RouterDispatcher --> PluginLifecycleMgr
    RouterDispatcher --> ControlPlaneSvcs
    RouterDispatcher --> AgenticOrchestratorPluginZ
    RouterDispatcher --> CapabilityPluginA
    RouterDispatcher --> CapabilityPluginB

    AgenticOrchestratorPluginZ --> CapabilityPluginA
    AgenticOrchestratorPluginZ --> CapabilityPluginB
    AgenticOrchestratorPluginZ --> ControlPlaneSvcs
    AgenticOrchestratorPluginZ --> OTEL_SDK
    AgenticOrchestratorPluginZ --> PluginDrivenAdapters

    CapabilityPluginA --> ControlPlaneSvcs
    CapabilityPluginB --> ControlPlaneSvcs
    CapabilityPluginA --> OTEL_SDK
    CapabilityPluginB --> OTEL_SDK
    CapabilityPluginA --> PluginDrivenAdapters
    CapabilityPluginB --> PluginDrivenAdapters

    CoreOutPorts --> CoreDrivenAdapters
    CoreOutPorts --> OTEL_SDK

    OTEL_SDK --> HMA_Validator
    HMA_Validator --> CoreDrivenAdapters

    CoreDrivenAdapters --> ExternalSystems
    PluginDrivenAdapters --> ExternalSystems

    %% Styling for Zones
    style Zone_L0_Actors fill:#fdebd0,stroke:#a04000,stroke-width:2px
    style Zone_L1_Interfaces fill:#eafaf1,stroke:#1abc9c,stroke-width:2px
    style Zone_L2_Core_Orch_Instr fill:#d6eaf8,stroke:#3498db,stroke-width:2px
        style L2_Core_Kernel fill:#ebf5fb,stroke:#3498db,stroke-width:1px,stroke-dasharray:5 5
        style L2_Orchestrators_SubZone fill:#fef9e7,stroke:#f39c12,stroke-width:1px,stroke-dasharray:5 5
        style L2_5_Instrumentation fill:#eaeded,stroke:#85929e,stroke-width:1px,stroke-dasharray:5 5
    style Zone_L3_Plugins fill:#d5f5e3,stroke:#2ecc71,stroke-width:2px
    style Zone_L4_Infrastructure fill:#f4ecf7,stroke:#af7ac5,stroke-width:2px

    classDef itemNode fill:#fff,stroke:#333,stroke-width:1.5px
    class User,ExtSystem,PeerAgent,RestAdapter,EventAdapterIn,A2AListener,RouterDispatcher,PluginLifecycleMgr,ControlPlaneSvcs,AgenticOrchestratorPluginZ,OTEL_SDK,HMA_Validator,CoreInPorts,CoreOutPorts,CapabilityPluginA,CapabilityPluginB,PluginPortsOut,CoreDrivenAdapters,PluginDrivenAdapters,ExternalSystems itemNode

```
*   **Diagram 4.2-A: HMA Layered Reference Model & Major Zones (Illustrative View):** This diagram visualizes the L0-L4 layers as distinct zones, emphasizing the separation. It shows the Core, Orchestrator Plugins, and Instrumentation within the L2 Zone, and how Capability Plugins form the L3 Zone. Interactions flow between these major zones. The formal definition of this architecture resides in a model compliant with APMDD's modeling strategy.

**(Note: The more detailed component diagram, previously Diagram 4-A in HMA v1.2, is still valuable and will be referenced or adapted for Part 3 when discussing component-level details within these zones.)**

### 4.3 Interaction Flow Between Layers

The primary dependency and interaction flow in HMA is generally unidirectional through the layers for requests, though responses and events can flow in other directions:

1.  **L0 Actors** initiate interactions.
2.  **L1 Interface Adapters** receive these, translate them, and call Inbound Ports on the **L2 Microkernel Core**.
3.  The **L2 Core** (Router/Dispatcher) then:
    *   For simple tasks, routes the request to an appropriate **L3 Capability Plugin** via the `PluginExecutionPort`.
    *   For complex tasks, routes the request to an appropriate **L2 Orchestrator Plugin**.
4.  An **L2 Orchestrator Plugin**, upon receiving a task, coordinates multiple **L3 Capability Plugins**. It does this by making calls *back through* the L2 Core's `PluginExecutionPort` (or by publishing/subscribing to events via the `EventBusPort`).
5.  **L3 Capability Plugins** (and L2 Orchestrator Plugins) execute their logic. They may:
    *   Interact with L2 Control Plane services (e.g., `CredentialBroker`) via their respective Ports.
    *   Use their *own* internal Adapters and Outbound Ports to interact with **L4 Infrastructure** (e.g., databases, external APIs, Vector Stores).
    *   Publish events to, or consume events from, the `EventBusPort` (which is connected to an L4 Event Bus Broker via a Core Driven Adapter).
6.  **L4 Infrastructure** components (Driven Adapters) are implementations of Ports defined by L2 or L3 components. They interact with actual external systems (also L4).

**Key Dependency Rule:** Higher layers (e.g., L3 Plugins) generally depend on interfaces defined by lower layers (e.g., L2 Core Ports for Control Plane access). Direct dependencies from lower layers to higher layers are typically avoided, with interactions mediated by Ports or events. The Core (L2) does not depend on concrete Plugin (L3) implementations, only on the abstract `PluginExecutionPort` contract.

## 5. The HMA Microkernel Core Zone (L2): Role & Responsibilities
#hma-zone-core #hma-layer-L2 #c4-level-2
[[HMA v2.0 - Part 3 - Internal Components and Interfaces#8. Deeper Dive: Microkernel Core Components (L2)]]

The L2 Zone is the central nervous system of HMA, but it is designed to be minimal and focused. It encompasses the Microkernel Core itself, any L2 Orchestrator Plugins, and the L2.5 Instrumentation sub-layer.

### 5.1 Core's Minimalist Mandate
#hma-core-component
*(See [[HMA v2.0 - Part 6 - Supporting Information#19.2 Core HMA Terms (Enhanced for v2.0)|Glossary: Core]])*

The Microkernel Core proper (excluding L2 Orchestrator Plugins) adheres to a strict minimalist mandate. Its sole responsibilities are:

*   **Request Routing & Dispatching:** Receiving validated requests from L1 Adapters (via Inbound Ports like `RequestPort`) and routing them to the correct L3 Capability Plugin or L2 Orchestrator Plugin (via the Outbound `PluginExecutionPort`).
*   **Plugin Lifecycle Management:** Discovering, registering, validating, activating, deactivating, and managing the overall lifecycle of all Plugins (both L3 Capability and L2 Orchestrator types).
*   **Control Plane Service Access:** Providing access for Plugins to essential, non-domain-specific Control Plane services (e.g., `CredentialBroker` via `CredBrokerQueryPort`, `EventBus` via `EventBusPort`, `Observability` via `ObservabilityPort`).

The Core **MUST NOT** contain any domain-specific business logic, complex multi-step workflow orchestration logic (that's for L2 Orchestrator Plugins), or manage any business-related state beyond its own operational needs (like the Plugin registry).

### 5.2 Core's Boundaries and Interactions with other Zones

*   **Interaction with L1 (Interface Zone):**
    *   The Core exposes Inbound Ports (e.g., `RequestPort`, `PluginMgmtPort`) that L1 Driving Adapters call.
    *   It receives translated, technology-agnostic requests from L1.
*   **Interaction with L3 (Capability Plugin Zone) & L2 Orchestrator Plugins:**
    *   The Core invokes operations on Plugins via the `PluginExecutionPort`.
    *   The Core manages the lifecycle of these Plugins.
    *   Plugins call back into the Core to access Control Plane services via specific Core Ports (e.g., `CredBrokerQueryPort`).
*   **Interaction with L2.5 (Instrumentation Zone):**
    *   The Core itself emits telemetry via the OTEL SDK.
    *   Its Plugin Lifecycle Manager may emit architecture events concerning Plugin state changes.
*   **Interaction with L4 (Infrastructure Zone):**
    *   The Core uses its own Outbound Ports and corresponding L4 Driven Adapters for its operational needs (e.g., `CoreEventBusAdapter` to connect to an Event Bus Broker, `CoreObsAdapter` to send telemetry to a backend).

### 5.3 Diagram: Core Zone Context
#hma-diagram

```mermaid
%%{ init: { 'theme': 'base', "flowchart": { "defaultRenderer": "elk" } } }%%
flowchart TD
    subgraph L1_Zone [L1: Interface Zone]
        L1_Adapter["Driving Adapter - e.g. REST"]
    end

    subgraph L2_Core_Zone [L2: Core Zone]
        direction LR
        Core_Kernel["`**Microkernel Core**\n- Router/Dispatcher\n- Plugin Lifecycle Mgr\n- Control Plane Ports`"]
        
        L2_Orchestrator_Instance["Optional L2 Orchestrator Plugins"]

        Core_Kernel -. Manages Lifecycle .-> L2_Orchestrator_Instance
    end

    subgraph L2_5_Zone [L2.5: Instrumentation]
        Instrumentation_SubSys["Instrumentation & Enforcement"]
    end

    subgraph L3_Plugin_Zone [L3: Capability Plugin Zone]
        L3_Plugin["Capability Plugins"]
    end

    subgraph L4_Infra_Zone [L4: Infrastructure Zone]
        L4_Core_Adapters["Core Driven Adapters"]
        L4_External_Services["External Systems: Event Broker, Telemetry Backend"]
    end

    L1_Adapter -- Calls Inbound Port --> Core_Kernel
    Core_Kernel -- Routes Task --> L2_Orchestrator_Instance
    Core_Kernel -- Routes Task / Manages --> L3_Plugin
    
    L2_Orchestrator_Instance -- Calls Core Port to invoke --> L3_Plugin
    L2_Orchestrator_Instance -- Accesses Control Plane --> Core_Kernel
    L3_Plugin -- Accesses Control Plane --> Core_Kernel

    Core_Kernel -- Uses Outbound Ports --> L4_Core_Adapters
    L4_Core_Adapters -- Connects to --> L4_External_Services
    
    Core_Kernel -- Emits Telemetry/Events --> Instrumentation_SubSys
    L2_Orchestrator_Instance -- Emits Telemetry/Events --> Instrumentation_SubSys
    L3_Plugin -- Emits Telemetry/Events --> Instrumentation_SubSys
    Instrumentation_SubSys -- Forwards to --> L4_Core_Adapters

    %% Styling
    style L1_Zone fill:#eafaf1,stroke:#1abc9c
    style L2_Core_Zone fill:#d6eaf8,stroke:#3498db,stroke-width:2px
        style Core_Kernel fill:#ebf5fb,stroke:#3498db
        style L2_Orchestrator_Instance fill:#fef9e7,stroke:#f39c12
    style L2_5_Zone fill:#eaeded,stroke:#85929e
    style L3_Plugin_Zone fill:#d5f5e3,stroke:#2ecc71
    style L4_Infra_Zone fill:#f4ecf7,stroke:#af7ac5

```
*   **Diagram 5.3-A: Core Zone Context (Illustrative View):** Highlights the Microkernel Core and associated L2 Orchestrator Plugins, showing their primary interactions with other HMA zones. This structure is formally defined as per APMDD's modeling guidelines.

## 6. HMA Plugins Zone (L3 Capability & L2 Orchestrator): Autonomy & Roles
#hma-zone-plugin #hma-layer-L3 #hma-plugin #c4-level-2
[[HMA v2.0 - Part 3 - Internal Components and Interfaces#9. Deeper Dive: Generic Plugin Components (L3 & L2 Orchestrator)]]

The Plugins Zone is where the application's unique value and business logic reside. HMA distinguishes between L3 Capability Plugins and L2 Orchestrator Plugins, though both are managed as "Plugins" by the Core.

### 6.1 L3 Capability Plugins: Encapsulating Business Logic
#hma-plugin-capability
*(See [[HMA v2.0 - Part 6 - Supporting Information#19.2 Core HMA Terms (Enhanced for v2.0)|Glossary: Plugin]])*

L3 Capability Plugins are the workhorses of an HMA system.

*   **Role:** Each L3 Capability Plugin MUST encapsulate a specific, cohesive piece of business functionality, domain logic, or a distinct system capability (e.g., "User Management Plugin," "Product Catalog Plugin," "Data Analysis Plugin," "RAG Capability Plugin").
*   **Autonomy:** They are designed to be highly autonomous:
    *   **Independent Development & Deployment:** Can be developed, tested, versioned, and deployed independently of other Plugins and the Core (once their Port contracts are stable).
    *   **Self-Contained State:** Manage their own internal state and persistence requirements (if any) via their own L4 Adapters (e.g., a specific database for a specific Plugin). They do not share state directly with other Plugins.
    *   **Encapsulated Dependencies:** All external dependencies (databases, external APIs, specific libraries) are accessed via their own internal Ports and Adapters, isolating these choices from the rest of the system.
*   **Interactions:**
    *   Invoked by the L2 Core (or an L2 Orchestrator Plugin via the Core) through the `PluginExecutionPort`.
    *   Can access L2 Core Control Plane services (e.g., `CredBrokerQueryPort`, `EventBusPort`).
    *   Can publish and subscribe to events on the Event Bus for asynchronous communication with other L3 Plugins.
    *   Direct synchronous calls to other L3 Plugins are generally discouraged; if absolutely necessary, they MUST occur via explicitly defined Ports and be mediated or discoverable via the Core, or use a well-defined service discovery mechanism compatible with HMA principles. EDA is preferred for inter-L3-Plugin communication.

### 6.2 L2 Orchestrator Plugins: Coordinating Complex Workflows
#hma-plugin-orchestrator
*(See [[HMA v2.0 - Part 6 - Supporting Information#19.2 Core HMA Terms (Enhanced for v2.0)|Glossary: Plugin]])*

L2 Orchestrator Plugins handle tasks that require the coordination of multiple L3 Capability Plugins.

*   **Role:** To implement complex, multi-step business processes or workflows that span across several distinct capabilities provided by L3 Plugins. For example, an "Order Processing Orchestrator" might coordinate calls to "Inventory Plugin," "Payment Plugin," and "Shipping Plugin." This coordination is typically achieved through LLM-driven intelligence, allowing for adaptive task sequencing, dynamic distribution of sub-tasks to appropriate L3 Capability Plugins based on their specialization and availability, and sophisticated management of the overall workflow state.
*   **Architectural Placement:** Functionally, they operate at L2 because they embody application control flow logic that is more complex than simple routing but is still application-specific (unlike the generic Core). However, they are *architected and managed as Plugins* by the Core's lifecycle manager. This allows them to be replaceable and independently deployable, just like L3 Plugins.
*   **Interactions:**
    *   Receive initial task requests from the L2 Core Router/Dispatcher (via `PluginExecutionPort`).
    *   Coordinate L3 Capability Plugins by:
        *   Making sequential or parallel calls to them via the L2 Core's `PluginExecutionPort`.
        *   Publishing command events or subscribing to status events on the Event Bus.
    *   Manage the state of the workflow they are orchestrating (e.g., step completion, intermediate results).
    *   Can access L2 Core Control Plane services.
*   **Multiple Orchestrators:** A system MAY have multiple specialized L2 Orchestrator Plugins, each responsible for a different set of complex workflows.

This clear distinction, yet common management mechanism, allows HMA to keep the Core truly minimal while still supporting sophisticated, evolvable application logic. The choice of whether a piece of logic is a simple L3 capability or a complex L2 orchestration is determined by the "Core vs. Plugin Decision Boundary Checklist" (see Part 3, Section 8 of APMDD v2.0, adapted from HMA v1.2 Sec 3.1).

### 6.3 Plugin Zone Boundaries and Interactions

*   **Plugin-Core Interaction:** Strictly via Core-defined Ports (`PluginExecutionPort` for invocation, Control Plane Ports for services).
*   **Plugin-Plugin Interaction (L3 to L3):**
    *   **Preferred:** Asynchronous via the Event Bus (`EventBusPort`).
    *   **Discouraged (Synchronous):** If unavoidable, must be through explicitly defined Ports on the target Plugin and ideally discoverable/routable via a Core mechanism or a dedicated, HMA-compliant service registry. Direct, unmanaged dependencies are forbidden.
*   **Plugin-Infrastructure (L4) Interaction:** Each Plugin manages its own L4 dependencies via its own internal Outbound Ports and Adapters. One Plugin does not directly access another Plugin's L4 infrastructure.

### 6.4 Diagram: Plugin Zone Context
#hma-diagram

```mermaid
%%{ init: { 'theme': 'base', "flowchart": { "defaultRenderer": "elk" } } }%%
flowchart TD
    subgraph L2_Core_Interaction_Point [L2: Core Zone - Interaction Points]
        Core_PluginExecPort["Core: PluginExecutionPort"]
        Core_ControlPlanePorts["Core: ControlPlanePorts - Creds, Events, Observability"]
    end

    subgraph Plugins_Zone [L2/L3: Plugins Zone]
        direction TB
        subgraph L2_Orchestrator_SubZone_Detail [L2 Orchestrator Plugins]
            Orch_PZ["`**LLM-Powered Orchestrator Plugin Z**<br>(Intelligent Workflow Coordination)<br>- Implements Complex Workflow<br>- Calls L3 Plugins (via Core)<br>- Manages Workflow State`"]
        end
        
        subgraph L3_Capability_SubZone_Detail [L3 Capability Plugins]
            Cap_PA["`**Capability Plugin A**\n- Implements Business Logic A\n- Self-contained State/Infra`"]
            Cap_PB["`**Capability Plugin B**\n- Implements Business Logic B\n- Self-contained State/Infra`"]
        end
    end
    
    subgraph L4_Infrastructure_Plugin_Specific [L4: Plugin-Specific Infrastructure]
        Orch_PZ_Infra["Orch.Z Specific Adapters/Infra"]
        Cap_PA_Infra["Plugin A Specific Adapters/Infra - e.g. DB A"]
        Cap_PB_Infra["Plugin B Specific Adapters/Infra - e.g. Ext. API B"]
    end

    %% Interactions
    Core_PluginExecPort -- Invokes / Dispatches Task --> Orch_PZ
    Core_PluginExecPort -- Invokes / Dispatches Task --> Cap_PA
    Core_PluginExecPort -- Invokes / Dispatches Task --> Cap_PB

    Orch_PZ -- Calls via Core_PluginExecPort --> Cap_PA
    Orch_PZ -- Calls via Core_PluginExecPort --> Cap_PB
    Orch_PZ -- Uses --> Core_ControlPlanePorts
    Orch_PZ -- Connects to its own infra --> Orch_PZ_Infra
    
    Cap_PA -- Uses --> Core_ControlPlanePorts
    Cap_PA -- Connects to its own infra --> Cap_PA_Infra
    Cap_PB -- Uses --> Core_ControlPlanePorts
    Cap_PB -- Connects to its own infra --> Cap_PB_Infra

    Cap_PA -. Async via Event Bus .-> Cap_PB

    %% Styling
    style L2_Core_Interaction_Point fill:#d6eaf8,stroke:#3498db
    style Plugins_Zone fill:#ddf,stroke:#555,stroke-width:2px
        style L2_Orchestrator_SubZone_Detail fill:#fef9e7,stroke:#f39c12
        style L3_Capability_SubZone_Detail fill:#d5f5e3,stroke:#2ecc71
    style L4_Infrastructure_Plugin_Specific fill:#f4ecf7,stroke:#af7ac5

```
*   **Diagram 6.4-A: Plugin Zone Context (Illustrative View):** Shows how L2 Orchestrator and L3 Capability Plugins interact with the Core's designated Ports and manage their own connections to L4 infrastructure, based on the formal architectural model.

## 7. Primary HMA Interaction Patterns (High-Level)
#hma-principle

HMA supports several key interaction patterns between its components. Understanding these patterns is crucial for designing compliant and effective HMA systems.

### 7.1 Direct Synchronous Request/Response (via Core to Plugin)

This is the fundamental pattern for invoking a specific capability.

1.  An L0 Actor sends a request, which is processed by an L1 Adapter.
2.  The L1 Adapter calls an Inbound Port on the L2 Core.
3.  The L2 Core's Router/Dispatcher identifies the target L3 Capability Plugin (or a simple task for an L2 Orchestrator Plugin).
4.  The Core invokes the Plugin via the `PluginExecutionPort`, passing the request data.
5.  The Plugin executes its logic and returns a response to the Core via the `PluginExecutionPort`'s contract.
6.  The Core forwards the response back through L1 to the L0 Actor.

### 7.2 Asynchronous Event-Driven Communication
[[HMA v2.0 - Part 4 - Detailed Specifications and Standards#13. Event Design & Schema Standards]]

This pattern is recommended for decoupling Plugins, especially L3 Capability Plugins.

1.  A source Plugin (L3 or L2 Orchestrator) encounters a significant state change or needs to notify other parts of the system.
2.  It constructs an Event message adhering to a standard schema.
3.  It publishes this Event to the Event Bus via the Core's `EventBusPort` (implemented by a Core Driven Adapter connecting to an L4 Event Bus Broker).
4.  One or more other Plugins (L3 or L2 Orchestrator) that have subscribed to this Event type (or topic) receive the Event from the Event Bus (via their own subscription mechanism, which ultimately uses the Core's `EventBusPort` infrastructure).
5.  Consuming Plugins process the Event asynchronously.

### 7.3 Orchestrated Multi-Plugin Workflows
[[HMA v2.0 - Part 3 - Internal Components and Interfaces#9. Deeper Dive: Generic Plugin Components (L3 & L2 Orchestrator)]]

This pattern is used for complex tasks requiring coordination of multiple L3 Capability Plugins, managed by an L2 Orchestrator Plugin.

1.  An L0 Actor's request for a complex workflow reaches the L2 Core (as in 7.1).
2.  The Core's Router/Dispatcher routes the task to a designated L2 Orchestrator Plugin (via `PluginExecutionPort`).
3.  The L2 Orchestrator Plugin executes its workflow logic, which involves:
    *   Potentially making multiple synchronous calls to different L3 Capability Plugins (via the Core's `PluginExecutionPort`). It receives responses and uses them to decide the next step.
    *   OR, publishing command Events and/or subscribing to status Events from L3 Capability Plugins to manage the flow asynchronously.
4.  The L2 Orchestrator Plugin aggregates results or determines the final outcome of the workflow.
5.  It returns the final result to the Core (via `PluginExecutionPort`), which then forwards it to the L0 Actor.
    (As illustrated in original HMA v1.2 Diagram 4.3-A)

### 7.4 Diagram: Key Interaction Patterns Overview
#hma-diagram

```mermaid
%%{ init: { 'theme': 'base', "flowchart": { "defaultRenderer": "elk", "elk.direction": "RIGHT" } } }%%
graph LR
    subgraph SystemBoundary["HMA System Boundary"]
        Core["L2 Microkernel Core"]
        OrchP["L2 Orchestrator Plugin"]
        CapP1["L3 Capability Plugin 1"]
        CapP2["L3 Capability Plugin 2"]
        EventBus[("L4 Event Bus Broker")]
    end
    
    Actor["L0 Actor"]

    %% Pattern 1: Direct Sync Request/Response
    Actor -- 1. Request --> Core
    Core -- 2. Route to CapP1 (Sync) --> CapP1
    CapP1 -- 3. Response --> Core
    Core -- 4. Response --> Actor
    
    %% Pattern 2: Async Event-Driven
    CapP1 -- 5. Publish Event --> EventBus
    EventBus -- 6. Deliver Event --> CapP2
    note_event["Note: Access to EventBus via Core's EventBusPort"]
    Core -.-> note_event
    
    %% Pattern 3: Orchestrated Workflow
    Actor -- 7. Complex Request --> Core
    Core -- 8. Route to OrchP (Sync) --> OrchP
    OrchP -- "9a. Call CapP1 (Sync, via Core)" --> Core
    Core --- CapP1
    CapP1 --- Core
    Core --- OrchP
    OrchP -- "9b. Call CapP2 (Sync, via Core)" --> Core 
    Core --- CapP2
    CapP2 --- Core
    Core --- OrchP
    OrchP -- 10. Final Response --> Core
    Core -- 11. Response --> Actor

    %% Styling
    style Actor fill:#fdebd0,stroke:#a04000
    style Core fill:#d6eaf8,stroke:#3498db
    style OrchP fill:#fef9e7,stroke:#f39c12
    style CapP1 fill:#d5f5e3,stroke:#2ecc71
    style CapP2 fill:#d5f5e3,stroke:#2ecc71
    style EventBus fill:#f4ecf7,stroke:#af7ac5
    style note_event fill:#eee,stroke:#999,color:#333,stroke-dasharray:2 2
```
*   **Diagram 7.4-A: Key Interaction Patterns Overview:** Illustrates simplified versions of the three primary interaction patterns within an HMA system.

--- 