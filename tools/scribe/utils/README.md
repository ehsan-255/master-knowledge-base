# Scribe Utilities

This directory contains shared utility functions and modules used across the Scribe codebase. All utilities follow HMA v2.2 standards and provide technology-agnostic functionality.

## Available Utilities

### frontmatter_parser.py

**Purpose**: Consolidated YAML frontmatter parsing functionality for use across action plugins.

**Features**:
- Standardized parsing with error handling
- Preprocessing for special keys (e.g., `@key` formatting)
- Consistent YAML processing across plugins
- Cross-platform compatibility

**API**:
```python
from tools.scribe.utils.frontmatter_parser import (
    parse_frontmatter,
    has_frontmatter,
    remove_frontmatter,
    apply_frontmatter
)

# Parse frontmatter from document content
frontmatter_dict = parse_frontmatter(content)

# Check if content has frontmatter
if has_frontmatter(content):
    # Process accordingly

# Remove frontmatter from content
clean_content = remove_frontmatter(content)

# Apply frontmatter to content
updated_content = apply_frontmatter(content, frontmatter_dict)
```

**Used by**:
- `reconciliation_action.py` - Document reconciliation and indexing
- `enhanced_frontmatter_action.py` - LLM-enhanced frontmatter generation

**Migration Note**: This utility was created as part of DEP-007 cleanup to consolidate duplicated frontmatter parsing logic previously found in multiple plugins.

## Development Guidelines

### Adding New Utilities

1. **Scope**: Utilities should be technology-agnostic and reusable across plugins
2. **Documentation**: Include comprehensive docstrings and usage examples
3. **Testing**: Add unit tests with edge case coverage
4. **Import Path**: Use consistent import paths: `from tools.scribe.utils.module_name import function`

### Design Principles

- **Pure Functions**: Prefer stateless, pure functions where possible
- **Error Handling**: Robust error handling with meaningful error messages
- **Type Hints**: Use proper type annotations for all functions
- **Cross-Platform**: Ensure compatibility across Windows, macOS, and Linux

## Testing

```bash
# Test utilities
cd tools/scribe
python -m pytest utils/ -v
```

## Related Documentation

- [Plugin Development](../actions/README.md) - Using utilities in plugins
- [Architecture Decision Records](../docs/decisions/) - Design decisions for utilities