---
title: Untitled Document
info-type: general
version: 0.0.1
date-created: '2025-06-17'
date-modified: '2025-06-17T02:29:16Z'
tags:
- content-type/general
- criticality/p0-critical
- kb-id/global
kb-id: tools
primary-topic: '[MISSING_PRIMARY_TOPIC]'
scope_application: '[MISSING_SCOPE_APPLICATION]'
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas: []
---
# Knowledge Base Tools - Comprehensive Documentation

**Generated**: 2025-06-09 23:10:50  
**Version**: 3.1.0  
**Scope**: Complete documentation of all tools, utilities, and automation systems  

---

## 🎯 Overview

The `tools/` directory contains a comprehensive suite of automation tools, utilities, and systems for managing the knowledge base. This includes content validation, naming enforcement, build systems, and advanced automation engines.

## 📁 Directory Structure

```
tools/
├── builder/                    # Collection generation and build tools
├── file-format-utils/          # File format conversion and cleanup utilities
├── frontmatter-management/     # YAML frontmatter processing and management
├── indexer/                    # Standards index generation with JSON-LD schema
├── linter/                     # Comprehensive content validation and linting
├── naming-enforcer/            # Advanced naming convention enforcement system
├── refactoring-scripts/        # Content refactoring and transformation tools
├── scribe/                     # Advanced automation engine with event processing
├── utilities/                  # General purpose utilities and helpers
├── validators/                 # Data validation and integrity checking tools
├── changelog.md               # Centralized changelog for all tools
└── README.md                  # This comprehensive documentation
```

---

## 🏗️ Builder Tools

**Location**: `tools/builder/`  
**Purpose**: Generate derived collection documents and build artifacts

### Files

#### `generate_collections.py`
**Purpose**: Creates derived collection documents from standards index  
**Functionality**:
- Loads collection definitions from YAML configuration
- Filters standards based on criteria (domain, type, tags)
- Generates markdown collection documents with internal linking
- Resolves `[[STANDARD_ID]]` links within collections
- Creates table of contents and frontmatter

**Usage**:
```bash
python tools/builder/generate_collections.py
python tools/builder/generate_collections.py --config custom-collections.yaml
```

**Key Features**:
- GitHub Flavored Markdown (GFM) anchor generation
- Intra-collection link resolution
- Automatic frontmatter generation
- Criteria-based filtering (equals, in, not_equals, not_in)

#### `collection_definitions.yaml`
**Purpose**: Configuration file defining collection criteria and output settings  
**Structure**:
```yaml
collections:
  - id: "domain-specific-collection"
    title: "Domain Specific Standards"
    criteria:
      - field: "primary_domain"
        operator: "equals"
        value: "GM"
    output_filename: "gm-standards.md"
```

---

## 📄 File Format Utils

**Location**: `tools/file-format-utils/`  
**Purpose**: File format conversion and standardization utilities

### Files

#### `crlf_to_lf_converter.py`
**Purpose**: Converts line endings from CRLF/CR to LF for cross-platform compatibility  
**Functionality**:
- Scans directories recursively for `.md` files
- Detects CRLF (`\r\n`) and CR (`\r`) line endings
- Converts to LF (`\n`) line endings
- Supports dry-run mode for safe testing

**Usage**:
```bash
# Dry run (safe preview)
python tools/file-format-utils/crlf_to_lf_converter.py --dry-run ./standards

# Live conversion
python tools/file-format-utils/crlf_to_lf_converter.py ./standards ./tools
```

**Features**:
- Binary file reading for accurate detection
- Comprehensive logging of changes
- Error handling for file access issues

#### `add_readme_frontmatter.py`
**Purpose**: Automatically adds standardized frontmatter to README.md files  
**Functionality**:
- Generates standard_id based on directory structure
- Creates canonical frontmatter with proper field ordering
- Extracts title from first H1 heading
- Determines kb-id based on file location

**Usage**:
```bash
python tools/file-format-utils/add_readme_frontmatter.py
```

**Target Files**:
- `tools/README.md`
- `tools/linter/README.md`
- `tools/builder/README.md`
- `tools/indexer/README.md`
- `standards/README.md`
- `standards/templates/README.md`

