---
title: File with Links Test
standard_id: TEST-LINK-UPDATING
date-created: 2025-01-11
info-type: general
version: 0.0.1
date-modified: '2025-06-17T02:29:16Z'
tags:
- content-type/general
- criticality/p0-critical
- kb-id/global
kb-id: test-environment
primary-topic: '[MISSING_PRIMARY_TOPIC]'
scope_application: '[MISSING_SCOPE_APPLICATION]'
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas: []
---
# File with Links for Testing Link Update Functionality

This file contains various types of links that should be updated when files are renamed:

## Markdown Links
- [CamelCase File](camel-case-file.md)
- [Uppercase Extension](uppercase-extension-test.md)
- [Frontmatter Violations](frontmatter-field-violations.md)

## Relative Path References
- See file: ./camel-case-file.md for examples
- Configuration: ../config/test-config.json
- Image: ![test](../images/test-image.PNG)

## Wiki-style Links
- [[camel-case-file]]
- [[uppercase-extension-test.md]]

This file tests the critical link updating functionality that must be implemented to prevent breaking references when files are renamed.
