# generate_index.py
# Standards Index Generator with Schema Validation and Enhanced Reporting

import json
import os
import datetime
import yaml 
import jsonschema # For JSON schema validation
from jsonschema import validate
import argparse # Added for CLI arguments
import re # Added for regex checks
import logging # For better debug/info messages

# Fields required by standards_index.schema.json for each standard entry
# These must be present and non-null in the frontmatter for a standard to be indexed.
INDEX_REQUIRED_FIELDS = [
    "standard_id", "title", "primary_domain", "sub_domain", 
    "info-type", "version", "status", "filepath", "date-modified",
    "date-created", "criticality", "lifecycle_gatekeeper"
]

def get_frontmatter_from_content(file_content):
    """Extracts YAML frontmatter string from file content."""
    lines = file_content.splitlines(True)
    if not lines or not lines[0].startswith("---"):
        return None
    fm_end_index = -1
    for i, line in enumerate(lines[1:], start=1):
        if line.startswith("---"):
            fm_end_index = i
            break
    if fm_end_index == -1: return None
    return "".join(lines[1:fm_end_index])

def get_status_from_tags(tags_list):
    """Extracts status (e.g., 'draft') from a list of tags."""
    if not isinstance(tags_list, list): return None
    for tag in tags_list:
        if isinstance(tag, str) and tag.startswith("status/"):
            return tag.split("/", 1)[1]
    return None # If no status tag found

def extract_metadata(filepath_rel_to_repo, file_content):
    """
    Extracts metadata required for the index.
    Returns a dictionary or None if essential data for schema compliance is missing or invalid.
    """
    frontmatter_str = get_frontmatter_from_content(file_content)
    if not frontmatter_str:
        return None, "No frontmatter found"

    try:
        frontmatter_data = yaml.safe_load(frontmatter_str)
        if not isinstance(frontmatter_data, dict):
            return None, "Frontmatter is not a valid dictionary"
    except yaml.YAMLError as e:
        return None, f"Invalid YAML in frontmatter: {e.problem}"

    metadata = {"filepath": filepath_rel_to_repo.replace(os.sep, '/')}
    
    # Populate metadata from frontmatter based on INDEX_REQUIRED_FIELDS
    for field in INDEX_REQUIRED_FIELDS:
        if field == "filepath": # Already set
            continue
        elif field == "status":
            tags = frontmatter_data.get("tags", [])
            metadata[field] = get_status_from_tags(tags)
        else:
            metadata[field] = frontmatter_data.get(field)
            # Ensure version is a string if it's a number
            if field == "version" and isinstance(metadata[field], (int, float)):
                metadata[field] = str(metadata[field])

    # Check if all fields required by the index schema are present and not None after attempting to populate them
    missing_or_empty_fields = []
    for req_field in INDEX_REQUIRED_FIELDS:
        if metadata.get(req_field) is None:
            missing_or_empty_fields.append(req_field)
            
    if missing_or_empty_fields:
        return None, f"Missing/empty required field(s) for index: {', '.join(missing_or_empty_fields)}"
            
    return metadata, None # metadata, error_reason

def load_json_schema(schema_filepath_abs):
    try:
        with open(schema_filepath_abs, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"CRITICAL ERROR: JSON Schema file not found at {schema_filepath_abs}.")
    except json.JSONDecodeError:
        print(f"CRITICAL ERROR: Could not parse JSON Schema file at {schema_filepath_abs}.")
    return None

