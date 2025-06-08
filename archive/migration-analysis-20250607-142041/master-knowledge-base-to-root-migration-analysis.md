# Master Knowledge Base to Root Migration Analysis

**Generated**: 2025-01-27 (Analysis Date)  
**Purpose**: Comprehensive analysis of changes required to move `master-knowledge-base/` contents to repository root  
**Scope**: All files excluding `./archive/` folder  

---

## Executive Summary

Moving the contents of `📁 master-knowledge-base` to the root directory requires updating **hundreds of path references** across the entire repository. This analysis identifies all files that contain hardcoded paths, relative references, and configuration settings that must be modified.

---

## Required Changes by File

### **Root Directory Files**

**repo_tree.py** → Update script path reference
- Line 18: `script_path = Path("tools/utilities/repo-tree/main_repo_tree.py")` → `script_path = Path("tools/utilities/repo-tree/main_repo_tree.py")`

**repo-tree.md** → Update script path references  
- Line 3: `**Script**: tools/utilities/repo-tree/main_repo_tree.py` → `**Script**: tools/utilities/repo-tree/main_repo_tree.py`
- Line 241: `**Configuration Location**: tools/utilities/repo-tree/` → `**Configuration Location**: tools/utilities/repo-tree/`

**README.md** → Update all directory structure references
- Line 12: `master-knowledge-base/` → Remove prefix
- Line 42: `standards/src/` → `standards/src/`
- Line 45: `tools/` → `tools/`
- Line 49: `standards/src/` → `standards/src/`
- Line 50: `standards/registry/` → `standards/registry/`
- Line 51: `tools/` → `tools/`

### **Active Project Directory**

**active-project/README.md** → Update template links and references
- Line 148: `standards/templates/` → `standards/templates/`
- Line 150: `../standards/templates/analysis-report-template.md` → `../standards/templates/analysis-report-template.md`
- Line 151: `../standards/templates/roadmap-template.md` → `../standards/templates/roadmap-template.md`
- Line 152: `../standards/templates/tpl-canonical-frontmatter.md` → `../standards/templates/tpl-canonical-frontmatter.md`
- Line 158: `standards/templates/` → `standards/templates/`

**active-project/current-state.md** → Update path references
- Line 65: `/standards/src/`, `/tools/`, `/dist/collections/` → Remove `/master-knowledge-base` prefix
- Line 69: `standards/src/OM-AUTOMATION-LLM-IO-SCHEMAS.MD` → `standards/src/OM-AUTOMATION-LLM-IO-SCHEMAS.MD`

**active-project/project-guidelines/project-reminders.md** → Update standards references
- Line 56: `standards/src/` → `standards/src/`
- Line 65: `standards/src/` → `standards/src/`

**active-project/-refactoring-initiative-completed/master-roadmap.md** → Update all path references (53+ instances)
- All instances of `/standards/` → `/standards/`
- All instances of `/tools/` → `/tools/`
- All instances of `standards/` → `standards/`

### **Tools Directory**

**tools/utilities/repo-tree/main_repo_tree.py** → Update configuration location references
- Line 351: `tools/utilities/repo-tree/` → `tools/utilities/repo-tree/`
- Line 356: `tools/utilities/repo-tree/main_repo_tree.py` → `tools/utilities/repo-tree/main_repo_tree.py`

**tools/utilities/repo-tree/.treeicon** → Update all icon mappings
- Lines 19-29: All `master-knowledge-base/` prefixes → Remove prefix

**tools/utilities/repo-tree/.treeaddtext** → Update all text annotations
- Lines 9-19: All `master-knowledge-base/` prefixes → Remove prefix

**tools/utilities/repo-tree/.subtreeignore** → Update ignore patterns
- Lines 8, 11-13: All `master-knowledge-base/` prefixes → Remove prefix

**tools/utilities/README-repository-tree-generator.md** → Update example paths
- Line 23: `master-knowledge-base/archive` → `archive`
- Line 43: `python tools/utilities/generate_repository_tree.py` → `python tools/utilities/generate_repository_tree.py`

**tools/refactoring-scripts/refactor_ids_filenames.py** → Update example commands
- Line 258: `python tools/refactor_ids_filenames.py standards/src` → `python tools/refactoring-scripts/refactor_ids_filenames.py standards/src`
- Line 259: Similar update for second example

**tools/naming-enforcer/.naminginclude** → Update include patterns
- Lines 7, 12, 18, 30: All commented `master-knowledge-base/` references → Remove prefix

**tools/naming-enforcer/.namingignore** → Update ignore patterns
- Lines 16-18, 69-70: All `tools/reports/` → `tools/reports/`

**tools/naming-enforcer/naming_enforcer.py** → Update relative path calculations
- Lines 410, 463, 503, 561, 880: `script_dir.parent.parent.parent` logic needs adjustment
- Line 955: `/tools/` path check logic

**tools/naming-enforcer/generate_naming_configs.py** → Update relative path
- Line 110: `Path("../../standards/src/GM-CONVENTIONS-NAMING.md")` → `Path("../standards/src/GM-CONVENTIONS-NAMING.md")`

**tools/linter/kb_linter.py** → Update all path detection logic
- Lines 63-64: Master-knowledge-base detection logic
- Lines 208, 244-247: Template and tool file detection
- Lines 532-533: Default directory argument
- Lines 559-560, 605-606: Path prefix handling
- Lines 453-454: Reports directory detection

