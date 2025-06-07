---
title: 'Standard: Universal Naming Conventions - Single Source of Truth'
standard_id: GM-CONVENTIONS-NAMING
aliases:
  - Naming Conventions
  - File Naming
  - ID Conventions
  - Universal Naming Standard
  - Single Source of Truth for Naming
tags:
  - status/active
  - criticality/p0-critical
  - content-type/technical-standard
kb-id: standards
info-type: standard-definition
primary-topic: Universal naming conventions for all entities in the knowledge base system
related-standards: []
version: 3.0.0
date-created: '2025-05-29'
date-modified: '2025-01-11'
primary_domain: GM
sub_domain: CONVENTIONS
scope_application: Defines ALL naming conventions for files, directories, identifiers, variables, fields, and other named entities across the entire knowledge base system. This is the SINGLE SOURCE OF TRUTH - all other standards must reference this document rather than defining their own naming rules.
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas:
  - File organization
  - Standard identification
  - System consistency
  - Tool compatibility
  - Code integrity
  - Configuration management
  - Frontmatter schema
  - Variable naming
  - API consistency
---

# Standard: Universal Naming Conventions - Single Source of Truth

## AUTHORITY AND PRECEDENCE

**This document is the SINGLE SOURCE OF TRUTH for ALL naming conventions in the knowledge base system.**

### Rule 0.1: Absolute Authority
- This standard takes precedence over ALL other documents regarding naming
- No other standard may define naming conventions independently
- All references to naming in other standards MUST link to this document
- Any conflicts between this standard and others are resolved in favor of this document

### Rule 0.2: Maintenance Discipline
- ALL naming rules MUST be defined here and ONLY here
- Other standards may reference specific sections but NEVER duplicate rules
- Tool configurations are GENERATED from this document (see Generation Templates section)
- Updates to naming conventions require updating ONLY this document
- **Section 2.2 is auto-generated** from `standards/registry/mt-schema-frontmatter.yaml` via `tools/frontmatter-management/generate_schema_docs.py`

## CORE PRINCIPLE: CONTEXT-AWARE NAMING

**Different contexts require different naming conventions. The system was designed with mixed conventions for compatibility and functionality.**

## 1. CONTEXT-SPECIFIC NAMING RULES

### 1.1 Files and Directories
**Rule**: **kebab-case** (lowercase with hyphens)
- **Pattern**: `^[a-z0-9]+(-[a-z0-9]+)*$`
- **Examples**: `my-document.md`, `project-files/`, `user-guide.md`
- **Rationale**: Filesystem compatibility, URL-friendly, consistent

### 1.2 Python Code Elements
**Variables and Functions**: **snake_case**
- **Pattern**: `^[a-z_][a-z0-9_]*$`
- **Examples**: `standards_index`, `load_config`, `file_path`

**Classes**: **PascalCase**
- **Pattern**: `^[A-Z][a-zA-Z0-9]*$`
- **Examples**: `NamingEnforcer`, `ContentValidator`

**Constants**: **UPPER_SNAKE_CASE**
- **Pattern**: `^[A-Z_][A-Z0-9_]*$`
- **Examples**: `MAX_FILE_SIZE`, `DEFAULT_CONFIG`

**Rationale**: Python PEP 8 compliance, tool compatibility

### 1.3 Frontmatter Fields
**Rule**: **snake_case** (CRITICAL: Tools expect this format)
- **Pattern**: `^[a-z_][a-z0-9_]*$`
- **Examples**: `standard_id`, `primary_domain`, `sub_domain`, `scope_application`
- **Rationale**: YAML convention, existing tool dependencies, schema compatibility

### 1.4 JSON/YAML Configuration Keys
**Rule**: **snake_case**
- **Pattern**: `^[a-z_][a-z0-9_]*$`
- **Examples**: `standards_index`, `naming_exceptions`, `domain_codes`
- **Rationale**: Data structure conventions, parser compatibility

### 1.5 Standard IDs
**Rule**: **DOMAIN-SUBDOMAIN-NAME** (uppercase with hyphens)
- **Pattern**: `^[A-Z]{1,3}-[A-Z]{2,15}-[A-Z0-9\-]+$`
- **Examples**: `GM-CONVENTIONS-NAMING`, `MT-SCHEMA-FRONTMATTER`
- **Rationale**: Established system convention, hierarchical organization

### 1.6 JavaScript/TypeScript Elements
**Variables and Functions**: **camelCase**
- **Pattern**: `^[a-z][a-zA-Z0-9]*$`
- **Examples**: `fileName`, `dateModified`, `validateInput`

**Classes**: **PascalCase**
- **Pattern**: `^[A-Z][a-zA-Z0-9]*$`
- **Examples**: `ContentValidator`, `NamingEnforcer`

**Constants**: **UPPER_SNAKE_CASE**
- **Pattern**: `^[A-Z_][A-Z0-9_]*$`
- **Examples**: `MAX_RETRIES`, `API_BASE_URL`

