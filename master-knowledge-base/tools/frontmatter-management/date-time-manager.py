#!/usr/bin/env python3
"""
Date/Time Management Script for Knowledge Base

Manages date-created and date-modified fields in frontmatter using:
- File system timestamps (mtime, ctime)
- Manual updates with YYYY-MM-DD or YYYY-MM-DD-HH-MM format
- Git commit integration with automatic timestamp updates
- Date locking mechanism to prevent automatic updates
"""

import os
import sys
import json
import argparse
import shutil
from datetime import datetime
from pathlib import Path
import re
import subprocess
import yaml

class DateTimeManager:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.lock_marker = "# date-locked"
        
    def get_file_timestamps(self, file_path):
        """Get file system timestamps"""
        stat = os.stat(file_path)
        created = datetime.fromtimestamp(stat.st_ctime)
        modified = datetime.fromtimestamp(stat.st_mtime)
        return created, modified
    
    def is_date_locked(self, content):
        """Check if file has date-locked marker"""
        return self.lock_marker in content
    
    def parse_frontmatter(self, content):
        """Parse YAML frontmatter from markdown content"""
        if not content.startswith('---\n'):
            return None, content
        
        try:
            # Find end of frontmatter
            end_marker = content.find('\n---\n', 4)
            if end_marker == -1:
                return None, content
            
            frontmatter_yaml = content[4:end_marker]
            body = content[end_marker + 5:]
            frontmatter = yaml.safe_load(frontmatter_yaml)
            return frontmatter, body
            
        except yaml.YAMLError:
            return None, content
    
    def format_datetime(self, dt, include_time=False):
        """Format datetime according to requirements"""
        if include_time:
            return dt.strftime('%Y-%m-%d-%H-%M')
        else:
            return dt.strftime('%Y-%m-%d')
    
    def parse_date_input(self, date_str):
        """Parse date input in YYYY-MM-DD or YYYY-MM-DD-HH-MM format"""
        try:
            if '-' in date_str and len(date_str.split('-')) == 5:
                # YYYY-MM-DD-HH-MM format
                return datetime.strptime(date_str, '%Y-%m-%d-%H-%M')
            else:
                # YYYY-MM-DD format
                return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Invalid date format: {date_str}. Use YYYY-MM-DD or YYYY-MM-DD-HH-MM")
    
    def create_backup(self, file_path):
        """Create backup of file before modification"""
        backup_path = Path(str(file_path) + '.backup')
        shutil.copy2(file_path, backup_path)
        return backup_path
    
    def restore_backup(self, file_path):
        """Restore file from backup"""
        backup_path = Path(str(file_path) + '.backup')
        if backup_path.exists():
            shutil.copy2(backup_path, file_path)
            backup_path.unlink()
            return True
        return False
    
    def cleanup_backup(self, file_path):
        """Remove backup file after successful operation"""
        backup_path = Path(str(file_path) + '.backup')
        if backup_path.exists():
            backup_path.unlink()
    
    def validate_yaml_integrity(self, content):
        """Validate YAML frontmatter integrity"""
        try:
            frontmatter, body = self.parse_frontmatter(content)
            if frontmatter is None:
                return False, "No valid frontmatter found"
            
            # Re-serialize to check if it's valid
            yaml.dump(frontmatter, default_flow_style=False)
            return True, "Valid"
            
        except yaml.YAMLError as e:
            return False, f"YAML error: {str(e)}"
        except Exception as e:
            return False, f"Validation error: {str(e)}"

    def update_frontmatter_dates(self, file_path, manual_date=None, include_time=False, force=False, dry_run=False):
        """Update date fields in frontmatter with safety measures"""
        backup_path = None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if dates are locked
            if self.is_date_locked(content) and not force:
                print(f"Skipping {file_path}: dates are locked")
                return False
            
            frontmatter, body = self.parse_frontmatter(content)
            if frontmatter is None:
                print(f"No frontmatter found in {file_path}")
                return False
            
            # Create backup before any changes
            if not dry_run:
                backup_path = self.create_backup(file_path)
            
            # Get timestamps
            created, modified = self.get_file_timestamps(file_path)
            
            # Update dates
            original_frontmatter = frontmatter.copy()
            if manual_date:
                # Manual date provided
                if include_time:
                    frontmatter['date-modified'] = self.format_datetime(manual_date, True)
                else:
                    frontmatter['date-modified'] = self.format_datetime(manual_date, False)
            else:
                # Use file system timestamps
                if 'date-created' not in frontmatter:
                    frontmatter['date-created'] = self.format_datetime(created, False)
                
                frontmatter['date-modified'] = self.format_datetime(modified, include_time)
            
            # Create new content
            new_content = f"---\n{yaml.dump(frontmatter, default_flow_style=False)}---\n{body}"
            
            # Validate new content before writing
            is_valid, validation_msg = self.validate_yaml_integrity(new_content)
            if not is_valid:
                print(f"Validation failed for {file_path}: {validation_msg}")
                if backup_path:
                    backup_path.unlink()  # Remove backup since we didn't modify
                return False
            
            if dry_run:
                print(f"DRY RUN - Would update {file_path}:")
                print(f"  Original date-modified: {original_frontmatter.get('date-modified', 'None')}")
                print(f"  New date-modified: {frontmatter.get('date-modified', 'None')}")
                return True
            
            # Write to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            # Verify the file was written correctly
            with open(file_path, 'r', encoding='utf-8') as f:
                verify_content = f.read()
            
            is_valid, validation_msg = self.validate_yaml_integrity(verify_content)
            if not is_valid:
                print(f"File corruption detected after write: {validation_msg}")
                print(f"Restoring backup for {file_path}")
                self.restore_backup(file_path)
                return False
            
            # Success - cleanup backup
            self.cleanup_backup(file_path)
            return True
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            # Restore backup if something went wrong
            if backup_path and backup_path.exists():
                print(f"Restoring backup for {file_path}")
                self.restore_backup(file_path)
            return False
    
    def is_real_change(self, file_path):
        """Check if file has real content changes (not just line endings/formatting)"""
        try:
            result = subprocess.run(
                ['git', 'diff', '--word-diff=porcelain', 'HEAD', str(file_path)],
                capture_output=True, text=True, cwd=self.root_dir
            )
            
            if result.returncode != 0:
                # File not in git or other error, assume real change
                return True
            
            diff_output = result.stdout
            
            # Check for real changes (not just whitespace/line endings)
            for line in diff_output.split('\n'):
                if line.startswith('+') or line.startswith('-'):
                    # Skip pure whitespace changes
                    content = line[1:].strip()
                    if content and not content.isspace():
                        return True
            
            return False
            
        except Exception:
            # If git check fails, assume real change
            return True
    
    def lock_dates(self, file_path):
        """Add date-locked marker to prevent automatic updates"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if self.lock_marker not in content:
                # Add lock marker after frontmatter
                if content.startswith('---\n'):
                    end_marker = content.find('\n---\n', 4)
                    if end_marker != -1:
                        insert_pos = end_marker + 5
                        new_content = (content[:insert_pos] + 
                                     f"\n{self.lock_marker}\n" + 
                                     content[insert_pos:])
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        print(f"Locked dates for {file_path}")
                        return True
            
            print(f"Dates already locked for {file_path}")
            return False
            
        except Exception as e:
            print(f"Error locking {file_path}: {e}")
            return False
    
    def unlock_dates(self, file_path):
        """Remove date-locked marker"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if self.lock_marker in content:
                new_content = content.replace(f"\n{self.lock_marker}\n", "\n")
                new_content = new_content.replace(f"{self.lock_marker}\n", "")
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"Unlocked dates for {file_path}")
                return True
            
            print(f"Dates not locked for {file_path}")
            return False
            
        except Exception as e:
            print(f"Error unlocking {file_path}: {e}")
            return False
    
    def update_multiple_files(self, file_paths, manual_date=None, include_time=False, check_changes=False, dry_run=False, force=False):
        """Update multiple files with date/time"""
        updated_count = 0
        
        for file_path in file_paths:
            if not file_path.exists():
                print(f"File not found: {file_path}")
                continue
            
            if not file_path.name.endswith('.md'):
                print(f"Skipping non-markdown file: {file_path}")
                continue
            
            # Check for real changes if requested
            if check_changes and not self.is_real_change(file_path):
                print(f"Skipping {file_path}: no real content changes")
                continue
            
            if self.update_frontmatter_dates(file_path, manual_date, include_time, force, dry_run):
                updated_count += 1
        
        return updated_count

