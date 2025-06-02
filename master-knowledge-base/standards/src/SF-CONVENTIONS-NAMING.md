---
title: 'Standard: File and ID Naming Conventions'
standard_id: SF-CONVENTIONS-NAMING
aliases:
  - Naming Conventions
  - File Naming
  - ID Conventions
tags:
  - status/active
  - criticality/p1-high
  - content-type/technical-standard
kb-id: standards
info-type: standard-definition
primary-topic: File and ID Naming Conventions
related-standards: []
version: 2.0.0
date-created: '2025-05-29'
date-modified: '2025-01-11'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines the naming conventions for files, standard IDs, and other identifiers in the knowledge base.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
  - File organization
  - Standard identification
  - System consistency
change_log_url: ../changelog.md
---

# Standard: File and ID Naming Conventions

## Core Rule

**Everything is strictly kebab-case unless listed in the exceptions.**

## 1. Primary Naming Convention

### Rule 1.1: Kebab-Case Default
ALL files, directories, identifiers, and other named entities MUST use **kebab-case** formatting:
- All lowercase
- Words separated by single hyphens
- No spaces, underscores, or other separators
- **Examples**: `my-file.md`, `some-directory/`, `standard-id-name`

### Rule 1.2: File Extensions
All file extensions MUST be lowercase:
- **Correct**: `.md`, `.py`, `.js`, `.json`
- **Incorrect**: `.MD`, `.PY`, `.JS`, `.JSON`

## 2. Exceptions List

The following categories are explicitly exempted from kebab-case requirements:

### 2.1 Script Internal Variables
- Python variables: `snake_case` (e.g., `file_path`, `date_modified`)
- JavaScript variables: `camelCase` (e.g., `fileName`, `dateModified`)

### 2.2 Standard IDs 
- Format: `{DOMAIN}-{SUBDOMAIN}-{NAME}` where components use UPPERCASE
- **Examples**: `SF-CONVENTIONS-NAMING`, `OM-AUTOMATION-LLM-PROMPT-LIBRARY`

### 2.3 Frontmatter Field Names
- Use hyphen-separated lowercase: `date-created`, `date-modified`, `standard-id`
- **Never**: `date_created`, `dateCreated`, `Date-Created`

### 2.4 Technical Identifiers
- Git branch names: Follow git conventions
- Environment variables: `UPPER_SNAKE_CASE`
- JSON/YAML keys in configuration: Follow format-specific conventions

### 2.5 External System Requirements
- Files required by external tools that mandate specific naming
- Must be documented in exceptions configuration

## 3. Exception Management

### Rule 3.1: Exception Configuration
Exceptions are managed in `/master-knowledge-base/tools/naming-exceptions.json`:
```json
{
  "directories": ["node_modules", ".git"],
  "files": ["LICENSE", "README.md"],
  "patterns": ["*.min.js", "*.bundle.*"],
  "standard_ids": true,
  "script_variables": true
}
```

### Rule 3.2: Adding New Exceptions
New exceptions require:
1. Clear justification
2. Update to exceptions configuration
3. Documentation in this standard

## 4. Validation

### Rule 4.1: Automated Checking
The linter automatically validates naming conventions:
- Checks all files against kebab-case rule
- Applies exceptions from configuration
- Reports violations for manual review

### Rule 4.2: Manual Override
Critical exceptions not suitable for automation:
- Add `# naming-exception: reason` comment
- Document reason in commit message
- Review during code/content review

## 5. Examples

### Correct Naming
```
my-document.md
project-files/
user-guide.md
api-reference.md
build-scripts/
```

### Incorrect Naming
```
MyDocument.md
project_files/
User_Guide.md
API-Reference.md  (exception: standard IDs only)
buildScripts/
```

---

*This standard replaces the complex multi-rule approach with a simple default + exceptions model for maximum clarity and consistency.*
```
