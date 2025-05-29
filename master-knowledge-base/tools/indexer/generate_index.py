# generate_index.py
# Standards Index Generator with Schema Validation and Enhanced Reporting

import json
import os
import datetime
import yaml 
import jsonschema # For JSON schema validation
from jsonschema import validate

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
    repo_base_dir = "." 
    standards_src_dir_rel = os.path.join("master-knowledge-base", "standards", "src")
    standards_src_dir_abs = os.path.abspath(os.path.join(repo_base_dir, standards_src_dir_rel))
    
    output_dir_rel = os.path.join("master-knowledge-base", "dist")
    output_dir_abs = os.path.abspath(os.path.join(repo_base_dir, output_dir_rel))
    
    output_file_rel = os.path.join(output_dir_rel, "standards_index.json")
    output_file_abs = os.path.abspath(output_file_rel)

    schema_file_rel = os.path.join("master-knowledge-base", "tools", "indexer", "standards_index.schema.json")
    schema_file_abs = os.path.abspath(os.path.join(repo_base_dir, schema_file_rel))

    if not os.path.isdir(standards_src_dir_abs):
        print(f"Error: Standards source directory not found at {standards_src_dir_abs}")
        return
    
    index_schema = load_json_schema(schema_file_abs)
    if not index_schema:
        print("Exiting due to failure to load index schema.")
        return

    index_data = {
        "schemaVersion": "1.0.0", 
        "generatedDate": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "standards": []
    }

    print(f"Scanning for Markdown files in: {standards_src_dir_abs}...")
    total_files_found = 0
    files_indexed_count = 0
    skipped_file_details = []

    for root, _, files in os.walk(standards_src_dir_abs):
        for file in files:
            if file.endswith(".md"):
                total_files_found += 1
                filepath_abs = os.path.join(root, file)
                filepath_for_index = os.path.relpath(filepath_abs, start=os.path.abspath(repo_base_dir))
                
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

    # Validate generated index data against the schema
    validation_passed = False
    try:
        validate(instance=index_data, schema=index_schema)
        print("\nGenerated index successfully validated against schema.")
        validation_passed = True
    except jsonschema.ValidationError as ve: # More specific catch
        print(f"\nERROR: Generated index is NOT VALID against schema {schema_file_rel}:")
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
            print(f"Successfully generated {output_file_rel}")
        except IOError as e:
            print(f"Error writing index file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during file writing: {e}")
    else:
        print("No index file written due to schema validation failures.")


if __name__ == "__main__":
    main()
