---
title: 'Standard: Metadata Validation Procedures'
standard_id: QM-VALIDATION-METADATA
aliases:
- Frontmatter Validation Rules
- Metadata Quality Assurance
tags:
- content-type/standard-definition
- criticality/p1-high
- kb-id/standards
- status/draft
- topic/metadata
- topic/qm
- topic/quality-assurance
- topic/validation
kb-id: standards
info-type: standard-definition
primary-topic: Defines the procedures and rules for validating document metadata (YAML
  frontmatter) against the official schema to ensure accuracy, consistency, and completeness.
related-standards:
- MT-SCHEMA-FRONTMATTER
- OM-PROCESS-SST-UPDATE
version: 0.1.0
date-created: '2025-05-29T15:49:24Z'
date-modified: '2025-06-17T02:29:15Z'
primary_domain: QM
sub_domain: VALIDATION
scope_application: Applies to the YAML frontmatter of all Markdown documents across
  all knowledge bases.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Metadata integrity
- Data quality
- Content validation
- Authoring consistency
- Automated processing
- Interoperability
- Search accuracy
change_log_url: '[MISSING_CHANGE_LOG_URL]'
---
# Standard: Metadata Validation Procedures (QM-VALIDATION-METADATA)

## 1. Standard Statement

This standard defines the rules, procedures, and criteria for validating the YAML frontmatter (metadata) of all Markdown documents within the knowledge base ecosystem. The primary goal is to ensure that all metadata adheres strictly to the official schema defined in `[[MT-SCHEMA-FRONTMATTER]]`, thereby maintaining data quality, consistency, and supporting automated processing.

## 2. Importance of Metadata Validation

Accurate and consistent metadata is fundamental to:
- **Discoverability:** Enabling effective searching, filtering, and navigation.
- **Automation:** Allowing scripts and tools to reliably process, categorize, and manage content.
- **Interoperability:** Ensuring content can be shared and utilized across different systems or platforms.
- **Governance:** Supporting content lifecycle management, auditing, and reporting.
- **Data Integrity:** Maintaining the trustworthiness and reliability of the knowledge base.

## 3. Scope of Validation

This standard applies to the entire YAML frontmatter block of every Markdown document across all knowledge bases within the ecosystem.

## 4. Reference Schema

All metadata validation MUST be performed against the criteria specified in:
- `[[MT-SCHEMA-FRONTMATTER]]`: Defines all allowed keys, their order, data types, mandatory status, and specific validation rules (e.g., regex patterns, controlled vocabularies).

Additional resources for controlled vocabularies include:
- `standards/registry/schema-registry.jsonld`: For tags, `kb-id` values, `criticality` values, and `lifecycle_gatekeeper` values via the JSON-LD registry system.
- `[[MT-SCHEMA-FRONTMATTER]]`: For `primary_domain` and `sub_domain` values in the controlled_vocabularies section.

## 5. Validation Process

Metadata validation should occur at multiple points in the content lifecycle:
- **Authoring Time:** Authors are responsible for ensuring initial compliance. Tooling (e.g., editor plugins, linters) should assist where possible.
- **Pre-commit/Pre-merge:** Automated checks should ideally be integrated into the version control workflow to catch errors before they are merged.
- **Periodic Audits:** Regular automated or manual audits of the knowledge base should be performed to identify and correct any non-compliant metadata.

## 6. Key Validation Points

The following aspects of the frontmatter MUST be validated, as detailed in `[[MT-SCHEMA-FRONTMATTER]]`:

### 6.1. Key Presence and Order
- **All Mandatory Keys Present:** Verify that all keys designated as 'Mandatory' in `[[MT-SCHEMA-FRONTMATTER]]` are present.
- **No Extraneous Keys:** Ensure no keys are present that are not defined in the schema.
- **Correct Key Order:** Confirm that all keys appear in the exact order specified.

### 6.2. Data Types
- Validate that the value for each key conforms to the specified 'Data Type' (e.g., String, List of Strings, Boolean, ISO-8601 Date String).

### 6.3. Controlled Vocabularies
- **`tags`:** Must be kebab-case. Must include required categories (e.g., `status/*`, `content-type/*`, `topic/*`). All tags must be from or align with the controlled vocabulary in the JSON-LD schema registry (`standards/registry/schema-registry.jsonld`).
- **`kb-id`:** Must be a kebab-case string from the controlled vocabulary in the JSON-LD schema registry (`standards/registry/schema-registry.jsonld`).
- **`info-type`:** Must be a kebab-case string from the explicit list provided in `[[MT-SCHEMA-FRONTMATTER]]`.
- **`criticality` (field):** Must be a string from the controlled vocabulary defined for `criticality/*` tags in the JSON-LD schema registry (`standards/registry/schema-registry.jsonld`).
- **`lifecycle_gatekeeper` (field):** Must be a string from the controlled vocabulary defined for `lifecycle_gatekeeper/*` tags in the JSON-LD schema registry (`standards/registry/schema-registry.jsonld`).
- **`primary_domain`:** Must be a 2-letter uppercase string present in `[[MT-SCHEMA-FRONTMATTER]]` controlled_vocabularies.primary_domain.
- **`sub_domain`:** Must be a 2-6 letter uppercase string present in `[[MT-SCHEMA-FRONTMATTER]]` controlled_vocabularies.sub_domain for the given `primary_domain`.

