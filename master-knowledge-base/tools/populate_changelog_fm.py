import os
import re
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap
import argparse
from datetime import datetime, timezone

# Expected standard_id regex for parent IDs
PARENT_ID_REGEX = r"^[A-Z]{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*$"

DEFAULT_CHANGELOG_INFO_TYPE = "changelog"
DEFAULT_CHANGELOG_VERSION = "1.0.0" # Initial version for the changelog doc itself
DEFAULT_CHANGELOG_TAGS = ["status/active", "content-type/changelog", "topic/governance"]
DEFAULT_CHANGELOG_CRITICALITY = "p3-low" # Ensure this is lowercase to match vocabulary
DEFAULT_CHANGELOG_IMPACT_AREAS = ["auditing", "version-tracking"]

# Defined key order for consistent frontmatter output for changelogs
# This should align with the main DEFINED_KEY_ORDER from kb_linter.py, 
# possibly subsetted or adapted for changelogs.
CHANGELOG_KEY_ORDER = [
    "title", "standard_id", "aliases", "tags", "kb-id", "info-type",
    "primary-topic", "related-standards", "version", "date-created",
    "date-modified", "primary_domain", "sub_domain", "scope_application",
    "criticality", "lifecycle_gatekeeper", "impact_areas", "change_log_url"
]

def get_frontmatter_and_content_indices(file_content_lines):
    if not file_content_lines or not file_content_lines[0].strip() == "---":
        return None, None, None # fm_str_lines, body_start_idx, existing_fm_data
    fm_end_line_idx = -1
    for i, line in enumerate(file_content_lines[1:]):
        if line.strip() == "---":
            fm_end_line_idx = i + 1 
            break
    if fm_end_line_idx == -1:
        return None, None, None
    
    fm_content_lines = file_content_lines[1:fm_end_line_idx]
    frontmatter_str = "".join(fm_content_lines)
    body_start_idx = fm_end_line_idx + 1
    
    yaml_parser = YAML(typ='safe') # Use ruamel.yaml for loading too, for consistency
    try:
        frontmatter_data = yaml_parser.load(frontmatter_str)
        return fm_content_lines, body_start_idx, frontmatter_data
    except Exception: # Broader exception for ruamel.yaml parsing
        print(f"  WARN: Invalid YAML in existing frontmatter. Will overwrite if forced.")
        return fm_content_lines, body_start_idx, None

