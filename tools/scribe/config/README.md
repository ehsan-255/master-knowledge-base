# Scribe Configuration - HMA v2.2 Compliant Settings

This directory contains all configuration files for the Scribe engine. All configurations follow HMA v2.2 standards with JSON Schema validation and externalized security policies.

## Configuration Files

### Core Configuration

| File | Purpose | Schema |
|------|---------|--------|
| **config.json** | Main engine configuration | `../schemas/scribe_config.schema.json` |
| **security_policy.yaml** | Externalized security policies | Custom YAML format |

## Main Configuration (config.json)

The main configuration file defines all engine settings with HMA v2.2 compliance:

### Configuration Structure

```json
{
  "config_version": "2.2",
  "hma_compliance": {
    "version": "2.2",
    "tier_1_technologies": {
      "telemetry": "opentelemetry",
      "security": "mtls",
      "validation": "json_schema"
    },
    "tier_2_technologies": {
      "messaging": "nats",
      "logging": "structured",
      "orchestration": "kubernetes"
    }
  },
  "engine": {
    "watch_paths": ["."],
    "file_patterns": ["*.md", "*.txt", "*.json"],
    "max_workers": 4,
    "enable_hot_reload": true,
    "health_check_port": 9090
  },
  "plugins": {
    "manifest_required": true,
    "validation_strict": true,
    "load_order": [
      "enhanced_frontmatter_action",
      "naming_enforcement_action",
      "graph_validation_action",
      "reconciliation_action"
    ]
  },
  "security": {
    "enable_mtls": true,
    "audit_enabled": true,
    "allowed_commands": ["git", "python", "echo"],
    "policy_file": "config/security_policy.yaml"
  },
  "telemetry": {
    "enabled": true,
    "service_name": "scribe-engine",
    "export_endpoint": "http://jaeger:14268/api/traces",
    "metrics_port": 9090,
    "trace_sampling_rate": "1.0"
  },
  "nats": {
    "url": "nats://localhost:4222",
    "max_reconnect_attempts": -1,
    "reconnect_time_wait": 2,
    "connection_timeout": 30
  },
  "performance": {
    "async_processing": {
      "enabled": true,
      "max_queue_size": 1000,
      "worker_count": 4,
      "timeout_seconds": 300
    },
    "caching": {
      "enabled": true,
      "max_size": 1000,
      "ttl_seconds": 3600
    }
  },
  "logging": {
    "level": "INFO",
    "format": "structured",
    "include_stdlib_logs": true,
    "correlation_ids": true
  }
}
```

### Configuration Sections

#### HMA Compliance

Defines HMA v2.2 compliance settings and technology tier selections:

```json
{
  "hma_compliance": {
    "version": "2.2",
    "tier_1_technologies": {
      "telemetry": "opentelemetry",
      "security": "mtls", 
      "validation": "json_schema"
    },
    "tier_2_technologies": {
      "messaging": "nats",
      "logging": "structured"
    },
    "tier_3_adapters": {
      "shacl_adapter": "enabled"
    }
  }
}
```

#### Engine Settings

Core engine behavior and file watching configuration:

```json
{
  "engine": {
    "watch_paths": ["."],                    // Directories to monitor
    "file_patterns": ["*.md", "*.txt"],     // File patterns to process
    "exclude_patterns": ["*.tmp", "*.bak"], // Patterns to exclude
    "max_workers": 4,                       // Maximum concurrent workers
    "enable_hot_reload": true,              // Plugin hot-reloading
    "health_check_port": 9090,              // Health endpoint port
    "graceful_shutdown_timeout": 30         // Shutdown timeout in seconds
  }
}
```

#### Plugin Configuration

Plugin loading and management settings:

