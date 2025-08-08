# Hexagonal Microkernel Architecture (HMA) Specification
_Version 2.1 (Flexible Implementation Edition)_

**Part 1a: Boundary Standards and Implementation Flexibility**

This part defines the revolutionary "Boundary vs Implementation" framework that distinguishes between mandatory boundary standards for interoperability and optional implementation choices for optimization. This approach resolves the rigidity issues of v2.0 while preserving all ecosystem benefits.

## 1. Boundary Standards vs Implementation Flexibility

### 1.1 Boundary Compliance Requirements (MANDATORY)

These standards MUST be implemented at all external boundaries to ensure interoperability:

#### External Port Contracts
- **Requirement Level:** MANDATORY
- **Scope:** All external-facing Port interfaces
- **Technology:** JSON Schema validation
- **Purpose:** Ensures interoperability between different HMA implementations
- **Internal Alternative:** Components MAY use additional validation internally

#### External API Documentation  
- **Requirement Level:** MANDATORY
- **Scope:** All L1 Adapter external APIs
- **Technology:** OpenAPI 3.0+ specifications
- **Purpose:** Standardized API documentation and validation
- **Internal Alternative:** Internal APIs MAY use alternative documentation

#### Boundary Observability
- **Requirement Level:** MANDATORY
- **Scope:** All external communication points
- **Technology:** OpenTelemetry SDK for telemetry emission
- **Purpose:** Enable cross-system observability and troubleshooting
- **Internal Alternative:** Components MAY use additional telemetry systems internally

#### Boundary Security
- **Requirement Level:** MANDATORY
- **Scope:** All external communication channels
- **Technology:** mTLS for plugin-to-plugin, TLS 1.3+ for external traffic
- **Purpose:** Secure communication and authentication
- **Internal Alternative:** Internal systems MAY use service mesh or zero-trust models

### 1.2 Implementation Flexibility Zones (OPTIONAL)

These areas allow technology choice based on domain requirements:

#### Internal Validation Technologies
- **Requirement Level:** OPTIONAL
- **Scope:** Internal plugin validation, business logic constraints
- **Technology Options:** 
  - SHACL for semantic/RDF data
  - Protocol Buffers for high performance
  - Custom validators for domain-specific needs
  - ML-based validation for AI systems
- **Constraint:** Must not affect external contract compliance

#### Internal Communication Protocols
- **Requirement Level:** OPTIONAL  
- **Scope:** Plugin-internal communication, microservice coordination
- **Technology Options:**
  - gRPC streaming for real-time data
  - GraphQL for flexible querying
  - WebSockets for bidirectional communication
  - Custom protocols for specialized needs
- **Constraint:** External interfaces must remain HMA-compliant

#### Internal Observability Systems
- **Requirement Level:** OPTIONAL
- **Scope:** Internal monitoring, metrics, and diagnostics
- **Technology Options:**
  - High-performance custom telemetry
  - Domain-specific metrics (financial, AI/ML, IoT)
  - Specialized monitoring for latency-sensitive systems
  - Business intelligence integration
- **Constraint:** Must emit OTEL telemetry at boundaries

#### Internal Security Models
- **Requirement Level:** OPTIONAL
- **Scope:** Internal authentication, authorization, encryption
- **Technology Options:**
  - Service mesh security (Istio, Linkerd)
  - Zero-trust architectures
  - Hardware security modules (HSMs)
  - Custom encryption for sensitive domains
- **Constraint:** External boundaries must use standard mTLS/TLS

### 1.3 Hybrid Implementation Pattern (RECOMMENDED)

The recommended approach combines boundary compliance with internal innovation:

```python
class FlexibleHMAComponent:
    def __init__(self):
        # MANDATORY: External boundary compliance
        self.external_validator = JSONSchemaValidator()
        self.boundary_tracer = OTELTracer("hma-boundary")
        self.mtls_client = MTLSClient()
        
        # OPTIONAL: Internal optimization
        self.internal_validator = self._choose_optimal_validator()
        self.internal_tracer = self._choose_optimal_tracer()
        self.internal_client = self._choose_optimal_client()
    
    def _choose_optimal_validator(self):
        if self.domain == "semantic":
            return SHACLValidator()
        elif self.domain == "high_performance":
            return ProtocolBufferValidator()
        elif self.domain == "ai_ml":
            return MLBasedValidator()
        else:
            return self.external_validator
    
    def validate_at_boundary(self, data):
        # MANDATORY: Always validate external contracts
        return self.external_validator.validate(data)
    
    def validate_internally(self, data):
        # OPTIONAL: Use optimal internal validation
        return self.internal_validator.validate(data)
    
    def process_external_request(self, request):
        # MANDATORY: Boundary compliance
        with self.boundary_tracer.start_span("hma.external.request"):
            validated_request = self.validate_at_boundary(request)
            
            # OPTIONAL: Internal processing optimization
            with self.internal_tracer.start_span("internal.processing"):
                result = self.process_with_internal_tools(validated_request)
            
            # MANDATORY: Ensure compliant response
            validated_response = self.validate_at_boundary(result)
            return validated_response
```

