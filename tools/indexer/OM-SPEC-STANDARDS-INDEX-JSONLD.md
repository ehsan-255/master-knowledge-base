---
title: Standards Index JSON-LD – Spec Sketch
standard_id: OM-SPEC-STANDARDS-INDEX-JSONLD
aliases:
- JSON-LD Index Spec
tags:
- content-type/design-specification
- content-type/specification
- criticality/p2-medium
- kb-id/global
- kb-id/tools
- status/draft
- topic/automation
- topic/indexing
- topic/json-ld
- topic/om
kb-id: tools
info-type: design-specification
primary-topic: Design specification sketch for the standards_index.json in JSON-LD
  format.
related-standards: []
version: 0.1.0
date-created: '2025-05-27T00:00:00Z'
date-modified: '2025-06-17T02:29:16Z'
primary_domain: OM
sub_domain: AUTOMATION
scope_application: Tooling
criticality: P2-Medium
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Automation
- Indexing
change_log_url: ./changelog.md
---
# Standards Index JSON‑LD – Spec Sketch

## Context

```json
{
  "@context": {
    "kb": "https://kb.example.org/vocab#",
    "title": "kb:title",
    "standard_id": "kb:standardId",
    "domain": "kb:primaryDomain",
    "maturity": "kb:maturity",
    "info_type": "kb:infoType",
    "version": "kb:version",
    "date_modified": {
      "@id": "kb:dateModified",
      "@type": "xsd:dateTime"
    },
    "path": "kb:filepath"
  }
}
```

*(Note: The final `@context` will be hosted at a persistent URL, e.g., `https://kb.example.org/context.jsonld`)*

## Minimal Record (now "extended‑minimal")

```json
{
  "@context": "https://kb.example.org/context.jsonld",
  "@id": "kb://standard/U-AS-001",
  "title": "Directory Convention",
  "standard_id": "U-AS-001",
  "domain": "AS",
  "maturity": "FINAL",
  "info_type": "policy",
  "version": "1.0.0",
  "date_modified": "2025-05-26T18:40:00Z",
  "path": "/standards/U-AS-001.md"
}
```

## Generation Notes

*   `info_type`, `version`, and `date_modified` derive from each standard's front‑matter.
*   CI generator will enrich missing dates using Git last‑commit information.
*   All registry look‑ups performed in‑build; failures trigger CI errors.
*   Script path: `scripts/generate_standards_index.py`.
*   Output location: `/views/standards_index.json`.