```json
{
  "plugins": {
    "manifest_required": true,              // Require manifest.json for all plugins
    "validation_strict": true,              // Strict manifest validation
    "load_order": [                         // Plugin loading order
      "enhanced_frontmatter_action",
      "naming_enforcement_action"
    ],
    "directories": ["actions"],             // Plugin search directories
    "auto_reload": true,                    // Automatic plugin reloading
    "timeout_seconds": 60                   // Plugin execution timeout
  }
}
```

#### Security Configuration

Security policies and enforcement settings:

```json
{
  "security": {
    "enable_mtls": true,                    // Enable mutual TLS
    "audit_enabled": true,                  // Enable security auditing
    "allowed_commands": ["git", "python"],  // Whitelist of allowed commands
    "policy_file": "config/security_policy.yaml", // External policy file
    "max_command_timeout": 300,             // Command execution timeout
    "env_var_whitelist": ["PATH", "HOME"]   // Allowed environment variables
  }
}
```

#### Telemetry Configuration

OpenTelemetry and observability settings:

```json
{
  "telemetry": {
    "enabled": true,
    "service_name": "scribe-engine",
    "service_version": "2.2.0",
    "export_endpoint": "http://jaeger:14268/api/traces",
    "metrics_endpoint": "http://prometheus:9090/metrics",
    "trace_sampling_rate": "1.0",           // Sample 100% of traces
    "resource_attributes": {                // Custom resource attributes
      "environment": "production",
      "deployment.zone": "us-west-2"
    }
  }
}
```

#### NATS Configuration

Message broker settings for event communication:

```json
{
  "nats": {
    "url": "nats://localhost:4222",         // NATS server URL
    "cluster_urls": [                       // Cluster URLs for HA
      "nats://nats-1:4222",
      "nats://nats-2:4222"
    ],
    "max_reconnect_attempts": -1,           // Unlimited reconnects
    "reconnect_time_wait": 2,               // Seconds between reconnect attempts
    "connection_timeout": 30,               // Connection timeout
    "credentials_file": "nats.creds",       // NATS credentials file
    "tls_enabled": true                     // Enable TLS
  }
}
```

## Security Policy (security_policy.yaml)

Externalized security policies that can be updated without code changes:

```yaml
# Security Policy v2.2
policy_version: "2.2"
last_updated: "2025-07-24T00:00:00Z"

# Dangerous command patterns to block
dangerous_patterns:
  - "rm -rf"
  - "del /s"
  - "format c:"
  - "shutdown"
  - "reboot"
  - "mkfs"
  - "fdisk"

# Environment variables to always scrub from logs
dangerous_env_keys_to_always_scrub:
  - "PASSWORD"
  - "SECRET"
  - "TOKEN"
  - "KEY"
  - "CREDENTIAL"
  - "AUTH"
  - "API_KEY"
  - "PRIVATE_KEY"

# File path restrictions
restricted_paths:
  - "/etc/passwd"
  - "/etc/shadow"
  - "C:\\Windows\\System32"
  - "/proc"
  - "/sys"

# Network restrictions
network_restrictions:
  allowed_domains:
    - "api.github.com"
    - "registry.npmjs.org"
  blocked_ips:
    - "169.254.169.254"  # AWS metadata
    - "metadata.google.internal"

# Command execution limits
execution_limits:
  max_execution_time: 300      # 5 minutes
  max_memory_mb: 1024         # 1GB
  max_file_descriptors: 100   # File handles
  max_processes: 10           # Child processes
```

## Environment-Specific Configuration

### Development Configuration

```json
{
  "config_version": "2.2",
  "engine": {
    "watch_paths": ["./dev-content"],
    "enable_hot_reload": true,
    "health_check_port": 9090
  },
  "security": {
    "enable_mtls": false,
    "audit_enabled": false
  },
  "telemetry": {
    "enabled": true,
    "export_endpoint": "http://localhost:14268/api/traces",
    "trace_sampling_rate": "0.1"
  },
  "logging": {
    "level": "DEBUG",
    "include_stdlib_logs": true
  }
}
```

### Production Configuration

