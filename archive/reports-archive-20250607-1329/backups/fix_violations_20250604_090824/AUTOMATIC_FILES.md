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
# Automatic File Loading Documentation

## Overview

The naming enforcer now supports **automatic file loading** similar to `.gitignore`. The tool automatically looks for and loads `.namingignore` and `.naminginclude` files, making it easy to configure persistent include/exclude patterns without command line arguments.

## Automatic Files

### `.namingignore` File
- **Purpose**: Automatically loaded exclusion patterns
- **Behavior**: Works like `.gitignore` - patterns are automatically excluded
- **Location**: Current directory or scan directory
- **Precedence**: Combined with command line exclusions

### `.naminginclude` File  
- **Purpose**: Automatically loaded inclusion patterns
- **Behavior**: Limits processing to only matching patterns
- **Location**: Current directory or scan directory
- **Precedence**: Combined with command line inclusions

## File Loading Behavior

### Loading Order
1. **Initialization**: Load from current working directory
2. **Scan Directory**: If `--scan DIR` is specified and different from current directory, reload from scan directory
3. **Command Line**: Add patterns from command line arguments
4. **Final Patterns**: Combination of automatic files + command line options

### Loading Rules
- Files are loaded automatically if they exist
- No error if files don't exist
- Command line patterns are **added to** (not replaced by) automatic patterns
- Same precedence rules apply: **exclude takes precedence over include**

## File Format

Both `.namingignore` and `.naminginclude` use the same format as exclude/include list files:

```text
# Comments start with #
# Blank lines are ignored

# Specific files
script.py
config.json

# Directories (trailing slash optional)
src/
build
tests/

# Glob patterns (auto-detected by wildcards)
*.tmp
*.log
test_*

# Explicit glob patterns
glob:*.backup
glob:**/node_modules/**

# Regex patterns
regex:.*\.bak$
regex:^temp_.*\.json$

# Relative paths
./current-dir
../parent-dir
```

## Usage Examples

### Basic Setup

Create `.namingignore` in your project root:
```text
# .namingignore - Project exclusions
*.tmp
*.log
build/
dist/
__pycache__/
node_modules/
.git/
```

Create `.naminginclude` for focused processing:
```text
# .naminginclude - Only process these
*.py
*.js
*.md
src/
docs/
```

### Running with Automatic Files

```bash
# Files are automatically loaded
python naming_enforcer.py --scan .

# Combine with command line options
python naming_enforcer.py --scan . --exclude-file additional.txt

# Scan different directory (loads its automatic files)
python naming_enforcer.py --scan /other/project

# Show what was loaded
python naming_enforcer.py --show-inclusions --show-exclusions
```

## Common Patterns

### Development Environment `.namingignore`

```text
# .namingignore for development projects

# Build outputs
build/
dist/
out/
target/

# Dependencies
node_modules/
vendor/
.venv/
venv/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Logs and temp files
*.log
*.tmp
*.cache

# Version control
.git/
.svn/
.hg/

# Test files
*_test.py
test_*.py
*.test.js
__tests__/
```

### Documentation Focus `.naminginclude`

```text
# .naminginclude for documentation projects

# Documentation files
*.md
*.rst
*.txt

# Documentation directories
docs/
documentation/
guides/
tutorials/

# Configuration for docs
*.yaml
*.yml
*.json

# Root level important files
README*
LICENSE*
CHANGELOG*
CONTRIBUTING*
```

### Source Code Focus `.naminginclude`

```text
# .naminginclude for source code projects

# Source files
*.py
*.js
*.ts
*.jsx
*.tsx
*.java
*.cpp
*.c
*.h

# Source directories
src/
lib/
app/
components/

# Configuration
*.json
*.yaml
*.toml
```

## Advanced Usage

### Project-Specific Patterns

Different projects can have different automatic files:

```bash
# Web project
cd /projects/web-app
cat .naminginclude
# *.js *.css *.html *.jsx
# src/ public/ components/

# Python project  
cd /projects/python-lib
cat .naminginclude
# *.py *.md
# src/ docs/ tests/

# Documentation project
cd /projects/docs
cat .naminginclude  
# *.md *.rst
# docs/ guides/ tutorials/
```

### Hierarchical Configuration

You can have automatic files at different levels:

