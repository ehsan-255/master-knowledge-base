#!/usr/bin/env python3
"""
Rollback Manager for Master Knowledge Base Migration

This script provides rollback capabilities to restore the repository from backup
if the migration fails or needs to be undone.

Author: Automated Migration System
Generated: 2025-01-27
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict
import logging

class RollbackManager:
    """Manages rollback operations for migration."""
    
    def __init__(self, repo_root: Path, logger: logging.Logger):
        self.repo_root = repo_root
        self.logger = logger
        self.archive_dir = repo_root / "archive"
    
    def find_latest_backup(self) -> Path:
        """Find the most recent migration backup."""
        backup_dirs = []
        
        if self.archive_dir.exists():
            for item in self.archive_dir.iterdir():
                if item.is_dir() and item.name.startswith("migration-backup-"):
                    backup_dirs.append(item)
        
        if not backup_dirs:
            raise Exception("No migration backup found in archive directory")
        
        # Sort by name (which includes timestamp)
        backup_dirs.sort(key=lambda x: x.name, reverse=True)
        return backup_dirs[0]
    
    def rollback_from_backup(self, backup_dir: Path = None) -> bool:
        """Rollback migration using specified or latest backup."""
        try:
            if backup_dir is None:
                backup_dir = self.find_latest_backup()
            
            if not backup_dir.exists():
                self.logger.error(f"Backup directory not found: {backup_dir}")
                return False
            
            self.logger.info(f"Starting rollback from backup: {backup_dir}")
            
            # Verify backup integrity
            if not self.verify_backup_integrity(backup_dir):
                self.logger.error("Backup integrity check failed")
                return False
            
            # Remove current migrated items
            self.remove_migrated_items()
            
            # Restore from backup
            self.restore_from_backup(backup_dir)
            
            self.logger.info("✅ Rollback completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Rollback failed: {e}")
            return False
    
    def verify_backup_integrity(self, backup_dir: Path) -> bool:
        """Verify that the backup is complete and valid."""
        try:
            self.logger.info("Verifying backup integrity...")
            
            # Check for master-knowledge-base directory
            mkb_backup = backup_dir / "master-knowledge-base"
            if not mkb_backup.exists():
                self.logger.error("master-knowledge-base not found in backup")
                return False
            
            # Check for critical directories
            critical_dirs = ["standards", "tools"]
            for dir_name in critical_dirs:
                if not (mkb_backup / dir_name).exists():
                    self.logger.error(f"Critical directory {dir_name} not found in backup")
                    return False
            
            # Check for key files
            key_files = ["README.md", "repo-tree.md"]
            for file_name in key_files:
                if not (backup_dir / file_name).exists():
                    self.logger.warning(f"Key file {file_name} not found in backup")
            
            self.logger.info("Backup integrity verification passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Backup integrity verification failed: {e}")
            return False
    
    def remove_migrated_items(self):
        """Remove items that were migrated to root during migration."""
        migrated_items = [
            "standards",
            "tools",
            "dist", 
            "AS-INDEX-KB-MASTER.md",
            "repo-tree.md"
        ]
        
        self.logger.info("Removing migrated items from root...")
        
        for item_name in migrated_items:
            item_path = self.repo_root / item_name
            if item_path.exists():
                try:
                    if item_path.is_dir():
                        shutil.rmtree(item_path)
                        self.logger.info(f"Removed directory: {item_name}")
                    else:
                        item_path.unlink()
                        self.logger.info(f"Removed file: {item_name}")
                except Exception as e:
                    self.logger.error(f"Failed to remove {item_name}: {e}")
                    raise
    
    def restore_from_backup(self, backup_dir: Path):
        """Restore repository contents from backup."""
        self.logger.info("Restoring from backup...")
        
        # Restore all items from backup
        for item in backup_dir.iterdir():
            dest_path = self.repo_root / item.name
            
            try:
                if item.is_dir():
                    if dest_path.exists():
                        shutil.rmtree(dest_path)
                    shutil.copytree(item, dest_path)
                    self.logger.info(f"Restored directory: {item.name}")
                else:
                    if dest_path.exists():
                        dest_path.unlink()
                    shutil.copy2(item, dest_path)
                    self.logger.info(f"Restored file: {item.name}")
                    
            except Exception as e:
                self.logger.error(f"Failed to restore {item.name}: {e}")
                raise
    
    def list_available_backups(self) -> List[Dict]:
        """List all available migration backups."""
        backups = []
        
        if self.archive_dir.exists():
            for item in self.archive_dir.iterdir():
                if item.is_dir() and item.name.startswith("migration-backup-"):
                    # Extract timestamp from backup name
                    timestamp = item.name.replace("migration-backup-", "")
                    
                    backup_info = {
                        "path": item,
                        "name": item.name,
                        "timestamp": timestamp,
                        "size": self.get_directory_size(item)
                    }
                    backups.append(backup_info)
        
        # Sort by timestamp (newest first)
        backups.sort(key=lambda x: x["timestamp"], reverse=True)
        return backups
    
    def get_directory_size(self, directory: Path) -> int:
        """Get total size of directory in bytes."""
        total_size = 0
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = Path(root) / file
                    try:
                        total_size += file_path.stat().st_size
                    except (OSError, FileNotFoundError):
                        pass
        except Exception:
            pass
        return total_size
    
    def cleanup_old_backups(self, keep_count: int = 3):
        """Clean up old migration backups, keeping only the most recent ones."""
        try:
            backups = self.list_available_backups()
            
            if len(backups) <= keep_count:
                self.logger.info(f"Only {len(backups)} backups found, no cleanup needed")
                return
            
            backups_to_remove = backups[keep_count:]
            
            for backup in backups_to_remove:
                try:
                    shutil.rmtree(backup["path"])
                    self.logger.info(f"Removed old backup: {backup['name']}")
                except Exception as e:
                    self.logger.error(f"Failed to remove backup {backup['name']}: {e}")
            
            self.logger.info(f"Cleanup completed, kept {keep_count} most recent backups")
            
        except Exception as e:
            self.logger.error(f"Backup cleanup failed: {e}")

if __name__ == "__main__":
    # This script is meant to be imported, not run directly
    print("This script should be imported by the migration controller.") 