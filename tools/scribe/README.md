# Scribe Engine - HMA-Based Automation Engine

**Version**: 1.0.1  
**Architecture**: Hexagonal Microkernel Architecture (HMA)  
**Status**: Production Ready

## Overview

Scribe is a lightweight, event-driven automation engine designed for plain-text knowledge and code repositories. Built on the Hexagonal Microkernel Architecture (HMA), it follows a simple yet powerful **Observe → Trigger → Act** pattern to automate file-based workflows with enterprise-grade reliability.

### Key Features

- **🏗️ HMA Architecture**: Clean separation of concerns with L1-L4 layers
- **⚡ Event-Driven**: Real-time file system monitoring with sub-50ms response
- **🔒 Crash-Safe**: Atomic file operations prevent data corruption
- **📊 Observable**: Structured JSON logging and HTTP health endpoints
- **🧵 Multi-Threaded**: Producer-consumer pattern for high throughput
- **🛡️ Resilient**: Graceful shutdown and error handling
- **🔌 Extensible**: Advanced V2.0 plugin system with hot-reloading, dependency management, and security validation.

## Architecture

Scribe implements the Hexagonal Microkernel Architecture with four distinct layers:

```
┌─────────────────────────────────────────────────────────────┐
│ L1: Interface Zone (Driving Adapters)                      │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ File System Events → Watcher (Producer Thread)         │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ L2: Microkernel Core Zone                                  │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Event Bus (Thread-Safe Queue) ← → Engine Core (Worker) │ │
│ │ Config Manager | Plugin Loader | Circuit Breaker       │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ L3: Capability Plugin Zone                                 │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Action Dispatcher → Action Plugins (BaseAction)        │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ L4: Infrastructure Zone (Driven Adapters)                  │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Target Files | External Commands | HTTP Endpoints      │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Installation

### Prerequisites

- Python 3.9+
- Conda environment manager

### Setup

1. **Activate the conda environment:**
   ```bash
   conda activate conda-kb
   ```

2. **Install the Scribe engine as an editable package:**
   ```bash
   cd tools/scribe
   pip install -e .
   ```

3. **Verify installation:**
   ```bash
   python engine.py --help
   ```

## Quick Start

1. **Start the engine:**
   ```bash
   cd tools/scribe
   python engine.py
   ```

2. **Monitor health:**
   ```bash
   curl http://localhost:9468/health
   ```

## Configuration (`tools/scribe/config/config.json`)

Scribe is configured via `tools/scribe/config/config.json`. The configuration is validated against a schema and supports hot-reloading for near-instantaneous changes.

```json
{
  "config_version": "1.0",
  "engine_settings": {
    "log_level": "INFO",
    "quarantine_path": "archive/scribe/quarantine/",
    "pause_file": ".engine-pause"
  },
  "plugins": {
    "directories": ["actions", "custom_plugins"],
    "auto_reload": true,
    "load_order": ["actions", "custom_plugins"]
  },
  "security": {
    "allowed_commands": ["git"],
    "restricted_paths": [".git/"]
  },
  "rules": [
    {
      "id": "RULE-001",
      "name": "Update Task Timestamp on State Change",
      "enabled": true,
      "file_glob": "**/tasks/*.md",
      "trigger_pattern": "^(> \\[!TASK\\].*?\\| state: (\\w+).*)$",
      "actions": [
        {
          "type": "update_structured_field",
          "params": {
            "field": "updated",
            "value_template": "{timestamp_utc_iso}"
          }
        }
      ]
    }
  ]
}
```

---

## Plugin System (V2.0)

Scribe V2 features a powerful, dynamic plugin system that allows for extensive customization. It is built on four key pillars: **Multi-Directory Support**, **Hot-Reloading**, **Dependency Management**, and **Security Validation**.

### 1. Plugin Configuration

The plugin system is configured in `config.json` under the `plugins` key:

-   `"directories"`: An array of directories where Scribe looks for plugins. This allows you to organize plugins logically (e.g., core actions, custom business logic, third-party extensions).
-   `"load_order"`: An array specifying the order in which to load the directories. This is crucial when one directory's plugins might depend on another's.
-   `"auto_reload"`: A boolean (`true` or `false`) to enable or disable plugin hot-reloading. When `true`, any change to a plugin file will cause it to be reloaded automatically without restarting the engine.

### 2. Creating a Custom Action Plugin

An "Action" is a Python class that inherits from `BaseAction` and performs a specific task.

**Example Plugin (`custom_plugins/add_metadata_action.py`):**

```python
# custom_plugins/add_metadata_action.py

