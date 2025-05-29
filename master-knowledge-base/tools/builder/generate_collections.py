# generate_collections.py
# Derived Collection View Generator with Advanced Link Resolution

import json
import os
import datetime
import yaml # Using PyYAML
import re

def load_standards_index(index_path):
    """Loads the standards index and returns a dictionary keyed by standard_id."""
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if "standards" not in data:
                print(f"Error: 'standards' key not found in index: {index_path}")
                return None
            # Create a dictionary for faster lookups by standard_id
            return {std["standard_id"]: std for std in data.get("standards", []) if "standard_id" in std}
    except FileNotFoundError:
        print(f"Error: Standards index not found at {index_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not parse standards index at {index_path}")
        return None

def load_collection_definitions(config_path):
    """Loads collection definitions from a YAML file."""
    print(f"Loading collection definitions from {config_path}...")
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if "collections" not in data:
                print(f"Error: 'collections' key not found in {config_path}")
                return []
            return data["collections"]
    except FileNotFoundError:
        print(f"Error: Collection definitions file not found at {config_path}")
        return []
    except yaml.YAMLError as e: # Catching specific PyYAML error
        print(f"Error: Could not parse collection definitions YAML at {config_path}: {e}")
        return []

def generate_anchor_for_standard(standard_id):
    """Generates a unique and Markdown-compatible anchor from a standard_id."""
    return standard_id.lower() # Standard IDs are already quite URL-friendly

def get_body_content_from_markdown(file_content):
    """Extracts Markdown content after the YAML frontmatter block."""
    lines = file_content.splitlines(True)
    if not lines or not lines[0].startswith("---"):
        return file_content 
    fm_end_index = -1
    for i, line in enumerate(lines[1:], start=1):
        if line.startswith("---"):
            fm_end_index = i
            break
    if fm_end_index == -1:
        return file_content 
    return "".join(lines[fm_end_index+1:])

def filter_standards(all_standards_map, criteria_list):
    """Filters the standards map based on criteria, returns a list of matching metadata."""
    if not criteria_list: # If no criteria, include all standards
        return list(all_standards_map.values())

    filtered_list = []
    for std_id, standard_meta in all_standards_map.items():
        match_all_criteria = True
        for criterion in criteria_list:
            field, operator, value = criterion.get("field"), criterion.get("operator"), criterion.get("value")
            
            standard_value = standard_meta.get(field)
            if standard_value is None and field not in standard_meta: # Field truly missing
                match_all_criteria = False; break
            
            if operator == "equals":
                if standard_value != value: match_all_criteria = False; break
            elif operator == "in":
                if not isinstance(value, list) or standard_value not in value: match_all_criteria = False; break
            elif operator == "not_equals":
                if standard_value == value: match_all_criteria = False; break
            elif operator == "not_in":
                if isinstance(value, list) and standard_value in value: match_all_criteria = False; break
            else:
                print(f"Warning: Unknown operator '{operator}' for field '{field}'. Criterion skipped.")
        
        if match_all_criteria:
            filtered_list.append(standard_meta)
    return filtered_list

def resolve_internal_links(body_content, current_collection_standard_ids, all_standards_map):
    """Resolves [[STANDARD_ID]] and [[STANDARD_ID#anchor]] links within the body content."""
    # Regex to find [[STANDARD_ID(#anchor)?(|alias)?]]
    link_pattern = r"\[\[([A-Z]{2}-[A-Z]{2,6}-[A-Z0-9\-]+)(\#[A-Za-z0-9\-]+)?((\|)([^\]]+))?\]\]"

    def replace_link(match):
        target_id = match.group(1)
        target_sub_anchor = match.group(2) or ""  # e.g., #my-heading
        has_alias = match.group(4) # True if '|' is present
        alias_text = match.group(5) if has_alias else None

        # Determine display text: if alias exists use it, else use title from index, else target_id
        display_text = alias_text
        if not display_text:
            target_meta = all_standards_map.get(target_id)
            if target_meta and target_meta.get("title"):
                display_text = target_meta.get("title")
            else: # Fallback if target_id not in index or has no title
                display_text = target_id 

        if target_id in current_collection_standard_ids:
            # Target is in the same collection. Link to its H2 anchor.
            # Original sub-anchor (#heading) is usually dropped, linking to start of that standard's section.
            collection_anchor = generate_anchor_for_standard(target_id)
            print(f"  Resolving intra-collection link: [[{target_id}{target_sub_anchor}]] -> [#{collection_anchor}] ({display_text})")
            return f"[{display_text}](#{collection_anchor})"
        else:
            # Target is external. Leave as [[STANDARD_ID#anchor|alias]] or [[STANDARD_ID|alias]] or [[STANDARD_ID#anchor]] or [[STANDARD_ID]]
            original_link_content = f"{target_id}{target_sub_anchor}"
            if alias_text:
                original_link_content += f"|{alias_text}"
            print(f"  Keeping external link: [[{original_link_content}]]")
            return f"[[{original_link_content}]]"
                 
    return re.sub(link_pattern, replace_link, body_content)

