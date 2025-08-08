# AOS Port, API, and Event Standards

**Version:** 1.0
**Applies to:** AOS v4.1

---

## 1. Principle: Explicit and Stable Contracts

In the Hexagonal Microkernel Architecture (HMA), all interactions across boundaries happen through well-defined, versioned contracts. This prevents the tight coupling and integration chaos common in complex systems.

This document specifies the mandatory standards for all Ports, external-facing APIs, and asynchronous Events within the Antifragile OS (AOS).

## 2. Standard HMA Port Contracts

AOS adopts the standard HMA Core Ports. Plugins interact with these ports to access **[Control Plane Services](./control-plane-services.md)**.

*   ### `PluginExecutionPort`
    *   **Purpose:** The single, standardized interface the Core uses to invoke any plugin.
    *   **Contract:** Defines a generic `invoke(taskPayload)` method. The payload contains all necessary data for the plugin to perform its function. The contract also defines how results and errors are returned.

*   ### `CredBrokerQueryPort`
    *   **Purpose:** Allows plugins to request temporary, scoped credentials.
    *   **Contract:** Defines a `getCredentials(resourceIdentifier)` method that returns a credential object or token.

*   ### `EventBusPort`
    *   **Purpose:** Provides a technology-agnostic way to use the event bus.
    *   **Contract:** Defines `publish(event)` and `subscribe(eventType, handler)` methods.

*   ### `ObservabilityPort`
    *   **Purpose:** Provides a standard way to emit telemetry.
    *   **Contract:** Defines `emitMetric(metricData)`, `emitTrace(traceData)`, and `emitLog(logData)` methods.

## 3. API Design Standards

All external-facing APIs (e.g., REST APIs in L1 Adapters) MUST:
*   Be defined using the **OpenAPI specification**.
*   Use **Semantic Versioning** (MAJOR.MINOR.PATCH).
*   Employ **URL Path Versioning** (e.g., `/api/v1/resource`).
*   Have clearly defined Data Transfer Objects (DTOs) for requests and responses.
*   Use standardized error-reporting structures.

## 4. Event Design & Schema Standards

To ensure reliable asynchronous communication, all events published on the AOS Event Bus MUST adhere to these standards.

### 4.1. Event Schema

*   All events MUST have a schema defined using **JSON Schema**.
*   The schema MUST be versioned. A Schema Registry is HIGHLY RECOMMENDED for managing schemas.

### 4.2. Standard Event Metadata Envelope

Every event payload MUST be wrapped in an envelope containing the following metadata fields:

*   `eventId` (string, UUID): A unique identifier for this specific event instance.
*   `eventType` (string): The versioned type of the event (e.g., `user.created.v1`).
*   `eventVersion` (string, SemVer): The version of the schema this event conforms to.
*   `sourceComponentId` (string): The ID of the plugin or Core component that published the event.
*   `timestamp` (string, ISO 8601): The UTC timestamp of when the event was created.
*   `traceId` (string): The distributed tracing ID to correlate this event with the originating request.
*   `correlationId` (string, optional): An ID to correlate related events in a larger business process. 
