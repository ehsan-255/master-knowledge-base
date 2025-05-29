# generate_index.py
# Placeholder for Standards Index Generator

import json
import os # For future file walking
import datetime # For date handling

# Specifications:
# 1. Input: Path to the /standards/src/ directory.
# 2. Parsing: Read and parse YAML frontmatter from all .md files in the directory.
# 3. Data Extraction: Extract key metadata:
#    - standard_id
#    - title
#    - primary_domain
#    - sub_domain
#    - info-type
#    - version
#    - status (derived from tags, e.g., the part of status/* tag)
#    - filepath (relative to repo root)
#    - date-modified
# 4. Output: Generate `standards_index.json` in a specified output directory (e.g., /dist/ or /tools/indexer/).
#    - Include a root-level "schemaVersion": "1.0.0" (or similar semantic version for the index structure itself).
#    - Include a "generatedDate": current ISO-8601 datetime.
#    - The main content should be a list of objects, each representing a standard.
# 5. Schema: The output MUST conform to `standards_index.schema.json`.

def extract_metadata(filepath, base_dir):
    # TODO: Implement robust frontmatter parsing from filepath
    # This function should:
    # 1. Read the file content.
    # 2. Parse the YAML frontmatter.
    # 3. Extract the required fields.
    # 4. Derive 'status' from the 'tags' list (e.g., find 'status/draft' -> 'draft').
    # 5. Construct the relative filepath from the base_dir.
    
    # Example data structure (replace with actual extracted data)
    # metadata = {
    #     "standard_id": "XX-YYYY-ZZZZ", "title": "Example Standard",
    #     "primary_domain": "XX", "sub_domain": "YYYY",
    #     "info-type": "standard-definition", "version": "1.0.0",
    #     "status": "draft", 
    #     "filepath": os.path.relpath(filepath, start=base_dir).replace(os.sep, '/'), # Ensure POSIX paths
    #     "date-modified": "YYYY-MM-DDTHH:MM:SSZ"
    # }
    # return metadata
    return None # Placeholder

def main():
    # Determine paths relative to the script's location or a known base
    # For this example, assuming script is run from repo root or paths are adjusted.
    repo_base_dir = "master-knowledge-base" # This might need to be determined more robustly
    standards_src_dir = os.path.join(repo_base_dir, "standards", "src")
    # Outputting to the same directory as the script for simplicity in this skeleton
    script_dir = os.path.dirname(__file__) 
    output_file = os.path.join(script_dir, "standards_index.json")
    
    index_data = {
        "schemaVersion": "1.0.0", # Version of this index's schema
        "generatedDate": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "standards": []
    }

    # TODO: Replace simulation with actual file walking and processing
    # current_script_path = os.path.dirname(os.path.abspath(__file__))
    # repo_root = os.path.abspath(os.path.join(current_script_path, "..", "..")) # Example: if tools/indexer is two levels down
    # standards_src_abs_dir = os.path.join(repo_root, standards_src_dir)
    # if not os.path.isdir(standards_src_abs_dir):
    #    print(f"Error: Standards source directory not found at {standards_src_abs_dir}")
    #    return

    # for root, dirs, files in os.walk(standards_src_abs_dir):
    #     for file in files:
    #         if file.endswith(".md"):
    #             filepath_abs = os.path.join(root, file)
    #             # Pass repo_root to allow creation of relative paths from that point
    #             parsed_meta = extract_metadata(filepath_abs, repo_root) 
    #             if parsed_meta:
    #                 index_data["standards"].append(parsed_meta)
    
    # Simulate adding one item for now
    print(f"Simulating metadata extraction for index generation...")
    example_meta = {
        "standard_id": "MT-SCHEMA-FRONTMATTER", "title": "Standard: Frontmatter Schema Definition",
        "primary_domain": "MT", "sub_domain": "FRONTMATTER",
        "info-type": "standard-definition", "version": "0.1.0",
        "status": "draft", # Assuming this was parsed from "status/draft" tag
        "filepath": "master-knowledge-base/standards/src/MT-SCHEMA-FRONTMATTER.md", # Relative to repo root
        "date-modified": "2025-05-29T15:53:52Z" # Example, use actual from file
    }
    index_data["standards"].append(example_meta)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(index_data, f, indent=2)
    
    print(f"Generated {output_file}")

if __name__ == "__main__":
    main()
