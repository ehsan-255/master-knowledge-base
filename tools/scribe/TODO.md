# Scribe Engine TODO & Task Tracking

## Overview

This document tracks all pending tasks, improvements, and technical debt for the Scribe Engine following the HMA v2.2 compliance implementation.

**Last Updated**: July 24, 2025  
**Status**: Post-HMA v2.2 Implementation Tasks

---

## 🔥 Critical Priority

### CRIT-001: SHACL Adapter Real Implementation
**Status**: Mock implementation needs production code  
**Effort**: Medium (1-2 days)  
**Description**: Replace simulation code with real SHACL validation using pyshacl

**Tasks**:
- [ ] Add `pyshacl = "^0.25.0"` and `rdflib = "^7.0.0"` to pyproject.toml
- [ ] Replace `_simulate_shacl_validation()` with real `pyshacl.validate()` calls
- [ ] Implement `_extract_shacl_violations()` using SPARQL queries on results graph
- [ ] Add RDF format detection (Turtle, RDF/XML, JSON-LD)
- [ ] Add shapes graph caching for performance
- [ ] Implement comprehensive error handling for malformed RDF

**Files**: `adapters/shacl_adapter.py`

### CRIT-002: Security Policy Deployment Setup
**Status**: External YAML configuration needs deployment guide  
**Effort**: Medium (1-2 days)  
**Description**: Create production-ready security policy deployment

**Tasks**:
- [ ] Create `/etc/scribe/security_policy.yaml` template with full configuration
- [ ] Document mTLS certificate generation process
- [ ] Create Dockerfile with proper certificate handling
- [ ] Create Kubernetes ConfigMap and Secret manifests
- [ ] Update `security_manager.py` with proper policy loading and validation
- [ ] Document environment variable overrides
- [ ] Create deployment checklist for production

**Files**: `core/security_manager.py`, new deployment files

---

## 🟡 High Priority

### HIGH-001: NATS Operational Setup
**Status**: Core dependency needs operational guide  
**Effort**: Medium (1 day)  
**Description**: Document NATS broker deployment and configuration

**Tasks**:
- [ ] Create NATS broker configuration templates
- [ ] Document clustering setup for high availability
- [ ] Add connection retry and failover logic
- [ ] Create health checks for NATS connectivity
- [ ] Document monitoring and alerting setup

**Files**: `core/adapters/nats_adapter.py`, deployment docs

### HIGH-002: Dependencies Update
**Status**: Missing production dependencies  
**Effort**: Small (2 hours)  
**Description**: Update pyproject.toml with all required dependencies

**Tasks**:
- [ ] Add `nats-py` for NATS adapter
- [ ] Add `pyshacl` and `rdflib` for SHACL validation
- [ ] Add `opentelemetry-api` and related packages
- [ ] Pin dependency versions for stability
- [ ] Update lock file and test installations

**Files**: `pyproject.toml`

### HIGH-003: Testing Framework
**Status**: No tests for new HMA v2.2 code  
**Effort**: Large (3-4 days)  
**Description**: Implement comprehensive test suite

**Tasks**:
- [ ] Set up pytest framework and test structure
- [ ] Unit tests for all port adapters
- [ ] Integration tests for NATS event bus
- [ ] Mock tests for SHACL adapter with real pyshacl
- [ ] End-to-end tests for file processing orchestrator
- [ ] Security policy validation tests
- [ ] Performance benchmarks for async workflows

**Files**: New `tests/` directory

---

## 🟢 Medium Priority

### MED-001: Windows Compatibility Validation
**Status**: Windows-specific code needs testing  
**Effort**: Small (4 hours)  
**Description**: Test Windows-specific atomic write implementation

**Tasks**:
- [ ] Test `core/windows_atomic_write.py` on Windows systems
- [ ] Validate file locking behavior
- [ ] Test concurrent access scenarios
- [ ] Add error handling for permission issues
- [ ] Document Windows-specific deployment notes

**Files**: `core/windows_atomic_write.py`

