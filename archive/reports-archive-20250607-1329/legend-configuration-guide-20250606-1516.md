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
# Repository Tree Legend Configuration Guide

**Generated**: 2025-01-06 15:16:00  
**System**: Repository Tree Generator  
**Configuration File**: `.treelegend`  

---

## 🔧 Legend Configuration Methods

### **Method 1: Configuration File (Recommended)**

Edit `master-knowledge-base/tools/utilities/repo-tree/.treelegend`:

```
# .treelegend - Legend descriptions for icons
# Format: icon|description
# Only icons actually used in .treeicon will appear in the legend

# Basic icons (always shown)
📁|Standard Directory
📄|File

# Your custom icons here:
🚀|Deployment Directory
🧪|Testing Directory
📦|Package Directory
🌐|Web Assets Directory
🗄️|Database Directory
```

### **Method 2: Edit Icons in Use**

Add/remove icons from `.treeicon` to control which appear in legend:

```
# .treeicon
your-new-folder|🚀
deployment|🚀
tests|🧪
packages|📦
```

### **Method 3: Script Modification (Not Recommended)**

Edit the fallback `icon_descriptions` dictionary in `main_repo_tree.py` (lines 138-154).

---

## 📊 Current Legend Icons

| Icon | Description | Usage |
|------|-------------|-------|
| 📁 | Standard Directory | Always shown |
| 📄 | File | Always shown |
| ⛔ | System/Ignored Directory | System folders |
| ✅ | Important Directory (with specific requirements) | Critical directories |
| ❌ | Restricted Directory (with usage restrictions) | Restricted access |
| 🔧 | Tools/Build Directory | Development tools |
| 📋 | Documentation/Standards Directory | Documentation |
| 🎯 | Project Management Directory | Project control |
| 📇 | Indexing Directory | Index management |
| 🔍 | Linting/Validation Directory | Code quality |
| 🔄 | Refactoring Directory | Code improvements |
| 🏗️ | Building Directory | Build processes |
| 📊 | Registry/Data Directory | Data management |
| 📝 | Source/Content Directory | Source code |
| 📚 | Documentation Directory | General docs |
| 💡 | Examples/Samples Directory | Examples |
| 💾 | Backup Directory | Backups |
| 🗂️ | Temporary Directory | Temporary files |

---

## 🎨 Adding Custom Icons

### **Step 1: Add Icon to .treelegend**

```
🚀|Deployment Directory
🧪|Testing Laboratory  
📦|Package Distribution
🌐|Web Resources
🗄️|Database Storage
🔐|Security Module
🌟|Featured Content
```

### **Step 2: Use Icon in .treeicon**

```
deployment|🚀
lab|🧪
dist|📦
web|🌐
database|🗄️
security|🔐
featured|🌟
```

### **Step 3: Regenerate Tree**

```bash
cd master-knowledge-base/tools/utilities/repo-tree
python main_repo_tree.py
```

---

## 🔄 Dynamic Legend Generation

**Features:**
- ✅ **Automatic**: Only shows icons actually used
- ✅ **Configuration-driven**: Uses `.treelegend` file
- ✅ **Fallback protection**: Has default descriptions
- ✅ **Sorted display**: Icons appear in sorted order
- ✅ **Unicode safe**: Handles encoding errors gracefully

**Process:**
1. Script scans `.treeicon` for used icons
2. Loads descriptions from `.treelegend`
3. Matches used icons with descriptions
4. Generates sorted legend automatically

---

## 🛠️ Icon Selection Guidelines

### **Recommended Icon Categories:**

| Category | Icons | Usage |
|----------|-------|-------|
| **System** | ⛔ 🔧 🔐 | Administrative |
| **Status** | ✅ ❌ ⚠️ 🟢 🔴 | Conditional |
| **Content** | 📝 📋 📄 📊 📚 | Documentation |
| **Development** | 🔍 🔄 🏗️ 🧪 | Process |
| **Data** | 🗄️ 💾 📦 📇 | Storage |
| **Navigation** | 📁 🎯 🗂️ 💡 | Organization |

### **Icon Best Practices:**
- **Consistency**: Use similar icons for similar functions
- **Clarity**: Choose recognizable symbols
- **Contrast**: Ensure icons are visually distinct
- **Limit variety**: Don't exceed ~20 different icons
- **Unicode compatibility**: Test on different systems

---

## 📋 Configuration File Format

```
# .treelegend
# Lines starting with # are comments
# Format: icon|description
# Spaces around | are trimmed

📁|Standard Directory         # Basic folder
🔧|Tools Directory           # Development tools  
📊|Data Registry            # Data management
🚀|Deploy System           # Deployment related

# Group related icons together
⛔|Ignored
❌|Restricted  
✅|Important
```

---

## 🔍 Troubleshooting

### **Icon Not Appearing in Legend**
1. Check if icon exists in `.treeicon`
2. Verify icon has description in `.treelegend`
3. Ensure correct format: `icon|description`
4. Regenerate tree after changes

### **Wrong Description**
1. Edit `.treelegend` file
2. Update the line: `icon|new description`
3. Regenerate tree

### **Missing Legend File**
- Script will use built-in defaults
- Create `.treelegend` in `repo-tree/` folder
- Copy format from this guide

### **Unicode Issues**
- Use UTF-8 encoding for `.treelegend`
- Test icons in your terminal
- Script has fallback handling

---

## 📈 Legend Maintenance

### **Regular Updates:**
- Review icon usage quarterly
- Remove unused icon descriptions
- Add descriptions for new icons
- Maintain consistency across projects

### **Version Control:**
- Commit `.treelegend` changes
- Document icon meaning changes
- Coordinate with team on icon standards

**Configuration Location**: `master-knowledge-base/tools/utilities/repo-tree/.treelegend`  
**Last Updated**: 2025-01-06 15:16:00
