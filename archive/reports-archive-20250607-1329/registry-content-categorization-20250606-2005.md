---
title: Untitled Document
info-type: general
version: 0.0.1
date-created: '2025-06-17'
date-modified: '2025-06-17T02:29:15Z'
tags:
- content-type/general
- criticality/p0-critical
- kb-id/global
kb-id: archive
primary-topic: '[MISSING_PRIMARY_TOPIC]'
scope_application: '[MISSING_SCOPE_APPLICATION]'
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas: []
---
# Registry Content Categorization and Target File Assignment - 20250606-2005

**Generated**: 2025-06-06 20:05  
**Purpose**: Detailed categorization plan specifying exactly which content from each source file will be integrated into each target file  
**Task**: TASK 1.1.3 - Categorize Content for Target File Assignment  

---

## Executive Summary

**Target Files**: 2 consolidated registry files  
**Source Content Mappings**: 7 source files → 2 target files  
**Content Categories**: 6 controlled vocabularies + 1 tag glossary  
**Integration Complexity**: 3 low, 2 medium, 2 high complexity integrations  

---

## Target File 1: mt-registry-tag-glossary.yaml

### Purpose
Consolidated YAML registry for all tag-related content, categories, definitions, and usage guidelines.

### Source Content
- **Primary Source**: `MT-REGISTRY-TAG-GLOSSARY.md` (complete conversion)
- **Secondary Sources**: None (self-contained)

### Target Structure Overview
- Metadata section with source tracking
- Tag categories with hierarchical organization  
- Cross-references and relationships
- Usage guidelines and validation rules
- Generation metadata

### Target Structure
```yaml
# Metadata section
metadata:
  source_document: "MT-REGISTRY-TAG-GLOSSARY.md"
  standard_id: "MT-REGISTRY-TAG-GLOSSARY"
  version: "1.0.0"
  description: "Consolidated tag glossary and registry"
  generated_date: "2025-06-06"
  generated_by: "Registry Consolidation Project"

# Tag categories with hierarchical organization
tag_categories:
  status:
    prefix: "status/"
    description: "Content lifecycle status indicators"
    tags:
      - id: "draft"
        full_tag: "status/draft"
        description: "Content is in initial draft stage, subject to significant change"
      - id: "in-review"
        full_tag: "status/in-review"
        description: "Content is under review by subject matter experts or stakeholders"
      # ... continue for all status tags
  
  kb_id:
    prefix: "kb-id/"
    description: "Knowledge base identification tags"
    tags:
      - id: "standards"
        full_tag: "kb-id/standards"
        description: "For notes belonging to the Standards KB"
      # ... continue for all kb-id tags
  
  # ... continue for all tag categories

# Cross-references and relationships
tag_relationships:
  criticality_alignment:
    description: "Alignment between criticality tags and criticality field values"
    mappings:
      - tag: "criticality/P0-Critical"
        field_value: "P0-Critical"
      # ... continue mappings

# Usage guidelines and validation rules
usage_guidelines:
  mandatory_categories:
    - "status/*"
    - "content-type/*"
    - "topic/*"
  validation_rules:
    - "All tags MUST be in kebab-case"
    - "Tags MUST follow category/value pattern"

# Generation metadata
generation_info:
  created_date: "2025-06-06"
  created_by: "Registry Consolidation Script"
  source_files:
    - "MT-REGISTRY-TAG-GLOSSARY.md"
  replaces:
    - "MT-REGISTRY-TAG-GLOSSARY.md (content converted to YAML)"
```

---

## Target File 2: mt-schema-frontmatter.yaml (Updated)

### Purpose
Enhanced frontmatter schema with all controlled vocabularies integrated from separate YAML files.

### Source Content Integration
- **Existing Content**: Preserve all current sections
- **New Controlled Vocabularies**: Add 6 new controlled vocabulary sections

### Integration Plan
1. **audience_types.yaml** → controlled_vocabularies.audience_type
2. **criticality_levels.yaml** → controlled_vocabularies.criticality  
3. **domain_codes.yaml** → controlled_vocabularies.primary_domain
4. **lifecycle_gatekeepers.yaml** → controlled_vocabularies.lifecycle_gatekeeper
5. **maturity_levels.yaml** → controlled_vocabularies.maturity_level
6. **subdomain_registry.yaml** → controlled_vocabularies.sub_domain

