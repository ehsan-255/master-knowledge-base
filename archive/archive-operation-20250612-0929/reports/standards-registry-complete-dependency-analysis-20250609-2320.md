# Complete Standards Registry Dependency Analysis

**Generated**: 2025-06-09 23:20:00  
**Scope**: Every single file in `standards/registry/*`  
**Analysis Type**: COMPREHENSIVE DEPENDENCY MAPPING  

---

## Registry Files Overview

**Location**: `standards/registry/`  
**Total Files**: 10  
**File Types**: YAML (4), TXT (5), Other (1)

```
standards/registry/
├── .gitkeep                        # Repository file
├── criticality_levels.txt          # Generated file  
├── field_order.yaml                # Generated file
├── frontmatter_fields.yaml         # Generated file
├── info_types.txt                  # Generated file
├── lifecycle_gatekeepers.txt       # Generated file
├── mt-registry-tag-glossary.yaml   # Source file
├── mt-schema-frontmatter.yaml      # MASTER Source file
├── registry_schema.yaml            # Schema file
└── tag_categories.txt              # Generated file
```

---

## File-by-File Dependency Analysis

### 1. `mt-schema-frontmatter.yaml` 
**Status**: 🔥 **CRITICAL MASTER SOURCE FILE**  
**Type**: Single Source of Truth  
**Size**: 15KB, 431 lines  

#### **Dependencies (6 tools)**:

**A. `tools/linter/kb_linter.py`**
- **Line 70**: `self.schema_yaml_path = self.registry_path / "mt-schema-frontmatter.yaml"`
- **Usage**: Schema validation for frontmatter linting
- **Impact**: CRITICAL - Linter cannot validate frontmatter without this file

**B. `tools/frontmatter-management/generate_frontmatter_registry.py`**
- **Lines 33, 37, 43**: Path resolution and source loading
- **Lines 162, 177, 178, 202, 203**: Generated file headers reference this
- **Lines 211, 212, 220, 239, 240, 248**: Controlled vocabulary extraction
- **Lines 321, 407, 414, 471**: Main processing and reporting
- **Usage**: GENERATES 5 registry files from this master source
- **Impact**: CRITICAL - This tool regenerates entire registry from this file

**C. `tools/frontmatter-management/generate_schema_docs.py`**
- **Line 27**: `self.schema_yaml_source_path = self.repo_root / "standards" / "registry" / "mt-schema-frontmatter.yaml"`
- **Usage**: Documentation generation from schema
- **Impact**: HIGH - Schema documentation depends on this file

**D. `tools/refactoring-scripts/refactor_criticality_field.py`**
- **Lines 10, 13**: Load criticality vocabulary mappings
- **Lines 39, 125, 127**: Error handling and argument parsing
- **Usage**: Field value normalization based on controlled vocabularies
- **Impact**: HIGH - Field refactoring relies on vocabulary definitions

**E. `tools/naming-enforcer/generate_naming_configs.py`**
- **Line 41**: Listed in protected files array
- **Usage**: Protection from naming enforcement modifications
- **Impact**: MEDIUM - Prevents accidental naming changes

**F. Dependency Chain**: Generates 5 other registry files
- → `criticality_levels.txt`
- → `lifecycle_gatekeepers.txt`  
- → `info_types.txt`
- → `frontmatter_fields.yaml`
- → `field_order.yaml`

---

### 2. `mt-registry-tag-glossary.yaml`
**Status**: 🔥 **CRITICAL SOURCE FILE**  
**Type**: Tag Vocabulary Source  
**Size**: 13KB, 325 lines  

#### **Dependencies (3 tools)**:

**A. `tools/linter/kb_linter.py`**
- **Line 71**: `self.tag_glossary_yaml_path = self.registry_path / "mt-registry-tag-glossary.yaml"`
- **Usage**: Tag validation during linting
- **Impact**: CRITICAL - Tag validation impossible without this file

**B. `tools/frontmatter-management/generate_frontmatter_registry.py`**
- **Lines 44, 264, 265, 269, 273, 417**: Tag category generation source
- **Usage**: GENERATES `tag_categories.txt` from this file
- **Impact**: HIGH - Tag category registry depends on this file

**C. `tools/frontmatter-management/generate_schema_docs.py`**
- **Line 28**: `self.tag_glossary_yaml_source_path = self.repo_root / "standards" / "registry" / "mt-registry-tag-glossary.yaml"`
- **Usage**: Tag documentation generation
- **Impact**: MEDIUM - Tag documentation depends on this file