### 1.7 Tags and Metadata Values
**Rule**: **kebab-case**
- **Pattern**: `^[a-z0-9]+(-[a-z0-9]+)*$`
- **Examples**: `status/active`, `content-type/standard-definition`
- **Rationale**: Consistency, readability, URL compatibility

### 1.8 Key References (Placeholders)
**Rule**: **camelCase**
- **Pattern**: `^[a-z][a-zA-Z0-9]*$`
- **Examples**: `{{key.officialCompanyName}}`, `{{key.projectVersion}}`
- **Rationale**: Readability, established convention

## 2. PROTECTED NAMES (NEVER CHANGE)

These names are hardcoded in tools and systems. Changing them breaks functionality.

### 2.1 Python Variable Dependencies
```
standards_index, config, __init__, self, args, kwargs, 
_load_standards_index, generate_index, kb_linter,
file_path, date_modified, content_validator, naming_enforcer
```

### 2.2 Frontmatter Field Names (CRITICAL)
### 2.2 Frontmatter Field Names (CRITICAL)
```
title, standard_id, aliases, tags, kb-id, info-type, primary-topic,
related-standards, version, date-created, date-modified,
primary_domain, sub_domain, scope_application, criticality,
lifecycle_gatekeeper, impact_areas, change_log_url
```

### 2.3 Configuration File Names
```
standards_index.json, standards_index.schema.json,
naming_exceptions.json, protected_names.json,
collection_definitions.yaml, domain_codes.yaml,
subdomain_registry.yaml
```

### 2.4 Tool Script Names
```
generate_index.py, generate_collections.py, 
kb_linter.py, naming_enforcer.py, corruption_reverser.py,
validate_metadata.py, frontmatter_validator.py
```

### 2.5 JSON/YAML Configuration Keys
```
standards_index, standard_definitions, naming_exceptions,
protected_names, context_rules, domain_codes, subdomain_registry
```

### 2.6 Environment Variables
```
PYTHONPATH, NODE_ENV, API_KEY, DATABASE_URL,
LOG_LEVEL, DEBUG_MODE
```

## 3. VALIDATION RULES

### 3.1 Context-Aware Enforcement
**Files and Directories**: Enforce kebab-case strictly
**Python Code**: Validate syntax, don't modify existing variables
**Frontmatter Fields**: Validate against schema, NEVER change field names
**Protected Names**: NEVER modify under any circumstances

### 3.2 Exception Handling
**Temporary Files**: Skip validation for files matching `*.tmp`, `*.temp`, `*.bak`
**System Directories**: Exclude `.git/`, `node_modules/`, `__pycache__/`
**External Dependencies**: Files required by external tools with specific naming

### 3.3 Validation Hierarchy
1. **Protected Names**: Absolute protection, no exceptions
2. **Context Rules**: Apply appropriate convention for context
3. **Exception Patterns**: Skip validation for excluded patterns
4. **Default Rule**: Apply kebab-case as fallback

## 4. TOOL CONFIGURATION GENERATION

### 4.1 Protected Names JSON Generation
```json
{
  "protected_names": {
    "python_variables": [
      "standards_index", "config", "__init__", "self", "args", "kwargs",
      "_load_standards_index", "generate_index", "kb_linter",
      "file_path", "date_modified", "content_validator", "naming_enforcer"
    ],
    "frontmatter_fields": [
      "standard_id", "primary_domain", "sub_domain", "scope_application",
      "lifecycle_gatekeeper", "impact_areas", "change_log_url",
      "info-type", "criticality", "date-created", "date-modified",
      "title", "version", "tags", "aliases", "related-standards",
      "kb-id", "primary-topic"
    ],
    "json_keys": [
      "standards_index", "standard_definitions", "naming_exceptions",
      "protected_names", "context_rules", "domain_codes", "subdomain_registry"
    ],
    "file_patterns": [
      "standards_index.json", "standards_index.schema.json",
      "naming_exceptions.json", "protected_names.json",
      "collection_definitions.yaml", "domain_codes.yaml"
    ],
    "tool_dependencies": [
      "generate_index.py", "generate_collections.py", 
      "kb_linter.py", "naming_enforcer.py", "corruption_reverser.py"
    ]
  },
  "context_rules": {
    "python_files": {
      "variables": "snake_case",
      "functions": "snake_case", 
      "classes": "PascalCase",
      "constants": "UPPER_SNAKE_CASE"
    },
    "markdown_files": {
      "filenames": "kebab-case",
      "frontmatter_fields": "snake_case"
    },
    "javascript_files": {
      "variables": "camelCase",
      "functions": "camelCase",
      "classes": "PascalCase", 
      "constants": "UPPER_SNAKE_CASE"
    },
    "json_yaml_files": {
      "keys": "snake_case",
      "filenames": "snake_case"
    },
    "directories": {
      "names": "kebab-case"
    }
  }
}
```

