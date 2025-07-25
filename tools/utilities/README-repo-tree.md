---
title: Untitled Document
info-type: general
version: 0.0.1
date-created: '2025-06-17'
date-modified: '2025-06-17T02:29:16Z'
tags:
- content-type/general
- criticality/p0-critical
- kb-id/global
kb-id: tools
primary-topic: '[MISSING_PRIMARY_TOPIC]'
scope_application: '[MISSING_SCOPE_APPLICATION]'
criticality: P0-Critical
lifecycle_gatekeeper: Architect-Review
impact_areas: []
---
# Repository Tree Generator

**Script**: `generate_repository_tree.py`
**Output**: `repository-tree.md` (in repository root)
**Purpose**: Automated generation of repository structure overview with proper folder icons and annotations

---

## Features

### **🎯 Smart Folder Icons**
- **📁** Standard directories
- **📄** Files
- **⛔** System/ignored directories (`.vscode`, `.git`, etc.)
- **✅** Important directories with specific requirements
- **❌** Restricted directories with usage restrictions

### **📋 Automatic Annotations**
The script automatically adds contextual annotations to important directories:

| Directory | Icon | Annotation |
|-----------|------|------------|
| `archive` | ✅ | `ALWAYS ARCHIVE HERE` |
| `master-knowledge-base/archive` | ❌ | `NEVER ARCHIVE HERE (content must be moved to archive folder and this folder must be deleted)` |
| `registry` | ✅ | `REGISTRY FILES MUST ALWAYS BE HERE` |
| `src` | ✅ | `STANDARDS MUST ALWAYS BE HERE` |
| `templates` | ✅ | `TEMPLATES MUST ALWAYS BE HERE` |
| `tools` | ✅ | `ALL TOOLS AND SCRIPTS MUST ALWAYS BE HERE` |
| `reports` | ✅ | `ALL SCRIPT OUTPUTS, LOGS, AND REPORTS MUST ALWAYS BE HERE` |
| `test-environment` | ✅ | `ALWAYS TEST HERE` |
| `tests` (in tools) | ❌ | `NEVER TEST HERE (content must be moved to test-environment folder and this folder must be deleted)` |

### **🚫 Smart Filtering**
- **Excludes system directories**: `.git`, `__pycache__`, `.pytest_cache`, `node_modules`
- **Includes relevant files**: `.md`, `.py`, `.yaml`, `.json`, `.txt`, and other documentation/code files
- **Handles encoding issues**: Graceful fallback for Unicode display problems on Windows

---

## Usage

### **Method 1: Direct Script Execution**
```bash
python tools/utilities/generate_repository_tree.py
```

### **Method 2: Quick Runner (from root)**
```bash
python repo_tree.py
```

### **Output**
- **File**: `repo-tree.md` (automatically overwrites previous version)
- **Location**: Repository root directory
- **Format**: Markdown with code block containing tree structure

---

## Configuration

### **Customizing Folder Icons**
Edit the `folder_icons` dictionary in the script:

```python
self.folder_icons = {
    'your-folder': '🎯',  # Custom icon
    'special-dir': '⚡',  # Another custom icon
    # ... existing entries
}
```

### **Adding New Annotations**
Edit the `folder_annotations` dictionary:

```python
self.folder_annotations = {
    'your-folder': 'YOUR CUSTOM ANNOTATION HERE',
    # ... existing entries
}
```

### **Excluding Additional Directories**
Add to the `excluded_dirs` set:

```python
self.excluded_dirs = {
    '.git', '__pycache__', 'your-exclude-dir',
    # ... existing entries
}
```

### **Including Additional File Types**
Add to the `included_extensions` set:

```python
self.included_extensions = {
    '.md', '.py', '.your-extension',
    # ... existing entries
}
```

---

## Output Format

### **Header Information**
- Generation timestamp
- Script location reference
- Purpose description
- Icon legend

### **Tree Structure**
- Hierarchical folder/file listing
- Proper indentation using spaces
- Consistent icon application
- Alphabetical sorting within each directory level

### **Example Output Structure**
```
📁 master-knowledge-base
    ⛔ .vscode
        📄 settings.json
    📁 active-project
        📄 README.md
        📄 roadmap-template.md
    ✅ archive ALWAYS ARCHIVE HERE
        📁 legacy-content
    📁 master-knowledge-base
        ✅ registry REGISTRY FILES MUST ALWAYS BE HERE
            📄 mt-schema-frontmatter.yaml
        ✅ src STANDARDS MUST ALWAYS BE HERE
            📄 GM-CONVENTIONS-NAMING.md
```

---

## Technical Details

### **Path Handling**
- Cross-platform path resolution
- Relative path calculation from repository root
- Windows/Unix path separator normalization

### **Unicode Support**
- UTF-8 encoding with error handling
- Graceful fallback for display issues
- Windows terminal compatibility

### **Performance**
- Efficient directory traversal
- Sorted output for consistency
- Memory-conscious file processing

---

## Maintenance

### **Regular Updates**
Run the script whenever:
- New directories are added to the repository
- File structure changes significantly
- Directory purposes change requiring different annotations

### **Integration Options**
- Add to pre-commit hooks
- Include in CI/CD pipeline
- Schedule for automatic updates

### **Troubleshooting**
- **Unicode errors**: Script handles automatically with fallback
- **Permission errors**: Directories without read access are skipped
- **Missing folders**: Check `excluded_dirs` configuration

---

## Repository Standards Compliance

This script generates output that:
- ✅ Follows repository documentation standards
- ✅ Maintains consistent formatting
- ✅ Provides clear directory purpose indicators
- ✅ Supports audit trail requirements
- ✅ Enables quick repository structure understanding

---

**Last Updated**: Auto-generated with each script run
**Maintained By**: Repository Tree Generator Script
**Version**: 1.0
