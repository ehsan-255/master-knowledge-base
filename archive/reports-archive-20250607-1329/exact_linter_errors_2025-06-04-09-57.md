# Exact Linter Errors Report - GitHub Actions Execution

**Generated:** 2025-06-04 09:57:00  
**Source:** Standards Check GitHub Actions workflow execution  
**Total Files with Issues:** 9  
**Total Errors:** 43  
**Total Warnings:** 30

## Files with Errors and Warnings

### 1. Collection Documents (4 files) - Missing Mandatory Frontmatter

#### `master-knowledge-base/dist/collections/collection-architecture-structure.md`
**Errors (9):**
- [L1] Mandatory key 'version' missing
- [L1] Mandatory key 'date-created' missing
- [L1] Mandatory key 'date-modified' missing
- [L1] Mandatory key 'primary-topic' missing
- [L1] Mandatory key 'kb-id' missing
- [L1] Mandatory key 'scope_application' missing
- [L1] Mandatory key 'criticality' missing
- [L1] Mandatory key 'lifecycle_gatekeeper' missing
- [L1] Mandatory key 'impact_areas' missing

**Warnings (15):**
- [L7] Tag 'kb-collection' has unrecognized category prefix
- [L7] Tag 'derived-view' has unrecognized category prefix
- [L7] Tag 'info-type/collection-document' has unrecognized category prefix
- [L82] Broken link: '[[SF-CONVENTIONS-NAMING]]' not found
- [L166] Broken link: '[[SF-CONVENTIONS-NAMING]]' not found
- [L786] Broken link: '[[SF-CONVENTIONS-NAMING]]' not found
- [L792] Broken link: '[[SF-CONVENTIONS-NAMING]]' not found
- [L826] Broken link: '[[SF-CONVENTIONS-NAMING]]' not found
- [L919] Broken link: '[[SF-CONVENTIONS-NAMING]]' not found
- [L941] Broken link: '[[SF-CONVENTIONS-NAMING]]' not found
- [L986] Broken link: '[[SF-CONVENTIONS-NAMING]]' not found
- [L1006] Broken link: '[[SF-CONVENTIONS-NAMING]]' not found
- [L1020] Broken link: '[[SF-CONVENTIONS-NAMING]]' not found
- [L1055] Broken link: '[[SF-CONVENTIONS-NAMING]]' not found
- [L1112] Broken link: '[[SF-CONVENTIONS-NAMING]]' not found

#### `master-knowledge-base/dist/collections/collection-content-policies.md`
**Errors (9):**
- [L1] Mandatory key 'version' missing
- [L1] Mandatory key 'date-created' missing
- [L1] Mandatory key 'date-modified' missing
- [L1] Mandatory key 'primary-topic' missing
- [L1] Mandatory key 'kb-id' missing
- [L1] Mandatory key 'scope_application' missing
- [L1] Mandatory key 'criticality' missing
- [L1] Mandatory key 'lifecycle_gatekeeper' missing
- [L1] Mandatory key 'impact_areas' missing

**Warnings (7):**
- [L7] Tag 'kb-collection' has unrecognized category prefix
- [L7] Tag 'derived-view' has unrecognized category prefix
- [L7] Tag 'info-type/collection-document' has unrecognized category prefix
- [L551] Broken link: '[[SF-CONVENTIONS-NAMING]]' not found
- [L577] Broken link: '[[SF-CONVENTIONS-NAMING]]' not found
- [L598] Broken link: '[[SF-CONVENTIONS-NAMING]]' not found
- [L626] Broken link: '[[SF-CONVENTIONS-NAMING]]' not found

#### `master-knowledge-base/dist/collections/collection-metadata-tagging.md`
**Errors (9):**
- [L1] Mandatory key 'version' missing
- [L1] Mandatory key 'date-created' missing
- [L1] Mandatory key 'date-modified' missing
- [L1] Mandatory key 'primary-topic' missing
- [L1] Mandatory key 'kb-id' missing
- [L1] Mandatory key 'scope_application' missing
- [L1] Mandatory key 'criticality' missing
- [L1] Mandatory key 'lifecycle_gatekeeper' missing
- [L1] Mandatory key 'impact_areas' missing

**Warnings (3):**
- [L7] Tag 'kb-collection' has unrecognized category prefix
- [L7] Tag 'derived-view' has unrecognized category prefix
- [L7] Tag 'info-type/collection-document' has unrecognized category prefix

#### `master-knowledge-base/dist/collections/collection-syntax-formatting.md`
**Errors (9):**
- [L1] Mandatory key 'version' missing
- [L1] Mandatory key 'date-created' missing
- [L1] Mandatory key 'date-modified' missing
- [L1] Mandatory key 'primary-topic' missing
- [L1] Mandatory key 'kb-id' missing
- [L1] Mandatory key 'scope_application' missing
- [L1] Mandatory key 'criticality' missing
- [L1] Mandatory key 'lifecycle_gatekeeper' missing
- [L1] Mandatory key 'impact_areas' missing

