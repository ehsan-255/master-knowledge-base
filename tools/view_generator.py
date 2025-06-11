#!/usr/bin/env python3
"""
Knowledge Base View Generator
Generates human-readable (.md) or AI-consumable (.yaml) views
of standards or schema components from the JSON-LD SSTs.
"""

import json
import yaml
import argparse
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# --- Configuration ---
# Relative paths from the script's location or a defined repo root
# Assuming script is in tools/
REPO_BASE_PATH = Path(__file__).resolve().parent.parent
SCHEMA_REGISTRY_PATH = REPO_BASE_PATH / "standards" / "registry" / "schema-registry.jsonld"
MASTER_INDEX_PATH = REPO_BASE_PATH / "standards" / "registry" / "master-index.jsonld"
CONTEXT_BASE_PATH = REPO_BASE_PATH / "standards" / "registry" / "contexts"

# --- Data Loading Functions ---
def load_json_file(file_path: Path) -> dict:
    """Loads a JSON file."""
    if not file_path.exists():
        logging.error(f"File not found: {file_path}")
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from {file_path}: {e}")
        return None
    except IOError as e:
        logging.error(f"IOError reading {file_path}: {e}")
        return None

# --- View Generation Functions ---
def generate_markdown_view_standard(standard_data: dict, schema_registry: dict) -> str:
    """Generates a Markdown view for a standard document."""
    if not standard_data:
        return "Error: Standard data is empty."

    md_lines = []
    title = standard_data.get("kb:title", "Unknown Standard")
    standard_id = standard_data.get("kb:standard_id", standard_data.get("@id", "Unknown ID"))

    md_lines.append(f"# View: {title} ({standard_id})")
    md_lines.append(f"Generated: {datetime.now().isoformat()}")
    md_lines.append("\n---")

    md_lines.append("## Fields")
    md_lines.append("| Field Name | Value | Description (from Schema) |")
    md_lines.append("|------------|-------|---------------------------|")

    field_definitions = {
        f"kb:{defn.get('kb:fieldName', '').replace('-', '_')}": defn
        for defn in schema_registry.get("kb:fieldDefinitions", [])
    }
    # Correctly map schema fieldName (e.g., "info-type") to actual kb:prefixed key (e.g., "kb:info_type")
    schema_field_map = {
        defn.get('kb:fieldName'): defn
        for defn in schema_registry.get("kb:fieldDefinitions", [])
    }


    for key, value in standard_data.items():
        if key in ["@id", "@type"]: # Skip JSON-LD structural keys for main table
            continue

        # Attempt to find field description from schema_registry
        field_desc = "N/A"
        # Derive simple_key for schema lookup (e.g. "title" from "kb:title")
        simple_key = key.split("kb:")[-1].replace("_", "-") if key.startswith("kb:") else key

        field_def = schema_field_map.get(simple_key)
        if field_def:
            field_desc = field_def.get("kb:description", "No description in schema.")

        val_str = str(value)
        if isinstance(value, list):
            val_str = "\n".join([f"- {v}" for v in value])
        elif isinstance(value, dict):
            val_str = yaml.dump(value, indent=2, sort_keys=False) # Pretty print dicts

        md_lines.append(f"| `{key}` | {val_str} | {field_desc} |")

    md_lines.append("\n## Raw JSON-LD Data")
    md_lines.append("```json")
    md_lines.append(json.dumps(standard_data, indent=2, ensure_ascii=False))
    md_lines.append("```")

    return "\n".join(md_lines)

def generate_yaml_view_standard(standard_data: dict) -> str:
    """
    Generates a YAML view for a standard document.
    This YAML represents the current state and can be used as a basis for a change request.
    """
    if not standard_data:
        return "# Error: Standard data is empty."

    # For a change request manifest, we might want to add some metadata
    # For now, just dump the standard_data, but ensure it's clean.
    # A real change request might look like:
    # target_id: "kb:doc-some-id"
    # operation: "update" # or "create_if_not_exists"
    # payload:
    #   <standard_data fields>

    # For a "view", we just output the data itself.
    try:
        return yaml.dump(standard_data, sort_keys=False, indent=2, allow_unicode=True)
    except yaml.YAMLError as e:
        logging.error(f"Error encoding YAML: {e}")
        return f"# Error encoding YAML: {e}"

# --- Main Logic ---
def main():
    parser = argparse.ArgumentParser(description="Knowledge Base View Generator.")
    parser.add_argument("--id", required=True, help="The ID of the standard or schema entity to generate a view for (e.g., a standard_id like 'XX-YYYY-ZZZZ').")
    parser.add_argument("--type", choices=['md', 'yaml'], required=True, help="Output type: 'md' for Markdown, 'yaml' for YAML.")
    parser.add_argument("--output", help="Output file path. If not provided, prints to stdout.")
    # Future: parser.add_argument("--entity-type", choices=['standard', 'schema-field', 'schema-vocab'], default='standard', help="Type of entity to view.")

    args = parser.parse_args()

    # Load main data sources
    logging.info(f"Loading schema registry from: {SCHEMA_REGISTRY_PATH}")
    schema_registry = load_json_file(SCHEMA_REGISTRY_PATH)
    if not schema_registry:
        logging.error("Failed to load schema registry. Exiting.")
        return 1

    logging.info(f"Loading master index from: {MASTER_INDEX_PATH}")
    master_index = load_json_file(MASTER_INDEX_PATH)
    if not master_index:
        logging.error("Failed to load master index. Exiting.")
        return 1

    # Find the standard document by standard_id (primary use case for now)
    target_standard_data = None
    if master_index.get("kb:documents"):
        for doc in master_index["kb:documents"]:
            # Check both kb:standard_id and @id (if id is a direct standard_id)
            if doc.get("kb:standard_id") == args.id or doc.get("@id") == args.id:
                target_standard_data = doc
                break
            # Allow lookup by the generated @id as well
            generated_id_suffix = args.id.replace('/', '-').replace('.md', '')
            if doc.get("@id") == f"kb:doc-{generated_id_suffix}":
                 target_standard_data = doc
                 break


    if not target_standard_data:
        logging.error(f"Standard with ID '{args.id}' not found in master index.")
        return 1

    logging.info(f"Found standard: {target_standard_data.get('kb:title', args.id)}")

    output_content = ""
    if args.type == 'md':
        logging.info("Generating Markdown view...")
        output_content = generate_markdown_view_standard(target_standard_data, schema_registry)
    elif args.type == 'yaml':
        logging.info("Generating YAML view...")
        output_content = generate_yaml_view_standard(target_standard_data)

    if args.output:
        try:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output_content)
            logging.info(f"View successfully written to: {output_path}")
        except IOError as e:
            logging.error(f"Error writing to output file {args.output}: {e}")
            print("\n--- Output ---") # Print to stdout if file write fails
            print(output_content)
            return 1
    else:
        print(output_content)

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
