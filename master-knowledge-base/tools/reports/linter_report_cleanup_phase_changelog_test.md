# Linter Report


## File: `master-knowledge-base/standards/src/bad_filename_id_mismatch.md`
### Warnings:
  - [L11] Key order issue: Key 'tags' (defined order index 3) is before key 'criticality' (defined order index 14), violating defined relative order.
  - [L13] Key order issue: Key 'kb-id' (defined order index 4) is before key 'primary-topic' (defined order index 6), violating defined relative order.
  - [L3] Filename 'bad_filename_id_mismatch.md' should match 'standard_id' 'XX-CORRECT-ID-001'.
### Errors:
  - [L10] 'criticality' ('p3-low') not in defined list. Valid (mixed-case from YAML): ['P0-Critical', 'P1-High', 'P2-Medium', 'P3-Low']

## File: `master-knowledge-base/standards/src/GM-CONVENTIONS-NAMING.md`
### Warnings:
  - [L288] Potentially broken link: Standard ID '[[GM-CONVENTIONS-NAMING]]' not found in standards_index.json.
  - [L289] Potentially broken link: Standard ID '[[GM-CONVENTIONS-NAMING]]' not found in standards_index.json.
  - [L290] Potentially broken link: Standard ID '[[GM-CONVENTIONS-NAMING]]' not found in standards_index.json.
### Errors:
  - [L19] 'date-created' ('2025-05-29') invalid ISO-8601 (YYYY-MM-DDTHH:MM:SSZ).
  - [L20] 'date-modified' ('2025-01-11') invalid ISO-8601 (YYYY-MM-DDTHH:MM:SSZ).

## File: `master-knowledge-base/standards/src/OM-AUTOMATION-LLM-IO-SCHEMAS.md`
### Warnings:
  - [L145] Potentially broken link: Standard ID '[[OM-AUTOMATION-LLM-PROMPT-LIBRARY]]' not found in standards_index.json.

## File: `master-knowledge-base/standards/src/OM-AUTOMATION-LLM-PROMPT-LIBRARY.md`
### Errors:
  - [L25] 'criticality' ('P4-Informational') not in defined list. Valid (mixed-case from YAML): ['P0-Critical', 'P1-High', 'P2-Medium', 'P3-Low']

## File: `master-knowledge-base/standards/src/XX-LINT-TESTDUMMY1.MD`
### Warnings:
  - [L11] Key order issue: Key 'tags' (defined order index 3) is before key 'criticality' (defined order index 14), violating defined relative order.
  - [L13] Key order issue: Key 'kb-id' (defined order index 4) is before key 'primary-topic' (defined order index 6), violating defined relative order.
  - [L17] Key order issue: Key 'aliases' (defined order index 2) is before key 'impact_areas' (defined order index 16), violating defined relative order.
  - [L1] File extension should be lowercase '.md', not '.MD'. File will be renamed automatically.
### Errors:
  - [L10] 'criticality' ('p1-high') not in defined list. Valid (mixed-case from YAML): ['P0-Critical', 'P1-High', 'P2-Medium', 'P3-Low']
  - [L3] Duplicate 'standard_id' 'XX-LINT-TESTDUMMY1' also found in: master-knowledge-base/standards/src/XX-LINT-TESTDUMMY2.MD

## File: `master-knowledge-base/standards/src/XX-LINT-TESTDUMMY2.MD`
### Warnings:
  - [L8] Key order issue: Key 'tags' (defined order index 3) is before key 'date-modified' (defined order index 10), violating defined relative order.
  - [L10] Key order issue: Key 'kb-id' (defined order index 4) is before key 'primary-topic' (defined order index 6), violating defined relative order.
  - [L3] Filename 'XX-LINT-TESTDUMMY2.md' should match 'standard_id' 'XX-LINT-TESTDUMMY1'.
  - [L16] Potentially broken link: Standard ID '[[XX-LINT-TESTDUMMY1]]' not found in standards_index.json.
  - [L1] File extension should be lowercase '.md', not '.MD'. File will be renamed automatically.
### Errors:
  - [L1] Mandatory key 'primary_domain' missing.
  - [L1] Mandatory key 'sub_domain' missing.
  - [L12] 'criticality' ('p2-medium') not in defined list. Valid (mixed-case from YAML): ['P0-Critical', 'P1-High', 'P2-Medium', 'P3-Low']
  - [L3] Duplicate 'standard_id' 'XX-LINT-TESTDUMMY1' also found in: master-knowledge-base/standards/src/XX-LINT-TESTDUMMY1.MD

---
## Linting Summary
- Total files processed: 79
- Total errors found: 10
- Total warnings found: 16
