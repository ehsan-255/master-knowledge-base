# Master Knowledge Base

Welcome to the Master Knowledge Base (MKB)!

This repository serves as a central hub for various Knowledge Bases (KBs). It enforces strict standards for structure, formatting, style, and more. It also incorporates automation capabilities to ensure adherence to these standards and to facilitate other operational aspects.

## Repository Structure

The MKB follows a clean, organized structure with clear separation of concerns:

**Core Directories:**

*   **`master-knowledge-base/`**: Contains the core MKB infrastructure including standards, tools, and registry files
    *   **`standards/`**: Authoritative standards documentation and controlled vocabularies
    *   **`tools/`**: Production automation tools, scripts, and utilities
*   **`active-project/`**: Current project management and ongoing initiatives
*   **`test-environment/`**: Centralized testing infrastructure with consolidated tool tests
*   **`archive/`**: Historical files and deprecated content with proper timestamping

## Recent Improvements (2025-06-07)

### Registry Consolidation Completed
- Multiple fragmented YAML registry files consolidated into unified sources
- `mt-schema-frontmatter.yaml` and `mt-registry-tag-glossary.yaml` serve as single sources of truth
- All tools and scripts updated to use consolidated sources
- Deprecated files properly archived with documentation

### Test Environment Optimization
- All scattered test directories consolidated into `test-environment/`
- Clean separation between production tools and testing infrastructure
- Centralized test execution and output management
- Improved repository organization following established standards

### Archive Management
- Proper archival of deprecated registry files with timestamping
- Clean removal of incorrectly placed archive directories
- Maintained audit trail for all consolidation activities

## Getting Started

**For New Contributors:**

1.  **Review Current Standards**: Explore `standards/src/` for the latest documentation standards and guidelines
2.  **Understand Project Management**: Check `active-project/` for current initiatives and project management approaches
3.  **Testing and Validation**: Use `test-environment/` for all testing activities - never test in production tool directories
4.  **Tool Usage**: Production tools in `tools/` are ready for use with consolidated registry sources

**For Repository Maintenance:**

1.  **Standards Updates**: All standards documentation in `standards/src/`
2.  **Registry Management**: Controlled vocabularies in `standards/registry/`
3.  **Tool Development**: Production tools in `tools/` with tests in `test-environment/`
4.  **Archive Policy**: Use `archive/` for historical content with proper timestamping

## Quality Assurance

The repository maintains high standards through:
- Automated linting and validation tools
- Consolidated registry sources for consistency
- Centralized testing infrastructure
- Comprehensive documentation standards
- Proper archive management with audit trails

We aim to create a robust and highly organized knowledge ecosystem. Your contributions and adherence to the established standards are appreciated.

---

**Last Updated**: 2025-06-07 09:45:00 (Post-consolidation and cleanup)
**Repository Status**: Optimized and ready for production use