**Generated Fields**:
- `title`, `standard_id`, `aliases`, `tags`
- `kb-id`, `info-type`, `primary-topic`
- `version`, `date-created`, `date-modified`
- `primary_domain`, `sub_domain`, `scope_application`
- `criticality`, `lifecycle_gatekeeper`, `impact_areas`

---

## 📝 Frontmatter Management

**Location**: `tools/frontmatter-management/`  
**Purpose**: YAML frontmatter processing, organization, and management

### Files

#### `date_time_manager.py`
**Purpose**: Manages date-created and date-modified fields in frontmatter  
**Functionality**:
- Updates timestamps based on file system metadata
- Supports both date-only and date-time formats
- Git integration for real change detection
- Date locking mechanism to prevent automatic updates

**Usage**:
```bash
# Update all files with filesystem timestamps
python tools/frontmatter-management/date_time_manager.py scan

# Update specific files with custom date
python tools/frontmatter-management/date_time_manager.py update file1.md --date 2025-01-11

# Update with time precision (for commits)
python tools/frontmatter-management/date_time_manager.py scan --time

# Lock dates to prevent automatic updates
python tools/frontmatter-management/date_time_manager.py lock file.md

# Update only files with real content changes
python tools/frontmatter-management/date_time_manager.py commit-update --time
```

**Date Formats**:
- Simple: `YYYY-MM-DD` (e.g., `2025-01-11`)
- With Time: `YYYY-MM-DD-HH-MM` (e.g., `2025-01-11-14-30`)

**Features**:
- Real change detection via Git integration
- Date locking with `# date-locked` marker
- Comprehensive logging and error handling
- Backup creation before modifications

#### `frontmatter_organizer.py`
**Purpose**: Reorders frontmatter keys according to canonical order  
**Functionality**:
- Enforces canonical key ordering from linter standards
- Preserves all content while reorganizing structure
- Creates backups before modifications
- Validates YAML syntax

**Usage**:
```bash
# Organize single file
python tools/frontmatter-management/frontmatter_organizer.py --file document.md

# Organize entire directory
python tools/frontmatter-management/frontmatter_organizer.py --directory ./standards

# Dry run preview
python tools/frontmatter-management/frontmatter_organizer.py --directory . --dry-run
```

**Canonical Order**:
```yaml
title, standard_id, aliases, tags, kb-id, info-type,
primary-topic, related-standards, version, date-created,
date-modified, primary_domain, sub_domain, scope_application,
criticality, lifecycle_gatekeeper, impact_areas
```

#### `view_generator.py`
**Purpose**: Generates human-readable views from JSON-LD Single Source of Truth  
**Functionality**:
- Converts JSON-LD schema definitions to markdown documentation
- Creates YAML views for human editing
- Supports multiple output formats (markdown, YAML, JSON)
- Maintains bidirectional workflow with change request system

**Usage**:
```bash
# Generate markdown documentation from JSON-LD
python tools/view_generator.py --id AS-SCHEMA-FRONTMATTER --format markdown

# Generate YAML view for editing
python tools/view_generator.py --id AS-SCHEMA-FRONTMATTER --format yaml

# Generate all views
python tools/view_generator.py --generate-all
```

**Features**:
- JSON-LD to human-readable conversion
- Schema validation and consistency checking
- Integration with change request workflow
- Multiple output format support

---

## 📝 Change Request Workflow

**Location**: `change-requests/`  
**Purpose**: Human-friendly interface for modifying JSON-LD Single Source of Truth

### Workflow Process

1. **Generate Human-Readable View**: Use `tools/view_generator.py` to create YAML/MD from JSON-LD
2. **Edit YAML File**: Make changes to the human-readable YAML file
3. **Submit Change Request**: Place edited YAML in `change-requests/` directory
4. **Automated Processing**: Scribe workflow processes changes and updates JSON-LD SST
5. **Validation**: Changes are validated against schema and applied to authoritative JSON-LD files

### Directory Structure
```
change-requests/
├── .gitkeep                    # Ensures directory exists in git
├── schema-updates/             # Schema modification requests
├── vocabulary-updates/         # Controlled vocabulary changes
└── processed/                  # Completed change requests (archived)
```

### Usage Example
```bash
# 1. Generate editable YAML from JSON-LD
python tools/view_generator.py --id AS-SCHEMA-FRONTMATTER --format yaml --output change-requests/schema-updates/

# 2. Edit the generated YAML file
# 3. Commit changes - Scribe workflow will process automatically

# 4. Verify changes applied to JSON-LD
python tools/validators/validate_registry.py
```

