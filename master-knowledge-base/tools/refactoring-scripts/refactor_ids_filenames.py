import os
import re
import yaml # Requires PyYAML (ensure it's in your environment)
import sys
import argparse
import logging # Added

# Expected standard_id regex (all uppercase, domain + hyphen + rest-of-id)
# This regex is for validation within this script if needed, but primary logic is direct string manipulation.
STANDARD_ID_TARGET_REGEX = r"""^[A-Z]{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*$""" # Used for validation
CHANGELOG_SUFFIX = "-CHANGELOG" # Canonical suffix for IDs
CHANGELOG_FILE_SUFFIX = "-CHANGELOG.MD" # Canonical suffix for filenames
NORMAL_FILE_SUFFIX = ".md" # Canonical suffix for normal filenames

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
    logging.info(f"Processing: {filepath}")
    made_fm_change = False
    original_std_id = None
    updated_std_id = None
    current_filename = os.path.basename(filepath) # Define current_filename earlier for use in suffix logic
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        fm_content_start_idx, fm_delimiter_end_idx, body_start_idx = get_frontmatter_and_content_indices(lines)

        if fm_content_start_idx is None:
            logging.warning(f"No YAML frontmatter block found in {filepath}. Skipping frontmatter processing.")
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
                        logging.info(f"Frontmatter standard_id CHANGE: '{original_std_id}' -> '{updated_std_id}' in {filepath}")
                elif isinstance(frontmatter_data, dict):
                    logging.info(f"No 'standard_id' key in frontmatter for {filepath}.")
                else:
                    logging.warning(f"Frontmatter in {filepath} is not a dictionary. Skipping standard_id update.")

                # Title update logic (if standard_id changed and title seems derived)
                if updated_std_id and "title" in frontmatter_data:
                    original_title = frontmatter_data["title"]
                    # Check if title seems derived from old ID (case-insensitive)
                    # This is a heuristic. More complex title derivations won't be caught.
                    if original_std_id and (original_title.lower() == original_std_id.lower() or
                                            original_title.lower() == original_std_id.lower().replace(CHANGELOG_SUFFIX.lower(), "")):
                        new_title = updated_std_id # Simplest is to set title to new ID
                        if updated_std_id.endswith(CHANGELOG_SUFFIX):
                            # Make title more human-readable for changelogs
                            base_id_for_title = updated_std_id[:-len(CHANGELOG_SUFFIX)]
                            new_title = f"Changelog: {base_id_for_title}"

                        if frontmatter_data["title"] != new_title:
                            logging.info(f"Frontmatter title CHANGE: '{frontmatter_data['title']}' -> '{new_title}' in {filepath}")
                            frontmatter_data["title"] = new_title
                            made_fm_change = True


                if made_fm_change and not dry_run:
                    try:
                        updated_frontmatter_block_str = yaml.dump(frontmatter_data, Dumper=yaml.SafeDumper, sort_keys=False, allow_unicode=True, width=float("inf"))
                    except Exception as e_yaml_dump:
                        logging.warning(f"Could not re-serialize frontmatter for {filepath} with full width due to: {e_yaml_dump}. Attempting with default width.")
                        updated_frontmatter_block_str = yaml.dump(frontmatter_data, Dumper=yaml.SafeDumper, sort_keys=False, allow_unicode=True)

                    new_file_lines = ["---\n"]
                    for line_fm in updated_frontmatter_block_str.splitlines():
                        new_file_lines.append(line_fm + "\n")
                    new_file_lines.append("---\n")
                    if body_start_idx < len(lines): # body_start_idx could be None if no FM
                        new_file_lines.extend(lines[body_start_idx:])
                    else: # No body if frontmatter was missing or malformed to start.
                        new_file_lines.append("\n")
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.writelines(new_file_lines)
                    logging.info(f"SUCCESS: Updated frontmatter in {filepath}")

            except yaml.YAMLError as e:
                logging.error(f"Invalid YAML in frontmatter for {filepath}: {e}. Skipping frontmatter update.")
            except Exception as e_fm_proc:
                logging.error(f"Could not process frontmatter for {filepath}: {e_fm_proc}. Skipping frontmatter update.")

        # Filename processing
        # Determine the canonical standard_id to use for filename generation
        # This should be the *updated* (corrected case) standard_id from frontmatter if available and valid
        # Otherwise, fall back to a corrected version of original_std_id, or finally, derive from filename if no ID in FM.
        
        id_for_filename = None
        if updated_std_id: # ID was changed in FM, use this new one
            id_for_filename = updated_std_id
        elif original_std_id: # ID was present in FM but not changed by logic above (e.g. already uppercase)
            id_for_filename = original_std_id
        else: # No standard_id in frontmatter, try to derive from current filename (and then uppercase it)
            base_name_no_ext = os.path.splitext(current_filename)[0]
            id_for_filename = base_name_no_ext # This might need further cleanup if filename is not ID-like
            logging.info(f"No standard_id in frontmatter of {filepath}, deriving target ID from filename: {id_for_filename}")

        if id_for_filename:
            # Canonical ID form: ALL UPPERCASE. If it's a changelog, it MUST end in -CHANGELOG.
            canonical_id = id_for_filename.upper()
            is_changelog_by_filename = current_filename.upper().endswith(CHANGELOG_FILE_SUFFIX)
            
            if is_changelog_by_filename and not canonical_id.endswith(CHANGELOG_SUFFIX):
                canonical_id += CHANGELOG_SUFFIX
            elif canonical_id.endswith(CHANGELOG_SUFFIX) and not is_changelog_by_filename:
                # This case is tricky: ID implies changelog, but filename doesn't.
                # For now, assume ID is source of truth for "is changelog" status for suffix.
                logging.warning(f"ID {canonical_id} ends with {CHANGELOG_SUFFIX} but filename {current_filename} does not. Filename will be corrected.")
                is_changelog_by_filename = True # Treat as changelog for filename suffix rule

            if is_changelog_by_filename: # This now means it *should* be a changelog
                # Ensure canonical_id also has the suffix if filename implies it's a changelog
                if not canonical_id.endswith(CHANGELOG_SUFFIX):
                    canonical_id += CHANGELOG_SUFFIX
                correct_filename = canonical_id + ".MD" # Uppercase .MD for changelogs
            else:
                # Ensure canonical_id does NOT have suffix if it's not a changelog
                if canonical_id.endswith(CHANGELOG_SUFFIX):
                    canonical_id = canonical_id[:-len(CHANGELOG_SUFFIX)]
                correct_filename = canonical_id + NORMAL_FILE_SUFFIX # Lowercase .md for non-changelogs

            if current_filename != correct_filename:
                new_filepath_candidate = os.path.join(os.path.dirname(filepath), correct_filename)
                logging.info(f"Filename CHANGE: '{current_filename}' -> '{correct_filename}' (Proposed: {new_filepath_candidate})")
                if not dry_run:
                    if os.path.exists(new_filepath_candidate) and filepath.lower() != new_filepath_candidate.lower():
                        logging.error(f"Target filename {new_filepath_candidate} already exists. Skipping rename for {filepath}.")
                    else:
                        try:
                            # Robust rename for case changes
                            if filepath.lower() == new_filepath_candidate.lower() and filepath != new_filepath_candidate:
                                temp_name = filepath + ".tmp_rename"
                                os.rename(filepath, temp_name)
                                logging.debug(f"Renamed {filepath} to {temp_name} for case change.")
                                os.rename(temp_name, new_filepath_candidate)
                                logging.debug(f"Renamed {temp_name} to {new_filepath_candidate}.")
                            else:
                                os.rename(filepath, new_filepath_candidate)
                            logging.info(f"SUCCESS: Renamed {filepath} to {new_filepath_candidate}")
                            return new_filepath_candidate
                        except Exception as e_rename:
                            logging.error(f"Failed to rename {filepath} to {new_filepath_candidate}: {e_rename}")
            else:
                 logging.info(f"Filename '{current_filename}' already matches its standard_id casing/structure.")

    except FileNotFoundError:
        logging.error(f"File not found during processing: {filepath}")
    except Exception as e:
        logging.error(f"Failed to process file {filepath}: {e}")
    return None