**tools/file-format-utils/add_readme_frontmatter.py** → Update target file paths
- Lines 9-14: All `master-knowledge-base/` prefixes → Remove prefix
- Line 66: Update directory level logic

**tools/frontmatter-management/generate_schema_docs.py** → Update sys.path logic
- Line 21: Verify tools_dir path calculation

**tools/builder/generate_collections.py** → Update default paths
- Line 253: `dist/standards_index.json` → `dist/standards_index.json`
- Line 254: `tools/builder/collection_definitions.yaml` → `tools/builder/collection_definitions.yaml`
- Line 255: `dist/collections` → `dist/collections`

**tools/changelog.md** → Update scope references
- Line 21: `tools/` → `tools/`
- Lines 90-95: All `tools/` → `tools/`

### **Standards Directory**

**standards/templates/UA-TPL-CANONICAL-FRONTMATTER.md** → Update changelog reference
- Line 21: `"../changelog.md"` comment needs clarification for new structure

**standards/templates/UA-TPL-CHANGELOG-DOCUMENT.md** → Update example paths
- Line 31: `standards/changelog.md` → `standards/changelog.md`
- Line 32: `tools/changelog.md` → `tools/changelog.md`

**standards/src/** (Multiple files) → Update path references in content
- **OM-POLICY-STANDARDS-DEPRECATION.md**: Line 63 archive location
- **OM-OVERVIEW-PUBLISHING-PIPELINE.md**: Line 60 input path
- **OM-AUTOMATION-LLM-IO-SCHEMAS.md**: Line 64 schema directory
- **MT-KEYREF-MANAGEMENT.md**: Line 77 example file path
- **GM-REGISTRY-GOVERNANCE.md**: Line 34 registry location
- **GM-MANDATE-STANDARDS-GLOSSARY.md**: Line 39 glossary location
- **GM-MANDATE-KB-USAGE-GUIDE.md**: Line 38 guide location
- **GM-GUIDE-KB-USAGE.md**: Line 93 source documents path
- **GM-GUIDE-STANDARDS-BY-TASK.md**: Line 641 replacement reference
- **GM-CONVENTIONS-NAMING.md**: Line 54 auto-generation reference
- **CS-TOC-POLICY.md**: Line 51 atomic standards location
- **AS-STRUCTURE-TEMPLATES-DIRECTORY.md**: Lines 42, 47, 60, 76 template directory paths
- **AS-SCHEMA-RELTABLE-DEFINITION.md**: Lines 62, 66, 68, 102, 104 example paths
- **AS-MAP-STANDARDS-KB.md**: Line 45 standards directory reference
- **AS-KB-DIRECTORY-STRUCTURE.md**: Lines 40, 42, 47, 52 directory structure definitions

**standards/changelog.md** → Update scope reference
- Line 20: `standards/` → `standards/`

### **Generated Files (Require Regeneration)**

**dist/standards_index.json** → Complete regeneration required
- Lines 5-1153: All 80+ `"filepath": "standards/src/..."` entries → Remove `master-knowledge-base/` prefix

**dist/collections/** → All collection files require regeneration
- **collection-content-policies.md**: Line 976 and other path references
- **collection-architecture-structure.md**: Lines 43, 76, 78, 83, 88, 121, 613, 1129, 1134, 1147, 1163

**AS-INDEX-KB-MASTER.md** → Update primary folder reference
- Line 32: `/standards/` → `/standards/`

### **Other Files**

**refactoring-initiative-remaining-tasks.md** → Update directory references
- Line 28: `standards/registry/` (already correct)
- Line 61: `standards/src/` (already correct)

---

## Summary by Change Type

### **Direct Path Updates** (Remove `master-knowledge-base/` prefix)
- **Root files**: 3 files
- **Active project**: 4 files  
- **Tools**: 15 files
- **Standards**: 20+ files
- **Generated files**: 5+ files

### **Relative Path Updates** (Adjust `../` references)
- **active-project/README.md**: 3 template links
- **tools/naming-enforcer/generate_naming_configs.py**: 1 relative path
- **standards/templates/UA-TPL-CANONICAL-FRONTMATTER.md**: 1 changelog reference

### **Python Logic Updates** (Path calculation changes)
- **tools/naming-enforcer/naming_enforcer.py**: Parent directory traversal logic
- **tools/linter/kb_linter.py**: Repository base detection and path handling
- **tools/frontmatter-management/generate_schema_docs.py**: sys.path modifications

### **Configuration Updates** (Tool configuration files)
- **tools/utilities/repo-tree/**: 4 configuration files
- **tools/naming-enforcer/**: 2 configuration files

### **Complete Regeneration Required**
- **dist/standards_index.json**: 80+ filepath entries
- **dist/collections/**: All collection files
- **repo-tree.md**: Generated repository structure

---

## Migration Complexity Assessment

**HIGH COMPLEXITY**: This migration affects **100+ files** with **300+ individual path references**. The changes span:

1. **Hardcoded paths** in documentation and configuration
2. **Python script logic** for path detection and traversal  
3. **Generated files** requiring complete regeneration
4. **Relative path relationships** between directories
5. **Tool configuration** files with path patterns

**RECOMMENDATION**: Implement this migration with extreme caution using automated scripts with comprehensive dry-run testing and backup procedures. 