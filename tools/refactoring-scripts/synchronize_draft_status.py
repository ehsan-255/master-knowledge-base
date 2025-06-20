#!/usr/bin/env python3
"""
Synchronizes the 'status/draft' state of standards to match the official list.

This script ensures that exactly the 47 standards listed in the canonical
tracking sheet have the status 'draft', and any other standard that might
be incorrectly marked as 'draft' is promoted to 'active'.

This corrects the state of the repository after an uncontrolled process left
an incorrect number of standards in draft status.
"""

import argparse
from pathlib import Path
import sys
import re

# Define project structure
ROOT = Path(__file__).resolve().parents[2]
TRACKING_SHEET_PATH = ROOT / 'archive/audit-remediation-initiative-completed-20250620-1710/l2-sl3-establish-draft-promotion-process-completed/draft-standards-tracking-sheet.md'
STANDARDS_DIR = ROOT / 'standards' / 'src'

def get_official_draft_files(tracker_path: Path) -> set[Path]:
    """Parses the tracking sheet to get the official set of draft file paths."""
    if not tracker_path.exists():
        print(f"Error: Tracking sheet not found at '{tracker_path}'")
        sys.exit(1)
    content = tracker_path.read_text(encoding='utf-8')
    path_pattern = re.compile(r'\|\s*([A-Z0-9-]+)\s*\|\s*[A-Z]{2}\s*\|\s*(standards/src/[^|\s]+?\.md)\s*\|')
    return {ROOT / path for _, path in path_pattern.findall(content)}

def get_current_draft_files(standards_dir: Path) -> set[Path]:
    """Globs all standards and returns a set of those currently in draft status."""
    current_drafts = set()
    for md_file in standards_dir.glob('**/*.md'):
        content = md_file.read_text(encoding='utf-8')
        if "status: draft" in content.lower():
            current_drafts.add(md_file)
    return current_drafts

def set_file_status(file_path: Path, new_status: str, dry_run: bool):
    """Sets the status of a file to the new_status ('draft' or 'active')."""
    try:
        if not file_path.exists():
            return False
        
        content = file_path.read_text(encoding='utf-8')
        current_status = "draft" if "status: draft" in content.lower() else "active"

        if current_status == new_status:
            return False # No change needed

        # Regex to find and replace the status value
        new_content, count = re.subn(
            rf"(status:\s*){current_status}",
            rf"\1{new_status}",
            content,
            flags=re.IGNORECASE
        )

        if count > 0:
            if not dry_run:
                print(f"    - WRITING to {file_path.relative_to(ROOT)}")
                file_path.write_text(new_content, encoding='utf-8')
            return True
        return False
    except Exception as e:
        print(f"  - ERROR processing {file_path.relative_to(ROOT)}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Synchronize draft status of standards to match the canonical list.")
    parser.add_argument('--dry-run', action='store_true', help="Preview changes without modifying files.")
    args = parser.parse_args()

    print("Starting synchronization of draft standards...")
    if args.dry_run:
        print("--- DRY RUN MODE ---")

    official_drafts = get_official_draft_files(TRACKING_SHEET_PATH)
    current_drafts = get_current_draft_files(STANDARDS_DIR)
    
    print(f"Official list contains {len(official_drafts)} draft standards.")
    print(f"Currently found {len(current_drafts)} files in draft status.")

    # Files that should be draft but are not
    to_make_draft = official_drafts - current_drafts
    
    # Files that are draft but should not be
    to_make_active = current_drafts - official_drafts

    changes_made = 0
    
    print(f"\nFound {len(to_make_draft)} files to change to 'draft':")
    for file in sorted(list(to_make_draft)):
        print(f"- Processing {file.relative_to(ROOT)}...")
        if set_file_status(file, "draft", args.dry_run):
            if args.dry_run:
                print(f"  - WILL CHANGE TO DRAFT: {file.relative_to(ROOT)}")
            else:
                print(f"  - CHANGED TO DRAFT: {file.relative_to(ROOT)}")
            changes_made += 1

    print(f"\nFound {len(to_make_active)} files to change to 'active':")
    for file in sorted(list(to_make_active)):
        print(f"- Processing {file.relative_to(ROOT)}...")
        if set_file_status(file, "active", args.dry_run):
            if args.dry_run:
                print(f"  - WILL CHANGE TO ACTIVE: {file.relative_to(ROOT)}")
            else:
                print(f"  - CHANGED TO ACTIVE: {file.relative_to(ROOT)}")
            changes_made += 1

    print(f"\n--- Summary ---")
    if args.dry_run:
        print(f"Dry run complete. {changes_made} files would be changed.")
    else:
        print(f"Live run complete. {changes_made} files were changed.")
        print("\nVerifying final state...")
        final_drafts = get_current_draft_files(STANDARDS_DIR)
        print(f"Final count of draft files is: {len(final_drafts)}")
        if len(final_drafts) == len(official_drafts):
            print(f"Verification successful. Count is {len(official_drafts)}.")
            return 0
        else:
            print(f"Verification FAILED. Expected {len(official_drafts)}, but found {len(final_drafts)}.")
            return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main()) 