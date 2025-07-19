# Hexagonal Microkernel Architecture (HMA) Specification

_Version 2.1 (Flexible Implementation Edition)_

**(Companion document to the AI-Powered Model-Driven Development (APMDD) Methodology v2.1)**

---

**Part 3: HMA Internal Components & Key Interfaces (Analogous to C4 Level 3 - Components)**

This part zooms into the major zones identified in Part 2 (Core, Plugins) and describes their key internal components and the enhanced flexible interfaces (Ports) they expose or consume. This level of detail is crucial for understanding how HMA achieves its architectural goals while enabling innovation through extended port types and flexible communication patterns.

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

## 10. Flexible Port Framework (ENHANCED in v2.1)

### 10.1 Baseline Port Types (MANDATORY)

All HMA implementations MUST support these standard ports:

#### 10.1.1 PluginExecutionPort (MANDATORY)
*Standard plugin invocation interface - required for all plugins*

```python
class PluginExecutionPort:
    """Standard plugin execution interface"""
    
    def execute(self, request: PluginRequest) -> PluginResponse:
        """MANDATORY: Standard execution method"""
        # MANDATORY: JSON Schema validation at boundary
        self.validate_request(request)
        result = self.process_request(request)
        self.validate_response(result)
        return result
    
    def get_capabilities(self) -> PluginCapabilities:
        """MANDATORY: Return plugin capabilities"""
        return self.capabilities
```

#### 10.1.2 CredBrokerQueryPort (MANDATORY)  
*Secure credential access - required for all plugins*

```python
class CredBrokerQueryPort:
    """Secure credential management interface"""
    
    def get_credentials(self, credential_id: str) -> Credentials:
        """MANDATORY: Secure credential retrieval"""
        # MANDATORY: Must be backed by secure storage
        return self.secure_backend.retrieve(credential_id)
    
    def refresh_credentials(self, credential_id: str) -> Credentials:
        """MANDATORY: Credential rotation support"""
        return self.secure_backend.refresh(credential_id)
```

#### 10.1.3 EventBusPort (MANDATORY)
*Asynchronous messaging - required for event-driven communication*

```python
class EventBusPort:
    """Standard event bus interface"""
    
    def publish(self, event: Event) -> None:
        """MANDATORY: Publish events with schema validation"""
        # MANDATORY: JSON Schema validation for events
        self.validate_event_schema(event)
        self.event_broker.publish(event)
    
    def subscribe(self, event_type: str, handler: EventHandler) -> Subscription:
        """MANDATORY: Subscribe to events"""
        return self.event_broker.subscribe(event_type, handler)
```

#### 10.1.4 ObservabilityPort (MANDATORY)
*Telemetry emission - required for all components*

```python
class ObservabilityPort:
    """Standard observability interface"""
    
    def emit_trace(self, span_name: str, attributes: Dict) -> Span:
        """MANDATORY: OTEL trace emission"""
        # MANDATORY: Use OTEL SDK
        return self.otel_tracer.start_span(span_name, attributes)
    
    def emit_metric(self, metric_name: str, value: float, attributes: Dict) -> None:
        """MANDATORY: OTEL metric emission"""
        self.otel_meter.record(metric_name, value, attributes)
```

### 10.2 Extended Port Types (OPTIONAL)

Plugins MAY implement additional ports for enhanced capabilities:

#### 10.2.1 QueryPort (OPTIONAL)
```python
class QueryPort:
    """Flexible querying interface"""
    
    def execute_query(self, query_spec: QuerySpecification) -> QueryResult:
        """Execute flexible queries (SQL, GraphQL, SPARQL, etc.)"""
        # OPTIONAL: Domain-specific query processing
        if query_spec.type == "graphql":
            return self.graphql_executor.execute(query_spec)
        elif query_spec.type == "sparql":
            return self.sparql_executor.execute(query_spec)
        else:
            # MANDATORY: Fallback to standard execution
            return self.standard_executor.execute(query_spec)
    
    def get_schema(self) -> QuerySchema:
        """Return query capability schema"""
        return self.query_schema
```

