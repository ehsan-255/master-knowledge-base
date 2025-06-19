---
title: 'DEPRECATED: Master Tag Glossary and Registry - See JSON-LD Registry'
standard_id: MT-REGISTRY-TAG-GLOSSARY
aliases:
- Tag Glossary
- Controlled Vocabulary for Tags
tags:
- content-type/glossary-document
- content-type/registry-document
- criticality/p0-critical
- kb-id/global
- kb-id/standards
- status/deprecated
- topic/metadata
- topic/mt
- topic/registry
- topic/tagging
kb-id: kb-id/standards
info-type: registry-document
primary-topic: '[DEPRECATED] Previously defined official tags. Now migrated to JSON-LD schema registry.'
related-standards:
- OM-PROCESS-SST-UPDATE
- MT-TAGGING-STRATEGY-POLICY
- GM-REGISTRY-GOVERNANCE
version: 1.1.0
date-created: '2025-05-15T00:00:00Z'
date-modified: '2025-06-18T00:52:00Z'
primary_domain: MT
sub_domain: REGISTRY
scope_application: '[DEPRECATED] Tag definitions now maintained in JSON-LD schema registry.'
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Metadata consistency
- Content discoverability
- Automation
- Search accuracy
---

> **⚠️ DEPRECATION NOTICE ⚠️**
>
> **This document has been DEPRECATED as of June 18, 2025.**
>
> **NEW AUTHORITATIVE LOCATION:** All tag definitions, controlled vocabularies, and schema validation rules are now maintained in the **JSON-LD schema registry** system:
>
> - **Primary Registry:** `standards/registry/schema-registry.jsonld`
> - **Master Index:** `standards/registry/master-index.jsonld`
> - **Context Files:** `standards/registry/contexts/*.jsonld`
> - **Validation Shapes:** `standards/registry/shacl-shapes.ttl`
>
> **Update Process:** For changes to tag definitions or controlled vocabularies, follow the process defined in [[OM-PROCESS-SST-UPDATE]].
>
> **Migration Status:** This content has been migrated to the JSON-LD registry system. This document is preserved for historical reference only.

# [DEPRECATED] Master Tag Glossary and Registry (MT-REGISTRY-TAG-GLOSSARY)

**⚠️ This document is DEPRECATED. The authoritative tag definitions are now maintained in the JSON-LD schema registry (`standards/registry/schema-registry.jsonld`).**

For the current tagging strategy, refer to [[MT-TAGGING-STRATEGY-POLICY]]. For registry governance, see [[GM-REGISTRY-GOVERNANCE]]. For updating tag definitions, follow the process in [[OM-PROCESS-SST-UPDATE]].

## [HISTORICAL REFERENCE] Tag Categories 

**⚠️ The content below is preserved for historical reference only. Current tag definitions are maintained in `standards/registry/schema-registry.jsonld`.**

### Status Tags (`status/*`)
- `status/draft`: Content is in initial draft stage, subject to significant change.
- `status/in-review`: Content is under review by subject matter experts or stakeholders.
- `status/approved`: Content has been formally approved and is considered stable.
- `status/published`: Content has been formally published (if applicable to workflow).
- `status/deprecated`: Content is no longer current or recommended for use.
- `status/archived`: Content is preserved for historical reference but is not actively maintained.

### KB Identification Tags (`kb-id/*`)
- `kb-id/standards`: For notes belonging to the Standards KB.
- `kb-id/research-methodology`: For notes belonging to the Research Methodology KB.
- `kb-id/llm-cookbook`: For notes belonging to the LLM Content Generation Cookbook KB.
- `kb-id/global`: For vault-level utility files not specific to one KB.

### Structural Tags
- `kb-master-index`: Applied to `kb-directory.md`.
- `kb-root`: Applied to the `root.md` file of each KB.
- `kb-part-overview`: Applied to `_overview.md` files for Parts within a KB.
- `kb-utility`: Applied to utility documents like this glossary.

