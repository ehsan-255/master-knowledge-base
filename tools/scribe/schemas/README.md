# Scribe Schemas - JSON Schema Validation Definitions

This directory contains all JSON Schema definitions used for validation throughout the Scribe engine. These schemas ensure HMA v2.2 compliance and maintain data integrity across all components.

## Overview

JSON Schema validation is a **Tier 1 mandatory** technology in HMA v2.2. All configuration files, plugin manifests, and API inputs/outputs are validated against these schemas to ensure:

- **Data Integrity**: Prevent malformed data from causing system failures
- **API Consistency**: Ensure consistent data structures across all interfaces
- **Security**: Validate inputs to prevent injection attacks and malformed data
- **Documentation**: Schemas serve as living documentation of data structures

## Schema Files

### Core System Schemas

| Schema File | Purpose | Used By |
|-------------|---------|---------|
| **scribe_config.schema.json** | Main engine configuration validation | `config/config.json` |
| **plugin_manifest.schema.json** | Plugin manifest validation (HMA v2.2) | All `manifest.json` files |

## Configuration Schema (scribe_config.schema.json)

Validates the main engine configuration with complete HMA v2.2 compliance requirements.

### Schema Structure

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Scribe Engine Configuration Schema v2.2",
  "description": "HMA v2.2 compliant configuration schema for Scribe engine",
  "type": "object",
  "required": ["config_version", "hma_compliance", "engine"],
  "properties": {
    "config_version": {
      "type": "string",
      "const": "2.2",
      "description": "Configuration schema version (must be 2.2)"
    },
    "hma_compliance": {
      "$ref": "#/definitions/hma_compliance"
    },
    "engine": {
      "$ref": "#/definitions/engine_config"
    }
  }
}
```

### Key Validation Rules

#### HMA Compliance Section

```json
{
  "hma_compliance": {
    "type": "object",
    "required": ["version", "tier_1_technologies"],
    "properties": {
      "version": {
        "type": "string",
        "const": "2.2"
      },
      "tier_1_technologies": {
        "type": "object",
        "required": ["telemetry", "security", "validation"],
        "properties": {
          "telemetry": {
            "type": "string",
            "enum": ["opentelemetry"]
          },
          "security": {
            "type": "string", 
            "enum": ["mtls"]
          },
          "validation": {
            "type": "string",
            "enum": ["json_schema"]
          }
        }
      }
    }
  }
}
```

#### Engine Configuration

```json
{
  "engine_config": {
    "type": "object",
    "required": ["watch_paths", "file_patterns"],
    "properties": {
      "watch_paths": {
        "type": "array",
        "items": {
          "type": "string",
          "minLength": 1
        },
        "minItems": 1,
        "description": "Directories to monitor for file changes"
      },
      "file_patterns": {
        "type": "array",
        "items": {
          "type": "string",
          "pattern": "^\\*\\.[a-zA-Z0-9]+$"
        },
        "minItems": 1,
        "description": "File patterns to process (e.g., '*.md', '*.txt')"
      },
      "max_workers": {
        "type": "integer",
        "minimum": 1,
        "maximum": 32,
        "default": 4
      }
    }
  }
}
```

## Plugin Manifest Schema (plugin_manifest.schema.json)

Validates all plugin manifest files for HMA v2.2 compliance.

### Schema Overview

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "HMA v2.2 Plugin Manifest Schema", 
  "description": "Validation schema for HMA v2.2 compliant plugin manifests",
  "type": "object",
  "required": [
    "manifest_version",
    "plugin_metadata", 
    "hma_compliance",
    "interface_contracts"
  ]
}
```

### Manifest Validation Rules

#### Version Requirements

```json
{
  "manifest_version": {
    "type": "string",
    "const": "2.2",
    "description": "Manifest version must be 2.2 for HMA compliance"
  }
}
```

#### Plugin Metadata

```json
{
  "plugin_metadata": {
    "type": "object",
    "required": ["name", "version", "type", "description"],
    "properties": {
      "name": {
        "type": "string",
        "pattern": "^[a-z][a-z0-9_]*$",
        "description": "Plugin name in snake_case"
      },
      "version": {
        "type": "string",
        "pattern": "^\\d+\\.\\d+\\.\\d+$",
        "description": "Semantic version (e.g., '2.2.0')"
      },
      "type": {
        "type": "string",
        "enum": ["L2-Orchestrator", "L3-Capability"],
        "description": "HMA plugin type classification"
      }
    }
  }
}
```

