import os
import re
import argparse
import logging
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

# Regex for frontmatter change_log_url
FM_CHANGELOG_URL_REGEX = r"^\./(.+)-changelog\.md(#.*)?$"
# Regex for Markdown links in body
BODY_MD_LINK_REGEX = r"(\[([^\]]+)\]\(\./)([^/]+)-changelog\.md((?:#[^)]+)?\))"


def get_frontmatter_and_content_indices(file_content_lines):
    if not file_content_lines or not file_content_lines[0].strip() == "---":
        return None, None, 0
    fm_end_line_idx = -1
    for i, line in enumerate(file_content_lines[1:]):
        if line.strip() == "---":
            fm_end_line_idx = i + 1
            break
    if fm_end_line_idx == -1:
        return None, None, 0 # No closing '---'

    # fm_content_start_idx for ruamel.yaml is the line after '---'
    # fm_delimiter_end_idx is the line *with* the second '---'
    # body_start_idx is after the second '---'
    return 1, fm_end_line_idx, fm_end_line_idx + 1


def process_file(filepath, dry_run=True, repo_base_abs_path=None):
    if repo_base_abs_path is None:
        repo_base_abs_path = os.getcwd() # Default if not provided

    logging.debug(f"Processing file: {filepath}")
    made_change = False

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        logging.error(f"Could not read file {filepath}: {e}")
        return False

    fm_content_start_idx, fm_delimiter_end_idx, body_start_idx = get_frontmatter_and_content_indices(lines)

    yaml_parser = YAML()
    yaml_parser.preserve_quotes = True

    frontmatter_data = None
    if fm_content_start_idx is not None:
        frontmatter_str = "".join(lines[fm_content_start_idx:fm_delimiter_end_idx])
        try:
            frontmatter_data = yaml_parser.load(frontmatter_str)
        except Exception as e:
            logging.warning(f"Could not parse frontmatter for {filepath}: {e}")
            frontmatter_data = None # Treat as if no valid FM

    # 1. Process frontmatter change_log_url
    if isinstance(frontmatter_data, dict) and "change_log_url" in frontmatter_data:
        original_url = frontmatter_data["change_log_url"]
        if isinstance(original_url, str):
            match = re.match(FM_CHANGELOG_URL_REGEX, original_url)
            if match:
                base_name = match.group(1)
                anchor = match.group(2) if match.group(2) else ""
                new_filename_stem = f"{base_name}-CHANGELOG.MD" # Note .MD for changelogs
                new_url = f"./{new_filename_stem}{anchor}"

                # Check if the new target file exists
                current_file_dir = os.path.dirname(filepath)
                target_file_path = os.path.normpath(os.path.join(current_file_dir, new_filename_stem))

                if os.path.exists(target_file_path):
                    if original_url != new_url:
                        logging.info(f"Frontmatter change_log_url UPDATE in {filepath}: '{original_url}' -> '{new_url}'")
                        frontmatter_data["change_log_url"] = new_url
                        made_change = True
                else:
                    logging.debug(f"Target for potential FM change_log_url update '{new_filename_stem}' does not exist relative to {filepath}. Skipping this specific URL.")

    # 2. Process Markdown links in body
    body_content_str = "".join(lines[body_start_idx:])
    new_body_content_str = body_content_str

    # Use a function for substitution to check existence for each match
    def replace_link(m):
        nonlocal made_change # To modify made_change from outer scope
        link_prefix = m.group(1) # E.g. "[Link Text](./"
        base_name = m.group(3)
        anchor_and_suffix = m.group(4) # E.g. ".md#anchor)" or ".md)"

        new_changelog_filename_stem = f"{base_name}-CHANGELOG.MD"

        current_file_dir = os.path.dirname(filepath)
        target_file_path = os.path.normpath(os.path.join(current_file_dir, new_changelog_filename_stem))

        if os.path.exists(target_file_path):
            new_link = f"{link_prefix}{new_changelog_filename_stem}{anchor_and_suffix}"
            if m.group(0) != new_link:
                 logging.info(f"Markdown link UPDATE in {filepath}: '{m.group(0)}' -> '{new_link}'")
                 made_change = True
                 return new_link
        else:
            logging.debug(f"Target for potential Markdown link update '{new_changelog_filename_stem}' does not exist relative to {filepath}. Skipping this link.")
        return m.group(0) # No change

    new_body_content_str = re.sub(BODY_MD_LINK_REGEX, replace_link, new_body_content_str)

    if made_change and not dry_run:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                if fm_content_start_idx is not None: # Rewrite frontmatter if it existed
                    f.write("---\n")
                    yaml_dumper = YAML() # Use a new instance for dumping to keep styles
                    yaml_dumper.indent(mapping=2, sequence=4, offset=2)
                    yaml_dumper.preserve_quotes = True
                    yaml_dumper.dump(frontmatter_data, f)
                    f.write("---\n")
                f.write(new_body_content_str)
            logging.info(f"SUCCESS: Updated links in {filepath}")
        except Exception as e:
            logging.error(f"Failed to write updated file {filepath}: {e}")
            return False # Indicate change was not successfully written
    elif made_change and dry_run:
        logging.info(f"DRY RUN: Would update links in {filepath}")

    return made_change


def main():
    parser = argparse.ArgumentParser(description="Refactor changelog links in frontmatter (change_log_url) and Markdown body links.")
    parser.add_argument("--target-dir", default="master-knowledge-base/standards/src",
                        help="Target directory to scan for Markdown files, relative to repo-base. Default: master-knowledge-base/standards/src")
    parser.add_argument("--repo-base", default=".", help="Path to the repository root. Default is current directory.")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without making changes.")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="Set the logging level.")

    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log_level.upper()), format='%(levelname)s: %(message)s')

    repo_base_abs_path = os.path.abspath(args.repo_base)
    target_dir_abs = os.path.join(repo_base_abs_path, args.target_dir)

    if not os.path.isdir(target_dir_abs):
        logging.error(f"Target directory not found: {target_dir_abs}. Exiting.")
        return

    logging.info(f"Starting changelog link refactoring. Dry run: {args.dry_run}. Target directory: {target_dir_abs}")

    files_processed = 0
    files_changed_or_would_change = 0

    for root, _, files in os.walk(target_dir_abs):
        for filename in files:
            if filename.endswith(".md"):
                files_processed += 1
                filepath = os.path.join(root, filename)
                if process_file(filepath, dry_run=args.dry_run, repo_base_abs_path=repo_base_abs_path):
                    files_changed_or_would_change += 1

    logging.info(f"Changelog link refactoring finished. Scanned {files_processed} files.")
    if args.dry_run:
        logging.info(f"  Files that would have links updated: {files_changed_or_would_change}")
    else:
        logging.info(f"  Files where links were updated: {files_changed_or_would_change}")

if __name__ == "__main__":
    main()