def generate_single_collection(collection_def, all_standards_map, output_dir, repo_base_dir):
    collection_id = collection_def.get('id', 'unknown-collection')
    collection_title = collection_def.get('title', 'Untitled Collection')
    collection_filename = collection_def.get('output_filename', f"{collection_id}.md")
    collection_description = collection_def.get('description', '')
    
    print(f"\nProcessing collection: {collection_title} (ID: {collection_id})")

    criteria = collection_def.get("criteria", [])
    included_standards_metadata_list = filter_standards(all_standards_map, criteria)

    if not included_standards_metadata_list:
        print(f"  No standards matched criteria for collection: {collection_title}")
        return

    print(f"  Found {len(included_standards_metadata_list)} standards for collection '{collection_title}'.")
    
    current_collection_standard_ids = {std_meta['standard_id'] for std_meta in included_standards_metadata_list}

    collection_frontmatter_str = f"""---
title: "{collection_title}"
description: "{collection_description}"
date_generated: "{datetime.datetime.now(datetime.timezone.utc).isoformat()}"
source_collection_definition_id: "{collection_id}"
number_of_standards: {len(included_standards_metadata_list)}
tags: ["kb-collection", "derived-view"]
info-type: "collection-document" 
---

"""
    
    toc_parts = ["## Table of Contents\n"]
    aggregated_content_parts = []

    # Sort standards by standard_id for consistent ToC and content order
    included_standards_metadata_list.sort(key=lambda x: x.get('standard_id', ''))

    for standard_meta in included_standards_metadata_list:
        standard_title = standard_meta.get('title', 'Untitled Standard')
        standard_id = standard_meta.get('standard_id')
        
        anchor = generate_anchor_for_standard(standard_id) # Use standard_id for anchor
        toc_parts.append(f"- [{standard_title} (`{standard_id}`)](#{anchor})\n")
        
        aggregated_content_parts.append(f"\n## <a id=\"{anchor}\"></a>{standard_title} (`{standard_id}`)\n\n")
        
        standard_filepath_abs = os.path.join(repo_base_dir, standard_meta.get('filepath'))
        
        try:
            with open(standard_filepath_abs, 'r', encoding='utf-8') as f_std:
                file_content = f_std.read()
                body_content = get_body_content_from_markdown(file_content)
                resolved_body_content = resolve_internal_links(body_content, current_collection_standard_ids, all_standards_map)
                aggregated_content_parts.append(resolved_body_content.strip() + "\n\n---\n")
        except FileNotFoundError:
            print(f"  Warning: File not found for '{standard_title}' at {standard_filepath_abs}. Content missing.")
            aggregated_content_parts.append(f"*Error: Content for '{standard_title}' (`{standard_id}`) could not be loaded. File not found.* \n\n---\n")
        except Exception as e:
            print(f"  Warning: Error reading/processing file {standard_filepath_abs} for '{standard_title}': {e}")
            aggregated_content_parts.append(f"*Error: Content for '{standard_title}' (`{standard_id}`) could not be loaded: {e}* \n\n---\n")

    final_markdown = collection_frontmatter_str + "".join(toc_parts) + "\n" + "".join(aggregated_content_parts)
    if final_markdown.endswith("\n\n---\n"): # Clean up last separator
        final_markdown = final_markdown[:-5]

    output_filepath = os.path.join(output_dir, collection_filename)
    try:
        with open(output_filepath, 'w', encoding='utf-8') as f_coll:
            f_coll.write(final_markdown)
        print(f"  Successfully wrote collection: {output_filepath}")
    except IOError as e:
        print(f"  Error writing collection file {output_filepath}: {e}")

def main():
    repo_base_dir = "." 

    index_file_path_rel = os.path.join("master-knowledge-base", "dist", "standards_index.json")
    index_file_path_abs = os.path.abspath(index_file_path_rel)

    collection_config_path_rel = os.path.join("master-knowledge-base", "tools", "builder", "collection_definitions.yaml")
    collection_config_path_abs = os.path.abspath(collection_config_path_rel)
    
    output_base_dir_rel = os.path.join("master-knowledge-base", "dist", "collections")
    output_base_dir_abs = os.path.abspath(output_base_dir_rel)

    if not os.path.exists(output_base_dir_abs):
        os.makedirs(output_base_dir_abs)
        print(f"Created output directory: {output_base_dir_abs}")

    all_standards_map = load_standards_index(index_file_path_abs)
    if not all_standards_map:
        print("Could not load standards map from index or index is empty/invalid. Exiting.")
        return

    collection_defs = load_collection_definitions(collection_config_path_abs)
    if not collection_defs:
        print(f"No collection definitions found or loaded from {collection_config_path_abs}. Please check the file.")
        return

    print(f"Loaded {len(all_standards_map)} standards from index.")
    print(f"Loaded {len(collection_defs)} collection definitions.")

    for collection_def in collection_defs:
        generate_single_collection(collection_def, all_standards_map, output_base_dir_abs, os.path.abspath(repo_base_dir))
    
    print("\nCollection generation process completed.")

if __name__ == "__main__":
    main()
