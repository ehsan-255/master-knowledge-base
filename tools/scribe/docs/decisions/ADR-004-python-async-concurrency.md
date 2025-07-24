# ADR-004: Python Async/Await for Concurrency

## Status
**Accepted** - July 24, 2025

## Context

The Scribe engine previously used a mixed concurrency model with threading and synchronous operations. This created several challenges:

1. **Thread Safety Issues**: Race conditions and deadlocks, especially on Windows
2. **Resource Contention**: Multiple threads competing for I/O resources
3. **Debugging Complexity**: Thread-based debugging is notoriously difficult
4. **Scalability Limits**: Thread overhead limits concurrent operations
5. **Mixed Patterns**: Inconsistent use of sync/async patterns across codebase

The migration to HMA v2.2 provided an opportunity to standardize on a modern concurrency model.

## Decision

We will standardize on **Python's async/await concurrency model** throughout the Scribe engine.

### Implementation Strategy

1. **Core Components**: All major components support async operations
   - Plugin execution through ports is async
   - File operations are async where beneficial
   - Network operations (NATS, HTTP) are naturally async

2. **Plugin Interface**: Plugins can implement either sync or async execution
   - `execute()` method for synchronous plugins (legacy compatibility)
   - `execute_async()` method for asynchronous plugins (preferred)
   - Automatic wrapping of sync plugins in thread pools

3. **Event Loop Management**: Dedicated event loops for different components
   - Engine startup/shutdown uses temporary event loops
   - NATS adapter manages its own event loop context
   - Proper cleanup and resource management

### Backward Compatibility

- Legacy synchronous plugins continue to work
- Automatic thread pool execution for sync plugins
- Gradual migration path from sync to async

## Consequences

### Positive
- ✅ **Performance**: Better I/O concurrency and resource utilization
- ✅ **Scalability**: Can handle many more concurrent operations
- ✅ **Reliability**: Eliminates many race conditions and deadlocks
- ✅ **Modern Python**: Aligns with modern Python best practices
- ✅ **Integration**: Better integration with async libraries (NATS, HTTP clients)
- ✅ **Debugging**: Easier to debug than thread-based code

### Negative
- ❌ **Learning Curve**: Team needs async/await expertise
- ❌ **Complexity**: Async code can be more complex to write correctly
- ❌ **Library Constraints**: Some libraries don't support async operations
- ❌ **Event Loop Management**: Need careful event loop lifecycle management

### Migration Challenges
- Converting existing synchronous code to async
- Managing mixed sync/async interfaces during transition
- Ensuring proper error handling in async contexts

## Implementation Status

### Completed Async Components
- ✅ **Plugin Execution**: `execute_plugin()` is async with automatic sync plugin wrapping
- ✅ **NATS Adapter**: Full async implementation with proper connection management
- ✅ **Port Interfaces**: Most port methods are async for I/O operations
- ✅ **Engine Lifecycle**: Async startup/shutdown with proper resource cleanup
- ✅ **File Processing Orchestrator**: Full async workflow coordination

### Async Patterns Implemented

#### Plugin Execution
```python
# Async plugin
async def execute_async(self, input_data):
    result = await self.some_async_operation()
    return result

# Legacy sync plugin (automatically wrapped)
def execute(self, file_content, match, file_path, params):
    return self.process_synchronously()
```

#### Port Operations
```python
# Command execution through port
async def execute_command_safely(self, command_list, **kwargs):
    command_port = self.get_command_port()
    return await command_port.execute_command_safely(command_list, **kwargs)
```

#### Event Loop Management
```python
# Engine startup
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    success = loop.run_until_complete(self.initialize_minimal_core())
finally:
    loop.close()
```

### Synchronous Compatibility
- Legacy plugins automatically executed in thread pools
- Synchronous methods available where async isn't beneficial
- Gradual migration without breaking existing functionality

## Best Practices Established

1. **Async by Default**: New code should use async/await unless there's a specific reason not to
2. **Proper Error Handling**: Use try/except blocks in async contexts
3. **Resource Cleanup**: Always use proper async context managers and cleanup
4. **Event Loop Isolation**: Don't share event loops between unrelated components
5. **Timeout Handling**: Always specify timeouts for async operations

## Performance Impact

### Positive
- **I/O Bound Operations**: Significant performance improvement for file and network operations
- **Concurrent Processing**: Can handle many more simultaneous plugin executions
- **Memory Efficiency**: Lower memory overhead compared to thread-based concurrency

### Benchmarks (Estimated)
- **Plugin Execution**: 3-5x improvement for I/O heavy plugins
- **Event Processing**: 10x improvement in event throughput
- **Memory Usage**: 40-60% reduction in memory overhead for concurrent operations

## Related ADRs
- ADR-001: NATS Message Broker Adoption (benefits from async)
- ADR-002: Ports and Adapters Architecture (async port interfaces)
- ADR-005: HMA v2.2 Compliance Strategy (modern architecture)