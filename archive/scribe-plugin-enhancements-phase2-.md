# Scribe Plugin Development Guide

## Overview

This guide covers the enhanced plugin development features in Scribe v2.0, including multiple directories, hot-reloading, dependency management, and security validation.

## Plugin Directory Structure

Scribe supports multiple plugin directories configured in `config/config.json`:

```json
{
  "plugins": {
    "directories": ["actions", "custom_plugins", "third_party"],
    "auto_reload": true,
    "load_order": ["actions", "custom_plugins", "third_party"]
  }
}
```

### Directory Types

- **`actions/`** - Core built-in actions
- **`custom_plugins/`** - Organization-specific plugins  
- **`third_party/`** - External community plugins

## Basic Plugin Structure

```python
#!/usr/bin/env python3
"""
Example Plugin - Shows basic plugin structure
"""
# DEPENDENCIES: base_action, utility_action

import re
from typing import Dict, Any, List
from tools.scribe.actions.base import BaseAction

class ExampleAction(BaseAction):
    """Example action plugin demonstrating best practices."""
    
    def get_required_params(self) -> List[str]:
        """Get required parameters for this action."""
        return ["example_param"]
    
    def get_optional_params(self) -> Dict[str, Any]:
        """Get optional parameters and their defaults."""
        return {
            "optional_param": "default_value",
            "timeout": 30
        }
    
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """Validate parameters for the action."""
        # Custom validation logic here
        return True
    
    def execute(self, 
                file_content: str, 
                match: re.Match, 
                file_path: str, 
                params: Dict[str, Any]) -> str:
        """
        Execute the action.
        
        Args:
            file_content: The full content of the file
            match: The regex match that triggered this action
            file_path: Path to the file being processed
            params: Action parameters from the rule
            
        Returns:
            Modified file content
        """
        # Your action logic here
        return file_content
```

## Plugin Dependencies

### Declaring Dependencies

Use the `DEPENDENCIES` comment at the top of your plugin file:

```python
# DEPENDENCIES: base_utilities, file_operations, network_tools
```

### Dependency Resolution

- Plugins are loaded in dependency order automatically
- Circular dependencies are detected and reported
- Missing dependencies cause load failures with clear error messages

## Security Features

### Automatic Security Validation

All plugins are automatically validated for:

- **Dangerous imports**: `subprocess`, `os.system`, `eval`, `exec`
- **Dangerous functions**: `eval()`, `exec()`, `compile()`, `__import__()`
- **File permissions**: World-writable files are rejected
- **Code patterns**: Suspicious code patterns are flagged

### Security Best Practices

```python
# ✅ GOOD - Safe file operations via BaseAction utilities
self.write_file_safely(file_path, content)

# ❌ BAD - Direct file operations
with open(file_path, 'w') as f:
    f.write(content)

# ✅ GOOD - Use SecurityManager for commands
self.security_manager.execute_command_safely(['git', 'status'])

# ❌ BAD - Direct subprocess calls
subprocess.run(['git', 'status'])
```

## Hot-Reloading

### Enabling Hot-Reload

Set `auto_reload: true` in your configuration:

```json
{
  "plugins": {
    "auto_reload": true
  }
}
```

### Development Workflow

1. Edit your plugin file
2. Save the file
3. Plugin is automatically reloaded
4. Test your changes immediately

### Hot-Reload Events

Monitor logs for reload events:

```
Plugin file changed, reloading: /path/to/plugin.py
Plugin hot-reloading enabled
```

## Advanced Features

### Runtime Plugin Management

```python
# Add new plugin directory
engine.worker.plugin_loader.add_plugin_directory("experimental")

# Remove plugin directory  
engine.worker.plugin_loader.remove_plugin_directory("old_plugins")

# Manual reload
engine.worker.plugin_loader.reload_plugins()
```

### Plugin Statistics

```python
stats = plugin_loader.get_plugin_stats()
print(f"Loaded {stats['total_plugins']} plugins")
print(f"Active directories: {stats['plugins_directory']}")
```

## Testing Your Plugins

### Unit Tests

```python
import unittest
from your_plugin import YourAction

class TestYourAction(unittest.TestCase):
    def setUp(self):
        self.action = YourAction(
            action_type="your_action",
            params={"test_param": "value"},
            config_manager=mock_config,
            security_manager=mock_security
        )
    
    def test_execution(self):
        result = self.action.execute(
            file_content="test content",
            match=mock_match,
            file_path="/test/file.txt",
            params={"test_param": "value"}
        )
        self.assertIn("expected_change", result)
```

### Integration Tests

Create test configurations in `test-environment/scribe-tests/`:

```python
def test_your_plugin():
    # Create test environment
    # Configure Scribe with your plugin
    # Trigger action and validate results
    pass
```

## Configuration Schema

### Plugin Rules Configuration

```json
{
  "rules": [
    {
      "id": "RULE-001",
      "name": "Your Plugin Rule",
      "enabled": true,
      "file_glob": "*.md",
      "trigger_pattern": "your_pattern",
      "actions": [
        {
          "type": "your_action_type",
          "params": {
            "your_param": "value"
          }
        }
      ]
    }
  ]
}
```

## Troubleshooting

### Common Issues

1. **Plugin not loading**: Check security validation logs
2. **Dependency errors**: Verify dependency declarations
3. **Hot-reload not working**: Ensure `auto_reload: true` in config
4. **Permission errors**: Check file permissions and ownership

### Debug Mode

Enable debug logging for detailed plugin information:

```json
{
  "engine_settings": {
    "log_level": "DEBUG"
  }
}
```

### Plugin Load Order Issues

If plugins load in wrong order:

1. Check dependency declarations
2. Verify `load_order` in configuration
3. Look for circular dependencies

## Best Practices

1. **Always declare dependencies** in comments
2. **Use descriptive action type names** 
3. **Implement proper parameter validation**
4. **Handle errors gracefully**
5. **Write comprehensive tests**
6. **Follow security guidelines**
7. **Document your plugins well**

## Migration Guide

### From V1.0 to V2.0

1. Update configuration to use new `plugins` section
2. Add dependency declarations to existing plugins
3. Test plugins with security validation
4. Consider enabling hot-reload for development

### Breaking Changes

- Plugin directories must be explicitly configured
- Security validation is now mandatory
- Plugin loading order is dependency-driven

For more information, see the main Scribe documentation. 