### Target Structure (New/Updated Sections)
```yaml
# Existing sections preserved: metadata, field_order, fields, business_rules, generation_info

# ENHANCED: controlled_vocabularies section
controlled_vocabularies:
  # Existing
  info_type:
    - standard-definition
    - policy-document
    # ... existing values preserved
  
  # NEW: From audience_types.yaml
  audience_type:
    - id: "AUTHOR"
      preferred_label: "Author"
      description: "Primary content producers and maintainers"
    - id: "ENGINEER"
      preferred_label: "Engineer"
      description: "Technical stakeholders integrating or tooling the KB"
    - id: "REVIEWER"
      preferred_label: "Reviewer"
      description: "Subject‑matter or governance reviewers"
  
  # NEW: From criticality_levels.yaml (converted to standard format)
  criticality:
    - id: "P0-Critical"
      preferred_label: "P0-Critical"
      description: "Standard or policy that, if not followed, can lead to severe operational disruption, data loss, security vulnerabilities, or major compliance failures"
      tag: "criticality/P0-Critical"
    - id: "P1-High"
      preferred_label: "P1-High"
      description: "Standard or policy that, if not followed, can lead to significant operational inefficiencies, data integrity issues, or notable compliance gaps"
      tag: "criticality/P1-High"
    # ... continue for all levels
  
  # NEW: From domain_codes.yaml
  primary_domain:
    - id: "AS"
      preferred_label: "Architecture & Structure"
      description: "Rules defining directory structure, modularity, and single‑source build patterns"
    - id: "CS"
      preferred_label: "Content & Semantics"
      description: "Standards governing meaning, metadata keys, and controlled vocabularies"
    # ... continue for all domains
  
  # NEW: From lifecycle_gatekeepers.yaml (converted to standard format)
  lifecycle_gatekeeper:
    - id: "Architect-Review"
      preferred_label: "Architect Review"
      description: "Requires review and approval from a designated system/solution architect or architectural body"
    - id: "SME-Consensus"
      preferred_label: "Subject Matter Expert (SME) Consensus"
      description: "Requires consensus agreement from a defined group of subject matter experts"
    # ... continue for all gatekeepers
  
  # NEW: From maturity_levels.yaml
  maturity_level:
    - id: "IDEA"
      preferred_label: "Idea"
      description: "Initial brainstorming—no formal draft exists yet"
    - id: "DRAFT"
      preferred_label: "Draft"
      description: "Actively being written and refined"
    # ... continue for all levels
  
  # NEW: From subdomain_registry.yaml (hierarchical structure preserved)
  sub_domain:
    AS:  # Architecture & Structure
      - id: "STRUCTURE"
        preferred_label: "Structural Standards"
        description: "Standards related to the overall organization and structure of knowledge bases"
        parent_domain: "AS"
      - id: "INDEXING"
        preferred_label: "Indexing and Mapping"
        description: "Standards for creating and managing indexes, maps, and tables of contents"
        parent_domain: "AS"
      # ... continue for all AS subdomains
    CS:  # Content & Semantics
      - id: "POLICY"
        preferred_label: "Content Policies"
        description: "Policies governing the creation, style, and lifecycle of content"
        parent_domain: "CS"
      # ... continue for all domains

# UPDATED: external_vocabularies section
external_vocabularies:
  tags:
    source: "mt-registry-tag-glossary.yaml"
    description: "Categories and specific tags for document classification"
  kb_id:
    source: "mt-registry-tag-glossary.yaml"
    description: "Knowledge base identifiers"
  # REMOVED: criticality, lifecycle_gatekeeper, primary_domain, sub_domain
  # (now in controlled_vocabularies)

# UPDATED: generation_info section
generation_info:
  created_date: "2025-06-04"
  updated_date: "2025-06-06"
  created_by: "SST Migration Script"
  updated_by: "Registry Consolidation Project"
  purpose: "Single Source of Truth for frontmatter schema"
  replaces: "Manual parsing of MT-SCHEMA-FRONTMATTER.md"
  integrated_sources:
    - "audience_types.yaml"
    - "criticality_levels.yaml"
    - "domain_codes.yaml"
    - "lifecycle_gatekeepers.yaml"
    - "maturity_levels.yaml"
    - "subdomain_registry.yaml"
  consumers:
    - "generate_frontmatter_registry.py"
    - "generate_schema_docs.py"
    - "frontmatter validators"
    - "naming enforcer"
    - "linting tools"
```

---

## Content Mapping Details

### Low Complexity Integrations (3 files)
- **audience_types.yaml**: Direct mapping, standard registry format
- **domain_codes.yaml**: Direct mapping, standard registry format  
- **maturity_levels.yaml**: Direct mapping, standard registry format

