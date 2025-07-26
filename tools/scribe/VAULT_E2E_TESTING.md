# Vault End-to-End Testing Guide

## Overview

This document describes the comprehensive end-to-end testing suite for HashiCorp Vault integration in Scribe HMA v2.2. The test suite validates the complete secret lifecycle, enterprise resilience patterns, and observability integration.

## Architecture Validation

The E2E tests validate the following enterprise-grade components:

### 🔐 Core Vault Integration
- **VaultSecretProvider**: Secret management with caching and authentication
- **VaultPolicyManager**: Enterprise policy management and AppRole configuration
- **VaultRotationManager**: Automated secret and certificate rotation
- **VaultMetricsCollector**: Comprehensive Prometheus and OTLP metrics
- **VaultOTLPIntegration**: OpenTelemetry traces and metrics export

### 🛡️ Enterprise Resilience Patterns
- **Circuit Breaker**: Fault tolerance with automatic recovery
- **Retry Handler**: Exponential backoff with jitter anti-thundering herd
- **Graceful Degradation**: Service continuity during Vault outages
- **Comprehensive Fallbacks**: Filesystem and cache-based fallback strategies

### 📊 Observability & Monitoring
- **Prometheus Metrics**: 20+ comprehensive metrics for all operations
- **Grafana Dashboards**: 3 professional dashboards for monitoring
- **OTLP Integration**: Full OpenTelemetry traces and metrics
- **Alerting Rules**: 25+ alert rules for proactive monitoring

## Test Categories

### 1. Connectivity & Authentication Tests
- Basic Vault server connectivity validation
- Complete authentication flow with metrics recording
- Authentication failure handling and circuit breaker behavior
- Token validation and refresh mechanisms

### 2. Secret Operations Tests
- Complete secret write/read cycle with caching validation
- Secret versioning and historical access
- Cache expiration and refresh mechanisms
- Multi-tenant secret isolation

### 3. Certificate Lifecycle Tests
- Certificate generation with validation
- Temporary file creation with secure permissions
- Certificate rotation and renewal
- PKI policy compliance

### 4. Rotation Lifecycle Tests
- Rotation job registration and execution
- Scheduled rotation system operation
- Manual rotation triggers
- Rollback mechanisms and failure handling

### 5. Resilience Pattern Tests
- Circuit breaker operation under failure conditions
- Retry mechanism with exponential backoff
- Graceful degradation under various failure scenarios
- Service mode transitions (Normal → Degraded → Emergency)

### 6. Metrics & Observability Tests
- Metrics collection across all operations
- OTLP integration and telemetry export
- Prometheus metrics endpoint validation
- OpenTelemetry span creation and attributes

### 7. Performance & Load Tests
- Concurrent secret operations performance
- Certificate generation performance benchmarks
- Load testing under realistic conditions
- Memory and resource utilization validation

### 8. Integration Tests
- Vault server integration with live services
- OTLP collector integration and health checks
- Prometheus metrics export validation
- Grafana dashboard data sources

### 9. Complete Lifecycle Scenario
- End-to-end scenario with all components
- Multi-phase workflow validation
- Cross-component integration verification
- Enterprise compliance validation

## Running the Tests

### Prerequisites

1. **Docker & Docker Compose**: Required for service orchestration
2. **Python 3.10+**: With test dependencies installed
3. **Network Access**: Ports 8200, 4317, 8889, 3000 available

### Quick Start

```bash
# Navigate to project root
cd /path/to/scribe-hma-v2.2

# Install test dependencies
pip install -e ".[test]"

# Run the complete E2E test suite
python test-environment/run_vault_e2e_tests.py
```

### Manual Test Execution

```bash
# Start Docker stack manually
cd tools/scribe/deployment
docker-compose -f docker-compose.runtime.yml up -d

# Wait for services to be healthy (2-3 minutes)
# Run specific test categories
pytest test-environment/scribe-tests/test_vault_e2e_lifecycle.py::TestVaultConnectivityAndAuthentication -v
pytest test-environment/scribe-tests/test_vault_e2e_lifecycle.py::TestSecretOperations -v
pytest test-environment/scribe-tests/test_vault_e2e_lifecycle.py::TestCertificateLifecycle -v
pytest test-environment/scribe-tests/test_vault_e2e_lifecycle.py::TestRotationLifecycle -v
pytest test-environment/scribe-tests/test_vault_e2e_lifecycle.py::TestResiliencePatterns -v
pytest test-environment/scribe-tests/test_vault_e2e_lifecycle.py::TestMetricsAndObservability -v
pytest test-environment/scribe-tests/test_vault_e2e_lifecycle.py::TestPerformanceAndLoad -v
pytest test-environment/scribe-tests/test_vault_e2e_lifecycle.py::TestIntegrationWithExternalServices -v
pytest test-environment/scribe-tests/test_vault_e2e_lifecycle.py::TestFullEndToEndScenario -v

# Cleanup
docker-compose -f docker-compose.runtime.yml down -v
```

### Environment Configuration

The tests use the following environment variables:

```bash
# Vault Configuration
VAULT_ADDR=http://localhost:8200
VAULT_TOKEN=dev-only-token
VAULT_AUTH_METHOD=token

# OTLP Configuration
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
OTEL_SERVICE_NAME=scribe-vault-e2e-test
OTEL_RESOURCE_ATTRIBUTES_ENVIRONMENT=test

# Test Configuration
PYTHONPATH=/path/to/project/root
```

