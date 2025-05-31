import os
import re
import yaml # Requires PyYAML (ensure it's in your environment)
import sys
import argparse

# Expected standard_id regex (all uppercase, domain + hyphen + rest-of-id)
# This regex is for validation within this script if needed, but primary logic is direct string manipulation.
STANDARD_ID_TARGET_REGEX = r"""^[A-Z]{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*$"""

def get_frontmatter_and_content_indices(file_content_lines):
    """
    Parses a list of file lines to find the start and end of YAML frontmatter.
    Returns: (fm_start_line_idx, fm_end_line_idx, content_start_line_idx)
    Indices are 0-based for list slicing. content_start_line_idx is after the second '---'.
    Returns (None, None, None) if no valid frontmatter block is found.
    """
    if not file_content_lines or not file_content_lines[0].strip() == "---":
        return None, None, None

    fm_end_line_idx = -1
    for i, line in enumerate(file_content_lines[1:]):
        if line.strip() == "---":
            fm_end_line_idx = i + 1 # 0-based index in original list
            break
    
    if fm_end_line_idx == -1:
        return None, None, None # No closing '---'

    # fm_start_line_idx for frontmatter content is 1 (after first '---')
    # fm_end_line_idx is the line *with* the second '---'
    # content_start_line_idx is after the second '---'
    return 1, fm_end_line_idx, fm_end_line_idx + 1

def process_file(filepath, dry_run=True):
    """
    Processes a single Markdown file to:
    1. Uppercase its standard_id in frontmatter.
    2. Change -changelog to -CHANGELOG in standard_id.
    3. If filename ends with -changelog.md, prepare to rename it to -CHANGELOG.md.
    Returns new_filepath if rename is needed, else None.
    Modifies file content in place if not dry_run.
    """
    print(f"INFO: Processing: {filepath}")
    made_fm_change = False
    original_std_id = None
    updated_std_id = None
    current_filename = os.path.basename(filepath) # Define current_filename earlier for use in suffix logic
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        fm_content_start_idx, fm_delimiter_end_idx, body_start_idx = get_frontmatter_and_content_indices(lines)

        if fm_content_start_idx is None:
            print(f"  WARN: No YAML frontmatter block found in {filepath}. Skipping frontmatter processing.")
        else:
            frontmatter_str = "".join(lines[fm_content_start_idx:fm_delimiter_end_idx])
            try:
                # Preserve comments and style if possible, though basic dump might lose them
                # Using a basic load/dump for now. ruamel.yaml is better for preserving style.
                frontmatter_data = yaml.safe_load(frontmatter_str)
                
                if isinstance(frontmatter_data, dict) and "standard_id" in frontmatter_data:
                    original_std_id = str(frontmatter_data["standard_id"]) # Ensure string
                    
                    # Convert entire standard_id to uppercase first
                    temp_std_id = original_std_id.upper()
                    
                    # Ensure -changelog (any case) becomes -CHANGELOG
                    # More robustly replace if it ends with -changlog or -changelog (any case)
                    if re.search(r"-CHANGELOG$", temp_std_id, re.IGNORECASE):
                        temp_std_id = re.sub(r"-CHANGELOG$", "-CHANGELOG", temp_std_id, flags=re.IGNORECASE)
                    elif current_filename.upper().endswith("-CHANGELOG.MD") and not temp_std_id.endswith("-CHANGELOG"):
                        # If filename clearly indicates it's a changelog, ensure ID has the suffix
                        if not temp_std_id.endswith("-CHANGELOG"):
                            temp_std_id += "-CHANGELOG"

                    if temp_std_id != original_std_id:
                        frontmatter_data["standard_id"] = temp_std_id
                        updated_std_id = temp_std_id
                        made_fm_change = True
                        print(f"  CHANGE (standard_id): '{original_std_id}' -> '{updated_std_id}'")
                elif isinstance(frontmatter_data, dict): # Frontmatter is dict but no standard_id
                    print(f"  INFO: No 'standard_id' key in frontmatter for {filepath}.")
                else: # Frontmatter not a dict
                    print(f"  WARN: Frontmatter in {filepath} is not a dictionary. Skipping standard_id update.")

                if made_fm_change and not dry_run:
                    # Re-dump YAML carefully
                    try:
                        updated_frontmatter_block_str = yaml.dump(frontmatter_data, sort_keys=False, allow_unicode=True, width=float("inf"))
                    except Exception as e_yaml_dump: # Catch potential issues with custom tags if any
                        print(f"  WARN: Could not re-serialize frontmatter for {filepath} with full width due to: {e_yaml_dump}. Attempting with default width.")
                        updated_frontmatter_block_str = yaml.dump(frontmatter_data, sort_keys=False, allow_unicode=True) # Default width

                    new_file_lines = ["---\n"]
                    for line_fm in updated_frontmatter_block_str.splitlines():
                        new_file_lines.append(line_fm + "\n")
                    new_file_lines.append("---\n")
                    if body_start_idx < len(lines):
                        new_file_lines.extend(lines[body_start_idx:])
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.writelines(new_file_lines)
                    print(f"  SUCCESS: Updated frontmatter in {filepath}")

            except yaml.YAMLError as e:
                print(f"  ERROR: Invalid YAML in frontmatter for {filepath}: {e}. Skipping frontmatter update.")
            except Exception as e_fm_proc:
                print(f"  ERROR: Could not process frontmatter for {filepath}: {e_fm_proc}. Skipping frontmatter update.")

        # Filename processing
        id_for_filename_base = None
        if updated_std_id: # An ID was changed in FM
            id_for_filename_base = updated_std_id
        elif original_std_id: # FM had an ID, but it wasn't changed by the logic above (e.g. already uppercase)
            id_for_filename_base = original_std_id.upper() # Ensure we use uppercase version for filename consistency
        
        if id_for_filename_base:
            # Ensure base is all uppercase
            correct_filename_base = id_for_filename_base.upper() 
            
            # Determine correct suffix for filename
            is_changelog_file_by_name = current_filename.upper().endswith("-CHANGELOG.MD")
            is_changelog_id_by_suffix = correct_filename_base.endswith("-CHANGELOG")

            if is_changelog_id_by_suffix or is_changelog_file_by_name:
                # If ID ends with -CHANGELOG, or filename implies it's a changelog, ensure base ID reflects this
                if not correct_filename_base.endswith("-CHANGELOG"):
                    correct_filename_base += "-CHANGELOG"
                correct_filename = correct_filename_base + ".md"
            else: # Non-changelog file
                correct_filename = correct_filename_base + ".md"

            if current_filename != correct_filename:
                new_filepath_candidate = os.path.join(os.path.dirname(filepath), correct_filename)
                print(f"  CHANGE (filename): '{current_filename}' -> '{correct_filename}' (Proposed: {new_filepath_candidate})")
                if not dry_run:
                    # Check for collision only if the transformation results in a different name
                    # (case difference on Windows might be an issue, but os.rename handles it)
                    if os.path.exists(new_filepath_candidate) and filepath.lower() != new_filepath_candidate.lower():
                        print(f"  ERROR: Target filename {new_filepath_candidate} already exists. Skipping rename for {filepath}.")
                    else:
                        try:
                            os.rename(filepath, new_filepath_candidate)
                            print(f"  SUCCESS: Renamed {filepath} to {new_filepath_candidate}")
                            return new_filepath_candidate
                        except Exception as e_rename:
                            print(f"  ERROR: Failed to rename {filepath} to {new_filepath_candidate}: {e_rename}")
            # else:
                # print(f"  INFO: Filename '{current_filename}' already matches its standard_id casing/structure.")

    except FileNotFoundError:
        print(f"  ERROR: File not found during processing: {filepath}")
    except Exception as e:
        print(f"  ERROR: Failed to process file {filepath}: {e}")
    return None

