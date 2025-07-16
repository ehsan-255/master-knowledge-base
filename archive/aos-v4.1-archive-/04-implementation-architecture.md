## Part IV: Implementation Architecture

This document outlines the implementation architecture for the Antifragile OS (AOS) v4.1, which is a direct realization of the **Hexagonal Microkernel Architecture (HMA) v1.3**. This new architecture replaces the previous monolithic, three-layer model to resolve critical issues related to fragility, separation of concerns, and academic theory dependency (Critiques #38, #10, #41).

The normative source for the HMA architecture is the `HMA v1.3` specification located in the repository. This implementation adheres strictly to the layers, zones, and interaction patterns defined therein.

## HMA L0-L4 Layered Model Adoption

AOS v4.1 fully adopts the HMA layered reference model to enforce a strict separation of concerns:

*   **L0: Actor Layer:** Human users (e.g., System Architects, Project Managers) and external systems that interact with AOS.
*   **L1: Interface Layer:** Technology-specific Driving Adapters (e.g., a future command-line interface, a web UI's GraphQL API) that translate actor requests into calls on the L2 Core's ports.
*   **L2: Microkernel Core & Orchestration Layer:** The heart of the system. It contains the minimal, non-domain-specific Microkernel Core for routing and lifecycle management, alongside one or more L2 Orchestrator Plugins that manage the complex, adaptive workflows of the 5D Journey.
*   **L3: Capability Plugin Layer:** Contains all the core AOS methodologies and tools, each encapsulated as an independent, replaceable Capability Plugin (e.g., Wardley Mapping Plugin, TOC Analysis Plugin, TRIZ Plugin).
*   **L4: Infrastructure Layer:** Contains all Driven Adapters and their corresponding external systems (e.g., databases, knowledge graph backends, event bus brokers).

## HMA Core Components and Behavior

To fully adopt HMA, the L2 Microkernel Core contains several key components with specific behaviors:

*   **Request Router/Dispatcher:** This component is the primary entry point for tasks routed from L1 adapters. Its role is to perform deterministic routing, dispatching the task to the correct L2 Orchestrator or L3 Capability plugin based on request metadata and the plugin registry. It does not contain business logic itself.
*   **Plugin Lifecycle Manager:** This component governs the entire lifecycle of all plugins as detailed in the **[HMA Plugin Lifecycle Concept](./hma-plugin-lifecycle-concept.md)**.
*   **Automatic Plugin Registration:** A critical behavior of the Core is that the Router/Dispatcher **must** automatically integrate newly registered and activated plugins into its routing table. When the Lifecycle Manager successfully activates a new plugin, the Router must be able to immediately dispatch tasks to it without requiring any manual reconfiguration or restarts of the Core. This enables true dynamic pluggability.
*   **Control Plane Services:** The Core provides essential, non-domain-specific services that all plugins can consume via standardized ports. These are detailed in **[AOS Control Plane Services](./control-plane-services.md)**.

## AOS Capabilities as HMA Plugins

The modular nature of HMA allows AOS to treat its core intellectual property as swappable, independently managed components.

*   **L3 Capability Plugins:** Each distinct analytical or methodological tool within AOS is implemented as a self-contained L3 Capability Plugin. This makes the framework extensible and less dependent on any single academic theory (resolving Critique #41). Examples include:
    *   `wardley-mapping-plugin`
    *   `theory-of-constraints-plugin`
    *   `design-thinking-plugin`
    *   `triz-methods-plugin`

*   **L2 Orchestrator Plugins:** The complex, multi-step logic of AOS is managed by a system of cooperating L2 Orchestrator Plugins. This replaces the previous monolithic model to enhance flexibility and architectural purity.
    *   **`Meta-Orchestrator` (`Process-Router`):** A minimal L2 plugin that acts as the primary entry point. It reads a "Process Recipe" from the Project Digital Twin (PDP) and routes the project to the appropriate Phase Orchestrator.
    *   **`Phase Orchestrators`:** Each phase of a process is encapsulated in its own L2 Orchestrator plugin (e.g., `DefinePhaseOrchestrator`, `DiagnosePhaseOrchestrator`, `DMAIC-Analysis-Orchestrator`). These plugins execute the logic for a single phase and then publish a generic event upon completion, returning control to the Meta-Orchestrator.

This plugin-based structure forces all interactions to be mediated through the HMA Core via well-defined ports, directly resolving the "Composition Fallacy" (Critique #1).

## Core Interaction Patterns in AOS

AOS utilizes the three primary HMA interaction patterns:

1.  **Direct Synchronous:** An actor uses an L1 interface to request a specific analysis (e.g., "Generate a Wardley Map"). The L2 Core routes this request directly to the `wardley-mapping-plugin` for immediate execution and response.
2.  **Asynchronous Event-Driven:** A plugin publishes a significant finding as an event (e.g., `ConstraintIdentifiedEvent`). Other plugins can subscribe to this event to react and perform their own analysis, decoupling the components.
3.  **Orchestrated Multi-Plugin Workflow:** The `Meta-Orchestrator` receives a project and routes it to the `DesignPhaseOrchestrator`. This Phase Orchestrator then synchronously calls the `design-thinking-plugin` and `triz-methods-plugin` (both L3), reconciles their outputs, updates the PDP, and publishes a `phase.completed` event.

## Conceptual Configuration

The following YAML snippet illustrates the conceptual configuration for an HMA-based AOS v4.1 instance. It defines which plugins are active and provides configuration for core infrastructure components like the event bus.

```yaml
# Conceptual HMA Configuration for an AOS v4.1 Instance
version: 1.3
hma_core:
  plugin_registry:
    # L2 Meta-Orchestrator
    - name: "aos-process-router"
      version: "1.0.0"
      state: "active"
      type: "L2-Orchestrator"

    # L2 Phase Orchestrator Plugins for the 5D Journey
    - name: "aos-define-phase-orchestrator"
      version: "1.0.0"
      state: "active"
      type: "L2-Orchestrator"
    - name: "aos-diagnose-phase-orchestrator"
      version: "1.0.0"
      state: "active"
      type: "L2-Orchestrator"
    # ... (add other 5D phase orchestrators as needed) ...

    # L3 Capability Plugins providing specific methodologies
    - name: "aos-wardley-mapping-plugin"
      version: "1.2.0"
      state: "active"
      type: "L3-Capability"
    - name: "aos-toc-analysis-plugin"
      version: "1.1.0"
      state: "active"
      type: "L3-Capability"
    - name: "aos-triz-methods-plugin"
      version: "1.0.0"
      state: "active"
      type: "L3-Capability"
    - name: "aos-design-thinking-plugin"
      version: "1.5.1"
      state: "active"
      type: "L3-Capability"

infrastructure:
  event_bus:
    provider: "NATS" # Example, could be Kafka, RabbitMQ, etc.
    url: "nats://message-broker:4222"
  observability:
    provider: "OTLP"
    endpoint: "http://otel-collector:4317"
```

---

*This document conceptually supersedes the previous monolithic implementation. All other documents in the `aos/` folder should be interpreted through the lens of this HMA-based architecture.* 

### Intelligent Plugin Advisor (Rule-Based Adapter)  <!-- NEW INTEGRATION C-2 -->

A lightweight micro-service runs alongside the Core. It listens for `pdp.phase.entered.v1` events, inspects the Problem Ontology attributes attached to the current PDP, and executes a declarative rule engine (e.g., Open Policy Agent or Drools). The service then emits a ranked list of recommended capability plugins via the Event Bus (`plugin.recommendation.v1`).

Because guidance is expressed as data (rules) rather than code branches, new decision logic can be deployed at runtime without redeploying or restarting the Core. This keeps the Microkernel small while delivering context-aware orchestration. 

### Standard HMA Port Catalogue  <!-- HMA ALIGNMENT -->

AOS v4.1 now *inherits verbatim* the five canonical port types defined in HMA v1.3 Part 3 §10.

| Port | Layer | Purpose |
|------|-------|---------|
| `PluginExecutionPort` | Core ↔ L3 | Invokes a plugin’s primary function in a technology-agnostic way. |
| `CredBrokerQueryPort` | Core | Issues short-lived, scoped credentials to plugins. |
| `EventBusPort` | Core ↔ L1/L3 | Publishes/subscribes domain events on the central bus. |
| `ObservabilityPort` | Core ↔ All | Emits metrics, traces, logs in OTEL format. |
| `StoragePort` (optional) | L3 ↔ L4 | Abstracts external data stores (SQL, graph, blob). |

All new plugins **MUST** declare which of these ports they implement/consume in their `plugin-manifest.json`.

### Plugin Lifecycle Manager (PLM)  <!-- HMA ALIGNMENT -->

A dedicated Core sub-component now enforces the lifecycle defined in HMA Part 3 §11:

`Discovered → Registered → Inactive → Activating → Active → Deactivating → Failed → Deprecated`

Lifecycle transitions emit events (`plugin.registered.v1`, `plugin.failed.v1`, etc.) that are routed through `EventBusPort`.  The PLM verifies code signing hashes before activation and consults policy rules to block non-compliant versions. 

### LLM Operating Mode & Gateway  <!-- LLM INTEGRATION -->

AOS v4.1 treats Large-Language-Model calls as **L3 Capability Plugins** that are strictly *single-responsibility*:

1. A Core component (LLM-Gateway Adapter) implements `PluginExecutionPort` and proxies requests to OpenAI, Anthropic, or a local model.
2. Every LLM-driven feature (Clarifier-LLM, Brainstorm-LLM, WBS-LLM, etc.) is a *thin wrapper* that:
   - composes a prompt template,
   - invokes the Gateway **once**,
   - returns a deterministic JSON result.
3. The Orchestrator never passes an entire PDP to an LLM.  It extracts the **minimal task description** and supplies a *system prompt* that forbids out-of-scope actions.
4. Provenance metadata (`llm_model`, `prompt_hash`, `temperature`, `response_tokens`) is added to every LLM result node so humans can audit and reproduce.

This pattern keeps the Core algorithm in charge while still letting LLMs perform high-leverage reasoning or code generation for each toolkit step. 

