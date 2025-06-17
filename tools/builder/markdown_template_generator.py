#!/usr/bin/env python3
"""
Markdown Template Generation Engine

Implementation of Phase 2: Step 2.1.3 - Markdown Template Generation Engine  
From: ultimate-frontmatter-enhancement-guideline-20250617-0312.md

This module generates concise Markdown documentation from SHACL profile hierarchies
with strict line limit enforcement and comprehensive template management.
"""

from typing import Dict, List, Any, Tuple
from pathlib import Path
import re
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MarkdownTemplateGenerator:
    """
    Markdown Template Generation Engine for SHACL profile documentation.
    
    Generates concise documentation under specified line limits with 
    comprehensive template management and auto-generation notices.
    """
    
    def __init__(self, profile_hierarchy: Dict[str, Any]):
        self.profiles = profile_hierarchy
        self.templates = {
            'header': self._load_header_template(),
            'profile_section': self._load_profile_template(),
            'field_table': self._load_field_table_template(),
            'footer': self._load_footer_template()
        }
        
        # Initialize logger
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # Line counting cache
        self._line_count_cache = {}
    
    def generate_concise_documentation(self, target_line_limit: int = 180) -> str:
        """
        Generate concise documentation under specified line limit.
        
        Args:
            target_line_limit: Maximum number of lines for the generated documentation
            
        Returns:
            Generated Markdown documentation as string
        """
        self.logger.info(f"Starting concise documentation generation with {target_line_limit} line limit")
        
        # Step 1: Calculate space allocation per section
        self.logger.info("Step 1: Calculating space allocation...")
        space_allocation = self._calculate_space_allocation(target_line_limit)
        
        # Step 2: Generate header section
        self.logger.info("Step 2: Generating header section...")
        header_content = self._generate_header_section(space_allocation['header'])
        
        # Step 3: Generate profile sections with space constraints
        self.logger.info("Step 3: Generating profile sections...")
        profile_sections = []
        for profile_name, profile_data in self.profiles.get('document_type_profiles', {}).items():
            section = self._generate_profile_section(
                profile_name, profile_data, 
                space_allocation['profile']
            )
            profile_sections.append(section)
        
        # Step 4: Generate field reference tables
        self.logger.info("Step 4: Generating field reference tables...")
        field_tables = self._generate_field_tables(space_allocation['tables'])
        
        # Step 5: Generate footer with auto-generation notice
        self.logger.info("Step 5: Generating footer section...")
        footer_content = self._generate_footer_section()
        
        # Step 6: Assemble final document
        self.logger.info("Step 6: Assembling final document...")
        final_document = self._assemble_document(
            header_content, profile_sections, 
            field_tables, footer_content
        )
        
        # Step 7: Validate line count and optimize if needed
        self.logger.info("Step 7: Validating line count and optimizing...")
        actual_line_count = self._count_lines(final_document)
        if actual_line_count > target_line_limit:
            self.logger.warning(f"Document exceeds target ({actual_line_count} > {target_line_limit}), optimizing...")
            final_document = self._optimize_for_line_limit(final_document, target_line_limit)
        
        final_line_count = self._count_lines(final_document)
        self.logger.info(f"Documentation generation complete. Final line count: {final_line_count}")
        
        return final_document
    
    def _calculate_space_allocation(self, target_line_limit: int) -> Dict[str, int]:
        """Step 1: Calculate space allocation per section."""
        # Reserve space for fixed sections
        header_lines = 15  # Title, metadata, intro
        footer_lines = 8   # Auto-generation notice, timestamps
        reserved_lines = header_lines + footer_lines
        
        # Calculate available space for content
        available_lines = target_line_limit - reserved_lines
        
        # Allocate space based on content importance
        profile_count = len(self.profiles.get('document_type_profiles', {}))
        
        if profile_count == 0:
            profile_lines = 0
            table_lines = available_lines
        else:
            # Allocate 60% to profiles, 40% to tables
            profile_lines = int(available_lines * 0.6)
            table_lines = available_lines - profile_lines
        
        allocation = {
            'header': header_lines,
            'profile': profile_lines // max(profile_count, 1),  # Per profile
            'tables': table_lines,
            'footer': footer_lines,
            'total_available': available_lines,
            'target_total': target_line_limit
        }
        
        self.logger.info(f"Space allocation: {allocation}")
        return allocation
    
    def _generate_header_section(self, allocated_lines: int) -> str:
        """Step 2: Generate header section."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        header = f"""---
