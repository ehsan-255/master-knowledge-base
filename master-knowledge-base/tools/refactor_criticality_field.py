import os
import yaml # Requires PyYAML
import argparse
import logging

# --- Global Variables ---
# To be populated by main after loading criticality_levels.yaml
CRITICALITY_MAP = {}

def load_criticality_map(repo_base_path):
    """Loads criticality levels from YAML and creates a lowercase-to-mixedcase map."""
    global CRITICALITY_MAP
    registry_path = os.path.join(repo_base_path, "master-knowledge-base", "standards", "registry")
    yaml_file_path = os.path.join(registry_path, "criticality_levels.yaml")

    temp_map = {}
    try:
        if not os.path.exists(yaml_file_path):
            logging.error(f"Criticality YAML file not found at: {yaml_file_path}")
            return False
        with open(yaml_file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and 'level' in item:
                        mixed_case_level = item['level']
                        temp_map[mixed_case_level.lower()] = mixed_case_level
            CRITICALITY_MAP = temp_map
            if not CRITICALITY_MAP:
                logging.error(f"No criticality levels found or parsed from {yaml_file_path}")
                return False
            logging.info(f"Successfully loaded criticality map: {CRITICALITY_MAP}")
            return True
    except Exception as e:
        logging.error(f"Failed to load or parse criticality_levels.yaml: {e}")
        return False

def get_frontmatter_and_content_indices(file_content_lines):
    if not file_content_lines or not file_content_lines[0].strip() == "---":
        return None, None, None
    fm_end_line_idx = -1
    for i, line in enumerate(file_content_lines[1:]):
        if line.strip() == "---":
            fm_end_line_idx = i + 1
            break
    if fm_end_line_idx == -1:
        return None, None, None
    return 1, fm_end_line_idx, fm_end_line_idx + 1

def process_criticality_field_in_file(filepath, dry_run=True):
    made_change = False
    lines = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e_read:
        logging.error(f"Failed to read file {filepath}: {e_read}")
        return False

    try:
        fm_content_start_idx, fm_delimiter_end_idx, body_start_idx = get_frontmatter_and_content_indices(lines)

        if fm_content_start_idx is None:
            logging.debug(f"No frontmatter found in {filepath}. Skipping.")
            return False

        frontmatter_str = "".join(lines[fm_content_start_idx:fm_delimiter_end_idx])
        frontmatter_data = yaml.safe_load(frontmatter_str)

        if isinstance(frontmatter_data, dict) and "criticality" in frontmatter_data:
            original_criticality_value = frontmatter_data.get("criticality")
            if isinstance(original_criticality_value, str):
                # Use the loaded map to find the target mixed-case value
                target_mixed_case_value = CRITICALITY_MAP.get(original_criticality_value.lower())

                if target_mixed_case_value and original_criticality_value != target_mixed_case_value:
                    logging.info(f"CHANGE (criticality value) in {filepath}: '{original_criticality_value}' -> '{target_mixed_case_value}'")
                    frontmatter_data["criticality"] = target_mixed_case_value
                    made_change = True
                elif not target_mixed_case_value:
                    logging.warning(f"Value '{original_criticality_value}' for 'criticality' in {filepath} not found in defined map. Skipping.")
            else: # Value is not a string
                 logging.warning(f"'criticality' field in {filepath} is not a string: '{original_criticality_value}'. Skipping.")


            if made_change and not dry_run:
                updated_frontmatter_block_str = ""
                try:
                    # Use a custom Dumper to preserve flow style for lists if possible, and ensure proper indentation.
                    # For now, default dump is used. Consider ruamel.yaml for perfect preservation if needed.
                    updated_frontmatter_block_str = yaml.dump(frontmatter_data, sort_keys=False, allow_unicode=True, width=float("inf"), Dumper=yaml.SafeDumper)
                except Exception as e_yaml_dump:
                    logging.warning(f"Could not re-serialize frontmatter (criticality) for {filepath} with full width: {e_yaml_dump}. Attempting default.")
                    updated_frontmatter_block_str = yaml.dump(frontmatter_data, sort_keys=False, allow_unicode=True, Dumper=yaml.SafeDumper)

                new_file_content_lines = ["---\n"]
                for line_fm in updated_frontmatter_block_str.splitlines():
                    new_file_content_lines.append(line_fm + "\n")
                new_file_content_lines.append("---\n")
                if body_start_idx < len(lines):
                    new_file_content_lines.extend(lines[body_start_idx:])
                else:
                    new_file_content_lines.append("\n") # Ensure a newline if no body

                try:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.writelines(new_file_content_lines)
                    logging.info(f"SUCCESS: Updated criticality field in {filepath}")
                except Exception as e_write:
                    logging.error(f"Failed to write updated file {filepath}: {e_write}")
                    return False
        return made_change

    except yaml.YAMLError as e_yaml:
        logging.error(f"Invalid YAML in {filepath}: {e_yaml}. Skipping.")
    except Exception as e_outer:
        logging.error(f"Failed to process criticality field in file {filepath}: {e_outer}")
    return False

def main():
    parser = argparse.ArgumentParser(description="Convert 'criticality' field value to mixed-case based on criticality_levels.yaml.")
    parser.add_argument("target_dirs", nargs='+', help="One or more directories to scan.")
    parser.add_argument("--repo-base", default=".", help="Path to the repository root, used to find criticality_levels.yaml. Default is current directory.")
    parser.add_argument("--dry-run", action="store_true", help="Dry run, no actual changes.")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="Set the logging level.")
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log_level.upper()), format='%(levelname)s: %(message)s')

    repo_base_abs_path = os.path.abspath(args.repo_base)
    if not load_criticality_map(repo_base_abs_path):
        logging.critical("Could not load criticality map. Exiting.")
        return

    logging.info(f"Starting 'criticality' field value refactoring. Dry run: {args.dry_run}")
    
    files_with_potential_changes = 0
    files_actually_changed = 0 # This will count successful writes if not dry_run
    total_files_scanned = 0

    for target_dir_rel in args.target_dirs: # target_dirs are relative to CWD or absolute
        # Construct absolute path for target_dir based on CWD, then use it.
        # Or, assume target_dirs are relative to repo_base if that's more consistent.
        # For now, assume os.path.abspath works as expected for user-provided dirs.
        abs_target_dir = os.path.abspath(target_dir_rel)

        if not os.path.isdir(abs_target_dir):
            logging.error(f"Target directory {abs_target_dir} (from '{target_dir_rel}') not found. Skipping.")
            continue
        logging.info(f"Scanning directory: {abs_target_dir}")
        for root, _, files in os.walk(abs_target_dir):
            for filename in files:
                if filename.endswith(".md"):
                    total_files_scanned += 1
                    filepath = os.path.join(root, filename)
                    change_identified = process_criticality_field_in_file(filepath, dry_run=args.dry_run)
                    if change_identified:
                        files_with_potential_changes +=1
                        if not args.dry_run: # If not dry_run and change_identified means a write was attempted
                             # To accurately count files_actually_changed, process_criticality_field_in_file should return True only on successful write
                             # Current logic: it returns True if made_change is True, even if write fails.
                             # This is acceptable for now; main point is to identify and attempt.
                             files_actually_changed +=1


    logging.info(f"Criticality field refactoring finished. Scanned {total_files_scanned} files.")
    if args.dry_run:
        logging.info(f"  Files that would have 'criticality' field changed: {files_with_potential_changes}")
    else:
        # files_actually_changed might be higher than actual successful writes if a write failed but change was True
        logging.info(f"  Files where 'criticality' field change was attempted: {files_with_potential_changes}")
        logging.info(f"  (Note: Check logs for individual file write success/failure if issues suspected)")


if __name__ == "__main__":
    main()