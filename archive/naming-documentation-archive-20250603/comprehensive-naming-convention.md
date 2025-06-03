# DEPRECATED: Comprehensive Naming Convention for Knowledge Base

⚠️ **THIS DOCUMENT IS DEPRECATED** ⚠️

**The authoritative single source of truth for ALL naming conventions is now:**
**`SF-CONVENTIONS-NAMING.md`** in `/master-knowledge-base/standards/src/`

**What changed:**
- All naming rules are now defined in ONE place only
- Configuration files are GENERATED from the authoritative standard  
- No more contradictions between multiple naming sources
- Context-aware rules that prevent system corruption

**For current naming conventions, see:** `[[SF-CONVENTIONS-NAMING]]`

**For tool configurations, use:** `python generate_naming_configs.py`

---

*The content below is preserved for historical reference but should NOT be used.*

## Core Principle: Context-Aware Naming

**Different contexts require different naming conventions.** The system was designed with mixed conventions for good reasons.

## 1. Context-Specific Rules

### 1.1 Files & Directories
- **Rule**: `kebab-case`
- **Examples**: `my-document.md`, `project-files/`, `user-guide.md`
- **Rationale**: Filesystem compatibility, URL-friendly

### 1.2 Python Code
- **Variables/Functions**: `snake_case` (e.g., `standards_index`, `load_config`)
- **Classes**: `PascalCase` (e.g., `NamingEnforcer`, `ContentUpdate`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_FILE_SIZE`)
- **Rationale**: Python PEP 8 compliance

### 1.3 Frontmatter Fields
- **Rule**: `snake_case` (CRITICAL: Tools expect this format)
- **Examples**: `standard_id`, `primary_domain`, `sub_domain`, `scope_application`
- **Rationale**: YAML convention, tool compatibility

### 1.4 JSON/YAML Configuration Keys
- **Rule**: `snake_case`
- **Examples**: `standards_index`, `naming_exceptions`
- **Rationale**: Data structure conventions

### 1.5 Standard IDs
- **Rule**: `DOMAIN-SUBDOMAIN-NAME` (uppercase with hyphens)
- **Examples**: `SF-CONVENTIONS-NAMING`, `MT-SCHEMA-FRONTMATTER`
- **Rationale**: Established system convention

## 2. Protected Names (NEVER CHANGE)

These names are hardcoded in tools and MUST be preserved:

### 2.1 Python Dependencies
```
standards_index, config, __init__, self, args, 
_load_standards_index, generate_index, kb_linter
```

### 2.2 Frontmatter Fields (Tool Dependencies)
```
standard_id, primary_domain, sub_domain, scope_application,
lifecycle_gatekeeper, impact_areas, change_log_url,
info-type, criticality, date-created, date-modified,
title, version, tags, aliases, related-standards
```

### 2.3 Configuration Files
```
standards_index.json, naming_exceptions.json, 
collection_definitions.yaml, domain_codes.yaml
```

### 2.4 Tool Scripts
```
generate_index.py, generate_collections.py, 
kb_linter.py, naming_enforcer.py
```

## 3. Validation Rules

### 3.1 Automated Enforcement
- **Files/Directories**: Check for `kebab-case`
- **Python Code**: Check syntax, don't modify
- **Frontmatter**: Validate against schema, don't change field names
- **Protected Names**: Never modify

### 3.2 Manual Review Required
- Changes to protected names list
- New tool dependencies  
- Cross-system integrations

## 4. Implementation

### 4.1 Updated Naming Enforcer
```python
# Context-aware validation
if context == 'filename':
    enforce_kebab_case()
elif context == 'frontmatter_field':
    validate_against_schema()  # Don't change
elif context == 'python_code':
    skip_enforcement()  # Syntax-aware only
```

### 4.2 Configuration-Driven
- Protected names in `protected-names.json`
- Context rules in `naming_exceptions.json`
- Schema validation from `MT-SCHEMA-FRONTMATTER.md`

## 5. Standard Updates Required

### 5.1 Fix `SF-CONVENTIONS-NAMING.md`
- **CRITICAL**: Change frontmatter section to reflect `snake_case`
- Add context-aware rules
- Reference protected names list

### 5.2 Enhance `MT-SCHEMA-FRONTMATTER.md`  
- Add naming convention reference
- Clarify tool dependencies
- Document field name requirements

### 5.3 New Standard: Tool Dependencies
- Document all hardcoded names
- Define change management process
- Establish impact assessment requirements

## 6. Migration Strategy

### 6.1 Immediate (Critical)
1. Fix `SF-CONVENTIONS-NAMING.md` frontmatter section
2. Update naming enforcer to be context-aware
3. Add protected names validation

### 6.2 Short-term (1-2 weeks)
1. Create comprehensive tool dependency documentation
2. Enhance linter with context awareness
3. Update contributor guidelines

### 6.3 Long-term (1-2 months)
1. Implement change impact analysis
2. Create automated dependency tracking
3. Establish governance for protected names

---

**This convention resolves the contradictions and ensures system stability while maintaining necessary consistency.** 