---

## 📇 Indexer

**Location**: `tools/indexer/`  
**Purpose**: Standards index generation with JSON-LD schema validation

### Files

#### `generate_index.py`
**Purpose**: Generates comprehensive standards index from markdown files  
**Functionality**:
- Scans standards directories for markdown files
- Extracts metadata from frontmatter
- Validates against JSON schema
- Generates JSON index with statistics

**Usage**:
```bash
# Generate index with defaults
python tools/indexer/generate_index.py

# Custom source directories
python tools/indexer/generate_index.py --src-dirs standards/src custom/standards

# Custom output location
python tools/indexer/generate_index.py --output-dir ./dist --output-filename custom-index.json

# Debug mode
python tools/indexer/generate_index.py --log-level DEBUG
```

**Required Fields**:
- `standard_id`, `title`, `primary_domain`, `sub_domain`
- `info-type`, `version`, `status`, `filepath`
- `date-modified`, `date-created`, `criticality`, `lifecycle_gatekeeper`

**Features**:
- JSON schema validation
- Duplicate standard_id detection
- Comprehensive error reporting
- Statistics and summary generation

#### `standards_index.schema.json`
**Purpose**: JSON Schema for validating standards index structure  
**Functionality**:
- Defines required fields and data types
- Validates index structure and content
- Ensures data consistency and completeness

**Schema Structure**:
```json
{
  "schemaVersion": "string",
  "generatedDate": "ISO 8601 datetime",
  "standards": [
    {
      "standard_id": "string",
      "title": "string",
      "primary_domain": "string",
      // ... additional fields
    }
  ]
}
```

#### `OM-SPEC-STANDARDS-INDEX-JSONLD.md`
**Purpose**: Specification document for JSON-LD standards index format  
**Content**: Technical specification for index structure, schema requirements, and usage guidelines

---

## 🔍 Linter

**Location**: `tools/linter/`  
**Purpose**: Comprehensive content validation and linting system

### Files

#### `kb_linter.py`
**Purpose**: Advanced knowledge base content validation and linting  
**Functionality**:
- Frontmatter validation against schema
- Standard ID format validation
- Date format validation (ISO 8601)
- Tag format validation (kebab-case)
- Internal link validation
- Controlled vocabulary validation
- Field ordering validation

**Usage**:
```bash
# Lint entire directory
python tools/linter/kb_linter.py --directory ./standards

# Lint specific files
python tools/linter/kb_linter.py --files file1.md file2.md

# Generate detailed report
python tools/linter/kb_linter.py --directory . --output-format detailed

# CI-friendly mode
python tools/linter/kb_linter.py --directory . --ci-mode
```

**Validation Categories**:
- **Frontmatter Structure**: YAML syntax, required fields, field types
- **Standard ID Format**: `^[A-Z]{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*$`
- **Date Validation**: ISO 8601 format compliance
- **Tag Validation**: Kebab-case format, category prefixes
- **Link Validation**: Internal link resolution, anchor validation
- **Vocabulary Validation**: Controlled vocabulary compliance

**Configuration Sources**:
- `standards/registry/mt-schema-frontmatter.yaml`
- `standards/registry/mt-registry-tag-glossary.yaml`
- `dist/standards_index.json`

**Features**:
- Line-number accurate error reporting
- Severity levels (error, warning, info)
- Comprehensive logging
- Standards index integration
- Controlled vocabulary loading

---



## 🏷️ Naming Enforcer

**Location**: `tools/naming-enforcer/`  
**Purpose**: Advanced naming convention enforcement system with single source of truth

### Files

#### `naming_enforcer.py`
**Purpose**: Comprehensive naming convention enforcement with dynamic rule parsing  
**Functionality**:
- Parses naming rules directly from `GM-CONVENTIONS-NAMING.md`
- Context-aware validation (files, directories, frontmatter)
- Protected name management
- Exception handling
- Content reference updating
- Comprehensive violation reporting

**Usage**:
```bash
# Scan for violations (safe)
python tools/naming-enforcer/naming_enforcer.py scan

# Dry run with detailed report
python tools/naming-enforcer/naming_enforcer.py scan --dry-run --verbose

# Apply fixes (DANGEROUS - requires link updating)
python tools/naming-enforcer/naming_enforcer.py fix --dry-run

# Scan specific directory
python tools/naming-enforcer/naming_enforcer.py scan --directory ./standards
```

