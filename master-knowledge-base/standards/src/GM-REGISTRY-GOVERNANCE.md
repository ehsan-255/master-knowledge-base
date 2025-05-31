---
title: "Standard: Registry Governance Framework"
standard_id: "GM-REGISTRY-GOVERNANCE"
aliases: ["Registry Management", "Governance Framework"]
tags:
  - status/draft
  - criticality/p1-high
  - content-type/technical-standard
kb-id: "standards"
info-type: "standard-definition"
primary-topic: "Registry Governance Framework"
related-standards: []
version: '1.0.0'
date-created: "2025-05-29T13:24:53Z"
date-modified: "2025-05-30T18:00:00Z"
primary_domain: "GM"
sub_domain: "CONVENTIONS"
scope_application: "Defines the governance framework for managing registries and controlled vocabularies."
criticality: "P1-High"
lifecycle_gatekeeper: "Architect-Review"
impact_areas: ["Registry management", "Vocabulary control", "Standards consistency"]
change_log_url: "./GM-REGISTRY-GOVERNANCE-changelog.md"
---
# Standard: Registry Governance Policy (GM-REGISTRY-GOVERNANCE)

## 1. Policy Statement

This policy defines the normative processes for proposing, creating, modifying, versioning, and deprecating controlled vocabularies and other formal registries used within the knowledge base ecosystem. Effective governance of these registries is essential for maintaining metadata consistency, data integrity, and interoperability.

Registries typically reside in the `/master-knowledge-base/standards/registry/` directory.

## 2. Scope

This policy applies to all documented controlled vocabularies, including but not limited to:
- Tag glossaries (e.g., `[[MT-REGISTRY-TAG-GLOSSARY]]`)
- Domain and sub-domain codes (e.g., `[[domain_codes.yaml]]`, `[[subdomain_registry.yaml]]`)
- Key definition files (e.g., `[[UA-KEYDEFS-GLOBAL]]`)
- Other formally managed lists of terms or identifiers.

## 3. Governance Rules

### 3.1. Change Control and Review
- **Proposal:** All proposed changes to registries (additions, modifications, deprecations) MUST be submitted via a formal change request process (e.g., a pull request in a version control system).
- **Review:** Proposals require a minimum of two reviewers before approval and implementation:
    - At least one **Domain Subject Matter Expert (SME)** relevant to the registry's content.
    - At least one **Standards Architect** or designated governance lead to ensure alignment with overall architecture and policies (see `[[OM-POLICY-STANDARDS-GOVERNANCE]]`).
- **Justification:** All change proposals MUST include a clear justification for the change.

### 3.2. Versioning of Registries
- Registries that are subject to evolution (e.g., tag glossaries, key definition files) SHOULD be versioned.
- **Semantic Versioning (`MAJOR.MINOR.PATCH`)** (as defined in `[[OM-VERSIONING-CHANGELOGS]]`) is the preferred method:
    - **MAJOR** increment for incompatible schema changes to the registry itself or changes that would break existing usage significantly.
    - **MINOR** increment for new entries, non-breaking schema additions, or significant new descriptive information.
    - **PATCH** increment for minor corrections (e.g., typos in descriptions, formatting fixes) that do not alter meaning or add new entries.
- The version of a registry SHOULD be documented within the registry file itself (e.g., in its frontmatter if it's a Markdown file, or via a version key if YAML/JSON).

### 3.3. Deprecation of Registry Entries
- Individual entries within a registry (e.g., a specific tag, a keyref) SHOULD NOT be deleted if they have been in active use.
- Instead, they MUST be marked with a `status: "deprecated"` or equivalent mechanism.
- A `deprecated_reason` or `deprecation_notes` field SHOULD be added, explaining why the term is deprecated and what alternatives (if any) should be used.
- A `deprecated_date` SHOULD also be included.

### 3.4. Release and Publication Workflow (for version-controlled registries)
- **Merge:** Approved changes are merged into the main branch of the version control system.
- **Validation (Automated):** Where applicable (e.g., for YAML or JSON registries), automated validation against a defined schema for that registry type SHOULD be performed by a continuous integration (CI) process upon merge.
- **Tagging (Version Control):** For significant registry versions (e.g., MINOR or MAJOR updates), a version control tag (e.g., `git tag registry/{registry_name}/v{X.Y.Z}`) SHOULD be applied to the repository commit corresponding to the release.

### 3.5. Registry Documentation and Cataloging
- Each managed registry MUST be documented. This documentation should include its purpose, scope, structure, and how it is maintained.
- A central catalog or index of all official registries SHOULD be maintained to ensure discoverability. (e.g., potentially a future `GM-REGISTRY-CATALOG.md` standard). This catalog should provide a brief description of each registry and a link to it.

## 4. Responsibilities
- **Registry Custodians/SMEs:** Responsible for the accuracy, relevance, and clarity of the content within specific registries.
- **Standards Governance Team/Architects:** Responsible for overseeing the registry governance process, ensuring consistency across registries, and managing the technical aspects of registry publication.
- **Users/Contributors:** Responsible for adhering to the defined values from official registries and proposing changes via the established process.
