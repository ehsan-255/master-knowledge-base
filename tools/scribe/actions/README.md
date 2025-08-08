# Scribe Actions - L3 Capability Plugins

This directory contains all L3 Capability Plugins for the Scribe engine. Each plugin implements specific file processing functionality and is fully HMA v2.2 compliant.

## Plugin Architecture

### HMA v2.2 Compliance

All plugins in this directory follow the HMA v2.2 L3 Capability Plugin pattern:

- **Layer**: L3 (Capability Plugins)
- **Manifest Version**: 2.2
- **Port Access**: Strict ports-and-adapters-only interaction
- **Security**: mTLS and permission-based access control
- **Observability**: OpenTelemetry boundary telemetry

### Plugin Structure

Each plugin follows this standardized structure:

```
plugin_name/
├── manifest.json          # HMA v2.2 compliant manifest
├── plugin_name.py         # Main plugin implementation
└── README.md              # Plugin documentation (optional)
```

### Base Plugin Class

All plugins inherit from `BaseAction` which provides:

- **Port Access**: `self.context.get_port(port_type)`
- **Convenience Methods**: `execute_command_safely()`, `read_file_safely()`, etc.
- **Logging**: Structured logging through `LoggingPort`
- **Events**: Event publishing through `EventBusPort`
- **Configuration**: Config access through `ConfigurationPort`

## Available Plugins

### L3 Capability Plugins

| Plugin | Type | Description |
|--------|------|-------------|
| **enhanced_frontmatter_action** | L3-Capability | LLM-enhanced frontmatter generation with SHACL validation |
| **graph_validation_action** | L3-Capability | Knowledge graph structure and relationship validation |
| **naming_enforcement_action** | L3-Capability | Naming convention enforcement with schema registry |
| **reconciliation_action** | L3-Capability | Data inconsistency reconciliation and synchronization |
| **roadmap_populator_action** | L3-Capability | Roadmap document population with structured data |
| **run_command_action** | L3-Capability | Secure system command execution |
| **view_generation_action** | L3-Capability | Dynamic view and report generation |

### L2 Orchestrator Plugins

| Plugin | Type | Description |
|--------|------|-------------|
| **file_processing_orchestrator** | L2-Orchestrator | Coordinates complex multi-stage workflows |

## Plugin Development

### Creating a New Plugin

1. **Create plugin directory**:
   ```bash
   mkdir actions/my_new_plugin
   ```

2. **Implement plugin class**:
   ```python
   from ..base import BaseAction
   
   class MyNewPlugin(BaseAction):
       def __init__(self, action_type, params, plugin_context):
           super().__init__(action_type, params, plugin_context)
       
       async def execute(self, file_content, match, file_path, params):
           # Use ports for all operations
           await self.execute_command_safely(["echo", "hello"])
           return file_content
   ```

3. **Create HMA v2.2 manifest**:
   ```json
   {
     "manifest_version": "2.2",
     "plugin_metadata": {
       "name": "my_new_plugin",
       "version": "2.2.0",
       "type": "L3-Capability"
     },
     "hma_compliance": {
       "hma_version": "2.2",
       "tier_classification": {
         "mandatory": ["json_schema", "otel_boundary", "mtls"],
         "recommended": ["structured_logging", "health_checks"],
         "alternative": []
       }
     }
   }
   ```

### Plugin Requirements

- **Manifest**: Must include valid `manifest.json` with version "2.2"
- **Base Class**: Must inherit from `BaseAction`
- **Port Access**: All external interactions through ports only
- **Async Support**: Prefer async methods for I/O operations
- **Error Handling**: Proper exception handling and logging
- **Documentation**: Clear docstrings and parameter validation

### Testing Plugins

```python
# Example plugin test
import pytest
from unittest.mock import Mock, AsyncMock

async def test_my_plugin():
    # Mock plugin context and ports
    context = Mock()
    context.get_port.return_value = AsyncMock()
    
    # Create plugin instance
    plugin = MyNewPlugin("test_type", {}, context)
    
    # Test execution
    result = await plugin.execute("content", None, "test.txt", {})
    assert result is not None
```

## Port Usage Patterns

### Common Port Operations

```python
# Command execution
result = await self.execute_command_safely(["git", "status"])

# File operations
content = await self.read_file_safely("path/to/file.txt")
success = await self.write_file_safely("path/to/output.txt", content)

# Configuration access
value = await self.get_config_value("my_setting", default="default")

# Event publishing
await self.publish_event("file_processed", {"file": file_path})

# Logging
self.log_port.log_info("Processing file", file_path=file_path)
```

### Direct Port Access

```python
# Get specific ports when needed
command_port = self.context.get_port("command_execution")
event_port = self.context.get_port("event_bus")
config_port = self.context.get_port("configuration")
```

## Security Considerations

- **Permissions**: Plugins specify required permissions in manifest
- **Isolation**: Each plugin runs with limited system access
- **mTLS**: All inter-plugin communication secured with mutual TLS
- **Audit Logging**: All operations logged for security auditing
- **Input Validation**: All inputs validated against JSON schemas

## Performance Guidelines

- **Async Operations**: Use async/await for I/O operations
- **Resource Limits**: Respect memory and CPU limits in manifest
- **Caching**: Use built-in caching for expensive operations
- **Batch Processing**: Process multiple items when possible
- **Timeout Handling**: Implement proper timeout handling

## Migration from v2.1

### Breaking Changes from v2.1 to v2.2

- **Constructor**: Now takes `plugin_context` instead of direct dependencies (`config_manager`, `security_manager`)
- **Port Access**: All operations must go through ports via `self.context.get_port()`
- **Async Methods**: Prefer async methods for better performance
- **Manifest Schema**: Updated to version "2.2" with new fields
- **Removed Legacy Files**: `run_command_action_legacy.py` has been removed

### Migration Steps

1. Update manifest version to "2.2"
2. **Update constructor**: Change from `__init__(self, action_type, params, config_manager, security_manager)` to `__init__(self, action_type, params, plugin_context)`
3. **Replace direct calls**: Change `self.config_manager.get(...)` to `await self.get_config_value(...)` or `self.context.get_port("configuration").get(...)`
4. Add async support where beneficial
5. Update error handling and logging

## Troubleshooting

### Common Issues

- **Port Not Found**: Ensure port is registered in engine factory
- **Permission Denied**: Check plugin permissions in manifest
- **Validation Errors**: Verify manifest against v2.2 schema
- **Async Errors**: Ensure proper async/await usage

### Debug Commands

```bash
# Check plugin manifests
python -c "from core.plugin_loader import PluginLoader; pl = PluginLoader(); pl.load_all_plugins()"

# Validate specific manifest
python -c "import json; jsonschema.validate(json.load(open('manifest.json')), schema)"
```

## Related Documentation

- [Base Action API](base.py) - Plugin base class reference
- [HMA Ports](../core/hma_ports.py) - Available port interfaces
- [Plugin Manifests](../schemas/plugin_manifest.schema.json) - Manifest schema
- [Shared Utilities](../utils/README.md) - Common utilities like frontmatter parsing
- [Architecture Decision Records](../docs/decisions/) - Design decisions and rationale