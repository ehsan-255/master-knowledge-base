# generate_collections.py
# Derived Collection View Generator with GFM Anchors and Enhanced Robustness

import json
import os
import datetime
import yaml # Using PyYAML
import re
from collections import defaultdict
import argparse
import logging

# Basic Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def load_standards_index(index_path):
    """Loads the standards index and returns a dictionary keyed by standard_id."""
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if "standards" not in data:
                logging.error(f"'standards' key not found in index: {index_path}")
                return None
            return {std["standard_id"]: std for std in data.get("standards", []) if "standard_id" in std}
    except FileNotFoundError:
        logging.error(f"Standards index not found at {index_path}")
        return None
    except json.JSONDecodeError:
        logging.error(f"Could not parse standards index at {index_path}")
        return None

def load_collection_definitions(config_path):
    """Loads collection definitions from a YAML file."""
    logging.info(f"Loading collection definitions from {config_path}...")
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if "collections" not in data:
                logging.error(f"'collections' key not found in {config_path}")
                return []
            return data["collections"]
    except FileNotFoundError:
        logging.error(f"Collection definitions file not found at {config_path}")
        return []
    except yaml.YAMLError as e:
        logging.error(f"Could not parse collection definitions YAML at {config_path}: {e}")
        return []

def generate_gfm_anchor(text_heading, used_anchors_in_collection):
    """
    Generates a GitHub Flavored Markdown (GFM)-compatible anchor.
    Handles duplicates by appending -1, -2, etc.
    """
    if not text_heading: return "untitled-section"
    anchor = text_heading.lower()
    anchor = re.sub(r'[^\w\s\-_]', '', anchor) # Remove punctuation not allowed
    anchor = re.sub(r'\s+', '-', anchor)       # Replace spaces with hyphens
    anchor = re.sub(r'-+', '-', anchor)        # Collapse multiple hyphens
    anchor = anchor.strip('-')

    if not anchor: # Handle cases where title was all special chars
        anchor = "section"

    original_anchor = anchor
    counter = 1
    while anchor in used_anchors_in_collection:
        anchor = f"{original_anchor}-{counter}"
        counter += 1
    used_anchors_in_collection.add(anchor)
    return anchor

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
    """
    Filters the standards map based on criteria, returns a list of matching metadata.
    Assumes AND logic for all criteria in the list.
    TODO: Implement more complex criteria_logic (AND/OR groups) from collection_definitions.yaml.
    """
    if not criteria_list:
        return list(all_standards_map.values()) 

    filtered_list = []
    for std_id, standard_meta in all_standards_map.items():
        match_all_criteria = True
        for criterion in criteria_list:
            field, operator, value = criterion.get("field"), criterion.get("operator"), criterion.get("value")
            
            standard_value = standard_meta.get(field)
            if standard_value is None and field not in standard_meta: 
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
                logging.warning(f"  Unknown operator '{operator}' for field '{field}' in collection definition. Criterion skipped.")
        
        if match_all_criteria:
            filtered_list.append(standard_meta)
    return filtered_list