### Medium Complexity Integrations (2 files)
- **criticality_levels.yaml**: Format standardization required (list → standard registry)
- **lifecycle_gatekeepers.yaml**: Format standardization required (list → standard registry)

### High Complexity Integrations (2 files)
- **subdomain_registry.yaml**: Hierarchical structure preservation required
- **MT-REGISTRY-TAG-GLOSSARY.md**: Complete markdown to YAML conversion

---

## External Reference Updates Required

### Remove from external_vocabularies
- criticality (moving to controlled_vocabularies)
- lifecycle_gatekeeper (moving to controlled_vocabularies)
- primary_domain (moving to controlled_vocabularies)
- sub_domain (moving to controlled_vocabularies)

### Update remaining external_vocabularies
- tags: source changed to "mt-registry-tag-glossary.yaml"
- kb_id: source changed to "mt-registry-tag-glossary.yaml"

---

## Archive Strategy

### Files to Archive (6 YAML + 3 TXT)
- audience_types.yaml
- criticality_levels.yaml
- domain_codes.yaml
- lifecycle_gatekeepers.yaml
- maturity_levels.yaml
- subdomain_registry.yaml
- criticality_levels.txt
- lifecycle_gatekeepers.txt
- tag_categories.txt

### File to Move
- MT-REGISTRY-TAG-GLOSSARY.md → Move to standards/src/

---

## Content Preservation Validation

### Data Integrity Checklist
- [ ] All audience types preserved (3 items)
- [ ] All criticality levels preserved (5 items)
- [ ] All domain codes preserved (8 items)
- [ ] All lifecycle gatekeepers preserved (6 items)
- [ ] All maturity levels preserved (5 items)
- [ ] All subdomain mappings preserved (~25 items across 8 domains)
- [ ] All tag categories preserved
- [ ] All tag definitions preserved
- [ ] All usage guidelines preserved
- [ ] All cross-references preserved

---

## Next Steps for STEP 1.2

1. **Design mt-registry-tag-glossary.yaml Architecture**
2. **Design mt-schema-frontmatter.yaml Updates**
3. **Validate Integration Strategy**

---

**Categorization Complete**: 2025-06-06 20:05  
**Content Mappings**: 7 source files → 2 target files  
#### Content Analysis
- **Registry ID**: AUDIENCE
- **Title**: "Intended Audience"
- **Entries**: 3 items
- **Format**: Standard registry format

#### Target Assignment
- **Target File**: `mt-schema-frontmatter.yaml`
- **Target Section**: `controlled_vocabularies.audience_type`
- **Conversion**: Direct mapping (Low Complexity)

#### Mapping Details
```yaml
# Source format
entries:
  - id: "AUTHOR"
    preferred_label: "Author"
    description: "Primary content producers and maintainers."

# Target format
controlled_vocabularies:
  audience_type:
    - id: "AUTHOR"
      preferred_label: "Author"
      description: "Primary content producers and maintainers"
```

### 📋 **SOURCE FILE 2: criticality_levels.yaml**

#### Content Analysis
- **Format**: List format (non-standard)
- **Entries**: 5 levels
- **Structure**: level/tag/description

#### Target Assignment
- **Target File**: `mt-schema-frontmatter.yaml`
- **Target Section**: `controlled_vocabularies.criticality`
- **Conversion**: Format standardization (Medium Complexity)

#### Mapping Details
```yaml
# Source format
- level: P0-Critical
  tag: criticality/P0-Critical
  description: "Standard or policy that, if not followed, can lead to severe operational disruption..."

# Target format
controlled_vocabularies:
  criticality:
    - id: "P0-Critical"
      preferred_label: "P0-Critical"
      description: "Standard or policy that, if not followed, can lead to severe operational disruption..."
      tag: "criticality/P0-Critical"
```

### 📋 **SOURCE FILE 3: domain_codes.yaml**

#### Content Analysis
- **Registry ID**: DOMAIN
- **Title**: "Primary Domain of Concern"
- **Entries**: 8 domains
- **Format**: Standard registry format

#### Target Assignment
- **Target File**: `mt-schema-frontmatter.yaml`
- **Target Section**: `controlled_vocabularies.primary_domain`
- **Conversion**: Direct mapping (Low Complexity)

