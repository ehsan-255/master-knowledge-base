# Hexagonal Microkernel Architecture (HMA) Specification
_Version 2.2 (Guided Implementation Edition)_

**Part 1a: Mandatory Interoperability Standards**

This part defines the essential standards that MUST be implemented for HMA v2.2 compliance and ecosystem interoperability. These requirements ensure that HMA implementations can communicate effectively regardless of their internal technology choices, forming the foundation of the guided flexibility framework.

## 1. Mandatory Interoperability Standards

### 1.1 Boundary Compliance Requirements (MANDATORY)

These standards MUST be implemented at all external boundaries to ensure interoperability across the HMA ecosystem:

#### 1.1.1 External Port Contracts
- **Requirement Level:** MANDATORY  
- **Scope:** All external-facing Port interfaces
- **Technology:** JSON Schema validation
- **Purpose:** Ensures interoperability between different HMA implementations
- **Implementation:** All data crossing HMA boundaries MUST be validated against declared JSON Schema

#### 1.1.2 External API Documentation  
- **Requirement Level:** MANDATORY
- **Scope:** All L1 Adapter external APIs
- **Technology:** OpenAPI 3.0+ specifications
- **Purpose:** Standardized API documentation and validation
- **Implementation:** L1 Adapters MUST document APIs using OpenAPI specifications

#### 1.1.3 Event Schema Compliance
- **Requirement Level:** MANDATORY
- **Scope:** All events crossing HMA boundaries
- **Technology:** JSON Schema validation for event payloads
- **Purpose:** Enable cross-system event interoperability
- **Standard Format:**
```json
{
  "eventId": "uuid",
  "eventType": "string", 
  "eventVersion": "semver",
  "source": "component-id",
  "timestamp": "ISO8601",
  "data": { /* validated against schema */ }
}
```

### 1.2 Infrastructure Requirements (MANDATORY)

#### 1.2.1 Secure Secrets Storage Backend
- **Requirement Level:** MANDATORY (Type)
- **Scope:** CredentialBroker implementation
- **Purpose:** Secure credential storage and distribution
- **Implementation:** CredentialBroker MUST be backed by secure storage
- **Compliance:** Required for secure plugin-to-plugin communication

#### 1.2.2 Plugin Lifecycle Management
- **Requirement Level:** MANDATORY
- **Scope:** Plugin Lifecycle Manager, All Plugins
- **Purpose:** Standardized plugin metadata and lifecycle management
- **Implementation:** Plugin Lifecycle Manager MUST validate manifest.json files
- **Schema:** Defined in Section 3 of this document

### 1.3 Security Requirements (MANDATORY)

#### 1.3.1 Boundary Communication Security
- **External Traffic:** MANDATORY TLS 1.3+ for all L1 Adapter communication
- **Inter-Plugin:** MANDATORY mTLS for plugin-to-plugin communication via Core
- **Infrastructure:** MANDATORY secure credential access via CredentialBroker

#### 1.3.2 Input Validation Security
- **Port Boundaries:** MANDATORY JSON Schema validation at all Port boundaries
- **API Boundaries:** MANDATORY OpenAPI validation for all L1 Adapter APIs  
- **Event Boundaries:** MANDATORY event schema validation for Event Bus interactions

### 1.4 Observability Requirements (MANDATORY)

#### 1.4.1 Boundary Observability Standards
All HMA boundaries MUST emit standardized telemetry for ecosystem-wide observability:

**OpenTelemetry Integration for Interoperability:**
- **Scope:** External boundaries only
- **Requirements:**
  - Trace context propagation across plugin boundaries
  - Standard HMA resource attributes
  - Interoperable span and metric naming
- **Purpose:** Enable cross-system observability and monitoring

**Mandatory Resource Attributes:**
```yaml
hma_resource_attributes:
  required:
    - "hma.component.type: L2-Core | L2-Orchestrator | L3-Capability"
    - "hma.component.id: unique-identifier"
    - "hma.layer: L2 | L3"
    - "service.name: component-name"
    - "service.version: semantic-version"
```

**Boundary Telemetry Requirements:**
- External plugin invocations MUST emit OTEL spans with HMA conventions
- Cross-plugin communication MUST propagate trace context
- Boundary metrics MUST use standard HMA naming patterns  
- Error events at boundaries MUST be captured with OTEL

## 2. Compliance Testing Requirements

### 2.1 Mandatory Validation Tests
- **Boundary Validation:** Automated tests MUST verify JSON Schema compliance at all external interfaces
- **Security Testing:** Automated tests MUST verify mTLS/TLS implementation at boundaries
- **Observability Testing:** Automated tests MUST verify OTEL telemetry emission at boundaries
- **Plugin Lifecycle:** Automated tests MUST validate manifest schema compliance

### 2.2 Integration Testing Requirements
- **Interoperability Testing:** End-to-end tests MUST verify compatibility with standard HMA implementations
- **Event Flow Testing:** Event schema validation in cross-plugin message flows
- **Security Integration:** Certificate validation and credential flow tests
- **Observability Integration:** End-to-end trace propagation across plugin boundaries

### 2.3 Compliance Validation Framework

