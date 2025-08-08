# Hexagonal Microkernel Architecture (HMA) Specification
_Version 2.0 (Mandatory Dependencies Edition)_

**Part 1a: Mandatory Dependencies and Standards**

This part defines the essential dependencies, libraries, and standards that MUST be implemented for HMA v2.0 compliance. These requirements ensure interoperability, security, and observability across all HMA implementations.

## 1. Mandatory Dependencies & Standards

### 1.1 Core Observability Dependencies

#### OpenTelemetry (OTEL) SDK
- **Requirement Level:** MANDATORY
- **Scope:** All HMA components (L2 Core, L2 Orchestrators, L3 Plugins)
- **Purpose:** Standardized telemetry emission for traces, metrics, and logs
- **Implementation:** Components MUST use OTEL-compliant SDK for all telemetry
- **Compliance:** Required for L2.5 Instrumentation layer (Part 5, Section 16)

### 1.2 Security Dependencies

#### mTLS/TLS Cryptographic Libraries
- **Requirement Level:** MANDATORY
- **Scope:** L1 Adapters (TLS), Internal communication (mTLS)
- **Purpose:** Secure communication channels as required by security-by-design
- **Implementation:** 
  - L1 Adapters MUST use TLS libraries for external communication
  - Internal component communication MUST use mTLS-capable libraries
- **Compliance:** Required for Part 5, Section 17.2 security controls

### 1.3 Contract Validation Dependencies

#### JSON Schema Validation Libraries
- **Requirement Level:** MANDATORY
- **Scope:** All Port contracts, Event schemas, API definitions
- **Purpose:** Enforce interface contract integrity and versioning
- **Implementation:** Components MUST validate all data against defined schemas
- **Compliance:** Required for Part 4, Sections 12-13 standards

#### OpenAPI Specification Libraries
- **Requirement Level:** MANDATORY
- **Scope:** All L1 Adapter external APIs
- **Purpose:** Standardized API documentation and validation
- **Implementation:** L1 Adapters MUST document APIs using OpenAPI 3.0+
- **Compliance:** Required for Part 4, Section 12 API standards

### 1.4 Plugin Architecture Dependencies

#### Plugin Manifest Schema Validation
- **Requirement Level:** MANDATORY
- **Scope:** Plugin Lifecycle Manager, All Plugins
- **Purpose:** Standardized plugin metadata and lifecycle management
- **Implementation:** Plugin Lifecycle Manager MUST validate manifest.json files
- **Schema:** Defined in Section 6 of this document
- **Compliance:** Required for Part 3, Section 11 plugin lifecycle

### 1.5 Infrastructure Dependencies

#### Secure Secrets Storage Backend
- **Requirement Level:** MANDATORY (Type)
- **Scope:** CredentialBroker implementation
- **Purpose:** Secure credential storage and distribution
- **Implementation:** CredentialBroker MUST be backed by secure storage
- **Reference Implementations:**
  - HashiCorp Vault OSS
  - External Secrets Operator + Kubernetes Secrets
  - Bitwarden Secrets Manager
  - AWS Secrets Manager (cloud environments)
- **Compliance:** Required for Part 5, Section 17.2 credential management

## 2. Highly Recommended Standards

### 2.1 Interoperability Standards

#### W3C Trace Context Standard
- **Requirement Level:** HIGHLY RECOMMENDED
- **Scope:** All distributed tracing implementations
- **Purpose:** Maximum interoperability with external systems
- **Implementation:** Components SHOULD use W3C Trace Context headers
- **Benefit:** Seamless integration with service meshes, proxies, external systems

#### Code Signing Frameworks
- **Requirement Level:** HIGHLY RECOMMENDED
- **Scope:** Plugin distribution and validation
- **Purpose:** Plugin integrity verification
- **Implementation:** 
  - Plugins SHOULD be cryptographically signed
  - Plugin Lifecycle Manager SHOULD verify signatures before activation
- **Reference Implementations:**
  - GPG signing for plugin packages
  - X.509 certificate-based signing
  - Container image signing (Cosign)

### 2.2 Reference Implementation Guidance

#### Observability Backend Stack
- **Requirement Level:** HIGHLY RECOMMENDED (Type)
- **Scope:** L4 Infrastructure observability backends
- **Purpose:** Complete observability for the three pillars
- **Requirements:** 
  - MUST provide backends for traces, metrics, and logs
  - SHOULD support OTEL protocol ingestion
- **Reference Implementation Stack:**
  - **Metrics:** Prometheus + Grafana
  - **Tracing:** Jaeger
  - **Logging:** Loki + Grafana
- **Alternative Compliant Backends:** VictoriaMetrics, Zipkin, OpenSearch, etc.

#### Event Bus Broker (Conditional)
- **Requirement Level:** CONDITIONAL (Type)
- **Scope:** Event-driven communication implementations
- **Purpose:** Asynchronous inter-plugin communication
- **Requirement:** L4 Event Bus Broker MUST be used if implementing EDA patterns
- **Reference Implementations:**
  - **High Performance:** NATS (simple deployments)
  - **High Scale:** Apache Kafka (enterprise deployments)
  - **Feature Rich:** RabbitMQ (complex routing needs)