def resolve_internal_links(body_content, current_collection_standard_ids_map, all_standards_map, used_anchors_in_collection):
    """Resolves [[STANDARD_ID]] and [[STANDARD_ID#anchor]] links within the body content."""
    # Regex to find [[STANDARD_ID(#target-sub-anchor)?(|alias)?]]
    link_pattern = r"\[\[([A-Z]{2}-[A-Z]{2,6}-[A-Z0-9\-]+)((?:#[A-Za-z0-9\-]+)*)(?:\|([^\]]+))?\]\]"
    # Group 1: STANDARD_ID
    # Group 2: #target-sub-anchor (optional, can be multiple like #anchor1#anchor2 - though unusual)
    # Group 3: |alias (optional, only last part)
    # Group 4: alias text (if group 3 exists)


    def replace_link(match):
        target_id = match.group(1)
        target_sub_anchor_part = match.group(2) or ""  # e.g., #my-heading or #anchor1#anchor2
        # Group 3 is the alias text. It will be None if the alias part of the regex didn't match.
        alias_text = match.group(3)
        
        display_text = alias_text
        if not display_text: # No alias, try to use target title
            target_meta_for_title = all_standards_map.get(target_id)
            if target_meta_for_title and target_meta_for_title.get("title"):
                display_text = target_meta_for_title.get("title")
            else: # Fallback if target_id not in index or has no title
                display_text = target_id 
        
        if target_id in current_collection_standard_ids_map:
            # Target is in the same collection. Link to its H2 anchor.
            # The GFM anchor for the H2 is based on its full heading text.
            target_standard_in_collection_meta = current_collection_standard_ids_map[target_id]
            heading_text_for_anchor = f"{target_standard_in_collection_meta.get('title')} ({target_id})"
            # We need to ensure this anchor matches exactly how it's generated for the H2
            # This requires access to the *used_anchors_in_collection* set specific to *this collection's generation pass*
            # to correctly predict the GFM anchor if there were duplicates.
            # For simplicity now, we'll assume titles+IDs are unique enough that -1, -2 aren't common for *target* links.
            # A more robust solution would pre-calculate all anchors for the current collection.
            # For now, generate it simply, assuming it's the first instance.
            temp_used_anchors_for_check = set() # Simulate for single link resolution
            collection_anchor = generate_gfm_anchor(heading_text_for_anchor, temp_used_anchors_for_check)

            logging.debug(f"    Resolving intra-collection link: [[{match.group(0)}]] -> [{display_text}](#{collection_anchor})")
            return f"[{display_text}](#{collection_anchor})"
        else:
            # Target is external. Leave as [[STANDARD_ID#anchor|alias]] or similar.
            original_link_text = f"{target_id}{target_sub_anchor_part}"
            if alias_text:
                original_link_text += f"|{alias_text}"
            # logging.debug(f"    Keeping external link: [[{original_link_text}]]") # Less verbose
            return f"[[{original_link_text}]]"
                 
    return re.sub(link_pattern, replace_link, body_content)


