# Linter Report


## File: `master-knowledge-base/AS-INDEX-KB-MASTER.md`
### Errors:
  - [L16] 'criticality' ('p0-critical') not in defined list. Valid (mixed-case from YAML): ['P0-Critical', 'P1-High', 'P2-Medium', 'P3-Low']

## File: `master-knowledge-base/standards/README.md`
### Warnings:
  - [L3] Filename 'README.md' should match 'standard_id' 'DOC-STANDARDS-README'.
### Errors:
  - [L3] 'standard_id' ('DOC-STANDARDS-README') fails regex: '^[A-Z]{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*$'.
  - [L21] 'criticality' ('P4-Informational') not in defined list. Valid (mixed-case from YAML): ['P0-Critical', 'P1-High', 'P2-Medium', 'P3-Low']
  - [L26] Relative 'change_log_url' non-existent: ./README-CHANGELOG.MD (resolved: /app/master-knowledge-base/standards/README-CHANGELOG.MD)
  - [L65] Path-based link '[[[[kb-id/standards]]]]'. Must use '[[STANDARD_ID]]' or '[[STANDARD_ID#Anchor|Display Text]]'.

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

## File: `master-knowledge-base/standards/templates/tpl-canonical-frontmatter.md`
### Errors:
  - [L3] 'standard_id' ('tpl-canonical-frontmatter') fails regex: '^[A-Z]{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*$'.
  - [L19] 'criticality' ('p2-medium') not in defined list. Valid (mixed-case from YAML): ['P0-Critical', 'P1-High', 'P2-Medium', 'P3-Low']
  - [L22] Relative 'change_log_url' non-existent: ./tpl-canonical-frontmatter-CHANGELOG.MD (resolved: /app/master-knowledge-base/standards/templates/tpl-canonical-frontmatter-CHANGELOG.MD)

## File: `master-knowledge-base/standards/templates/analysis-report-template.md`
### Warnings:
  - [L8] Filename 'analysis-report-template.md' should match 'standard_id' 'TPL-ANALYSIS-REPORT'.
  - [L19] Primary domain 'TEMPLATES' not found in subdomain registry structure for sub_domain check.
  - [L22] 'lifecycle_gatekeeper' ('N/A') not in defined list. Valid: ['Architect-Review', 'Security-Team-Approval', 'Editorial-Board-Approval', 'Stakeholder-Review', 'SME-Consensus', 'No-Gatekeeper', 'Governance-Board-Approval']
### Errors:
  - [L8] 'standard_id' ('TPL-ANALYSIS-REPORT') fails regex: '^[A-Z]{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*$'.
  - [L18] 'primary_domain' ('TEMPLATES') not in defined domain_codes. Valid: ['AS', 'CS', 'MT', 'SF', 'OM', 'GM', 'UA', 'QM']
  - [L13] 'info-type' ('template') not in defined list. Valid: ['standard-definition', 'policy-document', 'guide-document', 'glossary-document', 'template-document', 'registry-document', 'schema-document', 'navigation-document', 'chapter-document', 'key-definition-set', 'kb-definition-map', 'how-to-guide', 'tutorial-document', 'troubleshooting-guide', 'reference-document', 'architecture-overview', 'design-specification', 'meeting-notes', 'report-document', 'process-definition', 'role-definition', 'service-definition', 'api-specification', 'data-model-definition', 'security-standard', 'compliance-guideline', 'collection-document', 'mandate-document', 'changelog']
  - [L21] 'criticality' ('N/A') not in defined list. Valid (mixed-case from YAML): ['P0-Critical', 'P1-High', 'P2-Medium', 'P3-Low']

## File: `master-knowledge-base/standards/templates/README.md`
### Warnings:
  - [L3] Filename 'README.md' should match 'standard_id' 'DOC-STANDARDS-TEMPLATES-README'.