def main():
    parser = argparse.ArgumentParser(description="Manage date/time fields in frontmatter")
    parser.add_argument("--root", "-r", default=".", help="Root directory to scan")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Update command
    update_parser = subparsers.add_parser("update", help="Update date/time fields")
    update_parser.add_argument("files", nargs="+", help="Files to update")
    update_parser.add_argument("--date", "-d", help="Manual date (YYYY-MM-DD or YYYY-MM-DD-HH-MM)")
    update_parser.add_argument("--time", "-t", action="store_true", help="Include time in timestamps")
    update_parser.add_argument("--force", "-f", action="store_true", help="Force update even if locked")
    update_parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying them")
    
    # Dry-run command
    dry_run_parser = subparsers.add_parser("dry-run", help="Preview changes without applying them")
    dry_run_parser.add_argument("files", nargs="+", help="Files to preview")
    dry_run_parser.add_argument("--date", "-d", help="Manual date to preview")
    dry_run_parser.add_argument("--time", "-t", action="store_true", help="Include time in preview")
    
    # Commit update command
    commit_parser = subparsers.add_parser("commit-update", help="Update timestamps for real changes only")
    commit_parser.add_argument("files", nargs="*", help="Files to check (default: all changed files)")
    commit_parser.add_argument("--time", "-t", action="store_true", help="Include time in timestamps")
    
    # Lock/unlock commands
    lock_parser = subparsers.add_parser("lock", help="Lock dates to prevent automatic updates")
    lock_parser.add_argument("files", nargs="+", help="Files to lock")
    
    unlock_parser = subparsers.add_parser("unlock", help="Unlock dates to allow automatic updates")
    unlock_parser.add_argument("files", nargs="+", help="Files to unlock")
    
    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan directory and update all markdown files")
    scan_parser.add_argument("--directory", "-d", default=".", help="Directory to scan")
    scan_parser.add_argument("--time", "-t", action="store_true", help="Include time in timestamps")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = DateTimeManager(args.root)
    
    if args.command == "update":
        manual_date = None
        if args.date:
            manual_date = manager.parse_date_input(args.date)
        
        file_paths = [Path(f) for f in args.files]
        dry_run = getattr(args, 'dry_run', False)
        count = manager.update_multiple_files(file_paths, manual_date, args.time, 
                                            check_changes=False, dry_run=dry_run, force=args.force)
        if dry_run:
            print(f"DRY RUN: Would update {count} files")
        else:
            print(f"Updated {count} files")
    
    elif args.command == "dry-run":
        manual_date = None
        if args.date:
            manual_date = manager.parse_date_input(args.date)
        
        file_paths = [Path(f) for f in args.files]
        count = manager.update_multiple_files(file_paths, manual_date, args.time, 
                                            check_changes=False, dry_run=True, force=False)
        print(f"DRY RUN: Would update {count} files")
    
    elif args.command == "commit-update":
        if args.files:
            file_paths = [Path(f) for f in args.files]
        else:
            # Get changed files from git
            try:
                result = subprocess.run(
                    ['git', 'diff', '--name-only', 'HEAD'],
                    capture_output=True, text=True, cwd=manager.root_dir
                )
                file_paths = [Path(f.strip()) for f in result.stdout.split('\n') if f.strip()]
            except Exception:
                print("Could not get changed files from git")
                return
        
        count = manager.update_multiple_files(file_paths, None, args.time, check_changes=True, dry_run=False, force=False)
        print(f"Updated {count} files with real changes")
    
    elif args.command == "lock":
        for file_path in args.files:
            manager.lock_dates(Path(file_path))
    
    elif args.command == "unlock":
        for file_path in args.files:
            manager.unlock_dates(Path(file_path))
    
    elif args.command == "scan":
        directory = Path(args.directory)
        md_files = list(directory.rglob("*.md"))
        count = manager.update_multiple_files(md_files, None, args.time, check_changes=False, dry_run=False, force=False)
        print(f"Scanned {len(md_files)} files, updated {count}")

if __name__ == "__main__":
    main() 