---
title: "Standard: Metadata Validation Procedures"
standard_id: "QM-VALIDATION-METADATA"
aliases: ["Frontmatter Validation Rules", "Metadata Quality Assurance"]
tags: ["status/draft", "criticality/P1-High", "content-type/standard-definition", "topic/metadata", "topic/validation", "topic/quality-assurance", "kb-id/standards"]
kb-id: "standards"
info-type: "standard-definition"
primary-topic: "Defines the procedures and rules for validating document metadata (YAML frontmatter) against the official schema to ensure accuracy, consistency, and completeness."
related-standards: ["MT-SCHEMA-FRONTMATTER", "MT-REGISTRY-TAG-GLOSSARY", "[[domain_codes.yaml]]", "[[subdomain_registry.yaml]]"]
version: '0.1.0'
date-created: "2025-05-29T15:49:24Z"
date-modified: "2025-05-30T14:00:00Z"
primary_domain: "QM"
sub_domain: "VALIDATION"
scope_application: "Applies to the YAML frontmatter of all Markdown documents across all knowledge bases."
criticality: "P1-High"
lifecycle_gatekeeper: "Architect-Review"
impact_areas: ["Metadata integrity", "Data quality", "Content validation", "Authoring consistency", "Automated processing", "Interoperability", "Search accuracy"]
change_log_url: "./QM-VALIDATION-METADATA-changelog.md"
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
- `[[MT-REGISTRY-TAG-GLOSSARY]]`: For tags, `kb-id` values, `criticality` values, and `lifecycle_gatekeeper` values.
- `[[domain_codes.yaml]]`: For `primary_domain` values.
- `[[subdomain_registry.yaml]]`: For `sub_domain` values.

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
- **`tags`:** Must be kebab-case. Must include required categories (e.g., `status/*`, `content-type/*`, `topic/*`). All tags must be from or align with `[[MT-REGISTRY-TAG-GLOSSARY]]`.
- **`kb-id`:** Must be a kebab-case string from the controlled vocabulary in `[[MT-REGISTRY-TAG-GLOSSARY]]`.
- **`info-type`:** Must be a kebab-case string from the explicit list provided in `[[MT-SCHEMA-FRONTMATTER]]`.
- **`criticality` (field):** Must be a string from the controlled vocabulary defined for `criticality/*` tags in `[[MT-REGISTRY-TAG-GLOSSARY]]`.
- **`lifecycle_gatekeeper` (field):** Must be a string from the controlled vocabulary defined for `lifecycle_gatekeeper/*` tags in `[[MT-REGISTRY-TAG-GLOSSARY]]`.
- **`primary_domain`:** Must be a 2-letter uppercase string present in `[[domain_codes.yaml]]`.
- **`sub_domain`:** Must be a 2-6 letter uppercase string present in `[[subdomain_registry.yaml]]` for the given `primary_domain`.

### 6.4. Specific Key Constraints
- **`title`:** String, not empty.
- **`standard_id`:** (If applicable) String, MUST follow regex `^[A-Z]{2}-[A-Z]{2,6}-[A-Z0-9\-]+$`. Filename (sans `.md`) SHOULD equal `standard_id`.
- **`version`:** String, semantic versioning preferred.
- **`date-created` / `date-modified`:** String, ISO-8601 format `YYYY-MM-DDTHH:MM:SSZ`.
- **`primary-topic`:** String, not empty.
- **`related-standards`:** List of Strings, each must be a valid `standard_id` or internal link `[[STANDARD_ID]]`.
- **`change_log_url`:** String. If relative path, MUST start `./`. Existence of local file SHOULD be checked.

### 6.5. File Hygiene for Frontmatter
- Frontmatter must be valid YAML.
- Adherence to `[[SF-SYNTAX-YAML-FRONTMATTER]]` regarding delimiters (`---`).
- Adherence to `[[SF-FORMATTING-FILE-HYGIENE]]` (UTF-8 encoding, LF line endings).

## 7. Tooling for Validation

- **Linters:** Tools like `yamllint` (for basic YAML syntax) and custom schema validators (e.g., Python scripts using `pykwalify` or `jsonschema` adapted for YAML) should be employed.
- **Editor Integrations:** Plugins for editors like VS Code can provide real-time feedback.
- **Pre-commit Hooks:** Git hooks can run validation scripts before commits are finalized.

## 8. Reporting and Remediation

- Validation errors MUST be reported clearly, indicating the file, the problematic key(s), and the nature of the error.
- Authors or designated content maintainers are responsible for correcting validation errors promptly.
- Automated reports on metadata quality SHOULD be generated periodically.

## 9. Scope of Application
This standard applies to all individuals involved in creating, reviewing, or managing content within the knowledge base ecosystem, as well as developers creating tooling for the KB.
