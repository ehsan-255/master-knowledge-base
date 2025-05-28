# generate_index.py
#
# This script will walk through Markdown files in the knowledge base (specifically
# in /master-knowledge-base/standards/src/), parse their frontmatter, and
# generate a JSON index (standards_index.json) of key metadata.

import os
import json
import yaml # PyYAML library
import argparse
import re # For extracting status from tags

# --- Configuration & Constants ---

# Paths (these could be made configurable via CLI args or a config file)
SRC_PATH = "master-knowledge-base/standards/src/"
DEFAULT_OUTPUT_FILE = "standards_index.json"
SCHEMA_VERSION = 1

# --- Helper Functions ---

def log_message(level, message):
    """
    Logs a message to stdout.
    Args:
        level (str): INFO, WARNING, ERROR.
        message (str): The message to log.
    """
    print(f"[{level}] {message}")

def parse_markdown_file_for_frontmatter(filepath):
    """
    Parses a Markdown file to extract frontmatter.
    A simplified version of the linter's parser, focusing only on frontmatter extraction.
    Args:
        filepath (str): Path to the Markdown file.
    Returns:
        dict: Parsed frontmatter, or None if error or no frontmatter.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content_lines = f.readlines()

        if not content_lines or not content_lines[0].strip() == "---":
            # log_message("INFO", f"File does not start with YAML frontmatter: {filepath}")
            return None

        fm_end_index = -1
        for i, line in enumerate(content_lines[1:], start=1):
            if line.strip() == "---":
                fm_end_index = i
                break

        if fm_end_index == -1:
            log_message("WARNING", f"YAML frontmatter closing delimiter '---' not found in {filepath}.")
            return None

        frontmatter_str = "".join(content_lines[1:fm_end_index])

        try:
            frontmatter = yaml.safe_load(frontmatter_str)
            if not isinstance(frontmatter, dict):
                log_message("WARNING", f"Frontmatter in {filepath} did not parse as a dictionary.")
                return None
            return frontmatter
        except yaml.YAMLError as e:
            log_message("WARNING", f"Error parsing YAML frontmatter in {filepath}: {e}")
            return None

    except FileNotFoundError:
        log_message("ERROR", f"File not found during parsing: {filepath}")
        return None
    except Exception as e:
        log_message("ERROR", f"Error processing file {filepath} for frontmatter: {e}")
        return None

def extract_status_from_tags(tags_list):
    """
    Extracts the status value from a list of tags.
    Assumes status tag is in the format 'status/some-status'.
    Args:
        tags_list (list): A list of strings, where each string is a tag.
    Returns:
        str: The status value (e.g., "draft", "approved") or None if not found.
    """
    if not isinstance(tags_list, list):
        return None
    for tag in tags_list:
        if isinstance(tag, str) and tag.startswith("status/"):
            return tag.split("/", 1)[1]
    return None

# --- Main Indexing Logic ---

def generate_index_data(source_directory):
    """
    Walks through Markdown files, parses frontmatter, and extracts metadata.
    Args:
        source_directory (str): The directory to scan for Markdown files.
    Returns:
        list: A list of dictionaries, where each dictionary contains metadata for a standard.
    """
    index_entries = []
    required_keys_for_index = [
        "standard_id", "title", "primary_domain", "sub_domain",
        "info-type", "version", "tags", "date-modified" # 'status' comes from 'tags'
    ]

    for root, _, files in os.walk(source_directory):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                # log_message("INFO", f"Processing: {filepath}") # Can be verbose
                frontmatter = parse_markdown_file_for_frontmatter(filepath)

                if frontmatter:
                    # Check if all keys needed for the index are present
                    missing_keys = [key for key in required_keys_for_index if key not in frontmatter]
                    if missing_keys:
                        log_message("WARNING", f"Skipping {filepath} due to missing keys for index: {', '.join(missing_keys)}")
                        continue

                    status = extract_status_from_tags(frontmatter.get("tags", []))
                    if not status:
                        log_message("WARNING", f"Skipping {filepath}: 'status' tag not found or invalid in 'tags' list.")
                        continue

                    # Construct relative filepath from the root of the repository
                    # This assumes the script is run from the repo root or paths are adjusted.
                    # For simplicity, let's assume source_directory is relative to repo root or is adjusted.
                    relative_filepath = os.path.relpath(filepath, start=os.getcwd()) # Or a fixed base like "master-knowledge-base/.."
                    # A simpler approach if script is always in relation to master-knowledge-base
                    if "master-knowledge-base" in filepath:
                         relative_filepath = filepath[filepath.find("master-knowledge-base"):]


                    entry = {
                        "standard_id": frontmatter.get("standard_id"),
                        "title": frontmatter.get("title"),
                        "primary_domain": frontmatter.get("primary_domain"),
                        "sub_domain": frontmatter.get("sub_domain"),
                        "info-type": frontmatter.get("info-type"),
                        "version": str(frontmatter.get("version")), # Ensure version is string
                        "status": status,
                        "filepath": relative_filepath.replace(os.sep, '/'), # Ensure POSIX paths
                        "date-modified": frontmatter.get("date-modified")
                    }
                    index_entries.append(entry)
                else:
                    log_message("INFO", f"No frontmatter found or parsed for {filepath}.")
    return index_entries

# --- Main Execution ---

def main():
    """
    Main function to drive the indexer.
    """
    parser = argparse.ArgumentParser(description="Generates a JSON index from Knowledge Base Markdown files.")
    parser.add_argument(
        "--dir",
        default=SRC_PATH,
        help=f"Directory to scan for Markdown files (default: {SRC_PATH})"
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT_FILE,
        help=f"Output file for the JSON index (default: {DEFAULT_OUTPUT_FILE})"
    )
    # Add more arguments (e.g., config file, base path for relative filepaths)
    args = parser.parse_args()

    log_message("INFO", "Starting Knowledge Base Indexer...")
    log_message("INFO", f"Source directory: {args.dir}")
    log_message("INFO", f"Output file: {args.output}")

    standards_data = generate_index_data(args.dir)

    if not standards_data:
        log_message("WARNING", "No standards data extracted. Index file will be empty or not updated.")
        # Optionally, still write an empty structure if required
        # standards_data = []

    output_structure = {
        "schemaVersion": SCHEMA_VERSION,
        "standards": standards_data
    }

    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output_structure, f, indent=2, ensure_ascii=False)
        log_message("INFO", f"Successfully wrote index to {args.output} with {len(standards_data)} entries.")
    except IOError as e:
        log_message("ERROR", f"Failed to write index to {args.output}: {e}")
    except Exception as e:
        log_message("ERROR", f"An unexpected error occurred while writing JSON output: {e}")


if __name__ == "__main__":
    main()
```