#### Mapping Details
```yaml
# Source format
entries:
  - id: "AS"
    preferred_label: "Architecture & Structure"
    description: "Rules defining directory structure, modularity, and single‑source build patterns."

# Target format
controlled_vocabularies:
  primary_domain:
    - id: "AS"
      preferred_label: "Architecture & Structure"
      description: "Rules defining directory structure, modularity, and single‑source build patterns"
```

### 📋 **SOURCE FILE 4: lifecycle_gatekeepers.yaml**

#### Content Analysis
- **Format**: List format (non-standard)
- **Entries**: 6 gatekeepers
- **Structure**: gatekeeper/name/description

#### Target Assignment
- **Target File**: `mt-schema-frontmatter.yaml`
- **Target Section**: `controlled_vocabularies.lifecycle_gatekeeper`
- **Conversion**: Format standardization (Medium Complexity)

#### Mapping Details
```yaml
# Source format
- gatekeeper: Architect-Review
  name: Architect Review
  description: "Requires review and approval from a designated system/solution architect or architectural body."

# Target format
controlled_vocabularies:
  lifecycle_gatekeeper:
    - id: "Architect-Review"
      preferred_label: "Architect Review"
      description: "Requires review and approval from a designated system/solution architect or architectural body"
```

### 📋 **SOURCE FILE 5: maturity_levels.yaml**

#### Content Analysis
- **Registry ID**: MATURITY
- **Title**: "Lifecycle Maturity"
- **Entries**: 5 levels
- **Format**: Standard registry format

#### Target Assignment
- **Target File**: `mt-schema-frontmatter.yaml`
- **Target Section**: `controlled_vocabularies.maturity_level`
- **Conversion**: Direct mapping (Low Complexity)

#### Mapping Details
```yaml
# Source format
entries:
  - id: "IDEA"
    preferred_label: "Idea"
    description: "Initial brainstorming—no formal draft exists yet."

# Target format
controlled_vocabularies:
  maturity_level:
    - id: "IDEA"
      preferred_label: "Idea"
      description: "Initial brainstorming—no formal draft exists yet"
```

### 📋 **SOURCE FILE 6: subdomain_registry.yaml**

#### Content Analysis
- **Format**: Hierarchical mapping by domain
- **Entries**: 8 domains with ~25 subdomains total
- **Structure**: Complex nested structure

#### Target Assignment
- **Target File**: `mt-schema-frontmatter.yaml`
- **Target Section**: `controlled_vocabularies.sub_domain`
- **Conversion**: Hierarchical structure preservation (High Complexity)

#### Mapping Details
```yaml
# Source format
AS: # Architectural Standards
  - code: STRUCTURE
    name: Structural Standards
    description: "Standards related to the overall organization and structure of knowledge bases."

# Target format
controlled_vocabularies:
  sub_domain:
    AS:
      - id: "STRUCTURE"
        preferred_label: "Structural Standards"
        description: "Standards related to the overall organization and structure of knowledge bases"
        parent_domain: "AS"
```

### 📋 **SOURCE FILE 7: MT-REGISTRY-TAG-GLOSSARY.md**

#### Content Analysis
- **Format**: Markdown with structured sections
- **Content**: Tag categories, definitions, usage guidelines
- **Size**: 8.2KB, 146 lines

#### Target Assignment
- **Target File**: `mt-registry-tag-glossary.yaml`
- **Target Section**: Complete file conversion
- **Conversion**: Markdown to YAML structure (High Complexity)

#### Mapping Strategy
1. **Extract tag categories**: Parse markdown sections into YAML categories
2. **Convert tag definitions**: Transform markdown lists into structured YAML
3. **Preserve relationships**: Maintain cross-references and hierarchies
4. **Add metadata**: Include generation tracking and source information

---

## Content Preservation Validation

### ✅ **Data Integrity Checklist**

#### Controlled Vocabularies
- [ ] All audience types preserved (3 items)
- [ ] All criticality levels preserved (5 items)
- [ ] All domain codes preserved (8 items)
- [ ] All lifecycle gatekeepers preserved (6 items)
- [ ] All maturity levels preserved (5 items)
- [ ] All subdomain mappings preserved (~25 items across 8 domains)

#### Tag Content
- [ ] All tag categories preserved
- [ ] All tag definitions preserved
- [ ] All usage guidelines preserved
- [ ] All cross-references preserved

#### Metadata
- [ ] Source tracking information added
- [ ] Generation timestamps included
- [ ] Version information preserved
- [ ] Consumer references updated

### 🔍 **Format Standardization Validation**

