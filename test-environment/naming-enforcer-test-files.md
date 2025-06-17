---
title: Naming Enforcer Test Files Inventory
standard_id: TEST-NAMING-ENFORCER
date-created: 2025-01-11
info-type: general
version: 0.0.1
date-modified: '2025-06-17T02:29:16Z'
tags:
- content-type/general
- criticality/p0-critical
- kb-id/global
kb-id: test-environment
primary-topic: '[MISSING_PRIMARY_TOPIC]'
scope_application: '[MISSING_SCOPE_APPLICATION]'
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas: []
---
# Naming Enforcer Test File Inventory

## Test Categories

### 1. Extension Case Violations
- uppercase-extension-test.MD (should be .md)
- yaml-case-test.YAML (should be .yaml)
- json-case-test.JSON (should be .json)

### 2. Filename Convention Violations
- CamelCaseFile.md (should be camel-case-file.md)
- snake_case_file.md (should be snake-case-file.md)
- MixedCase_With_Underscores.md (should be mixed-case-with-underscores.md)

### 3. Standard ID Pattern Tests
- VALID-STANDARD-GM-CONVENTIONS-NAMING.md (valid)
- INVALID-G-SHORT-DOMAIN.md (domain too short)
- INVALID-TOOLONG-DOMAIN-NAME.md (domain too long)

### 4. Protected Name Tests
- README.md (should NEVER be changed)
- LICENSE (should NEVER be changed)
- standards_index.json (protected config file)

### 5. Python File Tests
- pythonScript.py (should be python_script.py)
- kebab-case-script.py (should be kebab_case_script.py)

### 6. Link Reference Test Files
- file-with-links.md (contains links to files that will be renamed)
- config-references.json (contains file path references)
- import-test.py (contains import statements)

### 7. Frontmatter Field Tests
- frontmatter-field-violations.md (contains non-snake_case fields)

### 8. Context-Specific Tests
- JSON files with different naming contexts
- JavaScript files with camelCase requirements
- Registry files requiring snake_case
