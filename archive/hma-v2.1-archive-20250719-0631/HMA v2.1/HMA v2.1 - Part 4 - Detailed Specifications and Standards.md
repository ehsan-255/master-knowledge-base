# Hexagonal Microkernel Architecture (HMA) Specification

_Version 2.1 (Flexible Implementation Edition)_

**(Companion document to the AI-Powered Model-Driven Development (APMDD) Methodology v2.1)**

---

**Part 4: HMA Detailed Specifications, Standards, & Implementation Guidance (Analogous to C4 Level 4 - Code/Classes)**

This part provides the detailed technical specifications that govern HMA implementations with enhanced flexibility. It defines the precise rules for Port design, Event schemas, naming conventions, and the revolutionary flexible validation framework that enables innovation while maintaining interoperability.

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

### 12.3 Flexible Validation Framework (ENHANCED in v2.1)

#### 12.3.1 Boundary Validation Requirements (MANDATORY)

All external HMA boundaries MUST implement JSON Schema validation:

**External Port Contracts:**
```json
{
  "boundary_validation": {
    "scope": "external_ports_only",
    "technology": "json_schema",
    "requirement": "MANDATORY",
    "purpose": "interoperability"
  }
}
```

**Implementation Requirements:**

- L1 Adapters MUST validate all incoming data against OpenAPI specifications
- Core MUST validate all plugin invocations against PluginExecutionPort schema
- Plugins MUST validate external responses against declared output schemas

#### 12.3.2 Internal Validation Flexibility (OPTIONAL)

Components MAY use alternative validation technologies internally:

**Semantic Data Validation:**

```python
# Example: SHACL for semantic validation
class SemanticValidator:
    def validate_pdp_semantics(self, json_ld_data):
        rdf_graph = self.convert_to_rdf(json_ld_data)
        return self.shacl_engine.validate(rdf_graph, self.shapes_graph)
```

**High-Performance Validation:**

```python
# Example: Protocol Buffers for performance
class PerformanceValidator:
    def validate_high_frequency_data(self, proto_data):
        return self.protobuf_validator.validate(proto_data)
```

**Domain-Specific Validation:**

```python
# Example: Financial constraints
class FinancialValidator:
    def validate_trading_rules(self, transaction_data):
        return self.domain_rule_engine.validate(transaction_data)
```

#### 12.3.3 Hybrid Validation Pattern (RECOMMENDED)

**Validation Adapter Implementation:**

```python
class HMAValidationAdapter:
    """
    Recommended pattern for combining boundary compliance 
    with internal innovation
    """
    
    def __init__(self, internal_validator=None):
        # MANDATORY: Boundary compliance
        self.boundary_validator = JSONSchemaValidator()
        
        # OPTIONAL: Internal optimization
        self.internal_validator = internal_validator
        
    def validate_external_contract(self, data, schema):
        """MANDATORY: Validate all external boundaries"""
        result = self.boundary_validator.validate(data, schema)
        if not result.valid:
            raise HMAComplianceError(result.errors)
        return result
        
    def validate_internal_semantics(self, data):
        """OPTIONAL: Additional internal validation"""
        if self.internal_validator:
            return self.internal_validator.validate(data)
        return ValidationResult.VALID
        
    def full_validation(self, data, external_schema):
        """Complete validation workflow"""
        # 1. Ensure HMA compliance
        boundary_result = self.validate_external_contract(data, external_schema)
        
        # 2. Perform internal semantic validation
        semantic_result = self.validate_internal_semantics(data)
        
        return CombinedValidationResult(boundary_result, semantic_result)
```

#### 12.3.4 Technology Selection Guidelines

**Selection Criteria:**

```yaml
technology_selection:
  semantic_systems:
    recommended: ["SHACL", "OWL", "SPARQL"]
    use_case: "RDF graphs, ontologies, knowledge graphs"
    example: "AOS v5.0 Project Digital Twins"
    
  high_performance:
    recommended: ["Protocol Buffers", "MessagePack", "FlatBuffers"]
    use_case: "Low latency, high throughput systems"
    example: "Real-time trading systems"
    
  ai_ml_systems:
    recommended: ["TensorFlow Data Validation", "Great Expectations", "Custom ML"]
    use_case: "ML pipelines, data quality, model validation"
    example: "ML feature validation"
    
  financial_systems:
    recommended: ["IBAN validators", "Currency validators", "Regulatory compliance"]
    use_case: "Financial data, regulatory requirements"
    example: "Payment processing systems"
```

#### 12.3.5 Migration and Fallback Strategies

**Fallback Requirements:** Every internal validation technology MUST provide:

1. **Conversion to JSON Schema**: For emergency fallback
2. **Error Mapping**: Translate internal errors to HMA-compliant errors
3. **Documentation**: Clear migration path to baseline technology
4. **Testing**: Compatibility tests with baseline validation

