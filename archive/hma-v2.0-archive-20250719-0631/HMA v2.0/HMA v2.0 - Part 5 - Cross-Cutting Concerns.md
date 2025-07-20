# Hexagonal Microkernel Architecture (HMA) Specification

_Version 2.0 (Mandatory Dependencies Edition)_

**(Companion document to the AI-Powered Model-Driven Development (APMDD) Methodology v2.0)**

---

**Part 5: Applying Cross-Cutting HMA Concerns**

This part addresses the cross-cutting concerns that span across all HMA components: observability, security, and enforcement mechanisms. These concerns are essential for operational excellence and compliance.

## 16. HMA Observability Implementation

### 16.1 Observability Principles in HMA

HMA systems MUST provide comprehensive observability across all layers and components:
- **Distributed Tracing:** Track requests across plugin boundaries
- **Metrics Collection:** Monitor system health and performance
- **Structured Logging:** Capture detailed operational data
- **Correlation:** Link related events across components

### 16.2 Observability Requirements (Tracing, Metrics, Logging)

#### **NEW in v2.0: Mandatory OTEL Integration**

*   **Universal OTEL Requirement:**
    *   ALL HMA components (Core, L2 Orchestrators, L3 Plugins, L1/L4 Adapters) MUST use the OpenTelemetry SDK
    *   The OTEL SDK MUST be configured with HMA-specific conventions (resource attributes, span naming, metric naming)
    *   This integration is NOT optional - it is required for HMA v2.0 compliance

*   **Standardized Configuration:**
    *   **Resource Attributes:** MUST include `hma.component.type`, `hma.component.id`, `hma.layer`
    *   **Span Naming:** MUST follow pattern `hma.{layer}.{component}.{operation}`
    *   **Metric Naming:** MUST follow pattern `hma_{layer}_{component}_{metric_name}`

*   **Compliance Validation:**
    *   The L2.5 HMA Compliance Validator MUST verify OTEL integration
    *   Non-compliant components MUST be flagged in observability dashboards
    *   Automated tests MUST validate telemetry emission patterns

*   **Reference Configuration Example:**
```yaml
otel:
  resource:
    attributes:
      hma.component.type: "L3-Capability"
      hma.component.id: "user-management-plugin"
      hma.layer: "L3"
      service.name: "user-management-plugin"
      service.version: "1.2.3"
  tracing:
    span_naming: "hma.l3.user_management.{operation}"
  metrics:
    prefix: "hma_l3_user_management_"
```

### 16.3 Conceptual Data Flow & Instrumentation

All HMA components MUST instrument:
- Request entry and exit points
- Plugin lifecycle events
- Error conditions and exceptions
- Performance metrics and resource usage
- Security-relevant events

## 17. HMA Security Implementation

### 17.1 Trust Boundaries in HMA

HMA defines clear trust boundaries:
- **L1 External Boundary:** Untrusted external traffic
- **L2 Core Boundary:** Trusted internal communication
- **L3 Plugin Boundary:** Semi-trusted plugin execution
- **L4 Infrastructure Boundary:** Infrastructure service communication

### 17.2 Mandatory Security Controls (Enhanced in v2.0)

To protect HMA systems, the following security controls are MANDATORY:

#### **Enhanced Communication Security**
*   **TLS (Transport Layer Security):** 
    *   MANDATORY for all external network traffic to and from L1 Adapters
    *   MUST use TLS 1.3 or higher
    *   MUST implement proper certificate validation
*   **mTLS (Mutual TLS):** 
    *   MANDATORY for internal communication between HMA components
    *   Core ↔ Plugins, Plugin ↔ Plugin (if direct), Core/Plugin ↔ L4 services
    *   MUST use certificate-based mutual authentication
    *   Certificates MUST be managed through the CredentialBroker system

#### **Enhanced Credential Management**
*   **Secure Backend Requirement (NEW):**
    *   The L2 Core's `CredentialBroker` MUST be backed by a secure secrets storage system
    *   Acceptable backends include: HashiCorp Vault OSS, External Secrets Operator, cloud-native secret stores
    *   Static secrets MUST NOT be embedded in code or configuration files
*   **Credential Rotation:**
    *   MUST support automatic credential rotation
    *   MUST provide credentials with configurable TTL (time-to-live)
    *   MUST handle credential refresh transparently

#### **Plugin Security Enhancements (NEW)**
*   **Code Signing (Highly Recommended):**
    *   Plugin artifacts SHOULD be cryptographically signed
    *   Plugin Lifecycle Manager SHOULD verify signatures before activation
    *   Unsigned plugins SHOULD require explicit approval for activation
*   **Runtime Isolation:**
    *   Enhanced isolation requirements for L3 Plugins
    *   MUST use container-based isolation or equivalent
    *   MUST implement resource quotas and network policies

#### **Validation and Compliance**
*   **Input Validation (Enhanced):**
    *   MANDATORY JSON Schema validation at all Port boundaries
    *   MANDATORY OpenAPI validation for all L1 Adapter APIs
    *   MANDATORY event schema validation for Event Bus interactions
*   **Security Monitoring:**
    *   MUST log all security-relevant events via ObservabilityPort
    *   MUST monitor for failed authentication attempts
    *   MUST alert on unusual credential access patterns

#### **Implementation Requirements**
```yaml
security:
  communication:
    external_tls: "TLS_1_3_REQUIRED"
    internal_mtls: "MANDATORY"
    certificate_management: "CREDENTIAL_BROKER"
  secrets:
    backend_type: "SECURE_STORAGE_REQUIRED"
    rotation: "AUTOMATIC"
    ttl: "CONFIGURABLE"
  plugins:
    code_signing: "HIGHLY_RECOMMENDED"
    runtime_isolation: "CONTAINER_BASED"
    resource_quotas: "MANDATORY"
  validation:
    input_validation: "JSON_SCHEMA_REQUIRED"
    api_validation: "OPENAPI_REQUIRED"
    event_validation: "SCHEMA_REQUIRED"
```

### 17.3 Threat Model Considerations for HMA Structures

Key threats addressed by HMA security model:
- **Plugin Compromise:** Isolation prevents lateral movement
- **Credential Theft:** Centralized credential management with short TTL
- **Man-in-the-Middle:** mTLS prevents eavesdropping and tampering
- **Malicious Plugins:** Code signing and validation prevent deployment
- **Data Exfiltration:** Network policies and monitoring detect anomalies

## 18. HMA Enforcement Mechanisms & Tooling

### 18.1 Static Analysis (hma-lint Concept)

HMA implementations SHOULD include static analysis tools that validate:
- Plugin manifest schema compliance
- Port contract adherence
- Security best practices
- Observability instrumentation completeness

### 18.2 Runtime Policy Enforcement

The L2.5 HMA Compliance Validator MUST enforce:
- Schema validation for all data exchanges
- Security policy compliance
- Observability requirements
- Plugin lifecycle compliance

### 18.3 Plugin Registry Validation

The Plugin Registry MUST validate:
- Plugin manifest schema compliance
- Digital signatures (if enabled)
- Dependency compatibility
- Security permissions alignment

**NEW in v2.0:** All validation failures MUST be logged via the ObservabilityPort and trigger appropriate alerts in monitoring systems. 