### Errors:
  - [L3] 'standard_id' ('DOC-STANDARDS-TEMPLATES-README') fails regex: '^[A-Z]{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*$'.
  - [L21] 'criticality' ('P4-Informational') not in defined list. Valid (mixed-case from YAML): ['P0-Critical', 'P1-High', 'P2-Medium', 'P3-Low']
  - [L26] Relative 'change_log_url' non-existent: ./README-CHANGELOG.MD (resolved: /app/master-knowledge-base/standards/templates/README-CHANGELOG.MD)
  - [L56] Path-based link '[[[[MT-SCHEMA-FRONTMATTER.md]]]]'. Must use '[[STANDARD_ID]]' or '[[STANDARD_ID#Anchor|Display Text]]'.
  - [L56] Path-based link '[[[[AS-STRUCTURE-DOC-CHAPTER.md]]]]'. Must use '[[STANDARD_ID]]' or '[[STANDARD_ID#Anchor|Display Text]]'.

## File: `master-knowledge-base/standards/templates/tpl-changelog-document.md`
### Errors:
  - [L3] 'standard_id' ('tpl-changelog-document') fails regex: '^[A-Z]{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*$'.
  - [L22] For 'info-type: changelog', 'change_log_url' must be self-referential ('./tpl-changelog-document.md'). Found: './tpl-changelog-document-CHANGELOG.MD'
  - [L22] Relative 'change_log_url' non-existent: ./tpl-changelog-document-CHANGELOG.MD (resolved: /app/master-knowledge-base/standards/templates/tpl-changelog-document-CHANGELOG.MD)

## File: `master-knowledge-base/standards/templates/roadmap-template.md`
### Warnings:
  - [L8] Filename 'roadmap-template.md' should match 'standard_id' 'TPL-ROADMAP'.
  - [L19] Primary domain 'TEMPLATES' not found in subdomain registry structure for sub_domain check.
  - [L22] 'lifecycle_gatekeeper' ('N/A') not in defined list. Valid: ['Architect-Review', 'Security-Team-Approval', 'Editorial-Board-Approval', 'Stakeholder-Review', 'SME-Consensus', 'No-Gatekeeper', 'Governance-Board-Approval']
### Errors:
  - [L8] 'standard_id' ('TPL-ROADMAP') fails regex: '^[A-Z]{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*$'.
  - [L18] 'primary_domain' ('TEMPLATES') not in defined domain_codes. Valid: ['AS', 'CS', 'MT', 'SF', 'OM', 'GM', 'UA', 'QM']
  - [L13] 'info-type' ('template') not in defined list. Valid: ['standard-definition', 'policy-document', 'guide-document', 'glossary-document', 'template-document', 'registry-document', 'schema-document', 'navigation-document', 'chapter-document', 'key-definition-set', 'kb-definition-map', 'how-to-guide', 'tutorial-document', 'troubleshooting-guide', 'reference-document', 'architecture-overview', 'design-specification', 'meeting-notes', 'report-document', 'process-definition', 'role-definition', 'service-definition', 'api-specification', 'data-model-definition', 'security-standard', 'compliance-guideline', 'collection-document', 'mandate-document', 'changelog']
  - [L21] 'criticality' ('N/A') not in defined list. Valid (mixed-case from YAML): ['P0-Critical', 'P1-High', 'P2-Medium', 'P3-Low']

## File: `master-knowledge-base/tools/README.md`
### Warnings:
  - [L3] Filename 'README.md' should match 'standard_id' 'DOC-TOOLS-README'.
### Errors:
  - [L3] 'standard_id' ('DOC-TOOLS-README') fails regex: '^[A-Z]{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*$'.
  - [L21] 'criticality' ('P4-Informational') not in defined list. Valid (mixed-case from YAML): ['P0-Critical', 'P1-High', 'P2-Medium', 'P3-Low']
  - [L26] Relative 'change_log_url' non-existent: ./README-CHANGELOG.MD (resolved: /app/master-knowledge-base/tools/README-CHANGELOG.MD)

