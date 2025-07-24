# Scribe Core - L2 Microkernel Components

This directory contains the L2 Microkernel Core components that implement the central logic and coordination for the Scribe engine. All components are HMA v2.2 compliant and follow strict architectural patterns.

## Architecture Overview

The core implements the HMA v2.2 L2 Microkernel pattern with these key principles:

- **Minimalist Core**: `engine.py` contains only routing and lifecycle management
- **Factory Pattern**: `engine_factory.py` handles all component instantiation
- **Ports-Only Interactions**: All external communication through registered ports
- **Dependency Injection**: Components receive dependencies via constructor injection
- **Boundary Telemetry**: OpenTelemetry spans on all boundary crossings

## Core Components

### Engine and Lifecycle

| Component | Purpose | HMA Layer |
|-----------|---------|-----------|
| **engine.py** | Minimalist L2 Core with routing and lifecycle only | L2-Core |
| **engine_factory.py** | Component creation and dependency injection | L2-Infrastructure |
| **minimal_core.py** | HMA-compliant minimal core implementation | L2-Core |

### Port System

| Component | Purpose | HMA Layer |
|-----------|---------|-----------|
| **hma_ports.py** | Technology-agnostic port interface definitions | L2-Interfaces |
| **port_adapters.py** | Concrete port implementations with adapters | L2-Infrastructure |
| **adapters/** | Specialized adapters (NATS, SHACL, etc.) | L2-Infrastructure |

### Plugin Management

| Component | Purpose | HMA Layer |
|-----------|---------|-----------|
| **plugin_loader.py** | HMA v2.2 plugin discovery and validation | L2-Infrastructure |
| **action_dispatcher.py** | Plugin execution coordination | L2-Core |

### Configuration and Security

| Component | Purpose | HMA Layer |
|-----------|---------|-----------|
| **config_manager.py** | Centralized configuration management | L2-Infrastructure |
| **security_manager.py** | Security policy enforcement and validation | L2-Infrastructure |
| **mtls.py** | Mutual TLS implementation for secure communication | L2-Infrastructure |

### Observability and Telemetry

| Component | Purpose | HMA Layer |
|-----------|---------|-----------|
| **hma_telemetry.py** | HMA v2.2 compliant OpenTelemetry implementation | L2-Infrastructure |
| **logging_config.py** | Structured logging configuration | L2-Infrastructure |
| **health_server.py** | Health check endpoints and monitoring | L2-Infrastructure |

### Processing and Coordination

| Component | Purpose | HMA Layer |
|-----------|---------|-----------|
| **async_processor.py** | Asynchronous task processing with queues | L2-Infrastructure |
| **rule_processor.py** | File pattern matching and rule evaluation | L2-Core |
| **boundary_validator.py** | HMA boundary validation and enforcement | L2-Infrastructure |

### Utility Components

| Component | Purpose | HMA Layer |
|-----------|---------|-----------|
| **atomic_write.py** | Cross-platform atomic file operations | L2-Infrastructure |
| **cache_manager.py** | Caching and memoization utilities | L2-Infrastructure |
| **circuit_breaker.py** | Circuit breaker pattern implementation | L2-Infrastructure |
| **error_recovery.py** | Error handling and recovery mechanisms | L2-Infrastructure |

## HMA v2.2 Compliance

### Mandatory Tier 1 Technologies

- ✅ **OpenTelemetry**: Boundary telemetry on all port interactions (`hma_telemetry.py`)
- ✅ **mTLS**: Mutual TLS for inter-component communication (`mtls.py`)
- ✅ **JSON Schema**: Validation for all configuration and manifests

### Recommended Tier 2 Technologies

- ✅ **NATS**: Message broker replacing in-memory queues (`adapters/nats_adapter.py`)
- ✅ **Structured Logging**: Contextual logging with correlation IDs
- ✅ **Health Checks**: Comprehensive health monitoring endpoints

### Architecture Patterns

- ✅ **Minimalist Core**: Engine contains only essential routing logic
- ✅ **Factory Pattern**: All instantiation externalized from core
- ✅ **Ports-and-Adapters**: Strict boundary enforcement with port registry
- ✅ **Dependency Injection**: Clean dependency management

## Key Design Patterns

### Factory Pattern

The `engine_factory.py` implements the factory pattern to eliminate god objects:

```python
def create_engine_components() -> EngineComponents:
    """Create all engine components with proper dependency injection."""
    components = EngineComponents()
    
    # Create components in correct order
    components.config_manager = ConfigManager(config_path)
    components.telemetry = create_hma_telemetry(...)
    components.security_manager = SecurityManager(components.config_manager)
    
    # Create and register port adapters
    _create_port_adapters(components)
    
    return components
```

### Port Registry Pattern

All external interactions go through registered ports:

```python
# Register ports
port_registry = PortRegistry()
port_registry.register_port("command_execution", command_adapter)
port_registry.register_port("event_bus", nats_adapter)

# Access through registry
command_port = port_registry.get_port("command_execution")
result = await command_port.execute_command_safely(["git", "status"])
```

### Boundary Telemetry Pattern

All port interactions include mandatory OpenTelemetry spans:

```python
async def execute_plugin(self, plugin_id: str, input_data: Dict[str, Any]):
    with self.telemetry.start_span("plugin_execution_boundary", plugin_id) as span:
        span.set_attribute("hma.boundary.type", "plugin_execution")
        span.set_attribute("hma.operation", "execute_plugin")
        # ... execution logic
```

## Component Interactions

### Engine Startup Sequence

1. **Factory Creation**: `create_engine_components()` instantiates all components
2. **Port Registration**: All adapters registered in port registry
3. **Plugin Loading**: `plugin_loader.load_all_plugins()` discovers and validates plugins
4. **Core Initialization**: `minimal_core.start()` initializes HMA core
5. **Service Startup**: Health server and NATS adapter started

### Plugin Execution Flow

1. **File Event**: Watcher detects file change
2. **Rule Processing**: `rule_processor` matches patterns and determines actions
3. **Plugin Dispatch**: `action_dispatcher` coordinates plugin execution
4. **Port Access**: Plugin accesses functionality through port registry
5. **Boundary Telemetry**: All interactions traced with OpenTelemetry
6. **Result Processing**: Results processed and events published

## Configuration

### Core Configuration

```json
{
  "engine": {
    "watch_paths": ["."],
    "max_workers": 4,
    "health_check_port": 9090
  },
  "telemetry": {
    "enabled": true,
    "service_name": "scribe-engine",
    "export_endpoint": "http://jaeger:14268/api/traces"
  },
  "nats": {
    "url": "nats://localhost:4222",
    "max_reconnect_attempts": -1
  }
}
```

### Security Configuration

External security policies in `../config/security_policy.yaml`:

```yaml
dangerous_patterns:
  - "rm -rf"
  - "del /s"
  - "format c:"

dangerous_env_keys_to_always_scrub:
  - "PASSWORD"
  - "SECRET"
  - "TOKEN"
```

## Development Guidelines

### Adding New Components

1. **Interface First**: Define port interface in `hma_ports.py` if needed
2. **Implementation**: Create concrete implementation with proper error handling
3. **Factory Integration**: Add to `engine_factory.py` with dependency injection
4. **Telemetry**: Add OpenTelemetry boundary spans
5. **Testing**: Unit tests with proper mocking
6. **Documentation**: Update this README and add docstrings

### Error Handling

```python
try:
    result = await some_operation()
    logger.info("Operation completed", operation="some_operation", result=result)
    return result
except Exception as e:
    logger.error("Operation failed", operation="some_operation", error=str(e))
    self.telemetry.record_error("operation_failed", "component_name", str(e))
    raise
```

### Async Patterns

```python
# Proper async method with timeout
async def process_with_timeout(self, data: Any, timeout: int = 30) -> Any:
    try:
        return await asyncio.wait_for(
            self._actual_processing(data),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        raise ProcessingTimeoutError(f"Processing timed out after {timeout}s")
```

## Testing

### Unit Testing

```python
import pytest
from unittest.mock import Mock, AsyncMock

@pytest.fixture
def mock_components():
    components = Mock()
    components.config_manager = Mock()
    components.telemetry = Mock()
    return components

async def test_component_function(mock_components):
    component = MyComponent(mock_components.config_manager, mock_components.telemetry)
    result = await component.process_data("test")
    assert result is not None
```

### Integration Testing

```python
async def test_engine_startup():
    components = create_engine_components("test_config.json")
    engine = ScribeEngine(components)
    
    # Test startup
    engine.start()
    assert engine.is_running
    
    # Test shutdown
    engine.stop()
    assert not engine.is_running
```

## Performance Considerations

- **Async Operations**: All I/O operations use async/await
- **Connection Pooling**: Reuse connections where possible
- **Caching**: Cache expensive operations with TTL
- **Resource Limits**: Respect memory and CPU constraints
- **Batch Processing**: Process multiple items when beneficial

## Security Considerations

- **mTLS**: All inter-component communication secured
- **Input Validation**: All inputs validated against schemas
- **Permission Checks**: Components verify permissions before operations
- **Audit Logging**: All security-relevant operations logged
- **Secret Management**: Secrets externalized and encrypted

## Troubleshooting

### Common Issues

- **Port Not Found**: Check port registration in `engine_factory.py`
- **Plugin Load Errors**: Validate manifest against v2.2 schema
- **Telemetry Issues**: Verify OpenTelemetry configuration
- **NATS Connection**: Check NATS server availability and configuration

### Debug Commands

```bash
# Check component health
curl http://localhost:9090/health

# View telemetry
curl http://localhost:9090/metrics

# Test plugin loading
python -c "from core.plugin_loader import PluginLoader; PluginLoader().load_all_plugins()"
```

## Related Documentation

- [HMA v2.2 Specification](../../HMA v2.2/) - Architecture specification
- [Architecture Decision Records](../docs/decisions/) - Design decisions
- [Plugin Development](../actions/README.md) - Plugin development guide
- [Deployment Guide](../deployment/) - Production deployment instructions