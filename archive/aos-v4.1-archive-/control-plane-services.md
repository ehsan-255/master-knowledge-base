# AOS Control Plane Services

**Version:** 1.0
**Applies to:** AOS v4.1

---

## 1. Principle: Centralized Governance for Autonomous Components

In accordance with the Hexagonal Microkernel Architecture (HMA), the Antifragile OS (AOS) provides a set of essential, non-domain-specific services from its L2 Microkernel Core. These **Control Plane Services** act as standardized utilities that all plugins rely on for secure and consistent operation.

By centralizing these functions, AOS ensures that core concerns like security, messaging, and observability are handled uniformly, allowing autonomous plugins to focus solely on their business capabilities. Access to these services is provided exclusively through well-defined, versioned Core Ports.

This document details the mandatory Control Plane services required for a compliant AOS v4.1 implementation, addressing a key HMA adoption requirement.

## 2. The Core Services

### 2.1 Credential Broker (`CredBrokerQueryPort`)

*   **Purpose:** To securely vend short-lived, narrowly-scoped credentials to plugins. This is the **only** approved mechanism for a plugin to get secrets like API keys, database passwords, or access tokens.
*   **HMA Mandate:** This service is critical for HMA security. It prevents the insecure practice of hardcoding secrets in plugin code or configuration. Plugins are treated as distinct, semi-trusted components that must request access to other resources.
*   **Interaction:** A plugin calls the `CredBrokerQueryPort` on the Core, requesting access to a specific resource (e.g., 'auth-database', 'billing-api'). The broker validates the plugin's identity and authorization, then returns a temporary credential.

### 2.2 Event Bus Access (`EventBusPort`)

*   **Purpose:** To provide a standardized, technology-agnostic interface for publishing and subscribing to asynchronous events on the central Event Bus.
*   **HMA Mandate:** This service is the foundation of event-driven communication between plugins, promoting loose coupling and resilience.
*   **Interaction:** A plugin uses the `EventBusPort` to publish events (e.g., `OrderCompleted`) or subscribe to topics of interest. The port's adapter handles the specific implementation details of connecting to the underlying message broker (e.g., NATS, Kafka).

### 2.3 Observability Access (`ObservabilityPort`)

*   **Purpose:** To provide a standardized endpoint for all components (Core and plugins) to emit telemetry data (metrics, traces, and logs).
*   **HMA Mandate:** This service ensures that all observability data is sent to a central collection point in a uniform way, enabling system-wide monitoring and analysis.
*   **Interaction:** All components use the `ObservabilityPort`, typically via an integrated OTEL SDK, to send their telemetry. The port's adapter forwards this data to the L4 observability backend (e.g., an OTEL Collector). For more details, see **[Observability and Compliance](./observability-and-compliance.md)**. 
