#!/usr/bin/env python3
"""
Schema Documentation Generator

This script reads from the YAML Single Source of Truth (mt-schema-frontmatter.yaml)
and generates markdown documentation sections for:
1. MT-SCHEMA-FRONTMATTER.md - Field definitions section
2. GM-CONVENTIONS-NAMING.md - Section 2.2 (Frontmatter Field Names)

The script preserves manual content while updating generated sections.
"""

import yaml
import os
import sys
import re
from datetime import datetime
from pathlib import Path

# Add the tools directory to the Python path for imports
tools_dir = Path(__file__).parent.parent
sys.path.insert(0, str(tools_dir))

class SchemaDocsGenerator:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.repo_root = Path(__file__).parent.parent.parent
        self.yaml_source = self.repo_root / "standards" / "registry" / "mt-schema-frontmatter.yaml"
        self.schema_md = self.repo_root / "standards" / "src" / "MT-SCHEMA-FRONTMATTER.md"
        self.naming_md = self.repo_root / "standards" / "src" / "GM-CONVENTIONS-NAMING.md"
        self.reports_dir = self.repo_root / "tools" / "reports"
        
        # Ensure reports directory exists
        self.reports_dir.mkdir(exist_ok=True)
        
        # Load YAML data
        self.schema_data = self._load_yaml_source()
        
        # Setup logging
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.reports_dir / f"schema_docs_generation_{timestamp}.log"
        self.log_messages = []
        
    def _load_yaml_source(self):
        """Load the YAML SST file"""
        try:
            with open(self.yaml_source, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self._log(f"ERROR: Failed to load YAML source {self.yaml_source}: {e}")
            sys.exit(1)
    
    def _log(self, message):
        """Log a message to both console and log file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        self.log_messages.append(log_entry)
    
    def _save_log(self):
        """Save log messages to file"""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.log_messages))
        self._log(f"Log saved to: {self.log_file}")
    
    def generate_field_definitions_section(self):
        """Generate the field definitions section for MT-SCHEMA-FRONTMATTER.md"""
        self._log("Generating field definitions section...")
        
        sections = []
        sections.append("## Detailed Key Definitions")
        sections.append("")
        
        # Get field order from YAML
        field_order = self.schema_data.get('field_order', [])
        fields = self.schema_data.get('fields', {})
        
        for field_name in field_order:
            if field_name not in fields:
                self._log(f"WARNING: Field '{field_name}' in order but not in definitions")
                continue
                
            field_def = fields[field_name]
            sections.append(f"### `{field_name}`")
            
            # Description
            desc = field_def.get('description', 'No description available')
            sections.append(f"*   **Description/Purpose:** {desc}")
            
            # Mandatory status
            mandatory = field_def.get('mandatory', False)
            if mandatory == True:
                sections.append("*   **Mandatory/Optional:** Mandatory.")
            elif mandatory == False:
                sections.append("*   **Mandatory/Optional:** Optional.")
            elif mandatory == "conditional":
                sections.append("*   **Mandatory/Optional:** Conditional.")
                conditions = field_def.get('mandatory_conditions', [])
                for condition in conditions:
                    sections.append(f"    - {condition}")
            
            # Data type
            data_type = field_def.get('data_type', 'Unknown')
            if data_type == "list_of_strings":
                sections.append("*   **Data Type:** List of Strings.")
            elif data_type == "string":
                sections.append("*   **Data Type:** String.")
            else:
                sections.append(f"*   **Data Type:** {data_type.title()}.")
            
            # Validation rules
            validation_rules = field_def.get('validation_rules', [])
            if validation_rules:
                if len(validation_rules) == 1:
                    sections.append(f"*   **Validation Rules & Constraints:** {validation_rules[0]}")
                else:
                    sections.append("*   **Validation Rules & Constraints:**")
                    for rule in validation_rules:
                        sections.append(f"    - {rule}")
            else:
                sections.append("*   **Validation Rules & Constraints:** None specified.")
            
            sections.append("")
        
        return '\n'.join(sections)
    
    def generate_controlled_vocabularies_section(self):
        """Generate the controlled vocabularies section"""
        self._log("Generating controlled vocabularies section...")
        
        sections = []
        sections.append("## Controlled Vocabularies")
        sections.append("")
        sections.append("This section defines or references the controlled vocabularies for specific frontmatter keys.")
        sections.append("")
        
        # Info-type vocabulary
        sections.append("### `info-type`")
        sections.append("")
        sections.append("The `info-type` key MUST use one of the following string values (all in kebab-case):")
        sections.append("")
        
        info_types = self.schema_data.get('controlled_vocabularies', {}).get('info_type', [])
        for info_type in info_types:
            sections.append(f"*   `{info_type}`")
        
        sections.append("")
        sections.append("### Other Controlled Vocabularies")
        sections.append("")
        
        # External vocabularies
        external_vocabs = self.schema_data.get('external_vocabularies', {})
        for field, vocab_info in external_vocabs.items():
            source = vocab_info.get('source', 'Unknown')
            desc = vocab_info.get('description', 'No description')
            sections.append(f"*   **`{field}`:** {desc} See `[[{source}]]`.")
        
        return '\n'.join(sections)
    
    def generate_naming_conventions_section(self):
        """Generate Section 2.2 for GM-CONVENTIONS-NAMING.md"""
        self._log("Generating naming conventions section...")
        
        sections = []
        sections.append("### 2.2 Frontmatter Field Names (CRITICAL)")
        sections.append("```")
        
        # Get all field names from the schema
        field_order = self.schema_data.get('field_order', [])
        
        # Format as comma-separated list with proper line breaks
        field_chunks = []
        current_chunk = []
        line_length = 0
        
        for field in field_order:
            field_with_comma = f"{field}, "
            if line_length + len(field_with_comma) > 70:  # Wrap at ~70 chars
                if current_chunk:
                    field_chunks.append(''.join(current_chunk).rstrip(', '))
                current_chunk = [field_with_comma]
                line_length = len(field_with_comma)
            else:
                current_chunk.append(field_with_comma)
                line_length += len(field_with_comma)
        
        # Add the last chunk
        if current_chunk:
            field_chunks.append(''.join(current_chunk).rstrip(', '))
        
        # Join chunks with line breaks
        for chunk in field_chunks:
            sections.append(chunk + ("," if chunk != field_chunks[-1] else ""))
        
        sections.append("```")
        sections.append("")
        
        return '\n'.join(sections)
    
    def update_schema_markdown(self):
        """Update MT-SCHEMA-FRONTMATTER.md with generated sections"""
        self._log(f"Updating {self.schema_md}...")
        
        try:
            with open(self.schema_md, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self._log(f"ERROR: Failed to read {self.schema_md}: {e}")
            return False
        
        # Generate new sections
        field_definitions = self.generate_field_definitions_section()
        controlled_vocabs = self.generate_controlled_vocabularies_section()
        
        # Replace field definitions section
        field_def_pattern = r'(## Detailed Key Definitions\n)(.*?)(\n## (?:Controlled Vocabularies|Relationship to Filename))'
        field_def_replacement = f'\\1\n{field_definitions}\n\\3'
        
        new_content = re.sub(field_def_pattern, field_def_replacement, content, flags=re.DOTALL)
        
        # Replace controlled vocabularies section
        vocab_pattern = r'(## Controlled Vocabularies\n)(.*?)(\n## (?:Relationship to Filename|$))'
        vocab_replacement = f'\\1\n{controlled_vocabs}\n\\3'
        
        new_content = re.sub(vocab_pattern, vocab_replacement, new_content, flags=re.DOTALL)
        
        if self.dry_run:
            preview_file = self.reports_dir / "MT-SCHEMA-FRONTMATTER_preview.md"
            with open(preview_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            self._log(f"DRY RUN: Preview saved to {preview_file}")
        else:
            with open(self.schema_md, 'w', encoding='utf-8') as f:
                f.write(new_content)
            self._log(f"Updated {self.schema_md}")
        
        return True
    
    def update_naming_markdown(self):
        """Update GM-CONVENTIONS-NAMING.md with generated Section 2.2"""
        self._log(f"Updating {self.naming_md}...")
        
        try:
            with open(self.naming_md, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self._log(f"ERROR: Failed to read {self.naming_md}: {e}")
            return False
        
        # Generate new section
        naming_section = self.generate_naming_conventions_section()
        
        # Replace Section 2.2
        section_pattern = r'(### 2\.2 Frontmatter Field Names \(CRITICAL\)\n)(.*?)(\n### 2\.3|\n## 3\.)'
        section_replacement = f'\\1{naming_section}\\3'
        
        new_content = re.sub(section_pattern, section_replacement, content, flags=re.DOTALL)
        
        if self.dry_run:
            preview_file = self.reports_dir / "GM-CONVENTIONS-NAMING_preview.md"
            with open(preview_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            self._log(f"DRY RUN: Preview saved to {preview_file}")
        else:
            with open(self.naming_md, 'w', encoding='utf-8') as f:
                f.write(new_content)
            self._log(f"Updated {self.naming_md}")
        
        return True
    
    def generate_summary_report(self):
        """Generate a summary report of the generation process"""
        self._log("Generating summary report...")
        
        field_count = len(self.schema_data.get('field_order', []))
        info_type_count = len(self.schema_data.get('controlled_vocabularies', {}).get('info_type', []))
        
        report = [
            "# Schema Documentation Generation Report",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Mode:** {'DRY RUN' if self.dry_run else 'LIVE RUN'}",
            "",
            "## Source Data Summary",
            f"- **YAML Source:** {self.yaml_source}",
            f"- **Fields Processed:** {field_count}",
            f"- **Info-type Values:** {info_type_count}",
            "",
            "## Generated Sections",
            "- **MT-SCHEMA-FRONTMATTER.md:** Field definitions and controlled vocabularies",
            "- **GM-CONVENTIONS-NAMING.md:** Section 2.2 (Frontmatter Field Names)",
            "",
            "## Field Order Processed",
        ]
        
        for i, field in enumerate(self.schema_data.get('field_order', []), 1):
            report.append(f"{i:2d}. `{field}`")
        
        report.extend([
            "",
            "## Info-type Values",
        ])
        
        for info_type in self.schema_data.get('controlled_vocabularies', {}).get('info_type', []):
            report.append(f"- `{info_type}`")
        
        # Save report
        report_file = self.reports_dir / f"schema_docs_generation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        self._log(f"Summary report saved to: {report_file}")
    
    def run(self):
        """Run the complete documentation generation process"""
        self._log("=== Schema Documentation Generator Started ===")
        self._log(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE RUN'}")
        self._log(f"YAML Source: {self.yaml_source}")
        
        if not self.yaml_source.exists():
            self._log(f"ERROR: YAML source file not found: {self.yaml_source}")
            return False
        
        success = True
        
        # Update schema markdown
        if not self.update_schema_markdown():
            success = False
        
        # Update naming markdown
        if not self.update_naming_markdown():
            success = False
        
        # Generate summary report
        self.generate_summary_report()
        
        # Save log
        self._save_log()
        
        if success:
            self._log("=== Schema Documentation Generation Completed Successfully ===")
        else:
            self._log("=== Schema Documentation Generation Completed with Errors ===")
        
        return success

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate schema documentation from YAML SST")
    parser.add_argument('--dry-run', action='store_true', 
                       help='Preview changes without modifying files')
    
    args = parser.parse_args()
    
    generator = SchemaDocsGenerator(dry_run=args.dry_run)
    success = generator.run()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 