### 1.4 Technology Evaluation Framework

### Criteria for Internal Technology Adoption
1. **Performance**: Does it perform better than the baseline?
2. **Domain Fit**: Is it appropriate for the specific domain?
3. **Maintainability**: Can the team effectively maintain it?
4. **Migration Path**: Can it fall back to baseline if needed?
5. **Compliance**: Does it maintain external boundary compliance?

### Innovation Documentation Requirements
Components using non-baseline technologies MUST document:
- **Technology Choice Rationale**: Why this technology was chosen
- **Performance Benefits**: Measurable improvements over baseline
- **Compliance Strategy**: How boundary compliance is maintained
- **Fallback Plan**: How to migrate back to baseline if needed

## 1.5 Future Technology Integration

### Evolution Mechanism
New technologies can be integrated through:
1. **Proof of Concept**: Demonstrate benefits in Innovation Zones
2. **Community Validation**: Gather feedback from HMA community
3. **Standard Evaluation**: Assess for inclusion in future HMA versions
4. **Migration Support**: Provide pathways for ecosystem adoption

### Technology Watch List
Emerging technologies under evaluation:
- **Validation**: JSON Schema alternatives, ML-based validation
- **Communication**: gRPC, GraphQL, Event Sourcing patterns
- **Security**: Zero-trust architectures, service mesh security
- **Observability**: Custom metrics, domain-specific telemetry

## 2. Domain-Specific Implementation Patterns

### 2.1 Semantic Systems Pattern
**Use Case**: Knowledge graphs, ontologies, RDF-based systems (e.g., AOS v5.0)

**Boundary Compliance**:
- External contracts validated with JSON Schema
- OTEL telemetry for external observability
- Standard mTLS for external communication

**Internal Innovation**:
- SHACL for semantic validation of RDF graphs
- SPARQL for internal querying
- OWL for ontology reasoning
- Custom RDF serialization for performance

**Implementation Example**:
```python
class SemanticSystemPlugin:
    def __init__(self):
        # MANDATORY: Boundary compliance
        self.boundary_validator = JSONSchemaValidator()
        self.otel_tracer = OTELTracer()
        
        # OPTIONAL: Semantic optimization
        self.shacl_validator = SHACLValidator()
        self.sparql_engine = SPARQLEngine()
        self.rdf_store = RDFTripleStore()
    
    def execute_hma_request(self, request):
        # MANDATORY: Validate HMA contract
        self.boundary_validator.validate(request)
        
        with self.otel_tracer.start_span("semantic.processing"):
            # OPTIONAL: Convert to RDF for internal processing
            rdf_data = self.json_ld_to_rdf(request.data)
            
            # OPTIONAL: Validate semantics with SHACL
            self.shacl_validator.validate(rdf_data)
            
            # OPTIONAL: Process with SPARQL
            result_rdf = self.sparql_engine.query(rdf_data, request.query)
            
            # MANDATORY: Convert back to HMA-compliant format
            json_result = self.rdf_to_json_ld(result_rdf)
            
        # MANDATORY: Validate response compliance
        self.boundary_validator.validate(json_result)
        return json_result
```

### 2.2 High-Performance Systems Pattern
**Use Case**: Trading systems, real-time analytics, low-latency processing

**Boundary Compliance**:
- JSON Schema validation for external APIs
- OTEL telemetry emission at boundaries
- Standard HMA port implementations

**Internal Innovation**:
- Protocol Buffers for high-speed serialization
- Custom memory pools and allocators
- Optimized networking libraries
- Hardware-specific optimizations