#### 10.2.2 StreamingPort (OPTIONAL)

```python
class StreamingPort:
    """Streaming data interface"""
    
    def create_stream(self, stream_config: StreamConfiguration) -> StreamHandle:
        """Create data stream"""
        # OPTIONAL: gRPC, WebSocket, or custom streaming
        if stream_config.protocol == "grpc":
            return self.grpc_streaming.create_stream(stream_config)
        elif stream_config.protocol == "websocket":
            return self.websocket_streaming.create_stream(stream_config)
        else:
            return self.standard_streaming.create_stream(stream_config)
    
    def subscribe_to_stream(self, stream_id: str, callback: StreamCallback) -> StreamSubscription:
        """Subscribe to stream updates"""
        return self.stream_manager.subscribe(stream_id, callback)
```

#### 10.2.3 RealtimePort (OPTIONAL)

```python
class RealtimePort:
    """Real-time communication interface"""
    
    def establish_connection(self, connection_config: RealtimeConfig) -> RealtimeConnection:
        """Establish real-time connection"""
        # OPTIONAL: WebSocket, Server-Sent Events, etc.
        return self.realtime_manager.establish(connection_config)
    
    def broadcast_message(self, channel: str, message: Message) -> None:
        """Broadcast to channel subscribers"""
        self.realtime_manager.broadcast(channel, message)
    
    def send_direct_message(self, connection_id: str, message: Message) -> None:
        """Send direct message to specific connection"""
        self.realtime_manager.send_direct(connection_id, message)
```

### 10.3 Domain-Specific Port Extensions

**Guidelines for Domain-Specific Ports:**

```python
class DomainSpecificPortGuidelines:
    """Framework for creating domain-specific ports"""
    
    def create_domain_port(self, domain_name: str, capabilities: List[str]) -> DomainPort:
        """
        Create domain-specific port while maintaining HMA compliance
        
        Requirements:
        1. Must not break standard port compliance
        2. Must provide fallback to standard ports
        3. Must document capabilities clearly
        4. Must maintain interface versioning
        """
        
        port = DomainPort(domain_name)
        port.add_standard_compliance(self.get_standard_ports())
        port.add_domain_capabilities(capabilities)
        port.add_fallback_strategy()
        return port
```

**Example Domain-Specific Ports:**

```yaml
domain_ports:
  financial_trading:
    extends: "PluginExecutionPort"
    additional_capabilities:
      - "MarketDataPort: Real-time market data streaming"
      - "OrderExecutionPort: Trade execution with atomic operations"
      - "RiskManagementPort: Real-time risk calculations"
    
  ai_ml_systems:
    extends: "PluginExecutionPort"  
    additional_capabilities:
      - "ModelInferencePort: ML model inference interface"
      - "FeatureStorePort: Feature data access"
      - "ModelTrainingPort: Training pipeline interface"
    
  semantic_systems:
    extends: "PluginExecutionPort"
    additional_capabilities:
      - "SPARQLQueryPort: Semantic query interface"
      - "OntologyPort: Ontology management interface"
      - "ReasoningPort: Inference and reasoning interface"
    
  iot_systems:
    extends: "PluginExecutionPort"
    additional_capabilities:
      - "DeviceControlPort: IoT device command interface"
      - "SensorDataPort: Sensor data streaming"
      - "EdgeComputePort: Edge processing interface"
```

### 10.4 Port Compatibility Matrix

**Ensuring Compatibility with Extended Ports:**

```yaml
compatibility_strategy:
  mandatory_baseline:
    description: "All plugins MUST support standard ports"
    enforcement: "Core validates standard port compliance"
    
  optional_extensions:
    description: "Plugins MAY add domain-specific ports"
    requirement: "Must not break standard port functionality"
    
  graceful_degradation:
    description: "System works with mixed port capabilities"
    implementation: "Core routes to best available port"
    
  capability_discovery:
    description: "Core can discover plugin capabilities"
    mechanism: "Plugin manifest declares all supported ports"
```

### 10.5 Port Implementation Examples

**Hybrid Port Implementation:**