**Warnings (3):**
- [L7] Tag 'kb-collection' has unrecognized category prefix
- [L7] Tag 'derived-view' has unrecognized category prefix
- [L7] Tag 'info-type/collection-document' has unrecognized category prefix

### 2. Standards Documents (3 files) - Invalid Criticality Values

#### `master-knowledge-base/standards/changelog.md`
**Errors (1):**
- [L22] 'criticality' ('P4-Informational') not in defined list. Valid: ['P0-Critical', 'P1-High', 'P2-Medium', 'P3-Low']

**Warnings (1):**
- [L3] Filename 'changelog.md' should match 'standard_id' 'OM-STANDARDS-CHANGELOG'

#### `master-knowledge-base/standards/src/OM-AUTOMATION-LLM-PROMPT-LIBRARY.md`
**Errors (1):**
- [L25] 'criticality' ('P4-Informational') not in defined list. Valid: ['P0-Critical', 'P1-High', 'P2-Medium', 'P3-Low']

#### `master-knowledge-base/tools/changelog.md`
**Errors (1):**
- [L23] 'criticality' ('P4-Informational') not in defined list. Valid: ['P0-Critical', 'P1-High', 'P2-Medium', 'P3-Low']

**Warnings (1):**
- [L3] Filename 'changelog.md' should match 'standard_id' 'OM-TOOLS-CHANGELOG'

### 3. Date Format Issues (1 file)

#### `master-knowledge-base/standards/src/GM-CONVENTIONS-NAMING.md`
**Errors (2):**
- [L19] 'date-created' ('2025-05-29') invalid ISO-8601 format. Required: YYYY-MM-DDTHH:MM:SSZ
- [L20] 'date-modified' ('2025-01-11') invalid ISO-8601 format. Required: YYYY-MM-DDTHH:MM:SSZ

### 4. Invalid Info-Type (1 file)

#### `master-knowledge-base/standards/templates/UA-TPL-CHANGELOG-DOCUMENT.md`
**Errors (2):**
- [L10] 'info-type' ('template') not in defined list. Valid: ['standard-definition', 'policy-document', 'guide-document', 'glossary-document', 'template-document', 'registry-document', 'schema-document', 'navigation-document', 'chapter-document', 'key-definition-set', 'kb-definition-map', 'how-to-guide', 'tutorial-document', 'troubleshooting-guide', 'reference-document', 'architecture-overview', 'design-specification', 'meeting-notes', 'report-document', 'process-definition', 'role-definition', 'service-definition', 'api-specification', 'data-model-definition', 'security-standard', 'compliance-guideline', 'collection-document', 'mandate-document', 'changelog']
- [L19] 'criticality' ('P4-Informational') not in defined list. Valid: ['P0-Critical', 'P1-High', 'P2-Medium', 'P3-Low']

## Error Categories Summary

### Missing Mandatory Frontmatter Fields (36 errors)
**Affected Files:** 4 collection documents
**Missing Fields:** version, date-created, date-modified, primary-topic, kb-id, scope_application, criticality, lifecycle_gatekeeper, impact_areas

### Invalid Criticality Values (4 errors)
**Affected Files:** 4 files
**Invalid Value:** 'P4-Informational'
**Valid Values:** 'P0-Critical', 'P1-High', 'P2-Medium', 'P3-Low'

### Invalid Date Formats (2 errors)
**Affected Files:** 1 file
**Issue:** Date format 'YYYY-MM-DD' instead of required 'YYYY-MM-DDTHH:MM:SSZ'

### Invalid Info-Type (1 error)
**Affected Files:** 1 file
**Issue:** 'template' should be 'template-document'

### Unrecognized Tag Prefixes (12 warnings)
**Affected Files:** 4 collection documents
**Invalid Tags:** 'kb-collection', 'derived-view', 'info-type/collection-document'

### Broken Internal Links (16 warnings)
**Affected Files:** 2 collection documents
**Missing Standard:** 'SF-CONVENTIONS-NAMING'

### Filename Mismatches (2 warnings)
**Affected Files:** 2 changelog files
**Issue:** Filename doesn't match standard_id

## Remediation Priority

### High Priority (Errors - 43 total)
1. **Collection Documents:** Add missing mandatory frontmatter fields (36 errors)
2. **Criticality Values:** Update 'P4-Informational' to valid values (4 errors)
3. **Date Formats:** Convert to ISO-8601 format (2 errors)
4. **Info-Type:** Change 'template' to 'template-document' (1 error)

### Medium Priority (Warnings - 30 total)
1. **Broken Links:** Create or fix 'SF-CONVENTIONS-NAMING' standard (16 warnings)
2. **Tag Prefixes:** Update collection document tags (12 warnings)
3. **Filename Mismatches:** Rename changelog files (2 warnings) 