### MED-002: Plugin Loader Dependency Resolution
**Status**: Complex logic needs real-world testing  
**Effort**: Medium (1 day)  
**Description**: Validate plugin dependency resolution in production scenarios

**Tasks**:
- [ ] Test circular dependency detection
- [ ] Test missing dependency handling
- [ ] Validate load order with complex dependency graphs
- [ ] Add dependency visualization tools
- [ ] Performance test with large plugin sets

**Files**: `core/plugin_loader.py`

### MED-003: Error Handling Edge Cases
**Status**: Some error paths not fully tested  
**Effort**: Medium (1 day)  
**Description**: Improve error handling robustness

**Tasks**:
- [ ] Add timeout handling for all async operations
- [ ] Implement circuit breaker pattern for external services
- [ ] Add retry logic with exponential backoff
- [ ] Improve error message clarity and actionability
- [ ] Add error correlation IDs for debugging

**Files**: Multiple core modules

### MED-004: Performance Optimization
**Status**: Async patterns need performance tuning  
**Effort**: Medium (1-2 days)  
**Description**: Optimize performance for high-throughput scenarios

**Tasks**:
- [ ] Profile async event processing bottlenecks
- [ ] Implement connection pooling for NATS
- [ ] Add metrics collection for performance monitoring
- [ ] Optimize file I/O operations
- [ ] Add caching for frequently accessed configurations

**Files**: Core adapters and engine

---

## 🔵 Low Priority

### LOW-001: Documentation Gaps
**Status**: Some areas need better documentation  
**Effort**: Medium (1 day)  
**Description**: Complete documentation coverage

**Tasks**:
- [ ] Add inline API documentation for all public methods
- [ ] Create troubleshooting guide
- [ ] Document performance tuning recommendations
- [ ] Add architectural decision records (ADRs) for key decisions
- [ ] Create developer onboarding guide

**Files**: Various, new docs

### LOW-002: Monitoring & Observability
**Status**: Basic OTEL setup needs enhancement  
**Effort**: Large (2-3 days)  
**Description**: Implement comprehensive observability

**Tasks**:
- [ ] Add custom metrics for business logic
- [ ] Implement distributed tracing correlation
- [ ] Set up log aggregation and structured logging
- [ ] Create monitoring dashboards
- [ ] Add alerting rules for critical issues
- [ ] Document observability best practices

**Files**: Core modules, new monitoring configs

### LOW-003: Security Hardening
**Status**: Beyond mTLS, additional security needed  
**Effort**: Medium (1-2 days)  
**Description**: Implement additional security measures

**Tasks**:
- [ ] Add input validation for all external inputs
- [ ] Implement rate limiting for API endpoints
- [ ] Add audit logging for security events
- [ ] Implement secrets management integration
- [ ] Add security scanning for dependencies
- [ ] Document security incident response procedures

**Files**: Security manager, core modules

---

## 📋 Completed Items

- ✅ **HMA-002**: NATS-based EventBusPort adapter implementation
- ✅ **ARC-002**: Enforce ports-and-adapters-only interaction policy  
- ✅ **HMA-003**: Update all plugin manifests to v2.2 schema
- ✅ **ARC-004**: Implement FileProcessingOrchestrator L2 plugin
- ✅ **HMA-004**: Implement SHACLToJSONSchemaAdapter for Tier 3 compliance
- ✅ **BUG-002**: Convert all TODOs to tracked issues
- ✅ **HMA-005**: Create ADRs for significant technology decisions
- ✅ **Documentation**: Update all documentation and add missing README files

---

## 🎯 Next Sprint Recommendations

**Sprint Focus**: Production Readiness  
**Duration**: 2 weeks  
**Priority Order**:
1. CRIT-001 (SHACL real implementation)
2. CRIT-002 (Security policy deployment)
3. HIGH-002 (Dependencies update)
4. HIGH-001 (NATS operational setup)
5. HIGH-003 (Testing framework - start with critical path tests)

**Success Criteria**:
- All CRITICAL items completed
- Real SHACL validation working
- Complete deployment documentation
- Basic test coverage >70%
- Production-ready security configuration