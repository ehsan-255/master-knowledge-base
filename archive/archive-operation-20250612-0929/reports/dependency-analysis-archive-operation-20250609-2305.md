# Dependency Analysis Report - Archive Operation

**Generated**: 2025-06-09 23:05  
**Operation**: Archive scribe files and migration scripts  
**Archive Folders Created**:
- `archive/scribe-files-archive-20250609-2305/`
- `archive/migration-scripts-archive-20250609-2305/`

---

## Files Archived

### A. Scribe-Specific Files (Root Directory)
✅ **ARCHIVED SUCCESSFULLY**
- `scribe-hma-blueprint.md` → `archive/scribe-files-archive-20250609-2305/`
- `scribe-refinements-progress-tracker.md` → `archive/scribe-files-archive-20250609-2305/`
- `scribe-refinements-roadmap-checklist.md` → `archive/scribe-files-archive-20250609-2305/`
- `scribe-refinements-roadmap.md` → `archive/scribe-files-archive-20250609-2305/`

**Dependency Analysis**: ✅ **NO TOOL DEPENDENCIES FOUND**
- No Python tools reference these files
- Safe to archive without tool modifications

### B. Migration Scripts Folder
✅ **ARCHIVED SUCCESSFULLY**
- `tools/migration-scripts/` → `archive/migration-scripts-archive-20250609-2305/migration-scripts/`

**Dependency Analysis**: ✅ **NO EXTERNAL DEPENDENCIES FOUND**
- Migration scripts are standalone utilities
- Only reference each other within the folder
- Safe to archive as complete unit

---

## Tool Dependencies on Target Files

### 1. Config Files (`config/config.json`, `config/config.schema.json`)

**Dependencies Found:**
- **`tools/scribe/core/config_manager.py`**
  - Lines 51-52: Hard-coded paths to config files
  - Default paths: `"config/config.json"`, `"config/config.schema.json"`
  - **Impact**: Config Manager will fail if files moved
  - **Recommendation**: Keep config files in current location

### 2. Dist Files (`dist/standards_index.json`)

**Dependencies Found:**
- **`tools/indexer/generate_index.py`** (Line 105)
  - Outputs to `standards_index.json` by default
  - **Impact**: Generator tool creates this file

- **`tools/builder/generate_collections.py`** (Line 253)
  - Default input: `"dist/standards_index.json"`
  - **Impact**: Collection builder reads this file

- **`tools/linter/kb_linter.py`** (Line 120)
  - Loads standards index for link validation
  - **Impact**: Linter requires this file for standard ID validation

- **`tools/naming-enforcer/generate_naming_configs.py`** (Line 39)
  - References in protected files list
  - **Impact**: Naming enforcer protects this file

- **`tools/migration-scripts/update_path_references.py`** (Lines 74, 370-384)
  - Special handling for standards_index.json updates
  - **Impact**: Migration tool manages this file

### 3. Standards Registry Files (`standards/registry/*`)

**Dependencies Found:**
- **`tools/linter/kb_linter.py`** (Lines 70-71)
  - `mt-schema-frontmatter.yaml`: Schema validation
  - `mt-registry-tag-glossary.yaml`: Tag validation
  - **Impact**: Core linting functionality

- **`tools/frontmatter-management/generate_frontmatter_registry.py`** (Lines 33-44)
  - Master source file: `mt-schema-frontmatter.yaml`
  - Tag glossary source: `mt-registry-tag-glossary.yaml`
  - **Impact**: Registry generation system

- **`tools/frontmatter-management/generate_schema_docs.py`** (Lines 27-28)
  - Schema documentation generation
  - **Impact**: Documentation automation

- **`tools/refactoring-scripts/refactor_criticality_field.py`** (Lines 10-39)
  - Loads criticality levels from `mt-schema-frontmatter.yaml`
  - **Impact**: Field refactoring automation

- **`tools/naming-enforcer/generate_naming_configs.py`** (Line 41)
  - References `mt-schema-frontmatter.yaml`
  - **Impact**: Naming configuration generation

### 4. AS-INDEX-KB-MASTER.md

**Dependencies Found:**
- **`tools/migration-scripts/validate_migration.py`** (Line 29)
  - Validation whitelist
  - **Impact**: Migration validation

- **`tools/migration-scripts/rollback_migration.py`** (Line 108)
  - Rollback protection list
  - **Impact**: Rollback safety

- **`tools/migration-scripts/migrate_file_structure.py`** (Line 31)
  - Migration protection list
  - **Impact**: Migration safety

**Note**: All dependent migration scripts have been archived, so these dependencies are no longer active.

---

## Critical Analysis

### Safe to Archive (✅)
1. **Scribe files**: No tool dependencies - archive safe
2. **Migration scripts**: Self-contained - archive safe as unit

### Must NOT Archive (⚠️)
1. **Config files**: Required by Scribe ConfigManager
2. **Dist files**: Required by indexer, builder, linter, naming-enforcer
3. **Standards registry**: Core dependency for multiple tools
4. **AS-INDEX-KB-MASTER.md**: Referenced by archived migration scripts only

---

## Recommendations

### Immediate Actions Required: NONE
- All archived files had no active dependencies
- Archive operation completed safely

### Files to Keep in Current Location
1. **`tools/scribe/config/config.json`** - Required by Scribe ConfigManager (MOVED from root)
2. **`tools/scribe/config/config.schema.json`** - Required by Scribe ConfigManager (MOVED from root)
3. **`dist/standards_index.json`** - Required by 5 tools
4. **`standards/registry/*`** - Required by 5 tools
5. **`AS-INDEX-KB-MASTER.md`** - Safe to keep (only archived scripts reference it)

**UPDATE 2025-06-09 23:15**: Config files have been relocated from root to `tools/scribe/config/` for better organization.

### Architecture Notes
- Standards registry files serve as "Single Source of Truth" for multiple tools
- Moving these would require significant tool modifications
- Config files are hardcoded in Scribe core components
- Dist files are generated and consumed by the toolchain

---

## Archive Operation Summary

**Status**: ✅ **COMPLETED SUCCESSFULLY**
**Files Archived**: 4 scribe files + 1 migration scripts folder
**Tools Affected**: 0 (no active dependencies)
**Action Required**: None 