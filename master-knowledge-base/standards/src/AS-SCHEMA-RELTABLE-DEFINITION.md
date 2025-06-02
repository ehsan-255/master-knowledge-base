---
title: 'Standard: Relationship Table (Reltable) Definition'
standard_id: AS-SCHEMA-RELTABLE-DEFINITION
aliases:
- Reltable Standard
- Semantic Linking Definition
tags:
- status/draft
- criticality/p2-medium
- content-type/standard-definition
- topic/linking
- topic/semantics
- topic/yaml
- topic/data-structure
- kb-id/standards
kb-id: standards
info-type: standard-definition
primary-topic: Defines the standard structure for 'Relationship Tables' (reltables) used to explicitly define typed, non-hierarchical relationships between topics.
related-standards:
- '[[AS-STRUCTURE-KB-ROOT]]'
- '[[SF-LINKS-INTERNAL-SYNTAX]]'
- '[[SF-SYNTAX-YAML-FRONTMATTER]]'
version: 0.1.2
date-created: '2025-05-19T00:00:00Z'
date-modified: '2025-06-01T23:24:00Z'
primary_domain: AS
sub_domain: STRUCTURE
scope_application: Defines the standard structure for 'Relationship Tables' (reltables) using YAML to define typed, non-hierarchical relationships between topics.
criticality: P2-Medium
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Semantic linking
- Knowledge graph generation
- Content navigability
change_log_url: ./AS-SCHEMA-RELTABLE-DEFINITION-CHANGELOG.MD
---

# Standard: Relationship Table (Reltable) Definition (AS-SCHEMA-RELTABLE-DEFINITION)

> [!TODO] This standard's content has been migrated from `U-RELTABLE-DEFINITION-001`. However, the overall concept of Reltables, their precise implementation details (especially the defined relationship types and their YAML structure), and their integration with other architectural and schema standards require further review and refinement. The relationship types listed are initial suggestions and need validation against broader use cases and semantic consistency.

This document defines the standard structure for "Relationship Tables" (reltables). Reltables are used to explicitly define typed, non-hierarchical relationships between topics within the knowledge base, enhancing semantic understanding and navigation.

