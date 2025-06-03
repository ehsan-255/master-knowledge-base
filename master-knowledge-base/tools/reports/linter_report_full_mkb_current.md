# Linter Report


## File: `master-knowledge-base/tools/README.md`
### Errors:
  - [L1] No YAML frontmatter block found.

## File: `master-knowledge-base/tools/linter/README.md`
### Errors:
  - [L1] No YAML frontmatter block found.

## File: `master-knowledge-base/tools/builder/README.md`
### Errors:
  - [L1] No YAML frontmatter block found.

## File: `master-knowledge-base/tools/indexer/standards_index-jsonld-spec.md`
### Errors:
  - [L1] Mandatory key 'scope_application' missing.
  - [L1] Mandatory key 'criticality' missing.
  - [L1] Mandatory key 'lifecycle_gatekeeper' missing.
  - [L1] Mandatory key 'impact_areas' missing.
  - [L12] Key 'related-standards' has value 'N/A' of type 'str'. Expected type 'list'.
  - [L14] 'date-created' ('2025-05-27') invalid ISO-8601 (YYYY-MM-DDTHH:MM:SSZ).
  - [L15] 'date-modified' ('2025-05-27') invalid ISO-8601 (YYYY-MM-DDTHH:MM:SSZ).
  - [L10] 'info-type' ('design-document') not in defined list. Valid: ['standard-definition', 'policy-document', 'guide-document', 'glossary-document', 'template-document', 'registry-document', 'schema-document', 'navigation-document', 'chapter-document', 'key-definition-set', 'kb-definition-map', 'how-to-guide', 'tutorial-document', 'troubleshooting-guide', 'reference-document', 'architecture-overview', 'design-specification', 'meeting-notes', 'report-document', 'process-definition', 'role-definition', 'service-definition', 'api-specification', 'data-model-definition', 'security-standard', 'compliance-guideline', 'collection-document', 'mandate-document', 'changelog']

## File: `master-knowledge-base/tools/indexer/README.md`
### Errors:
  - [L1] No YAML frontmatter block found.

## File: `master-knowledge-base/tools/reports/linter_report_final_registry.md`
### Errors:
  - [L1] No YAML frontmatter block found.

## File: `master-knowledge-base/tools/reports/linter_report_final.md`
### Errors:
  - [L1] No YAML frontmatter block found.

## File: `master-knowledge-base/tools/reports/linter_report_final_src.md`
### Errors:
  - [L1] No YAML frontmatter block found.

## File: `master-knowledge-base/tools/reports/linter_report_final_root.md`
### Errors:
  - [L1] No YAML frontmatter block found.

## File: `master-knowledge-base/standards/README.md`
### Errors:
  - [L1] No YAML frontmatter block found.

## File: `master-knowledge-base/standards/templates/tpl-changelog-document.md`
### Warnings:
  - [L3] Filename 'tpl-changelog-document.md' should match 'standard_id' 'XX-TEMPLATECL-CHANGELOG'.
  - [L20] 'lifecycle_gatekeeper' ('[GATEKEEPER_PLACEHOLDER]') not in defined list. Valid: ['Architect-Review', 'Security-Team-Approval', 'Editorial-Board-Approval', 'Stakeholder-Review', 'SME-Consensus', 'No-Gatekeeper', 'Governance-Board-Approval']
  - [L5] Tag 'topic/[TOPIC_PLACEHOLDER]' (at index 2) invalid kebab-case/structure.
### Errors:
  - [L19] 'criticality' ('[CRITICALITY_PLACEHOLDER]') not in defined list. Valid (mixed-case from YAML): ['P0-Critical', 'P1-High', 'P2-Medium', 'P3-Low']
  - [L22] For 'info-type: changelog', 'change_log_url' must be self-referential ('./tpl-changelog-document.md'). Found: './[FILENAME_PLACEHOLDER]'
  - [L22] Relative 'change_log_url' non-existent: ./[FILENAME_PLACEHOLDER] (resolved: /app/master-knowledge-base/standards/templates/[FILENAME_PLACEHOLDER])

## File: `master-knowledge-base/standards/templates/tpl-canonical-frontmatter.md`
### Warnings:
  - [L3] Filename 'tpl-canonical-frontmatter.md' should match 'standard_id' 'XX-TEMPLATESTD-PRIMARYTOPIC'.
  - [L20] 'lifecycle_gatekeeper' ('TBD: Define gatekeeper') not in defined list. Valid: ['Architect-Review', 'Security-Team-Approval', 'Editorial-Board-Approval', 'Stakeholder-Review', 'SME-Consensus', 'No-Gatekeeper', 'Governance-Board-Approval']
  - [L5] Tag 'criticality/P2-Medium' (at index 1) invalid kebab-case/structure.
### Errors:
  - [L14] 'date-created' ('YYYY-MM-DDTHH:MM:SSZ') invalid ISO-8601 (YYYY-MM-DDTHH:MM:SSZ).
  - [L15] 'date-modified' ('YYYY-MM-DDTHH:MM:SSZ') invalid ISO-8601 (YYYY-MM-DDTHH:MM:SSZ).
  - [L5] Tag value for 'criticality/' ('P2-Medium') not in defined list. Valid (lowercase from .txt): ['p0-critical', 'p1-high', 'p2-medium', 'p3-low', 'p4-informational']
  - [L22] Relative 'change_log_url' non-existent: ./changelog.md (resolved: /app/master-knowledge-base/standards/templates/changelog.md)

## File: `master-knowledge-base/standards/templates/README.md`
### Errors:
  - [L1] No YAML frontmatter block found.

## File: `master-knowledge-base/standards/src/OM-AUTOMATION-LLM-IO-SCHEMAS.md`
### Warnings:
  - [L147] Potentially broken link: Standard ID '[[OM-AUTOMATION-LLM-PROMPT-LIBRARY]]' not found in standards_index.json.

---
## Linting Summary
- Total files processed: 90
- Total errors found: 25
- Total warnings found: 7
