# generate_index.py
# Core functionality for Standards Index Generator

import json
import os
import datetime
import yaml # Using PyYAML or ruamel.yaml

# Specifications:
# 1. Input: Path to the /standards/src/ directory.
# 2. Parsing: Read and parse YAML frontmatter from all .md files in the directory.
# 3. Data Extraction: Extract key metadata.
# 4. Output: Generate `standards_index.json` in a specified output directory.
# 5. Schema: The output MUST conform to `standards_index.schema.json`.

def get_frontmatter_from_content(file_content):
    """
    Extracts YAML frontmatter string from file content.
    Returns frontmatter_string or None if not found.
    """
    lines = file_content.splitlines(True)
    if not lines or not lines[0].startswith("---"):
        return None

    fm_end_index = -1
    for i, line in enumerate(lines[1:], start=1):
        if line.startswith("---"):
            fm_end_index = i
            break
    
    if fm_end_index == -1:
        return None
        
    return "".join(lines[1:fm_end_index])

def get_status_from_tags(tags_list):
    """
    Extracts status (e.g., 'draft') from a list of tags.
    Example: "status/draft" -> "draft"
    Returns the status string or None if no status tag is found.
    """
    if not isinstance(tags_list, list):
        return None
    for tag in tags_list:
        if isinstance(tag, str) and tag.startswith("status/"):
            return tag.split("/", 1)[1]
    return None

def extract_metadata(filepath, file_content):
    """
    Extracts specified metadata from the file's frontmatter.
    filepath should be relative to the repository root.
    """
    frontmatter_str = get_frontmatter_from_content(file_content)
    if not frontmatter_str:
        print(f"Warning: No frontmatter found in {filepath}. Skipping.")
        return None

    try:
        frontmatter_data = yaml.safe_load(frontmatter_str)
        if not isinstance(frontmatter_data, dict):
            print(f"Warning: Frontmatter in {filepath} is not a valid dictionary. Skipping.")
            return None
    except yaml.YAMLError as e:
        print(f"Warning: Invalid YAML syntax in frontmatter for {filepath}: {e}. Skipping.")
        return None

    # Required fields for the index. If any of these are missing, we skip the file.
    required_index_fields = ["standard_id", "title", "info-type", "version", "date-modified"]
    
    # Fields like primary_domain and sub_domain are required for standards, but might be
    # missing in other general documents if this indexer were to process them.
    # For now, we'll fetch them but not make them strictly required for a basic entry to exist.
    # The JSON schema can enforce if they must always be present.
    
    standard_id = frontmatter_data.get("standard_id")
    title = frontmatter_data.get("title")

    if not standard_id or not title:
        print(f"Warning: Missing 'standard_id' or 'title' in {filepath}. Skipping.")
        return None

    # Extract other fields, allowing for them to be potentially None if not present
    # The JSON schema will ultimately determine if None is allowed for these non-core fields.
    primary_domain = frontmatter_data.get("primary_domain")
    sub_domain = frontmatter_data.get("sub_domain")
    info_type = frontmatter_data.get("info-type")
    version = frontmatter_data.get("version")
    date_modified = frontmatter_data.get("date-modified")
    
    tags = frontmatter_data.get("tags", [])
    status = get_status_from_tags(tags)

    # Check if essential fields (for indexing logic) are present
    if not all([info_type, version, date_modified, status is not None]):
         print(f"Warning: Missing one or more of info-type, version, date-modified, or valid status tag in {filepath}. Skipping.")
         return None


    metadata = {
        "standard_id": standard_id,
        "title": title,
        "primary_domain": primary_domain, # Can be None if not present
        "sub_domain": sub_domain,       # Can be None if not present
        "info-type": info_type,
        "version": str(version), # Ensure version is string
        "status": status,
        "filepath": filepath.replace(os.sep, '/'), # Ensure POSIX paths relative to repo root
        "date-modified": date_modified
    }
    
    # Validate required fields are not None before returning for this iteration
    for req_field in required_index_fields:
        if metadata.get(req_field) is None:
            print(f"Warning: Required field '{req_field}' ended up as None for {filepath} after extraction. Skipping.")
            return None
            
    return metadata

def main():
    # Assuming script is run from the repository root.
    # For SWE-bench, current working directory is /app (which is the repo root).
    repo_base_dir = "." # Current directory is repo root

    standards_src_dir_rel = os.path.join("master-knowledge-base", "standards", "src")
    standards_src_dir_abs = os.path.abspath(standards_src_dir_rel)
    
    output_dir_rel = os.path.join("master-knowledge-base", "dist")
    output_dir_abs = os.path.abspath(output_dir_rel)
    
    output_file_rel = os.path.join(output_dir_rel, "standards_index.json")
    output_file_abs = os.path.abspath(output_file_rel)

    if not os.path.isdir(standards_src_dir_abs):
        print(f"Error: Standards source directory not found at {standards_src_dir_abs}")
        return
    
    index_data = {
        "schemaVersion": "1.0.0", 
        "generatedDate": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "standards": []
    }

    print(f"Scanning for Markdown files in: {standards_src_dir_abs}...")
    for root, _, files in os.walk(standards_src_dir_abs):
        for file in files:
            if file.endswith(".md"):
                filepath_abs = os.path.join(root, file)
                # Create filepath relative to repo_base_dir for the index
                # Assumes repo_base_dir is a parent of filepath_abs
                filepath_for_index = os.path.relpath(filepath_abs, start=os.path.abspath(repo_base_dir))
                
                try:
                    with open(filepath_abs, 'r', encoding='utf-8') as f_content:
                        file_content = f_content.read()
                    
                    parsed_meta = extract_metadata(filepath_for_index, file_content)
                    if parsed_meta:
                        index_data["standards"].append(parsed_meta)
                except Exception as e:
                    print(f"Error processing file {filepath_abs}: {e}")

    if not index_data["standards"]:
        print("Warning: No standards were successfully indexed.")
    else:
        print(f"Successfully extracted metadata for {len(index_data['standards'])} standard(s).")

    os.makedirs(output_dir_abs, exist_ok=True)
    print(f"Writing index to: {output_file_abs}...")
    try:
        with open(output_file_abs, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2)
        print(f"Successfully generated {output_file_rel}")
    except IOError as e:
        print(f"Error writing index file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during file writing: {e}")


if __name__ == "__main__":
    main()
