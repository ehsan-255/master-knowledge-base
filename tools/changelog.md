---
title: Tools Changelog
standard_id: OM-TOOLS-CHANGELOG
aliases:
- Knowledge Base Tools Change Log
- Tools History
tags:
- content-type/changelog
- criticality/p4-informational
- kb-id/global
- status/active
- topic/automation
- topic/om
- topic/tools-management
kb-id: tools
info-type: changelog
primary-topic: Tracks changes, decisions, and major updates for all tools in the master
  knowledge base
related-standards: []
version: 1.0.0
date-created: '2025-01-11T00:00:00Z'
date-modified: '2025-06-17T02:29:16Z'
primary_domain: OM
sub_domain: AUTOMATION
scope_application: Documents changes and decisions affecting tools in tools/ and its
  subdirectories
criticality: P4-Informational
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Tools development
- Automation workflows
- Build processes
- Maintenance operations
change_log_url: ./changelog.md
---
# Tools Changelog

This document tracks changes, decisions, and major updates for all tools in the master knowledge base.

## Version 2.0.0 (2025-06-03)

**MAJOR OVERHAUL: Naming Enforcer System Complete Rewrite and Tool Organization**

### Added
- **`naming-enforcer/` subfolder**: Centralized all naming convention tools
  - `naming_enforcer.py` - Complete rewrite with single source of truth parsing
  - `generate_naming_configs.py` - Configuration generator from SF-CONVENTIONS-NAMING.md
  - `naming_exceptions.json` - System-generated exception patterns
  - `protected-names.json` - System-generated protected names list
- **`utilities/` subfolder**: General purpose tools
  - `todo_tracker.py` - TODO marker scanning and reporting utility

### Changed
- **Tools organization**: Restructured from flat to organized subfolder structure
- **Naming enforcer architecture**: Complete rewrite from JSON-based to dynamic markdown parsing
- **Single source of truth**: All naming rules now parsed from SF-CONVENTIONS-NAMING.md
- **Context-aware validation**: Different naming conventions for different file types and contexts
- **Protection framework**: Absolute protection for system dependencies and hardcoded names

### Removed/Archived
- **Archive consolidation**: Moved all legacy archives to main archive location
- **Development artifacts**: Archived obsolete config files and backup scripts
- **Outdated tools**: Archived corruption_reverser.py (incorrect logic for new enforcer)

### Fixed
- **93% violation reduction**: Fixed massive false positive detection (111 → 8 violations)
- **Frontmatter parsing bug**: Fixed YAML value flagging as field names
- **JSON context misclassification**: Corrected filename vs content naming conventions
- **System directory scanning**: Added proper exclusions for .obsidian/.space/archive
- **Tool reports context**: Added lenient validation for generated files
- **Dynamic standard ID extraction**: Replaced hardcoded prefixes with parsing from standard

### Critical Safety Updates
- **Link breaking danger identified**: Tool will break all links without link updating implementation
- **Comprehensive logging requirement**: Added requirement for action logging during live runs
- **Emergency reversal capability**: Documented need for proper rollback procedures

### Impact
- **Production ready for dry-run**: Excellent detection accuracy, safe for validation
- **NOT safe for live run**: Critical link updating feature missing
- **System protection**: All critical dependencies protected from corruption
- **Maintainable architecture**: Single source of truth eliminates configuration drift

## Version 1.0.0 (2025-01-11)

**MAJOR RESTRUCTURE: Individual to Folder-Level Changelogs**

### Changed
- **Replaced individual changelog approach**: Removed individual changelog files that were auto-generated for tool documentation
- **Implemented folder-level changelog strategy**: Created centralized changelog file for all tools
- **Adopted kebab-case naming**: Using `changelog.md` instead of `CHANGELOG.MD` to follow standard file naming conventions

### Affected Tools
- **Linter**: `tools/linter/` - Enhanced with extension case fixing and line ending normalization
- **Frontmatter Management**: `tools/frontmatter-management/` - Individual changelog automation tools will be deprecated
- **File Format Utils**: `tools/file-format-utils/` - Various formatting and cleanup utilities
- **Indexer**: `tools/indexer/` - Standards index generation
- **Validators**: `tools/validators/` - Content validation tools
- **Refactoring Scripts**: `tools/refactoring-scripts/` - Cleanup and migration utilities

### Deprecated Tools
- `populate_changelog_fm.py` - No longer needed with folder-level changelog approach
- `refactor_changelog_links.py` - Replaced by centralized changelog references

### Rationale
- **Maintainability**: Centralized tracking of tool changes and decisions
- **Meaningful Granularity**: Tool changes often affect multiple components and workflows
- **Technical Debt Reduction**: Eliminated auto-generated changelog files that provided no value

### Impact
- Tool documentation will reference this centralized changelog
- Future tool changes and decisions will be documented once
- Simplified maintenance of changelog automation

---

*This changelog follows the requirements defined in [[OM-VERSIONING-CHANGELOGS]]*
