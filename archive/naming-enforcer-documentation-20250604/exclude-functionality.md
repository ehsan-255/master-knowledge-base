---
title: Untitled Document
info-type: general
version: 0.0.1
date-created: '2025-06-17'
date-modified: '2025-06-17T02:29:14Z'
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
# Naming Enforcer Exclude Functionality

## Overview

The Naming Enforcer now supports comprehensive exclude functionality that allows you to exclude files, directories, and patterns from both dry-run and live-run operations. This feature provides flexible ways to specify what should be ignored during naming convention enforcement.

## Command Line Options

### Individual Exclusions

#### `--exclude-file FILE`
Exclude a specific file from processing.
- Can be used multiple times to exclude multiple files
- Supports both absolute and relative paths
- Files are resolved to absolute paths internally

```bash
python naming_enforcer.py --scan . --exclude-file temp.txt
python naming_enforcer.py --scan . --exclude-file temp.txt --exclude-file backup.md
```

#### `--exclude-dir DIR`
Exclude a specific directory and all its contents from processing.
- Can be used multiple times to exclude multiple directories
- Supports both absolute and relative paths
- Directories are resolved to absolute paths internally

```bash
python naming_enforcer.py --scan . --exclude-dir build/
python naming_enforcer.py --scan . --exclude-dir build/ --exclude-dir dist/
```

#### `--exclude-glob PATTERN`
Exclude files/directories matching a glob pattern.
- Can be used multiple times for multiple patterns
- Supports standard glob wildcards: `*`, `?`, `[...]`
- Patterns are matched against filenames, relative paths, and absolute paths

```bash
python naming_enforcer.py --scan . --exclude-glob "*.tmp"
python naming_enforcer.py --scan . --exclude-glob "*.tmp" --exclude-glob "test_*"
```

#### `--exclude-regex PATTERN`
Exclude files/directories matching a regular expression pattern.
- Can be used multiple times for multiple patterns
- Patterns are matched against filenames, relative paths, and absolute paths
- Uses Python regex syntax

```bash
python naming_enforcer.py --scan . --exclude-regex ".*\.backup$"
python naming_enforcer.py --scan . --exclude-regex ".*\.backup$" --exclude-regex "^temp_.*"
```

### Bulk Exclusions

#### `--exclude-list FILE`
Load exclusions from a file (one pattern per line).
- Each line in the file represents one exclusion pattern
- Comments (lines starting with `#`) are ignored
- Empty lines are ignored
- Supports all pattern types in a single file

```bash
python naming_enforcer.py --scan . --exclude-list excludes.txt
```

### Utility Options

#### `--show-exclusions`
Display a summary of all configured exclusions without running the scan.

```bash
python naming_enforcer.py --show-exclusions --exclude-file temp.txt --exclude-glob "*.tmp"
```

## Exclude File Format

When using `--exclude-list`, the file format supports multiple pattern types:

```
# Example exclude file
# Lines starting with # are comments

# Specific files
temp.txt
backup.md

# Directories (trailing slash optional)
build/
dist
__pycache__

# Glob patterns (auto-detected by wildcards)
*.tmp
*.backup
test_*
*_temp.py

# Explicit glob patterns
glob:*.log
glob:**/node_modules/**

# Regex patterns
regex:.*\.bak$
regex:^temp_.*\.json$

# Relative paths
./temp-files/
../backup-folder/
```

### Pattern Type Detection

The exclude file loader automatically detects pattern types:

1. **Regex patterns**: Lines starting with `regex:`
2. **Explicit glob patterns**: Lines starting with `glob:`
3. **Auto-detected glob patterns**: Lines containing `*`, `?`, or `[`
4. **File/directory paths**: Everything else
   - Absolute paths or paths starting with `./` or `../` are treated as specific paths
   - Other patterns are treated as glob patterns

## Exclusion Logic

### Precedence
Exclusions are checked in the following order:
1. Built-in exceptions (from the naming standard)
2. User-defined exclusions (all types combined)

### Matching Behavior
For each path being processed, the exclude manager checks:

1. **Exact file matches**: Direct comparison with excluded file paths
2. **Directory containment**: Whether the path is within any excluded directory
3. **Glob pattern matching**: Against filename, relative path, and absolute path
4. **Regex pattern matching**: Against filename, relative path, and absolute path