**Validation Contexts**:
- **Files**: Kebab-case with context-specific exceptions
- **Directories**: Kebab-case with system exceptions
- **Frontmatter Fields**: Field-specific naming conventions
- **Standard IDs**: UPPERCASE domain-based format

**Features**:
- Single source of truth parsing from markdown
- Context-aware naming conventions
- Protected name framework
- Exception pattern management
- Content reference tracking
- Comprehensive safety logging

#### `generate_naming_configs.py`
**Purpose**: Generates configuration files from naming standard markdown  
**Functionality**:
- Parses `GM-CONVENTIONS-NAMING.md`
- Extracts naming patterns and rules
- Generates JSON configuration files
- Creates exception and protection lists

#### `naming_exceptions.json`
**Purpose**: System-generated exception patterns  
**Content**: Automatically generated from naming standard, contains file and directory exceptions

#### `protected-names.json`
**Purpose**: System-generated protected names list  
**Content**: Critical system dependencies and hardcoded names that must not be modified

#### `recover_backup.py`
**Purpose**: Recovery utility for naming enforcer operations  
**Functionality**:
- Restores files from naming enforcer backups
- Validates backup integrity
- Provides selective recovery options

#### `.namingignore`
**Purpose**: Exclusion patterns for naming enforcer  
**Content**: Patterns for files and directories to exclude from naming validation

#### `.naminginclude`
**Purpose**: Inclusion patterns for naming enforcer  
**Content**: Patterns for files and directories to explicitly include in validation

---

## 🔄 Refactoring Scripts

**Location**: `tools/refactoring-scripts/`  
**Purpose**: Content refactoring and transformation tools

### Files

#### `refactor_ids_filenames.py`
**Purpose**: Refactors standard IDs and filenames to canonical format  
**Functionality**:
- Converts standard_id to UPPERCASE format
- Handles changelog suffix normalization (-CHANGELOG)
- Updates filenames to match standard_id casing
- Updates titles derived from standard_id
- Supports dry-run mode for safe testing

**Usage**:
```bash
# Dry run to preview changes
python tools/refactoring-scripts/refactor_ids_filenames.py --dry-run ./standards

# Live refactoring
python tools/refactoring-scripts/refactor_ids_filenames.py ./standards

# Process single file
python tools/refactoring-scripts/refactor_ids_filenames.py --file document.md
```

**Transformations**:
- `gm-guide-example` → `GM-GUIDE-EXAMPLE`
- `changelog-file.md` → `CHANGELOG-FILE.MD`
- Title updates for derived titles

#### `refactor_criticality_field.py`
**Purpose**: Refactors criticality field values to standard format  
**Functionality**:
- Normalizes criticality values (P0-Critical, P1-High, etc.)
- Updates both frontmatter fields and tags
- Validates against controlled vocabulary
- Provides comprehensive change logging

**Usage**:
```bash
python tools/refactoring-scripts/refactor_criticality_field.py --directory ./standards
python tools/refactoring-scripts/refactor_criticality_field.py --dry-run
```

#### `refactor_tag_casing.py`
**Purpose**: Refactors tag casing to kebab-case format  
**Functionality**:
- Converts tags to lowercase kebab-case
- Preserves tag category prefixes
- Validates tag format compliance
- Updates tag arrays in frontmatter

**Usage**:
```bash
python tools/refactoring-scripts/refactor_tag_casing.py --directory ./standards
python tools/refactoring-scripts/refactor_tag_casing.py --file document.md --dry-run
```

---

## 🤖 Scribe Automation Engine

**Location**: `tools/scribe/`  
**Purpose**: Advanced automation engine with event processing and rule-based actions

### Overview
Scribe is a sophisticated automation engine that monitors file system events and executes rule-based actions. It implements a microkernel architecture with producer-consumer patterns for high-performance event processing.

### Core Components

#### `engine.py`
**Purpose**: Main orchestrator for the Scribe automation engine  
**Functionality**:
- Coordinates producer-consumer pipeline
- Manages engine lifecycle and health monitoring
- Provides status reporting and statistics
- Handles graceful shutdown and error recovery

