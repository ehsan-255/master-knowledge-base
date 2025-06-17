---
title: Untitled Document
info-type: general
version: 0.0.1
date-created: '2025-06-17'
date-modified: '2025-06-17T02:29:15Z'
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
**2. Roadmap Progress**

**Phase 0: Foundations, Definitions & Initial Tooling (Pre-Refactoring)**

*   **Step 0.1: Finalize Naming Conventions & Identifiers**
    *   **Task 0.1.1:** Confirm the atomic file naming convention: `{DOMAIN_CODE}-{SUB_DOMAIN_CODE}-{PRIMARY_TOPIC_KEYWORD}-{OPTIONAL_SECONDARY_TOPICS*}.md`.
        *   **Status:** Defined conceptually. Awaiting `PRIMARY_TOPIC_KEYWORD` finalization to fully lock.
    *   **Task 0.1.2:** Define a strategy for `PRIMARY_TOPIC_KEYWORD` to ensure uniqueness and clear differentiation between "Standard Definition" files and their corresponding "Policy/Guideline" files.
        *   **Status:** **COMPLETED.** Algorithm for deriving `PRIMARY_TOPIC_KEYWORD` finalized and documented in `drafts/proposal-primary-keywords.md` (Revision 2). Full-tree scan completed; no raw collisions detected. Mapping table finalized.
        *   **Deliverables:**
            *   `scripts/derive_primary_keyword.py` (committed, executable)
            *   `drafts/primary-keyword-mapping.csv` (committed, authoritative mapping; no raw collisions)
    *   **Task 0.1.3:** Define and document the regex for `standard_id` syntax (e.g., `^[A-Z]{2}-[A-Z]{2,6}-[A-Z0-9\-]+$`, all-caps, numerals, hyphens; no spaces, no underscores).
        *   **Status:** Defined conceptually. To be formally documented in `U-METADATA-FRONTMATTER-RULES-001.md`.
    *   **Task 0.1.4:** Confirm that filenames (sans `.md`) SHOULD equal the `standard_id` metadata field.
        *   **Status:** Confirmed. To be formally documented in `U-METADATA-FRONTMATTER-RULES-001.md`.

**Next Up:** Phase-0 Task 0.2.x – Controlled Vocabulary Registries begins next session.

### Phase 0 · Step 0.2 – Controlled Vocabulary Registries  
*27 May 2025 – Status: **Specs Finalised (v0.4)***

- Registry schema plus Domain, Maturity, and Audience registries approved.
- Governance document and JSON-LD index spec drafted.
- Python validator script ready; GitHub Actions workflow postponed to Step 0.3.
- Next: submit PR containing files; Execute-LLM to perform repo changes after Ehsan approval.