title: "Frontmatter Schema Validation Profiles"
info-type: technical-reference
version: "2.0.0"
date-modified: "{timestamp}"
auto-generated: true
source: "SHACL shapes analysis"
---

# Frontmatter Schema Validation Profiles

**Auto-Generated Documentation**  
**Generated:** {timestamp}  
**Source:** SHACL shapes analysis from `standards/registry/shacl-shapes.ttl`

This document defines validation profiles for frontmatter schema compliance across different document types.

"""
        return header
    
    def _generate_profile_section(self, profile_name: str, profile_data: Dict[str, Any], 
                                allocated_lines: int) -> str:
        """Step 3: Generate profile sections with space constraints."""
        # Clean profile name for display
        display_name = profile_name.replace('-', ' ').title()
        
        section = f"## {display_name}\n\n"
        
        # Add inheritance information if available
        extends = profile_data.get('extends')
        if extends:
            section += f"**Extends:** {extends}\n\n"
        
        # Calculate line budget for subsections
        used_lines = self._count_lines(section)
        remaining_lines = allocated_lines - used_lines - 2  # Reserve 2 lines for spacing
        
        if remaining_lines <= 0:
            section += "*Profile details truncated due to space constraints.*\n\n"
            return section
        
        # Add required fields (highest priority)
        mandatory_fields = profile_data.get('mandatory_fields', [])
        if mandatory_fields and remaining_lines > 3:
            section += "**Required Fields:** "
            
            # Fit as many fields as possible in remaining space
            field_text = ", ".join(f"`{field}`" for field in mandatory_fields[:10])  # Limit to 10 fields
            if len(mandatory_fields) > 10:
                field_text += f" (+{len(mandatory_fields) - 10} more)"
            
            section += field_text + "\n\n"
            used_lines += 2
            remaining_lines -= 2
        
        # Add forbidden fields if space permits
        forbidden_fields = profile_data.get('forbidden_fields', [])
        if forbidden_fields and remaining_lines > 3:
            section += "**Forbidden:** "
            field_text = ", ".join(f"`{field}`" for field in forbidden_fields[:5])  # Limit to 5 fields
            if len(forbidden_fields) > 5:
                field_text += f" (+{len(forbidden_fields) - 5} more)"
            
            section += field_text + "\n\n"
            used_lines += 2
            remaining_lines -= 2
        
        # Add complexity info if space permits
        complexity_metrics = profile_data.get('complexity_metrics', {})
        if complexity_metrics and remaining_lines > 2:
            complexity_score = complexity_metrics.get('complexity_score', 0)
            section += f"**Complexity:** {complexity_score} constraints\n\n"
        
        return section
    
    def _generate_field_tables(self, allocated_lines: int) -> str:
        """Step 4: Generate field reference tables."""
        tables = "## Field Reference\n\n"
        
        # Collect all unique fields across profiles
        all_mandatory = set()
        all_forbidden = set()
        
        for profile_data in self.profiles.get('document_type_profiles', {}).values():
            all_mandatory.update(profile_data.get('mandatory_fields', []))
            all_forbidden.update(profile_data.get('forbidden_fields', []))
        
        # Calculate space for each table
        available_lines = allocated_lines - 4  # Header + spacing
        table_lines_each = available_lines // 2
        
        # Generate mandatory fields table
        if all_mandatory and table_lines_each > 3:
            tables += "### Universal Mandatory Fields\n\n"
            tables += "| Field | Required For |\n"
            tables += "|-------|-------------|\n"
            
            # Limit fields to fit in allocated space
            field_limit = table_lines_each - 3  # Header rows
            mandatory_list = sorted(list(all_mandatory))[:field_limit]
            
            for field in mandatory_list:
                # Find which profiles require this field
                requiring_profiles = []
                for profile_name, profile_data in self.profiles.get('document_type_profiles', {}).items():
                    if field in profile_data.get('mandatory_fields', []):
                        requiring_profiles.append(profile_name)
                
                profile_text = ", ".join(requiring_profiles[:3])  # Limit to 3 profiles
                if len(requiring_profiles) > 3:
                    profile_text += f" (+{len(requiring_profiles) - 3})"
                
                tables += f"| `{field}` | {profile_text} |\n"
            
            if len(all_mandatory) > field_limit:
                tables += f"| ... | *+{len(all_mandatory) - field_limit} more fields* |\n"
            
            tables += "\n"
        
        # Generate forbidden fields summary if space permits
        remaining_lines = allocated_lines - self._count_lines(tables)
        if all_forbidden and remaining_lines > 5:
            tables += "### Commonly Forbidden Fields\n\n"
            forbidden_list = sorted(list(all_forbidden))[:remaining_lines - 3]
            tables += "Fields that are forbidden in certain document types: "
            tables += ", ".join(f"`{field}`" for field in forbidden_list)
            if len(all_forbidden) > len(forbidden_list):
                tables += f" (+{len(all_forbidden) - len(forbidden_list)} more)"
            tables += "\n\n"
        
        return tables
    
    def _generate_footer_section(self) -> str:
        """Step 5: Generate footer with auto-generation notice."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        footer = f"""---