#### `watcher.py`
**Purpose**: File system event monitoring (Producer)  
**Functionality**:
- Monitors file system changes using watchdog
- Filters events based on file patterns
- Queues events for worker processing
- Provides event statistics and monitoring

#### `worker.py`
**Purpose**: Event processing worker (Consumer)  
**Functionality**:
- Processes events from queue
- Executes rule matching and action dispatching
- Performs atomic file operations
- Tracks processing statistics

### Core Services

#### `core/config_manager.py`
**Purpose**: Configuration management with hot-reloading  
**Features**:
- JSON schema validation
- Hot-reloading with file system watching
- Plugin configuration management
- Security settings management

#### `core/plugin_loader.py`
**Purpose**: Dynamic plugin loading and management  
**Features**:
- Multiple plugin directory support
- Hot-reloading capabilities
- Dependency resolution
- Security validation
- Runtime plugin management

#### `core/security_manager.py`
**Purpose**: Security enforcement for action execution  
**Features**:
- Command whitelisting
- Path restrictions
- Environment variable scrubbing
- Parameter validation
- Secure command execution

#### `core/rule_processor.py`
**Purpose**: Rule matching and processing  
**Features**:
- Pattern-based rule matching
- File content analysis
- Rule priority handling
- Match result generation

#### `core/action_dispatcher.py`
**Purpose**: Action execution and orchestration  
**Features**:
- Action plugin management
- Execution pipeline coordination
- Circuit breaker pattern
- Statistics collection

#### `core/health_server.py`
**Purpose**: Health monitoring HTTP server  
**Features**:
- RESTful health endpoints
- Real-time statistics
- Component status monitoring
- Performance metrics

### Action Plugins

#### `actions/base.py`
**Purpose**: Base class for all action plugins  
**Features**:
- Standardized plugin interface
- Parameter validation
- Error handling framework
- Logging integration

#### `actions/run_command_action.py`
**Purpose**: Secure command execution action  
**Features**:
- Security manager integration
- Environment variable control
- Command validation
- Output capture

### Usage
```bash
# Start Scribe engine
python tools/scribe/engine.py

# Monitor specific directories
python tools/scribe/engine.py --watch-paths ./standards ./tools

# Custom configuration
python tools/scribe/engine.py --config custom-config.json
```

---

## 🛠️ Utilities

**Location**: `tools/utilities/`  
**Purpose**: General purpose utilities and helper tools

### Files

#### `todo_tracker.py`
**Purpose**: Scans for and reports TODO markers in markdown files  
**Functionality**:
- Scans for `> [!TODO]` Obsidian-compatible callouts
- Extracts context lines before and after TODOs
- Generates multiple report formats (console, markdown, JSON)
- Provides TODO statistics and summaries

**Usage**:
```bash
# Scan and show console report
python tools/utilities/todo_tracker.py scan

# Generate markdown report
python tools/utilities/todo_tracker.py report --format markdown --output todo-report.md

# Get statistics
python tools/utilities/todo_tracker.py stats

# Custom directory
python tools/utilities/todo_tracker.py scan --directory ./standards
```

**TODO Format**:
```markdown
> [!TODO] This needs to be implemented
> [!TODO] Fix the validation logic here
```

**Output Formats**:
- **Console**: Quick summary with file counts
- **Markdown**: Detailed report with context
- **JSON**: Machine-readable data for automation

#### `README-repo-tree.md`
**Purpose**: Documentation for repository tree generation utility

### Subdirectory: repo-tree

#### `main_repo_tree.py`
**Purpose**: Generates formatted repository tree structure  
**Functionality**:
- Creates visual tree representation of repository
- Uses configuration files for customization
- Supports icons, annotations, and exclusions
- Generates markdown output with legend

**Usage**:
```bash
python tools/utilities/repo-tree/main_repo_tree.py
```

**Configuration Files**:
- `.treeignore`: Folders to completely exclude
- `.subtreeignore`: Folders to show but not expand
- `.treeaddtext`: Annotations for specific paths
- `.treeicon`: Icons for specific paths

**Output**: `repo-tree.md` in repository root

#### `.treeignore`
**Purpose**: Exclusion patterns for tree generation  
**Content**: Patterns for directories to completely exclude from tree

#### `.subtreeignore`
**Purpose**: Partial exclusion patterns  
**Content**: Directories to show but not expand contents

