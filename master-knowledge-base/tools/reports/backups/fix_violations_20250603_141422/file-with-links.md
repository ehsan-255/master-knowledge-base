---
title: File with Links Test
standard_id: TEST-LINK-UPDATING
date-created: 2025-01-11
---

# File with Links for Testing Link Update Functionality

This file contains various types of links that should be updated when files are renamed:

## Markdown Links
- [CamelCase File](CamelCaseFile.md)
- [Uppercase Extension](uppercase-extension-test.MD)
- [Frontmatter Violations](frontmatter-field-violations.md)

## Relative Path References
- See file: ./CamelCaseFile.md for examples
- Configuration: ../config/test-config.json
- Image: ![test](../images/test-image.PNG)

## Wiki-style Links
- [[CamelCaseFile]]
- [[uppercase-extension-test.MD]]

This file tests the critical link updating functionality that must be implemented to prevent breaking references when files are renamed. 