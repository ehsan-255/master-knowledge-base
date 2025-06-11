#!/usr/bin/env python3
"""
Knowledge Base Reconciliation Engine
Refactored from generate_index.py to implement three-way reconciliation logic

This script:
1. Loads existing master-index.jsonld (if it exists)
2. Scans the entire knowledge base for all .md files
3. Implements three-way reconciliation: ADD new file nodes, UPDATE existing nodes if frontmatter changed, REMOVE nodes for deleted files
4. Outputs the updated master-index.jsonld file in JSON-LD format
"""

import json
import os
import datetime
import yaml
import argparse
import logging
import hashlib
from pathlib import Path

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
    if fm_end_index == -1: 
        return None
    return "".join(lines[1:fm_end_index])

def calculate_content_hash(file_content):
    """Calculate SHA-256 hash of file content for change detection."""
    return hashlib.sha256(file_content.encode('utf-8')).hexdigest()

def extract_frontmatter_metadata(filepath_rel_to_repo, file_content):
    """
    Extracts frontmatter metadata from a markdown file.
    Returns a dictionary with the frontmatter data or None if no frontmatter.
    """
    frontmatter_str = get_frontmatter_from_content(file_content)
    if not frontmatter_str:
        return None

    try:
        frontmatter_data = yaml.safe_load(frontmatter_str)
        if not isinstance(frontmatter_data, dict):
            return None
    except yaml.YAMLError:
        return None

    return frontmatter_data

