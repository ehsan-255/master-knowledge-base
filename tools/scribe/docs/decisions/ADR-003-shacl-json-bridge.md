# ADR-003: SHACL to JSON Schema Compliance Bridge

## Status
**Accepted** - July 24, 2025

## Context

The Enhanced Frontmatter Action uses SHACL (Shapes Constraint Language) for semantic validation of frontmatter structures. While SHACL provides powerful RDF-based validation capabilities, it falls into HMA v2.2's Tier 3 (Alternative) technologies.

HMA v2.2 requires that Tier 3 technologies implement "compliance adapters" to bridge to Tier 1 mandatory standards. The challenge was to maintain SHACL's semantic validation power while ensuring interoperability with JSON Schema validation (Tier 1 mandatory).

### Problem Statement
- SHACL validation produces RDF-based reports that are not compatible with standard tooling
- HMA v2.2 mandates JSON Schema validation as Tier 1 technology
- Need to preserve SHACL's advanced validation capabilities while ensuring compliance

## Decision

We will implement a **SHACLToJSONSchemaAdapter** that transforms SHACL validation results into HMA v2.2 compliant JSON Schema validation reports.

### Adapter Architecture

1. **Compliance Bridge Pattern**: Transform Tier 3 outputs to Tier 1 formats
2. **Standardized Results**: Convert SHACL violation reports to standardized validation results
3. **HMA Report Format**: Generate HMA v2.2 compliant validation reports with full metadata
4. **Bidirectional Support**: Support both SHACL-first and JSON Schema-first workflows

### Technical Implementation

```python
# Core components
class ValidationResult:         # Standardized violation structure
class ComplianceReport:         # HMA v2.2 compliant report format
class SHACLToJSONSchemaAdapter: # Main bridge implementation

# Key methods
def transform_shacl_report()           # Convert SHACL to standard format
def create_json_schema_report()        # Generate JSON Schema report
def validate_with_compliance_bridge()  # End-to-end validation
```

### HMA Compliance Strategy

- **Input Tier**: 3 (Alternative) - SHACL RDF graphs
- **Output Tier**: 1 (Mandatory) - JSON Schema validation reports
- **Bridge Type**: Technology compliance adapter
- **Compliance Level**: Full HMA v2.2 compliance through transformation

## Consequences

### Positive
- ✅ **HMA Compliance**: Maintains Tier 1 compliance while using Tier 3 technology
- ✅ **Tool Interoperability**: JSON Schema reports work with standard tooling
- ✅ **Semantic Power**: Retains SHACL's advanced validation capabilities
- ✅ **Standardization**: Consistent validation report format across the system
- ✅ **Flexibility**: Can switch between SHACL and pure JSON Schema as needed

### Negative
- ❌ **Complexity**: Additional transformation layer adds complexity
- ❌ **Performance**: Some overhead from format transformation
- ❌ **Maintenance**: Need to maintain mapping between SHACL and JSON Schema concepts

### Use Cases Enabled
- Advanced semantic validation with standards compliance
- Integration with CI/CD pipelines expecting JSON Schema reports
- Compatibility with monitoring and alerting systems
- Future migration path from SHACL to pure JSON Schema if needed

## Implementation Status

### Completed Components
- ✅ `ValidationResult` dataclass for standardized violations
- ✅ `ComplianceReport` dataclass for HMA v2.2 reports
- ✅ `SHACLToJSONSchemaAdapter` main implementation
- ✅ SHACL violation extraction and transformation logic
- ✅ JSON Schema report generation
- ✅ Error handling and fallback reporting

### Key Features
- **Severity Mapping**: SHACL severities mapped to standard levels (ERROR, WARNING, INFO)
- **Metadata Preservation**: Source locations, constraint components, and focus nodes preserved
- **Report Versioning**: Full report metadata with timestamps and version tracking
- **Error Resilience**: Graceful handling of malformed SHACL reports

### Usage Example

```python
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

## Future Considerations

1. **Performance Optimization**: Consider caching for frequently used shapes
2. **Schema Evolution**: Plan for SHACL to JSON Schema schema migration paths
3. **Validation Enhancement**: Add support for more SHACL constraint types
4. **Integration**: Consider deeper integration with frontmatter processing pipeline

## Related ADRs
- ADR-005: HMA v2.2 Compliance Strategy
- ADR-002: Ports and Adapters Architecture