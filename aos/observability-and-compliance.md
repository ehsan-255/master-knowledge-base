# AOS Observability, Compliance, and Enforcement

**Version:** 1.0
**Applies to:** AOS v5.0

---

## 1. Principle: See, Understand, and Govern

The Antifragile OS (AOS) mandates that the system must be deeply observable and that its architecture must be continuously governed. This is not an optional add-on; it is a foundational requirement for building a resilient and evolvable system, as specified by the Hexagonal Microkernel Architecture (HMA).

This document details the three pillars of this principle:
1.  **Observability:** The architectural requirements for telemetry.
2.  **Compliance:** The L2.5 Instrumentation and Validation layer.
3.  **Enforcement:** The mechanisms for ensuring HMA rules are followed.

*Note: The metrics defined here are for architectural and operational health, distinct from the project and business-value KPIs detailed in **[Antifragile Metrics & Evolution](./05-metrics-and-evolution.md)**.*

## 2. HMA Observability Obligations

All AOS components MUST emit telemetry according to the "three pillars of observability." This data is sent through the `ObservabilityPort` defined in the **[Control Plane Services](./control-plane-services.md)**.

*   **Tracing:** All components MUST generate and propagate distributed trace context (e.g., W3C Trace Context) across all interactions. Spans MUST be created for key boundary crossings (e.g., API entry, Core routing, Plugin execution).
*   **Metrics:** Components SHOULD capture RED (Rate, Errors, Duration) metrics for all significant operations, including API requests, plugin invocations, and external calls (e.g., to databases).
*   **Logging:** All logs MUST be structured (e.g., JSON) and MUST include the `TraceID` and `SpanID` for correlation with other telemetry.

## 3. L2.5 Instrumentation & Compliance Validator

AOS adopts the HMA concept of a conceptual **L2.5 Instrumentation & Enforcement Sub-Layer**.

*   **Instrumentation (OTEL SDK):** All components MUST use a standardized OpenTelemetry (OTEL) SDK. This SDK is configured with AOS-specific conventions to ensure all telemetry is uniform and properly tagged.
*   **HMA Compliance Validator:** This is a critical conceptual component. As telemetry flows from the SDK, the validator intercepts it to:
    *   **Check for Compliance:** Ensure telemetry includes required metadata (e.g., `plugin_id`, `trace_id`).
    *   **Detect Violations:** Identify architectural violations, such as a plugin attempting a forbidden direct call to another plugin.
    *   **Generate Architecture Events:** Emit special events to a dedicated `ArchitectureEventBus` topic when violations or critical lifecycle events occur. This provides a real-time feed for governance.

## 4. Architecture Enforcement Mechanisms

To ensure HMA rules are not just suggestions, AOS relies on automated enforcement.

*   **Static Analysis (`aos-lint`):** In the CI/CD pipeline, a dedicated linter (`aos-lint`) MUST be used to check for architectural violations in the source code before deployment. It checks for illegal imports between plugins, incorrect naming, and other static rule violations. Builds MUST fail if violations are found.
*   **Runtime Policy Enforcement:** A policy engine (e.g., Open Policy Agent) SHOULD be used at critical runtime choke points (like the API gateway or Core router) to enforce security and interaction policies that cannot be checked statically.
*   **Plugin Registry Validation:** The Core's Plugin Lifecycle Manager MUST validate a plugin's manifest and signature before it can be activated, ensuring it complies with all declared dependencies and security policies. 

> **LLM Span Convention**: Any call through the LLM-Gateway MUST create an OTEL span named `llm.call` with attributes `llm.model`, `llm.prompt_hash`, `llm.tokens_in`, `llm.tokens_out`, `llm.latency_ms`. 

In the Architecture Enforcement Mechanisms section, add:

- Static Analysis: Run hma-lint in pipeline (HMA v1.3 Part 5, Section 18.1) to enforce naming and imports.

Example: For Failing state, hma-lint checks lifecycle handlers. 

Enforce with hma-lint in CI/CD to check compliance. 
