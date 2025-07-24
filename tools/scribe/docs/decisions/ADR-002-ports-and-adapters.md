# ADR-002: Ports and Adapters Architecture Implementation

## Status
**Accepted** - July 24, 2025

## Context

The Scribe engine previously allowed plugins to directly access core components like `SecurityManager` and `ConfigManager`. This created tight coupling and violated HMA v2.2's explicit boundaries principle, which mandates that all interactions must go through well-defined ports.

Key issues with the previous approach:
1. **Tight Coupling**: Plugins had direct dependencies on concrete implementations
2. **Testing Difficulty**: Hard to mock dependencies for unit testing  
3. **HMA Non-Compliance**: Violated Part 3, Sec 9 (explicit boundaries)
4. **Technology Lock-in**: Difficult to swap implementations without changing plugin code

## Decision

We will implement a **strict ports-and-adapters-only interaction policy** throughout the Scribe engine.

### Architecture Changes

1. **Extended Port Definitions**: Define technology-agnostic interfaces for all operations:
   - `CommandExecutionPort`: Secure command execution
   - `FileSystemPort`: File operations with security validation
   - `LoggingPort`: Structured logging interface
   - `PluginContextPort`: Plugin execution context and port access

2. **Plugin Context Injection**: Replace direct dependency injection with port-based access:
   - Plugins receive a `PluginContextPort` instead of concrete dependencies
   - Context provides access to all other ports through `get_port(port_type)`
   - Maintains security and observability boundaries

3. **BaseAction Refactoring**: Update the plugin base class:
   - Constructor accepts `PluginContextPort` instead of direct dependencies
   - Provide convenience methods for common port operations
   - All operations go through ports (no direct SDK calls)

### Port Implementation Strategy

- **Port Registry**: Central registry for all port implementations
- **Adapter Pattern**: Each port has a concrete adapter implementation
- **Boundary Telemetry**: All port interactions include mandatory OTEL spans
- **Security Enforcement**: mTLS and access control at port boundaries

## Consequences

### Positive
- ✅ **HMA Compliance**: Full compliance with explicit boundaries principle
- ✅ **Loose Coupling**: Plugins depend only on port interfaces
- ✅ **Testability**: Easy to mock ports for unit testing
- ✅ **Flexibility**: Can swap implementations without changing plugin code
- ✅ **Observability**: All interactions monitored through port boundaries
- ✅ **Security**: Centralized security controls at port level

### Negative
- ❌ **Complexity**: More abstraction layers and indirection
- ❌ **Performance**: Small overhead from port abstraction (mitigated by modern CPUs)
- ❌ **Migration Effort**: Existing plugins need refactoring

### Developer Experience
- **Learning Curve**: Developers need to understand port concepts
- **Consistency**: Clearer patterns for accessing core functionality
- **Documentation**: Well-defined interfaces improve API documentation

## Implementation Status

### Completed
- ✅ Extended port definitions in `hma_ports.py`
- ✅ Port adapter implementations in `port_adapters.py`
- ✅ Updated engine factory to register all ports
- ✅ Refactored `BaseAction` class for port-based access
- ✅ Updated plugin loader to use context injection
- ✅ Converted `run_command_action.py` as reference implementation

### Port Adapters Implemented
- `ScribeCommandExecutionAdapter`: Secure command execution with OTEL telemetry
- `ScribeFileSystemAdapter`: File operations with security validation
- `ScribeLoggingAdapter`: Structured logging with metrics
- `ScribePluginContextAdapter`: Plugin context and port access

### Example Usage

```python
# Old approach (direct dependencies)
class MyAction(BaseAction):
    def __init__(self, action_type, params, config_manager, security_manager):
        self.config_manager = config_manager
        self.security_manager = security_manager
    
    def execute(self, ...):
        result = self.security_manager.execute_command_safely(cmd)

# New approach (port-based)
class MyAction(BaseAction):
    def __init__(self, action_type, params, plugin_context):
        super().__init__(action_type, params, plugin_context)
    
    async def execute(self, ...):
        result = await self.execute_command_safely(cmd)  # Through port
```

## Related ADRs
- ADR-001: NATS Message Broker Adoption
- ADR-005: HMA v2.2 Compliance Strategy