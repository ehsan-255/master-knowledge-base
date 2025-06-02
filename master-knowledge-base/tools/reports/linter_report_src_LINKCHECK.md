# Linter Report


## File: `master-knowledge-base/standards/src/bad_filename_id_mismatch.md`
### Warnings:
  - [L11] Key order issue: Key 'tags' (defined order index 3) is before key 'criticality' (defined order index 14), violating defined relative order.
  - [L13] Key order issue: Key 'primary-topic' (defined order index 6) is before key 'change_log_url' (defined order index 17), violating defined relative order.
  - [L14] Key order issue: Key 'kb-id' (defined order index 4) is before key 'primary-topic' (defined order index 6), violating defined relative order.
  - [L3] Filename 'bad_filename_id_mismatch.md' should match 'standard_id' 'XX-CORRECT-ID-001'.
### Errors:
  - [L10] 'criticality' ('p3-low') not in defined list. Valid (mixed-case from YAML): ['P0-Critical', 'P1-High', 'P2-Medium', 'P3-Low']
  - [L12] Relative 'change_log_url' non-existent: ./XX-CORRECT-ID-001-CHANGELOG.MD (resolved: /app/master-knowledge-base/standards/src/XX-CORRECT-ID-001-CHANGELOG.MD)

## File: `master-knowledge-base/standards/src/GUIDE-FEATURE-ADVANCED-SETTINGS.md`
### Warnings:
  - [L17] 'lifecycle_gatekeeper' ('TBD') not in defined list. Valid: ['Architect-Review', 'Security-Team-Approval', 'Editorial-Board-Approval', 'Stakeholder-Review', 'SME-Consensus', 'No-Gatekeeper', 'Governance-Board-Approval']
### Errors:
  - [L3] 'standard_id' ('GUIDE-FEATURE-ADVANCED-SETTINGS') fails regex: '^[A-Z]{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*$'.
  - [L14] 'sub_domain' ('GUIDE') not valid for domain 'UA'. Valid: ['ACCESSIBILITY', 'KEYDEFS', 'SCHEMAS']
  - [L19] Relative 'change_log_url' non-existent: ./GUIDE-FEATURE-ADVANCED-SETTINGS-CHANGELOG.MD (resolved: /app/master-knowledge-base/standards/src/GUIDE-FEATURE-ADVANCED-SETTINGS-CHANGELOG.MD)

## File: `master-knowledge-base/standards/src/CONCEPT-CORE-RESEARCH-METHODOLOGY.md`
### Warnings:
  - [L14] Primary domain 'TBD' not found in subdomain registry structure for sub_domain check.
  - [L17] 'lifecycle_gatekeeper' ('TBD') not in defined list. Valid: ['Architect-Review', 'Security-Team-Approval', 'Editorial-Board-Approval', 'Stakeholder-Review', 'SME-Consensus', 'No-Gatekeeper', 'Governance-Board-Approval']
### Errors:
  - [L3] 'standard_id' ('CONCEPT-CORE-RESEARCH-METHODOLOGY') fails regex: '^[A-Z]{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*$'.
  - [L13] 'primary_domain' ('TBD') not in defined domain_codes. Valid: ['AS', 'CS', 'MT', 'SF', 'OM', 'GM', 'UA', 'QM']
  - [L7] 'info-type' ('concept-definition') not in defined list. Valid: ['standard-definition', 'policy-document', 'guide-document', 'glossary-document', 'template-document', 'registry-document', 'schema-document', 'navigation-document', 'chapter-document', 'key-definition-set', 'kb-definition-map', 'how-to-guide', 'tutorial-document', 'troubleshooting-guide', 'reference-document', 'architecture-overview', 'design-specification', 'meeting-notes', 'report-document', 'process-definition', 'role-definition', 'service-definition', 'api-specification', 'data-model-definition', 'security-standard', 'compliance-guideline', 'collection-document', 'mandate-document', 'changelog']
  - [L19] Relative 'change_log_url' non-existent: ./CONCEPT-CORE-RESEARCH-METHODOLOGY-CHANGELOG.MD (resolved: /app/master-knowledge-base/standards/src/CONCEPT-CORE-RESEARCH-METHODOLOGY-CHANGELOG.MD)

