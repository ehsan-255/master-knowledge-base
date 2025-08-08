# HMA v1.3 to v2.0 Migration Guide

## Overview
This guide helps organizations migrate from HMA v1.3 to v2.0 implementations.

## Key Changes Summary
- Added mandatory dependencies for interoperability
- Enhanced security requirements
- Formalized plugin manifest schema
- Added reference implementation guidance

## Migration Sequence
**Recommended: 5 phases for complete migration**

### Phase 1: Security Foundations
- Implement mTLS for internal communication
- Deploy secure secrets backend
- Update credential management workflows

### Phase 2: Observability Standards
- Deploy OpenTelemetry SDK across all components
- Implement standardized telemetry emission
- Deploy reference observability stack

### Phase 3: Contract Validation
- Implement JSON Schema validation libraries
- Add OpenAPI specifications for all APIs
- Deploy automated contract testing

### Phase 4: Plugin Standardization
- Update all plugins with manifest.json files
- Implement plugin manifest validation
- Deploy code signing (if applicable)

### Phase 5: Validation and Optimization
- Complete compliance testing
- Optimize performance with new standards
- Full reference implementation adoption

## Backward Compatibility
- v2.0 is architecturally compatible with v1.3
- Mandatory dependencies are additive
- Existing plugins work with manifest addition
- No breaking changes to core interfaces

## Detailed Migration Steps

### Phase 1: Security Foundations (Weeks 1-2)

#### Step 1.1: mTLS Implementation
```bash
# 1. Generate certificates for all components
# 2. Configure Core to use mTLS
# 3. Update plugin communication
# 4. Test certificate rotation
```

#### Step 1.2: Secure Secrets Backend
```bash
# Option A: HashiCorp Vault
# 1. Deploy Vault cluster
# 2. Configure CredentialBroker integration
# 3. Migrate existing secrets
# 4. Test credential vending

# Option B: External Secrets Operator
# 1. Deploy ESO in Kubernetes
# 2. Configure secret synchronization
# 3. Update CredentialBroker configuration
```

#### Step 1.3: Validation Checklist
- [ ] All internal communication uses mTLS
- [ ] CredentialBroker integrated with secure backend
- [ ] No static secrets in configurations
- [ ] Certificate rotation tested

### Phase 2: Observability Standards (Weeks 3-4)

#### Step 2.1: OTEL SDK Deployment
```yaml
# Core configuration
otel:
  resource:
    attributes:
      hma.component.type: "L2-Core"
      hma.component.id: "hma-core"
      hma.layer: "L2"
  exporters:
    jaeger: "http://jaeger:14268/api/traces"
    prometheus: "http://prometheus:9090/api/v1/write"
```

#### Step 2.2: Plugin Updates
```python
# Plugin OTEL integration
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

# Initialize with HMA conventions
tracer = trace.get_tracer(
    "hma.l3.user_management",
    version="1.0.0"
)
```

#### Step 2.3: Observability Stack
```docker-compose
version: '3.8'
services:
  prometheus:
    image: prom/prometheus:latest
  grafana:
    image: grafana/grafana:latest
  jaeger:
    image: jaegertracing/all-in-one:latest
  loki:
    image: grafana/loki:latest
```

#### Step 2.4: Validation Checklist
- [ ] All components emit OTEL telemetry
- [ ] Traces correlate across plugin boundaries
- [ ] Metrics follow HMA naming conventions
- [ ] Dashboards show end-to-end flows

### Phase 3: Contract Validation (Weeks 5-6)

#### Step 3.1: JSON Schema Implementation
```javascript
// Port contract validation
const Ajv = require('ajv');
const ajv = new Ajv();

const pluginExecutionSchema = {
  type: 'object',
  properties: {
    operation: { type: 'string' },
    parameters: { type: 'object' },
    metadata: { type: 'object' }
  },
  required: ['operation', 'parameters']
};

const validate = ajv.compile(pluginExecutionSchema);
```

#### Step 3.2: OpenAPI Documentation
```yaml
# L1 Adapter API specification
openapi: 3.0.0
info:
  title: HMA System API
  version: 2.0.0
paths:
  /api/v1/execute:
    post:
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ExecutionRequest'
```

#### Step 3.3: Event Schema Validation
```json
{
  "eventSchema": {
    "type": "object",
    "properties": {
      "eventId": { "type": "string", "format": "uuid" },
      "eventType": { "type": "string" },
      "eventVersion": { "type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$" },
      "source": { "type": "string" },
      "timestamp": { "type": "string", "format": "date-time" },
      "data": { "type": "object" }
    },
    "required": ["eventId", "eventType", "eventVersion", "source", "timestamp"]
  }
}
```