def create_node_from_file(filepath_rel_to_repo, file_content, file_stats):
    """
    Creates a JSON-LD node from a markdown file.
    """
    frontmatter = extract_frontmatter_metadata(filepath_rel_to_repo, file_content)
    content_hash = calculate_content_hash(file_content)
    
    # Create base node structure
    node = {
        "@type": "kb:Document",
        "@id": f"kb:doc-{filepath_rel_to_repo.replace('/', '-').replace('.md', '')}",
        "kb:filepath": filepath_rel_to_repo,
        "kb:contentHash": content_hash,
        "kb:fileSize": len(file_content),
        "kb:lastModified": datetime.datetime.fromtimestamp(file_stats.st_mtime, datetime.timezone.utc).isoformat(),
        "kb:indexed": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    
    # Add frontmatter fields if they exist
    if frontmatter:
        for key, value in frontmatter.items():
            # Convert frontmatter keys to kb: namespace
            kb_key = f"kb:{key.replace('-', '_')}"
            # Ensure dates are converted to strings for JSON serialization
            if hasattr(value, 'isoformat'):
                node[kb_key] = value.isoformat()
            else:
                node[kb_key] = value
    
    return node

def load_existing_index(index_filepath):
    """
    Loads existing master-index.jsonld file if it exists.
    Returns the index data or creates a new empty index structure.
    """
    if os.path.exists(index_filepath):
        try:
            with open(index_filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logging.warning(f"Could not load existing index from {index_filepath}: {e}")
            logging.warning("Creating new index from scratch.")
    
    # Create new index structure
    return {
        "@context": [
            "contexts/base.jsonld",
            "contexts/fields.jsonld"
        ],
        "@type": "kb:MasterIndex",
        "@id": "kb:master-index",
        "kb:schemaVersion": "1.0.0",
        "kb:title": "Knowledge Base Master Index",
        "kb:description": "Complete inventory of all knowledge base documents",
        "kb:created": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "kb:modified": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "kb:version": "1.0.0",
        "kb:documents": []
    }

def scan_knowledge_base(repo_base_path, exclude_dirs=None):
    """
    Scans the entire knowledge base for all .md files.
    Returns a dictionary mapping relative file paths to file info.
    """
    if exclude_dirs is None:
        exclude_dirs = {'.git', 'node_modules', '__pycache__', '.vscode', 'archive'}
    
    found_files = {}
    repo_path = Path(repo_base_path)
    
    for md_file in repo_path.rglob('*.md'):
        # Skip files in excluded directories
        if any(excluded in md_file.parts for excluded in exclude_dirs):
            continue
            
        rel_path = md_file.relative_to(repo_path).as_posix()
        
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            file_stats = md_file.stat()
            found_files[rel_path] = {
                'content': content,
                'stats': file_stats,
                'abs_path': str(md_file)
            }
        except (IOError, UnicodeDecodeError) as e:
            logging.warning(f"Could not read file {rel_path}: {e}")
            continue
    
    return found_files

def reconcile_index(existing_index, current_files):
    """
    Implements three-way reconciliation logic:
    - ADD: New files not in existing index
    - UPDATE: Existing files with changed content
    - REMOVE: Files in index but no longer exist
    """
    reconciliation_stats = {
        'added': 0,
        'updated': 0,
        'removed': 0,
        'unchanged': 0
    }
    
    # Create lookup for existing documents by filepath
    existing_docs = {}
    for doc in existing_index.get('kb:documents', []):
        filepath = doc.get('kb:filepath')
        if filepath:
            existing_docs[filepath] = doc
    
    new_documents = []
    
    # Process current files (ADD and UPDATE)
    for filepath, file_info in current_files.items():
        content = file_info['content']
        stats = file_info['stats']
        content_hash = calculate_content_hash(content)
        
        if filepath in existing_docs:
            # File exists in index - check if it needs updating
            existing_doc = existing_docs[filepath]
            existing_hash = existing_doc.get('kb:contentHash')
            
            if existing_hash != content_hash:
                # Content changed - UPDATE
                updated_node = create_node_from_file(filepath, content, stats)
                new_documents.append(updated_node)
                reconciliation_stats['updated'] += 1
                logging.debug(f"UPDATE: {filepath}")
            else:
                # Content unchanged - keep existing
                new_documents.append(existing_doc)
                reconciliation_stats['unchanged'] += 1
        else:
            # New file - ADD
            new_node = create_node_from_file(filepath, content, stats)
            new_documents.append(new_node)
            reconciliation_stats['added'] += 1
            logging.debug(f"ADD: {filepath}")
    
    # Check for removed files (REMOVE)
    current_filepaths = set(current_files.keys())
    for filepath in existing_docs.keys():
        if filepath not in current_filepaths:
            reconciliation_stats['removed'] += 1
            logging.debug(f"REMOVE: {filepath}")
    
    # Update the index
    existing_index['kb:documents'] = new_documents
    existing_index['kb:modified'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    existing_index['kb:documentCount'] = len(new_documents)
    
    return existing_index, reconciliation_stats

def save_index(index_data, output_filepath):
    """
    Saves the master index to the specified file.
    """
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    
    try:
        with open(output_filepath, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        logging.error(f"Error writing index file: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Knowledge Base Reconciliation Engine")
    parser.add_argument("--repo-base", default=".", 
                        help="Path to the repository root. Default is current directory.")
    parser.add_argument("--index-file", default="standards/registry/master-index.jsonld", 
                        help="Path to the master index file, relative to repo-base.")
    parser.add_argument("--log-level", default="INFO", 
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="Set the logging level (default: INFO).")
    parser.add_argument("--exclude-dirs", nargs='+', 
                        default=['.git', 'node_modules', '__pycache__', '.vscode', 'archive'],
                        help="Directories to exclude from scanning.")

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=getattr(logging, args.log_level.upper()),
                        format='%(levelname)s: %(message)s')

    logging.info("Starting Knowledge Base Reconciliation Engine...")
    
    repo_base_abs_path = os.path.abspath(args.repo_base)
    index_file_abs = os.path.join(repo_base_abs_path, args.index_file)
    
    # Load existing index
    logging.info("Loading existing master index...")
    existing_index = load_existing_index(index_file_abs)
    
    # Scan knowledge base for current files
    logging.info("Scanning knowledge base for markdown files...")
    current_files = scan_knowledge_base(repo_base_abs_path, set(args.exclude_dirs))
    logging.info(f"Found {len(current_files)} markdown files")
    
    # Perform reconciliation
    logging.info("Performing three-way reconciliation...")
    updated_index, stats = reconcile_index(existing_index, current_files)
    
    # Save updated index
    logging.info("Saving updated master index...")
    if save_index(updated_index, index_file_abs):
        logging.info(f"Successfully saved master index to: {args.index_file}")
    else:
        logging.error("Failed to save master index")
        return 1
    
    # Report reconciliation statistics
    logging.info("\n--- Reconciliation Summary ---")
    logging.info(f"Added: {stats['added']} files")
    logging.info(f"Updated: {stats['updated']} files")
    logging.info(f"Removed: {stats['removed']} files")
    logging.info(f"Unchanged: {stats['unchanged']} files")
    logging.info(f"Total documents in index: {len(updated_index['kb:documents'])}")
    
    return 0

if __name__ == "__main__":
    exit(main()) 