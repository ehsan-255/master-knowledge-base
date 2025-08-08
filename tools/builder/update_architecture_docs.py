#!/usr/bin/env python3
"""
This script automates the updating of the primary architectural documents:
- AS-MAP-STANDARDS-KB.md
- AS-ROOT-STANDARDS-KB.md

It reads data from the master JSON-LD index to ensure that the architectural
documents are always synchronized with the current state of the standards.
"""

import json
import os
import sys
import re
import argparse
from pathlib import Path
from datetime import datetime

# Define project structure
ROOT = Path(__file__).resolve().parents[2]
STANDARDS_SRC_DIR = ROOT / 'standards' / 'src'
MASTER_INDEX_PATH = ROOT / 'standards' / 'registry' / 'master-index.jsonld'
AS_MAP_PATH = STANDARDS_SRC_DIR / 'AS-MAP-STANDARDS-KB.md'
AS_ROOT_PATH = STANDARDS_SRC_DIR / 'AS-ROOT-STANDARDS-KB.md'
LOG_DIR = ROOT / 'tools' / 'reports'

def load_master_index(path: Path) -> dict:
    """Loads and parses the master index JSON-LD file."""
    if not path.exists():
        print(f"Error: Master index not found at '{path}'")
        sys.exit(1)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Could not parse master index JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while reading the master index: {e}")
        sys.exit(1)

def process_index_data(master_index: dict) -> tuple:
    """Processes the master index to extract counts and navigation links."""
    domain_counts = {}
    nav_links = {}
    concept_links = []

    for item in master_index.get('kb:documents', []):
        std_id = item.get('kb:standard_id')
        if not std_id:
            continue
        
        # Check if it's a foundational concept
        if std_id.startswith('CONCEPT-'):
            concept_links.append(std_id)
            # Concepts might not belong to a domain count of standards
            continue

        # Extract domain (e.g., 'AS' from 'AS-...')
        domain = std_id.split('-')[0]
        domain_counts[domain] = domain_counts.get(domain, 0) + 1
        
        # Store for navigation
        nav_links.setdefault(domain, []).append(std_id)

    return domain_counts, nav_links, sorted(concept_links)

def update_as_map(domain_counts: dict, dry_run: bool = False):
    """Updates the standard_count fields in AS-MAP-STANDARDS-KB.md."""
    print("Updating AS-MAP-STANDARDS-KB.md...")
    if dry_run:
        print("  (Dry run, no changes will be made)")

    # This is a simplified YAML parser. For production, a library like ruamel.yaml
    # would be better to preserve comments and structure.
    content = AS_MAP_PATH.read_text(encoding='utf-8')
    new_content = []
    in_frontmatter = False
    
    # Domain to part_id mapping from the document itself
    domain_to_part = {
        'AS': 'architecture-structure',
        'CS': 'content-style-policies',
        'GM': 'general-management',
        'MT': 'metadata-tagging',
        'OM': 'operational-management',
        'QM': 'quality-validation',
        'SF': 'syntax-formatting',
        'UA': 'utilities-assets'
    }

    current_part_id = None
    for line in content.splitlines():
        if line.strip() == '---':
            in_frontmatter = not in_frontmatter
            new_content.append(line)
            continue
        
        if in_frontmatter:
            part_id_match = re.search(r'part_id:\s*"([^"]+)"', line)
            if part_id_match:
                current_part_id = part_id_match.group(1)

            if 'standard_count:' in line and current_part_id:
                for domain, part_id in domain_to_part.items():
                    if part_id == current_part_id:
                        if domain in domain_counts:
                            line = f"    standard_count: {domain_counts[domain]}"
                        break
                current_part_id = None # Reset after use

        new_content.append(line)
    
    if not dry_run:
        AS_MAP_PATH.write_text('\n'.join(new_content), encoding='utf-8')

    print("AS-MAP-STANDARDS-KB.md update complete.")

def update_as_root(nav_links: dict, concept_links: list, dry_run: bool = False):
    """Updates the navigation link lists in AS-ROOT-STANDARDS-KB.md."""
    print("Updating AS-ROOT-STANDARDS-KB.md...")
    if dry_run:
        print("  (Dry run, no changes will be made)")

    # Generate new concepts content
    new_concepts_content = "### 1. Foundational Concepts\n\n"
    if concept_links:
        for concept_id in concept_links:
            new_concepts_content += f"- [[{concept_id}]]\n"
    else:
        # Provide helpful placeholder content when no concept documents exist
        new_concepts_content += "_Foundational concept documents are planned for future development._\n"
        new_concepts_content += "_This section will be populated as concept documents are created with IDs starting with 'CONCEPT-'._\n"
    new_concepts_content += "\n"

    # Generate new standards navigation content
    new_nav_content = "### 2. Standards by Domain\n\n"
    for domain in sorted(nav_links.keys()):
        new_nav_content += f"#### {domain}\n\n"
        for std_id in sorted(nav_links[domain]):
            new_nav_content += f"- [[{std_id}]]\n"
        new_nav_content += "\n"

    content = AS_ROOT_PATH.read_text(encoding='utf-8')
    
    # Replace the old concepts section - look for the actual next heading in the file
    content = re.sub(
        r"(### 1\. Foundational Concepts)[\s\S]*?(?=### 2\.)",
        new_concepts_content,
        content,
        count=1
    )

    # Don't replace the standards section since the current structure is manually maintained
    # This script only updates the Foundational Concepts section

    if not dry_run:
        AS_ROOT_PATH.write_text(content, encoding='utf-8')

    print("AS-ROOT-STANDARDS-KB.md update complete.")

def main():
    """Main function to update architectural documents."""
    parser = argparse.ArgumentParser(description="Update architectural documents from master index.")
    parser.add_argument('--dry-run', action='store_true', help="Run without making any changes.")
    args = parser.parse_args()

    print("Starting architectural document synchronization...")
    
    master_index = load_master_index(MASTER_INDEX_PATH)
    print(f"Successfully loaded master index with {len(master_index.get('kb:documents', []))} entries.")

    domain_counts, nav_links, concept_links = process_index_data(master_index)
    print(f"Processed data. Found {len(domain_counts)} domains and {len(concept_links)} concepts.")

    update_as_map(domain_counts, dry_run=args.dry_run)
    update_as_root(nav_links, concept_links, dry_run=args.dry_run)

    print("Architectural document synchronization complete.")

if __name__ == '__main__':
    sys.exit(main()) 