def main():
    parser = argparse.ArgumentParser(description="Refactor standard_id and filenames to uppercase, ensure -CHANGELOG.MD suffix for changelogs, and update titles if derived.")
    parser.add_argument("target_dirs", nargs='+', help="One or more directories to scan for Markdown files.")
    parser.add_argument("--repo-base", default=".", help="Path to the repository root. Default is current directory. (Currently unused by script logic but good for future use).")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without making changes.")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="Set the logging level.")
    
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log_level.upper()), format='%(levelname)s: %(message)s')

    logging.info(f"Starting ID and filename refactoring. Dry run: {args.dry_run}")
    
    all_files_to_process = []
    for target_dir_rel in args.target_dirs:
        abs_target_dir = os.path.abspath(target_dir_rel)
        if not os.path.isdir(abs_target_dir):
            logging.error(f"Target directory not found: {abs_target_dir} (from '{target_dir_rel}'). Skipping.")
            continue
        logging.info(f"Scanning directory: {abs_target_dir}")
        for root, _, files in os.walk(abs_target_dir):
            for filename in files:
                if filename.endswith(".md") or filename.endswith(".MD"): # Catch both cases for initial scan
                    all_files_to_process.append(os.path.join(root, filename))
    
    logging.info(f"Found {len(all_files_to_process)} Markdown files to check.")
    
    processed_paths_map = {} # Store old_path -> new_path for multi-stage processing

    for filepath_to_process in all_files_to_process:
        if not os.path.exists(filepath_to_process):
            # Check if it was processed under a different key if path normalization is tricky
            normalized_original = os.path.normpath(filepath_to_process)
            found_in_map = False
            for k,v in processed_paths_map.items():
                if os.path.normpath(k) == normalized_original or os.path.normpath(v) == normalized_original:
                    found_in_map = True
                    break
            if found_in_map:
                 logging.info(f"File {filepath_to_process} no longer exists (likely renamed and processed). Skipping.")
                 continue
            else: # If truly not found and not in map, then it's an issue or was deleted.
                 logging.warning(f"File {filepath_to_process} not found during iteration start. Skipping.")
                 continue

        new_path = process_file(filepath_to_process, dry_run=args.dry_run)
        if new_path and new_path != filepath_to_process:
            processed_paths_map[filepath_to_process] = new_path
            
    logging.info("Refactoring script finished.")

if __name__ == "__main__":
    # Example: python master-knowledge-base/tools/refactor_ids_filenames.py master-knowledge-base/standards/src --dry-run
    # Example: python master-knowledge-base/tools/refactor_ids_filenames.py master-knowledge-base/standards/src master-knowledge-base/standards/registry --dry-run
    # CAUTION: Run without --dry-run only after careful review of its output.
    main() 