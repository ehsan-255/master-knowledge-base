# Scribe Adapters - HMA v2.2 Compliance Bridges

This directory contains compliance adapters that implement the HMA v2.2 Tier 3 compliance pattern. These adapters bridge Tier 3 alternative technologies to Tier 1 mandatory standards, ensuring interoperability while preserving advanced capabilities.

## Overview

HMA v2.2 defines a three-tier technology framework:

- **Tier 1 (Mandatory)**: OpenTelemetry, mTLS, JSON Schema
- **Tier 2 (Recommended)**: NATS, Kubernetes, Vault, Structured Logging  
- **Tier 3 (Alternative)**: Specialized technologies with compliance bridges

Compliance adapters in this directory transform Tier 3 outputs into Tier 1 compatible formats, maintaining the benefits of specialized technologies while ensuring system-wide interoperability.

## Adapter Architecture

### Compliance Bridge Pattern

```python
class ComplianceBridge:
    """Base pattern for Tier 3 to Tier 1 transformation."""
    
    def transform_output(self, tier3_output: Any) -> Tier1StandardFormat:
        """Transform specialized output to standard format."""
        pass
    
    def create_compliance_report(self, data: Any) -> HMAComplianceReport:
        """Generate HMA v2.2 compliant report."""
        pass
```

### Bridge Responsibilities

1. **Format Transformation**: Convert proprietary formats to standard formats
2. **Metadata Preservation**: Maintain semantic information during transformation  
3. **Error Handling**: Graceful handling of malformed or incomplete data
4. **Compliance Reporting**: Generate HMA v2.2 compliant reports with full metadata
5. **Bidirectional Support**: Support workflows starting from either technology tier

## Available Adapters

### SHACL to JSON Schema Bridge

**File**: `shacl_adapter.py`  
**Purpose**: Transforms SHACL (RDF-based) validation reports to JSON Schema validation reports  
**Tier Bridge**: 3 (SHACL) → 1 (JSON Schema)

#### Key Components

- `ValidationResult`: Standardized violation structure
- `ComplianceReport`: HMA v2.2 compliant report format  
- `SHACLToJSONSchemaAdapter`: Main bridge implementation

#### Usage Example

```python
from adapters.shacl_adapter import SHACLToJSONSchemaAdapter

adapter = SHACLToJSONSchemaAdapter()

# Transform existing SHACL report
compliance_report = adapter.transform_shacl_report(shacl_graph, conforms)

# End-to-end validation with compliance bridge
compliance_report = adapter.validate_with_compliance_bridge(
    data, shacl_shapes, report_id="frontmatter_validation"
)

# Generate JSON Schema compatible report
json_report = adapter.create_json_schema_report(compliance_report)
```

#### Features

- **Severity Mapping**: SHACL severities mapped to standard levels (ERROR, WARNING, INFO)
- **Metadata Preservation**: Source locations, constraint components, and focus nodes preserved
- **Report Versioning**: Full report metadata with timestamps and version tracking
- **Error Resilience**: Graceful handling of malformed SHACL reports

## Adapter Development

### Creating New Compliance Adapters

1. **Identify Bridge Requirements**: Determine source (Tier 3) and target (Tier 1) formats
2. **Design Transformation Logic**: Plan how to preserve semantic information
3. **Implement Adapter Class**: Follow the compliance bridge pattern
4. **Add Error Handling**: Ensure graceful failure modes
5. **Create Tests**: Comprehensive testing with real-world data
6. **Document Usage**: Clear examples and integration patterns

### Adapter Template

```python
#!/usr/bin/env python3
"""
MyTechnology to JSON Schema Compliance Adapter

Bridges MyTechnology (Tier 3) outputs to JSON Schema validation reports (Tier 1).
"""

import json
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from ..core.logging_config import get_scribe_logger

logger = get_scribe_logger(__name__)


@dataclass
class MyTechnologyResult:
    """Standardized result from MyTechnology."""
    valid: bool
    message: str
    # ... other fields


class MyTechnologyToJSONSchemaAdapter:
    """Compliance adapter for MyTechnology to JSON Schema bridge."""
    
    def __init__(self, adapter_version: str = "2.2.0"):
        self.adapter_version = adapter_version
        self.logger = get_scribe_logger(f"{__name__}.{self.__class__.__name__}")
    
    def transform_report(self, 
                        source_data: Any,
                        report_id: Optional[str] = None) -> ComplianceReport:
        """Transform MyTechnology output to HMA v2.2 compliant format."""
        # Implementation here
        pass
    
    def get_adapter_info(self) -> Dict[str, Any]:
        """Get adapter capabilities and metadata."""
        return {
            "adapter_name": "MyTechnologyToJSONSchemaAdapter",
            "adapter_version": self.adapter_version,
            "hma_compliance_version": "2.2",
            "tier_bridge": {
                "from_tier": "3_alternative",
                "to_tier": "1_mandatory",
                "from_technology": "MyTechnology",
                "to_technology": "JSON_Schema"
            }
        }
```

### Testing Adapters

```python
import pytest
from unittest.mock import Mock

class TestMyTechnologyAdapter:
    
    def setup_method(self):
        self.adapter = MyTechnologyToJSONSchemaAdapter()
    
    def test_successful_transformation(self):
        source_data = Mock()  # Mock source data
        result = self.adapter.transform_report(source_data)
        
        assert result.overall_valid is not None
        assert result.hma_compliance_version == "2.2"
        assert len(result.violations) >= 0
    
    def test_error_handling(self):
        invalid_data = None
        result = self.adapter.transform_report(invalid_data)
        
        assert result.overall_valid is False
        assert result.error_count > 0
```