```python
class HMAComplianceValidator:
    """Validates HMA v2.2 mandatory compliance requirements"""
    
    def validate_boundary_compliance(self, component):
        """Validate all boundary compliance requirements"""
        results = ComplianceResults()
        
        # Mandatory: JSON Schema validation at boundaries
        results.add(self.validate_json_schema_boundaries(component))
        
        # Mandatory: OpenAPI documentation for L1 adapters  
        results.add(self.validate_openapi_documentation(component))
        
        # Mandatory: OTEL telemetry at boundaries
        results.add(self.validate_otel_boundary_telemetry(component))
        
        # Mandatory: Security implementation
        results.add(self.validate_boundary_security(component))
        
        return results
    
    def validate_plugin_compliance(self, plugin_manifest):
        """Validate plugin-specific compliance requirements"""
        results = ComplianceResults()
        
        # Mandatory: Plugin manifest schema compliance
        results.add(self.validate_manifest_schema(plugin_manifest))
        
        # Mandatory: Port contract definitions
        results.add(self.validate_port_contracts(plugin_manifest))
        
        # Mandatory: Security permissions alignment
        results.add(self.validate_security_permissions(plugin_manifest))
        
        return results
```

## 3. Plugin Manifest Schema Definition

### 3.1 Required Schema: plugin-manifest.json

All plugins MUST provide a manifest file conforming to this schema:

```json
{
  "$schema": "https://hma-spec.org/schemas/v2.2/plugin-manifest.schema.json",
  "type": "object",
  "properties": {
    "manifestVersion": {
      "type": "string",
      "const": "2.2",
      "description": "HMA manifest schema version"
    },
    "hmaVersion": {
      "type": "string", 
      "pattern": "^2\\.[2-9]$",
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
              "contract": {"type": "string"},
              "schema": {"type": "string"}
            },
            "required": ["name", "version", "schema"]
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
    "compliance": {
      "type": "object",
      "properties": {
        "hma_version": {
          "type": "string",
          "const": "2.2",
          "description": "HMA compliance version"
        },
        "mandatory_standards": {
          "type": "object",
          "properties": {
            "boundary_validation": {"type": "string", "const": "json_schema"},
            "boundary_observability": {"type": "string", "const": "opentelemetry"},
            "boundary_security": {"type": "string", "const": "mtls_tls"},
            "api_documentation": {"type": "string", "const": "openapi"}
          },
          "required": ["boundary_validation", "boundary_observability", "boundary_security"]
        },
        "technology_tier": {
          "type": "string",
          "enum": ["recommended", "alternative"],
          "description": "Technology tier used by this plugin"
        }
      },
      "required": ["hma_version", "mandatory_standards"]
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
        "permissions": {
          "type": "array",
          "items": {"type": "string"},
          "description": "Required security permissions"
        },
        "trust_level": {
          "type": "string",
          "enum": ["trusted", "sandboxed", "isolated"],
          "description": "Plugin trust and isolation level"
        }
      }
    }
  },
  "required": ["manifestVersion", "hmaVersion", "plugin", "interfaces", "compliance"]
}
```

### 3.2 Validation Requirements

- **Plugin Lifecycle Manager MUST validate all manifests against this schema**
- **Invalid manifests MUST result in plugin rejection**
- **Schema versioning MUST follow semantic versioning principles**
- **Backward compatibility MUST be maintained within major versions**

### 3.3 Compliance Verification

```python
class PluginManifestValidator:
    """Validates plugin manifests against HMA v2.2 requirements"""
    
    def validate_manifest(self, manifest_path):
        """Validate plugin manifest for HMA v2.2 compliance"""
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        # Mandatory: Schema validation
        schema_result = self.validate_against_schema(manifest)
        if not schema_result.valid:
            raise ManifestValidationError(schema_result.errors)
        
        # Mandatory: Compliance requirements
        compliance_result = self.validate_compliance_section(manifest)
        if not compliance_result.valid:
            raise ComplianceValidationError(compliance_result.errors)
        
        # Mandatory: Port contract validation
        ports_result = self.validate_port_contracts(manifest)
        if not ports_result.valid:
            raise PortValidationError(ports_result.errors)
        
        return ValidationResult.VALID
```

## 4. Migration and Enforcement

### 4.1 Migration from Previous Versions

**From HMA v2.0/v2.1 to v2.2:**
- **Impact:** Addition of technology tier classification, no breaking architectural changes
- **Timeline:** Can be implemented incrementally
- **Priority Order:**
  1. Update plugin manifests to v2.2 schema
  2. Ensure boundary compliance validation
  3. Classify technology choices as recommended/alternative
  4. Document any alternative technology usage

### 4.2 Enforcement Mechanisms

- **Static Analysis:** hma-lint tools MUST validate manifest compliance
- **Runtime Validation:** Plugin Lifecycle Manager MUST enforce schema validation
- **Continuous Integration:** CI/CD pipelines SHOULD include HMA compliance tests
- **Ecosystem Monitoring:** Observability systems SHOULD track compliance metrics

### 4.3 Compliance Exceptions

**Emergency Override Process:**
- Critical security fixes MAY temporarily bypass non-security compliance requirements
- Emergency overrides MUST be documented and time-limited
- Post-emergency compliance restoration MUST be tracked and enforced

**Community Review Process:**
- Proposed changes to mandatory standards MUST undergo community review
- Breaking changes require major version increment and migration guide
- Community feedback MUST be incorporated before finalization

---

**All mandatory compliance failures MUST be logged via the ObservabilityPort and trigger appropriate alerts in monitoring systems.**