# HMA Layer Mapping for AOS v5.0

**Version:** 1.0
**Applies to:** AOS v5.0

---

## 1. Mapping AOS Concepts to HMA Layers

This document provides a clear mapping from the high-level concepts of the Antifragile OS to the specific layers of the Hexagonal Microkernel Architecture (HMA) v1.3. This ensures architectural clarity and provides a definitive reference for how AOS is structured.

This mapping is a critical step in resolving multiple architectural critiques, including #10 (Separation of Concerns).

## 2. The Layer Mapping

| AOS Concept / Component | HMA Layer | HMA Component Type | Rationale |
| :--- | :--- | :--- | :--- |
| **Human User / External System** | **L0: Actor Layer** | Actor | The initiators of requests and consumers of results. |
| **CLI, Web UI, API Endpoints** | **L1: Interface Layer** | Driving Adapter | Provides the technology-specific entry points into the system, translating external calls into internal port invocations. |
| **Request Router, Plugin Mgr.** | **L2: Core Layer** | Microkernel Core | The minimal, non-domain-specific heart of the system responsible for routing and lifecycle management. |
| **Meta-Orchestrator Logic** | **L2: Core Layer** | L2 Orchestrator Plugin | A minimal plugin responsible only for routing projects between phases based on a recipe. |
| **Phase-Specific Workflow Logic** | **L2: Core Layer** | L2 Orchestrator Plugin | Each phase (Define, Diagnose, etc.) is its own swappable L2 plugin, encapsulating the logic for that specific stage. |
| **OTEL SDK, Compliance Validator** | **L2.5: Instrumentation** | Instrumentation | The cross-cutting components for telemetry and architectural rule enforcement. |
| **Wardley, TOC, TRIZ, etc.** | **L3: Capability Layer** | L3 Capability Plugin | Each distinct methodology is an independent, swappable plugin, encapsulating its specific domain logic. |
| **Kafka, NATS, RabbitMQ** | **L4: Infrastructure Layer** | External System (Broker) | The concrete message broker technology used by the `EventBusPort`'s adapter. |
| **Postgres, Neo4j, Vault** | **L4: Infrastructure Layer**| External System | The specific database, graph, or secret store technologies used by a plugin's driven adapters. |
| **Plugin DB Connectors**| **L4: Infrastructure Layer**| Driven Adapter | The specific code within a plugin that implements its outbound port to connect to a database. |

This clear separation ensures that business logic (L3) is decoupled from orchestration (L2), which is decoupled from core routing (L2), which is decoupled from infrastructure (L4), providing maximum flexibility and resilience. 