## Table of Contents
- [[#Standard: Reltable Structure and Usage (AS-SCHEMA-RELTABLE-DEFINITION)]]
- [[#Defined Relationship Types (Initial Set)]]

## Standard: Reltable Structure and Usage (AS-SCHEMA-RELTABLE-DEFINITION)

| Metadata        | Value                                 |
| :-------------- | :------------------------------------ |
| Standard ID     | `AS-SCHEMA-RELTABLE-DEFINITION`       |
| Standard Name   | Relationship Table Definition         |
| Standard Category | Interlinking & Semantics              |

**Rule/Guideline Statement(s):**

| Rule # | Statement of Rule                                                                                                                               | Example (if illustrative)                                    | Notes / Further Specification (if any)                                       |
| :----- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | :--------------------------------------------------------------------------- |
| 1.1    | Relationship tables MUST be defined within the YAML frontmatter of "map" files (e.g., `root.md`, `_overview.md` for a KB Part) or in dedicated `_reltable.md` files. They use a top-level key `reltable:`. | See Illustrative Example.                                    | Centralizes relationship definitions for a given scope.                      |
| 1.2    | The `reltable:` key MUST contain a list of relationship entries. Each entry is an object.                                                       | `reltable:
  - topic: ...
  - topic: ...`                  | Each object defines relationships *from* a specific source topic.            |
| 1.3    | Each relationship entry object MUST have a `topic:` key, whose value is the path (from `master-knowledge-base` root) to the source topic file (e.g., `master-knowledge-base/standards/src/AS-STRUCTURE-KB-ROOT.md`). | `topic: master-knowledge-base/standards/src/AS-STRUCTURE-KB-ROOT.md`                             | Identifies the "from" side of the relationships. Link should be to new ID format if possible, or remain path based for now. This example uses path. |
| 1.4    | Each entry MAY contain one or more relationship type keys (e.g., `prerequisites:`, `relatedConcepts:`, `supportingTasks:`). These keys are defined in this standard (see "Defined Relationship Types"). | `prerequisites:
  - link: ...`                              | Defines the nature of the link.                                              |
| 1.5    | Each relationship type key (e.g., `prerequisites:`) MUST contain a list of target topic objects.                                                | `relatedConcepts:
  - link: master-knowledge-base/concepts/conceptA.md
    displayText: "Concept A Overview"` | Allows multiple targets for a given relationship type.                       |
| 1.6    | Each target topic object MUST have a `link:` key, whose value is the path (from `master-knowledge-base` root) to the target topic file. It MAY have an optional `displayText:` key for custom link text. | `link: master-knowledge-base/tasks/taskB.md
displayText: "How to Perform Task B"` | Links SHOULD eventually resolve to standard `[[TARGET_ID]]` syntax if the target is a standard. For other content, path-based links may be necessary. This example uses path. |
| 1.7    | Relationship types SHOULD be directional (e.g., "A is prerequisite for B" implies B has A as a prerequisite). Processing tools (e.g., DataviewJS) can infer reciprocal links. | N/A                                                          | Simplifies definition; tools handle bidirectionality if needed.              |

## Defined Relationship Types (Initial Set)

| Relationship Type         | Definition                                                                 | Directionality         | Example YAML Structure (within a `reltable` entry)                                                                 |
|--------------------------|----------------------------------------------------------------------------|-----------------------|--------------------------------------------------------------------------------------------------------------------|
| `isPrerequisiteFor`      | Indicates that the source is a required prerequisite for the target.        | Source → Target        | topic: path/to/source-topic.md
  isPrerequisiteFor:
    - link: path/to/target-topic.md |
| `isConceptualBasisFor`   | Indicates that the source provides the conceptual foundation for the target.| Source → Target        | topic: path/to/source-concept.md
  isConceptualBasisFor:
    - link: path/to/target-methodology.md |
| `isExampleOf`            | Indicates that the source is an example instance of the target concept.     | Source → Target        | topic: path/to/example-instance.md
  isExampleOf:
    - link: path/to/general-concept.md |
| `isAlternativeTo`        | Indicates that the source is an alternative to the target (peer relationship).| Bidirectional         | topic: path/to/method-a.md
  isAlternativeTo:
    - link: path/to/method-b.md |
| `referencesSpecification`| Indicates that the source references a formal specification or standard.    | Source → Target        | topic: path/to/implementation-guide.md
  referencesSpecification:
    - link: path/to/spec-document.md |
| `deepensUnderstandingOf` | Indicates that the source provides additional depth or detail for the target.| Source → Target        | topic: path/to/advanced-topic.md
  deepensUnderstandingOf:
    - link: path/to/introductory-topic.md |

This list can be expanded via the governance process (e.g., reference to a future `[[OM-POLICY-STANDARDS-GOVERNANCE]]` standard).

**Illustrative Examples (Overall):**

YAML snippet within `some-kb/part-1/_overview.md`:
```yaml
reltable:
  - topic: master-knowledge-base/some-kb/part-1/01-main-concept.md # Path based example
    relatedConcepts:
      - link: master-knowledge-base/some-kb/shared/supporting-concept-x.md
        displayText: "Understanding Concept X"
    supportingTasks:
      - link: master-knowledge-base/some-kb/part-1/tasks/how-to-use-main-concept.md
  - topic: master-knowledge-base/some-kb/part-1/tasks/how-to-use-main-concept.md
    prerequisites:
      - link: master-knowledge-base/some-kb/part-1/01-main-concept.md
    referenceMaterial:
      - link: master-knowledge-base/some-kb/references/main-concept-api.md
```

**Cross-References to Other Standard IDs:**
- [[AS-STRUCTURE-KB-ROOT]] (Placeholder for U-ARCH-001)
- [[SF-LINKS-INTERNAL-SYNTAX]] (Placeholder for O-USAGE-LINKS-001)
- [[SF-SYNTAX-YAML-FRONTMATTER]] (Placeholder for M-SYNTAX-YAML-001)
