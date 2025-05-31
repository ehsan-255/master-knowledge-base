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

# Fields required by standards_index.schema.json for each standard entry
# These must be present and non-null in the frontmatter for a standard to be indexed.
INDEX_REQUIRED_FIELDS = [
    "standard_id", "title", "primary_domain", "sub_domain", 
    "info-type", "version", "status", "filepath", "date-modified"
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
    
    direct_fields = ["standard_id", "title", "primary_domain", "sub_domain", 
                     "info-type", "version", "date-modified"]
    for field in direct_fields:
        metadata[field] = frontmatter_data.get(field)
        if isinstance(metadata[field], (int, float)) and field == "version":
            metadata[field] = str(metadata[field])

    tags = frontmatter_data.get("tags", [])
    metadata["status"] = get_status_from_tags(tags)

    # Check if all fields required by the index schema are present and not None
    missing_or_empty_fields = []
    for req_field in INDEX_REQUIRED_FIELDS:
        if metadata.get(req_field) is None: # Also catches if key was missing from frontmatter_data
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
    print("DEBUG: generate_index.py main() started.") # DEBUG
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

    args = parser.parse_args()

    repo_base_abs_path = os.path.abspath(args.repo_base)
    
    # Process multiple source directories
    source_directories_abs = [os.path.join(repo_base_abs_path, src_dir_rel) for src_dir_rel in args.src_dirs]
    
    output_dir_abs = os.path.join(repo_base_abs_path, args.output_dir)
    output_file_abs = os.path.join(output_dir_abs, args.output_filename)
    schema_file_abs = os.path.join(repo_base_abs_path, args.schema_file)

    # Check all source directories
    for s_dir_abs in source_directories_abs:
        if not os.path.isdir(s_dir_abs):
            print(f"Error: Standards source directory not found at {s_dir_abs}")
            print(f"DEBUG: Exiting because {s_dir_abs} is not a directory.") # DEBUG
            return
    
    print(f"DEBUG: Using source directories: {source_directories_abs}") # DEBUG
    print("DEBUG: Attempting to load JSON schema...") # DEBUG
    index_schema = load_json_schema(schema_file_abs)
    if not index_schema:
        print(f"Error: Failed to load index schema from {schema_file_abs}.")
        print("DEBUG: Exiting because index_schema could not be loaded.") # DEBUG
        return
    
    print("DEBUG: JSON schema loaded successfully.") # DEBUG

    index_data = {
        "schemaVersion": "1.0.0", 
        "generatedDate": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "standards": []
    }

    total_files_found = 0
    files_indexed_count = 0
    skipped_file_details = []

    for s_dir_abs in source_directories_abs:
        print(f"Scanning for Markdown files in: {s_dir_abs}...")
        for root, _, files in os.walk(s_dir_abs):
            for file in files:
                if file.endswith(".md"):
                    total_files_found += 1
                    filepath_abs = os.path.join(root, file)
                    filepath_for_index = os.path.relpath(filepath_abs, start=repo_base_abs_path)
                    
                    file_content = ""
                    try:
                        with open(filepath_abs, 'r', encoding='utf-8') as f_content:
                            file_content = f_content.read()
                    except Exception as e:
                        reason = f"Error reading file: {e}"
                        print(f"  SKIP: {filepath_for_index} ({reason})")
                        skipped_file_details.append((filepath_for_index, reason))
                        continue # Skip to next file
                    
                    parsed_meta, reason = extract_metadata(filepath_for_index, file_content)
                    if parsed_meta:
                        index_data["standards"].append(parsed_meta)
                        files_indexed_count += 1
                        # DEBUG: Print details of successfully indexed files
                        print(f"  DEBUG_INDEXED: ID: {parsed_meta.get('standard_id')}, File: {filepath_for_index}") 
                    else:
                        skipped_file_details.append((filepath_for_index, reason))

    print(f"\n--- Index Generation Summary ---")
    print(f"Total .md files found: {total_files_found}")
    print(f"Successfully indexed: {files_indexed_count}")
    skipped_count = len(skipped_file_details)
    print(f"Skipped (due to errors/missing fields): {skipped_count}")
    if skipped_file_details:
        print("Skipped file details:")
        for filepath, reason_text in skipped_file_details:
            print(f"  - {filepath}: {reason_text}")

    # DEBUG: Python-level regex check before jsonschema validation
    print("\nDEBUG: Performing Python-level regex check on standard_ids before jsonschema validation...")
    current_regex = r"^[A-Z]{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*$"
    for i, std_entry in enumerate(index_data["standards"]):
        std_id_to_check = std_entry.get("standard_id", "MISSING_ID_IN_ENTRY")
        if not re.match(current_regex, std_id_to_check):
            print(f"  DEBUG: Python re.match failed for standards[{i}]->standard_id: '{std_id_to_check}' with regex: {current_regex}")
        # else:
            # print(f"  DEBUG: Python re.match PASSED for standards[{i}]->standard_id: '{std_id_to_check}'") # Too verbose
    print("DEBUG: Python-level regex check complete.")

    # Validate generated index data against the schema
    validation_passed = False
    try:
        validate(instance=index_data, schema=index_schema)
        print(f"\nGenerated index successfully validated against schema.")
        validation_passed = True
    except jsonschema.ValidationError as ve: # More specific catch
        print(f"\nERROR: Generated index is NOT VALID against schema {args.schema_file} (resolved: {schema_file_abs}):")
        # Show simplified error path and message
        error_path = " -> ".join(str(p) for p in ve.path)
        print(f"  Error Path: {error_path}")
        print(f"  Error Message: {ve.message}")
        # To get more details if needed:
        # print(f"  Schema offending part: {ve.schema_path}")
        # print(f"  Instance offending part: {ve.instance}")
        print("Index will NOT be written due to schema validation errors.")
    except Exception as e: 
        print(f"\nERROR: An unexpected error occurred during JSON schema validation: {e}")
        print("Index will NOT be written due to validation error.")

    if validation_passed:
        os.makedirs(output_dir_abs, exist_ok=True)
        print(f"\nWriting index to: {output_file_abs}...")
        try:
            with open(output_file_abs, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, indent=2)
            print(f"Successfully generated {os.path.join(args.output_dir, args.output_filename)}")
        except IOError as e:
            print(f"Error writing index file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during file writing: {e}")
    else:
        print("No index file written due to schema validation failures.")


if __name__ == "__main__":
    main()