**D. Dependency Chain**: Generates 1 registry file
- → `tag_categories.txt`

---

### 3. `criticality_levels.txt`
**Status**: ⚡ **GENERATED FILE**  
**Type**: Controlled Vocabulary  
**Size**: 255B, 9 lines  
**Generator**: `generate_frontmatter_registry.py`  

#### **Dependencies (1 tool)**:

**A. `tools/frontmatter-management/generate_frontmatter_registry.py`**
- **Lines 211, 212, 356, 359, 361, 427**: Generation logic and reporting
- **Usage**: GENERATES this file from `mt-schema-frontmatter.yaml`
- **Impact**: This file is OUTPUT, not INPUT

**Direct Consumers**: ❌ **NONE FOUND**
**Status**: Potential dead file or consumed by non-Python tools

---

### 4. `lifecycle_gatekeepers.txt`
**Status**: ⚡ **GENERATED FILE**  
**Type**: Controlled Vocabulary  
**Size**: 321B, 10 lines  
**Generator**: `generate_frontmatter_registry.py`  

#### **Dependencies (1 tool)**:

**A. `tools/frontmatter-management/generate_frontmatter_registry.py`**
- **Lines 239, 240, 363, 366, 368, 428**: Generation logic and reporting
- **Usage**: GENERATES this file from `mt-schema-frontmatter.yaml`
- **Impact**: This file is OUTPUT, not INPUT

**Direct Consumers**: ❌ **NONE FOUND**
**Status**: Potential dead file or consumed by non-Python tools

---

### 5. `info_types.txt`
**Status**: ⚡ **GENERATED FILE**  
**Type**: Controlled Vocabulary  
**Size**: 693B, 31 lines  
**Generator**: `generate_frontmatter_registry.py`  

#### **Dependencies (1 tool)**:

**A. `tools/frontmatter-management/generate_frontmatter_registry.py`**
- **Lines 158, 159, 335, 338, 340, 424**: Generation logic and reporting
- **Usage**: GENERATES this file from `mt-schema-frontmatter.yaml`
- **Impact**: This file is OUTPUT, not INPUT

**Direct Consumers**: ❌ **NONE FOUND**
**Status**: Potential dead file or consumed by non-Python tools

---

### 6. `frontmatter_fields.yaml`
**Status**: ⚡ **GENERATED FILE**  
**Type**: Field Registry  
**Size**: 5.1KB, 126 lines  
**Generator**: `generate_frontmatter_registry.py`  

#### **Dependencies (1 tool)**:

**A. `tools/frontmatter-management/generate_frontmatter_registry.py`**
- **Lines 173, 342, 345, 347, 425**: Generation logic and reporting
- **Usage**: GENERATES this file from `mt-schema-frontmatter.yaml`
- **Impact**: This file is OUTPUT, not INPUT

**Direct Consumers**: ❌ **NONE FOUND**
**Status**: Potential dead file or consumed by non-Python tools

---

### 7. `field_order.yaml`
**Status**: ⚡ **GENERATED FILE**  
**Type**: Field Order Registry  
**Size**: 504B, 24 lines  
**Generator**: `generate_frontmatter_registry.py`  

#### **Dependencies (1 tool)**:

**A. `tools/frontmatter-management/generate_frontmatter_registry.py`**
- **Lines 198, 349, 352, 354, 426**: Generation logic and reporting
- **Usage**: GENERATES this file from `mt-schema-frontmatter.yaml`
- **Impact**: This file is OUTPUT, not INPUT

**Direct Consumers**: ❌ **NONE FOUND**
**Status**: Potential dead file or consumed by non-Python tools

---

### 8. `tag_categories.txt`
**Status**: ⚡ **GENERATED FILE**  
**Type**: Tag Category Registry  
**Size**: 322B, 12 lines  
**Generator**: `generate_frontmatter_registry.py`  

#### **Dependencies (1 tool)**:

**A. `tools/frontmatter-management/generate_frontmatter_registry.py`**
- **Lines 264, 265, 370, 373, 375, 429**: Generation logic and reporting
- **Usage**: GENERATES this file from `mt-registry-tag-glossary.yaml`
- **Impact**: This file is OUTPUT, not INPUT

**Direct Consumers**: ❌ **NONE FOUND**
**Status**: Potential dead file or consumed by non-Python tools

---

### 9. `registry_schema.yaml`
**Status**: 📋 **SCHEMA FILE**  
**Type**: Validation Schema  
**Size**: 1.1KB, 49 lines  

