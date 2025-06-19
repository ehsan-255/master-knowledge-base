#!/usr/bin/env python3
"""
Script to remove changelog metadata from standards frontmatter.
This script removes the 'change_log_url' key from the YAML frontmatter 
of all markdown files in standards/src/ where it exists.
"""

import os
import sys
import re
import argparse
from pathlib import Path
from datetime import datetime
import yaml

def read_file_content(file_path):
    """Read the content of a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        return None

def write_file_content(file_path, content, dry_run=False):
    """Write content to a file."""
    if dry_run:
        print(f"DRY RUN: Would write to {file_path}")
        return True
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing to file '{file_path}': {e}")
        return False

def extract_frontmatter_and_content(content):
    """
    Extract YAML frontmatter and content from a markdown file.
    Returns (frontmatter_lines, content_after_frontmatter) or (None, content) if no frontmatter.
    """
    if not content.startswith('---\n'):
        return None, content
    
    lines = content.split('\n')
    frontmatter_end = None
    
    # Find the closing ---
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == '---':
            frontmatter_end = i
            break
    
    if frontmatter_end is None:
        return None, content
    
    frontmatter_lines = lines[1:frontmatter_end]
    content_after = '\n'.join(lines[frontmatter_end + 1:])
    
    return frontmatter_lines, content_after

def remove_changelog_url_from_frontmatter(frontmatter_lines):
    """
    Remove the change_log_url key from frontmatter lines.
    Returns (modified_lines, was_modified).
    """
    if frontmatter_lines is None:
        return None, False
    
    modified_lines = []
    was_modified = False
    
    for line in frontmatter_lines:
        # Check if this line contains change_log_url
        if re.match(r'^\s*change_log_url\s*:', line):
            was_modified = True
            continue  # Skip this line
        modified_lines.append(line)
    
    return modified_lines, was_modified

def process_file(file_path, dry_run=False):
    """
    Process a single markdown file to remove change_log_url from frontmatter.
    Returns (was_modified, error_message).
    """
    content = read_file_content(file_path)
    if content is None:
        return False, f"Could not read file: {file_path}"
    
    # Extract frontmatter and content
    frontmatter_lines, content_after = extract_frontmatter_and_content(content)
    
    if frontmatter_lines is None:
        return False, None  # No frontmatter, no modification needed
    
    # Remove change_log_url from frontmatter
    modified_frontmatter, was_modified = remove_changelog_url_from_frontmatter(frontmatter_lines)
    
    if not was_modified or modified_frontmatter is None:
        return False, None  # No change_log_url found, no modification needed
    
    # Reconstruct the file content
    new_content = '---\n' + '\n'.join(modified_frontmatter) + '\n---\n' + content_after
    
    # Write the modified content
    if write_file_content(file_path, new_content, dry_run):
        return True, None
    else:
        return False, f"Failed to write modified content to {file_path}"

def scan_standards_directory(standards_dir, dry_run=False):
    """
    Scan the standards directory and process all markdown files.
    Returns (files_processed, files_modified, errors).
    """
    timestamp = datetime.now().strftime('%Y%m%d-%H%M')
    log_file = f"tools/reports/changelog-metadata-removal-{timestamp}.log"
    
    files_processed = 0
    files_modified = 0
    errors = []
    
    log_lines = [
        f"Changelog Metadata Removal Log - {datetime.now().isoformat()}",
        f"Mode: {'DRY RUN' if dry_run else 'LIVE'}",
        f"Target Directory: {standards_dir}",
        "=" * 60,
        ""
    ]
    
    # Get all markdown files in the standards directory
    md_files = list(Path(standards_dir).glob('*.md'))
    
    if not md_files:
        error_msg = f"No markdown files found in {standards_dir}"
        errors.append(error_msg)
        log_lines.append(f"ERROR: {error_msg}")
        return files_processed, files_modified, errors
    
    log_lines.append(f"Found {len(md_files)} markdown files to process")
    log_lines.append("")
    
    for md_file in sorted(md_files):
        file_path = str(md_file)
        relative_path = os.path.relpath(file_path)
        
        print(f"Processing: {relative_path}")
        log_lines.append(f"Processing: {relative_path}")
        
        was_modified, error = process_file(file_path, dry_run)
        files_processed += 1
        
        if error:
            errors.append(error)
            log_lines.append(f"  ERROR: {error}")
            print(f"  ERROR: {error}")
        elif was_modified:
            files_modified += 1
            if dry_run:
                print(f"  DRY RUN: Would remove change_log_url from frontmatter")
                log_lines.append(f"  DRY RUN: Would remove change_log_url from frontmatter")
            else:
                print(f"  ✓ Removed change_log_url from frontmatter")
                log_lines.append(f"  ✓ Removed change_log_url from frontmatter")
        else:
            print(f"  No change_log_url found (no modification needed)")
            log_lines.append(f"  No change_log_url found (no modification needed)")
        
        log_lines.append("")
    
    # Summary
    log_lines.extend([
        "=" * 60,
        "SUMMARY:",
        f"Files processed: {files_processed}",
        f"Files modified: {files_modified}",
        f"Errors encountered: {len(errors)}",
        ""
    ])
    
    if errors:
        log_lines.append("ERRORS:")
        for error in errors:
            log_lines.append(f"  - {error}")
    
    # Write log file
    try:
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(log_lines))
        print(f"\nLog written to: {log_file}")
    except Exception as e:
        print(f"Warning: Could not write log file: {e}")
    
    return files_processed, files_modified, errors

def verify_removal(standards_dir):
    """
    Verify that all change_log_url keys have been removed from the standards directory.
    Returns True if no change_log_url keys are found, False otherwise.
    """
    print("\nVerifying changelog metadata removal...")
    
    md_files = list(Path(standards_dir).glob('*.md'))
    remaining_files = []
    
    for md_file in md_files:
        content = read_file_content(str(md_file))
        if content and 'change_log_url:' in content:
            remaining_files.append(os.path.relpath(str(md_file)))
    
    if remaining_files:
        print("⚠️  Still found change_log_url in the following files:")
        for file_path in remaining_files:
            print(f"  - {file_path}")
        return False
    else:
        print("✅ All change_log_url keys have been removed!")
        return True

def main():
    parser = argparse.ArgumentParser(description='Remove change_log_url metadata from standards frontmatter')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Preview changes without applying them')
    parser.add_argument('--standards-dir', 
                       default='standards/src',
                       help='Path to the standards directory (default: standards/src)')
    
    args = parser.parse_args()
    
    # Verify we're in the right directory (workspace root)
    if not os.path.exists(args.standards_dir):
        print(f"Error: Standards directory '{args.standards_dir}' not found.")
        print("This script must be run from the repository root directory.")
        sys.exit(1)
    
    print(f"Processing markdown files in: {args.standards_dir}")
    
    if args.dry_run:
        print("\n🔍 DRY RUN MODE - No files will be modified")
    else:
        print("\n⚡ LIVE MODE - Files will be modified")
    
    # Process files
    processed, modified, errors = scan_standards_directory(args.standards_dir, args.dry_run)
    
    print(f"\nProcessed {processed} files")
    if not args.dry_run:
        print(f"Modified {modified} files")
        if errors:
            print(f"Encountered {len(errors)} errors")
            return 1
        
        # Verify removal
        if verify_removal(args.standards_dir):
            print("\n🎉 All changelog metadata successfully removed!")
            return 0
        else:
            print("\n❌ Some change_log_url keys may still need manual removal")
            return 1
    else:
        print(f"Would modify {modified} files")
        return 0

if __name__ == '__main__':
    sys.exit(main())