### Topic Tags (`topic/*`)
- `topic/metadata`: Documents about metadata standards, structure, or management.
- `topic/governance`: Documents about governance, versioning, or change management.
- `topic/yaml`: Documents about YAML syntax or usage.
- `topic/tagging`: Documents about tagging strategy or tag management.
- `topic/standards-governance`: Documents about standards governance or glossary.
- `topic/architecture`: Documents about KB or file/folder architecture.
- `topic/structure`: Documents about document or section structure.
- `topic/content-guidelines`: Documents about content creation, schemas, or tone.
- `topic/schemas`: Documents about content schemas or templates.
- `topic/markdown`: Documents about Markdown syntax or formatting.
- `topic/syntax`: Documents about syntax rules.
- `topic/obsidian`: Documents about Obsidian-specific usage and conventions.
- `topic/support-docs`: Documents about supporting documentation, onboarding, or guides.
- `topic/llm`: Documents about LLMs, prompt engineering, or automation.
- `topic/content-generation`: Documents about content generation workflows.
- `topic/project-management`: Documents about project management or TODO tracking.
- `topic/research-methodology`: Documents about research methodology KB or standards.
- `topic/glossary`: Documents about glossaries or terminology.
- `topic/utility-standards`: Documents about utility standards or supporting processes.
- `topic/build-process`: Documents about the assembly or build process for the KB.
- `topic/scripting`: Documents outlining scripts or automation logic.
- `topic/linking`: Documents focused on interlinking content.

### Content Type Tags (`content-type/*`)
(Align with `info-type` where sensible, but can be more granular)
- `content-type/technical-standard`: Describes technical rules, specifications.
- `content-type/procedural-guideline`: Outlines steps for a process.
- `content-type/conceptual-explanation`: Explains concepts or principles.
- `content-type/reference-material`: Provides data or information for lookup.
- `content-type/troubleshooting-guide`: Helps resolve issues.
- `content-type/example-code`: Provides code examples.
- `content-type/standard-definition`: For documents that define a standard.
- `content-type/policy-document`: For documents that define a policy.
- `content-type/guide-document`: For documents that provide guidance.
- `content-type/glossary-document`: For documents that define terms (like this one).
- `content-type/template-document`: For documents that serve as templates.
- `content-type/registry-document`: For documents that act as registries.
- `content-type/schema-document`: For documents that define a schema.

### Criticality Tags (`criticality/*`)
(Used for both the `tags` array and as the controlled vocabulary for the `criticality` field)
- `criticality/P0-Critical`: Essential for system operation, core understanding, or carries significant regulatory/compliance implications. Failure to adhere poses immediate and severe risk.
- `criticality/P1-High`: Important for system operation, key processes, or best practices. Failure to adhere poses a high risk of negative impact.
- `criticality/P2-Medium`: Useful for consistency, best practices, or operational efficiency. Failure to adhere may lead to minor issues or inefficiencies.
- `criticality/P3-Low`: Optional or advisory content. Non-adherence is unlikely to cause significant issues.
- `criticality/P4-Informational`: Purely informational content with no direct operational impact.

### Lifecycle Gatekeeper Tags (`lifecycle_gatekeeper/*`)
(Used for both the `tags` array and as the controlled vocabulary for the `lifecycle_gatekeeper` field)
- `lifecycle_gatekeeper/Architect-Review`: Requires review and approval by the architecture review board or designated architects.
- `lifecycle_gatekeeper/Security-Team-Approval`: Requires review and approval by the security team.
- `lifecycle_gatekeeper/Stakeholder-Review`: Requires review and approval by defined business or technical stakeholders.
- `lifecycle_gatekeeper/No-Gatekeeper`: Lifecycle managed by the author or immediate team; no formal external gatekeeper.

### Standards KB Tags (`standards-kb/*`)
- `standards-kb/core`: Core standards and meta-structure documents.
- `standards-kb/universal`: Universal standards applicable to all KBs.
- `standards-kb/kb-specific`: Standards unique to a specific KB.
- `standards-kb/markdown`: Standards related to Markdown syntax and formatting.
- `standards-kb/obsidian`: Standards related to Obsidian-specific usage and conventions.

### Utility & Process Tags
- `utility-standards`: Documents or sections related to utility standards or supporting processes.
- `build-process`: Documents related to the assembly or build process for the KB.
- `scripting`: Documents outlining scripts or automation logic.

### Linking, Metadata, and Content Structure Tags
- `linking`: Standards or documents focused on interlinking content.
- `metadata`: Standards or documents focused on metadata and tagging.
- `governance`: Standards or documents related to governance, versioning, and change management.
- `support-docs`: Supporting documentation, onboarding, and guides.
- `schemas`: Standards or templates for content schemas.
- `syntax-rules`: Rules for Markdown or other syntax.
- `obsidian-usage`: Conventions for using Obsidian features.

### KB-Specific Tags
- `research-methodology`: Used for the Research Methodology KB and related standards.
- `llm-cookbook`: Used for the LLM Content Generation Cookbook KB and related standards.

### Topic Tags (`topic/*`) - Additional from MT-SCHEMA-FRONTMATTER
- `topic/frontmatter`: Documents related to YAML frontmatter.
- `topic/schema`: Documents related to schema definitions.