**Implementation Example**:
```python
class HighPerformancePlugin:
    def __init__(self):
        # MANDATORY: Standard HMA interface
        self.hma_interface = StandardPluginExecutionPort()
        self.boundary_tracer = OTELTracer()
        
        # OPTIONAL: Performance optimization
        self.protobuf_serializer = ProtocolBufferSerializer()
        self.fast_validator = CompiledValidator()
        self.memory_pool = OptimizedMemoryPool()
    
    def execute_hma_request(self, request):
        # MANDATORY: Standard HMA processing
        with self.boundary_tracer.start_span("hma.request"):
            # OPTIONAL: Convert to high-performance format
            proto_request = self.protobuf_serializer.serialize(request)
            
            # OPTIONAL: Use optimized processing
            with self.memory_pool.get_buffer() as buffer:
                result = self.process_high_speed(proto_request, buffer)
            
            # MANDATORY: Convert back to HMA format
            hma_result = self.protobuf_serializer.deserialize(result)
            
        return hma_result
```

### 2.3 AI/ML Systems Pattern
**Use Case**: Machine learning pipelines, model inference, data science workflows

**Boundary Compliance**:
- Standard observability for model performance
- JSON Schema for feature and prediction contracts
- Standard plugin lifecycle management

**Internal Innovation**:
- ML-based validation and data quality checks
- Custom metrics for model drift and performance
- Specialized feature stores and model registries
- GPU-accelerated processing

**Implementation Example**:
```python
class AIMLPlugin:
    def __init__(self):
        # MANDATORY: HMA compliance
        self.hma_validator = JSONSchemaValidator()
        self.otel_tracer = OTELTracer()
        
        # OPTIONAL: ML-specific tools
        self.ml_validator = TensorFlowDataValidation()
        self.model_registry = MLModelRegistry()
        self.feature_store = FeatureStore()
        self.drift_detector = ModelDriftDetector()
    
    def execute_hma_request(self, request):
        # MANDATORY: Validate HMA contract
        self.hma_validator.validate(request)
        
        with self.otel_tracer.start_span("ml.inference"):
            # OPTIONAL: ML-specific validation
            features = self.feature_store.get_features(request.feature_ids)
            self.ml_validator.validate_features(features)
            
            # OPTIONAL: Model inference with drift detection
            model = self.model_registry.get_model(request.model_id)
            prediction = model.predict(features)
            self.drift_detector.check_drift(features, prediction)
            
            # OPTIONAL: Custom ML metrics
            self.record_ml_metrics(model.id, prediction.confidence)
            
        # MANDATORY: Return HMA-compliant result
        result = {"prediction": prediction.value, "confidence": prediction.confidence}
        self.hma_validator.validate(result)
        return result
```

### 2.4 Financial Systems Pattern
**Use Case**: Payment processing, trading platforms, regulatory compliance

**Boundary Compliance**:
- Standard security (mTLS, credential management)
- Regulatory audit trails via OTEL
- JSON Schema for financial data contracts

**Internal Innovation**:
- Domain-specific validation (IBAN, currency codes)
- Regulatory compliance engines
- Real-time risk management
- Encrypted data processing

**Implementation Example**:
```python
class FinancialPlugin:
    def __init__(self):
        # MANDATORY: HMA security compliance
        self.credential_broker = CredentialBrokerPort()
        self.mtls_client = MTLSClient()
        self.audit_tracer = OTELTracer()
        
        # OPTIONAL: Financial domain tools
        self.iban_validator = IBANValidator()
        self.compliance_engine = RegulatoryComplianceEngine()
        self.risk_engine = RealTimeRiskEngine()
        self.encrypted_processor = EncryptedDataProcessor()
    
    def execute_hma_request(self, request):
        # MANDATORY: Secure credential access
        credentials = self.credential_broker.get_credentials("financial-api")
        
        with self.audit_tracer.start_span("financial.transaction") as span:
            # MANDATORY: Audit trail for compliance
            span.set_attribute("transaction.id", request.transaction_id)
            span.set_attribute("amount", request.amount)
            
            # OPTIONAL: Financial domain validation
            self.iban_validator.validate(request.account_number)
            
            # OPTIONAL: Real-time risk assessment
            risk_score = self.risk_engine.assess_risk(request)
            if risk_score > self.risk_threshold:
                raise RiskLimitExceeded(risk_score)
            
            # OPTIONAL: Regulatory compliance check
            self.compliance_engine.verify_transaction(request)
            
            # OPTIONAL: Encrypted processing
            result = self.encrypted_processor.process_payment(request, credentials)
            
        return result
```

## 3. Implementation Compliance Matrix

