import os
import yaml # Requires PyYAML
import argparse

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
        print(f"  ERROR: Failed to read file {filepath}: {e_read}")
        return False

    try:
        fm_content_start_idx, fm_delimiter_end_idx, body_start_idx = get_frontmatter_and_content_indices(lines)

        if fm_content_start_idx is None:
            return False

        frontmatter_str = "".join(lines[fm_content_start_idx:fm_delimiter_end_idx])
        frontmatter_data = yaml.safe_load(frontmatter_str)

        if isinstance(frontmatter_data, dict) and "criticality" in frontmatter_data:
            original_criticality_value = frontmatter_data.get("criticality")
            if isinstance(original_criticality_value, str) and original_criticality_value != original_criticality_value.lower():
                new_criticality_value = original_criticality_value.lower()
                print(f"  CHANGE (criticality value) in {filepath}: '{original_criticality_value}' -> '{new_criticality_value}'")
                frontmatter_data["criticality"] = new_criticality_value
                made_change = True

            if made_change and not dry_run:
                updated_frontmatter_block_str = ""
                try:
                    updated_frontmatter_block_str = yaml.dump(frontmatter_data, sort_keys=False, allow_unicode=True, width=float("inf"))
                except Exception as e_yaml_dump:
                    print(f"  WARN: Could not re-serialize frontmatter (criticality) for {filepath} with full width: {e_yaml_dump}. Attempting default.")
                    updated_frontmatter_block_str = yaml.dump(frontmatter_data, sort_keys=False, allow_unicode=True)

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
                    print(f"  SUCCESS: Updated criticality field in {filepath}")
                except Exception as e_write:
                    print(f"  ERROR: Failed to write updated file {filepath}: {e_write}")
                    # Revert change in memory if write fails? For now, just report.
                    return False # Indicate change was not successfully written
        return made_change

    except yaml.YAMLError as e_yaml:
        print(f"  ERROR: Invalid YAML in {filepath}: {e_yaml}. Skipping.")
    except Exception as e_outer:
        print(f"  ERROR: Failed to process criticality field in file {filepath}: {e_outer}")
    return False

def main():
    parser = argparse.ArgumentParser(description="Convert 'criticality' field value to lowercase in frontmatter.")
    parser.add_argument("target_dirs", nargs='+', help="One or more directories to scan.")
    parser.add_argument("--dry-run", action="store_true", help="Dry run, no actual changes.")
    args = parser.parse_args()

    print(f"Starting 'criticality' field value refactoring. Dry run: {args.dry_run}")
    
    files_with_potential_changes = 0
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
                if filename.endswith(".md"):
                    total_files_scanned += 1
                    filepath = os.path.join(root, filename)
                    if process_criticality_field_in_file(filepath, dry_run=args.dry_run):
                        files_with_potential_changes +=1 # Counts if a change was identified
                        if not args.dry_run: # If not dry run, this means change was also attempted to be written
                            files_actually_changed +=1 # This count might be slightly off if write fails but made_change was True

    print(f"Criticality field refactoring finished. Scanned {total_files_scanned} files.")
    if args.dry_run:
        print(f"  Files that would have 'criticality' field changed: {files_with_potential_changes}")
    else:
        print(f"  Files with 'criticality' field actually changed: {files_actually_changed}")

if __name__ == "__main__":
    main()