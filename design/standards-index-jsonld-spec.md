---
title: 'Standards Index JSON-LD – Spec Sketch'
aliases: ['JSON-LD Index Spec']
tags:
  - kb-id/global # Placeholder
  - content-type/design-document # Placeholder
  - status/draft # Placeholder
  - topic/automation # Placeholder
kb-id: 'global' # Placeholder
info-type: 'design-document' # Placeholder
primary-topic: 'Design specification sketch for the standards_index.json in JSON-LD format.'
related-standards: "N/A" # Placeholder
version: '0.1.0-draft'
date-created: '2025-05-27' # Placeholder - use actual date
date-modified: '2025-05-27' # Placeholder - use actual date
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