## 3. Implementation Compliance Matrix

| **Dependency Category** | **MUST Have** | **SHOULD Have** | **MAY Have** |
|------------------------|---------------|-----------------|--------------|
| **Observability** | OTEL SDK | W3C Trace Context, Prometheus format | Custom telemetry |
| **Security** | mTLS/TLS, Secure secrets backend | Code signing | Additional auth layers |
| **Contracts** | JSON Schema, OpenAPI | Automated validation | Custom validation |
| **Plugin System** | Manifest schema validation | Signature verification | Custom metadata |
| **Communication** | Secure channels | Standard event formats | Custom protocols |

## 4. Validation & Testing Requirements

### 4.1 Compliance Testing
- **Dependency Validation:** Automated tests MUST verify presence of mandatory libraries
- **Contract Testing:** Automated tests MUST validate schema adherence
- **Security Testing:** Automated tests MUST verify TLS/mTLS implementation
- **Plugin Testing:** Automated tests MUST validate manifest schema compliance

### 4.2 Integration Testing
- **Observability:** End-to-end trace propagation tests
- **Security:** Certificate validation and credential flow tests
- **Event Flow:** Event schema validation in message flows
- **Plugin Lifecycle:** Complete plugin registration and activation tests

## 5. Migration Guidelines

### 5.1 From HMA v1.3 to v2.0
- **Impact:** Addition of mandatory dependencies, no breaking architectural changes
- **Timeline:** Can be implemented incrementally
- **Priority Order:**
  1. Security dependencies (TLS/mTLS)
  2. Observability standards (OTEL)
  3. Contract validation (JSON Schema/OpenAPI)
  4. Plugin manifest formalization
  5. Reference implementation adoption

### 5.2 Implementation Phases
- **Phase 1:** Core security and observability
- **Phase 2:** Contract validation and plugin standards
- **Phase 3:** Reference implementation adoption
- **Phase 4:** Advanced features (code signing, enhanced backends)

## 6. Plugin Manifest Schema Definition

### 6.1 Required Schema: plugin-manifest.json

```json
{
  "$schema": "https://hma-spec.org/schemas/v2.0/plugin-manifest.schema.json",
  "type": "object",
  "properties": {
    "manifestVersion": {
      "type": "string",
      "const": "2.0",
      "description": "HMA manifest schema version"
    },
    "hmaVersion": {
      "type": "string",
      "pattern": "^2\\.[0-9]+$",
      "description": "Compatible HMA specification version"
    },
    "plugin": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^[a-zA-Z][a-zA-Z0-9-]*[a-zA-Z0-9]$",
          "description": "Unique plugin identifier"
        },
        "name": {
          "type": "string",
          "description": "Human-readable plugin name"
        },
        "version": {
          "type": "string",
          "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$",
          "description": "Semantic version"
        },
        "type": {
          "type": "string",
          "enum": ["L2-Orchestrator", "L3-Capability"],
          "description": "Plugin type in HMA architecture"
        },
        "description": {
          "type": "string",
          "description": "Plugin functionality description"
        }
      },
      "required": ["id", "name", "version", "type"]
    },
    "interfaces": {
      "type": "object",
      "properties": {
        "implementedPorts": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": {"type": "string"},
              "version": {"type": "string"},
              "contract": {"type": "string"}
            },
            "required": ["name", "version"]
          },
          "description": "Ports this plugin implements"
        },
        "consumedPorts": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": {"type": "string"},
              "version": {"type": "string"},
              "required": {"type": "boolean", "default": true}
            },
            "required": ["name", "version"]
          },
          "description": "Core ports this plugin consumes"
        }
      }
    },
    "dependencies": {
      "type": "object",
      "properties": {
        "runtime": {
          "type": "object",
          "description": "Runtime dependencies and versions"
        },
        "infrastructure": {
          "type": "array",
          "items": {"type": "string"},
          "description": "Required L4 infrastructure"
        }
      }
    },
    "security": {
      "type": "object",
      "properties": {
        "signature": {
          "type": "object",
          "properties": {
            "algorithm": {"type": "string"},
            "keyId": {"type": "string"},
            "signature": {"type": "string"}
          },
          "description": "Digital signature information"
        },
        "permissions": {
          "type": "array",
          "items": {"type": "string"},
          "description": "Required security permissions"
        }
      }
    }
  },
  "required": ["manifestVersion", "hmaVersion", "plugin", "interfaces"]
}
```

### 6.2 Validation Requirements

- **Plugin Lifecycle Manager MUST validate all manifests against this schema**
- **Invalid manifests MUST result in plugin rejection**
- **Schema versioning MUST follow semantic versioning principles**
- **Backward compatibility MUST be maintained within major versions** 