### Path Resolution
- File and directory exclusions are resolved to absolute paths for consistent matching
- Glob and regex patterns work with both relative and absolute path representations
- This ensures exclusions work regardless of how the scan is invoked

## Examples

### Basic Usage

```bash
# Exclude specific files
python naming_enforcer.py --scan . --exclude-file temp.txt --exclude-file backup.md

# Exclude directories
python naming_enforcer.py --scan . --exclude-dir build/ --exclude-dir __pycache__/

# Exclude patterns
python naming_enforcer.py --scan . --exclude-glob "*.tmp" --exclude-glob "test_*"

# Exclude with regex
python naming_enforcer.py --scan . --exclude-regex ".*_backup\.py$"
```

### Combined Usage

```bash
# Mix different exclusion types
python naming_enforcer.py --scan . \
  --exclude-file temp.txt \
  --exclude-dir build/ \
  --exclude-glob "*.tmp" \
  --exclude-regex ".*_test\.py$"
```

### Using Exclude Files

```bash
# Load exclusions from file
python naming_enforcer.py --scan . --exclude-list my-excludes.txt

# Combine file exclusions with command-line exclusions
python naming_enforcer.py --scan . \
  --exclude-list my-excludes.txt \
  --exclude-file additional-temp.txt
```

### Dry Run with Exclusions

```bash
# See what would be processed with exclusions
python naming_enforcer.py --scan . --dry-run \
  --exclude-dir build/ \
  --exclude-glob "*.tmp"
```

### Show Exclusion Summary

```bash
# Display configured exclusions
python naming_enforcer.py --show-exclusions \
  --exclude-file temp.txt \
  --exclude-dir build/ \
  --exclude-glob "*.tmp"
```

## Integration with Existing Features

### Compatibility
- Exclusions work with all existing naming enforcer features
- Compatible with `--fix`, `--dry-run`, `--show-all` options
- Exclusions are applied during both scanning and content reference updates

### Built-in Exceptions
- User-defined exclusions work alongside built-in exceptions from the naming standard
- Both types of exclusions are respected during processing
- The exclusion summary shows only user-defined exclusions

### Backup and Safety
- Excluded files are not included in backups (since they're not processed)
- Exclusions are logged in operation logs for audit purposes
- Exclusions are shown in violation reports when configured

## Error Handling

### Invalid Patterns
- Invalid regex patterns are reported as warnings and skipped
- Invalid file paths are reported as warnings and skipped
- Processing continues with valid exclusions

### Missing Exclude Files
- Missing exclude list files result in an error and program termination
- This ensures exclude configurations are explicit and intentional

### Path Resolution Issues
- Paths that cannot be resolved are reported as warnings
- Processing continues with successfully resolved exclusions

## Performance Considerations

### Efficiency
- File and directory exclusions use set-based lookups for O(1) performance
- Glob patterns are checked using optimized `fnmatch` operations
- Regex patterns are pre-compiled for efficient matching

### Memory Usage
- Exclusion patterns are stored efficiently in memory
- Large exclude lists are supported without significant memory overhead
- Path resolution is done once during configuration, not during each check

## Best Practices

### Exclude File Organization
```
# Group related exclusions
# Build artifacts
build/
dist/
*.pyc
__pycache__/

# Temporary files
*.tmp
*.backup
temp_*

# Test files
regex:.*_test\.py$
test_*/

# IDE files
.vscode/
.idea/
```

### Performance Optimization
- Use directory exclusions for large directory trees
- Prefer glob patterns over regex when possible
- Group related exclusions in exclude files for maintainability

### Maintenance
- Document exclusion reasons in exclude files using comments
- Review exclusions periodically to ensure they're still needed
- Use `--show-exclusions` to verify current exclusion configuration

## Troubleshooting

### Common Issues

1. **Exclusions not working**: Verify paths are correct and patterns are valid
2. **Performance issues**: Check for overly broad regex patterns
3. **Unexpected exclusions**: Use `--show-exclusions` to verify configuration

### Debugging
```bash
# Show what exclusions are configured
python naming_enforcer.py --show-exclusions --exclude-list my-excludes.txt

# Test exclusions without running full scan
python naming_enforcer.py --scan . --dry-run --exclude-list my-excludes.txt
```
