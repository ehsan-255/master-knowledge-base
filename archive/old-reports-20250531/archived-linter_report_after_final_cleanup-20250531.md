---
title: Untitled Document
info-type: general
version: 0.0.1
date-created: '2025-06-17'
date-modified: '2025-06-17T02:29:14Z'
tags:
- content-type/general
- criticality/p0-critical
- kb-id/global
kb-id: archive
primary-topic: '[MISSING_PRIMARY_TOPIC]'
scope_application: '[MISSING_SCOPE_APPLICATION]'
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas: []
---
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

---
## Linting Summary
- Total files processed: 76
- Total errors found: 2
- Total warnings found: 4
