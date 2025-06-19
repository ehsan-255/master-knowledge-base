#!/usr/bin/env python3
"""
Script to correct invalid references to obsolete collection documents.
This script reads the mapping from l2-sl1-remediation-mapping.json and replaces
the outdated references with corrected text pointing to new standards.
"""

import json
import os
import sys
import argparse
import re
from pathlib import Path
from datetime import datetime

def load_mapping(mapping_file):
    """Load the mapping JSON file."""
    try:
        with open(mapping_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Mapping file '{mapping_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in mapping file: {e}")
        sys.exit(1)

def read_file_content(file_path):
    """Read the content of a file."""
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

def escape_for_regex(text):
    """Escape special regex characters in text."""
    return re.escape(text)

def apply_corrections(mapping_data, dry_run=False):
    """Apply corrections based on the mapping data."""
    timestamp = datetime.now().strftime('%Y%m%d-%H%M')
    log_file = f"tools/reports/collection-reference-correction-{timestamp}.log"
    
    corrections_applied = 0
    files_processed = 0
    errors = []
    
    log_lines = [
        f"Collection Reference Correction Log - {datetime.now().isoformat()}",
        f"Mode: {'DRY RUN' if dry_run else 'LIVE'}",
        "=" * 60,
        ""
    ]
    
    for mapping in mapping_data['mappings']:
        file_path = mapping['file']
        old_text = mapping['old_text']
        new_text = mapping['new_text']
        old_reference = mapping['old_reference']
        
        print(f"Processing: {file_path}")
        log_lines.append(f"Processing: {file_path}")
        
        # Read file content
        content = read_file_content(file_path)
        if content is None:
            error_msg = f"Failed to read file: {file_path}"
            errors.append(error_msg)
            log_lines.append(f"ERROR: {error_msg}")
            continue
        
        # Check if the old text exists in the file
        if old_text not in content:
            warning_msg = f"Old text not found in {file_path}. File may have already been updated."
            print(f"WARNING: {warning_msg}")
            log_lines.append(f"WARNING: {warning_msg}")
            continue
        
        # Replace the old text with new text
        new_content = content.replace(old_text, new_text)
        
        if new_content != content:
            # Log the change
            log_lines.append(f"  OLD: {old_text}")
            log_lines.append(f"  NEW: {new_text}")
            log_lines.append(f"  REFERENCE REMOVED: {old_reference}")
            
            if dry_run:
                print(f"  DRY RUN: Would replace reference to {old_reference}")
                log_lines.append(f"  DRY RUN: Change prepared but not applied")
            else:
                # Write the updated content
                if write_file_content(file_path, new_content):
                    print(f"  ✓ Updated reference to {old_reference}")
                    log_lines.append(f"  ✓ Change applied successfully")
                    corrections_applied += 1
                else:
                    error_msg = f"Failed to write updated content to {file_path}"
                    errors.append(error_msg)
                    log_lines.append(f"ERROR: {error_msg}")
        else:
            log_lines.append(f"  No changes needed (content already correct)")
        
        files_processed += 1
        log_lines.append("")
    
    # Summary
    log_lines.extend([
        "=" * 60,
        "SUMMARY:",
        f"Files processed: {files_processed}",
        f"Corrections applied: {corrections_applied}",
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
    
    return corrections_applied, files_processed, errors

def verify_corrections(mapping_data):
    """Verify that all corrections have been applied by checking for obsolete references."""
    print("\nVerifying corrections...")
    
    remaining_references = []
    
    for mapping in mapping_data['mappings']:
        file_path = mapping['file']
        old_reference = mapping['old_reference']
        
        content = read_file_content(file_path)
        if content is None:
            continue
        
        # Check if the old reference still exists
        if old_reference in content:
            remaining_references.append((file_path, old_reference))
    
    if remaining_references:
        print("⚠️  Still found obsolete references:")
        for file_path, reference in remaining_references:
            print(f"  - {file_path}: {reference}")
        return False
    else:
        print("✅ All obsolete references have been corrected!")
        return True

def main():
    parser = argparse.ArgumentParser(description='Correct invalid references to obsolete collection documents')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Preview changes without applying them')
    parser.add_argument('--mapping-file', 
                       default='active-project/-audit-remediation-initiative-blocked/l2-sl1-correct-invalid-references-active/l2-sl1-remediation-mapping.json',
                       help='Path to the mapping JSON file')
    
    args = parser.parse_args()
    
    # Verify we're in the right directory (workspace root)
    if not os.path.exists('standards/src'):
        print("Error: This script must be run from the repository root directory.")
        sys.exit(1)
    
    # Load mapping
    print(f"Loading mapping from: {args.mapping_file}")
    mapping_data = load_mapping(args.mapping_file)
    
    print(f"Loaded {len(mapping_data['mappings'])} file mappings")
    
    if args.dry_run:
        print("\n🔍 DRY RUN MODE - No files will be modified")
    else:
        print("\n⚡ LIVE MODE - Files will be modified")
    
    # Apply corrections
    corrections, processed, errors = apply_corrections(mapping_data, args.dry_run)
    
    print(f"\nProcessed {processed} files")
    if not args.dry_run:
        print(f"Applied {corrections} corrections")
        if errors:
            print(f"Encountered {len(errors)} errors")
            return 1
        
        # Verify corrections
        if verify_corrections(mapping_data):
            print("\n🎉 All corrections successfully applied!")
            return 0
        else:
            print("\n❌ Some references may still need manual correction")
            return 1
    else:
        print(f"Would apply {corrections} corrections")
        return 0

if __name__ == '__main__':
    sys.exit(main())