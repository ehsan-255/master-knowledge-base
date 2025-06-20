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
- content-type/standard-definition
- content-type/technical-standard
- criticality/p0-critical
- kb-id/standards
- status/active
- topic/conventions
- topic/gm
kb-id: standards
info-type: standard-definition
primary-topic: Universal naming conventions for all entities in the knowledge base
  system
related-standards: []
version: 3.0.0
date-created: '2025-05-29'
date-modified: '2025-06-17T02:29:15Z'
primary_domain: GM
sub_domain: CONVENTIONS
scope_application: Defines ALL naming conventions for files, directories, identifiers,
  variables, fields, and other named entities across the entire knowledge base system.
  This is the SINGLE SOURCE OF TRUTH - all other standards must reference this document
  rather than defining their own naming rules.
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
- Tool configurations are GENERATED from this document
- Updates to naming conventions require updating ONLY this document

## 1. CONTEXT-SPECIFIC NAMING RULES

### 1.1 Files and Directories: **kebab-case**
- **Pattern**: `^[a-z0-9]+(-[a-z0-9]+)*$`
- **Examples**: `my-document.md`, `project-files/`, `user-guide.md`

### 1.2 Python Code Elements
- **Variables/Functions**: `snake_case` - `^[a-z_][a-z0-9_]*$`
- **Classes**: `PascalCase` - `^[A-Z][a-zA-Z0-9]*$`
- **Constants**: `UPPER_SNAKE_CASE` - `^[A-Z_][A-Z0-9_]*$`

### 1.3 Frontmatter Fields: **snake_case** (CRITICAL: Tools expect this format)
- **Pattern**: `^[a-z_][a-z0-9_]*$`
- **Examples**: `standard_id`, `primary_domain`, `sub_domain`, `scope_application`

### 1.4 JSON/YAML Configuration Keys: **snake_case**
- **Pattern**: `^[a-z_][a-z0-9_]*$`
- **Examples**: `standards_index`, `naming_exceptions`, `domain_codes`

### 1.5 Standard IDs: **DOMAIN-SUBDOMAIN-NAME**
- **Pattern**: `^[A-Z]{1,3}-[A-Z]{2,15}-[A-Z0-9\-]+$`
- **Examples**: `GM-CONVENTIONS-NAMING`, `MT-SCHEMA-FRONTMATTER`

### 1.6 JavaScript/TypeScript Elements
- **Variables/Functions**: `camelCase` - `^[a-z][a-zA-Z0-9]*$`
- **Classes**: `PascalCase` - `^[A-Z][a-zA-Z0-9]*$`
- **Constants**: `UPPER_SNAKE_CASE` - `^[A-Z_][A-Z0-9_]*$`

### 1.7 Tags and Metadata Values: **kebab-case**
- **Pattern**: `^[a-z0-9]+(-[a-z0-9]+)*$`
- **Examples**: `status/active`, `content-type/standard-definition`

### 1.8 Key References (Placeholders): **camelCase**
- **Pattern**: `^[a-z][a-zA-Z0-9]*$`
- **Examples**: `{{key.officialCompanyName}}`, `{{key.projectVersion}}`

## 2. PROTECTED NAMES (NEVER CHANGE)

These names are hardcoded in tools and systems. Changing them breaks functionality.

### 2.1 Python Variable Dependencies
```
standards_index, config, __init__, self, args, kwargs, 
_load_standards_index, generate_index, kb_linter,
file_path, date_modified, content_validator, naming_enforcer
```

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
collection_definitions.yaml, schema-registry.jsonld,
master-index.jsonld, shacl-shapes.ttl
```

### 2.4 Tool Script Names
```
generate_index.py, generate_collections.py, 
kb_linter.py, naming_enforcer.py, corruption_reverser.py,
validate_metadata.py, frontmatter_validator.py
```

## 3. VALIDATION RULES

### 3.1 Context-Aware Enforcement
- **Files and Directories**: Enforce kebab-case strictly
- **Python Code**: Validate syntax, don't modify existing variables
- **Frontmatter Fields**: Validate against schema, NEVER change field names
- **Protected Names**: NEVER modify under any circumstances

### 3.2 Exception Handling
- **Temporary Files**: Skip validation for files matching `*.tmp`, `*.temp`, `*.bak`
- **System Directories**: Exclude `.git/`, `node_modules/`, `__pycache__/`
- **External Dependencies**: Files required by external tools with specific naming

### 3.3 Validation Hierarchy
1. **Protected Names**: Absolute protection, no exceptions
2. **Context Rules**: Apply appropriate convention for context
3. **Exception Patterns**: Skip validation for excluded patterns
4. **Default Rule**: Apply kebab-case as fallback

## 4. STANDARD AUTHORITY AND REFERENCES

### 4.1 Standards That Must Reference This Document
- **SF-SYNTAX-YAML-FRONTMATTER**: Must reference Section 1.3 for field naming
- **MT-SCHEMA-FRONTMATTER**: Must reference Section 2.2 for field definitions
- **UA-KEYDEFS-GLOBAL**: Must reference Section 1.8 for key naming
- **SF-SYNTAX-KEYREF**: Must reference Section 1.8 for placeholder conventions
- **ALL OTHER STANDARDS**: Must reference this document for any naming requirements

### 4.2 Reference Template for Other Standards
```markdown
### Naming Conventions
All naming in this standard follows the context-aware rules defined in 
[[GM-CONVENTIONS-NAMING]]. Specifically:
- [Context]: See [[GM-CONVENTIONS-NAMING#Section-X.X]]
- Protected names: See [[GM-CONVENTIONS-NAMING#Section-2]]
```

---

**This standard eliminates all naming contradictions by establishing absolute authority and context-aware rules that reflect actual system requirements. All other standards must reference this document rather than defining their own naming conventions.**
```