## Auto-Generation Notice

**⚠️ This document is automatically generated from SHACL shapes.**

- **Source:** `standards/registry/shacl-shapes.ttl`
- **Generated:** {timestamp}
- **Generator:** `tools/builder/markdown_template_generator.py`

**Do not edit this file manually.** Changes will be overwritten on next generation.
To modify validation rules, update the SHACL shapes file and regenerate this documentation.
"""
        
        return footer
    
    def _assemble_document(self, header: str, profile_sections: List[str], 
                          field_tables: str, footer: str) -> str:
        """Step 6: Assemble final document."""
        document_parts = [header]
        
        # Add profile sections
        for section in profile_sections:
            document_parts.append(section)
        
        # Add field tables
        document_parts.append(field_tables)
        
        # Add footer
        document_parts.append(footer)
        
        return "".join(document_parts)
    
    def _optimize_for_line_limit(self, document: str, target_line_limit: int) -> str:
        """Step 7: Optimize document to fit within line limit."""
        current_lines = self._count_lines(document)
        lines_to_remove = current_lines - target_line_limit
        
        if lines_to_remove <= 0:
            return document
        
        self.logger.info(f"Optimizing document: need to remove {lines_to_remove} lines")
        
        # Split document into sections
        sections = document.split('\n## ')
        header = sections[0]
        content_sections = sections[1:] if len(sections) > 1 else []
        
        # Optimization strategies (in order of preference)
        optimized_sections = []
        
        for section in content_sections:
            section_content = '## ' + section if not section.startswith('##') else section
            
            # Strategy 1: Truncate field lists
            section_content = self._truncate_field_lists(section_content)
            
            # Strategy 2: Remove less critical information
            section_content = self._remove_less_critical_info(section_content)
            
            optimized_sections.append(section_content)
        
        # Reassemble document
        optimized_document = header
        for section in optimized_sections:
            if not section.startswith('## '):
                optimized_document += '\n## '
            optimized_document += section.lstrip('## ')
        
        # If still too long, truncate from the end
        if self._count_lines(optimized_document) > target_line_limit:
            lines = optimized_document.split('\n')
            truncated_lines = lines[:target_line_limit - 2]  # Reserve 2 lines for truncation notice
            truncated_lines.append("")
            truncated_lines.append("*[Documentation truncated to meet line limit]*")
            optimized_document = '\n'.join(truncated_lines)
        
        return optimized_document
    
    def _truncate_field_lists(self, section_content: str) -> str:
        """Optimization: Truncate long field lists."""
        # Truncate field lists that are too long
        field_pattern = r'(\*\*[^:]+:\*\*\s*)([^*\n]+)'
        
        def truncate_match(match):
            label = match.group(1)
            field_list = match.group(2)
            
            # If field list is very long, truncate it
            if len(field_list) > 150:  # Arbitrary threshold
                truncated = field_list[:120] + "..."
                return label + truncated
            return match.group(0)
        
        return re.sub(field_pattern, truncate_match, section_content)
    
    def _remove_less_critical_info(self, section_content: str) -> str:
        """Optimization: Remove less critical information."""
        # Remove complexity scores if present
        section_content = re.sub(r'\*\*Complexity:\*\*[^\n]*\n\n', '', section_content)
        
        # Remove empty lines
        section_content = re.sub(r'\n\s*\n\s*\n', '\n\n', section_content)
        
        return section_content
    
    def _count_lines(self, text: str) -> int:
        """Count lines in text, with caching for performance."""
        text_hash = hash(text)
        if text_hash in self._line_count_cache:
            return self._line_count_cache[text_hash]
        
        line_count = len(text.split('\n'))
        self._line_count_cache[text_hash] = line_count
        return line_count
    
    def _load_header_template(self) -> str:
        """Load header template."""
        return """---
title: "{title}"
info-type: technical-reference
version: "{version}"
date-modified: "{timestamp}"
auto-generated: true
source: "SHACL shapes analysis"
---

# {title}

**Auto-Generated Documentation**  
**Generated:** {timestamp}  
**Source:** SHACL shapes analysis