# This plugin depends on another action to be loaded first
# depends: log_event

from ..actions.base import BaseAction, ActionExecutionError
import re
from typing import Dict, Any, List

class AddMetadataAction(BaseAction):
    """
    Action to add a metadata key-value pair to the end of a file.
    """
    def get_required_params(self) -> List[str]:
        return ["key", "value"]

    def execute(self, file_content: str, match: re.Match, file_path: str, params: Dict[str, Any]) -> str:
        """
        Appends a 'key: value' line to the file content.
        """
        self.validate_params(params)
        key = params["key"]
        value = params["value"]
        
        self.logger.info(f"Adding metadata '{{key}}: {{value}}' to file.", file_path=file_path)
        
        return f"{file_content.strip()}\\n{{key}}: {{value}}\\n"

    def get_description(self) -> str:
        return "Appends a key-value pair to the end of a file."
```

### 3. Dependency Management

Scribe can manage dependencies between plugins. If `PluginA` requires `PluginB` to be loaded first, you can declare this with a special comment.

-   **Declaration**: Use a comment at the top of your plugin file: `# depends: <action_type>`
-   **Resolution**: The `PluginLoader` performs a topological sort to ensure dependencies are loaded in the correct order.
-   **Error Handling**: The engine will fail to start if a dependency is missing or if a circular dependency is detected, preventing runtime errors.

### 4. Security Validation

Before loading any plugin, the `PluginLoader` performs several security checks to create a safe execution sandbox:

-   **File Permissions**: Rejects plugins that are world-writable to prevent unauthorized modification.
-   **Dangerous Imports**: Scans the plugin's source code for dangerous Python modules like `subprocess`, `eval`, `exec`, or `os.system`.
-   **Dangerous Function Calls**: Analyzes the code to detect direct calls to potentially harmful functions.

These checks significantly reduce the risk of executing malicious or unsafe code.

---

## Testing

### Running Tests

With the new packaging system, tests can be run directly without any path modifications:

```bash
cd test-environment/scribe-tests
conda activate conda-kb
python -m pytest -v
```

All imports now use the installed package, eliminating the need for `sys.path` modifications.

### Test Categories

1. **Unit Tests**: Individual component testing
   - `test_worker.py` - Event processor
   - `test_atomic_write.py` - Crash-safe file operations

2. **Integration Tests**: End-to-end testing
   - `test_integration.py` - Complete event flow
   - `test_health_endpoint.py` - HTTP monitoring

## Troubleshooting

### Common Issues

1. **Engine won't start**
   - Check conda environment is activated
   - Verify all dependencies are installed
   - Check file permissions on watch directories

2. **High memory usage**
   - Check queue size via health endpoint
   - Look for stuck events in logs
   - Verify file patterns aren't too broad

3. **Events not processing**
   - Check file patterns match your files
   - Verify watch paths are correct
   - Look for errors in structured logs

---

## Roadmap

### Phase 1: The Resilient Core ✅
- [x] Core architecture & event loop
- [x] Foundational reliability & observability
- [x] Crash-safe file operations
- [x] Structured logging
- [x] Health monitoring

### Phase 2: The Extensible Platform ✅
- [x] Rule engine & configuration management
- [x] **V2.0 Action Plugin System (Hot-Reload, Dependencies, Security)**
- [x] Circuit breaker pattern for rule actions
- [x] Hot-reloading for main configuration and plugins

### Future Enhancements
- [ ] Web UI for monitoring
- [ ] Metrics export (Prometheus)
- [ ] Distributed deployment
- [ ] Advanced rule patterns

## Contributing

1. Follow the HMA architecture principles
2. Maintain 100% test coverage for new features
3. Use structured logging for all components
4. Ensure atomic operations for file modifications
5. Add comprehensive documentation

## License

[License information to be added]

---

**Built with ❤️ using Hexagonal Microkernel Architecture** 
