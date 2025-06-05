#!/usr/bin/env python3
"""
Generate Registry Files from YAML Single Source of Truth

This script implements the Single Source of Truth principle by reading from the authoritative
mt-schema-frontmatter.yaml file and generating all related registry files.

Following the DITA/RDF/OWL inspired KB architecture where mt-schema-frontmatter.yaml
is the canonical source for all frontmatter-related controlled vocabularies.

Author: Auto-generated from SST principles
Date: 2025-06-04 (Updated for YAML SST)
"""

import os
import sys
import re
import yaml
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

class FrontmatterRegistryGenerator:
    """Generates registry files from YAML single source of truth."""
    
    def __init__(self, repo_base: str, dry_run: bool = True):
        self.repo_base = Path(repo_base).resolve()
        self.dry_run = dry_run
        self.timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        
        # Auto-detect if we're in the wrong directory and adjust
        # If repo_base doesn't contain the expected structure, look for master-knowledge-base
        expected_yaml = self.repo_base / "standards" / "registry" / "mt-schema-frontmatter.yaml"
        if not expected_yaml.exists():
            # Try looking in master-knowledge-base subdirectory
            alt_base = self.repo_base / "master-knowledge-base"
            alt_yaml = alt_base / "standards" / "registry" / "mt-schema-frontmatter.yaml"
            if alt_yaml.exists():
                self.repo_base = alt_base
                print(f"INFO: Auto-detected correct repo base: {self.repo_base}")
        
        # Paths following established conventions
        self.yaml_source = self.repo_base / "standards" / "registry" / "mt-schema-frontmatter.yaml"
        self.registry_dir = self.repo_base / "standards" / "registry"
        self.reports_dir = self.repo_base / "tools" / "reports"
        
        # Ensure reports directory exists
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize logging
        self.log_file = self.reports_dir / f"frontmatter-registry-generation-{self.timestamp}.log"
        self.log_entries = []
        
        self.log(f"Initializing FrontmatterRegistryGenerator")
        self.log(f"Resolved repo base: {self.repo_base}")
        self.log(f"YAML source: {self.yaml_source}")
        self.log(f"Registry target: {self.registry_dir}")
        self.log(f"Dry run mode: {self.dry_run}")
    
    def log(self, message: str, level: str = "INFO"):
        """Log message with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        self.log_entries.append(log_entry)
        print(log_entry)
    
    def save_log(self):
        """Save log to reports directory."""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(self.log_entries))
            self.log(f"Log saved to: {self.log_file}")
        except Exception as e:
            print(f"ERROR: Failed to save log: {e}")
    
    def load_yaml_source(self) -> Dict[str, Any]:
        """Load the YAML single source of truth."""
        try:
            if not self.yaml_source.exists():
                raise FileNotFoundError(f"YAML source file not found: {self.yaml_source}")
            
            with open(self.yaml_source, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            self.log(f"Loaded YAML source: {len(str(data))} characters")
            return data
        except Exception as e:
            self.log(f"Failed to load YAML source: {e}", "ERROR")
            raise
    
    def extract_info_types(self, data: Dict[str, Any]) -> List[str]:
        """Extract info-type controlled vocabulary from YAML data."""
        self.log("Extracting info-type controlled vocabulary...")
        
        info_types = data.get('controlled_vocabularies', {}).get('info_type', [])
        
        self.log(f"Extracted {len(info_types)} info-type values")
        for info_type in info_types:
            self.log(f"  - {info_type}")
        
        return info_types
    
    def extract_field_definitions(self, data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Extract field definitions from YAML data."""
        self.log("Extracting field definitions...")
        
        fields_data = data.get('fields', {})
        fields = {}
        
        for field_name, field_def in fields_data.items():
            # Convert YAML structure to expected format
            processed_field = {
                'name': field_name,
                'description': field_def.get('description', ''),
                'mandatory': field_def.get('mandatory', 'unknown'),
                'data_type': field_def.get('data_type', 'unknown'),
                'validation_rules': '; '.join(field_def.get('validation_rules', [])),
                'controlled_vocabulary': field_def.get('controlled_vocabulary', False)
            }
            fields[field_name] = processed_field
            self.log(f"  - {field_name}: {processed_field.get('mandatory', 'unknown')} | {processed_field.get('data_type', 'unknown')}")
        
        self.log(f"Extracted {len(fields)} field definitions")
        return fields
    

    
    def extract_field_order(self, data: Dict[str, Any]) -> List[str]:
        """Extract the mandatory field order from YAML data."""
        self.log("Extracting field order...")
        
        field_order = data.get('field_order', [])
        
        self.log(f"Extracted field order with {len(field_order)} fields")
        for i, field in enumerate(field_order, 1):
            self.log(f"  {i}. {field}")
        
        return field_order
    
    def generate_info_types_txt(self, info_types: List[str]) -> str:
        """Generate info_types.txt content."""
        self.log("Generating info_types.txt content...")
        
        header = [
            "# Generated from mt-schema-frontmatter.yaml - Single Source of Truth",
            f"# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "# DO NOT EDIT MANUALLY - Regenerate using generate_frontmatter_registry.py",
            ""
        ]
        
        content_lines = header + info_types
        return "\n".join(content_lines)
    
    def generate_frontmatter_fields_yaml(self, fields: Dict[str, Dict[str, Any]]) -> str:
        """Generate comprehensive frontmatter fields registry."""
        self.log("Generating frontmatter_fields.yaml content...")
        
        registry_data = {
            'registry_id': 'FRONTMATTER_FIELDS',
            'description': 'Comprehensive registry of frontmatter fields generated from mt-schema-frontmatter.yaml',
            'generated_from': 'mt-schema-frontmatter.yaml',
            'generated_on': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'fields': []
        }
        
        for field_name, field_def in fields.items():
            field_entry = {
                'name': field_name,
                'description': field_def.get('description', ''),
                'mandatory': field_def.get('mandatory', 'unknown'),
                'data_type': field_def.get('data_type', 'unknown'),
                'validation_rules': field_def.get('validation_rules', ''),
                'controlled_vocabulary': field_def.get('controlled_vocabulary', False)
            }
            registry_data['fields'].append(field_entry)
        
        return yaml.dump(registry_data, default_flow_style=False, sort_keys=False)
    
    def generate_field_order_yaml(self, field_order: List[str]) -> str:
        """Generate field order registry."""
        self.log("Generating field_order.yaml content...")
        
        registry_data = {
            'registry_id': 'FRONTMATTER_FIELD_ORDER',
            'description': 'Mandatory field order for frontmatter generated from mt-schema-frontmatter.yaml',
            'generated_from': 'mt-schema-frontmatter.yaml',
            'generated_on': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'mandatory_order': field_order
        }
        
        return yaml.dump(registry_data, default_flow_style=False, sort_keys=False)
    
    def load_additional_yaml(self, filename: str) -> Dict[str, Any]:
        """Load additional YAML files from registry directory."""
        yaml_path = self.registry_dir / filename
        try:
            if not yaml_path.exists():
                self.log(f"Additional YAML file not found: {yaml_path}", "WARNING")
                return {}
            
            with open(yaml_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                self.log(f"Loaded additional YAML: {filename} ({len(str(data))} characters)")
                return data if data is not None else {}
        except Exception as e:
            self.log(f"Failed to load additional YAML {filename}: {e}", "ERROR")
            return {}
    
    def generate_criticality_levels_txt(self) -> str:
        """Generate criticality_levels.txt from criticality_levels.yaml."""
        self.log("Generating criticality_levels.txt content...")
        
        criticality_data = self.load_additional_yaml("criticality_levels.yaml")
        if not criticality_data:
            self.log("No criticality levels data found", "WARNING")
            return ""
        
        content_lines = [
            "# Generated from criticality_levels.yaml - Single Source of Truth",
            "# Generated on: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "# DO NOT EDIT MANUALLY - Regenerate using generate_frontmatter_registry.py",
            ""
        ]
        
        # Extract tag values (lowercase format for tags)
        if isinstance(criticality_data, list):
            for item in criticality_data:
                if isinstance(item, dict) and 'level' in item:
                    # Convert P0-Critical to p0-critical format for tags
                    level = item['level'].lower().replace('-', '-')
                    content_lines.append(level)
        
        return '\n'.join(content_lines)
    
    def generate_lifecycle_gatekeepers_txt(self) -> str:
        """Generate lifecycle_gatekeepers.txt from lifecycle_gatekeepers.yaml."""
        self.log("Generating lifecycle_gatekeepers.txt content...")
        
        gatekeeper_data = self.load_additional_yaml("lifecycle_gatekeepers.yaml")
        if not gatekeeper_data:
            self.log("No lifecycle gatekeepers data found", "WARNING")
            return ""
        
        content_lines = [
            "# Generated from lifecycle_gatekeepers.yaml - Single Source of Truth",
            "# Generated on: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "# DO NOT EDIT MANUALLY - Regenerate using generate_frontmatter_registry.py",
            ""
        ]
        
        # Extract gatekeeper values
        if isinstance(gatekeeper_data, list):
            for item in gatekeeper_data:
                if isinstance(item, dict) and 'gatekeeper' in item:
                    content_lines.append(item['gatekeeper'])
        
        return '\n'.join(content_lines)
    
    def generate_tag_categories_txt(self) -> str:
        """Generate tag_categories.txt from common tag prefixes."""
        self.log("Generating tag_categories.txt content...")
        
        content_lines = [
            "# Generated tag category prefixes - Single Source of Truth",
            "# Generated on: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "# DO NOT EDIT MANUALLY - Regenerate using generate_frontmatter_registry.py",
            "",
            "# Common tag category prefixes used in the knowledge base",
            "status/",
            "criticality/",
            "content-type/",
            "topic/",
            "kb-id/",
            "lifecycle_gatekeeper/"
        ]
        
        return '\n'.join(content_lines)
    
    def write_registry_file(self, filename: str, content: str) -> bool:
        """Write registry file with dry-run support."""
        file_path = self.registry_dir / filename
        
        if self.dry_run:
            self.log(f"DRY RUN: Would write {filename} ({len(content)} characters)")
            # Save to reports for review
            preview_path = self.reports_dir / f"preview-{filename}"
            try:
                with open(preview_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.log(f"DRY RUN: Preview saved to {preview_path}")
            except Exception as e:
                self.log(f"Failed to save preview: {e}", "ERROR")
            return True
        else:
            try:
                # Ensure registry directory exists
                self.registry_dir.mkdir(parents=True, exist_ok=True)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.log(f"LIVE: Written {filename} ({len(content)} characters)")
                return True
            except Exception as e:
                self.log(f"Failed to write {filename}: {e}", "ERROR")
                return False
    
    def generate_all_registries(self) -> bool:
        """Main method to generate all registry files from YAML source."""
        try:
            self.log("Starting registry generation from mt-schema-frontmatter.yaml")
            
            # Load YAML source
            data = self.load_yaml_source()
            
            # Extract data
            info_types = self.extract_info_types(data)
            fields = self.extract_field_definitions(data)
            field_order = self.extract_field_order(data)
            
            # Generate registry files
            success = True
            
            # 1. Generate info_types.txt
            if info_types:
                info_types_content = self.generate_info_types_txt(info_types)
                success &= self.write_registry_file("info_types.txt", info_types_content)
            else:
                self.log("No info-types extracted, skipping info_types.txt", "WARNING")
            
            # 2. Generate frontmatter_fields.yaml
            if fields:
                fields_content = self.generate_frontmatter_fields_yaml(fields)
                success &= self.write_registry_file("frontmatter_fields.yaml", fields_content)
            else:
                self.log("No fields extracted, skipping frontmatter_fields.yaml", "WARNING")
            
            # 3. Generate field_order.yaml
            if field_order:
                order_content = self.generate_field_order_yaml(field_order)
                success &= self.write_registry_file("field_order.yaml", order_content)
            else:
                self.log("No field order extracted, skipping field_order.yaml", "WARNING")
            
            # 4. Generate criticality_levels.txt
            criticality_content = self.generate_criticality_levels_txt()
            if criticality_content:
                success &= self.write_registry_file("criticality_levels.txt", criticality_content)
            else:
                self.log("Failed to generate criticality_levels.txt", "WARNING")
            
            # 5. Generate lifecycle_gatekeepers.txt
            gatekeepers_content = self.generate_lifecycle_gatekeepers_txt()
            if gatekeepers_content:
                success &= self.write_registry_file("lifecycle_gatekeepers.txt", gatekeepers_content)
            else:
                self.log("Failed to generate lifecycle_gatekeepers.txt", "WARNING")
            
            # 6. Generate tag_categories.txt
            tag_categories_content = self.generate_tag_categories_txt()
            if tag_categories_content:
                success &= self.write_registry_file("tag_categories.txt", tag_categories_content)
            else:
                self.log("Failed to generate tag_categories.txt", "WARNING")
            
            # Generate summary report
            self.generate_summary_report(info_types, fields, field_order)
            
            if success:
                self.log("Registry generation completed successfully")
            else:
                self.log("Registry generation completed with errors", "WARNING")
            
            return success
            
        except Exception as e:
            self.log(f"Registry generation failed: {e}", "ERROR")
            return False
    
    def generate_summary_report(self, info_types: List[str], fields: Dict[str, Dict[str, Any]], field_order: List[str]):
        """Generate summary report of extraction and generation."""
        report_content = [
            "# Frontmatter Registry Generation Report",
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Source: {self.yaml_source}",
            f"Mode: {'DRY RUN' if self.dry_run else 'LIVE'}",
            "",
            "## Extraction Summary",
            f"- Info-types extracted: {len(info_types)}",
            f"- Field definitions extracted: {len(fields)}",
            f"- Field order positions: {len(field_order)}",
            "",
            "## Generated Files",
            "- info_types.txt (from mt-schema-frontmatter.yaml)",
            "- frontmatter_fields.yaml (from mt-schema-frontmatter.yaml)", 
            "- field_order.yaml (from mt-schema-frontmatter.yaml)",
            "- criticality_levels.txt (from criticality_levels.yaml)",
            "- lifecycle_gatekeepers.txt (from lifecycle_gatekeepers.yaml)",
            "- tag_categories.txt (common prefixes)",
            "",
            "## Info-Types Extracted",
        ]
        
        for info_type in info_types:
            report_content.append(f"- {info_type}")
        
        report_content.extend([
            "",
            "## Field Definitions Summary",
        ])
        
        for field_name, field_def in fields.items():
            mandatory = field_def.get('mandatory', 'unknown')
            data_type = field_def.get('data_type', 'unknown')
            controlled_vocab = field_def.get('controlled_vocabulary', False)
            cv_indicator = " [CV]" if controlled_vocab else ""
            report_content.append(f"- {field_name}: {mandatory} | {data_type}{cv_indicator}")
        
        report_content.extend([
            "",
            "## Field Order",
        ])
        
        for i, field in enumerate(field_order, 1):
            report_content.append(f"{i:2d}. {field}")
        
        # Save report
        report_path = self.reports_dir / f"frontmatter-registry-summary-{self.timestamp}.md"
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(report_content))
            self.log(f"Summary report saved to: {report_path}")
        except Exception as e:
            self.log(f"Failed to save summary report: {e}", "ERROR")

def main():
    """Main entry point with command line argument handling."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate registry files from mt-schema-frontmatter.yaml (Single Source of Truth)"
    )
    parser.add_argument(
        "--repo-base", 
        default=".", 
        help="Base path of the repository (default: current directory)"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        default=True,
        help="Perform dry run without writing files (default: True)"
    )
    parser.add_argument(
        "--live", 
        action="store_true", 
        help="Perform live run and write files (overrides --dry-run)"
    )
    
    args = parser.parse_args()
    
    # Determine run mode
    dry_run = not args.live if args.live else args.dry_run
    
    # Initialize generator
    generator = FrontmatterRegistryGenerator(args.repo_base, dry_run=dry_run)
    
    try:
        # Generate registries
        success = generator.generate_all_registries()
        
        # Save log
        generator.save_log()
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        generator.log("Generation interrupted by user", "WARNING")
        generator.save_log()
        sys.exit(130)
    except Exception as e:
        generator.log(f"Unexpected error: {e}", "ERROR")
        generator.save_log()
        sys.exit(1)

if __name__ == "__main__":
    main() 