#### Step 3.4: Validation Checklist
- [ ] All ports validate input/output with JSON Schema
- [ ] L1 Adapters documented with OpenAPI
- [ ] Events validated against schemas
- [ ] Validation errors properly handled

### Phase 4: Plugin Standardization (Weeks 7-8)

#### Step 4.1: Plugin Manifest Creation
```json
{
  "manifestVersion": "2.0",
  "hmaVersion": "2.0",
  "plugin": {
    "id": "user-management",
    "name": "User Management Plugin",
    "version": "1.2.3",
    "type": "L3-Capability",
    "description": "Handles user authentication and authorization"
  },
  "interfaces": {
    "implementedPorts": [
      {
        "name": "UserManagementPort",
        "version": "1.0",
        "contract": "schemas/user-management-port.json"
      }
    ],
    "consumedPorts": [
      {
        "name": "CredBrokerQueryPort",
        "version": "1.0",
        "required": true
      }
    ]
  },
  "dependencies": {
    "infrastructure": ["postgresql", "redis"]
  }
}
```

#### Step 4.2: Plugin Lifecycle Manager Updates
```python
# Enhanced lifecycle manager
class PluginLifecycleManager:
    def validate_manifest(self, manifest_path):
        """Validate plugin manifest against v2.0 schema"""
        with open(manifest_path) as f:
            manifest = json.load(f)
        
        # Validate against schema
        validate = ajv.compile(PLUGIN_MANIFEST_SCHEMA)
        if not validate(manifest):
            raise ValidationError(validate.errors)
        
        return manifest
    
    def activate_plugin(self, plugin_id):
        """Enhanced activation with manifest validation"""
        manifest = self.validate_manifest(f"{plugin_id}/manifest.json")
        
        # Check dependencies
        self.verify_dependencies(manifest.get('dependencies', {}))
        
        # Validate interfaces
        self.validate_interfaces(manifest.get('interfaces', {}))
        
        # Proceed with activation
        super().activate_plugin(plugin_id)
```

#### Step 4.3: Code Signing (Optional)
```bash
# GPG signing for plugins
gpg --armor --detach-sign plugin-package.tar.gz

# Verification in lifecycle manager
gpg --verify plugin-package.tar.gz.asc plugin-package.tar.gz
```

#### Step 4.4: Validation Checklist
- [ ] All plugins have valid manifest.json files
- [ ] Plugin Lifecycle Manager validates manifests
- [ ] Interface declarations match actual implementations
- [ ] Code signing implemented (if applicable)

### Phase 5: Validation and Optimization (Weeks 9-10)

#### Step 5.1: Compliance Testing
```python
# Automated compliance tests
class HMAComplianceTests:
    def test_otel_integration(self):
        """Verify all components emit OTEL telemetry"""
        pass
    
    def test_mtls_communication(self):
        """Verify internal communication uses mTLS"""
        pass
    
    def test_schema_validation(self):
        """Verify all data is schema-validated"""
        pass
    
    def test_plugin_manifests(self):
        """Verify all plugins have valid manifests"""
        pass
```

#### Step 5.2: Performance Optimization
```bash
# Optimize OTEL sampling
# Tune schema validation caching
# Optimize certificate handling
# Monitor resource usage
```

#### Step 5.3: Reference Implementation Adoption
```yaml
# Complete reference stack
observability:
  metrics: prometheus
  tracing: jaeger
  logging: loki
  
eventbus:
  implementation: nats
  
secrets:
  backend: vault
```

#### Step 5.4: Final Validation Checklist
- [ ] All compliance tests pass
- [ ] Performance meets requirements
- [ ] Monitoring shows healthy system
- [ ] Documentation updated
- [ ] Team training completed

## Rollback Plan

### Emergency Rollback
1. Disable v2.0 validation temporarily
2. Revert to v1.3 configuration
3. Remove mandatory dependencies
4. Restore previous monitoring

### Gradual Rollback
1. Phase-by-phase rollback
2. Maintain security improvements
3. Keep observability enhancements
4. Document lessons learned

## Success Metrics

### Technical Metrics
- 100% plugin manifest compliance
- Zero validation errors in production
- Complete trace correlation across plugins
- All security controls operational

### Operational Metrics
- Reduced integration time between teams
- Faster plugin deployment cycles
- Improved system observability
- Enhanced security posture

## Support and Resources

### Documentation
- [[HMA v2.0 - Part 1a - Mandatory Dependencies and Standards]]
- Reference implementation examples
- Best practices guides

### Tools
- Manifest validation CLI
- Compliance testing framework
- Migration scripts

### Training
- v2.0 features overview
- Security best practices
- Observability patterns
- Plugin development guidelines

---

**Migration Timeline:** 10 weeks for complete transition
**Team Effort:** 2-3 engineers, part-time
**Rollback Time:** 1-2 days if needed
**Business Impact:** Minimal, primarily additive enhancements 