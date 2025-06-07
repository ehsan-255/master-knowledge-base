# Script: tools/file-format-utils/add_readme_frontmatter.py
import os
import re
from datetime import datetime, timezone
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

# Configuration
TARGET_README_PATHS = [
    "tools/README.md",
    "tools/linter/README.md",
    "tools/builder/README.md",
    "tools/indexer/README.md",
    "standards/README.md",
    "standards/templates/README.md"
]

DEFAULT_KB_ID_MAP = {
    "tools": "tools",
    "standards": "standards"
}
DEFAULT_PRIMARY_DOMAIN = "GM"
DEFAULT_SUB_DOMAIN = "GUIDE"
DEFAULT_INFO_TYPE = "guide-document"
DEFAULT_TAGS_COMMON = ["status/active", "content-type/documentation", "topic/readme"]
DEFAULT_VERSION = "1.0.0"
DEFAULT_CRITICALITY = "P4-Informational"
DEFAULT_LIFECYCLE_GATEKEEPER = "No-Gatekeeper"
DEFAULT_IMPACT_AREAS = ["documentation", "usability"]

README_FM_KEY_ORDER = [
    "title", "standard_id", "aliases", "tags", "kb-id", "info-type",
    "primary-topic", "related-standards", "version", "date-created",
    "date-modified", "primary_domain", "sub_domain", "scope_application",
    "criticality", "lifecycle_gatekeeper", "impact_areas", "change_log_url"
]

def get_first_h1_title(content_lines):
    for line in content_lines:
        line_stripped = line.strip()
        if line_stripped.startswith("# "):
            return line_stripped[2:].strip()
    return None

def generate_standard_id(filepath, directory_name):
    # import os # Already imported at top of script
    # import re # Already imported at top of script

    norm_filepath = os.path.normpath(filepath)
    path_components = [p.upper().replace('_', '-') for p in norm_filepath.split(os.sep)
                       if p and p.lower() not in ['master-knowledge-base', 'readme.md']]

    significant_parts = []
    # Iterate from the directory containing README.md upwards
    current_path = os.path.dirname(norm_filepath)
    while True:
        part_name = os.path.basename(current_path).upper().replace('_', '-')
        if not part_name or part_name == 'MASTER-KNOWLEDGE-BASE':
            break

        significant_parts.insert(0, part_name) # Prepend to keep order

        # Stop if we have enough parts or hit a common root like TOOLS or STANDARDS from a deeper level
        if len(significant_parts) >= 2 or part_name in ["TOOLS", "STANDARDS"]:
             # If the very first part added was TOOLS or STANDARDS, ensure we have it.
            if len(significant_parts) == 1 and part_name not in ["TOOLS", "STANDARDS"]:
                 # This case means we are in a sub-sub-dir like tools/linter/README.md
                 # We want "TOOLS-LINTER"
                 # If parent_dir of current_path is tools or standards, add it.
                 grandparent_name = os.path.basename(os.path.dirname(current_path)).upper().replace('_', '-')
                 if grandparent_name in ["TOOLS", "STANDARDS"]:
                     significant_parts.insert(0, grandparent_name)

            break

        parent_of_current = os.path.dirname(current_path)
        if parent_of_current == current_path: # Reached root
            break
        current_path = parent_of_current

    if not significant_parts: # Fallback
        # Use parent directory name if available and sensible
        parent_dir = os.path.basename(os.path.dirname(norm_filepath)).upper().replace('_','-')
        if parent_dir and parent_dir != "MASTER-KNOWLEDGE-BASE" and parent_dir != ".": # Handle cases like ./README.md
            significant_parts.append(parent_dir)
        else: # If truly at repo root or master-knowledge-base/README.md (though not targeted)
            significant_parts.append("GENERAL")

    # Limit to max 3 significant parts to keep ID length reasonable
    if len(significant_parts) > 3:
        significant_parts = significant_parts[-3:]


    id_core = "-".join(significant_parts)
    id_core = re.sub(r"^-+|-+$", "", id_core) # Remove leading/trailing hyphens
    id_core = re.sub(r"-+", "-", id_core)     # Collapse multiple hyphens

    # Use 'GM' as the domain code for General Management/Documentation
    # Ensure final ID is all uppercase and valid characters
    final_id = f"GM-{id_core}-README"
    final_id = re.sub(r"[^A-Z0-9-]", "", final_id.upper()) # Sanitize just in case
    final_id = re.sub(r"-+", "-", final_id) # Re-collapse hyphens after sanitizing
    return final_id


