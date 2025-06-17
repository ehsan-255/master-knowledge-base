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
# Include Functionality Documentation

## Overview

The naming enforcer now supports comprehensive **include functionality** that allows you to specify exactly which files and directories should be processed. This works alongside the existing exclude functionality with clear precedence rules.

## Key Concepts

### Include vs Exclude Precedence
- **Exclude takes precedence over include**: If a file is both included and excluded, it will be excluded
- **Include patterns limit scope**: Only files matching include patterns will be processed
- **Default behavior**: If no include patterns are specified, all files are processed (except those explicitly excluded)

### Pattern Processing Order
1. Check if file matches any **include** patterns → if NO include patterns exist, include by default
2. Check if file matches any **exclude** patterns → if YES, exclude (takes precedence)
3. Final decision: Process only if included AND not excluded

## Command Line Options

### Individual Include Options

| Option | Description | Example |
|--------|-------------|---------|
| `--include-file FILE` | Include specific file (repeatable) | `--include-file script.py` |
| `--include-dir DIR` | Include specific directory (repeatable) | `--include-dir src/` |
| `--include-glob PATTERN` | Include glob patterns (repeatable) | `--include-glob "*.py"` |
| `--include-regex PATTERN` | Include regex patterns (repeatable) | `--include-regex ".*\.py$"` |
| `--include-list FILE` | Load inclusions from file | `--include-list includes.txt` |
| `--show-inclusions` | Display inclusion summary | `--show-inclusions` |

### Combining Include Options

All include options can be combined and used multiple times:

```bash
# Include multiple files and patterns
python naming_enforcer.py --scan . \
  --include-file important.py \
  --include-dir src/ \
  --include-glob "*.py" \
  --include-regex ".*_config\.json$"
```

## Include File Format

The include file format is identical to the exclude file format:

```text
# Include file example (includes.txt)
# Lines starting with # are comments

# Specific files
important_script.py
config.json

# Directories (trailing slash optional)
src/
docs
tests/

# Glob patterns (auto-detected by wildcards)
*.py
*.md
example-*

# Explicit glob patterns
glob:*.txt
glob:**/src/**

# Regex patterns
regex:.*\.py$
regex:^config.*\.json$

# Relative paths
./current_dir
../parent_dir
```

## Usage Examples

### Basic Include Operations

```bash
# Include only Python files
python naming_enforcer.py --scan . --include-glob "*.py"

# Include specific directories
python naming_enforcer.py --scan . --include-dir src/ --include-dir docs/

# Include from file list
python naming_enforcer.py --scan . --include-list my-includes.txt

# Show what would be included
python naming_enforcer.py --show-inclusions --include-glob "*.py"
```

### Advanced Include + Exclude Combinations

```bash
# Include all Python files but exclude test files
python naming_enforcer.py --scan . \
  --include-glob "*.py" \
  --exclude-glob "*test*"

# Include src directory but exclude specific files
python naming_enforcer.py --scan . \
  --include-dir src/ \
  --exclude-file src/legacy.py \
  --exclude-file src/deprecated.py

# Include documentation but exclude drafts
python naming_enforcer.py --scan . \
  --include-glob "*.md" \
  --exclude-dir drafts/
```

### Dry Run with Inclusions

```bash
# Preview what would be processed
python naming_enforcer.py --scan . --dry-run \
  --include-glob "*.py" \
  --exclude-glob "*_test.py"
```

## Precedence Examples

### Example 1: File Both Included and Excluded

```bash
# This file will be EXCLUDED (exclude wins)
python naming_enforcer.py --scan . \
  --include-file script.py \
  --exclude-file script.py
```

**Result**: `script.py` is excluded because exclude takes precedence.

### Example 2: Subdomain Exclusion

```bash
# Include all Python files but exclude test files
python naming_enforcer.py --scan . \
  --include-glob "*.py" \
  --exclude-glob "*test*.py"
```

**Result**: 
- ✅ `main.py` → included (matches include, no exclude)
- ✅ `utils.py` → included (matches include, no exclude)  
- ❌ `test_main.py` → excluded (matches include but also matches exclude)
- ❌ `main_test.py` → excluded (matches include but also matches exclude)

### Example 3: Directory with File Exclusions

```bash
# Include src directory but exclude specific files
python naming_enforcer.py --scan . \
  --include-dir src/ \
  --exclude-file src/legacy.py
```

