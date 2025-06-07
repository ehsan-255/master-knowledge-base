# Knowledge Base Tools

This directory contains automation tools for managing the knowledge base, including naming conventions, date/time management, TODO tracking, and content validation.

## Tools Overview

### 🔧 Core Tools

| Tool | Purpose | Usage |
|------|---------|-------|
| **date_time_manager.py** | Manage frontmatter date fields | `python date_time_manager.py scan` |
| **todo_tracker.py** | Track and report TODO items | `python todo_tracker.py scan` |
| **linter/kb_linter.py** | Validate content and formatting | `python kb_linter.py --directory .` |
| **naming_exceptions.json** | Configure naming convention exceptions | Edit configuration file |

### 📁 Directory Structure

```
tools/
├── README.md                          # This file
├── naming_exceptions.json             # Naming convention exceptions
├── todo_tracker.py                    # TODO tracking and reporting
├── frontmatter-management/
│   └── date_time_manager.py          # Date/time field management
├── linter/
│   └── kb_linter.py                  # Content validation
└── [other tools...]
```

## 🕐 Date/Time Management

### Quick Start

```bash
# Update all files with file system timestamps
python frontmatter-management/date_time_manager.py scan

# Update specific files with manual date
python frontmatter-management/date_time_manager.py update file1.md file2.md --date 2025-01-11

# Update with time included (for commits)
python frontmatter-management/date_time_manager.py update file.md --time

# Lock dates to prevent automatic updates
python frontmatter-management/date_time_manager.py lock file.md

# Update only files with real changes (commit mode)
python frontmatter-management/date_time_manager.py commit-update --time
```

### How It Works

**Date Fields**: Only 2 fields maintained:
- `date-created`: From file system `ctime` (creation time)
- `date-modified`: From file system `mtime` (modification time)

**Date Formats**:
- **Simple**: `YYYY-MM-DD` (e.g., `2025-01-11`)
- **With Time**: `YYYY-MM-DD-HH-MM` (e.g., `2025-01-11-14-30`)

**Locking Mechanism**:
- Add `# date-locked` marker to prevent automatic updates
- Use `--force` flag to override locks

**Real Change Detection**:
- Git integration detects content vs. formatting changes
- Only updates timestamps for actual content modifications
- Ignores CRLF/LF changes, whitespace, etc.

### Commands

| Command | Description | Example |
|---------|-------------|---------|
| `scan` | Update all markdown files in directory | `scan --directory . --time` |
| `update` | Update specific files | `update file1.md --date 2025-01-11` |
| `commit-update` | Update files with real changes only | `commit-update --time` |
| `lock` | Lock dates to prevent updates | `lock file1.md file2.md` |
| `unlock` | Remove date locks | `unlock file1.md` |

## 📋 TODO Tracking

### Quick Start

```bash
# Scan for TODOs and show console report
python todo_tracker.py scan

# Generate markdown report
python todo_tracker.py report --format markdown --output todo-report.md

# Get TODO statistics
python todo_tracker.py stats
```

### TODO Format

Use Obsidian-compatible callout syntax:

```markdown
> [!TODO] This needs to be implemented

> [!TODO] Fix the validation logic here
```

### How It Works

**Automatic Collection**:
- Scans all `.md` files recursively
- Extracts file path, line number, content
- Captures context lines before/after
- Generates detailed reports

**Output Formats**:
- **Console**: Quick summary with file counts
- **Markdown**: Detailed report with context
- **JSON**: Machine-readable data for automation

### Commands

| Command | Description | Example |
|---------|-------------|---------|
| `scan` | Scan directory and save to JSON | `scan --output todos.json` |
| `report` | Generate formatted report | `report --format markdown` |
| `stats` | Show TODO statistics | `stats --input todos.json` |

## 📝 Naming Conventions

### Core Rule

**Everything is strictly kebab-case unless listed in exceptions.**

### Examples

✅ **Correct**:
```
my-document.md
project-files/
user-guide.md
api-reference.md
```

❌ **Incorrect**:
```
MyDocument.md
project_files/
User_Guide.md
buildScripts/
```

### Exception Management

Edit `naming_exceptions.json` to configure exceptions:

```json
{
  "exceptions": {
    "directories": ["node_modules", ".git"],
    "files": ["LICENSE", "README.md"],
    "file_patterns": ["*.min.js", "*.bundle.*"],
    "standard_ids": {
      "enabled": true,
      "description": "Standard IDs use UPPERCASE format"
    }
  }
}
```

### Validation

The linter automatically checks naming conventions:
```bash
python linter/kb_linter.py --directory . --check-naming
```

## 🤖 Automation Integration

### GitHub Actions

Automatic timestamp updates on commits via `.github/workflows/update-timestamps.yml`:

- **Triggers**: On push/PR to main branches
- **Scope**: Only markdown files with real changes  
- **Updates**: Adds hour/minute precision for commits
- **TODO Reports**: Generated automatically on main branch

### Manual Workflows

**Daily Maintenance**:
```bash
# Update all timestamps
python frontmatter-management/date_time_manager.py scan

# Check TODOs
python todo_tracker.py scan

# Run linter
python linter/kb_linter.py --directory master-knowledge-base
```

**Before Commits**:
```bash
# Update only changed files with real content changes
python frontmatter-management/date_time_manager.py commit-update --time
```

**Project Reviews**:
```bash
# Generate comprehensive reports
python todo_tracker.py report --format markdown --output project-todos.md
python linter/kb_linter.py --directory . --output lint-report.json
```

## 🔧 Configuration

### Environment Setup

**Required Python packages**:
```bash
pip install pyyaml
```

**Make scripts executable**:
```bash
chmod +x frontmatter-management/date_time_manager.py
chmod +x todo_tracker.py
chmod +x linter/kb_linter.py
```

### Tool Configuration

**Date/Time Manager**:
- Default format: `YYYY-MM-DD`
- Lock marker: `# date-locked`
- Context detection: Git word-diff analysis

**TODO Tracker**:
- Pattern: `> [!TODO]` (case-insensitive)
- Context lines: 2 before/after
- Exclusions: `.git`, `__pycache__`, `node_modules`

**Naming Conventions**:
- Default: kebab-case for everything
- Exceptions: Configurable via JSON
- Validation: Integrated with linter

## 🚀 Quick Commands Reference

```bash
# === Date/Time Management ===
# Update all files
python frontmatter-management/date_time_manager.py scan

# Manual date update
python frontmatter-management/date_time_manager.py update *.md --date 2025-01-11

# Commit mode (real changes only)
python frontmatter-management/date_time_manager.py commit-update --time

# === TODO Tracking ===
# Quick scan and report
python todo_tracker.py scan

# Generate markdown report
python todo_tracker.py report --format markdown --output todos.md

# === Content Validation ===
# Run linter
python linter/kb_linter.py --directory master-knowledge-base

# === Naming Validation ===
# Check naming conventions
python linter/kb_linter.py --directory . --check-naming
```

## 📚 Related Standards

- [[SF-CONVENTIONS-NAMING]] - Naming convention standard
- [[OM-VERSIONING-CHANGELOGS]] - Changelog requirements  
- Tool changelogs: `tools/changelog.md`
- Standards changelogs: `standards/changelog.md` 