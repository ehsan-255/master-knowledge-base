import os
import re
import yaml
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

def process_tags_in_file(filepath, dry_run=True):
    print(f"INFO: Processing tags in: {filepath}")
    made_change_to_fm_data = False

    lines = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e_outer:
        print(f"  ERROR: Failed to read file {filepath}: {e_outer}")
        return False

    try:
        fm_content_start_idx, fm_delimiter_end_idx, body_start_idx = get_frontmatter_and_content_indices(lines)

        if fm_content_start_idx is None:
            return False

        frontmatter_str = "".join(lines[fm_content_start_idx:fm_delimiter_end_idx])
        frontmatter_data = yaml.safe_load(frontmatter_str)

        if isinstance(frontmatter_data, dict) and "tags" in frontmatter_data:
            original_tags = frontmatter_data.get("tags")
            if not isinstance(original_tags, list):
                print(f"  WARN: Tags field in {filepath} is not a list. Skipping tag processing.")
                return False

            new_tags = []
            tags_were_modified = False
            for tag in original_tags:
                if isinstance(tag, str):
                    if tag.lower().startswith("criticality/") and tag != tag.lower():
                        new_tag = tag.lower()
                        print(f"  CHANGE (tag casing): '{tag}' -> '{new_tag}' in {filepath}")
                        new_tags.append(new_tag)
                        tags_were_modified = True
                    else:
                        new_tags.append(tag)
                else:
                    new_tags.append(tag)

            if tags_were_modified:
                frontmatter_data["tags"] = new_tags
                made_change_to_fm_data = True

                if not dry_run:
                    updated_frontmatter_block_str = ""
                    try:
                        updated_frontmatter_block_str = yaml.dump(frontmatter_data, sort_keys=False, allow_unicode=True, width=float("inf"))
                    except Exception as e_yaml_dump:
                        print(f"  WARN: Could not re-serialize frontmatter (tags) for {filepath} with full width due to: {e_yaml_dump}. Attempting with default width.")
                        updated_frontmatter_block_str = yaml.dump(frontmatter_data, sort_keys=False, allow_unicode=True)

                    new_file_content_lines = ["---\n"]
                    for line_fm in updated_frontmatter_block_str.splitlines():
                        new_file_content_lines.append(line_fm + "\n")
                    new_file_content_lines.append("---\n")
                    if body_start_idx < len(lines):
                        new_file_content_lines.extend(lines[body_start_idx:])

                    try:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.writelines(new_file_content_lines)
                        print(f"  SUCCESS: Updated tags in {filepath}")
                    except Exception as e_write:
                        print(f"  ERROR: Failed to write updated file {filepath}: {e_write}")
        return made_change_to_fm_data

    except yaml.YAMLError as e_yaml:
        print(f"  ERROR: Invalid YAML in {filepath}: {e_yaml}. Skipping.")
    except FileNotFoundError:
        print(f"  ERROR: File not found during tag processing: {filepath}")
    except Exception as e_outer:
        print(f"  ERROR: Failed to process tags in file {filepath}: {e_outer}")
    return False

def main():
    parser = argparse.ArgumentParser(description="Convert criticality/* tags to lowercase in frontmatter.")
    parser.add_argument("target_dirs", nargs='+', help="One or more directories to scan for Markdown files.")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without making changes.")

    args = parser.parse_args()

    print(f"Starting criticality tag casing refactoring. Dry run: {args.dry_run}")

    files_with_actual_changes_count = 0
    total_files_scanned = 0

    for target_dir in args.target_dirs:
        abs_target_dir = os.path.abspath(target_dir)
        if not os.path.isdir(abs_target_dir):
            print(f"ERROR: Target directory not found: {abs_target_dir}. Skipping.")
            continue
        print(f"Scanning directory: {abs_target_dir}")
        for root, _, files in os.walk(abs_target_dir):
            for filename in files:
                if filename.endswith(".md"):
                    total_files_scanned += 1
                    filepath = os.path.join(root, filename)
                    if process_tags_in_file(filepath, dry_run=args.dry_run):
                        if not args.dry_run:
                            files_with_actual_changes_count += 1

    print(f"Tag casing refactoring finished. Scanned {total_files_scanned} files.")
    if args.dry_run:
        print(f"  (Dry run mode: Changes were identified but not written. Re-run without --dry-run to apply.)")
    else:
        print(f"  Files with actual changes written: {files_with_actual_changes_count}")

if __name__ == "__main__":
    main()