#### **Dependencies**: ❌ **NONE FOUND**
**Direct Consumers**: ❌ **NONE FOUND**
**Status**: Potential dead file or validation schema not used by current tools

---

### 10. `.gitkeep`
**Status**: 📁 **REPOSITORY FILE**  
**Type**: Git placeholder  
**Size**: 64B, 2 lines  

#### **Dependencies**: ❌ **NONE**
**Purpose**: Ensures empty directories are tracked in Git

---

## Registry Directory Access

### Tools that Access Registry Directory Directly:

**A. `tools/linter/kb_linter.py`**
- **Line 69**: `self.registry_path = self.repo_base / "standards" / "registry"`
- **Usage**: Base path for accessing schema and tag files
- **Impact**: CRITICAL - Linter requires registry directory access

**B. `tools/validators/validate_registry.py`**
- **Lines 12, 16, 26**: Registry path handling for validation
- **Usage**: Validates registry files against schemas
- **Impact**: MEDIUM - Registry validation utility

**C. `tools/refactoring-scripts/refactor_criticality_field.py`**
- **Line 12**: `registry_path = os.path.join(repo_base_path, "master-knowledge-base", "standards", "registry")`
- **Usage**: Path construction for accessing schema file
- **Impact**: HIGH - Field refactoring depends on registry access

---

## Critical Dependency Summary

### 🔥 **CANNOT BE REMOVED** (Critical Dependencies):
1. **`mt-schema-frontmatter.yaml`** - 6 tool dependencies, master source file
2. **`mt-registry-tag-glossary.yaml`** - 3 tool dependencies, tag source file

### ⚡ **GENERATED FILES** (Can be regenerated):
3. `criticality_levels.txt` - Generated from mt-schema-frontmatter.yaml
4. `lifecycle_gatekeepers.txt` - Generated from mt-schema-frontmatter.yaml  
5. `info_types.txt` - Generated from mt-schema-frontmatter.yaml
6. `frontmatter_fields.yaml` - Generated from mt-schema-frontmatter.yaml
7. `field_order.yaml` - Generated from mt-schema-frontmatter.yaml
8. `tag_categories.txt` - Generated from mt-registry-tag-glossary.yaml

### 📋 **POTENTIALLY UNUSED**:
9. `registry_schema.yaml` - No current tool dependencies found
10. `.gitkeep` - Repository file, safe to keep

---

## Dependency Chain Analysis

### Master Source Files → Generated Files:
```
mt-schema-frontmatter.yaml (MASTER)
├── criticality_levels.txt
├── lifecycle_gatekeepers.txt  
├── info_types.txt
├── frontmatter_fields.yaml
└── field_order.yaml

mt-registry-tag-glossary.yaml (SOURCE)
└── tag_categories.txt
```

### Tools → Registry Dependencies:
```
linter/kb_linter.py
├── mt-schema-frontmatter.yaml (schema validation)
└── mt-registry-tag-glossary.yaml (tag validation)

frontmatter-management/generate_frontmatter_registry.py
├── mt-schema-frontmatter.yaml (SOURCE)
└── mt-registry-tag-glossary.yaml (SOURCE)
└── GENERATES 6 registry files

frontmatter-management/generate_schema_docs.py
├── mt-schema-frontmatter.yaml (documentation)
└── mt-registry-tag-glossary.yaml (documentation)

refactoring-scripts/refactor_criticality_field.py
└── mt-schema-frontmatter.yaml (vocabulary)
```

---

## Risk Assessment

### 🚨 **HIGH RISK** - Moving These Files Would Break:
- **Linter functionality** (schema and tag validation)
- **Registry generation system** (6 generated files)
- **Schema documentation** (automated docs)
- **Field refactoring tools** (vocabulary mappings)

### ⚠️ **MEDIUM RISK** - Generated Files:
- Can be regenerated but tools may expect them to exist
- Unknown if external processes consume these files
- Safe to delete if regeneration is run afterward

### ✅ **LOW RISK**:
- `registry_schema.yaml` - No dependencies found
- `.gitkeep` - Repository management file

---

**CONCLUSION**: The `standards/registry/` directory contains the critical infrastructure for the entire knowledge base validation and processing system. The two master source files (`mt-schema-frontmatter.yaml` and `mt-registry-tag-glossary.yaml`) are ABSOLUTELY CRITICAL and cannot be moved without breaking multiple essential tools. 