```
project-root/
├── .namingignore          # Project-wide exclusions
├── .naminginclude         # Project-wide inclusions
├── src/
│   ├── .namingignore      # Source-specific exclusions
│   └── components/
└── docs/
    └── .naminginclude     # Documentation-specific inclusions
```

When scanning `src/`, it will load `src/.namingignore` and `src/.naminginclude` if they exist.

### Temporary Overrides

```bash
# Ignore automatic files and use only command line
python naming_enforcer.py --scan /tmp/empty-dir --include-glob "*.py"

# Add to automatic patterns
python naming_enforcer.py --scan . --exclude-file temp-exclude.txt
```

## Integration with Existing Workflows

### CI/CD Pipeline

```yaml
# .github/workflows/naming-check.yml
- name: Check naming conventions
  run: |
    # .namingignore and .naminginclude are automatically loaded
    python tools/naming-enforcer/naming_enforcer.py --scan . --dry-run
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit
cd "$(git rev-parse --show-toplevel)"
python tools/naming-enforcer/naming_enforcer.py --scan . --dry-run
```

### Development Scripts

```bash
# check-naming.sh
#!/bin/bash
# Automatic files make this simple
python naming_enforcer.py --scan . --show-all
```

## Troubleshooting

### Common Issues

1. **Files not loaded**: Check file location and permissions
   ```bash
   # Debug: Show what's loaded
   python naming_enforcer.py --show-inclusions --show-exclusions
   ```

2. **Wrong directory**: Automatic files are loaded from scan directory
   ```bash
   # Load from current directory
   python naming_enforcer.py --scan .
   
   # Load from other directory
   python naming_enforcer.py --scan /other/project
   ```

3. **Pattern conflicts**: Remember exclude takes precedence
   ```bash
   # Check both patterns
   python naming_enforcer.py --show-inclusions --show-exclusions
   ```

### Debug Commands

```bash
# Show loaded patterns
python naming_enforcer.py --show-inclusions --show-exclusions

# Test with different directory
python naming_enforcer.py --scan /other/dir --show-inclusions

# Combine with command line to see total
python naming_enforcer.py --include-glob "*.test" --show-inclusions
```

## Best Practices

### 1. Start with Common Exclusions

Create a basic `.namingignore` with common patterns:
```text
# Basic .namingignore
*.tmp
*.log
*.bak
build/
dist/
__pycache__/
node_modules/
.git/
```

### 2. Use Includes for Focus

Create `.naminginclude` to focus on important files:
```text
# Focus on source and docs
*.py
*.js
*.md
src/
docs/
```

### 3. Document Your Patterns

```text
# .namingignore
# Project-specific exclusions for MyProject
# Updated: 2024-06-04

# Build outputs (generated by webpack)
build/
dist/

# Dependencies (managed by npm)
node_modules/

# IDE files (VS Code workspace)
.vscode/
```

### 4. Test Your Patterns

```bash
# Always test patterns before committing
python naming_enforcer.py --show-inclusions --show-exclusions

# Dry run to see what would be processed
python naming_enforcer.py --scan . --dry-run
```

### 5. Version Control

```bash
# Include automatic files in version control
git add .namingignore .naminginclude
git commit -m "Add naming enforcer automatic patterns"
```

## Migration from Command Line

### Before (Command Line Only)
```bash
python naming_enforcer.py --scan . \
  --exclude-dir build/ \
  --exclude-dir dist/ \
  --exclude-glob "*.tmp" \
  --exclude-glob "*.log" \
  --include-glob "*.py" \
  --include-glob "*.md"
```

### After (Automatic Files)
Create `.namingignore`:
```text
build/
dist/
*.tmp
*.log
```

Create `.naminginclude`:
```text
*.py
*.md
```

Run simply:
```bash
python naming_enforcer.py --scan .
```

## Summary

Automatic file loading provides:

- ✅ **Persistent configuration**: No need to remember command line arguments
- ✅ **Project-specific patterns**: Different patterns for different projects
- ✅ **Team consistency**: Shared patterns in version control
- ✅ **Simple usage**: Just run the tool, patterns are loaded automatically
- ✅ **Flexible combination**: Automatic files + command line options
- ✅ **Familiar syntax**: Works like `.gitignore`

Use automatic files to make the naming enforcer more convenient and consistent across your projects!
