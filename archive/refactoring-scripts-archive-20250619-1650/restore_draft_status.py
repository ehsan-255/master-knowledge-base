#!/usr/bin/env python3
"""
Restores the 'status' of 47 standards from 'active' back to 'draft'.

This script was created to correct a critical failure in the first Audit
Remediation Initiative, where the draft standards were not correctly restored
after an accidental promotion.

It reads the list of target files from the original project's tracking sheet
and surgically reverts their status in the frontmatter.
"""

import argparse
from pathlib import Path
import sys
import re

# Define project structure
ROOT = Path(__file__).resolve().parents[2]
TRACKING_SHEET_PATH = ROOT / 'archive/audit-remediation-initiative-completed-20250620-1710/l2-sl3-establish-draft-promotion-process-completed/draft-standards-tracking-sheet.md'

def get_draft_files_from_tracker(tracker_path: Path) -> list[Path]:
    """Parses the tracking sheet to get the list of file paths."""
    if not tracker_path.exists():
        print(f"Error: Tracking sheet not found at '{tracker_path}'")
        sys.exit(1)

    content = tracker_path.read_text(encoding='utf-8')
    # Regex to find markdown table rows and extract the file path
    # Example: | AS-KB-DIRECTORY-STRUCTURE | AS | standards/src/AS-KB-DIRECTORY-STRUCTURE.md | ... |
    path_pattern = re.compile(r'\|\s*([A-Z0-9-]+)\s*\|\s*[A-Z]{2}\s*\|\s*(standards/src/[^|\s]+?\.md)\s*\|')
    
    file_paths = [ROOT / path for _, path in path_pattern.findall(content)]
    
    if not file_paths or len(file_paths) < 40: # Expecting 47
        print(f"Error: Could only parse {len(file_paths)} file paths from the tracking sheet. Check the regex or file content.")
        sys.exit(1)
        
    return file_paths

def revert_status_in_file(file_path: Path, dry_run: bool):
    """Reads a file, changes the status, and writes it back."""
    if not file_path.exists():
        print(f"  - WARNING: File not found, skipping: {file_path}")
        return False, "Not Found"

    content = file_path.read_text(encoding='utf-8')
    
    # Use regex to replace the status field safely
    new_content, count = re.subn(
        r"(status:\s*)active", 
        r"\1draft", 
        content,
        flags=re.IGNORECASE
    )

    if count == 0:
        if "status: draft" in content:
             print(f"  - INFO: Status is already 'draft' in {file_path}")
             return False, "Already Draft"
        else:
             print(f"  - WARNING: 'status: active' not found in {file_path}")
             return False, "Not Found"

    if not dry_run:
        file_path.write_text(new_content, encoding='utf-8')
        
    return True, "Reverted"


def main():
    parser = argparse.ArgumentParser(description="Restore 'draft' status to 47 standards.")
    parser.add_argument('--dry-run', action='store_true', help="Preview changes without modifying files.")
    args = parser.parse_args()
    
    print("Starting restoration of draft standards...")
    if args.dry_run:
        print("--- DRY RUN MODE ---")

    draft_files = get_draft_files_from_tracker(TRACKING_SHEET_PATH)
    print(f"Found {len(draft_files)} standards to process from tracking sheet.")

    reverted_count = 0
    already_draft_count = 0
    not_found_count = 0

    for file in draft_files:
        changed, status = revert_status_in_file(file, args.dry_run)
        if changed:
            print(f"  - REVERTED: {file.relative_to(ROOT)}")
            reverted_count += 1
        else:
            if status == "Already Draft":
                already_draft_count += 1
            elif status == "Not Found":
                not_found_count += 1
    
    print("\n--- Summary ---")
    print(f"Total files processed: {len(draft_files)}")
    print(f"Files reverted to draft: {reverted_count}")
    print(f"Files already in draft: {already_draft_count}")
    print(f"Files where 'status: active' was not found: {not_found_count}")

    if not args.dry_run:
        print("\nVerification: Counting final draft files...")
        # Use the same glob pattern from the other script for consistency
        final_drafts = list((ROOT / 'standards' / 'src').glob('**/*.md'))
        final_draft_count = 0
        for md_file in final_drafts:
            if "status: draft" in md_file.read_text(encoding='utf-8'):
                final_draft_count += 1
        
        print(f"Final count of files with 'status: draft': {final_draft_count}")
        if final_draft_count == 47:
            print("✅ Verification successful. Count is 47.")
            return 0
        else:
            print(f"❌ Verification FAILED. Expected 47, but found {final_draft_count}.")
            return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main()) 