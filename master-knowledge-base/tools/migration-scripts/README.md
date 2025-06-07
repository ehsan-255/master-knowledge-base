# Master Knowledge Base to Root Migration Scripts

**⚠️ CRITICAL WARNING: These scripts perform extensive repository modifications. ALWAYS run dry-run tests first!**

## Overview

This directory contains automated scripts for migrating the contents of `master-knowledge-base/` to the repository root. The migration affects **100+ files** with **300+ path references** and requires careful execution.

## Scripts Overview

### 🎯 Main Controller
- **`migrate_master_kb_to_root.py`** - Main orchestration script that coordinates the entire migration process

### 🔧 Supporting Scripts  
- **`update_path_references.py`** - Updates all file content path references
- **`migrate_file_structure.py`** - Handles physical file/directory movement
- **`validate_migration.py`** - Validates migration success and integrity
- **`rollback_migration.py`** - Provides rollback capabilities from backup

## 🚀 Quick Start

### Step 1: Dry Run (MANDATORY)
```bash
# Navigate to repository root
cd /path/to/your-repository-root

# Run comprehensive dry-run test
python master-knowledge-base/tools/migration-scripts/migrate_master_kb_to_root.py --dry-run
```

### Step 2: Review Results
- Check the generated log file in `master-knowledge-base/tools/reports/`
- Review all proposed changes carefully
- Verify backup creation would succeed

### Step 3: Live Migration (DANGEROUS)
```bash
# Only after successful dry-run validation
python master-knowledge-base/tools/migration-scripts/migrate_master_kb_to_root.py --live-run
```

### Step 4: Rollback (If Needed)
```bash
# Restore from backup if migration fails
python master-knowledge-base/tools/migration-scripts/migrate_master_kb_to_root.py --rollback
```

## 📋 Detailed Usage

### Main Migration Controller

```bash
# Show help
python migrate_master_kb_to_root.py --help

# Safe simulation (ALWAYS RUN FIRST)
python migrate_master_kb_to_root.py --dry-run

# Actual migration (DANGEROUS - only after dry-run)
python migrate_master_kb_to_root.py --live-run

# Rollback from backup
python migrate_master_kb_to_root.py --rollback

# Specify custom repository root
python migrate_master_kb_to_root.py --dry-run --repo-root /path/to/repo
```

### Migration Process Steps

The migration controller executes these steps in sequence:

1. **🛡️ Backup Creation**
   - Creates timestamped backup in `archive/migration-backup-YYYYMMDD-HHMMSS/`
   - Verifies backup integrity
   - Excludes existing archive folder

2. **📝 Path Reference Updates**
   - Updates all `master-knowledge-base/` references in files
   - Handles different file types (Python, Markdown, JSON, YAML)
   - Special handling for complex Python scripts

3. **📁 File Structure Migration**
   - Physically moves directories and files to root
   - Checks for conflicts before moving
   - Preserves file attributes and timestamps

4. **✅ Migration Validation**
   - Verifies directory structure is correct
   - Checks for remaining old path references
   - Validates file integrity and counts

5. **🔄 File Regeneration**
   - Regenerates repository tree structure
   - Updates standards index
   - Refreshes generated documentation

## 🛡️ Safety Features

### Comprehensive Backup
- Full repository backup before any changes
- Backup integrity verification
- Automatic rollback capability

### Dry-Run Testing
- Complete simulation without modifications
- Detailed logging of all proposed changes
- Conflict detection and reporting

### Validation & Verification
- Pre-migration conflict checking
- Post-migration integrity validation
- Comprehensive error reporting

### State Tracking
- JSON state file tracks migration progress
- Detailed logging with timestamps
- Error recovery and continuation support

## 📊 Output Files

All outputs are saved to `master-knowledge-base/tools/reports/`:

- **`migration-log-YYYYMMDD-HHMMSS.log`** - Detailed execution log
- **`migration-state-YYYYMMDD-HHMMSS.json`** - Migration state tracking
- **Backup**: `archive/migration-backup-YYYYMMDD-HHMMSS/`

## ⚠️ Important Warnings

### Before Migration
1. **ALWAYS run `--dry-run` first** to validate changes
2. **Review the analysis document** `master-knowledge-base-to-root-migration-analysis.md`
3. **Ensure no uncommitted changes** in the repository
4. **Close all editors and IDEs** that might have files open
5. **Verify sufficient disk space** for backup creation

### During Migration
- **Do not interrupt** the migration process
- **Do not modify files** while migration is running
- **Monitor the log output** for errors or warnings

### After Migration
1. **Verify migration success** using the validation results
2. **Test critical functionality** (tools, scripts, documentation)
3. **Regenerate any cached or derived files** as needed
4. **Update any external references** to the repository structure

## 🔧 Troubleshooting

### Common Issues

**Migration fails with "conflicts detected":**
- Check if target directories already exist in root
- Remove or rename conflicting items before migration

**Path reference updates incomplete:**
- Review the log for files that couldn't be processed
- Manually update any remaining references

**Validation fails after migration:**
- Check the validation report for specific issues
- Use rollback if critical problems are found

**Rollback needed:**
```bash
python migrate_master_kb_to_root.py --rollback
```

### Recovery Procedures

1. **Partial Migration Failure:**
   - Use rollback to restore from backup
   - Fix identified issues
   - Re-run dry-run and migration

2. **Validation Failures:**
   - Review validation report details
   - Fix specific issues manually if minor
   - Use rollback for major problems

3. **Backup Corruption:**
   - Check archive directory for multiple backups
   - Use most recent valid backup for rollback

## 📁 File Structure After Migration

```
repository-root/
├── standards/          # Moved from master-knowledge-base/standards/
├── tools/             # Moved from master-knowledge-base/tools/
├── dist/              # Moved from master-knowledge-base/dist/
├── AS-INDEX-KB-MASTER.md
├── repo-tree.md
├── active-project/
├── archive/
│   └── migration-backup-YYYYMMDD-HHMMSS/  # Full backup
├── test-environment/
└── master-knowledge-base/  # May be empty after migration
```

## 🧪 Testing

### Pre-Migration Testing
```bash
# Validate all scripts can be imported
python -c "from migrate_master_kb_to_root import MigrationController; print('✅ Import successful')"

# Run comprehensive dry-run
python migrate_master_kb_to_root.py --dry-run

# Check log output for any errors
cat master-knowledge-base/tools/reports/migration-log-*.log
```

### Post-Migration Testing
```bash
# Verify key tools still work
python tools/linter/kb_linter.py --help
python tools/indexer/generate_index.py --help

# Check repository structure
python tools/utilities/repo-tree/main_repo_tree.py

# Validate standards index
python tools/indexer/generate_index.py
```

## 📞 Support

If you encounter issues:

1. **Check the log files** in `master-knowledge-base/tools/reports/`
2. **Review the migration state** JSON file for progress tracking
3. **Use rollback** if migration cannot be completed successfully
4. **Consult the analysis document** for detailed change requirements

## 🔒 Archive Policy

After successful migration:
- **Migration scripts** will be moved to `archive/migration-scripts-YYYYMMDD/`
- **Backup files** will be retained for recovery purposes
- **Log files** will be preserved in the reports directory

---

**Remember: This migration is a one-time operation that fundamentally changes the repository structure. Proceed with extreme caution and always validate with dry-run first!** 