```json
{
  "config_version": "2.2",
  "engine": {
    "watch_paths": ["/app/content"],
    "enable_hot_reload": false,
    "health_check_port": 9090
  },
  "security": {
    "enable_mtls": true,
    "audit_enabled": true,
    "policy_file": "/etc/scribe/security_policy.yaml"
  },
  "telemetry": {
    "enabled": true,
    "export_endpoint": "https://jaeger.example.com/api/traces",
    "trace_sampling_rate": "0.1"
  },
  "logging": {
    "level": "INFO",
    "include_stdlib_logs": false
  }
}
```

## Configuration Validation

All configuration files are validated against JSON Schema:

### Validation Process

1. **Schema Loading**: Load schema from `../schemas/scribe_config.schema.json`
2. **Structure Validation**: Validate JSON structure and data types
3. **Business Logic Validation**: Check cross-field dependencies and constraints
4. **Security Validation**: Ensure secure defaults and no dangerous settings

### Validation Example

```python
import json
import jsonschema

def validate_config(config_path: str) -> bool:
    """Validate configuration against schema."""
    
    # Load configuration
    with open(config_path) as f:
        config = json.load(f)
    
    # Load schema
    with open("../schemas/scribe_config.schema.json") as f:
        schema = json.load(f)
    
    # Validate
    try:
        jsonschema.validate(config, schema)
        return True
    except jsonschema.ValidationError as e:
        print(f"Configuration validation failed: {e}")
        return False
```

## Configuration Management

### Dynamic Configuration Updates

Some settings can be updated at runtime:

```python
# Update logging level
config_manager.update_setting("logging.level", "DEBUG")

# Update plugin load order
config_manager.update_setting("plugins.load_order", ["new_plugin", "existing_plugin"])
```

### Configuration Hot-Reloading

The engine can reload configuration without restart for certain settings:

- Logging levels
- Plugin load order
- Security policies (external file)
- Telemetry sampling rates

### Configuration Sources

Configuration can be loaded from multiple sources (in order of precedence):

1. **Environment Variables**: `SCRIBE_WATCH_PATHS`, `SCRIBE_LOG_LEVEL`
2. **Command Line Arguments**: `--config-file`, `--log-level`
3. **Configuration File**: `config.json`
4. **Default Values**: Built-in defaults

## Troubleshooting

### Common Configuration Issues

#### Invalid JSON Format

```bash
# Validate JSON syntax
python -m json.tool config.json
```

#### Schema Validation Errors

```bash
# Validate against schema
python -c "
import json, jsonschema
config = json.load(open('config.json'))
schema = json.load(open('../schemas/scribe_config.schema.json'))
jsonschema.validate(config, schema)
print('Configuration is valid')
"
```

#### Permission Issues

```bash
# Check file permissions
ls -la config/
chmod 644 config.json
chmod 600 security_policy.yaml  # More restrictive for security file
```

### Debug Configuration Loading

```python
import json
from core.config_manager import ConfigManager

# Load with debug information
config_manager = ConfigManager("config/config.json", debug=True)
print(f"Loaded configuration: {json.dumps(config_manager.config, indent=2)}")
```

## Security Considerations

### File Permissions

- **config.json**: `644` (readable by all, writable by owner)
- **security_policy.yaml**: `600` (readable/writable by owner only)

### Sensitive Data

- **Never store secrets** in configuration files
- Use environment variables or secret management systems
- Scrub sensitive data from logs using security policies

### Configuration Validation

- All inputs validated against schemas
- Business logic validation for cross-field dependencies
- Security validation to prevent dangerous configurations

## Related Documentation

- [Schema Definitions](../schemas/) - JSON Schema validation files
- [Security Manager](../core/security_manager.py) - Security policy enforcement
- [Config Manager](../core/config_manager.py) - Configuration loading and validation
- [Deployment Guide](../deployment/) - Environment-specific deployment configurations