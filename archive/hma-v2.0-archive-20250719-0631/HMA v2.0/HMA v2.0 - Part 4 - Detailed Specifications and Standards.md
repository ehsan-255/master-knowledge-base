# Hexagonal Microkernel Architecture (HMA) Specification

_Version 2.0 (Mandatory Dependencies Edition)_

**(Companion document to the AI-Powered Model-Driven Development (APMDD) Methodology v2.0)**

---

**Part 4: HMA Detailed Specifications, Standards, & Implementation Guidance (Analogous to C4 Level 4 - Code/Classes)**

This part provides the detailed technical specifications that govern HMA implementations. It defines the precise rules for Port design, Event schemas, naming conventions, and validation requirements.

## 12. Port & API Design Standards

### 12.1 Interface Contract Rules

All Port contracts MUST be defined using formal specifications that include:
- Clear operation signatures
- Input/output parameter definitions
- Error condition specifications
- Version compatibility requirements

### 12.2 Versioning Strategies

Port contracts MUST follow semantic versioning principles:
- Major version changes for breaking changes
- Minor version changes for backward-compatible additions
- Patch version changes for backward-compatible fixes

### 12.3 Mandatory Validation Requirements (NEW in v2.0)

All HMA v2.0 implementations MUST include automated validation for:

#### **Contract Validation**
*   **JSON Schema Libraries:** Implementations MUST use JSON Schema validation libraries for:
    *   All Port operation parameters and return types
    *   All Event payload validation
    *   Plugin manifest validation
    *   Configuration parameter validation
*   **OpenAPI Validation:** L1 Adapters MUST validate all external API interactions against OpenAPI 3.0+ specifications
*   **Real-time Validation:** Validation MUST occur at runtime for all boundary crossings

#### **Schema Management**
*   **Version Control:** All schemas MUST be versioned using semantic versioning
*   **Registry:** Organizations SHOULD maintain a schema registry for centralized management
*   **Backward Compatibility:** Schema changes MUST maintain backward compatibility within major versions

#### **Implementation Libraries**
Recommended open-source libraries for implementation:
*   **JSON Schema:** Ajv (JavaScript), jsonschema (Python), JSON Schema Validator (Java)
*   **OpenAPI:** OpenAPI Generator, Swagger tools, Spectral for validation
*   **Schema Registry:** Confluent Schema Registry (Apache License), Apicurio Registry

## 13. Event Design & Schema Standards

### 13.1 Event Payload Structure and Schemas

All events MUST follow a standardized structure:
```json
{
  "eventId": "uuid",
  "eventType": "string",
  "eventVersion": "semver",
  "source": "component-id",
  "timestamp": "ISO8601",
  "data": { /* event-specific payload */ }
}
```

### 13.2 Standard Event Metadata

Mandatory metadata fields for all events:
- `eventId`: Unique identifier for the event
- `eventType`: Categorization of the event
- `eventVersion`: Schema version of the event
- `source`: Identifier of the component that generated the event
- `timestamp`: When the event occurred

### 13.3 Event Versioning

Events MUST follow semantic versioning for their schemas to ensure compatibility.

### 13.4 Mandatory Event Validation (NEW in v2.0)

#### **Schema Enforcement**
*   **Required Validation:** All events MUST be validated against their declared schemas before publication
*   **Metadata Validation:** Standard event metadata fields are MANDATORY and MUST be validated
*   **Consumer Validation:** Event consumers SHOULD validate received events against expected schemas

#### **Implementation Requirements**
```json
{
  "eventValidation": {
    "schemaValidation": "MANDATORY",
    "metadataValidation": "MANDATORY", 
    "consumerValidation": "HIGHLY_RECOMMENDED",
    "failureHandling": "REJECT_INVALID_EVENTS"
  }
}
```

#### **Error Handling**

- **Invalid Events:** MUST be rejected at publication time
- **Schema Mismatches:** MUST log errors and alert monitoring systems
- **Fallback Behavior:** Define graceful degradation for schema validation failures

## 14. HMA Naming Conventions

### 14.1 Component Naming
- L2 Core components: `Core{ComponentName}`
- L3 Capability Plugins: `{DomainName}Plugin`
- L2 Orchestrator Plugins: `{WorkflowName}Orchestrator`

### 14.2 Port Naming
- Inbound Ports: `{CapabilityName}Port`
- Outbound Ports: `{TargetService}Port`
- Standard Core Ports: `PluginExecutionPort`, `EventBusPort`, `ObservabilityPort`

### 14.3 Event Naming
- Event Types: `{Domain}.{Action}.{Version}` (e.g., `user.created.v1`)
- Event Schemas: `{EventType}Schema` (e.g., `UserCreatedV1Schema`)

## 15. Rule Syntax (RFC 2119)

This specification uses RFC 2119 terminology:
- **MUST/REQUIRED/SHALL:** Absolute requirement
- **MUST NOT/SHALL NOT:** Absolute prohibition
- **SHOULD/RECOMMENDED:** Strong recommendation
- **SHOULD NOT/NOT RECOMMENDED:** Strong discouragement
- **MAY/OPTIONAL:** Truly optional behavior

**NEW in v2.0:** All mandatory dependencies defined in [[HMA v2.0 - Part 1a - Mandatory Dependencies and Standards]] use MUST/REQUIRED terminology and are non-negotiable for compliance. 