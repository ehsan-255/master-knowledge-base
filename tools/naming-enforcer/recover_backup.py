#!/usr/bin/env python3
"""
Backup Recovery Tool for Naming Enforcer

This script recovers/restores files from a naming enforcer backup.
It reads the backup manifest and restores all backed up files to their original locations.
"""

import json
import shutil
import argparse
from pathlib import Path
from typing import Dict, List, Optional
import sys

class BackupRecovery:
    """Handles recovery of files from naming enforcer backups."""
    
    def __init__(self, backup_dir: Path):
        """Initialize recovery with backup directory."""
        self.backup_dir = Path(backup_dir)
        self.manifest_path = self.backup_dir / "backup-manifest.json"
        self.manifest: Optional[Dict] = None
        
    def load_manifest(self) -> bool:
        """Load the backup manifest file."""
        if not self.manifest_path.exists():
            print(f"❌ Backup manifest not found: {self.manifest_path}")
            return False
            
        try:
            with open(self.manifest_path, 'r', encoding='utf-8') as f:
                self.manifest = json.load(f)
            print(f"✅ Loaded backup manifest: {self.manifest['backup_id']}")
            print(f"   Timestamp: {self.manifest['timestamp']}")
            print(f"   Description: {self.manifest['operation_description']}")
            return True
        except Exception as e:
            print(f"❌ Error loading manifest: {e}")
            return False
    
    def list_backed_up_files(self) -> List[str]:
        """List all files in the backup."""
        if not self.manifest:
            return []
        return self.manifest.get('backed_up_files', [])
    
    def recover_file(self, original_path: str, dry_run: bool = False) -> bool:
        """Recover a single file from backup."""
        original_path_obj = Path(original_path)
        backup_filename = original_path_obj.name
        backup_file_path = self.backup_dir / backup_filename
        
        if not backup_file_path.exists():
            print(f"❌ Backup file not found: {backup_file_path}")
            return False
        
        if dry_run:
            print(f"🔍 Would restore: {backup_file_path} → {original_path}")
            return True
        
        try:
            # Create parent directories if they don't exist
            original_path_obj.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy the backup file to original location
            shutil.copy2(backup_file_path, original_path_obj)
            print(f"✅ Restored: {backup_filename} → {original_path}")
            return True
        except Exception as e:
            print(f"❌ Error restoring {backup_filename}: {e}")
            return False
    
    def recover_all(self, dry_run: bool = False) -> bool:
        """Recover all files from the backup."""
        if not self.manifest:
            print("❌ No manifest loaded")
            return False
        
        backed_up_files = self.list_backed_up_files()
        if not backed_up_files:
            print("❌ No files to recover")
            return False
        
        print(f"\n{'🔍 DRY RUN - ' if dry_run else ''}Recovering {len(backed_up_files)} files:")
        
        success_count = 0
        for file_path in backed_up_files:
            if self.recover_file(file_path, dry_run):
                success_count += 1
        
        if dry_run:
            print(f"\n🔍 DRY RUN COMPLETE: Would recover {success_count}/{len(backed_up_files)} files")
        else:
            print(f"\n✅ RECOVERY COMPLETE: {success_count}/{len(backed_up_files)} files recovered")
        
        return success_count == len(backed_up_files)
    
    def show_backup_info(self):
        """Display information about the backup."""
        if not self.manifest:
            print("❌ No manifest loaded")
            return
        
        print(f"\n📋 Backup Information:")
        print(f"   ID: {self.manifest['backup_id']}")
        print(f"   Timestamp: {self.manifest['timestamp']}")
        print(f"   Description: {self.manifest['operation_description']}")
        print(f"   Backup Directory: {self.manifest['backup_directory']}")
        
        backed_up_files = self.list_backed_up_files()
        print(f"\n📁 Files in backup ({len(backed_up_files)}):")
        for file_path in backed_up_files:
            file_obj = Path(file_path)
            backup_file = self.backup_dir / file_obj.name
            if backup_file.exists():
                size = backup_file.stat().st_size
                print(f"   ✅ {file_obj.name} ({size} bytes) → {file_path}")
            else:
                print(f"   ❌ {file_obj.name} (MISSING) → {file_path}")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Recover files from a naming enforcer backup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show backup information
  python recover_backup.py --backup-dir ../reports/backups/fix_violations_20250604_044245 --info
  
  # Dry run recovery
  python recover_backup.py --backup-dir ../reports/backups/fix_violations_20250604_044245 --dry-run
  
  # Perform actual recovery
  python recover_backup.py --backup-dir ../reports/backups/fix_violations_20250604_044245
        """
    )
    
    parser.add_argument(
        '--backup-dir',
        type=str,
        required=True,
        help='Path to the backup directory containing backup-manifest.json'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be recovered without actually doing it'
    )
    
    parser.add_argument(
        '--info',
        action='store_true',
        help='Show backup information only'
    )
    
    args = parser.parse_args()
    
    # Initialize recovery
    recovery = BackupRecovery(args.backup_dir)
    
    # Load manifest
    if not recovery.load_manifest():
        sys.exit(1)
    
    # Show info if requested
    if args.info:
        recovery.show_backup_info()
        return
    
    # Show backup info first
    recovery.show_backup_info()
    
    # Perform recovery
    if recovery.recover_all(dry_run=args.dry_run):
        if not args.dry_run:
            print("\n🎉 All files recovered successfully!")
    else:
        print("\n⚠️  Some files could not be recovered")
        sys.exit(1)

if __name__ == "__main__":
    main() 