```python
class FlexibleCapabilityPlugin:
    """Plugin with both standard and extended ports"""
    
    def __init__(self):
        # MANDATORY: Standard ports
        self.execution_port = PluginExecutionPort()
        self.credential_port = CredBrokerQueryPort()
        self.event_port = EventBusPort()
        self.observability_port = ObservabilityPort()
        
        # OPTIONAL: Extended ports
        self.query_port = QueryPort() if self.supports_querying() else None
        self.streaming_port = StreamingPort() if self.supports_streaming() else None
        self.realtime_port = RealtimePort() if self.supports_realtime() else None
    
    def get_available_ports(self) -> Dict[str, Port]:
        """Return all available ports"""
        ports = {
            'execution': self.execution_port,
            'credentials': self.credential_port,
            'events': self.event_port,
            'observability': self.observability_port
        }
        
        # Add optional ports if available
        if self.query_port:
            ports['query'] = self.query_port
        if self.streaming_port:
            ports['streaming'] = self.streaming_port
        if self.realtime_port:
            ports['realtime'] = self.realtime_port
            
        return ports
    
    def execute_with_best_port(self, request: Request) -> Response:
        """Use the best available port for the request"""
        if request.requires_streaming() and self.streaming_port:
            return self.streaming_port.process_streaming_request(request)
        elif request.requires_querying() and self.query_port:
            return self.query_port.execute_query(request.query_spec)
        else:
            # MANDATORY: Always fallback to standard execution
            return self.execution_port.execute(request)
```

## 11. HMA Plugin Lifecycle Management (Detailed)

### 11.1 Plugin States and Transitions
Standard plugin lifecycle states: Discovered → Validated → Activated → Running → Deactivated.

### 11.2 Flexible Technical Compliance for Plugins (ENHANCED in v2.1)

#### 11.2.1 Baseline Compliance Requirements (MANDATORY)

All plugins MUST meet these minimum requirements:

**Standard Interface Compliance:**
- MUST implement PluginExecutionPort correctly
- MUST validate external inputs using JSON Schema (or equivalent adapter)
- MUST consume Core Control Plane Ports according to contracts
- MUST emit OTEL telemetry at boundaries (or equivalent adapter)

**Security Compliance:**
- MUST obtain credentials via CredBrokerQueryPort only
- MUST support mTLS for external communication (or equivalent adapter)
- MUST NOT store static secrets in code or configuration

