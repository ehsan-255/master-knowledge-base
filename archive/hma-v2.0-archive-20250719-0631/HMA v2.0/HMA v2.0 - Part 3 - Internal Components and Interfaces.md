# Hexagonal Microkernel Architecture (HMA) Specification

_Version 2.0 (Mandatory Dependencies Edition)_

**(Companion document to the AI-Powered Model-Driven Development (APMDD) Methodology v2.0)**

---

**Part 3: HMA Internal Components & Key Interfaces (Analogous to C4 Level 3 - Components)**

This part zooms into the major zones identified in Part 2 (Core, Plugins) and describes their key internal components and the standard interfaces (Ports) they expose or consume. This level of detail is crucial for understanding how HMA achieves its architectural goals.

## 8. Deeper Dive: Microkernel Core Components (L2)
#hma-core-component #hma-zone-core #hma-layer-L2 #c4-level-3
[[HMA v2.0 - Part 2 - High-Level Structure#5. The HMA Microkernel Core Zone (L2): Role & Responsibilities]]

The L2 Microkernel Core, while minimalist, comprises several key logical components that fulfill its mandated responsibilities.

### 8.1 Request Router/Dispatcher Component
*(See [[HMA v2.0 - Part 6 - Supporting Information#19.2 Core HMA Terms (Enhanced for v2.0)|Glossary: Core]])*

*   **Responsibility:** This component is responsible for inspecting incoming requests (received via Inbound Ports like `RequestPort` from L1 Adapters) and determining which L3 Capability Plugin or L2 Orchestrator Plugin should handle the request.
*   **Mechanism:** It typically uses metadata from the request (e.g., path, headers, message type) and its internal routing configuration (which may be static or dynamically updated via Plugin registration) to make this decision.
*   **Output:** It dispatches the task to the selected Plugin by invoking the `PluginExecutionPort`, passing the necessary request data.
*   **Key Interface Used:** Consumes Inbound Ports (e.g., `RequestPort`), uses Outbound `PluginExecutionPort`.

### 8.2 Plugin Lifecycle Manager Component
*(See [[HMA v2.0 - Part 6 - Supporting Information#19.2 Core HMA Terms (Enhanced for v2.0)|Glossary: Plugin]])*

*   **Responsibility:** This component manages the entire lifecycle of all Plugins (both L3 Capability and L2 Orchestrator types) within the HMA system. This includes:
    *   **Discovery & Registration:** Detecting new/updated Plugin packages.
    *   **Validation:** Ensuring Plugins meet technical compliance requirements (see Section 11.2) before activation.
    *   **Activation/Deactivation:** Starting and stopping Plugins.
    *   **Health Monitoring:** Basic health checks to ensure active Plugins are responsive.
    *   **Update/Removal:** Managing Plugin updates and graceful removal.
*   **NEW in v2.0:** MUST validate plugin-manifest.json files against the schema defined in [[HMA v2.0 - Part 1a - Mandatory Dependencies and Standards#6. Plugin Manifest Schema Definition]].

### 8.3 Control Plane Service Components
#hma-core-component
*(See [[HMA v2.0 - Part 6 - Supporting Information#19.2 Core HMA Terms (Enhanced for v2.0)|Glossary: Core]])*

The Core provides access to essential, non-domain-specific services that Plugins rely on for governance and operation.

## 9. Deeper Dive: Generic Plugin Components (L3 & L2 Orchestrator)
#hma-plugin #hma-zone-plugin #c4-level-3

### 9.1 Defining Ports (Inbound/Outbound)
*(See [[HMA v2.0 - Part 6 - Supporting Information#19.2 Core HMA Terms (Enhanced for v2.0)|Glossary: Port]])*

**NEW in v2.0:** All Port contracts MUST use JSON Schema validation for data integrity.

### 9.2 Implementing Adapters (Driving/Driven)
*(See [[HMA v2.0 - Part 6 - Supporting Information#19.2 Core HMA Terms (Enhanced for v2.0)|Glossary: Adapter]])*

**NEW in v2.0:** All Adapters MUST implement proper error handling for validation failures.

## 10. Standard HMA Port Types & Their Purpose
[[HMA v2.0 - Part 1a - Mandatory Dependencies and Standards]]

### 10.1 PluginExecutionPort
**NEW in v2.0:** MUST include JSON Schema validation for all parameters and return types.

### 10.2 CredBrokerQueryPort
**NEW in v2.0:** MUST be backed by secure secrets storage as defined in Part 1a.

### 10.3 EventBusPort
**NEW in v2.0:** All events MUST be validated against schemas before publication.

### 10.4 ObservabilityPort
**NEW in v2.0:** MUST use OpenTelemetry SDK for all telemetry emission.

## 11. HMA Plugin Lifecycle Management (Detailed)

### 11.1 Plugin States and Transitions
Standard plugin lifecycle states: Discovered → Validated → Activated → Running → Deactivated.

### 11.2 Technical Compliance for Plugins

To be managed effectively by the HMA lifecycle system and to participate correctly in the architecture, all Plugins (L2 Orchestrator or L3 Capability) MUST adhere to specific technical compliance requirements:

#### **MANDATORY Requirements (NEW in v2.0)**
*   **Plugin Manifest Compliance:**
    *   MUST provide a `plugin-manifest.json` file conforming to the schema defined in [[HMA v2.0 - Part 1a - Mandatory Dependencies and Standards#6. Plugin Manifest Schema Definition]]
    *   MUST include all required fields: manifestVersion, hmaVersion, plugin metadata, and interface declarations
*   **Interface Contract Adherence:**
    *   MUST correctly implement the `PluginExecutionPort` contract
    *   MUST validate all inputs using JSON Schema validation libraries
    *   MUST correctly consume Core-provided Control Plane Ports according to their defined contracts
*   **Observability Compliance:**
    *   MUST integrate with OTEL SDK for standardized telemetry emission
    *   MUST include TraceID and SpanID in all log entries
    *   MUST emit metrics in Prometheus-compatible format (highly recommended)
*   **Security Compliance:**
    *   MUST obtain all necessary credentials exclusively via the Core's `CredBrokerQueryPort`
    *   MUST use mTLS for internal communication when required
    *   SHOULD implement code signing for plugin integrity verification

#### **Communication Protocol Requirements**
*   **Event Schemas:** MUST use JSON Schema validation for all published events
*   **API Documentation:** MUST provide OpenAPI 3.0+ specifications for any exposed APIs
*   **Version Compatibility:** MUST declare HMA version compatibility in manifest

#### **Validation Process**
The Core's Plugin Lifecycle Manager component performs the following validation before activation:
1. **Manifest Schema Validation:** Validates plugin-manifest.json against official schema
2. **Dependency Check:** Verifies all declared dependencies are available
3. **Security Validation:** Checks signatures if code signing is enabled
4. **Interface Compatibility:** Validates Port contract declarations
5. **Health Check:** Performs basic connectivity and responsiveness tests

**Failure to meet mandatory requirements results in plugin rejection during the registration phase.** 