def main():
    parser = argparse.ArgumentParser(description="Knowledge Base Index Generator")
    parser.add_argument("--repo-base", default=".", 
                        help="Path to the repository root. Default is current directory.")
    parser.add_argument("--src-dirs", nargs='+', 
                        default=[os.path.join("master-knowledge-base", "standards", "src")], 
                        help="Source directories for standards files, relative to repo-base. Can specify multiple.")
    parser.add_argument("--output-dir", default=os.path.join("master-knowledge-base", "dist"), 
                        help="Output directory for the index file, relative to repo-base.")
    parser.add_argument("--schema-file", default=os.path.join("master-knowledge-base", "tools", "indexer", "standards_index.schema.json"), 
                        help="Path to the JSON schema for the index, relative to repo-base.")
    parser.add_argument("--output-filename", default="standards_index.json", 
                        help="Filename for the generated index.")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="Set the logging level (default: INFO).")

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=getattr(logging, args.log_level.upper()),
                        format='%(levelname)s: %(message)s')

    logging.debug("generate_index.py main() started.")
    repo_base_abs_path = os.path.abspath(args.repo_base)
    
    # Process multiple source directories
    source_directories_abs = [os.path.join(repo_base_abs_path, src_dir_rel) for src_dir_rel in args.src_dirs]
    
    output_dir_abs = os.path.join(repo_base_abs_path, args.output_dir)
    output_file_abs = os.path.join(output_dir_abs, args.output_filename)
    schema_file_abs = os.path.join(repo_base_abs_path, args.schema_file)

    # Check all source directories
    for s_dir_abs in source_directories_abs:
        if not os.path.isdir(s_dir_abs):
            logging.error(f"Standards source directory not found at {s_dir_abs}")
            logging.debug(f"Exiting because {s_dir_abs} is not a directory.")
            return # Consider sys.exit(1) for critical errors
    
    logging.debug(f"Using source directories: {source_directories_abs}")
    logging.debug("Attempting to load JSON schema...")
    index_schema = load_json_schema(schema_file_abs)
    if not index_schema:
        # load_json_schema already prints critical errors
        logging.debug("Exiting because index_schema could not be loaded.")
        return # Consider sys.exit(1)
    
    logging.debug("JSON schema loaded successfully.")

    index_data = {
        "schemaVersion": "1.0.0", 
        "generatedDate": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "standards": []
    }

    total_files_found = 0
    files_indexed_count = 0
    skipped_file_details = []
    processed_standard_ids = set()
    processed_filepaths = set()

    for s_dir_abs in source_directories_abs:
        logging.info(f"Scanning for Markdown files in: {s_dir_abs}...")
        for root, _, files in os.walk(s_dir_abs):
            for file in files:
                if file.endswith(".md"):
                    total_files_found += 1
                    filepath_abs = os.path.normpath(os.path.join(root, file)) # Normalize path

                    if filepath_abs in processed_filepaths:
                        logging.debug(f"Skipping already processed file: {filepath_abs}")
                        skipped_file_details.append((os.path.relpath(filepath_abs, start=repo_base_abs_path).replace(os.sep, '/'), "Skipped (already processed path)"))
                        continue
                    processed_filepaths.add(filepath_abs)

                    filepath_for_index = os.path.relpath(filepath_abs, start=repo_base_abs_path).replace(os.sep, '/')
                    
                    file_content = ""
                    try:
                        with open(filepath_abs, 'r', encoding='utf-8') as f_content:
                            file_content = f_content.read()
                    except Exception as e:
                        reason = f"Error reading file: {e}"
                        logging.warning(f"SKIP: {filepath_for_index} ({reason})")
                        skipped_file_details.append((filepath_for_index, reason))
                        continue
                    
                    parsed_meta, reason = extract_metadata(filepath_for_index, file_content)

                    if parsed_meta:
                        current_std_id = parsed_meta.get("standard_id")
                        if current_std_id in processed_standard_ids:
                            reason = f"Duplicate standard_id '{current_std_id}' found. Original in index, this one skipped."
                            logging.error(f"{reason} File: {filepath_for_index}") # Changed to logging.error
                            skipped_file_details.append((filepath_for_index, reason))
                        else:
                            processed_standard_ids.add(current_std_id)
                            index_data["standards"].append(parsed_meta)
                            files_indexed_count += 1
                            logging.debug(f"INDEXED: ID: {current_std_id}, File: {filepath_for_index}")
                    else:
                        skipped_file_details.append((filepath_for_index, reason))

    logging.info(f"\n--- Index Generation Summary ---")
    logging.info(f"Total .md files found: {total_files_found}")
    logging.info(f"Successfully indexed: {files_indexed_count}")
    skipped_count = len(skipped_file_details)
    logging.info(f"Skipped (due to errors/missing fields): {skipped_count}")
    if skipped_file_details:
        logging.info("Skipped file details:")
        for filepath, reason_text in skipped_file_details:
            logging.info(f"  - {filepath}: {reason_text}")

    logging.debug("\nPerforming Python-level regex check on standard_ids before jsonschema validation...")
    current_regex = r"^[A-Z]{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*$"
    for i, std_entry in enumerate(index_data["standards"]):
        std_id_to_check = std_entry.get("standard_id", "MISSING_ID_IN_ENTRY")
        if not re.match(current_regex, std_id_to_check):
            logging.debug(f"Python re.match failed for standards[{i}]->standard_id: '{std_id_to_check}' with regex: {current_regex}")
    logging.debug("Python-level regex check complete.")

    # Validate generated index data against the schema
    validation_passed = False
    try:
        validate(instance=index_data, schema=index_schema)
        logging.info(f"\nGenerated index successfully validated against schema.")
        validation_passed = True
    except jsonschema.ValidationError as ve:
        logging.error(f"\nGenerated index is NOT VALID against schema {args.schema_file} (resolved: {schema_file_abs}):")
        error_path = " -> ".join(str(p) for p in ve.path)
        logging.error(f"  Error Path: {error_path}")
        logging.error(f"  Error Message: {ve.message}")
        logging.error("Index will NOT be written due to schema validation errors.")
    except Exception as e: 
        logging.error(f"\nAn unexpected error occurred during JSON schema validation: {e}")
        logging.error("Index will NOT be written due to validation error.")

    if validation_passed:
        os.makedirs(output_dir_abs, exist_ok=True)
        logging.info(f"\nWriting index to: {output_file_abs}...")
        try:
            with open(output_file_abs, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, indent=2)
            logging.info(f"Successfully generated {os.path.join(args.output_dir, args.output_filename)}")
        except IOError as e:
            logging.error(f"Error writing index file: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred during file writing: {e}")
    else:
        logging.info("No index file written due to schema validation failures.")


if __name__ == "__main__":
    main()
