# Collection Linter Issue Analysis

**Date:** 2025-06-04  
**Issue:** Collection documents failing linter validation with missing mandatory frontmatter fields  
**Root Cause:** Mismatch between collection builder output and linter expectations

## Problem Summary

The linter is flagging collection documents with 36 errors for missing mandatory frontmatter fields, but this is a **script logic issue**, not a document content issue.

## Root Cause Analysis

### 1. Collection Builder Output
The collection builder (`generate_collections.py`) generates frontmatter with these fields:
```yaml
---
title: "Collection Title"
description: "Collection description"
date_generated: "2025-06-04T16:57:56.435783+00:00"
source_collection_definition_id: "collection_id"
number_of_standards: 6
tags: ["kb-collection", "derived-view", "info-type/collection-document"]
info-type: "collection-document"
---
```

### 2. Linter Expectations
The linter (`kb_linter.py`) expects these mandatory fields for ALL documents:
```python
MANDATORY_KEYS_BASE = [
    "title", "info-type", "version", "date-created", "date-modified", 
    "primary-topic", "kb-id", "tags", "scope_application", 
    "criticality", "lifecycle_gatekeeper", "impact_areas"
]
```

### 3. The Mismatch
**Missing Fields in Collection Documents:**
- `version` - Collections don't have versions (they're auto-generated)
- `date-created` - Collections use `date_generated` instead
- `date-modified` - Collections are regenerated, not modified
- `primary-topic` - Collections aggregate multiple topics
- `kb-id` - Collections don't belong to a specific KB
- `scope_application` - Collections are derived views
- `criticality` - Collections are informational aggregations
- `lifecycle_gatekeeper` - Collections are auto-generated
- `impact_areas` - Collections don't have direct impact

## Issue Classification

This is a **SCRIPT LOGIC ISSUE** in two areas:

### 1. Linter Logic Issue
The linter applies the same mandatory field validation to ALL documents, including auto-generated collection documents that have a fundamentally different purpose and structure.

### 2. Collection Builder Logic Issue  
The collection builder doesn't generate frontmatter that complies with the linter's expectations, even though collection documents have `info-type: "collection-document"`.

## Solutions

### Option 1: Fix Linter Logic (RECOMMENDED)
Add special handling for collection documents in the linter:

```python
# In lint_file function, around line 241
current_info_type = frontmatter_data.get("info-type")
if current_info_type in ["standard-definition", "policy-document"]:
    mandatory_keys = MANDATORY_KEYS_FOR_STANDARD_DEFINITION_POLICY
elif current_info_type == "collection-document":
    # Collection documents have different mandatory fields
    mandatory_keys = ["title", "info-type", "tags", "description", "date_generated"]
else:
    mandatory_keys = MANDATORY_KEYS_BASE
```

### Option 2: Fix Collection Builder (NOT RECOMMENDED)
Add all mandatory fields to collection builder output, but this would be artificial since collections don't need these fields.

### Option 3: Exclude Collections from Linting (NOT RECOMMENDED)
Skip linting collection documents entirely, but this removes quality control.

## Tag Prefix Issues

**Additional Issue Found:** Collection documents use tags that don't match the linter's expected prefixes:
- `"kb-collection"` - No valid prefix
- `"derived-view"` - No valid prefix  
- `"info-type/collection-document"` - Invalid prefix

**Valid prefixes according to linter:** `['status/', 'kb-id/', 'content-type/', 'topic/', 'criticality/', 'lifecycle_gatekeeper/']`

**Fix:** Update collection builder to use valid tag prefixes:
```yaml
tags: ["content-type/collection-document", "status/published", "topic/derived-view"]
```

## Broken Links Issue

Collections reference `[[SF-CONVENTIONS-NAMING]]` which doesn't exist in the standards index. This is a separate content issue.

## Recommended Actions

1. **HIGH PRIORITY:** Modify linter to handle collection documents appropriately
2. **MEDIUM PRIORITY:** Update collection builder to use valid tag prefixes
3. **LOW PRIORITY:** Fix broken link references in source standards

## Impact Assessment

- **Current State:** 36 false positive errors blocking GitHub Actions workflow
- **After Fix:** Collection documents will pass linter validation
- **Risk:** Low - changes are isolated to collection document handling 