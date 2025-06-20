#!/usr/bin/env python3
"""
Frontmatter Organizer Tool

Reorders frontmatter keys according to canonical order defined in the SST schema file.
Preserves all content while ensuring compliance with linting standards.
"""

import os
import sys
import argparse
import yaml
from pathlib import Path

class FrontmatterOrganizer:
    def __init__(self, repo_base_path="."):
        """Initialize with repository base path to locate schema file"""
        self.repo_base = Path(repo_base_path).resolve()
        
        # Handle both direct repo root and master-knowledge-base subdirectory
        if self.repo_base.name == "master-knowledge-base":
            self.schema_path = self.repo_base / "standards" / "registry" / "mt-schema-frontmatter.yaml"
        else:
            # Assume we're in repo root, look for master-knowledge-base subdirectory
            mkb_path = self.repo_base / "master-knowledge-base"
            if mkb_path.exists():
                self.schema_path = mkb_path / "standards" / "registry" / "mt-schema-frontmatter.yaml"
            else:
                # Fallback: assume current directory structure
                self.schema_path = self.repo_base / "standards" / "registry" / "mt-schema-frontmatter.yaml"
        
        self.canonical_key_order = self._load_canonical_key_order()
    
    def _load_canonical_key_order(self):
        """Load canonical key order from SST schema file"""
        try:
            if not self.schema_path.exists():
                print(f"ERROR: Schema file not found: {self.schema_path}")
                print("Falling back to hardcoded order for compatibility")
                return [
                    "title", "standard_id", "aliases", "tags", "kb-id", "info-type",
                    "primary-topic", "related-standards", "version", "date-created",
                    "date-modified", "primary_domain", "sub_domain", "scope_application",
                    "criticality", "lifecycle_gatekeeper", "impact_areas"
                ]
            
            with open(self.schema_path, 'r', encoding='utf-8') as f:
                schema_data = yaml.safe_load(f)
            
            field_order = schema_data.get('field_order', [])
            if not field_order:
                print(f"WARNING: No field_order found in {self.schema_path}")
                print("Falling back to hardcoded order for compatibility")
                return [
                    "title", "standard_id", "aliases", "tags", "kb-id", "info-type",
                    "primary-topic", "related-standards", "version", "date-created",
                    "date-modified", "primary_domain", "sub_domain", "scope_application",
                    "criticality", "lifecycle_gatekeeper", "impact_areas"
                ]
            
            print(f"SUCCESS: Loaded {len(field_order)} canonical keys from {self.schema_path}")
            return field_order
            
        except Exception as e:
            print(f"ERROR: Failed to load schema file {self.schema_path}: {e}")
            print("Falling back to hardcoded order for compatibility")
            return [
                "title", "standard_id", "aliases", "tags", "kb-id", "info-type",
                "primary-topic", "related-standards", "version", "date-created",
                "date-modified", "primary_domain", "sub_domain", "scope_application",
                "criticality", "lifecycle_gatekeeper", "impact_areas"
            ]
    
    def parse_frontmatter(self, content):
        """Parse YAML frontmatter from markdown content"""
        if not content.startswith('---\n'):
            return None, content
        
        try:
            # Find end of frontmatter
            end_marker = content.find('\n---\n', 4)
            if end_marker == -1:
                return None, content
            
            frontmatter_yaml = content[4:end_marker]
            body = content[end_marker + 5:]
            frontmatter = yaml.safe_load(frontmatter_yaml)
            return frontmatter, body
            
        except yaml.YAMLError:
            return None, content
    
    def serialize_frontmatter_with_order(self, frontmatter_dict):
        """Serialize frontmatter dict preserving canonical key order"""
        # Create ordered dict following canonical order
        ordered_items = []
        
        # Add keys in canonical order if they exist
        for key in self.canonical_key_order:
            if key in frontmatter_dict:
                ordered_items.append((key, frontmatter_dict[key]))
        
        # Add any additional keys not in canonical order at the end
        for key, value in frontmatter_dict.items():
            if key not in self.canonical_key_order:
                ordered_items.append((key, value))
        
        # Manually build YAML string to preserve order
        yaml_lines = []
        for key, value in ordered_items:
            if isinstance(value, list):
                yaml_lines.append(f"{key}: {yaml.dump(value, default_flow_style=True).strip()}")
            elif isinstance(value, str) and ('\n' in value or value.startswith(' ') or value.endswith(' ')):
                # Quote strings with special characters
                yaml_lines.append(f'{key}: "{value}"')
            else:
                yaml_lines.append(f"{key}: {value}")
        
        return '\n'.join(yaml_lines) + '\n'
    
    def needs_reordering(self, frontmatter_dict):
        """Check if frontmatter keys need reordering"""
        keys_in_doc = list(frontmatter_dict.keys())
        canonical_keys_in_doc = [k for k in keys_in_doc if k in self.canonical_key_order]
        
        # Check if canonical keys are in correct relative order
        last_canonical_idx = -1
        for key in canonical_keys_in_doc:
            current_canonical_idx = self.canonical_key_order.index(key)
            if current_canonical_idx < last_canonical_idx:
                return True
            last_canonical_idx = current_canonical_idx
        
        return False
    
    def organize_file(self, file_path, dry_run=False):
        """Organize frontmatter keys in a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            frontmatter, body = self.parse_frontmatter(content)
            if frontmatter is None:
                print(f"SKIP: No frontmatter found in {file_path}")
                return False
            
            if not self.needs_reordering(frontmatter):
                print(f"SKIP: {file_path} already has correct key order")
                return False
            
            if dry_run:
                print(f"DRY RUN: Would reorder keys in {file_path}")
                return True
            
            # Create backup
            backup_path = file_path.with_suffix(file_path.suffix + '.backup')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Create new content with canonical key ordering
            frontmatter_yaml = self.serialize_frontmatter_with_order(frontmatter)
            new_content = f"---\n{frontmatter_yaml}---\n{body}"
            
            # Write to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            # Remove backup on success
            backup_path.unlink()
            
            print(f"SUCCESS: Reordered keys in {file_path}")
            return True
            
        except Exception as e:
            print(f"ERROR: Failed to process {file_path}: {e}")
            # Restore backup if it exists
            backup_path = file_path.with_suffix(file_path.suffix + '.backup')
            if backup_path.exists():
                backup_path.rename(file_path)
                print(f"RESTORED: Backup restored for {file_path}")
            return False
    
    def organize_directory(self, directory_path, dry_run=False):
        """Organize frontmatter keys in all markdown files in directory"""
        directory = Path(directory_path)
        md_files = list(directory.rglob("*.md"))
        
        if not md_files:
            print(f"No markdown files found in {directory_path}")
            return 0
        
        processed_count = 0
        for md_file in md_files:
            if self.organize_file(md_file, dry_run):
                processed_count += 1
        
        return processed_count

def main():
    parser = argparse.ArgumentParser(description="Organize frontmatter keys according to canonical order")
    parser.add_argument("--file", "-f", help="Single file to organize")
    parser.add_argument("--directory", "-d", help="Directory to scan for markdown files")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying them")
    parser.add_argument("--repo-base", default=".", help="Path to the repository root (default: current directory)")
    
    args = parser.parse_args()
    
    if not args.file and not args.directory:
        parser.print_help()
        return
    
    organizer = FrontmatterOrganizer(args.repo_base)
    
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"ERROR: File not found: {args.file}")
            sys.exit(1)
        
        success = organizer.organize_file(file_path, args.dry_run)
        if args.dry_run:
            print(f"DRY RUN completed for {args.file}")
        elif success:
            print(f"Successfully organized {args.file}")
        else:
            print(f"No changes needed for {args.file}")
    
    elif args.directory:
        directory_path = Path(args.directory)
        if not directory_path.exists():
            print(f"ERROR: Directory not found: {args.directory}")
            sys.exit(1)
        
        count = organizer.organize_directory(directory_path, args.dry_run)
        if args.dry_run:
            print(f"DRY RUN: Would organize {count} files in {args.directory}")
        else:
            print(f"Successfully organized {count} files in {args.directory}")

if __name__ == "__main__":
    main() 