#### HMA Compliance Section

```json
{
  "hma_compliance": {
    "type": "object",
    "required": ["hma_version", "tier_classification", "boundary_interfaces"],
    "properties": {
      "hma_version": {
        "type": "string",
        "const": "2.2"
      },
      "tier_classification": {
        "type": "object",
        "required": ["mandatory", "recommended", "alternative"],
        "properties": {
          "mandatory": {
            "type": "array",
            "items": {
              "type": "string",
              "enum": ["json_schema", "otel_boundary", "mtls"]
            }
          },
          "recommended": {
            "type": "array",
            "items": {
              "type": "string",
              "enum": ["structured_logging", "health_checks", "nats_messaging", "kubernetes"]
            }
          },
          "alternative": {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        }
      },
      "boundary_interfaces": {
        "type": "array",
        "items": {
          "$ref": "#/definitions/boundary_interface"
        }
      }
    }
  }
}
```

#### Boundary Interface Definition

```json
{
  "boundary_interface": {
    "type": "object",
    "required": ["port_type", "direction", "validation", "telemetry"],
    "properties": {
      "port_type": {
        "type": "string",
        "enum": [
          "PluginExecutionPort",
          "CommandExecutionPort", 
          "FileSystemPort",
          "LoggingPort",
          "EventBusPort",
          "PluginContextPort",
          "ConfigurationPort",
          "HealthCheckPort"
        ]
      },
      "direction": {
        "type": "string",
        "enum": ["inbound", "outbound", "bidirectional"]
      },
      "validation": {
        "type": "string",
        "description": "Validation method for this interface"
      },
      "telemetry": {
        "type": "string",
        "enum": ["otel_spans", "otel_metrics", "otel_logs"]
      }
    }
  }
}
```

## Schema Validation

### Validation Process

All schemas are used for validation at multiple points:

1. **Configuration Loading**: `config.json` validated against `scribe_config.schema.json`
2. **Plugin Loading**: All `manifest.json` files validated against `plugin_manifest.schema.json`
3. **Runtime Validation**: API inputs validated against relevant schemas
4. **Development**: Pre-commit hooks validate all JSON files

### Validation Implementation

```python
import json
import jsonschema
from pathlib import Path

class SchemaValidator:
    """Centralized schema validation for Scribe engine."""
    
    def __init__(self, schema_dir: str = "schemas"):
        self.schema_dir = Path(schema_dir)
        self._schemas = {}
        self._load_schemas()
    
    def _load_schemas(self):
        """Load all schema files."""
        for schema_file in self.schema_dir.glob("*.schema.json"):
            schema_name = schema_file.stem.replace(".schema", "")
            with open(schema_file) as f:
                self._schemas[schema_name] = json.load(f)
    
    def validate(self, data: dict, schema_name: str) -> bool:
        """Validate data against named schema."""
        if schema_name not in self._schemas:
            raise ValueError(f"Schema '{schema_name}' not found")
        
        try:
            jsonschema.validate(data, self._schemas[schema_name])
            return True
        except jsonschema.ValidationError as e:
            print(f"Validation error: {e}")
            return False
    
    def validate_config(self, config_path: str) -> bool:
        """Validate configuration file."""
        with open(config_path) as f:
            config = json.load(f)
        return self.validate(config, "scribe_config")
    
    def validate_manifest(self, manifest_path: str) -> bool:
        """Validate plugin manifest."""
        with open(manifest_path) as f:
            manifest = json.load(f)
        return self.validate(manifest, "plugin_manifest")
```

### Command Line Validation

```bash
# Validate configuration
python -c "
from schemas.validator import SchemaValidator
validator = SchemaValidator()
print('Config valid:', validator.validate_config('config/config.json'))
"

# Validate all plugin manifests
find actions -name 'manifest.json' -exec python -c "
import json, jsonschema, sys
manifest = json.load(open(sys.argv[1]))
schema = json.load(open('schemas/plugin_manifest.schema.json'))
try:
    jsonschema.validate(manifest, schema)
    print(f'{sys.argv[1]}: VALID')
except jsonschema.ValidationError as e:
    print(f'{sys.argv[1]}: INVALID - {e}')
" {} \;
```

