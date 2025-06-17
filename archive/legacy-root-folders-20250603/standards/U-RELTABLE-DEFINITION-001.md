---
title: 'Standard: Relationship Table Definition (U-RELTABLE-DEFINITION-001) - DEPRECATED'
tags:
- content-type/standard-document
- criticality/p0-critical
- kb-id/global
- kb-id/standards
- linking
- semantics
- standards-kb/universal
- status/deprecated
- utility-standards
date-created: '2025-05-19T00:00:00Z'
date-modified: '2025-06-17T02:29:13Z'
version: 0.2.0
info-type: standard-document
primary-topic: Defines the structure for defining non-hierarchical relationships between
  topics
related-standards:
- AS-SCHEMA-RELTABLE-DEFINITION
aliases:
- Reltable Standard
- Semantic Linking Definition
kb-id: archive
scope_application: '[MISSING_SCOPE_APPLICATION]'
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas: []
---
**DEPRECATED:** This document is superseded. Its content has been refactored into the new atomic standard: [[AS-SCHEMA-RELTABLE-DEFINITION]].

> [!WARNING] DEPRECATED: This Standard is No Longer Active
> **Reason for Deprecation:** This standard has been superseded by [[AS-SCHEMA-RELTABLE-DEFINITION]].
> Please refer to the new standard for current guidelines. This document is retained for historical purposes only.

# Standard: Relationship Table Definition (U-RELTABLE-DEFINITION-001)

This document defines the standard structure for "Relationship Tables" (reltables). Reltables are used to explicitly define typed, non-hierarchical relationships between topics within the knowledge base, enhancing semantic understanding and navigation.

## Table of Contents
- [[#Standard: Reltable Structure and Usage (U-RELTABLE-DEFINITION-001)]]
- [[#Defined Relationship Types (Initial Set)]]

## Standard: Reltable Structure and Usage (U-RELTABLE-DEFINITION-001)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `U-RELTABLE-DEFINITION-001`           |
| Standard Name   | Relationship Table Definition         |
| Standard Category | Interlinking & Semantics              |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                               | Example (if illustrative)                                    | Notes / Further Specification (if any)                                       |
| :----- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :--------------------------------------------------------------------------- |
| 1.1    | Relationship tables MUST be defined within the YAML frontmatter of "map" files (e.g., `root.md`, `_overview.md` for a KB Part) or in dedicated `_reltable.md` files. They use a top-level key `reltable:`. | See Illustrative Example.                                    | Centralizes relationship definitions for a given scope.                      |
| 1.2    | The `reltable:` key MUST contain a list of relationship entries. Each entry is an object.                                                       | `reltable:\n  - topic: ...\n  - topic: ...`                  | Each object defines relationships *from* a specific source topic.            |
| 1.3    | Each relationship entry object MUST have a `topic:` key, whose value is the path (from `master-knowledge-base` root) to the source topic file (e.g., `Standards/U-ARCH-001.md`). | `topic: Standards/U-ARCH-001.md`                             | Identifies the "from" side of the relationships.                             |
| 1.4    | Each entry MAY contain one or more relationship type keys (e.g., `prerequisites:`, `relatedConcepts:`, `supportingTasks:`). These keys are defined in this standard (see "Defined Relationship Types"). | `prerequisites:\n  - link: ...`                              | Defines the nature of the link.                                              |
| 1.5    | Each relationship type key (e.g., `prerequisites:`) MUST contain a list of target topic objects.                                                | `relatedConcepts:\n  - link: Concepts/conceptA.md\n    displayText: "Concept A Overview"` | Allows multiple targets for a given relationship type.                       |
| 1.6    | Each target topic object MUST have a `link:` key, whose value is the path (from `master-knowledge-base` root) to the target topic file. It MAY have an optional `displayText:` key for custom link text. | `link: Tasks/taskB.md\ndisplayText: "How to Perform Task B"` | Links MUST use syntax compatible with `O-USAGE-LINKS-001` (without the `[[` `]]`). |
| 1.7    | Relationship types SHOULD be directional (e.g., "A is prerequisite for B" implies B has A as a prerequisite). Processing tools (e.g., DataviewJS) can infer reciprocal links. | N/A                                                          | Simplifies definition; tools handle bidirectionality if needed.              |

## Defined Relationship Types (Initial Set)

| Relationship Type         | Definition                                                                 | Directionality         | Example YAML Structure (within a `reltable` entry)                                                                 |
|--------------------------|----------------------------------------------------------------------------|-----------------------|--------------------------------------------------------------------------------------------------------------------|
| `isPrerequisiteFor`      | Indicates that the source is a required prerequisite for the target.        | Source → Target        | topic: path/to/source-topic.md\n  isPrerequisiteFor:\n    - link: path/to/target-topic.md |
| `isConceptualBasisFor`   | Indicates that the source provides the conceptual foundation for the target.| Source → Target        | topic: path/to/source-concept.md\n  isConceptualBasisFor:\n    - link: path/to/target-methodology.md |
| `isExampleOf`            | Indicates that the source is an example instance of the target concept.     | Source → Target        | topic: path/to/example-instance.md\n  isExampleOf:\n    - link: path/to/general-concept.md |
| `isAlternativeTo`        | Indicates that the source is an alternative to the target (peer relationship).| Bidirectional         | topic: path/to/method-a.md\n  isAlternativeTo:\n    - link: path/to/method-b.md |
| `referencesSpecification`| Indicates that the source references a formal specification or standard.    | Source → Target        | topic: path/to/implementation-guide.md\n  referencesSpecification:\n    - link: path/to/spec-document.md |
| `deepensUnderstandingOf` | Indicates that the source provides additional depth or detail for the target.| Source → Target        | topic: path/to/advanced-topic.md\n  deepensUnderstandingOf:\n    - link: path/to/introductory-topic.md |

This list can be expanded via the governance process (`U-GOVERNANCE-001`).

**Illustrative Examples (Overall):**

YAML snippet within `some-kb/part-1/_overview.md`:
```yaml
reltable:
  - topic: some-kb/part-1/01-main-concept.md
    relatedConcepts:
      - link: some-kb/shared/supporting-concept-x.md
        displayText: "Understanding Concept X"
    supportingTasks:
      - link: some-kb/part-1/tasks/how-to-use-main-concept.md
  - topic: some-kb/part-1/tasks/how-to-use-main-concept.md
    prerequisites:
      - link: some-kb/part-1/01-main-concept.md
    referenceMaterial:
      - link: some-kb/references/main-concept-api.md
```

**Cross-References to Other Standard IDs:** [[COL-ARCH-UNIVERSAL#Standard: KB Root Structure and Top-Level Part Organization (U-ARCH-001)|U-ARCH-001]], [[COL-TOOLING-OBSIDIAN#Standard: Obsidian Internal Linking Conventions (O-USAGE-LINKS-001)|O-USAGE-LINKS-001]], [[M-SYNTAX-YAML-001|M-SYNTAX-YAML-001]]
