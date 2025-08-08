# Hexagonal Microkernel Architecture (HMA) Specification

_Version 2.1 (Flexible Implementation Edition)_

**(Companion document to the AI-Powered Model-Driven Development (APMDD) Methodology v2.1)**

---

**Part 5: Applying Cross-Cutting HMA Concerns**

This part addresses the cross-cutting concerns that span across all HMA components with enhanced flexibility: observability, security, and enforcement mechanisms. These concerns enable operational excellence and compliance while allowing domain-appropriate technology choices through the "Boundary vs Implementation" framework.

## 16. HMA Observability Implementation

### 16.1 Observability Principles in HMA

HMA systems MUST provide comprehensive observability across all layers and components:
- **Distributed Tracing:** Track requests across plugin boundaries
- **Metrics Collection:** Monitor system health and performance
- **Structured Logging:** Capture detailed operational data
- **Correlation:** Link related events across components

### 16.2 Flexible Observability Framework (ENHANCED in v2.1)

#### 16.2.1 Boundary Observability Standards (MANDATORY)

All HMA boundaries MUST emit standardized telemetry:

**OTEL Integration for Interoperability:**
```yaml
mandatory_otel_telemetry:
  scope: "external_boundaries_only"
  requirements:
    - "Trace context propagation across plugin boundaries"
    - "Standard HMA resource attributes"
    - "Interoperable span and metric naming"
  purpose: "Enable cross-system observability"
```

**Boundary Telemetry Requirements:**
- External plugin invocations MUST emit OTEL spans with HMA conventions
- Cross-plugin communication MUST propagate trace context
- Boundary metrics MUST use standard HMA naming patterns
- Error events at boundaries MUST be captured with OTEL

**Standardized Resource Attributes (MANDATORY):**
```yaml
hma_resource_attributes:
  required:
    - "hma.component.type: L2-Core | L2-Orchestrator | L3-Capability"
    - "hma.component.id: unique-identifier"
    - "hma.layer: L2 | L3"
    - "service.name: component-name"
    - "service.version: semantic-version"
```

#### 16.2.2 Internal Observability Flexibility (OPTIONAL)

Components MAY use specialized observability internally:

**High-Performance Telemetry:**

```python
class HighPerformanceTelemetry:
    """Custom telemetry for latency-sensitive systems"""
    
    def __init__(self):
        # MANDATORY: OTEL for boundaries
        self.boundary_tracer = OTELTracer("hma-boundary")
        
        # OPTIONAL: Custom for internal performance
        self.internal_tracer = CustomHighSpeedTracer()
    
    def trace_external_operation(self, operation_name):
        # MANDATORY: Use OTEL for external visibility
        return self.boundary_tracer.start_span(f"hma.{operation_name}")
    
    def trace_internal_operation(self, operation_name):
        # OPTIONAL: Use optimized internal tracing
        return self.internal_tracer.start_span(operation_name)
```

**Domain-Specific Metrics:**

```python
class FinancialSystemMetrics:
    """Domain-specific metrics with HMA compliance"""
    
    def track_trade_execution(self, trade_data):
        # MANDATORY: HMA-compliant metrics
        self.otel_meter.record_counter(
            "hma.l3.trading.trades.total",
            value=1,
            attributes={"trade_type": trade_data.type}
        )
        
        # OPTIONAL: Financial domain metrics
        self.financial_metrics.record_pnl(trade_data.pnl)
        self.risk_metrics.update_var(trade_data.risk)
```

**AI/ML System Observability:**

```python
class MLSystemObservability:
    """ML-specific observability with HMA boundaries"""
    
    def track_model_inference(self, model_id, prediction_data):
        # MANDATORY: HMA boundary telemetry
        with self.otel_tracer.start_span("hma.l3.ml.inference") as span:
            span.set_attribute("model.id", model_id)
            span.set_attribute("prediction.confidence", prediction_data.confidence)
            
            # OPTIONAL: ML-specific metrics
            self.model_drift_detector.track_prediction(prediction_data)
            self.feature_store_metrics.track_feature_usage(prediction_data.features)
            
            return prediction_data
```

#### 16.2.3 Observability Architecture Patterns

**Hybrid Observability Strategy:**

```yaml
observability_patterns:
  standard_systems:
    internal: "OTEL throughout"
    boundary: "OTEL (compliant)"
    benefit: "Simplicity, full compatibility"
    
  high_performance_systems:
    internal: "Custom low-latency telemetry"
    boundary: "OTEL (compliant)"
    benefit: "Performance optimization"
    
  domain_specific_systems:
    internal: "Domain metrics + OTEL"
    boundary: "OTEL (compliant)"
    benefit: "Business-relevant observability"
    
  ai_ml_systems:
    internal: "ML metrics + model monitoring"
    boundary: "OTEL (compliant)"
    benefit: "ML-specific observability"
```

#### 16.2.4 Observability Compliance Framework