def main():
    parser = argparse.ArgumentParser(description="Refactor standard_id usage and filenames to be ALL UPPERCASE and ensure -CHANGELOG suffix.")
    parser.add_argument("target_dirs", nargs='+', help="One or more directories to scan for Markdown files.")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without making changes.")
    
    args = parser.parse_args()

    print(f"Starting ID and filename refactoring. Dry run: {args.dry_run}")
    
    all_files_to_process = []
    for target_dir in args.target_dirs:
        abs_target_dir = os.path.abspath(target_dir)
        if not os.path.isdir(abs_target_dir):
            print(f"ERROR: Target directory not found: {abs_target_dir}. Skipping.")
            continue
        print(f"Scanning directory: {abs_target_dir}")
        for root, _, files in os.walk(abs_target_dir):
            for filename in files:
                if filename.endswith(".md"):
                    all_files_to_process.append(os.path.join(root, filename))
    
    print(f"Found {len(all_files_to_process)} Markdown files to check.")

    # Create a copy of the list for iteration as filenames might change
    # This is safer if renames affect the order or content of os.walk on subsequent iterations
    # for complex scenarios, but usually os.walk snapshot is at the beginning of its own loop.
    # A more robust way for renames is to collect all changes and apply them in a second pass,
    # or carefully manage the list of files to process.
    # For this script, we process and rename one by one.
    
    # Using a copy of the list for iteration as items might be effectively "removed" by rename
    # or their processing order could be sensitive to changes if we were re-walking.
    # For now, this single pass over the initially found files should be okay.
    
    # Let's refine the loop to handle processing potentially renamed files,
    # although the script currently renames and then the outer loop continues with original paths.
    # A better approach for robustness with renames might be more complex than a single pass.
    # The current `process_file` returns the new path, but the loop doesn't use it to update its iteration.
    # This will be a limitation: if a file is renamed, and was later in the all_files_to_process list,
    # the script will try to process it by its old name and fail.
    # A truly robust solution would collect all intended changes in a dry run, then apply them,
    # or use a while loop and manage the list of files to process dynamically.

    # For now, stick to the simpler loop, acknowledging this limitation for widespread renames.
    # The user should run dry-run first, review, then run actual.

    for i in range(len(all_files_to_process)):
        filepath_to_process = all_files_to_process[i]
        if not os.path.exists(filepath_to_process): # Skip if already renamed by a previous step in this run
            print(f"INFO: File {filepath_to_process} no longer exists (likely renamed). Skipping.")
            continue
        
        new_path = process_file(filepath_to_process, dry_run=args.dry_run)
        if new_path and new_path != filepath_to_process:
            # If we want to process the renamed file under its new name in the same run,
            # we'd need to update all_files_to_process or use a different loop structure.
            # For this version, we accept that it processes based on the initial scan.
            all_files_to_process[i] = new_path # Update path in list in case it's used later (though loop won't re-iterate over it)
            pass 
            
    print("Refactoring script finished.")

if __name__ == "__main__":
    # Example: python master-knowledge-base/tools/refactor_ids_filenames.py master-knowledge-base/standards/src --dry-run
    # Example: python master-knowledge-base/tools/refactor_ids_filenames.py master-knowledge-base/standards/src master-knowledge-base/standards/registry --dry-run
    # CAUTION: Run without --dry-run only after careful review of its output.
    main() 