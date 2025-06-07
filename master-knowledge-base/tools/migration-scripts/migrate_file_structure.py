#!/usr/bin/env python3
"""
File Structure Migrator for Master Knowledge Base Migration

This script handles the physical movement of files and directories from
master-knowledge-base/ to repository root.

Author: Automated Migration System
Generated: 2025-01-27
"""

import os
import shutil
from pathlib import Path
from typing import List, Tuple
import logging

class FileStructureMigrator:
    """Handles physical file and directory migration."""
    
    def __init__(self, repo_root: Path, dry_run: bool, logger: logging.Logger):
        self.repo_root = repo_root
        self.dry_run = dry_run
        self.logger = logger
        self.mkb_path = repo_root / "master-knowledge-base"
        
        # Define what to move and potential conflicts
        self.items_to_move = [
            "standards",
            "tools", 
            "dist",
            "AS-INDEX-KB-MASTER.md",
            "repo-tree.md"
        ]
        
        # Items that should NOT be moved (stay in master-knowledge-base)
        self.items_to_keep = [
            # These will be handled by the migration scripts themselves
        ]
    
    def migrate_structure(self) -> bool:
        """Execute the file structure migration."""
        try:
            self.logger.info("Starting file structure migration...")
            
            # Check for conflicts first
            conflicts = self.check_conflicts()
            if conflicts:
                self.logger.error("Migration conflicts detected:")
                for conflict in conflicts:
                    self.logger.error(f"  - {conflict}")
                return False
            
            # Move items
            success_count = 0
            error_count = 0
            
            for item_name in self.items_to_move:
                try:
                    if self.move_item(item_name):
                        success_count += 1
                    else:
                        error_count += 1
                except Exception as e:
                    self.logger.error(f"Error moving {item_name}: {e}")
                    error_count += 1
            
            # Clean up empty master-knowledge-base directory if all items moved
            if not self.dry_run and error_count == 0:
                self.cleanup_mkb_directory()
            
            self.logger.info(f"File structure migration completed: {success_count} success, {error_count} errors")
            return error_count == 0
            
        except Exception as e:
            self.logger.error(f"File structure migration failed: {e}")
            return False
    
    def check_conflicts(self) -> List[str]:
        """Check for potential conflicts before migration."""
        conflicts = []
        
        for item_name in self.items_to_move:
            source_path = self.mkb_path / item_name
            dest_path = self.repo_root / item_name
            
            if not source_path.exists():
                conflicts.append(f"Source does not exist: {source_path}")
                continue
            
            if dest_path.exists():
                conflicts.append(f"Destination already exists: {dest_path}")
        
        return conflicts
    
    def move_item(self, item_name: str) -> bool:
        """Move a single item from master-knowledge-base to root."""
        try:
            source_path = self.mkb_path / item_name
            dest_path = self.repo_root / item_name
            
            if not source_path.exists():
                self.logger.warning(f"Source does not exist: {source_path}")
                return True  # Not an error if it doesn't exist
            
            if self.dry_run:
                self.logger.info(f"[DRY RUN] Would move: {source_path} -> {dest_path}")
                return True
            
            # Perform the move
            if source_path.is_dir():
                shutil.move(str(source_path), str(dest_path))
                self.logger.info(f"Moved directory: {item_name}")
            else:
                shutil.move(str(source_path), str(dest_path))
                self.logger.info(f"Moved file: {item_name}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to move {item_name}: {e}")
            return False
    
    def cleanup_mkb_directory(self):
        """Clean up the master-knowledge-base directory after migration."""
        try:
            # Check if directory is empty (except for migration scripts)
            remaining_items = []
            for item in self.mkb_path.iterdir():
                if item.name not in ["tools"]:  # tools might contain migration scripts
                    remaining_items.append(item.name)
            
            if not remaining_items:
                self.logger.info("master-knowledge-base directory is empty after migration")
                # Note: We don't delete it as it might contain migration scripts
            else:
                self.logger.info(f"master-knowledge-base directory contains: {remaining_items}")
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")

if __name__ == "__main__":
    # This script is meant to be imported, not run directly
    print("This script should be imported by the migration controller.") 