def generate_single_collection(collection_def, all_standards_map, output_dir, repo_base_dir):
    collection_id = collection_def.get('id', 'unknown-collection')
    collection_title = collection_def.get('title', 'Untitled Collection')
    collection_filename = collection_def.get('output_filename', f"{collection_id}.md")
    collection_description = collection_def.get('description', '')
    
    logging.info(f"Processing collection: {collection_title} (ID: {collection_id})")

    criteria = collection_def.get("criteria", [])
    included_standards_metadata_list = filter_standards(all_standards_map, criteria)

    if not included_standards_metadata_list:
        logging.info(f"  No standards matched criteria for: {collection_title}")
        return

    logging.info(f"  Found {len(included_standards_metadata_list)} standards for collection '{collection_title}'.")
    
    current_collection_standard_ids_map = {std_meta['standard_id']: std_meta for std_meta in included_standards_metadata_list}
    
    # Sort standards by standard_id for consistent ToC and content order
    included_standards_metadata_list.sort(key=lambda x: x.get('standard_id', ''))

    collection_frontmatter_str = f"""---
title: "{collection_title}"
description: "{collection_description}"
date_generated: "{datetime.datetime.now(datetime.timezone.utc).isoformat()}"
source_collection_definition_id: "{collection_id}"
number_of_standards: {len(included_standards_metadata_list)}
tags: ["content-type/collection-document", "status/published", "topic/derived-view"] 
info-type: "collection-document" 
# Consider adding a standard_id for the collection itself, e.g.:
# standard_id: "COLL-{collection_id.upper().replace('_','-')}" 
---

"""
    
    toc_parts = ["## Table of Contents\n"]
    aggregated_content_parts = []
    
    # Set to track anchors used within this specific collection to handle duplicates for H2s
    used_anchors_this_collection = set() 

    for standard_meta in included_standards_metadata_list:
        standard_title = standard_meta.get('title', 'Untitled Standard')
        standard_id = standard_meta.get('standard_id')
        
        h2_heading_text = f"{standard_title} ({standard_id})"
        anchor = generate_gfm_anchor(h2_heading_text, used_anchors_this_collection)
        
        toc_parts.append(f"- [{standard_title} (`{standard_id}`)](#{anchor})\n")
        aggregated_content_parts.append(f"\n## {h2_heading_text}\n\n") # GFM creates anchor from this
        
        standard_filepath_abs = os.path.join(repo_base_dir, standard_meta.get('filepath'))
        
        try:
            logging.debug(f"    Aggregating: {standard_id} - {standard_title}")
            with open(standard_filepath_abs, 'r', encoding='utf-8') as f_std:
                file_content = f_std.read()
                body_content = get_body_content_from_markdown(file_content)
                resolved_body_content = resolve_internal_links(body_content, current_collection_standard_ids_map, all_standards_map, used_anchors_this_collection)
                aggregated_content_parts.append(resolved_body_content.strip() + "\n\n---\n")
        except FileNotFoundError:
            logging.error(f"  File not found for '{standard_title}' at {standard_filepath_abs}. Content will be missing.")
            aggregated_content_parts.append(f"*Error: Content for '{standard_title}' (`{standard_id}`) could not be loaded. File not found.* \n\n---\n")
        except Exception as e:
            logging.error(f"  Error reading/processing file {standard_filepath_abs} for '{standard_title}': {e}")
            aggregated_content_parts.append(f"*Error: Content for '{standard_title}' (`{standard_id}`) could not be loaded: {e}* \n\n---\n")

    final_markdown = collection_frontmatter_str + "".join(toc_parts) + "\n" + "".join(aggregated_content_parts)
    if final_markdown.endswith("\n\n---\n"): 
        final_markdown = final_markdown[:-5]

    output_filepath = os.path.join(output_dir, collection_filename)
    try:
        with open(output_filepath, 'w', encoding='utf-8') as f_coll:
            f_coll.write(final_markdown)
        logging.info(f"  Successfully wrote collection: {output_filepath}")
    except IOError as e:
        logging.error(f"  Error writing collection file {output_filepath}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Generate derived collection views from a standards index.")
    parser.add_argument("--repo-base", default=".", help="Base directory of the repository. Defaults to current directory.")
    parser.add_argument("--index-file", default="master-knowledge-base/dist/standards_index.json", help="Path to the standards index JSON file, relative to repo-base.")
    parser.add_argument("--definitions-file", default="master-knowledge-base/tools/builder/collection_definitions.yaml", help="Path to the collection definitions YAML file, relative to repo-base.")
    parser.add_argument("--output-dir", default="master-knowledge-base/dist/collections", help="Directory to save generated collection files, relative to repo-base.")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="Set the logging level.")
    
    args = parser.parse_args()

    # Reconfigure logging level based on CLI argument
    logging.basicConfig(level=getattr(logging, args.log_level.upper()), format='%(levelname)s: %(message)s', force=True)

    repo_base_abs = os.path.abspath(args.repo_base)
    index_file_abs = os.path.abspath(os.path.join(repo_base_abs, args.index_file))
    collection_config_abs = os.path.abspath(os.path.join(repo_base_abs, args.definitions_file))
    output_dir_abs = os.path.abspath(os.path.join(repo_base_abs, args.output_dir))

    if not os.path.exists(output_dir_abs):
        os.makedirs(output_dir_abs)
        logging.info(f"Created output directory: {output_dir_abs}")

    all_standards_map = load_standards_index(index_file_abs)
    if not all_standards_map:
        logging.error("Could not load standards map from index or index is empty/invalid. Exiting.")
        return

    collection_defs = load_collection_definitions(collection_config_abs)
    if not collection_defs:
        logging.warning(f"No collection definitions found or loaded from {collection_config_abs}. Please check the file.")
        return

    logging.info(f"Loaded {len(all_standards_map)} standards from index.")
    logging.info(f"Loaded {len(collection_defs)} collection definitions.")

    for collection_def in collection_defs:
        generate_single_collection(collection_def, all_standards_map, output_dir_abs, repo_base_abs)
    
    logging.info("Collection generation process completed.")

if __name__ == "__main__":
    main()