**Result**:
- ✅ `src/main.py` → included (in included directory, not excluded)
- ✅ `src/utils.py` → included (in included directory, not excluded)
- ❌ `src/legacy.py` → excluded (in included directory but specifically excluded)
- ❌ `docs/readme.md` → excluded (not in included directory)

## Performance Considerations

### Efficient Include Patterns

1. **Use specific patterns**: `--include-dir src/` is more efficient than `--include-glob "src/**"`
2. **Combine patterns wisely**: Multiple specific includes are better than broad includes with many excludes
3. **File-based patterns**: Use `--include-list` for complex pattern sets

### Pattern Optimization

```bash
# EFFICIENT: Specific directory inclusion
python naming_enforcer.py --scan . --include-dir src/

# LESS EFFICIENT: Broad inclusion with many exclusions  
python naming_enforcer.py --scan . \
  --include-glob "*" \
  --exclude-dir build/ \
  --exclude-dir dist/ \
  --exclude-dir node_modules/ \
  # ... many more excludes
```

## Troubleshooting

### Common Issues

1. **No files processed**: Check if include patterns are too restrictive
   ```bash
   # Debug: Show what's included
   python naming_enforcer.py --show-inclusions --include-glob "*.py"
   ```

2. **Unexpected exclusions**: Remember exclude takes precedence
   ```bash
   # Check both include and exclude patterns
   python naming_enforcer.py --show-inclusions --show-exclusions \
     --include-glob "*.py" --exclude-glob "*test*"
   ```

3. **Pattern not matching**: Test patterns with simple commands
   ```bash
   # Test glob pattern
   ls *.py
   
   # Test directory inclusion
   python naming_enforcer.py --show-inclusions --include-dir src/
   ```

### Debug Commands

```bash
# Show inclusion summary
python naming_enforcer.py --show-inclusions --include-list includes.txt

# Show both inclusion and exclusion summaries
python naming_enforcer.py --show-inclusions --show-exclusions \
  --include-glob "*.py" --exclude-glob "*test*"

# Dry run to see what would be processed
python naming_enforcer.py --scan . --dry-run \
  --include-dir src/ --exclude-file src/legacy.py
```

## Best Practices

### 1. Start with Broad Includes, Refine with Excludes

```bash
# Good approach
python naming_enforcer.py --scan . \
  --include-glob "*.py" \
  --exclude-glob "*test*" \
  --exclude-dir __pycache__/
```

### 2. Use Include Lists for Complex Scenarios

Create `project-includes.txt`:
```text
src/
docs/
*.py
*.md
config/
!temp/
!*.tmp
```

```bash
python naming_enforcer.py --scan . --include-list project-includes.txt
```

### 3. Test Patterns Before Live Runs

```bash
# Always test first
python naming_enforcer.py --show-inclusions --include-list my-patterns.txt

# Then dry run
python naming_enforcer.py --scan . --dry-run --include-list my-patterns.txt

# Finally live run
python naming_enforcer.py --scan . --fix --include-list my-patterns.txt
```

### 4. Document Your Include Patterns

```text
# project-includes.txt
# Project-specific include patterns for naming enforcer
# Updated: 2024-06-04
# Purpose: Process only source code and documentation

# Source code
src/
lib/
*.py
*.js

# Documentation  
docs/
*.md
*.rst

# Configuration
config/
*.json
*.yaml
```

## Integration with Existing Workflows

### CI/CD Pipeline Example

```bash
# Check only source files in CI
python naming_enforcer.py --scan . \
  --include-dir src/ \
  --include-dir lib/ \
  --exclude-dir tests/ \
  --dry-run
```

### Development Workflow

```bash
# Quick check of current changes
python naming_enforcer.py --scan . \
  --include-glob "*.py" \
  --exclude-dir __pycache__/ \
  --exclude-glob "*.pyc"
```

---

## Summary

The include functionality provides powerful control over which files the naming enforcer processes:

- ✅ **Flexible patterns**: Files, directories, globs, and regex
- ✅ **Clear precedence**: Exclude always wins over include  
- ✅ **Efficient processing**: Only scan what you need
- ✅ **Easy debugging**: `--show-inclusions` for verification
- ✅ **Seamless integration**: Works with all existing features

Use includes to focus the naming enforcer on exactly the files that matter for your project!