**Example Fallback Implementation:**

```python
class SHACLToJSONSchemaAdapter:
    """Fallback adapter for SHACL validation"""
    
    def convert_shacl_to_json_schema(self, shacl_shapes):
        """Convert SHACL shapes to equivalent JSON Schema"""
        # Implementation that extracts structural constraints
        # from SHACL and creates equivalent JSON Schema
        pass
        
    def create_fallback_validator(self):
        """Create JSON Schema fallback for SHACL validation"""
        json_schema = self.convert_shacl_to_json_schema(self.shacl_shapes)
        return JSONSchemaValidator(json_schema)
```

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

### 13.4 Flexible Event Validation Framework (ENHANCED in v2.1)

#### 13.4.1 Event Boundary Standards (MANDATORY)

All events crossing HMA boundaries MUST be validated against JSON Schema:

**Standard Event Metadata Validation:**
```json
{
  "event_metadata_schema": {
    "type": "object",
    "properties": {
      "eventId": {"type": "string", "format": "uuid"},
      "eventType": {"type": "string"},
      "eventVersion": {"type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$"},
      "source": {"type": "string"},
      "timestamp": {"type": "string", "format": "date-time"}
    },
    "required": ["eventId", "eventType", "eventVersion", "source", "timestamp"],
    "additionalProperties": false
  }
}
```

#### 13.4.2 Internal Event Processing Flexibility (OPTIONAL)

Components MAY use alternative event processing internally:

**Event Sourcing Pattern:**

```python
class EventSourcingProcessor:
    """Internal event sourcing with HMA boundary compliance"""
    
    def process_internal_event(self, domain_event):
        # Internal: Use domain-specific event processing
        return self.event_store.append(domain_event)
        
    def emit_hma_compliant_event(self, domain_event):
        # External: Convert to HMA-compliant format
        hma_event = self.convert_to_hma_format(domain_event)
        self.validate_boundary_compliance(hma_event)
        return self.event_bus.publish(hma_event)
```

**CQRS Pattern:**

```python
class CQRSEventProcessor:
    """Command-Query separation with HMA compliance"""
    
    def handle_command_internally(self, command):
        # Internal: Domain-specific command handling
        events = self.command_handler.handle(command)
        return self.apply_events_to_aggregate(events)
        
    def project_to_hma_events(self, domain_events):
        # External: Project to HMA-compliant events
        hma_events = [self.convert_to_hma(event) for event in domain_events]
        for event in hma_events:
            self.validate_event_schema(event)
        return hma_events
```

#### 13.4.3 Event Architecture Patterns

**Flexible Event Processing:**

```yaml
event_patterns:
  message_broker:
    description: "Traditional pub-sub with message broker"
    hma_compliance: "Standard EventBusPort implementation"
    internal_freedom: "Custom message routing, filtering"
    
  event_sourcing:
    description: "Event store with domain events"
    hma_compliance: "Project domain events to HMA format"
    internal_freedom: "Domain-specific event storage, replay"
    
  cqrs:
    description: "Command-query separation"
    hma_compliance: "Emit read model changes as HMA events"
    internal_freedom: "Custom command handling, projections"
    
  reactive_streams:
    description: "Streaming event processing"
    hma_compliance: "Batch stream events to HMA format"
    internal_freedom: "Real-time stream processing, backpressure"
```

#### 13.4.4 Event Validation Compliance Strategy

```python
class FlexibleEventValidator:
    """Event validation with boundary compliance and internal flexibility"""
    
    def __init__(self):
        # MANDATORY: HMA boundary compliance
        self.hma_event_validator = JSONSchemaValidator(hma_event_schema)
        
        # OPTIONAL: Internal event processing
        self.internal_event_processor = self._choose_event_pattern()
    
    def validate_boundary_event(self, event):
        """MANDATORY: Validate events crossing HMA boundaries"""
        result = self.hma_event_validator.validate(event)
        if not result.valid:
            raise EventComplianceError(result.errors)
        return result
    
    def process_internal_event(self, event):
        """OPTIONAL: Process events with internal patterns"""
        return self.internal_event_processor.process(event)
    
    def emit_compliant_event(self, internal_event):
        """Convert internal event to HMA-compliant format"""
        hma_event = self.convert_to_hma_format(internal_event)
        self.validate_boundary_event(hma_event)
        return hma_event
```

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

**ENHANCED in v2.1:** All boundary standards defined in [[HMA v2.1 - Part 1a - Boundary Standards and Implementation Flexibility]] use MUST/REQUIRED terminology for external interfaces, while internal implementations MAY use alternative technologies with appropriate compliance adapters. 