#### `.treeaddtext`
**Purpose**: Path annotations  
**Content**: Custom annotations for specific directories and files

#### `.treeicon`
**Purpose**: Icon assignments  
**Content**: Icon and description assignments for paths

---

## ✅ Validators

**Location**: `tools/validators/`  
**Purpose**: Data validation and integrity checking tools

### Files

#### `validate_registry.py`
**Purpose**: Validates registry files and data integrity  
**Functionality**:
- Validates YAML registry files
- Checks data consistency
- Verifies controlled vocabularies
- Generates validation reports

**Usage**:
```bash
python tools/validators/validate_registry.py
python tools/validators/validate_registry.py --registry-dir ./standards/registry
```

---

## 📋 Root Level Files

### `changelog.md`
**Purpose**: Centralized changelog for all tools  
**Content**: Version history, major changes, and decisions affecting tools

**Recent Changes**:
- **v2.0.0**: Major overhaul with naming enforcer rewrite and tool organization
- **v1.0.0**: Restructure to folder-level changelogs

---

## 🚀 Quick Start Guide

### Essential Daily Operations

```bash
# 1. Update timestamps for modified files
python tools/frontmatter-management/date_time_manager.py scan --time

# 2. Check for TODO items
python tools/utilities/todo_tracker.py scan

# 3. Validate content
python tools/linter/kb_linter.py --directory ./standards

# 4. Check naming conventions
python tools/naming-enforcer/naming_enforcer.py scan

# 5. Generate updated index
python tools/indexer/generate_index.py
```

### Before Major Changes

```bash
# 1. Run comprehensive validation
python tools/linter/kb_linter.py --directory . --ci-mode

# 2. Check naming violations
python tools/naming-enforcer/naming_enforcer.py scan --verbose

# 3. Generate updated repository tree
python tools/utilities/repo-tree/main_repo_tree.py
```

### Automation Integration

```bash
# Start Scribe automation engine
python tools/scribe/engine.py --watch-paths ./standards ./tools

# Generate collections
python tools/builder/generate_collections.py

# Update repository tree
python tools/utilities/repo-tree/main_repo_tree.py
```

---

## ⚠️ Safety Guidelines

### Critical Safety Rules

1. **ALWAYS run dry-run first** for any tool that modifies files
2. **Review logs carefully** before proceeding with live operations
3. **Create backups** before major operations
4. **Test in isolated environment** for complex operations
5. **Validate results** after any automated changes

### High-Risk Operations

- **Naming Enforcer Live Mode**: Can break links without proper link updating
- **Refactoring Scripts**: Modifies content and filenames
- **File Format Conversion**: Changes file encoding

### Recovery Procedures

- **Backup Restoration**: Use tool-specific backup recovery utilities
- **Git Rollback**: Use version control for content recovery
- **Manual Verification**: Always verify automated changes manually

---

## 🔗 Integration Points

### Tool Dependencies

- **Linter** ← Registry files, Standards index
- **Indexer** → Standards index → Builder, Linter
- **Naming Enforcer** ← Naming standards document
- **Scribe** → All automation workflows

### Data Flow

```
Standards Files → Indexer → Standards Index → Builder → Collections
                     ↓
                  Linter ← Registry Files
                     ↓
               Validation Reports
```

### Configuration Sources

- `tools/scribe/config/config.json` - Scribe engine configuration
- `standards/registry/` - Validation vocabularies and schemas
- `tools/builder/collection_definitions.yaml` - Collection generation
- `tools/naming-enforcer/.naming*` - Naming enforcement configuration

---

## 📊 Monitoring and Reporting

### Automated Reports

- **TODO Reports**: Generated by todo_tracker.py
- **Validation Reports**: Generated by kb_linter.py
- **Naming Violation Reports**: Generated by naming_enforcer.py

### Health Monitoring

- **Scribe Health Endpoint**: `http://localhost:9468/health`
- **Tool Execution Logs**: Stored in `tools/reports/`
- **Error Tracking**: Comprehensive logging across all tools

### Performance Metrics

- **Processing Times**: Tracked by individual tools
- **Success Rates**: Validation and processing success rates
- **Resource Usage**: Memory and CPU usage monitoring

---

*This documentation covers all tools and utilities in the knowledge base automation system. For specific tool usage and advanced configuration, refer to individual tool documentation and help commands.*
