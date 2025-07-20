# HMA v2.0 Fact Sheet

Quick reference guide for the Hexagonal Microkernel Architecture (HMA) specification.

## Hexagonal Microkernel Architecture (HMA) v2.0

**Definition:** The mandated architectural pattern for systems developed under APMDD v2.0. HMA v2.0 provides a framework for building AI-augmented platforms with enhanced standards for interoperability, security, and observability.

**NEW in v2.0: Mandatory Dependencies & Standards**
- OpenTelemetry SDK requirement for all components
- mTLS/TLS libraries for secure communication
- JSON Schema/OpenAPI validation for contract enforcement
- Plugin manifest schema formalization
- Secure secrets backend requirements

**Cross-reference:** For detailed dependency requirements, see [[HMA v2.0 - Part 1a - Mandatory Dependencies and Standards]].

---

## Core Architectural Elements

### Layers (L0-L4)
- **L0:** External Actors (users, systems, AI agents)
- **L1:** Interface Layer (REST APIs, event listeners, adapters)
- **L2:** Microkernel Core + L2 Orchestrator Plugins + L2.5 Instrumentation
- **L3:** Capability Plugins (business logic, domain functionality)
- **L4:** Infrastructure (databases, message brokers, external systems)

### Key Components

**Microkernel Core (L2):**
- Request Router/Dispatcher
- Plugin Lifecycle Manager
- Control Plane Services (CredentialBroker, EventBus, Observability)

**Plugins:**
- **L3 Capability Plugins:** Encapsulate specific business functions
- **L2 Orchestrator Plugins:** Coordinate complex multi-plugin workflows

**Ports & Adapters:**
- **Ports:** Technology-agnostic interfaces
- **Adapters:** Technology-specific implementations
- **NEW v2.0:** All ports MUST use JSON Schema validation

### Standard Ports
- `PluginExecutionPort`: Plugin invocation interface
- `CredBrokerQueryPort`: Secure credential access
- `EventBusPort`: Asynchronous messaging
- `ObservabilityPort`: Telemetry and monitoring

---

## HMA v2.0 Mandatory Dependencies

**Definition:** Essential libraries, standards, and tools required for HMA v2.0 compliance.

**Core Categories:**
- **Observability:** OpenTelemetry SDK (MANDATORY)
- **Security:** mTLS/TLS libraries (MANDATORY)
- **Validation:** JSON Schema/OpenAPI libraries (MANDATORY)
- **Plugin System:** Manifest schema validation (MANDATORY)
- **Infrastructure:** Secure secrets storage backend (MANDATORY)

**Purpose:** Ensure consistency, interoperability, and security across all HMA implementations while preserving architectural flexibility.

---

## Key Principles

1. **Maximal Plugin Autonomy:** Independent development and deployment
2. **Explicit Boundaries:** All interactions via Ports or Events
3. **Minimal Core:** Router, lifecycle manager, control plane only
4. **Replaceable Orchestration:** Complex workflows in dedicated plugins
5. **Governed Extensibility:** Managed plugin lifecycle with validation
6. **Comprehensive Observability:** Built-in monitoring and tracing
7. **Security by Design:** Trust boundaries and secure communication
8. **Context Management:** Architectural structure limits AI context needs
9. **NEW v2.0: Standards-Based Interoperability:** Mandatory compliance ensures integration

---

## Implementation Compliance

### Must Have (MANDATORY)
- OpenTelemetry SDK integration
- mTLS/TLS for secure communication
- JSON Schema validation for contracts
- Plugin manifest schema compliance
- Secure secrets storage backend

### Should Have (HIGHLY RECOMMENDED)
- W3C Trace Context standard
- Code signing for plugins
- Prometheus-compatible metrics
- Reference implementation stack

### May Have (OPTIONAL)
- Custom telemetry extensions
- Additional authentication layers
- Custom validation mechanisms

---

## Plugin Requirements (NEW in v2.0)

### Mandatory Plugin Manifest (plugin-manifest.json)
Required fields:
- `manifestVersion`: "2.0"
- `hmaVersion`: Compatible HMA version
- `plugin`: Metadata (id, name, version, type)
- `interfaces`: Port declarations

### Technical Compliance
- OTEL SDK integration for telemetry
- JSON Schema validation for all data
- mTLS for internal communication
- Secure credential access via CredentialBroker

---

## Reference Implementation Stack

**Observability:**
- Metrics: Prometheus + Grafana
- Tracing: Jaeger
- Logging: Loki + Grafana

**Event Bus (if using EDA):**
- High Performance: NATS
- High Scale: Apache Kafka
- Feature Rich: RabbitMQ

**Secure Storage:**
- HashiCorp Vault OSS
- External Secrets Operator
- Cloud-native secret stores

---

## Migration from v1.3 to v2.0

**Impact:** Additive enhancements, no breaking architectural changes

**Priority Order:**
1. Security dependencies (TLS/mTLS)
2. Observability standards (OTEL)
3. Contract validation (JSON Schema/OpenAPI)
4. Plugin manifest formalization
5. Reference implementation adoption

**Timeline:** Can be implemented incrementally over multiple phases

---

## Benefits of v2.0 Enhancements

**Interoperability:** Common standards enable cross-team integration
**Observability:** OTEL ensures consistent monitoring capabilities
**Security:** Enhanced controls provide enterprise-grade protection
**Validation:** Contract enforcement prevents integration failures
**Maintainability:** Standardized plugin lifecycle management

HMA v2.0 transforms the architecture from a framework to a complete implementation standard while preserving the flexibility that makes HMA valuable for AI-driven development. 