```python
class FlexibleObservabilityManager:
    """Manages observability with boundary compliance and internal flexibility"""
    
    def __init__(self, internal_telemetry_config=None):
        # MANDATORY: HMA boundary compliance
        self.boundary_tracer = OTELTracer("hma-boundary")
        self.boundary_meter = OTELMeter("hma-metrics")
        
        # OPTIONAL: Internal optimizations
        self.internal_telemetry = self._configure_internal_telemetry(internal_telemetry_config)
    
    def emit_boundary_telemetry(self, operation, attributes):
        """MANDATORY: Emit HMA-compliant telemetry at boundaries"""
        span = self.boundary_tracer.start_span(f"hma.{operation}")
        span.set_attributes(attributes)
        return span
    
    def emit_internal_telemetry(self, event_data):
        """OPTIONAL: Emit internal domain-specific telemetry"""
        if self.internal_telemetry:
            return self.internal_telemetry.emit(event_data)
    
    def ensure_compliance(self):
        """Verify boundary telemetry compliance"""
        return self.boundary_tracer.is_configured() and self.boundary_meter.is_configured()
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

### 17.2 Flexible Security Framework (ENHANCED in v2.1)

#### 17.2.1 Boundary Security Standards (MANDATORY)

All external boundaries MUST implement baseline security:

**External Communication Security:**
- **L1 Boundaries**: MANDATORY TLS 1.3+ for external traffic
- **Cross-Plugin**: MANDATORY mTLS for plugin-to-plugin via Core
- **Infrastructure**: MANDATORY secure credential access via CredentialBroker

#### 17.2.2 Internal Security Flexibility (OPTIONAL)

Components MAY use advanced security internally:

**Service Mesh Security:**
```python
class ServiceMeshSecurityAdapter:
    """Leverage service mesh for internal security"""
    
    def __init__(self):
        # MANDATORY: mTLS for HMA boundaries
        self.hma_mtls_client = MTLSClient(self.load_hma_certs())
        
        # OPTIONAL: Service mesh for internal security
        self.mesh_client = ServiceMeshClient()
    
    def call_external_plugin(self, plugin_id, request):
        # MANDATORY: Use HMA mTLS
        return self.hma_mtls_client.call(plugin_id, request)
    
    def call_internal_service(self, service, request):
        # OPTIONAL: Use service mesh security
        return self.mesh_client.call(service, request)
```

**Zero-Trust Architecture:**

```python
class ZeroTrustSecurityModel:
    """Zero-trust with HMA boundary compliance"""
    
    def authenticate_request(self, request):
        # MANDATORY: HMA credential validation
        hma_auth = self.validate_hma_credentials(request)
        
        # OPTIONAL: Additional zero-trust validation
        identity = self.identity_provider.authenticate(request)
        policy_result = self.policy_engine.authorize(identity, request)
        
        return AuthResult(hma_auth, identity, policy_result)
```

**Hardware Security Module (HSM) Integration:**

```python
class HSMSecurityPlugin:
    """Hardware security with HMA compliance"""
    
    def __init__(self):
        # MANDATORY: HMA credential broker compliance
        self.credential_broker = CredentialBrokerPort()
        
        # OPTIONAL: HSM for sensitive operations
        self.hsm = HardwareSecurityModule()
    
    def get_credentials(self, credential_id):
        # MANDATORY: Use HMA credential broker
        return self.credential_broker.get_credentials(credential_id)
    
    def perform_crypto_operation(self, operation_data):
        # OPTIONAL: Use HSM for high-security operations
        return self.hsm.perform_operation(operation_data)
```

#### 17.2.3 Security Pattern Guidelines

**Security Architecture Choices:**

```yaml
security_patterns:
  traditional_mtls:
    description: "mTLS throughout the system"
    hma_compliance: "Native compliance"
    complexity: "Low"
    
  service_mesh:
    description: "Service mesh handles internal security"
    hma_compliance: "mTLS at HMA boundaries only"
    complexity: "Medium"
    benefits: ["Advanced traffic management", "Observability"]
    
  zero_trust:
    description: "Identity-based security"
    hma_compliance: "mTLS + identity validation"
    complexity: "High"
    benefits: ["Fine-grained access control", "Compliance"]
    
  hybrid_security:
    description: "Mix of patterns based on requirements"
    hma_compliance: "Ensure boundary compliance"
    complexity: "Variable"
    benefits: ["Optimized for specific needs"]
```

#### 17.2.4 Credential Management Flexibility

**Boundary Requirements (MANDATORY):**
- CredentialBroker MUST be used for all external credential access
- Secure backend MUST store all credentials (HashiCorp Vault, etc.)
- Credential rotation MUST be supported with configurable TTL

**Internal Enhancements (OPTIONAL):**

```python
class FlexibleCredentialManager:
    """Credential management with boundary compliance and internal flexibility"""
    
    def __init__(self):
        # MANDATORY: HMA CredentialBroker compliance
        self.hma_credential_broker = CredentialBrokerPort()
        
        # OPTIONAL: Enhanced internal credential management
        self.internal_vault = self._configure_advanced_vault()
        self.hsm = self._configure_hsm_if_available()
    
    def get_external_credentials(self, credential_id):
        """MANDATORY: Use HMA CredentialBroker for external access"""
        return self.hma_credential_broker.get_credentials(credential_id)
    
    def manage_internal_secrets(self, secret_data):
        """OPTIONAL: Enhanced internal secret management"""
        if self.hsm:
            return self.hsm.encrypt_secret(secret_data)
        else:
            return self.internal_vault.store_secret(secret_data)
```

#### 17.2.5 Security Validation Strategy

**Implementation Requirements:**
```yaml
security_compliance:
  boundary_requirements:
    external_tls: "TLS_1_3_MANDATORY"
    inter_plugin_mtls: "MANDATORY"
    credential_broker: "MANDATORY"
    input_validation: "JSON_SCHEMA_MANDATORY"
    
  internal_flexibility:
    service_mesh_security: "OPTIONAL"
    zero_trust_models: "OPTIONAL"
    hsm_integration: "OPTIONAL"
    advanced_encryption: "OPTIONAL"
    
  compliance_validation:
    boundary_security_tests: "MANDATORY"
    credential_access_audits: "MANDATORY"
    encryption_verification: "MANDATORY"
    threat_model_validation: "RECOMMENDED"
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

**ENHANCED in v2.1:** All boundary validation failures MUST be logged via the ObservabilityPort and trigger appropriate alerts in monitoring systems. Internal validation systems MAY use additional alerting mechanisms while ensuring HMA boundary compliance. 