## Schema Development

### Creating New Schemas

1. **Identify Data Structure**: Determine what needs validation
2. **Define Requirements**: Specify required vs optional fields
3. **Add Constraints**: Define validation rules and patterns
4. **Test Thoroughly**: Test with valid and invalid data
5. **Document Usage**: Update this README with usage information

### Schema Best Practices

#### Use Semantic Constraints

```json
{
  "version": {
    "type": "string",
    "pattern": "^\\d+\\.\\d+\\.\\d+$",
    "description": "Semantic version format (major.minor.patch)"
  }
}
```

#### Provide Clear Descriptions

```json
{
  "watch_paths": {
    "type": "array",
    "items": {"type": "string"},
    "minItems": 1,
    "description": "List of directories to monitor for file changes. Must contain at least one path."
  }
}
```

#### Use Enums for Fixed Values

```json
{
  "log_level": {
    "type": "string",
    "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    "default": "INFO"
  }
}
```

#### Define Reusable Components

```json
{
  "definitions": {
    "plugin_type": {
      "type": "string",
      "enum": ["L2-Orchestrator", "L3-Capability"]
    }
  },
  "properties": {
    "type": {"$ref": "#/definitions/plugin_type"}
  }
}
```

## Error Handling

### Validation Error Types

```python
# Common validation errors and handling
try:
    jsonschema.validate(data, schema)
except jsonschema.ValidationError as e:
    if e.validator == "required":
        print(f"Missing required field: {e.message}")
    elif e.validator == "enum":
        print(f"Invalid value. Allowed values: {e.schema['enum']}")
    elif e.validator == "pattern":
        print(f"Invalid format. Expected pattern: {e.schema['pattern']}")
    else:
        print(f"Validation error: {e.message}")
```

### Custom Error Messages

```json
{
  "hma_version": {
    "type": "string",
    "const": "2.2",
    "errorMessage": "HMA version must be '2.2' for compliance. Current version indicates non-compliant plugin."
  }
}
```

## Schema Versioning

### Version Management

- **Schema Versioning**: Schemas versioned independently of the application
- **Backward Compatibility**: New versions maintain backward compatibility when possible
- **Breaking Changes**: Breaking changes require new major version and migration path

### Migration Support

```json
{
  "anyOf": [
    {"$ref": "#/definitions/v2_1_format"},
    {"$ref": "#/definitions/v2_2_format"}
  ],
  "errorMessage": "Configuration must conform to either v2.1 or v2.2 format"
}
```

## Performance Considerations

### Schema Caching

```python
# Cache compiled schemas for better performance
from functools import lru_cache

@lru_cache(maxsize=128)
def get_compiled_schema(schema_path: str):
    """Get cached compiled schema."""
    with open(schema_path) as f:
        schema = json.load(f)
    return jsonschema.Draft7Validator(schema)
```

### Validation Optimization

- **Early Termination**: Use `ErrorTree` for early validation termination
- **Partial Validation**: Validate only changed fields when possible
- **Async Validation**: Use async validation for large datasets

## Testing

### Schema Test Suite

```python
import pytest
import json
from pathlib import Path

class TestSchemas:
    
    @pytest.mark.parametrize("schema_file", Path("schemas").glob("*.schema.json"))
    def test_schema_validity(self, schema_file):
        """Test that all schemas are valid JSON Schema."""
        with open(schema_file) as f:
            schema = json.load(f)
        
        # Validate schema structure
        jsonschema.Draft7Validator.check_schema(schema)
    
    def test_config_validation(self):
        """Test configuration validation with valid/invalid examples."""
        valid_config = {
            "config_version": "2.2",
            "hma_compliance": {"version": "2.2"},
            "engine": {"watch_paths": ["."], "file_patterns": ["*.md"]}
        }
        
        invalid_config = {
            "config_version": "1.0"  # Invalid version
        }
        
        validator = SchemaValidator()
        assert validator.validate(valid_config, "scribe_config")
        assert not validator.validate(invalid_config, "scribe_config")
```

## Related Documentation

- [Configuration Guide](../config/README.md) - How to use configuration schemas
- [Plugin Development](../actions/README.md) - Plugin manifest requirements
- [HMA v2.2 Specification](../../HMA v2.2/) - Architecture requirements
- [JSON Schema Specification](https://json-schema.org/) - JSON Schema documentation