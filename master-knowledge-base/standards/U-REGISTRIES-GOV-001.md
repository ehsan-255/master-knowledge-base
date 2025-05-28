---
title: 'U-REGISTRIES-GOV-001 – Registry Governance Rules'
aliases: ['Registry Governance']
tags:
  - kb-id/standards # Placeholder
  - content-type/standard-document # Placeholder
  - status/draft # Placeholder
  - topic/governance # Placeholder
kb-id: 'standards' # Placeholder
info-type: 'standard-document' # Placeholder
primary-topic: 'Defines normative process for creating, updating, and versioning controlled vocabularies under /vocab/.'
related-standards: "N/A" # Placeholder
version: '0.1.0-draft'
date-created: '2025-05-27' # Placeholder - use actual date
date-modified: '2025-05-27' # Placeholder - use actual date
---

# U-REGISTRIES-GOV-001 – Registry Governance Rules

## Status

DRAFT — Phase 0 · Step 0.2

## Purpose

Define normative process for creating, updating, and versioning
controlled vocabularies under `/vocab/`.

## Key Rules

1.  **Change Control:** All modifications via PR; require two reviewers
    (one domain SME, one standards architect).
2.  **Versioning:** Semantic Versioning. Increment:
    *   **MAJOR** for incompatible schema changes
    *   **MINOR** for new entries or non‑breaking meta changes
    *   **PATCH** for typo/description fixes.
3.  **Deprecation:** Mark entry with `status: "deprecated"` and add
    `deprecated_reason`.
4.  **Release Workflow:** Merge to main ⇒ CI validates YAML against
    schema ⇒ tag `registry/{registry_id}/v{version}`.
5.  **Documentation:** Each registry must be referenced in
    `/docs/registry-catalog.md` *(to be authored in Phase 0·Step 0.3)* and appear in JSON-LD index. 