### 6.4. Specific Key Constraints
- **`title`:** String, not empty.
- **`standard_id`:** (If applicable) String, MUST follow regex `^[A-Z]{2}-[A-Z]{2,6}-[A-Z0-9\-]+$`. Filename (sans `.md`) MUST equal `standard_id`.
- **`version`:** String, semantic versioning preferred.
- **`date-created` / `date-modified`:** String, ISO-8601 format `YYYY-MM-DDTHH:MM:SSZ`.
- **`primary-topic`:** String, not empty.
- **`related-standards`:** List of Strings, each must be a valid `standard_id` or internal link `[[STANDARD_ID]]`.
- **`change_log_url`:** String. If relative path, MUST start `./`. Existence of local file MUST be checked.

### 6.5. File Hygiene for Frontmatter
- Frontmatter must be valid YAML.
- Adherence to `[[SF-SYNTAX-YAML-FRONTMATTER]]` regarding delimiters (`---`).
- Adherence to `[[SF-FORMATTING-FILE-HYGIENE]]` (UTF-8 encoding, LF line endings).

## 7. Validation Error Classification

### 7.1. Error Severity Levels

**Critical Errors (BLOCKING)**
- Schema violations: Invalid frontmatter structure or missing mandatory fields
- Naming convention violations: Non-compliant file or standard naming  
- Controlled vocabulary violations: Use of unapproved or deprecated terms
- Cross-reference failures: Broken internal links or invalid standard references

**High Priority Warnings (REVIEW REQUIRED)**
- Content quality issues: Spelling errors, formatting inconsistencies
- Best practice deviations: Suboptimal but not blocking violations
- Performance concerns: Large files or complex structures affecting system performance

**Informational Notices (ADVISORY)**
- Optimization suggestions: Recommendations for improvement
- Style guide reminders: Non-critical formatting suggestions
- Enhancement opportunities: Optional improvements for better quality

### 7.2. Cross-Reference and Link Validation

**Required Cross-Reference Checks:**
- Internal link resolution: All `[[STANDARD_ID]]` references must resolve to valid standards
- File path validation: All relative paths must point to existing files
- Standard ID consistency: Referenced standards must exist in the knowledge base
- Related-standards validation: All entries in `related-standards` arrays must be valid

**Link Checking Requirements:**
- Automated link validation should be performed on all internal references
- Broken links must be reported as Critical Errors
- Link validation must include both explicit links and implicit references

## 8. Automated Remediation Capabilities

### 8.1. Auto-Fix Capabilities
- **Format Correction:** Automatic YAML formatting and structure fixes
- **Tag Standardization:** Automatic conversion to proper controlled vocabulary terms  
- **Date Standardization:** Automatic conversion to required ISO-8601 format
- **Link Updates:** Automatic correction of simple link format issues

### 8.2. Guided Remediation
- **Error Messages:** Clear, actionable error descriptions with fix instructions
- **Documentation Links:** Direct links to relevant standards and guidelines
- **Example Corrections:** Sample fixes for common validation failures
- **Support Escalation:** Clear pathways for complex validation issues

## 9. Tooling for Validation

- **Linters:** Tools like `yamllint` (for basic YAML syntax) and custom schema validators (e.g., Python scripts using `pykwalify` or `jsonschema` adapted for YAML) should be employed.
- **Current Tool Arsenal:** 
  - `tools/linter/kb_linter.py` - Knowledge base content validation
  - `tools/naming-enforcer/naming_enforcer.py` - Naming convention compliance
  - `tools/validation/on_demand_validator.py` - On-demand validation capabilities
  - `tools/validators/graph_validator.py` - Graph and relationship validation
- **Editor Integrations:** Plugins for editors like VS Code can provide real-time feedback.
- **Pre-commit Hooks:** Git hooks can run validation scripts before commits are finalized.

## 10. Reporting and Remediation

- Validation errors MUST be reported clearly, indicating the file, the problematic key(s), and the nature of the error.
- Error reports MUST follow the classification system defined in Section 7.1 (Critical/Warning/Advisory)
- Authors or designated content maintainers are responsible for correcting validation errors promptly.
- Automated reports on metadata quality MUST be generated periodically using tools from our current arsenal.
- Validation reports should be stored in `tools/reports/` following our repository organization standards.

## 11. Integration with Current Tool Arsenal

**Existing Tools That Support This Standard:**
- **`tools/linter/kb_linter.py`:** Primary tool for comprehensive knowledge base validation
- **`tools/naming-enforcer/naming_enforcer.py`:** Enforces naming conventions as defined in [[GM-CONVENTIONS-NAMING]]
- **`tools/validation/on_demand_validator.py`:** Provides on-demand validation capabilities for immediate feedback
- **`tools/validators/graph_validator.py`:** Validates document relationships and cross-references
- **`tools/validators/validate_registry.py`:** Validates JSON-LD registry compliance

**Implementation Requirements:**
- All validation tools MUST implement the error classification system (Section 7.1)
- Tools MUST support automated remediation capabilities where possible (Section 8)
- Validation results MUST be stored in standardized format in `tools/reports/`

## 12. Scope of Application
This standard applies to all individuals involved in creating, reviewing, or managing content within the knowledge base ecosystem, as well as developers creating tooling for the KB. All validation implementations MUST utilize the current tool arsenal and follow the established repository organization patterns.