#### Standard Registry Format Adoption
```yaml
# Target format for all controlled vocabularies
field_name:
  - id: "CODE"
    preferred_label: "Display Name"
    description: "Description text"
    # Additional metadata as needed
```

#### Special Format Handling
1. **Hierarchical Data** (subdomain_registry):
   - Preserve domain grouping
   - Add parent_domain references
   - Maintain nested structure

2. **Tag References** (criticality_levels):
   - Include both field value and tag format
   - Maintain tag/field alignment

3. **Complex Descriptions** (all sources):
   - Preserve full description text
   - Remove trailing punctuation for consistency
   - Maintain special characters and formatting

---

## Integration Complexity Assessment

### 🟢 **Low Complexity (3 files)**
- `audience_types.yaml` → Direct mapping
- `domain_codes.yaml` → Direct mapping  
- `maturity_levels.yaml` → Direct mapping

**Characteristics**: Standard registry format, simple structure, no format conversion needed

### 🟡 **Medium Complexity (2 files)**
- `criticality_levels.yaml` → Format standardization required
- `lifecycle_gatekeepers.yaml` → Format standardization required

**Characteristics**: Non-standard format, requires structure conversion, field mapping needed

### 🔴 **High Complexity (2 files)**
- `subdomain_registry.yaml` → Hierarchical structure preservation
- `MT-REGISTRY-TAG-GLOSSARY.md` → Complete markdown to YAML conversion

**Characteristics**: Complex structure, content extraction required, relationship preservation critical

---

## External Reference Updates Required

### 📝 **mt-schema-frontmatter.yaml Updates**

#### Remove from external_vocabularies
```yaml
# REMOVE these entries (moving to controlled_vocabularies)
criticality:
  source: "MT-REGISTRY-TAG-GLOSSARY"
lifecycle_gatekeeper:
  source: "MT-REGISTRY-TAG-GLOSSARY"
primary_domain:
  source: "domain_codes.yaml"
sub_domain:
  source: "subdomain_registry.yaml"
```

#### Update remaining external_vocabularies
```yaml
# UPDATE these entries
tags:
  source: "mt-registry-tag-glossary.yaml"  # Changed from MD to YAML
kb_id:
  source: "mt-registry-tag-glossary.yaml"  # Changed from MD to YAML
```

### 📝 **Field Definition Updates**

#### Update validation rules references
```yaml
fields:
  primary_domain:
    validation_rules:
      - "Value MUST exist in controlled_vocabularies.primary_domain"  # Updated reference
  sub_domain:
    validation_rules:
      - "Value MUST exist in controlled_vocabularies.sub_domain for the given primary_domain"  # Updated reference
  criticality:
    validation_rules:
      - "Value MUST come from controlled_vocabularies.criticality"  # Updated reference
  lifecycle_gatekeeper:
    validation_rules:
      - "Value MUST come from controlled_vocabularies.lifecycle_gatekeeper"  # Updated reference
```

---

## Archive Strategy

### 📦 **Files to Archive**

#### Source YAML Files (6 files)
- `audience_types.yaml` → Archive after integration
- `criticality_levels.yaml` → Archive after integration
- `domain_codes.yaml` → Archive after integration
- `lifecycle_gatekeepers.yaml` → Archive after integration
- `maturity_levels.yaml` → Archive after integration
- `subdomain_registry.yaml` → Archive after integration

#### Generated TXT Files (3 files)
- `criticality_levels.txt` → Archive (will be regenerated from consolidated source)
- `lifecycle_gatekeepers.txt` → Archive (will be regenerated from consolidated source)
- `tag_categories.txt` → Archive (will be regenerated from consolidated source)

#### Markdown File (1 file)
- `MT-REGISTRY-TAG-GLOSSARY.md` → Move to `standards/src/` (not archive)

---

## Next Steps for STEP 1.2

1. **Design mt-registry-tag-glossary.yaml Architecture**:
   - Define complete YAML schema structure
   - Plan tag categories and hierarchies
   - Design metadata and generation tracking sections

2. **Design mt-schema-frontmatter.yaml Updates**:
   - Plan controlled vocabularies integration
   - Update external vocabularies references
   - Validate business rules compatibility

3. **Validate Integration Strategy**:
   - Ensure no content loss during conversion
   - Plan validation procedures for consolidated files

---

**Categorization Complete**: 2025-06-06 20:05  
**Content Mappings**: 7 source files → 2 target files  
**Complexity Assessment**: 3 low, 2 medium, 2 high  
**Ready for**: STEP 1.2 - Design mt-registry-tag-glossary.yaml Architecture