**Manifest Compliance:**
- MUST provide valid manifest.json file conforming to enhanced schema in [[HMA v2.1 - Part 1a - Boundary Standards and Implementation Flexibility#6. Enhanced Plugin Manifest Schema Definition]]
- MUST declare all implemented and consumed ports
- MUST specify compliance strategy for non-standard technologies

#### 11.2.2 Innovation Flexibility (OPTIONAL)

Plugins MAY implement enhancements while maintaining baseline compliance:

**Advanced Validation Technologies:**
```python
class FlexibleValidationPlugin:
    """Plugin with advanced validation and compliance"""
    
    def __init__(self):
        # MANDATORY: Baseline compliance
        self.hma_validator = JSONSchemaValidator()
        self.otel_tracer = OTELTracer()
        
        # OPTIONAL: Advanced capabilities
        self.semantic_validator = SHACLValidator()
        self.performance_tracer = CustomTracer()
    
    def execute(self, request):
        """MANDATORY: Standard execution interface"""
        # Boundary compliance
        self.hma_validator.validate(request)
        
        with self.otel_tracer.start_span("plugin.execute"):
            # Internal processing with advanced tools
            with self.performance_tracer.start_span("internal.process"):
                semantic_validation = self.semantic_validator.validate(request)
                result = self.process_with_semantics(request, semantic_validation)
            
            # Ensure response compliance
            self.hma_validator.validate(result)
            return result
```

**Custom Communication Patterns:**

```python
class StreamingPlugin:
    """Plugin with streaming capabilities"""
    
    def execute(self, request):
        """MANDATORY: Standard synchronous interface"""
        if request.type == "streaming_request":
            # Convert streaming to synchronous for compliance
            stream_id = self.initiate_stream(request.stream_config)
            return {"stream_id": stream_id, "type": "stream_initiated"}
        else:
            return self.process_standard_request(request)
    
    def stream_data(self, stream_id):
        """OPTIONAL: Additional streaming capability"""
        for data_chunk in self.generate_stream_data(stream_id):
            yield self.process_chunk(data_chunk)
```

**Domain-Specific Enhancements:**

```python
class FinancialPlugin:
    """Plugin with financial domain enhancements"""
    
    def __init__(self):
        # MANDATORY: Standard HMA compliance
        self.standard_ports = self.initialize_standard_ports()
        
        # OPTIONAL: Financial domain ports
        self.market_data_port = MarketDataPort()
        self.risk_management_port = RiskManagementPort()
    
    def execute(self, request):
        """MANDATORY: Standard interface"""
        return self.process_with_standard_compliance(request)
    
    def get_real_time_market_data(self, symbol):
        """OPTIONAL: Domain-specific capability"""
        return self.market_data_port.stream_market_data(symbol)
```

#### 11.2.3 Compliance Validation Framework

**Enhanced Validation Process:**

```python
class EnhancedPluginValidator:
    """Validates plugins with flexibility support"""
    
    def validate_plugin_compliance(self, plugin):
        validation_result = PluginValidationResult()
        
        # MANDATORY: Baseline compliance
        validation_result.baseline = self.validate_baseline_compliance(plugin)
        
        # OPTIONAL: Extension validation
        if plugin.has_extensions():
            validation_result.extensions = self.validate_extensions(plugin)
            validation_result.adapters = self.validate_compliance_adapters(plugin)
        
        # MANDATORY: Integration testing
        validation_result.integration = self.test_hma_integration(plugin)
        
        return validation_result
    
    def validate_compliance_adapters(self, plugin):
        """Validate that non-standard technologies have proper adapters"""
        adapters_result = AdapterValidationResult()
        
        manifest = plugin.get_manifest()
        compliance = manifest.get('compliance', {})
        
        # Check validation strategy
        if compliance.get('validation_strategy') != 'json_schema':
            adapters_result.validation = self.test_validation_adapter(plugin)
        
        # Check observability strategy  
        if compliance.get('observability_model') != 'otel_only':
            adapters_result.observability = self.test_observability_adapter(plugin)
        
        # Check security strategy
        if compliance.get('security_model') != 'mtls':
            adapters_result.security = self.test_security_adapter(plugin)
        
        return adapters_result
```

#### 11.2.4 Runtime Flexibility Management

**Dynamic Capability Switching:**

```python
class RuntimeCapabilityManager:
    """Manages plugin capabilities at runtime"""
    
    def switch_to_baseline_mode(self, plugin_id, reason):
        """Switch plugin to baseline compliance mode"""
        plugin = self.get_plugin(plugin_id)
        
        # Log the switch reason
        self.log_capability_switch(plugin_id, "baseline", reason)
        
        # Disable advanced features
        plugin.disable_advanced_validation()
        plugin.disable_custom_observability()
        plugin.enable_pure_hma_mode()
        
        # Verify baseline compliance
        self.verify_baseline_compliance(plugin)
    
    def enable_advanced_mode(self, plugin_id, capabilities):
        """Enable advanced capabilities if supported"""
        plugin = self.get_plugin(plugin_id)
        
        # Verify advanced capabilities are available
        if not plugin.supports_advanced_capabilities(capabilities):
            raise UnsupportedCapabilityError(capabilities)
        
        # Enable advanced features
        plugin.enable_advanced_capabilities(capabilities)
        
        # Verify continued compliance
        self.verify_compliance_with_extensions(plugin)
```

#### 11.2.5 Enhanced Lifecycle States

**Extended Plugin States:**

```yaml
plugin_lifecycle_states:
  standard_states:
    - "Discovered: Plugin detected but not validated"
    - "Validated: Baseline compliance verified"
    - "Activated: Plugin ready for execution"
    - "Running: Plugin actively processing requests"
    - "Deactivated: Plugin stopped gracefully"
    
  enhanced_states:
    - "Capability_Discovery: Detecting extended capabilities"
    - "Adapter_Validation: Verifying compliance adapters"
    - "Hybrid_Mode: Running with extended capabilities"
    - "Fallback_Mode: Running in baseline compliance mode"
    - "Upgrading: Transitioning between capability levels"
```

**Lifecycle Management Example:**

```python
class FlexiblePluginLifecycleManager:
    """Enhanced lifecycle management with flexibility support"""
    
    def activate_plugin(self, plugin_manifest):
        """Enhanced plugin activation process"""
        
        # 1. MANDATORY: Baseline validation
        baseline_validation = self.validate_baseline_compliance(plugin_manifest)
        if not baseline_validation.valid:
            raise PluginActivationError(baseline_validation.errors)
        
        # 2. OPTIONAL: Detect extended capabilities
        capabilities = self.discover_extended_capabilities(plugin_manifest)
        
        # 3. OPTIONAL: Validate compliance adapters
        if capabilities.requires_adapters():
            adapter_validation = self.validate_compliance_adapters(plugin_manifest)
            if not adapter_validation.valid:
                self.log_warning("Advanced features disabled due to adapter validation failures")
                capabilities = self.get_baseline_capabilities()
        
        # 4. Activate with appropriate capability level
        plugin = self.create_plugin_instance(plugin_manifest, capabilities)
        self.register_plugin(plugin)
        
        return PluginActivationResult(plugin.id, capabilities)
    
    def handle_capability_failure(self, plugin_id, failure_reason):
        """Handle failures in extended capabilities"""
        plugin = self.get_plugin(plugin_id)
        
        # Attempt graceful degradation
        if plugin.supports_fallback():
            self.switch_to_baseline_mode(plugin_id, failure_reason)
            self.log_info(f"Plugin {plugin_id} switched to baseline mode due to: {failure_reason}")
        else:
            # If no fallback possible, deactivate plugin
            self.deactivate_plugin(plugin_id, failure_reason)
            self.log_error(f"Plugin {plugin_id} deactivated due to: {failure_reason}")
```

#### 11.2.6 Compliance Testing Framework

**Automated Compliance Testing:**

```python
class PluginComplianceTestSuite:
    """Comprehensive compliance testing for flexible plugins"""
    
    def run_full_compliance_test(self, plugin):
        """Run complete compliance test suite"""
        test_results = ComplianceTestResults()
        
        # MANDATORY: Baseline compliance tests
        test_results.baseline = self.test_baseline_compliance(plugin)
        
        # OPTIONAL: Extended capability tests
        if plugin.has_extended_capabilities():
            test_results.extensions = self.test_extended_capabilities(plugin)
            test_results.adapters = self.test_compliance_adapters(plugin)
        
        # MANDATORY: Integration tests
        test_results.integration = self.test_ecosystem_integration(plugin)
        
        return test_results
    
    def test_baseline_compliance(self, plugin):
        """Test mandatory baseline compliance"""
        tests = [
            self.test_plugin_execution_port(),
            self.test_json_schema_validation(),
            self.test_otel_telemetry_emission(),
            self.test_credential_broker_usage(),
            self.test_event_schema_compliance()
        ]
        
        return BaselineComplianceResult(tests)
    
    def test_extended_capabilities(self, plugin):
        """Test optional extended capabilities"""
        tests = []
        
        if plugin.has_graphql_capability():
            tests.append(self.test_graphql_interface())
        
        if plugin.has_streaming_capability():
            tests.append(self.test_streaming_interface())
        
        if plugin.has_domain_specific_ports():
            tests.append(self.test_domain_specific_ports())
        
        return ExtendedCapabilityResult(tests)
```

**Validation Requirements:**
- Plugins using non-standard technologies MUST pass adapter validation tests
- All plugins MUST pass baseline compliance tests regardless of extensions
- Extended capabilities MUST NOT break standard HMA functionality
- Compliance adapters MUST provide emergency fallback to baseline technologies 