## Integration Patterns

### Plugin Integration

Adapters are typically used within L3 Capability Plugins:

```python
class MyValidationAction(BaseAction):
    def __init__(self, action_type, params, plugin_context):
        super().__init__(action_type, params, plugin_context)
        self.adapter = MyTechnologyToJSONSchemaAdapter()
    
    async def execute(self, file_content, match, file_path, params):
        # Use specialized technology
        specialized_result = my_technology_validate(file_content)
        
        # Transform to HMA compliant format
        compliance_report = self.adapter.transform_report(
            specialized_result, 
            report_id=f"validation_{file_path}"
        )
        
        # Log compliance report
        self.log_port.log_info("Validation completed",
                              report_id=compliance_report.report_id,
                              overall_valid=compliance_report.overall_valid)
        
        return file_content
```

### Event Publishing

Compliance reports can be published as events:

```python
# Publish validation event with compliance report
await self.publish_event(
    "validation_completed",
    {
        "file_path": file_path,
        "compliance_report": compliance_report.to_dict(),
        "adapter_used": "MyTechnologyToJSONSchemaAdapter"
    }
)
```

## Performance Considerations

### Caching Strategies

```python
from functools import lru_cache

class OptimizedAdapter:
    
    @lru_cache(maxsize=128)
    def transform_cached(self, data_hash: str, data: Any) -> ComplianceReport:
        """Cache expensive transformations."""
        return self.transform_report(data)
```

### Streaming Processing

```python
async def transform_large_dataset(self, data_stream):
    """Process large datasets in chunks."""
    async for chunk in data_stream:
        compliance_chunk = self.transform_report(chunk)
        yield compliance_chunk
```

## Security Considerations

- **Input Validation**: Validate all inputs before processing
- **Error Information**: Avoid leaking sensitive information in error messages
- **Resource Limits**: Prevent resource exhaustion with large inputs
- **Audit Logging**: Log all transformation activities

### Secure Transformation

```python
def secure_transform(self, source_data: Any) -> ComplianceReport:
    """Securely transform data with validation and sanitization."""
    
    # Validate input structure
    if not self._validate_input(source_data):
        raise ValidationError("Invalid input structure")
    
    # Sanitize sensitive data
    sanitized_data = self._sanitize_data(source_data)
    
    # Perform transformation
    result = self._transform_internal(sanitized_data)
    
    # Audit log the transformation
    self.logger.info("Transformation completed",
                    input_type=type(source_data).__name__,
                    output_valid=result.overall_valid,
                    violation_count=result.total_violations)
    
    return result
```

## Monitoring and Observability

### Metrics Collection

```python
def transform_with_metrics(self, data: Any) -> ComplianceReport:
    """Transform with comprehensive metrics collection."""
    
    start_time = time.time()
    
    try:
        result = self.transform_report(data)
        
        # Record success metrics
        self.telemetry.emit_metric(
            "adapter_transformations_total", 1.0,
            {
                "adapter_type": self.__class__.__name__,
                "status": "success",
                "valid": str(result.overall_valid)
            }
        )
        
        return result
        
    except Exception as e:
        # Record error metrics
        self.telemetry.emit_metric(
            "adapter_transformations_total", 1.0,
            {
                "adapter_type": self.__class__.__name__,
                "status": "error",
                "error_type": type(e).__name__
            }
        )
        raise
    
    finally:
        # Record duration metrics
        duration = (time.time() - start_time) * 1000
        self.telemetry.emit_metric(
            "adapter_transformation_duration_ms", duration,
            {"adapter_type": self.__class__.__name__}
        )
```

## Troubleshooting

### Common Issues

- **Transformation Failures**: Usually due to unexpected input formats
- **Performance Issues**: Large datasets may require streaming or caching
- **Memory Usage**: Complex transformations may consume significant memory
- **Compatibility Issues**: Source technology version changes may break adapters

### Debug Utilities

```python
def debug_transformation(self, data: Any) -> Dict[str, Any]:
    """Debug utility for troubleshooting transformations."""
    
    return {
        "input_type": type(data).__name__,
        "input_size": len(str(data)) if data else 0,
        "adapter_version": self.adapter_version,
        "transformation_steps": self._get_transformation_steps(data),
        "expected_output_format": "HMAComplianceReport"
    }
```

## Future Enhancements

### Planned Adapters

- **GraphQL to OpenAPI**: Transform GraphQL schemas to OpenAPI specifications
- **Prometheus to OpenTelemetry**: Bridge Prometheus metrics to OpenTelemetry format
- **Custom Schema to JSON Schema**: Transform proprietary schemas to JSON Schema

### Enhancement Opportunities

- **Bidirectional Transformation**: Support reverse transformations (Tier 1 → Tier 3)
- **Chain Adapters**: Support adapter pipelines for complex transformations
- **Performance Optimization**: Implement parallel processing for large datasets
- **Schema Evolution**: Support automated schema migration and version handling

## Related Documentation

- [HMA v2.2 Specification](../../HMA v2.2/) - Architecture specification
- [ADR-003: SHACL JSON Bridge](../docs/decisions/ADR-003-shacl-json-bridge.md) - Design rationale
- [Plugin Development](../actions/README.md) - Integration with plugins
- [Core Architecture](../core/README.md) - Core component integration