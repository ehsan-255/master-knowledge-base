# Linter Report


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

---
## Linting Summary
- Total files processed: 5
- Total errors found: 19
- Total warnings found: 7
