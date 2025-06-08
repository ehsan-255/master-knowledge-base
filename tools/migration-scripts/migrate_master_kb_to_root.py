#!/usr/bin/env python3
"""
Master Knowledge Base to Root Migration Controller

This script orchestrates the migration of master-knowledge-base/ contents to repository root.
Includes comprehensive dry-run testing, backup procedures, and rollback capabilities.

CRITICAL: This script performs extensive repository modifications.
ALWAYS run with --dry-run first to validate changes.

Usage:
    python migrate_master_kb_to_root.py --dry-run    # Safe simulation
    python migrate_master_kb_to_root.py --live-run   # Actual migration (DANGEROUS)
    python migrate_master_kb_to_root.py --rollback   # Restore from backup

Author: Automated Migration System
Generated: 2025-01-27
"""

import os
import sys
import argparse
import logging
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import subprocess
import hashlib

# Add tools directory to path for imports
script_dir = Path(__file__).parent
tools_dir = script_dir.parent
sys.path.insert(0, str(tools_dir))

class MigrationController:
    """Main controller for master-knowledge-base to root migration."""
    
    def __init__(self, repo_root: Path, dry_run: bool = True):
        self.repo_root = repo_root.resolve()
        self.dry_run = dry_run
        self.timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.backup_dir = self.repo_root / "archive" / f"migration-backup-{self.timestamp}"
        self.log_file = self.repo_root / "master-knowledge-base" / "tools" / "reports" / f"migration-log-{self.timestamp}.log"
        self.migration_state_file = self.repo_root / "master-knowledge-base" / "tools" / "reports" / f"migration-state-{self.timestamp}.json"
        
        # Setup logging
        self.setup_logging()
        
        # Migration state tracking
        self.migration_state = {
            "timestamp": self.timestamp,
            "dry_run": dry_run,
            "backup_created": False,
            "backup_path": str(self.backup_dir),
            "steps_completed": [],
            "errors": [],
            "files_modified": [],
            "validation_results": {}
        }
        
        # Minimal console output for performance
        print(f"Migration Controller initialized - {'DRY RUN' if dry_run else 'LIVE RUN'}")
        print(f"Repository root: {self.repo_root}")
        self.logger.info(f"Migration Controller initialized - {'DRY RUN' if dry_run else 'LIVE RUN'}")
        self.logger.info(f"Repository root: {self.repo_root}")
        self.logger.info(f"Backup directory: {self.backup_dir}")
    
    def setup_logging(self):
        """Setup comprehensive logging."""
        # Ensure reports directory exists
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Configure logging - reduced for performance
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file)
                # Console logging removed for performance
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def save_migration_state(self):
        """Save current migration state to file."""
        try:
            with open(self.migration_state_file, 'w') as f:
                json.dump(self.migration_state, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save migration state: {e}")
    
    def create_backup(self) -> bool:
        """Create comprehensive repository backup."""
        self.logger.info("=" * 60)
        self.logger.info("STEP 1: CREATING REPOSITORY BACKUP")
        self.logger.info("=" * 60)
        
        try:
            if self.dry_run:
                self.logger.info(f"[DRY RUN] Would create backup at: {self.backup_dir}")
                self.migration_state["backup_created"] = True
                return True
            
            # Create backup directory
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy entire repository except archive folder
            for item in self.repo_root.iterdir():
                if item.name == "archive":
                    continue
                
                dest = self.backup_dir / item.name
                if item.is_dir():
                    shutil.copytree(item, dest, ignore=shutil.ignore_patterns('*.pyc', '__pycache__'))
                else:
                    shutil.copy2(item, dest)
                
                self.logger.info(f"Backed up: {item.name}")
            
            # Verify backup
            if self.verify_backup():
                self.migration_state["backup_created"] = True
                self.logger.info("✅ Backup created and verified successfully")
                return True
            else:
                self.logger.error("❌ Backup verification failed")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Backup creation failed: {e}")
            self.migration_state["errors"].append(f"Backup creation failed: {e}")
            return False
    
    def verify_backup(self) -> bool:
        """Verify backup integrity."""
        try:
            # Check if master-knowledge-base exists in backup
            mkb_backup = self.backup_dir / "master-knowledge-base"
            if not mkb_backup.exists():
                self.logger.error("master-knowledge-base not found in backup")
                return False
            
            # Check critical directories
            critical_dirs = ["standards", "tools"]
            for dir_name in critical_dirs:
                if not (mkb_backup / dir_name).exists():
                    self.logger.error(f"Critical directory {dir_name} not found in backup")
                    return False
            
            self.logger.info("Backup verification passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Backup verification failed: {e}")
            return False
    
    def update_path_references(self) -> bool:
        """Update all path references in files."""
        self.logger.info("=" * 60)
        self.logger.info("STEP 2: UPDATING PATH REFERENCES")
        self.logger.info("=" * 60)
        
        try:
            # Import path reference updater from same directory
            import sys
            sys.path.insert(0, str(script_dir))
            from update_path_references import PathReferenceUpdater
            
            updater = PathReferenceUpdater(self.repo_root, self.dry_run, self.logger)
            success = updater.update_all_references()
            
            if success:
                self.migration_state["files_modified"].extend(updater.get_modified_files())
                self.logger.info("✅ Path references updated successfully")
                return True
            else:
                self.logger.error("❌ Path reference update failed")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Path reference update failed: {e}")
            self.migration_state["errors"].append(f"Path reference update failed: {e}")
            return False
    
    def migrate_file_structure(self) -> bool:
        """Migrate the physical file structure."""
        self.logger.info("=" * 60)
        self.logger.info("STEP 3: MIGRATING FILE STRUCTURE")
        self.logger.info("=" * 60)
        
        try:
            # Import file structure migrator from same directory
            from migrate_file_structure import FileStructureMigrator
            
            migrator = FileStructureMigrator(self.repo_root, self.dry_run, self.logger)
            success = migrator.migrate_structure()
            
            if success:
                self.logger.info("✅ File structure migrated successfully")
                return True
            else:
                self.logger.error("❌ File structure migration failed")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ File structure migration failed: {e}")
            self.migration_state["errors"].append(f"File structure migration failed: {e}")
            return False
    
    def validate_migration(self) -> bool:
        """Validate the migration results."""
        self.logger.info("=" * 60)
        self.logger.info("STEP 4: VALIDATING MIGRATION")
        self.logger.info("=" * 60)
        
        try:
            # Import validation suite from same directory
            from validate_migration import MigrationValidator
            
            validator = MigrationValidator(self.repo_root, self.logger)
            results = validator.validate_migration()
            
            self.migration_state["validation_results"] = results
            
            if results["overall_success"]:
                self.logger.info("✅ Migration validation passed")
                return True
            else:
                self.logger.error("❌ Migration validation failed")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Migration validation failed: {e}")
            self.migration_state["errors"].append(f"Migration validation failed: {e}")
            return False
    
    def regenerate_files(self) -> bool:
        """Regenerate files that depend on the new structure."""
        self.logger.info("=" * 60)
        self.logger.info("STEP 5: REGENERATING DEPENDENT FILES")
        self.logger.info("=" * 60)
        
        try:
            # Regenerate repository tree
            if self.dry_run:
                self.logger.info("[DRY RUN] Would regenerate repository tree")
            else:
                repo_tree_script = self.repo_root / "tools" / "utilities" / "repo-tree" / "main_repo_tree.py"
                if repo_tree_script.exists():
                    subprocess.run([sys.executable, str(repo_tree_script)], cwd=self.repo_root)
                    self.logger.info("Regenerated repository tree")
            
            # Regenerate standards index
            if self.dry_run:
                self.logger.info("[DRY RUN] Would regenerate standards index")
            else:
                index_script = self.repo_root / "tools" / "indexer" / "generate_index.py"
                if index_script.exists():
                    subprocess.run([sys.executable, str(index_script)], cwd=self.repo_root)
                    self.logger.info("Regenerated standards index")
            
            self.logger.info("✅ File regeneration completed")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ File regeneration failed: {e}")
            self.migration_state["errors"].append(f"File regeneration failed: {e}")
            return False
    
    def run_migration(self) -> bool:
        """Execute the complete migration process."""
        # Console output for key milestones
        print("STARTING MASTER-KNOWLEDGE-BASE TO ROOT MIGRATION")
        print(f"Mode: {'DRY RUN (SAFE)' if self.dry_run else 'LIVE RUN (DANGEROUS)'}")
        
        self.logger.info("STARTING MASTER-KNOWLEDGE-BASE TO ROOT MIGRATION")
        self.logger.info(f"Mode: {'DRY RUN (SAFE)' if self.dry_run else 'LIVE RUN (DANGEROUS)'}")
        self.logger.info("=" * 80)
        
        if not self.dry_run:
            print("WARNING: LIVE RUN MODE - REPOSITORY WILL BE MODIFIED")
            self.logger.warning("WARNING: LIVE RUN MODE - REPOSITORY WILL BE MODIFIED")
            self.logger.warning("Ensure you have reviewed the dry-run results first!")
        
        # Execute migration steps
        steps = [
            ("create_backup", self.create_backup),
            ("update_path_references", self.update_path_references),
            ("migrate_file_structure", self.migrate_file_structure),
            ("validate_migration", self.validate_migration),
            ("regenerate_files", self.regenerate_files)
        ]
        
        for step_name, step_func in steps:
            print(f"Executing step: {step_name}")
            self.logger.info(f"Executing step: {step_name}")
            
            if step_func():
                self.migration_state["steps_completed"].append(step_name)
                print(f"SUCCESS: {step_name}")
                self.logger.info(f"Step completed: {step_name}")
            else:
                print(f"ERROR: {step_name}")
                self.logger.error(f"Step failed: {step_name}")
                self.save_migration_state()
                return False
            
            self.save_migration_state()
        
        # Final summary
        self.logger.info("=" * 80)
        if self.dry_run:
            print("DRY RUN COMPLETED SUCCESSFULLY")
            print("Review the log file for detailed changes")
            print("Run with --live-run to execute actual migration")
            self.logger.info("DRY RUN COMPLETED SUCCESSFULLY")
            self.logger.info("Review the log file for detailed changes")
            self.logger.info("Run with --live-run to execute actual migration")
        else:
            print("MIGRATION COMPLETED SUCCESSFULLY")
            print("Backup available at: " + str(self.backup_dir))
            print("Migration log: " + str(self.log_file))
            self.logger.info("MIGRATION COMPLETED SUCCESSFULLY")
            self.logger.info("Backup available at: " + str(self.backup_dir))
            self.logger.info("Migration log: " + str(self.log_file))
        
        self.save_migration_state()
        return True
    
    def rollback_migration(self) -> bool:
        """Rollback migration using backup."""
        self.logger.info("🔄 STARTING MIGRATION ROLLBACK")
        
        try:
            # Import rollback manager
            from rollback_migration import RollbackManager
            
            rollback_manager = RollbackManager(self.repo_root, self.logger)
            success = rollback_manager.rollback_from_backup(self.backup_dir)
            
            if success:
                self.logger.info("✅ Rollback completed successfully")
                return True
            else:
                self.logger.error("❌ Rollback failed")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Rollback failed: {e}")
            return False

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Master Knowledge Base to Root Migration Controller",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python migrate_master_kb_to_root.py --dry-run     # Safe simulation
    python migrate_master_kb_to_root.py --live-run    # Actual migration
    python migrate_master_kb_to_root.py --rollback    # Restore from backup

IMPORTANT: Always run --dry-run first to validate changes!
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true", 
                      help="Simulate migration without making changes (SAFE)")
    group.add_argument("--live-run", action="store_true", 
                      help="Execute actual migration (DANGEROUS)")
    group.add_argument("--rollback", action="store_true", 
                      help="Rollback migration using backup")
    
    parser.add_argument("--repo-root", type=Path, default=Path.cwd().parent.parent.parent,
                       help="Repository root directory (default: auto-detect)")
    
    args = parser.parse_args()
    
    # Validate repository root
    repo_root = args.repo_root.resolve()
    if not (repo_root / "master-knowledge-base").exists():
        print(f"❌ Error: master-knowledge-base not found in {repo_root}")
        print("Please specify correct --repo-root or run from correct directory")
        sys.exit(1)
    
    # Create migration controller
    if args.rollback:
        controller = MigrationController(repo_root, dry_run=False)
        success = controller.rollback_migration()
    else:
        controller = MigrationController(repo_root, dry_run=args.dry_run)
        success = controller.run_migration()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 