### 4.2 Naming Exceptions JSON Generation
```json
{
  "directories": [
    "node_modules", ".git", "__pycache__", ".vscode",
    "dist", "build", "target", "bin", "obj"
  ],
  "files": [
    "LICENSE", "README.md", "CHANGELOG.md", "Makefile",
    "Dockerfile", ".gitignore", ".eslintrc.js"
  ],
  "patterns": [
    "*.min.js", "*.bundle.*", "*.tmp", "*.temp", "*.bak",
    "*.log", "*.pid", ".*"
  ],
  "protected_extensions": [
    ".py", ".js", ".ts", ".json", ".yaml", ".yml"
  ],
  "system_files": true,
  "external_dependencies": true
}
```

## 5. STANDARD AUTHORITY AND REFERENCES

### 5.1 Standards That Must Reference This Document
- **SF-SYNTAX-YAML-FRONTMATTER**: Must reference Section 1.3 for field naming
- **MT-SCHEMA-FRONTMATTER**: Must reference Section 2.2 for field definitions
- **UA-KEYDEFS-GLOBAL**: Must reference Section 1.8 for key naming
- **SF-SYNTAX-KEYREF**: Must reference Section 1.8 for placeholder conventions
- **ALL OTHER STANDARDS**: Must reference this document for any naming requirements

### 5.2 Reference Template for Other Standards
```markdown
### Naming Conventions
All naming in this standard follows the context-aware rules defined in 
[[GM-CONVENTIONS-NAMING]]. Specifically:
- [Context]: See [[GM-CONVENTIONS-NAMING#Section-X.X]]
- Protected names: See [[GM-CONVENTIONS-NAMING#Section-2]]
```

## 6. MIGRATION AND MAINTENANCE

### 6.1 Updating Naming Conventions
1. **Update ONLY this document** (GM-CONVENTIONS-NAMING.md)
2. **Regenerate tool configurations** using generation templates
3. **Update references** in other standards if section numbers change
4. **Validate system integrity** before committing changes

### 6.2 Adding New Protected Names
1. **Identify system dependency** (document WHY it cannot be changed)
2. **Add to appropriate section** in Section 2 with explanation
3. **Update generation templates** in Section 4
4. **Regenerate configuration files**

### 6.3 Conflict Resolution Process
1. **This document wins** - always
2. **Update conflicting standard** to reference this document
3. **Remove duplicate naming rules** from other standards
4. **Document resolution** in change log

## 7. EXAMPLES

### 7.1 Correct Naming by Context

**Files/Directories:**
```
my-document.md ✓
project-files/ ✓  
user-guide.md ✓
api-reference.md ✓
```

**Python Code:**
```python
standards_index = load_config()  ✓
class ContentValidator:  ✓
MAX_FILE_SIZE = 1024  ✓
```

**Frontmatter:**
```yaml
standard_id: GM-CONVENTIONS-NAMING  ✓
primary_domain: GM  ✓
sub_domain: CONVENTIONS  ✓
```

**JavaScript:**
```javascript
const fileName = getFileName();  ✓
class DocumentProcessor {}  ✓
const API_BASE_URL = "...";  ✓
```

### 7.2 Incorrect Naming (Context Violations)

**Files:**
```
MyDocument.md ✗ (should be my-document.md)
project_files/ ✗ (should be project-files/)
```

**Frontmatter:**
```yaml
standard-id: GM-CONVENTIONS-NAMING ✗ (should be standard_id)
primary-domain: GM ✗ (should be primary_domain)
```

**Python:**
```python
standards-index = load_config() ✗ (should be standards_index)
standardsIndex = loadConfig() ✗ (should be standards_index)
```

## 8. TOOL IMPLEMENTATION REQUIREMENTS

### 8.1 Naming Enforcer Requirements
- **Context Detection**: Identify file type and apply appropriate rules
- **Protected Name Validation**: Never modify protected names
- **Exception Handling**: Skip validation for excluded patterns
- **Configuration Driven**: Use generated JSON configurations

### 8.2 Linter Integration
- **Validate Against This Standard**: Check all naming against these rules
- **Report Context Violations**: Identify incorrect naming for context
- **Protected Name Alerts**: Flag any changes to protected names
- **Reference Validation**: Ensure other standards reference this document

## 9. EMERGENCY PROCEDURES

### 9.1 If System Breaks Due to Naming Changes
1. **STOP**: Immediately halt any naming enforcement
2. **Assess**: Identify what names were changed
3. **Reverse**: Use corruption_reverser.py or manual rollback
4. **Investigate**: Determine if names should be protected
5. **Update**: Add to protected names list if necessary

### 9.2 If Naming Conflicts Are Discovered
1. **Document Conflict**: Record exactly what conflicts and where
2. **Determine Authority**: This document wins, always
3. **Update Conflicting Standard**: Remove duplicate rules, add reference
4. **Validate System**: Ensure no functional dependencies broken

---

**This standard eliminates all naming contradictions by establishing absolute authority and context-aware rules that reflect actual system requirements. All other standards must reference this document rather than defining their own naming conventions.**
```