def read_parent_frontmatter(parent_filepath):
    try:
        with open(parent_filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        _, _, parent_fm_data = get_frontmatter_and_content_indices(lines)
        if isinstance(parent_fm_data, dict):
            return parent_fm_data
        else:
            print(f"  WARN: Parent file {parent_filepath} has no valid dictionary frontmatter.")
    except FileNotFoundError:
        print(f"  WARN: Parent file {parent_filepath} not found.")
    except Exception as e:
        print(f"  ERROR: Could not read or parse parent file {parent_filepath}: {e}")
    return None

def process_changelog_file(changelog_filepath, dry_run=True, force_overwrite_fm=False):
    print(f"INFO: Processing changelog: {changelog_filepath}")
    changelog_filename = os.path.basename(changelog_filepath)
    
    match = re.match(r"(.+)-CHANGELOG\.MD", changelog_filename.upper()) # Ensure we match against uppercase
    if not match:
        print(f"  INFO: Filename {changelog_filename} does not match PARENT_ID-CHANGELOG.MD pattern. Skipping.")
        return False

    parent_id = match.group(1)
    if not re.match(PARENT_ID_REGEX, parent_id):
        print(f"  WARN: Derived parent ID '{parent_id}' from {changelog_filename} is not a valid standard ID. Skipping.")
        return False

    parent_filename = parent_id + ".MD"
    parent_filepath = os.path.join(os.path.dirname(changelog_filepath), parent_filename)

    lines = []
    try:
        with open(changelog_filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"  ERROR: Could not read changelog file {changelog_filepath}: {e}")
        return False

    _original_fm_lines, body_start_idx, existing_fm_data = get_frontmatter_and_content_indices(lines)

    if existing_fm_data is not None and not force_overwrite_fm:
        print(f"  INFO: File {changelog_filepath} already has frontmatter. Use --force to overwrite. Skipping.")
        return False
    
    if existing_fm_data is not None and force_overwrite_fm:
        print(f"  INFO: Overwriting existing frontmatter in {changelog_filepath} due to --force.")

    parent_fm = read_parent_frontmatter(parent_filepath)
    if not parent_fm:
        print(f"  WARN: Could not get frontmatter from parent '{parent_filepath}' for {changelog_filepath}. Cannot fully populate. Skipping.")
        # Optionally, could create a very minimal FM here, but better to have parent info.
        return False

    changelog_std_id = f"{parent_id}-CHANGELOG"
    current_time_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    parent_title = parent_fm.get('title', parent_id)

    # Use CommentedMap to preserve order for ruamel.yaml dump
    final_fm_data = CommentedMap()

    for key in CHANGELOG_KEY_ORDER:
        value = None
        if key == "title":
            value = f"Changelog: {parent_title}"
        elif key == "standard_id":
            value = changelog_std_id
        elif key == "aliases":
            value = [f"{parent_title} Changelog"]
        elif key == "tags":
            value = existing_fm_data.get('tags') if existing_fm_data and isinstance(existing_fm_data.get('tags'), list) else list(DEFAULT_CHANGELOG_TAGS)
        elif key == "kb-id":
            value = parent_fm.get('kb-id', 'standards')
        elif key == "info-type":
            value = DEFAULT_CHANGELOG_INFO_TYPE
        elif key == "primary-topic":
            value = f"Tracks changes for the standard: [[{parent_id}]] - {parent_title}."
        elif key == "related-standards":
            value = [parent_id]
        elif key == "version":
            value = parent_fm.get('version', DEFAULT_CHANGELOG_VERSION)
        elif key == "date-created":
            value = existing_fm_data.get('date-created') if existing_fm_data else parent_fm.get('date-created', current_time_iso)
        elif key == "date-modified":
            value = current_time_iso
        elif key == "primary_domain":
            value = parent_fm.get('primary_domain')
        elif key == "sub_domain":
            value = parent_fm.get('sub_domain')
        elif key == "scope_application":
            value = f"Tracks changes for [[{parent_id}]]."
        elif key == "criticality":
            value = (parent_fm.get('criticality') or DEFAULT_CHANGELOG_CRITICALITY).lower()
        elif key == "lifecycle_gatekeeper":
            value = parent_fm.get('lifecycle_gatekeeper')
        elif key == "impact_areas":
            value = parent_fm.get('impact_areas') if isinstance(parent_fm.get('impact_areas'), list) else list(DEFAULT_CHANGELOG_IMPACT_AREAS)
        elif key == "change_log_url":
            value = f"./{changelog_filename}"
        
        if value is not None: # Only add key if it has a value
            final_fm_data[key] = value

    print(f"  CONSTRUCTED FM for {changelog_filepath}: Title '{final_fm_data.get('title')}'")

    if not dry_run:
        yaml_dumper = YAML()
        yaml_dumper.indent(mapping=2, sequence=4, offset=2) # Preserves block style for sequences
        yaml_dumper.preserve_quotes = True
        
        import io
        string_stream = io.StringIO()
        yaml_dumper.dump(final_fm_data, string_stream)
        updated_frontmatter_block_str = string_stream.getvalue()
        string_stream.close()

        new_file_content_lines = ["---\n"]
        # Manually add a newline after each item from ruamel.yaml dump if needed
        # Ruamel often produces good formatting itself.
        new_file_content_lines.append(updated_frontmatter_block_str) 
        # updated_frontmatter_block_str likely ends with a newline from ruamel
        if not updated_frontmatter_block_str.endswith('\n'):
            new_file_content_lines.append("\n")
        
        new_file_content_lines.append("---\n")
        
        if body_start_idx is not None and body_start_idx < len(lines):
            new_file_content_lines.extend(lines[body_start_idx:])
        else: 
            new_file_content_lines.append("\n# Changelog\n\nThis document records the change history.\n")
        
        try:
            with open(changelog_filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_file_content_lines)
            print(f"  SUCCESS: {'Overwrote' if existing_fm_data else 'Added'} frontmatter to {changelog_filepath}")
            return True
        except Exception as e_write:
            print(f"  ERROR: Failed to write updated file {changelog_filepath}: {e_write}")
            return False
    else:
        print(f"  DRY RUN: Would {'overwrite' if existing_fm_data else 'add'} frontmatter to {changelog_filepath}")
        return True # Indicates a change would be made
    return False

def main():
    parser = argparse.ArgumentParser(description="Add or update frontmatter for changelog files based on their parent standards.")
    parser.add_argument("target_dirs", nargs='+', help="One or more directories to scan for Markdown files.")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without making changes.")
    parser.add_argument("--force", action="store_true", help="Force overwrite of existing frontmatter in changelog files.")
    args = parser.parse_args()

    print(f"Starting changelog frontmatter population. Dry run: {args.dry_run}, Force: {args.force}")
    
    files_processed_potentially_changed = 0
    files_actually_changed = 0
    total_files_scanned = 0

    for target_dir in args.target_dirs:
        abs_target_dir = os.path.abspath(target_dir)
        if not os.path.isdir(abs_target_dir):
            print(f"ERROR: Target directory {abs_target_dir} not found. Skipping.")
            continue
        print(f"Scanning directory: {abs_target_dir}")
        for root, _, files in os.walk(abs_target_dir):
            for filename in files:
                if filename.upper().endswith("-CHANGELOG.MD"):
                    total_files_scanned += 1
                    filepath = os.path.join(root, filename)
                    if process_changelog_file(filepath, dry_run=args.dry_run, force_overwrite_fm=args.force):
                        files_processed_potentially_changed +=1
                        if not args.dry_run:
                            files_actually_changed +=1
            
    print(f"Changelog frontmatter script finished. Scanned {total_files_scanned} potential changelog files.")
    if args.dry_run:
        print(f"  Files that would have frontmatter added/overwritten: {files_processed_potentially_changed}")
    else:
        print(f"  Files with frontmatter actually added/overwritten: {files_actually_changed}")

if __name__ == "__main__":
    main() 