## Test Results & Reporting

### Automated Reporting

The test runner generates comprehensive reports including:

- **Test Summary**: Pass/fail counts, duration, coverage
- **Performance Metrics**: Operation timing, throughput measurements
- **Integration Status**: Service health, connectivity validation
- **Error Analysis**: Detailed failure information and stack traces

### Success Criteria

Tests are considered successful when:

✅ **All Core Operations**: 100% pass rate for basic operations  
✅ **Resilience Patterns**: Circuit breakers, retries, degradation work correctly  
✅ **Performance Standards**: Operations complete within acceptable time limits  
✅ **Integration Health**: All external services respond correctly  
✅ **Security Compliance**: Authentication, authorization, and encryption work  
✅ **Observability**: Metrics, traces, and logs are generated correctly  

### Sample Test Output

```
🔐 VAULT END-TO-END TEST RESULTS - SCRIBE HMA v2.2
================================================================================
Timestamp: 2024-01-15 10:30:45
Overall Result: ✅ PASSED
Return Code: 0

📊 Test Configuration:
  Vault URL: http://localhost:8200
  OTLP Endpoint: http://localhost:4317
  Test Timeout: 300s

📈 Test Summary:
  Total Tests: 28
  Passed: 28
  Failed: 0
  Skipped: 0
  Duration: 87.3s

🧪 Test Details:
  ✅ test_vault_connectivity (2.1s)
  ✅ test_vault_authentication_flow (1.8s)
  ✅ test_secret_write_read_cycle (3.2s)
  ✅ test_certificate_generation_and_validation (4.7s)
  ✅ test_rotation_job_registration_and_execution (8.3s)
  ✅ test_circuit_breaker_operation (5.9s)
  ✅ test_metrics_collection (2.4s)
  ✅ test_complete_vault_lifecycle_scenario (15.8s)
  ...

🏁 Test Execution Summary:
  Services Started: ✅
  Docker Environment: ✅
  Overall Success: ✅
```

## Monitoring Integration Validation

### Prometheus Metrics

The tests validate the following metrics are properly exported:

```promql
# Authentication metrics
scribe_vault_auth_attempts_total
scribe_vault_auth_duration_seconds

# Secret operation metrics
scribe_vault_secret_operations_total
scribe_vault_secret_operation_duration_seconds
scribe_vault_secret_cache_size
scribe_vault_secret_cache_hit_ratio

# Certificate metrics
scribe_vault_certificate_operations_total
scribe_vault_certificate_generation_duration_seconds
scribe_vault_certificate_expiry_seconds

# Rotation metrics
scribe_vault_rotation_operations_total
scribe_vault_rotation_duration_seconds
scribe_vault_rotation_queue_size

# Resilience metrics
scribe_vault_circuit_breaker_state
scribe_vault_circuit_breaker_trips_total
scribe_vault_retry_attempts_total
scribe_vault_degradation_events_total

# Connectivity metrics
scribe_vault_vault_connectivity
scribe_vault_vault_response_time_seconds
```

### Grafana Dashboards

The tests verify the following dashboards are functional:

1. **Vault Operations Overview**: High-level operational metrics
2. **Vault Secret Lifecycle**: Detailed secret and rotation monitoring
3. **Vault Resilience Monitoring**: Circuit breakers, retries, degradation

### Alert Rules

Validation includes 25+ alert rules covering:

- Authentication failure rates
- Certificate expiration warnings
- Service degradation events
- Circuit breaker trips
- Performance thresholds

## Troubleshooting

### Common Issues

**Services Not Starting**
```bash
# Check Docker daemon
docker info

# Check port availability
netstat -an | grep -E "(8200|4317|8889|3000)"

# Review Docker logs
docker-compose logs vault
docker-compose logs otel-collector
```

**Test Failures**
```bash
# Run tests with detailed output
pytest -v -s --tb=long test-environment/scribe-tests/test_vault_e2e_lifecycle.py

# Check service health
curl http://localhost:8200/v1/sys/health
curl http://localhost:13133
```

**Performance Issues**
```bash
# Increase timeouts
export PYTEST_TIMEOUT=600

# Check system resources
docker stats
```

### Log Analysis

Key log locations:
- **Vault**: `docker-compose logs vault`
- **OTLP Collector**: `docker-compose logs otel-collector`
- **Test Output**: `vault_e2e_report_*.txt`
- **Application Logs**: Structured JSON logs from test execution

## Professional Validation

This comprehensive test suite validates enterprise-grade capabilities:

🔒 **Security**: Multi-tier authentication, policy isolation, mTLS certificates  
🔄 **Reliability**: Circuit breakers, retries, graceful degradation, rollbacks  
📊 **Observability**: Prometheus metrics, OpenTelemetry traces, Grafana dashboards  
⚡ **Performance**: Sub-second operations, concurrent request handling, load testing  
🔧 **Operations**: Automated rotation, health monitoring, failure detection  
🏗️ **Architecture**: HMA v2.2 compliance, microkernel patterns, loose coupling  

The test suite provides comprehensive validation that the Vault integration meets enterprise production requirements for security, reliability, and operational excellence.