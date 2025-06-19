---
title: 'Standard: Code Block Syntax'
standard_id: SF-SYNTAX-CODE-BLOCKS
aliases:
- Code Block Syntax
- Inline and Fenced Code
tags:
- content-type/standard-definition
- content-type/technical-standard
- criticality/p1-high
- kb-id/standards
- status/active
- topic/markdown
- topic/sf
kb-id: standards
info-type: standard-definition
primary-topic: Code Block Syntax
related-standards:
- SF-SYNTAX-CHARACTER-ESCAPING
version: 1.0.0
date-created: '2025-01-20T00:00:00Z'
date-modified: '2025-01-20T00:00:00Z'
primary_domain: SF
sub_domain: MARKDOWN
scope_application: Defines code block syntax for all Markdown documents.
criticality: P1-High
lifecycle_gatekeeper: Architect-Review
impact_areas:
- Technical content
- Code representation
---
# Standard: Code Block Syntax (SF-SYNTAX-CODE-BLOCKS)

## 1. Standard Statement

This standard **MANDATES** code block syntax for all Markdown documents.

## 2. Mandatory Rules

### Rule 2.1: Inline Code
**MUST** use single backticks for inline code spans.

**Syntax:** `` `code` ``

### Rule 2.2: Fenced Code Blocks
**MUST** use triple backticks for multi-line code blocks.

**Syntax:** 
````markdown
```
code content
```
````

### Rule 2.3: Language Identifiers
**SHOULD** specify language identifier for syntax highlighting.

**Syntax:**
````markdown
```python
def hello():
    print("Hello")
```
````

### Rule 2.4: Standard Language Names
**MUST** use standard language identifiers: `python`, `javascript`, `bash`, `yaml`, `json`, `markdown`.

## 3. Examples

```markdown
Use the `printf()` function for output.

```python
def hello_world():
    print("Hello, World!")
```

```bash
ls -la
```
````

## 4. Scope of Application

**MANDATORY** for all Markdown documents in the Knowledge Base. 