def create_frontmatter_for_readme(filepath, content_lines):
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    norm_filepath = os.path.normpath(filepath)
    parent_dir_name = os.path.basename(os.path.dirname(norm_filepath))

    title = get_first_h1_title(content_lines)
    if not title:
        title = f"README for {parent_dir_name if parent_dir_name else os.path.basename(os.path.dirname(os.path.abspath(filepath)))}"

    kb_id = "general"
    if "tools" in norm_filepath:
        kb_id = "tools"
    elif "standards" in norm_filepath:
        kb_id = "standards"

    standard_id = generate_standard_id(norm_filepath, parent_dir_name)

    fm_data = CommentedMap()
    fm_data["title"] = title
    fm_data["standard_id"] = standard_id
    fm_data["aliases"] = [f"{parent_dir_name.replace('-', ' ').replace('_', ' ').title()} README"] if parent_dir_name and parent_dir_name != "." else [f"{title} Alias"]

    tags = list(DEFAULT_TAGS_COMMON)
    tags.append(f"kb-id/{kb_id}")
    fm_data["tags"] = tags

    fm_data["kb-id"] = kb_id
    fm_data["info-type"] = DEFAULT_INFO_TYPE
    fm_data["primary-topic"] = f"Overview and guidance for the {parent_dir_name if parent_dir_name and parent_dir_name != '.' else os.path.basename(os.path.dirname(os.path.abspath(filepath)))} directory and its contents."
    fm_data["related-standards"] = []
    fm_data["version"] = DEFAULT_VERSION
    fm_data["date-created"] = now_iso
    fm_data["date-modified"] = now_iso
    fm_data["primary_domain"] = DEFAULT_PRIMARY_DOMAIN
    fm_data["sub_domain"] = DEFAULT_SUB_DOMAIN
    fm_data["scope_application"] = f"Provides an overview for the {norm_filepath}."
    fm_data["criticality"] = DEFAULT_CRITICALITY
    fm_data["lifecycle_gatekeeper"] = DEFAULT_LIFECYCLE_GATEKEEPER
    fm_data["impact_areas"] = list(DEFAULT_IMPACT_AREAS)
    fm_data["change_log_url"] = f"./{os.path.splitext(os.path.basename(filepath))[0].upper()}-CHANGELOG.MD"

    ordered_fm_data = CommentedMap()
    for key in README_FM_KEY_ORDER:
        if key in fm_data:
            ordered_fm_data[key] = fm_data[key]

    return ordered_fm_data

def main():
    yaml_processor = YAML()
    yaml_processor.indent(mapping=2, sequence=4, offset=2)
    yaml_processor.preserve_quotes = True

    # ruamel.yaml is imported at the top-level.
    # If the import fails, the script won't run at all.

    for readme_path_rel in TARGET_README_PATHS:
        abs_readme_path = os.path.abspath(readme_path_rel)
        if not os.path.exists(abs_readme_path):
            print(f"INFO: README file not found, skipping: {abs_readme_path}")
            continue

        print(f"Processing: {abs_readme_path}")

        original_content_lines = []
        try:
            with open(abs_readme_path, 'r', encoding='utf-8') as f:
                original_content_lines = f.readlines()
        except Exception as e:
            print(f"  ERROR: Could not read file {abs_readme_path}: {e}")
            continue

        if original_content_lines and original_content_lines[0].strip() == "---":
            fm_end_found = False
            for i, line in enumerate(original_content_lines[1:]):
                if line.strip() == "---":
                    fm_end_found = True
                    break
            if fm_end_found:
                print(f"  INFO: Frontmatter already exists in {abs_readme_path}. Skipping.")
                continue

        new_fm_data = create_frontmatter_for_readme(abs_readme_path, original_content_lines)

        import io
        string_stream = io.StringIO()
        yaml_processor.dump(new_fm_data, string_stream)
        frontmatter_block_str = string_stream.getvalue()
        string_stream.close()

        try:
            with open(abs_readme_path, 'w', encoding='utf-8') as f:
                f.write("---\n")
                f.write(frontmatter_block_str)
                # ruamel.yaml typically adds a newline at the end of its dump
                if not frontmatter_block_str.endswith('\n'):
                     f.write("\n") # Ensure newline before closing ---
                f.write("---\n")
                if original_content_lines: # Add a newline if there was original content
                    f.write("\n")
                f.writelines(original_content_lines)
            print(f"  SUCCESS: Added frontmatter to {abs_readme_path}")
        except Exception as e:
            print(f"  ERROR: Could not write updated file {abs_readme_path}: {e}")

if __name__ == "__main__":
    main()
