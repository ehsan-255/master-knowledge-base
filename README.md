# Master Knowledge Base

Welcome to the Master Knowledge Base (MKB)!

This repository serves as a central hub for various Knowledge Bases (KBs). It enforces strict standards for structure, formatting, style, and more. It also incorporates automation capabilities to ensure adherence to these standards and to facilitate other operational aspects.

## Repository Structure

The MKB follows a clean, organized structure with clear separation of concerns:

**Core Directories:**

*   **`master-knowledge-base/`**: Contains the core MKB infrastructure including standards, tools, and registry files
    *   **`standards/`**: Authoritative standards documentation and controlled vocabularies
    *   **`tools/`**: Production automation tools, scripts, and utilities (including the Scribe Engine)
*   **`active-project/`**: Current project management and ongoing initiatives
*   **`test-environment/`**: Centralized testing infrastructure with consolidated tool tests
*   **`archive/`**: Historical files and deprecated content with proper timestamping

## Recent Improvements (2025-06-07) - General MKB

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

---

## Scribe Automation Engine

The Scribe Automation Engine, located in `tools/scribe/`, is a sophisticated tool designed for automated file processing based on configurable rules and extensible actions. It has recently undergone significant refinements based on a comprehensive audit.

**Current Status (Post-Audit Refinements):** Fully Operational and Enhanced.

### Key Features & Recent Enhancements:

*   **Core Event Processing Pipeline**:
    *   The engine's primary pipeline for detecting file system events, matching them against user-defined rules, and dispatching actions is fully functional and robust.
    *   End-to-end processing is verified by automated integration tests.

*   **Security Enhancements**:
    *   **`allowed_env_vars` for `run_command` Action**: The `run_command` action plugin now supports an `allowed_env_vars` parameter in its configuration. This allows specific environment variables to be explicitly passed to executed commands, while all other variables are scrubbed, enhancing security by default. This feature has been tested and verified.

*   **Observability & Monitoring**:
    *   **Enhanced `/health` Endpoint**: The `/health` monitoring endpoint has been significantly improved. It now exposes detailed operational statistics, including:
        *   `action_dispatcher_stats`: Metrics from the ActionDispatcher, such as total dispatches, success/failure rates, and total execution time.
        *   `circuit_breaker_stats`: Status and metrics for all configured circuit breakers, providing insights into rule execution health and resilience.
    *   These enhancements provide greater visibility into the engine's internal state and performance.

*   **Plugin Architecture Improvements**:
    *   **Robust Plugin Loading**: The plugin loading mechanism (`PluginLoader`) has been refactored to correctly handle relative imports within action plugins (e.g., `from ..core import SecurityManager`). This ensures that plugins which are part of the Scribe package structure can reliably access shared core components.
    *   **Dependency Injection for Plugins**: Action plugins now receive necessary dependencies (e.g., `ConfigManager`, `SecurityManager`, action-specific `params`) directly through their constructors. This makes plugins more self-contained, easier to test, and aligns with better software design principles. The `RunCommandAction` plugin, for example, now correctly receives and utilizes the `SecurityManager` instance.

*   **Automated Testing**:
    *   The core event processing pipeline and key security features like `allowed_env_vars` are now verified by automated integration tests located in `test-environment/scribe-tests/test_full_pipeline.py`.
    *   These tests ensure the reliability and correctness of the implemented features.

The Scribe engine is now more secure, observable, and robust, with a more maintainable plugin architecture.

---

## Getting Started

**For New Contributors:**

1.  **Review Current Standards**: Explore `standards/src/` for the latest documentation standards and guidelines
2.  **Understand Project Management**: Check `active-project/` for current initiatives and project management approaches
3.  **Testing and Validation**: Use `test-environment/` for all testing activities - never test in production tool directories
4.  **Tool Usage**: Production tools in `tools/` are ready for use with consolidated registry sources. For Scribe Engine specific documentation, refer to its own README within the `tools/scribe/` directory (if available) or related design documents.

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

**Last Updated**: 2025-06-10 00:23 (Scribe Engine Refinements Completed)
**Repository Status**: Optimized and ready for production use. Scribe Engine Phase 1 & 2 Refinements Completed.