## File: `master-knowledge-base/tools/builder/README.md`
### Warnings:
  - [L3] Filename 'README.md' should match 'standard_id' 'DOC-TOOLS-BUILDER-README'.
### Errors:
  - [L3] 'standard_id' ('DOC-TOOLS-BUILDER-README') fails regex: '^[A-Z]{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*$'.
  - [L21] 'criticality' ('P4-Informational') not in defined list. Valid (mixed-case from YAML): ['P0-Critical', 'P1-High', 'P2-Medium', 'P3-Low']
  - [L26] Relative 'change_log_url' non-existent: ./README-CHANGELOG.MD (resolved: /app/master-knowledge-base/tools/builder/README-CHANGELOG.MD)

## File: `master-knowledge-base/tools/indexer/standards-index-jsonld-spec.md`
### Warnings:
  - [L3] Filename 'standards-index-jsonld-spec.md' should match 'standard_id' 'DOC-TOOLS-INDEXER-JSONLD-SPEC'.
### Errors:
  - [L3] 'standard_id' ('DOC-TOOLS-INDEXER-JSONLD-SPEC') fails regex: '^[A-Z]{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*$'.
  - [L25] Relative 'change_log_url' non-existent: ./standards-index-jsonld-spec-CHANGELOG.md (resolved: /app/master-knowledge-base/tools/indexer/standards-index-jsonld-spec-CHANGELOG.md)

## File: `master-knowledge-base/tools/indexer/README.md`
### Warnings:
  - [L3] Filename 'README.md' should match 'standard_id' 'DOC-TOOLS-INDEXER-README'.
### Errors:
  - [L3] 'standard_id' ('DOC-TOOLS-INDEXER-README') fails regex: '^[A-Z]{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*$'.
  - [L21] 'criticality' ('P4-Informational') not in defined list. Valid (mixed-case from YAML): ['P0-Critical', 'P1-High', 'P2-Medium', 'P3-Low']
  - [L26] Relative 'change_log_url' non-existent: ./README-CHANGELOG.MD (resolved: /app/master-knowledge-base/tools/indexer/README-CHANGELOG.MD)

## File: `master-knowledge-base/tools/linter/README.md`
### Warnings:
  - [L3] Filename 'README.md' should match 'standard_id' 'DOC-TOOLS-LINTER-README'.
### Errors:
  - [L3] 'standard_id' ('DOC-TOOLS-LINTER-README') fails regex: '^[A-Z]{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*$'.
  - [L21] 'criticality' ('P4-Informational') not in defined list. Valid (mixed-case from YAML): ['P0-Critical', 'P1-High', 'P2-Medium', 'P3-Low']
  - [L26] Relative 'change_log_url' non-existent: ./README-CHANGELOG.MD (resolved: /app/master-knowledge-base/tools/linter/README-CHANGELOG.MD)
  - [L71] Path-based link '[[[[link/path.md]]]]'. Must use '[[STANDARD_ID]]' or '[[STANDARD_ID#Anchor|Display Text]]'.

## File: `master-knowledge-base/tools/reports/linter_report_final.md`
### Errors:
  - [L1] No YAML frontmatter block found.

## File: `master-knowledge-base/tools/reports/linter_report_final_root.md`
### Errors:
  - [L1] No YAML frontmatter block found.

## File: `master-knowledge-base/tools/reports/linter_report_final_registry.md`
### Errors:
  - [L1] No YAML frontmatter block found.

## File: `master-knowledge-base/tools/reports/linter_report_registry_RECHECK.md`
### Errors:
  - [L1] No YAML frontmatter block found.

## File: `master-knowledge-base/tools/reports/linter_report_full_mkb_current.md`
### Errors:
  - [L1] No YAML frontmatter block found.

## File: `master-knowledge-base/tools/reports/linter_report_final_src.md`
### Errors:
  - [L1] No YAML frontmatter block found.

---
## Linting Summary
- Total files processed: 98
- Total errors found: 60
- Total warnings found: 21