| **Technology Category** | **Boundary (MUST)** | **Internal (MAY)** | **Compliance Adapter Required** |
|------------------------|---------------------|-------------------|--------------------------------|
| **Validation** | JSON Schema | SHACL, Protocol Buffers, ML validation | Yes, if non-JSON Schema |
| **Observability** | OTEL at boundaries | Custom telemetry, domain metrics | Yes, if non-OTEL internal |
| **Communication** | Standard HMA ports | gRPC, GraphQL, WebSockets | Yes, if additional protocols |
| **Security** | mTLS/TLS | Service mesh, zero-trust | Yes, if non-mTLS internal |
| **Data Processing** | HMA-compliant APIs | Custom serialization, optimization | No, if boundary compliance maintained |

## 4. Validation & Testing Requirements

### 4.1 Compliance Testing
- **Boundary Validation**: Automated tests MUST verify JSON Schema compliance at all external interfaces
- **Security Testing**: Automated tests MUST verify mTLS/TLS implementation at boundaries
- **Observability Testing**: Automated tests MUST verify OTEL telemetry emission at boundaries
- **Integration Testing**: End-to-end tests MUST verify interoperability with standard HMA implementations

### 4.2 Innovation Testing
- **Performance Testing**: Document performance improvements from internal innovations
- **Compatibility Testing**: Verify that internal innovations don't break boundary compliance
- **Fallback Testing**: Ensure graceful degradation to baseline technologies
- **Adapter Testing**: Validate compliance adapters function correctly

## 5. Migration Guidelines

### 5.1 From HMA v2.0 to v2.1
- **Impact**: Additive enhancements, full backward compatibility
- **Opportunity**: Adopt optimal technologies while maintaining compliance
- **Timeline**: Can be implemented incrementally as optimization opportunities arise
- **Priority Order**:
  1. Identify optimization opportunities in your domain
  2. Implement compliance adapters for boundary standards
  3. Adopt domain-appropriate internal technologies
  4. Document technology choices and benefits
  5. Verify continued ecosystem interoperability

### 5.2 Implementation Phases
- **Phase 1**: Assessment of current technology limitations and optimization opportunities
- **Phase 2**: Implementation of compliance adapters for boundary standards
- **Phase 3**: Adoption of domain-appropriate internal technologies
- **Phase 4**: Performance measurement and documentation of benefits
- **Phase 5**: Knowledge sharing with HMA community for potential standardization

## 6. Enhanced Plugin Manifest Schema Definition

### 6.1 Flexible Manifest Schema (ENHANCED for v2.1)

All plugins MUST provide a baseline manifest for HMA compliance, with optional extensions for flexibility:

```json
{
  "$schema": "https://hma-spec.org/schemas/v2.1/plugin-manifest-flexible.schema.json",
  "manifestVersion": "2.1",
  "hmaVersion": "2.1",
  "plugin": {
    "id": "string",
    "name": "string", 
    "version": "semver",
    "type": "L2-Orchestrator | L3-Capability",
    "description": "string"
  },
  "interfaces": {
    "implementedPorts": [
      {
        "name": "PluginExecutionPort",
        "version": "semver",
        "contract": "schema_reference",
        "required": true
      }
    ],
    "consumedPorts": [
      {
        "name": "CredBrokerQueryPort", 
        "version": "semver",
        "required": true
      }
    ]
  },
  "compliance": {
    "hma_baseline": "2.1",
    "boundary_standards": {
      "validation": "json_schema",
      "observability": "otel",
      "security": "mtls",
      "documentation": "openapi"
    },
    "internal_innovations": {
      "validation_tech": ["shacl", "protocol_buffers", "ml_validation"],
      "observability_tech": ["custom_metrics", "domain_telemetry"],
      "communication_tech": ["grpc", "graphql", "websockets"],
      "security_tech": ["service_mesh", "zero_trust"]
    }
  },
  "extensions": {
    "domain": {
      "type": "semantic | financial | ai_ml | iot | high_performance",
      "optimization_rationale": "string",
      "performance_benefits": "string"
    },
    "compliance_adapters": [
      {
        "technology": "shacl",
        "adapter_class": "SHACLToJSONSchemaAdapter",
        "fallback_strategy": "json_schema_validation"
      }
    ]
  }
}
```

### 6.2 Validation Requirements

- **Plugin Lifecycle Manager MUST validate baseline compliance**
- **Innovation extensions are OPTIONAL but MUST include compliance adapters**
- **Schema versioning MUST follow semantic versioning principles**
- **Backward compatibility MUST be maintained within major versions**
- **Documentation MUST explain technology choices and benefits** 