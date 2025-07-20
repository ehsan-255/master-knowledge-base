# Hexagonal Microkernel Architecture (HMA) Specification

_Version 2.2 (Guided Implementation Edition)_

**(Companion document to the AI-Powered Model-Driven Development (APMDD) Methodology v2.2)**

---

**Part 3: HMA Internal Components & Key Interfaces (Analogous to C4 Level 3 - Components)**

This part zooms into the major zones identified in Part 2 (Core, Plugins) and describes their key internal components and the technology-guided interfaces (Ports) they expose or consume. **ENHANCED in v2.2:** All components now include clear technology recommendations through the three-tier framework, enabling optimal implementation choices while maintaining ecosystem compatibility.

## 8. Deeper Dive: Microkernel Core Components (L2) with Technology Guidance
#hma-core-component #hma-zone-core #hma-layer-L2 #c4-level-3
[[HMA v2.2 - Part 2 - High-Level Structure#5. The HMA Microkernel Core Zone (L2): Role & Responsibilities]]

The L2 Microkernel Core comprises several key logical components that fulfill its mandated responsibilities using recommended technologies for optimal operation.

### 8.1 Request Router/Dispatcher Component (Technology-Enhanced)
*(See [[HMA v2.2 - Part 6 - Supporting Information#19.2 Core HMA Terms (Enhanced for v2.2)|Glossary: Core]])*

*   **Responsibility:** Routes incoming requests to appropriate plugins using intelligent routing strategies
*   **Recommended Technologies (Tier 2):**
    *   **API Gateway:** Kong for HTTP routing, Istio for service mesh routing
    *   **Load Balancing:** Kubernetes native load balancing, Envoy proxy
    *   **Service Discovery:** Kubernetes DNS, Consul for advanced scenarios
    *   **Circuit Breaking:** Istio circuit breakers, Kong rate limiting
*   **Alternative Technologies (Tier 3):** Custom routing engines with specialized algorithms, performance-optimized routers
*   **Mandatory Standards (Tier 1):** JSON Schema validation for all routing decisions, OpenTelemetry tracing for all routing operations

**Technology Implementation Example:**
```python
class TechnologyGuidedRequestRouter:
    """Request router with recommended technology stack"""
    
    def __init__(self):
        # Recommended Tier 2 Technologies
        self.kong_gateway = KongGatewayClient()
        self.istio_service_mesh = IstioServiceMeshClient()
        self.kubernetes_discovery = KubernetesServiceDiscovery()
        
        # Mandatory Tier 1 Standards
        self.json_schema_validator = JSONSchemaValidator()
        self.otel_tracer = OpenTelemetryTracer()
        
        # Alternative Tier 3 (if configured)
        self.custom_router = self.load_custom_router_if_configured()
    
    def route_request(self, request: Request) -> RoutingDecision:
        """Route request using recommended technologies"""
        with self.otel_tracer.start_span("request.routing") as span:
            # Mandatory: Validate request schema
            self.json_schema_validator.validate(request)
            
            # Recommended: Use Kubernetes service discovery
            available_plugins = self.kubernetes_discovery.find_plugins(
                request.get_capability_requirements()
            )
            
            # Recommended: Apply Kong/Istio routing policies
            routing_decision = self.istio_service_mesh.select_target(
                available_plugins, request.routing_preferences
            )
            
            # Alternative: Use custom router if configured and beneficial
            if self.custom_router and request.requires_specialized_routing():
                routing_decision = self.custom_router.route_with_compliance_adapter(
                    request, routing_decision
                )
            
            span.set_attributes(self.get_routing_attributes(routing_decision))
            return routing_decision
```

### 8.2 Plugin Lifecycle Manager Component (Container-Orchestrated)
*(See [[HMA v2.2 - Part 6 - Supporting Information#19.2 Core HMA Terms (Enhanced for v2.2)|Glossary: Plugin]])*

*   **Responsibility:** Manages complete plugin lifecycle using cloud-native orchestration
*   **Recommended Technologies (Tier 2):**
    *   **Container Orchestration:** Kubernetes for production, Docker Compose for development
    *   **Container Registry:** Docker Hub, AWS ECR, Harbor for enterprise
    *   **Configuration Management:** Kubernetes ConfigMaps/Secrets, Helm charts
    *   **Health Monitoring:** Kubernetes health checks, Prometheus metrics
*   **Alternative Technologies (Tier 3):** Custom orchestration platforms, serverless deployment models
*   **Mandatory Standards (Tier 1):** Plugin manifest.json v2.2 schema validation, secure credential injection

**Enhanced Lifecycle Management:**
```python
class KubernetesPluginLifecycleManager:
    """Plugin lifecycle manager using recommended Kubernetes stack"""
    
    def __init__(self):
        # Recommended Tier 2 Technologies  
        self.k8s_client = KubernetesClient()
        self.docker_registry = DockerRegistryClient()
        self.helm_client = HelmClient()
        self.prometheus_client = PrometheusClient()
        
        # Mandatory Tier 1 Standards
        self.manifest_validator = PluginManifestValidator()
        self.vault_client = VaultCredentialBroker()
        
        # Alternative Tier 3 (if configured)
        self.serverless_deployer = self.load_serverless_deployer_if_configured()
    
    def deploy_plugin(self, plugin_manifest: PluginManifest) -> DeploymentResult:
        """Deploy plugin using recommended Kubernetes deployment"""
        
        # Mandatory: Validate manifest schema
        validation_result = self.manifest_validator.validate_v2_2_schema(plugin_manifest)
        if not validation_result.valid:
            raise PluginValidationError(validation_result.errors)
        
        # Recommended: Create Kubernetes deployment
        if plugin_manifest.deployment_strategy == "kubernetes":
            return self.deploy_with_kubernetes(plugin_manifest)
        elif plugin_manifest.deployment_strategy == "serverless" and self.serverless_deployer:
            return self.deploy_with_serverless(plugin_manifest)
        else:
            return self.deploy_with_docker_compose(plugin_manifest)
    
    def deploy_with_kubernetes(self, manifest: PluginManifest) -> DeploymentResult:
        """Deploy using recommended Kubernetes stack"""
        
        # Create Kubernetes resources
        deployment = self.create_k8s_deployment(manifest)
        service = self.create_k8s_service(manifest)
        config_map = self.create_k8s_config_map(manifest)
        
        # Inject secrets securely
        secret_refs = self.vault_client.create_secret_references(
            manifest.required_credentials
        )
        deployment.spec.template.spec.volumes.extend(secret_refs)
        
        # Apply Kubernetes resources
        self.k8s_client.apply_resources([deployment, service, config_map])
        
        # Set up monitoring
        self.prometheus_client.configure_plugin_monitoring(manifest.plugin_id)
        
        return DeploymentResult.success(manifest.plugin_id)
```

### 8.3 Control Plane Service Components with Technology Stack
#hma-core-component
*(See [[HMA v2.2 - Part 6 - Supporting Information#19.2 Core HMA Terms (Enhanced for v2.2)|Glossary: Core]])*

The Core provides essential services using recommended technologies for security, reliability, and observability.

#### 8.3.1 CredentialBroker with Recommended Secrets Management
```python
class RecommendedCredentialBroker:
    """Credential broker using recommended secrets management stack"""
    
    def __init__(self):
        # Recommended Tier 2 Technologies
        self.vault_client = HashiCorpVaultClient()
        self.k8s_secrets = KubernetesSecretsClient()
        self.external_secrets = ExternalSecretsOperator()
        
        # Alternative Tier 3 (cloud-native options)
        self.aws_secrets = AWSSecretsManagerClient() if self.is_aws_env() else None
        self.azure_keyvault = AzureKeyVaultClient() if self.is_azure_env() else None
        
        # Mandatory Tier 1 Standards
        self.encryption_handler = AESEncryptionHandler()
        self.audit_logger = AuditLogger()
    
    def get_credentials(self, plugin_id: str, credential_id: str) -> Credentials:
        """Retrieve credentials using recommended technology stack"""
        
        # Mandatory: Audit credential access
        self.audit_logger.log_credential_access(plugin_id, credential_id)
        
        # Recommended: Try Vault first
        if self.vault_client.is_available():
            return self.vault_client.get_secret(
                f"plugins/{plugin_id}/{credential_id}"
            )
        
        # Alternative: Use cloud-native secrets management
        elif self.aws_secrets and self.is_aws_env():
            return self.aws_secrets.get_secret_value(credential_id)
        
        # Fallback: Kubernetes secrets
        else:
            return self.k8s_secrets.get_secret(plugin_id, credential_id)
```

#### 8.3.2 EventBus with Recommended Message Brokers
```python
class RecommendedEventBus:
    """Event bus using recommended messaging technologies"""
    
    def __init__(self):
        # Recommended Tier 2 Technologies
        self.nats_client = NATSClient()  # For simple deployments
        self.kafka_client = KafkaClient()  # For enterprise scale
        self.rabbitmq_client = RabbitMQClient()  # For complex routing
        
        # Alternative Tier 3 Technologies
        self.redis_streams = RedisStreamsClient() if self.needs_ultra_low_latency() else None
        self.apache_pulsar = ApachePulsarClient() if self.needs_geo_replication() else None
        
        # Mandatory Tier 1 Standards
        self.event_schema_validator = CloudEventsValidator()
        self.otel_tracer = OpenTelemetryTracer()
    
    def publish_event(self, event: Event) -> PublishResult:
        """Publish event using optimal message broker"""
        
        # Mandatory: Validate event schema
        self.event_schema_validator.validate(event)
        
        with self.otel_tracer.start_span("event.publish") as span:
            # Select optimal broker based on requirements
            if event.requires_ultra_low_latency() and self.redis_streams:
                result = self.redis_streams.publish_with_adapter(event)
            elif event.requires_enterprise_scale():
                result = self.kafka_client.publish(event)
            elif event.requires_complex_routing():
                result = self.rabbitmq_client.publish(event)
            else:
                result = self.nats_client.publish(event)  # Default recommended
            
            span.set_attributes(self.get_publish_attributes(event, result))
            return result
```

## 9. Deeper Dive: Generic Plugin Components (L3 & L2 Orchestrator) with Technology Guidance
#hma-plugin #hma-zone-plugin #c4-level-3

### 9.1 Technology-Guided Port Definitions (Enhanced in v2.2)
*(See [[HMA v2.2 - Part 6 - Supporting Information#19.2 Core HMA Terms (Enhanced for v2.2)|Glossary: Port]])*

**NEW in v2.2:** All Port contracts now include technology tier classifications and implementation recommendations.

#### 9.1.1 Port Technology Classification Framework
```yaml
port_technology_classification:
  tier_1_mandatory:
    description: "Standards required for all port implementations"
    requirements:
      - "JSON Schema validation at boundaries"
      - "OpenTelemetry telemetry emission"
      - "TLS/mTLS secure communication"
      - "OpenAPI documentation for REST ports"
    
  tier_2_recommended:
    description: "Proven technologies for port implementations"
    technologies:
      - "HTTP/2 + gRPC for synchronous ports"
      - "NATS/Kafka for asynchronous ports"
      - "Prometheus metrics for port monitoring"
      - "Kubernetes service discovery"
    
  tier_3_alternative:
    description: "Specialized technologies with compliance adapters"
    examples:
      - "GraphQL endpoints with JSON Schema adapters"
      - "Protocol Buffers with JSON boundary adapters"
      - "Redis Streams with CloudEvents adapters"
      - "SPARQL endpoints with REST API adapters"
```

### 9.2 Technology-Enhanced Adapter Implementation
*(See [[HMA v2.2 - Part 6 - Supporting Information#19.2 Core HMA Terms (Enhanced for v2.2)|Glossary: Adapter]])*

**NEW in v2.2:** Adapters now include technology-specific implementations with clear recommendations and compliance strategies.

```python
class TechnologyGuidedAdapter:
    """Base adapter with technology guidance"""
    
    def __init__(self, technology_tier: str):
        self.technology_tier = technology_tier
        
        # Mandatory Tier 1 Standards (always required)
        self.json_schema_validator = JSONSchemaValidator()
        self.otel_tracer = OpenTelemetryTracer()
        self.tls_handler = TLSConnectionHandler()
        
        # Recommended Tier 2 Technologies (default choice)
        if technology_tier in ["recommended", "tier_2"]:
            self.http_client = HTTP2Client()
            self.grpc_client = gRPCClient()
            self.prometheus_metrics = PrometheusMetricsClient()
        
        # Alternative Tier 3 Technologies (with compliance adapters)
        elif technology_tier in ["alternative", "tier_3"]:
            self.load_alternative_technologies()
            self.compliance_adapters = self.initialize_compliance_adapters()
    
    def process_request_with_compliance(self, request: Request) -> Response:
        """Process request ensuring compliance regardless of technology tier"""
        
        # Mandatory: Validate at boundary
        self.json_schema_validator.validate(request)
        
        with self.otel_tracer.start_span("adapter.process") as span:
            if self.technology_tier == "recommended":
                response = self.process_with_recommended_tech(request)
            elif self.technology_tier == "alternative":
                response = self.process_with_alternative_tech(request)
                response = self.compliance_adapters.ensure_boundary_compliance(response)
            
            # Mandatory: Validate response
            self.json_schema_validator.validate(response)
            return response
```

## 10. Enhanced Port Framework with Technology Recommendations (v2.2)

### 10.1 Mandatory Port Types with Technology Implementation

All HMA implementations MUST support these standard ports using recommended technologies:

#### 10.1.1 PluginExecutionPort (Technology-Enhanced)
*Standard plugin invocation interface with technology guidance*

```python
class PluginExecutionPort:
    """Enhanced plugin execution interface with technology recommendations"""
    
    def __init__(self, technology_config: TechnologyConfig):
        # Mandatory Tier 1 Standards
        self.json_schema_validator = JSONSchemaValidator()
        self.otel_tracer = OpenTelemetryTracer()
        
        # Recommended Tier 2 Technologies
        self.grpc_server = gRPCServer() if technology_config.use_grpc else None
        self.http2_server = HTTP2Server()
        self.prometheus_metrics = PrometheusMetricsCollector()
        
        # Alternative Tier 3 Technologies (with adapters)
        self.graphql_endpoint = None
        self.custom_protocol = None
        if technology_config.has_alternatives():
            self.load_alternative_implementations(technology_config)
    
    def execute(self, request: PluginRequest) -> PluginResponse:
        """MANDATORY: Standard execution method with technology optimization"""
        
        # Mandatory: JSON Schema validation at boundary
        self.json_schema_validator.validate(request)
        
        with self.otel_tracer.start_span("plugin.execute") as span:
            # Recommended: Use gRPC for high-performance scenarios
            if self.grpc_server and request.requires_high_performance():
                response = self.execute_via_grpc(request)
            
            # Alternative: Use GraphQL for flexible querying
            elif self.graphql_endpoint and request.is_query_type():
                response = self.execute_via_graphql(request)
                response = self.ensure_standard_compliance(response)
            
            # Default: Standard HTTP/2 execution
            else:
                response = self.execute_via_http2(request)
            
            # Mandatory: Validate response at boundary
            self.json_schema_validator.validate(response)
            
            # Recommended: Record metrics
            self.prometheus_metrics.record_execution_metrics(request, response)
            
            return response
    
    def get_capabilities(self) -> PluginCapabilities:
        """MANDATORY: Return plugin capabilities with technology details"""
        capabilities = PluginCapabilities()
        capabilities.technology_tier = self.get_technology_tier()
        capabilities.supported_protocols = self.get_supported_protocols()
        capabilities.performance_characteristics = self.get_performance_profile()
        return capabilities
```

#### 10.1.2 CredBrokerQueryPort (Security-Enhanced)
*Secure credential access with recommended secrets management*

```python
class CredBrokerQueryPort:
    """Enhanced credential management with recommended security stack"""
    
    def __init__(self, security_config: SecurityConfig):
        # Recommended Tier 2 Technologies
        self.vault_client = HashiCorpVaultClient()
        self.k8s_secrets = KubernetesSecretsClient()
        self.external_secrets = ExternalSecretsOperatorClient()
        
        # Alternative Tier 3 Technologies (cloud-native)
        self.cloud_secrets = self.initialize_cloud_secrets_client(security_config)
        
        # Mandatory Tier 1 Standards
        self.encryption_handler = AESGCMEncryptionHandler()
        self.audit_logger = SecurityAuditLogger()
        self.mTLS_client = mTLSClient()
    
    def get_credentials(self, credential_id: str) -> Credentials:
        """MANDATORY: Secure credential retrieval with technology optimization"""
        
        # Mandatory: Audit all credential access
        self.audit_logger.log_credential_access(credential_id)
        
        # Recommended: Try HashiCorp Vault first
        if self.vault_client.is_available():
            credentials = self.vault_client.get_secret(credential_id)
        
        # Alternative: Use cloud-native secrets management
        elif self.cloud_secrets and self.cloud_secrets.is_configured():
            credentials = self.cloud_secrets.get_secret(credential_id)
        
        # Fallback: Kubernetes secrets
        else:
            credentials = self.k8s_secrets.get_secret(credential_id)
        
        # Mandatory: Encrypt credentials in transit
        return self.encryption_handler.encrypt_for_transport(credentials)
    
    def refresh_credentials(self, credential_id: str) -> Credentials:
        """MANDATORY: Credential rotation with recommended automation"""
        
        # Recommended: Use Vault's dynamic secrets
        if self.vault_client.supports_dynamic_secrets(credential_id):
            return self.vault_client.generate_dynamic_secret(credential_id)
        
        # Alternative: Use cloud provider rotation
        elif self.cloud_secrets and self.cloud_secrets.supports_rotation(credential_id):
            return self.cloud_secrets.rotate_secret(credential_id)
        
        # Fallback: Manual rotation process
        else:
            return self.manual_credential_rotation(credential_id)
```

#### 10.1.3 EventBusPort (Message Broker Enhanced)
*Asynchronous messaging with recommended broker technologies*

```python
class EventBusPort:
    """Enhanced event bus with recommended messaging technologies"""
    
    def __init__(self, messaging_config: MessagingConfig):
        # Recommended Tier 2 Technologies
        self.nats_client = NATSClient()  # Simple, fast messaging
        self.kafka_client = KafkaClient()  # Enterprise-scale messaging
        self.rabbitmq_client = RabbitMQClient()  # Complex routing needs
        
        # Alternative Tier 3 Technologies
        self.redis_streams = RedisStreamsClient() if messaging_config.ultra_low_latency else None
        self.apache_pulsar = ApachePulsarClient() if messaging_config.geo_distributed else None
        
        # Mandatory Tier 1 Standards
        self.event_schema_validator = CloudEventsValidator()
        self.otel_tracer = OpenTelemetryTracer()
        self.encryption_handler = EventEncryptionHandler()
    
    def publish(self, event: Event) -> PublishResult:
        """MANDATORY: Publish events with optimal broker selection"""
        
        # Mandatory: Validate event schema (CloudEvents format)
        self.event_schema_validator.validate(event)
        
        with self.otel_tracer.start_span("event.publish") as span:
            # Select optimal broker based on event characteristics
            broker_client = self.select_optimal_broker(event)
            
            # Mandatory: Encrypt sensitive events
            if event.contains_sensitive_data():
                event = self.encryption_handler.encrypt_event(event)
            
            # Publish with selected broker
            result = broker_client.publish(event)
            
            # Alternative: Use compliance adapter if needed
            if hasattr(broker_client, 'compliance_adapter'):
                result = broker_client.compliance_adapter.ensure_cloudevents_compliance(result)
            
            span.set_attributes(self.get_publish_attributes(event, result))
            return result
    
    def select_optimal_broker(self, event: Event) -> MessageBrokerClient:
        """Select optimal message broker based on event requirements"""
        
        # Ultra-low latency requirements (financial trading, IoT)
        if event.requires_ultra_low_latency() and self.redis_streams:
            return self.redis_streams
        
        # Enterprise scale requirements (high throughput, durability)
        elif event.requires_enterprise_scale():
            return self.kafka_client
        
        # Complex routing requirements (workflow, business rules)
        elif event.requires_complex_routing():
            return self.rabbitmq_client
        
        # Default: NATS for simplicity and performance
        else:
            return self.nats_client
    
    def subscribe(self, event_type: str, handler: EventHandler) -> Subscription:
        """MANDATORY: Subscribe to events with recommended patterns"""
        
        # Recommended: Use consumer groups for scalability
        consumer_group = f"{self.plugin_id}_{event_type}_consumers"
        
        # Subscribe using optimal broker
        broker_client = self.get_broker_for_event_type(event_type)
        subscription = broker_client.subscribe(
            event_type, 
            handler, 
            consumer_group=consumer_group
        )
        
        # Mandatory: Add OTEL instrumentation to handler
        instrumented_handler = self.otel_tracer.instrument_event_handler(handler)
        subscription.set_handler(instrumented_handler)
        
        return subscription
```

#### 10.1.4 ObservabilityPort (Full-Stack Observability)
*Comprehensive telemetry with recommended observability stack*

```python
class ObservabilityPort:
    """Enhanced observability with recommended technology stack"""
    
    def __init__(self, observability_config: ObservabilityConfig):
        # Mandatory Tier 1 Standards
        self.otel_tracer = OpenTelemetryTracer()
        self.otel_meter = OpenTelemetryMeter()
        self.otel_logger = OpenTelemetryLogger()
        
        # Recommended Tier 2 Technologies
        self.prometheus_client = PrometheusClient()
        self.grafana_client = GrafanaClient()
        self.jaeger_client = JaegerClient()
        self.loki_client = LokiClient()
        
        # Alternative Tier 3 Technologies (with OTEL compliance)
        self.custom_metrics = None
        self.specialized_tracing = None
        if observability_config.has_specialized_requirements():
            self.initialize_specialized_observability(observability_config)
    
    def emit_trace(self, span_name: str, attributes: Dict) -> Span:
        """MANDATORY: OTEL trace emission with recommended backend"""
        
        # Mandatory: Use OpenTelemetry for boundary compliance
        span = self.otel_tracer.start_span(span_name)
        span.set_attributes(attributes)
        
        # Recommended: Export to Jaeger for visualization
        if self.jaeger_client.is_configured():
            self.jaeger_client.export_span(span)
        
        # Alternative: Export to specialized tracing system
        if self.specialized_tracing:
            adapted_span = self.specialized_tracing.adapter.convert_otel_span(span)
            self.specialized_tracing.export_span(adapted_span)
        
        return span
    
    def emit_metric(self, metric_name: str, value: float, attributes: Dict) -> None:
        """MANDATORY: OTEL metric emission with recommended storage"""
        
        # Mandatory: Use OpenTelemetry for boundary compliance
        self.otel_meter.record_value(metric_name, value, attributes)
        
        # Recommended: Export to Prometheus for storage and alerting
        prometheus_metric = self.prometheus_client.create_metric(
            metric_name, value, attributes
        )
        self.prometheus_client.record(prometheus_metric)
        
        # Alternative: Export to custom metrics system
        if self.custom_metrics:
            adapted_metric = self.custom_metrics.adapter.convert_otel_metric(
                metric_name, value, attributes
            )
            self.custom_metrics.record(adapted_metric)
    
    def emit_log(self, level: str, message: str, attributes: Dict) -> None:
        """MANDATORY: Structured logging with recommended aggregation"""
        
        # Mandatory: Use OpenTelemetry for structured logging
        log_record = self.otel_logger.create_log_record(level, message, attributes)
        
        # Recommended: Send to Loki for log aggregation
        if self.loki_client.is_configured():
            loki_log = self.loki_client.format_log(log_record)
            self.loki_client.push_log(loki_log)
        
        # Alternative: Send to specialized logging system
        elif self.custom_logging:
            adapted_log = self.custom_logging.adapter.convert_otel_log(log_record)
            self.custom_logging.emit(adapted_log)
        
        # Fallback: Standard logging
        else:
            self.standard_logger.log(level, message, attributes)
```

### 10.2 Domain-Specific Port Extensions with Technology Guidance (NEW in v2.2)

Plugins MAY implement domain-specific ports using alternative technologies with proper compliance adapters:

#### 10.2.1 Semantic Systems Port
```python
class SemanticSystemsPort:
    """Domain-specific port for semantic/RDF systems"""
    
    def __init__(self):
        # Alternative Tier 3 Technologies
        self.shacl_validator = SHACLValidator()
        self.rdf_triplestore = ApacheJenaClient()
        self.sparql_engine = SPARQLQueryEngine()
        
        # Mandatory Tier 1 Compliance Adapters
        self.shacl_to_json_adapter = SHACLToJSONSchemaAdapter()
        self.sparql_to_rest_adapter = SPARQLToRESTAdapter()
        self.rdf_to_jsonld_adapter = RDFToJSONLDAdapter()
        
        # Mandatory boundary compliance
        self.json_schema_validator = JSONSchemaValidator()
        self.otel_tracer = OpenTelemetryTracer()
    
    def validate_semantic_data(self, rdf_data: RDFGraph) -> ValidationResult:
        """Validate RDF data using SHACL with JSON Schema boundary compliance"""
        
        with self.otel_tracer.start_span("semantic.validation") as span:
            # Alternative: Advanced SHACL validation
            shacl_result = self.shacl_validator.validate(rdf_data)
            
            # Mandatory: Convert to standard validation result
            json_result = self.shacl_to_json_adapter.convert_validation_result(shacl_result)
            
            # Mandatory: Validate boundary compliance
            self.json_schema_validator.validate(json_result)
            
            span.set_attributes({
                "semantic.validator": "SHACL",
                "boundary.compliance": "JSON Schema",
                "validation.result": json_result.is_valid
            })
            
            return json_result
    
    def query_semantic_data(self, sparql_query: str) -> QueryResult:
        """Execute SPARQL query with REST API boundary compliance"""
        
        # Alternative: SPARQL query execution
        sparql_result = self.sparql_engine.execute(sparql_query)
        
        # Mandatory: Convert to REST-compatible result
        rest_result = self.sparql_to_rest_adapter.convert_query_result(sparql_result)
        
        # Mandatory: Validate boundary compliance
        self.json_schema_validator.validate(rest_result)
        
        return rest_result
    
    def expose_as_standard_port(self) -> PluginExecutionPort:
        """Expose semantic capabilities via standard HMA port"""
        
        def execute_handler(request: PluginRequest) -> PluginResponse:
            if request.operation == "validate":
                rdf_data = self.rdf_to_jsonld_adapter.parse_request(request)
                result = self.validate_semantic_data(rdf_data)
                return PluginResponse.from_validation_result(result)
            
            elif request.operation == "query":
                sparql_query = self.sparql_to_rest_adapter.extract_query(request)
                result = self.query_semantic_data(sparql_query)
                return PluginResponse.from_query_result(result)
            
            else:
                return PluginResponse.error("Unsupported semantic operation")
        
        return PluginExecutionPort(execute_handler)
```

#### 10.2.2 High-Performance Financial Port
```python
class HighPerformanceFinancialPort:
    """Domain-specific port for financial trading systems"""
    
    def __init__(self):
        # Alternative Tier 3 Technologies (performance-optimized)
        self.redis_streams = RedisStreamsClient()
        self.protobuf_serializer = ProtocolBuffersSerializer()
        self.inmemory_database = InMemoryDatabaseClient()
        self.fix_protocol_handler = FIXProtocolHandler()
        
        # Mandatory Tier 1 Compliance Adapters
        self.redis_to_cloudevents_adapter = RedisToCloudEventsAdapter()
        self.protobuf_to_json_adapter = ProtoBufToJSONAdapter()
        self.fix_to_rest_adapter = FIXToRESTAdapter()
        
        # Mandatory boundary compliance
        self.json_schema_validator = JSONSchemaValidator()
        self.otel_tracer = OpenTelemetryTracer()
    
    def execute_high_frequency_trade(self, trade_order: TradeOrder) -> TradeResult:
        """Execute trade with microsecond latency requirements"""
        
        with self.otel_tracer.start_span("financial.trade.execute") as span:
            # Alternative: Serialize using Protocol Buffers for speed
            protobuf_order = self.protobuf_serializer.serialize(trade_order)
            
            # Alternative: Store in in-memory database for ultra-fast access
            order_id = self.inmemory_database.store_order(protobuf_order)
            
            # Alternative: Execute via FIX protocol
            fix_result = self.fix_protocol_handler.execute_order(protobuf_order)
            
            # Alternative: Publish via Redis Streams for low latency
            trade_event = self.create_trade_event(order_id, fix_result)
            self.redis_streams.publish(trade_event)
            
            # Mandatory: Convert to standard compliance format
            json_result = self.protobuf_to_json_adapter.convert_trade_result(fix_result)
            standard_event = self.redis_to_cloudevents_adapter.convert_event(trade_event)
            
            # Mandatory: Validate boundary compliance
            self.json_schema_validator.validate(json_result)
            
            span.set_attributes({
                "financial.protocol": "FIX",
                "latency.optimization": "ProtoBuf + Redis Streams",
                "boundary.compliance": "JSON + CloudEvents"
            })
            
            return TradeResult.from_json_result(json_result)
    
    def stream_market_data(self, symbol: str) -> MarketDataStream:
        """Stream real-time market data with compliance adaptation"""
        
        # Alternative: High-performance Redis Streams
        redis_stream = self.redis_streams.subscribe_to_market_data(symbol)
        
        # Mandatory: Adapt to CloudEvents for HMA compliance
        cloudevents_stream = self.redis_to_cloudevents_adapter.adapt_stream(redis_stream)
        
        return MarketDataStream(cloudevents_stream)
    
    def expose_as_standard_port(self) -> PluginExecutionPort:
        """Expose financial capabilities via standard HMA port"""
        
        def execute_handler(request: PluginRequest) -> PluginResponse:
            if request.operation == "trade":
                trade_order = TradeOrder.from_json(request.data)
                result = self.execute_high_frequency_trade(trade_order)
                return PluginResponse.from_trade_result(result)
            
            elif request.operation == "market_data":
                symbol = request.parameters.get("symbol")
                stream = self.stream_market_data(symbol)
                return PluginResponse.from_market_stream(stream)
            
            else:
                return PluginResponse.error("Unsupported financial operation")
        
        return PluginExecutionPort(execute_handler)
```

#### 10.2.3 AI/ML Systems Port
```python
class AIMLSystemsPort:
    """Domain-specific port for AI/ML systems"""
    
    def __init__(self):
        # Alternative Tier 3 Technologies (ML-optimized)
        self.tensorflow_serving = TensorFlowServingClient()
        self.feast_client = FeastFeatureStoreClient()
        self.mlflow_client = MLflowClient()
        self.tfx_validator = TensorFlowDataValidation()
        
        # Mandatory Tier 1 Compliance Adapters
        self.tfx_to_json_adapter = TFXToJSONSchemaAdapter()
        self.feast_to_rest_adapter = FeastToRESTAdapter()
        self.mlflow_to_api_adapter = MLflowToAPIAdapter()
        
        # Mandatory boundary compliance
        self.json_schema_validator = JSONSchemaValidator()
        self.otel_tracer = OpenTelemetryTracer()
    
    def validate_ml_data(self, dataset: MLDataset) -> MLValidationResult:
        """Validate ML data using TensorFlow Data Validation"""
        
        with self.otel_tracer.start_span("ml.data.validation") as span:
            # Alternative: TensorFlow Data Validation for ML-specific checks
            tfx_result = self.tfx_validator.validate_dataset(dataset)
            
            # Mandatory: Convert to standard validation format
            json_result = self.tfx_to_json_adapter.convert_validation_result(tfx_result)
            
            # Mandatory: Validate boundary compliance
            self.json_schema_validator.validate(json_result)
            
            span.set_attributes({
                "ml.validator": "TensorFlow Data Validation",
                "dataset.features": len(dataset.features),
                "validation.anomalies": len(tfx_result.anomalies)
            })
            
            return MLValidationResult.from_json(json_result)
    
    def serve_ml_model(self, model_request: MLModelRequest) -> MLPrediction:
        """Serve ML model predictions with standard API compliance"""
        
        # Alternative: Get features from Feast feature store
        features = self.feast_client.get_online_features(
            model_request.feature_names,
            model_request.entity_ids
        )
        
        # Alternative: Serve prediction via TensorFlow Serving
        prediction = self.tensorflow_serving.predict(
            model_request.model_name,
            features
        )
        
        # Mandatory: Convert to standard API response
        rest_response = self.feast_to_rest_adapter.convert_prediction(prediction)
        
        # Mandatory: Validate boundary compliance
        self.json_schema_validator.validate(rest_response)
        
        return MLPrediction.from_rest_response(rest_response)
    
    def expose_as_standard_port(self) -> PluginExecutionPort:
        """Expose ML capabilities via standard HMA port"""
        
        def execute_handler(request: PluginRequest) -> PluginResponse:
            if request.operation == "validate_data":
                dataset = MLDataset.from_json(request.data)
                result = self.validate_ml_data(dataset)
                return PluginResponse.from_ml_validation(result)
            
            elif request.operation == "predict":
                model_request = MLModelRequest.from_json(request.data)
                prediction = self.serve_ml_model(model_request)
                return PluginResponse.from_ml_prediction(prediction)
            
            else:
                return PluginResponse.error("Unsupported ML operation")
        
        return PluginExecutionPort(execute_handler)
```

### 10.3 Port Technology Selection Framework (NEW in v2.2)

```yaml
port_technology_selection:
  decision_matrix:
    standard_business_logic:
      recommended_tier: "tier_2"
      technologies: ["HTTP/2 + gRPC", "NATS messaging", "Prometheus metrics"]
      rationale: "Proven reliability, broad compatibility, community support"
      
    high_performance_requirements:
      recommended_tier: "tier_3_with_adapters"
      technologies: ["Protocol Buffers", "Redis Streams", "Custom serialization"]
      rationale: "Performance optimization with compliance maintained"
      compliance_strategy: "Boundary adapters for JSON/CloudEvents"
      
    domain_specific_optimization:
      recommended_tier: "tier_3_with_adapters"
      technologies: ["SHACL", "SPARQL", "TensorFlow serving", "FIX protocol"]
      rationale: "Domain expertise and specialized capabilities"
      compliance_strategy: "Domain-to-standard adapters"
      
    real_time_requirements:
      recommended_tier: "tier_2_with_tier_3_optimization"
      technologies: ["WebSockets + NATS", "gRPC streaming", "Redis pub/sub"]
      rationale: "Balance of real-time capability and standard compliance"
      
  implementation_guidelines:
    tier_1_compliance:
      always_required:
        - "JSON Schema validation at boundaries"
        - "OpenTelemetry telemetry emission"
        - "TLS/mTLS secure communication"
        - "CloudEvents format for events"
      
    tier_2_defaults:
      start_with:
        - "HTTP/2 for synchronous communication"
        - "gRPC for high-performance synchronous"
        - "NATS for simple event-driven communication"
        - "Kafka for enterprise event streaming"
        - "Prometheus for metrics collection"
      
    tier_3_alternatives:
      use_when:
        - "Performance requirements exceed Tier 2 capabilities"
        - "Domain-specific protocols provide significant benefits"
        - "Specialized validation or processing is required"
        - "Integration with existing alternative systems"
      requirements:
        - "Documented performance/capability benefits"
        - "Compliance adapters for boundary compatibility"
        - "Migration plan back to Tier 2 if needed"
        - "Team expertise in alternative technology"
```

## 11. Enhanced Plugin Lifecycle Management with Technology Integration (v2.2)

### 11.1 Technology-Aware Plugin States and Transitions

**Enhanced Plugin States with Technology Classification:**
```yaml
enhanced_plugin_states:
  discovery_and_classification:
    - "Discovered: Plugin package detected"
    - "Technology_Assessment: Analyzing technology tier and dependencies"
    - "Compliance_Planning: Planning compliance adapters if needed"
    
  validation_and_preparation:
    - "Schema_Validated: Manifest.json v2.2 schema validation passed"
    - "Technology_Validated: Technology stack validation completed"
    - "Adapter_Prepared: Compliance adapters initialized if required"
    
  deployment_and_activation:
    - "Deploying: Plugin being deployed with recommended technologies"
    - "Health_Checking: Verifying plugin health with monitoring stack"
    - "Activated: Plugin ready for execution with full observability"
    
  runtime_management:
    - "Running: Plugin actively processing with technology optimization"
    - "Adaptive_Mode: Plugin adjusting technology usage based on performance"
    - "Fallback_Mode: Plugin using baseline technologies due to issues"
    
  maintenance_and_evolution:
    - "Upgrading: Plugin technology stack being updated"
    - "Migrating: Moving between technology tiers"
    - "Deactivating: Graceful shutdown with cleanup"
```

### 11.2 Technology-Guided Plugin Compliance (Enhanced in v2.2)

#### 11.2.1 Baseline Compliance with Technology Requirements

```python
class TechnologyGuidedPluginValidator:
    """Enhanced plugin validator with technology guidance"""
    
    def __init__(self):
        # Technology validation clients
        self.k8s_validator = KubernetesManifestValidator()
        self.docker_validator = DockerImageValidator()
        self.security_scanner = ContainerSecurityScanner()
        
        # Compliance validation
        self.schema_validator = PluginManifestSchemaValidator()
        self.port_validator = PortContractValidator()
        self.adapter_validator = ComplianceAdapterValidator()
    
    def validate_plugin_with_technology_guidance(self, plugin_manifest: PluginManifest) -> ValidationResult:
        """Comprehensive validation with technology recommendations"""
        
        validation_result = ValidationResult()
        
        # 1. MANDATORY: Schema validation
        schema_result = self.schema_validator.validate_v2_2_schema(plugin_manifest)
        validation_result.add_result("schema", schema_result)
        
        # 2. Technology tier assessment
        tech_assessment = self.assess_technology_tier(plugin_manifest)
        validation_result.add_result("technology_assessment", tech_assessment)
        
        # 3. Compliance strategy validation
        if tech_assessment.tier == "alternative":
            adapter_result = self.validate_compliance_adapters(plugin_manifest)
            validation_result.add_result("compliance_adapters", adapter_result)
        
        # 4. Deployment technology validation
        deployment_result = self.validate_deployment_technology(plugin_manifest)
        validation_result.add_result("deployment", deployment_result)
        
        # 5. Security and observability validation
        security_result = self.validate_security_compliance(plugin_manifest)
        observability_result = self.validate_observability_compliance(plugin_manifest)
        validation_result.add_result("security", security_result)
        validation_result.add_result("observability", observability_result)
        
        return validation_result
    
    def assess_technology_tier(self, manifest: PluginManifest) -> TechnologyAssessment:
        """Assess plugin technology tier and provide recommendations"""
        
        assessment = TechnologyAssessment()
        
        # Analyze declared technologies
        declared_tech = manifest.compliance.get("technology_stack", {})
        
        # Classify technology tier
        if self.uses_only_mandatory_standards(declared_tech):
            assessment.tier = "mandatory"
            assessment.recommendations = self.get_tier_2_upgrade_recommendations(declared_tech)
        
        elif self.uses_recommended_technologies(declared_tech):
            assessment.tier = "recommended"
            assessment.validation_status = "compliant"
        
        elif self.uses_alternative_technologies(declared_tech):
            assessment.tier = "alternative"
            assessment.required_adapters = self.identify_required_adapters(declared_tech)
            assessment.validation_requirements = self.get_adapter_validation_requirements()
        
        # Performance and operational assessment
        assessment.performance_profile = self.assess_performance_characteristics(declared_tech)
        assessment.operational_complexity = self.assess_operational_complexity(declared_tech)
        assessment.team_readiness = self.assess_team_readiness_requirements(declared_tech)
        
        return assessment
    
    def validate_compliance_adapters(self, manifest: PluginManifest) -> AdapterValidationResult:
        """Validate compliance adapters for alternative technologies"""
        
        result = AdapterValidationResult()
        alternative_tech = manifest.compliance.get("alternative_technologies", [])
        
        for tech in alternative_tech:
            adapter_config = tech.get("compliance_adapter")
            if not adapter_config:
                result.add_error(f"Missing compliance adapter for {tech['technology']}")
                continue
            
            # Validate adapter implementation
            adapter_validation = self.adapter_validator.validate_adapter(
                tech["technology"], 
                adapter_config
            )
            result.add_adapter_result(tech["technology"], adapter_validation)
            
            # Test adapter functionality
            if adapter_validation.valid:
                functional_test = self.test_adapter_functionality(adapter_config)
                result.add_functional_test(tech["technology"], functional_test)
        
        return result
    
    def validate_deployment_technology(self, manifest: PluginManifest) -> DeploymentValidationResult:
        """Validate deployment technology choices"""
        
        deployment_config = manifest.deployment
        result = DeploymentValidationResult()
        
        # Validate container configuration
        if deployment_config.get("container_image"):
            container_result = self.docker_validator.validate_image(
                deployment_config["container_image"]
            )
            result.add_result("container", container_result)
            
            # Security scan
            security_scan = self.security_scanner.scan_image(
                deployment_config["container_image"]
            )
            result.add_result("security_scan", security_scan)
        
        # Validate Kubernetes configuration
        if deployment_config.get("kubernetes_manifest"):
            k8s_result = self.k8s_validator.validate_manifest(
                deployment_config["kubernetes_manifest"]
            )
            result.add_result("kubernetes", k8s_result)
        
        # Validate resource requirements
        resource_result = self.validate_resource_requirements(deployment_config)
        result.add_result("resources", resource_result)
        
        return result
```

#### 11.2.2 Runtime Technology Adaptation (NEW in v2.2)

```python
class RuntimeTechnologyManager:
    """Manages plugin technology adaptation at runtime"""
    
    def __init__(self):
        self.performance_monitor = PerformanceMonitor()
        self.health_checker = HealthChecker()
        self.fallback_manager = FallbackManager()
        self.metrics_collector = MetricsCollector()
    
    def monitor_plugin_performance(self, plugin_id: str) -> PerformanceMetrics:
        """Monitor plugin performance and suggest technology optimizations"""
        
        metrics = self.performance_monitor.collect_metrics(plugin_id)
        
        # Analyze performance patterns
        analysis = self.analyze_performance_patterns(metrics)
        
        # Generate technology recommendations
        if analysis.suggests_optimization():
            recommendations = self.generate_technology_recommendations(analysis)
            self.log_optimization_suggestions(plugin_id, recommendations)
        
        # Check for fallback requirements
        if analysis.suggests_fallback():
            self.initiate_technology_fallback(plugin_id, analysis.fallback_reason)
        
        return metrics
    
    def initiate_technology_fallback(self, plugin_id: str, reason: str) -> FallbackResult:
        """Fallback to more reliable technology tier"""
        
        plugin = self.get_plugin(plugin_id)
        current_tier = plugin.get_technology_tier()
        
        if current_tier == "alternative":
            # Fallback to recommended technologies
            fallback_result = self.fallback_manager.fallback_to_recommended(plugin_id, reason)
            
        elif current_tier == "recommended":
            # Fallback to mandatory baseline
            fallback_result = self.fallback_manager.fallback_to_mandatory(plugin_id, reason)
        
        else:
            # Already at baseline, investigate deeper issues
            fallback_result = FallbackResult.no_fallback_available(reason)
        
        # Log fallback action
        self.log_technology_fallback(plugin_id, current_tier, fallback_result)
        
        return fallback_result
    
    def suggest_technology_upgrade(self, plugin_id: str) -> UpgradeRecommendation:
        """Suggest technology tier upgrade based on performance and stability"""
        
        plugin = self.get_plugin(plugin_id)
        performance_history = self.get_performance_history(plugin_id)
        
        # Analyze upgrade potential
        if self.meets_upgrade_criteria(performance_history):
            current_tier = plugin.get_technology_tier()
            
            if current_tier == "mandatory":
                return UpgradeRecommendation.to_recommended(
                    performance_history, 
                    self.get_recommended_technologies_for_plugin(plugin)
                )
            
            elif current_tier == "recommended":
                return UpgradeRecommendation.to_alternative(
                    performance_history,
                    self.get_alternative_optimizations_for_plugin(plugin)
                )
        
        return UpgradeRecommendation.no_upgrade_recommended()
```

---

**This enhanced internal components specification provides clear technology guidance while maintaining HMA's core principles of modularity, autonomy, and replaceability. The three-tier technology framework enables informed technology choices that balance proven reliability with specialized optimization.**