{description}
"""
    
    def _load_profile_template(self) -> str:
        """Load profile section template."""
        return """## {profile_name}

{inheritance_info}

**Required Fields:** {mandatory_fields}
{forbidden_info}
{complexity_info}
"""
    
    def _load_field_table_template(self) -> str:
        """Load field table template."""
        return """## Field Reference

### {table_title}

| Field | {column_header} |
|-------|{column_separator}|
{table_rows}
"""
    
    def _load_footer_template(self) -> str:
        """Load footer template."""
        return """---

## Auto-Generation Notice

**⚠️ This document is automatically generated from SHACL shapes.**

- **Source:** `{source_file}`
- **Generated:** {timestamp}
- **Generator:** `{generator_script}`

**Do not edit this file manually.** Changes will be overwritten on next generation.
"""
    
    def generate_profile_specific_docs(self, profile_name: str) -> str:
        """Generate documentation for a specific profile."""
        profile_data = self.profiles.get('document_type_profiles', {}).get(profile_name)
        
        if not profile_data:
            return f"# Profile Not Found: {profile_name}\n\nThe requested profile was not found in the SHACL shapes."
        
        # Generate detailed documentation for single profile
        doc = f"# {profile_name.replace('-', ' ').title()} Profile\n\n"
        
        # Add inheritance info
        extends = profile_data.get('extends')
        if extends:
            doc += f"**Extends:** {extends}\n\n"
        
        # Add all mandatory fields
        mandatory_fields = profile_data.get('mandatory_fields', [])
        if mandatory_fields:
            doc += "## Required Fields\n\n"
            for field in mandatory_fields:
                doc += f"- `{field}`\n"
            doc += "\n"
        
        # Add forbidden fields
        forbidden_fields = profile_data.get('forbidden_fields', [])
        if forbidden_fields:
            doc += "## Forbidden Fields\n\n"
            for field in forbidden_fields:
                doc += f"- `{field}`\n"
            doc += "\n"
        
        # Add pattern constraints
        pattern_constraints = profile_data.get('pattern_constraints', {})
        if pattern_constraints:
            doc += "## Pattern Constraints\n\n"
            for field, constraint in pattern_constraints.items():
                pattern = constraint.get('pattern', 'N/A')
                doc += f"- `{field}`: `{pattern}`\n"
            doc += "\n"
        
        return doc
    
    def get_generation_stats(self, generated_doc: str) -> Dict[str, Any]:
        """Get statistics about the generated documentation."""
        lines = generated_doc.split('\n')
        
        stats = {
            'total_lines': len(lines),
            'total_characters': len(generated_doc),
            'total_words': len(generated_doc.split()),
            'sections': {
                'profiles': len(self.profiles.get('document_type_profiles', {})),
                'base_profiles': len(self.profiles.get('base_profiles', [])),
                'specializations': sum(len(specs) for specs in self.profiles.get('specialization_profiles', {}).values())
            },
            'field_counts': self._analyze_field_distribution(),
            'optimization_applied': 'truncated' in generated_doc.lower()
        }
        
        return stats
    
    def _analyze_field_distribution(self) -> Dict[str, int]:
        """Analyze field distribution across profiles."""
        all_mandatory = set()
        all_forbidden = set()
        all_patterns = set()
        
        for profile_data in self.profiles.get('document_type_profiles', {}).values():
            all_mandatory.update(profile_data.get('mandatory_fields', []))
            all_forbidden.update(profile_data.get('forbidden_fields', []))
            all_patterns.update(profile_data.get('pattern_constraints', {}).keys())
        
        return {
            'unique_mandatory_fields': len(all_mandatory),
            'unique_forbidden_fields': len(all_forbidden), 
            'unique_pattern_fields': len(all_patterns),
            'total_unique_fields': len(all_mandatory | all_forbidden | all_patterns)
        }


if __name__ == "__main__":
    # Example usage for testing
    from shacl_parser import SHACLParser
    from profile_categorizer import ProfileCategorizer
    
    parser = SHACLParser('standards/registry/shacl-shapes.ttl')
    rules = parser.extract_validation_rules()
    
    categorizer = ProfileCategorizer()
    hierarchy = categorizer.categorize_profiles(rules)
    
    generator = MarkdownTemplateGenerator(hierarchy)
    documentation = generator.generate_concise_documentation(target_line_limit=180)
    
    print("Generated Documentation:")
    print("=" * 60)
    print(documentation)
    
    stats = generator.get_generation_stats(documentation)
    print(f"\nGeneration Stats: {stats}")