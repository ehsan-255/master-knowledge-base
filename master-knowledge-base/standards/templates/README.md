# Standards Templates Directory

This directory (`/master-knowledge-base/standards/templates/`) contains template files designed to assist authors in creating new, standards-conformant documents for the knowledge base ecosystem. Using these templates provides a consistent starting point and helps ensure that all necessary metadata and structural elements are considered from the outset.

## Purpose

The primary purpose of these templates is to:
- Promote consistency across all documented standards and related artifacts.
- Simplify the creation process for new documents.
- Ensure adherence to core structural and metadata standards, particularly `[[MT-SCHEMA-FRONTMATTER]]`.
- Reduce errors and omissions in document setup.

## Available Templates

Currently, the following templates are available:

1.  **`tpl-canonical-frontmatter.md`**:
    *   **Purpose:** Provides the standard YAML frontmatter structure required for all new Markdown documents, especially for standards, policies, and guides. It includes all mandatory keys as defined in `[[MT-SCHEMA-FRONTMATTER]]`, along with placeholders and comments to guide the author.
    *   **When to use:** Use this as the starting point for the frontmatter of any new standard, policy, or detailed guide document.

> [!TODO] Additional templates may be developed, for example:
> - `tpl-standard-definition-document.md`: A full template for a `standard-definition` document, including `tpl-canonical-frontmatter.md` and common H2 sections like "Standard Statement", "Rules", "Examples", etc.
> - `tpl-policy-document.md`: A full template for a `policy-document`, including frontmatter and common H2 sections like "Policy Statement", "Scope", "Rules", "Rationale", etc.
> - `tpl-schema-document.md`: A template for documents defining schemas (like `[[AS-SCHEMA-CONCEPT-DEFINITION]]`), including relevant H2 sections.

## Maintenance

These templates should be regularly reviewed and updated to ensure they remain aligned with the latest versions of core standards, especially `[[MT-SCHEMA-FRONTMATTER.md]]` and any relevant structural standards (e.g., `[[AS-STRUCTURE-DOC-CHAPTER.md]]`). If core standards evolve, these templates MUST be updated accordingly.