## File: `master-knowledge-base/standards/src/CONCEPT-P-VALUE.md`
### Warnings:
  - [L14] Primary domain 'TBD' not found in subdomain registry structure for sub_domain check.
  - [L17] 'lifecycle_gatekeeper' ('TBD') not in defined list. Valid: ['Architect-Review', 'Security-Team-Approval', 'Editorial-Board-Approval', 'Stakeholder-Review', 'SME-Consensus', 'No-Gatekeeper', 'Governance-Board-Approval']
### Errors:
  - [L3] 'standard_id' ('CONCEPT-P-VALUE') fails regex: '^[A-Z]{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*$'.
  - [L13] 'primary_domain' ('TBD') not in defined domain_codes. Valid: ['AS', 'CS', 'MT', 'SF', 'OM', 'GM', 'UA', 'QM']
  - [L7] 'info-type' ('concept-definition') not in defined list. Valid: ['standard-definition', 'policy-document', 'guide-document', 'glossary-document', 'template-document', 'registry-document', 'schema-document', 'navigation-document', 'chapter-document', 'key-definition-set', 'kb-definition-map', 'how-to-guide', 'tutorial-document', 'troubleshooting-guide', 'reference-document', 'architecture-overview', 'design-specification', 'meeting-notes', 'report-document', 'process-definition', 'role-definition', 'service-definition', 'api-specification', 'data-model-definition', 'security-standard', 'compliance-guideline', 'collection-document', 'mandate-document', 'changelog']
  - [L19] Relative 'change_log_url' non-existent: ./CONCEPT-P-VALUE-CHANGELOG.MD (resolved: /app/master-knowledge-base/standards/src/CONCEPT-P-VALUE-CHANGELOG.MD)

## File: `master-knowledge-base/standards/src/OM-AUTOMATION-LLM-IO-SCHEMAS.md`
### Warnings:
  - [L147] Potentially broken link: Standard ID '[[OM-AUTOMATION-LLM-PROMPT-LIBRARY]]' not found in standards_index.json.

## File: `master-knowledge-base/standards/src/CONCEPT-HYPOTHESIS-TESTING.md`
### Warnings:
  - [L14] Primary domain 'TBD' not found in subdomain registry structure for sub_domain check.
  - [L17] 'lifecycle_gatekeeper' ('TBD') not in defined list. Valid: ['Architect-Review', 'Security-Team-Approval', 'Editorial-Board-Approval', 'Stakeholder-Review', 'SME-Consensus', 'No-Gatekeeper', 'Governance-Board-Approval']
### Errors:
  - [L3] 'standard_id' ('CONCEPT-HYPOTHESIS-TESTING') fails regex: '^[A-Z]{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*$'.
  - [L13] 'primary_domain' ('TBD') not in defined domain_codes. Valid: ['AS', 'CS', 'MT', 'SF', 'OM', 'GM', 'UA', 'QM']
  - [L7] 'info-type' ('concept-definition') not in defined list. Valid: ['standard-definition', 'policy-document', 'guide-document', 'glossary-document', 'template-document', 'registry-document', 'schema-document', 'navigation-document', 'chapter-document', 'key-definition-set', 'kb-definition-map', 'how-to-guide', 'tutorial-document', 'troubleshooting-guide', 'reference-document', 'architecture-overview', 'design-specification', 'meeting-notes', 'report-document', 'process-definition', 'role-definition', 'service-definition', 'api-specification', 'data-model-definition', 'security-standard', 'compliance-guideline', 'collection-document', 'mandate-document', 'changelog']
  - [L19] Relative 'change_log_url' non-existent: ./CONCEPT-HYPOTHESIS-TESTING-CHANGELOG.MD (resolved: /app/master-knowledge-base/standards/src/CONCEPT-HYPOTHESIS-TESTING-CHANGELOG.MD)

---
## Linting Summary
- Total files processed: 80
- Total errors found: 17
- Total warnings found: 12
