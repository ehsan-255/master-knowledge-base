#!/usr/bin/env python3
"""
Schema Constraint Prompt Engineering

Implementation of Phase 3: Step 3.1.2 - Schema Constraint Prompt Engineering
From: ultimate-frontmatter-enhancement-guideline-20250617-0312.md

This module provides sophisticated prompt engineering for LLM frontmatter generation
with SHACL constraint awareness and validation loop integration.
"""

import re
import yaml
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SchemaConstraintPromptEngine:
    """
    Schema Constraint Prompt Engine for LLM frontmatter generation.
    
    Provides sophisticated prompt engineering that converts SHACL constraints
    into detailed LLM instructions for accurate frontmatter generation.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # Prompt templates for different constraint types
        self.constraint_templates = self._initialize_constraint_templates()
        
        # Field type mappings for better generation
        self.field_type_mappings = self._initialize_field_type_mappings()
        
        # Common validation patterns
        self.validation_patterns = self._initialize_validation_patterns()
    
    def build_schema_constrained_prompt(self, document_content: str, info_type: str, 
                                      constraints: Dict[str, Any]) -> str:
        """
        Step 2: Build LLM prompts with SHACL constraints.
        
        Args:
            document_content: The content of the document
            info_type: Target info-type for the document
            constraints: SHACL constraints dictionary
            
        Returns:
            Comprehensive prompt for LLM generation
        """
        self.logger.info(f"Building schema-constrained prompt for {info_type}")
        
        # Sub-step 2.1: Analyze document content for context
        content_analysis = self._analyze_document_content(document_content)
        
        # Sub-step 2.2: Extract mandatory fields for info-type
        mandatory_fields = constraints.get('mandatory_fields', [])
        
        # Sub-step 2.3: Extract forbidden fields for info-type
        forbidden_fields = constraints.get('forbidden_fields', [])
        
        # Sub-step 2.4: Build constraint instructions
        constraint_instructions = self._build_constraint_instructions(
            mandatory_fields, forbidden_fields, constraints
        )
        
        # Sub-step 2.5: Create context-aware prompt
        prompt = self._create_context_aware_prompt(
            content_analysis, info_type, constraint_instructions
        )
        
        return prompt
    
    def _analyze_document_content(self, document_content: str) -> Dict[str, Any]:
        """Sub-step 2.1: Analyze document content for context."""
        analysis = {
            'length': len(document_content),
            'word_count': len(document_content.split()),
            'has_headings': self._detect_headings(document_content),
            'heading_structure': self._extract_heading_structure(document_content),
            'content_type_indicators': self._detect_content_type_indicators(document_content),
            'language_complexity': self._assess_language_complexity(document_content),
            'technical_terms': self._extract_technical_terms(document_content),
            'document_purpose': self._infer_document_purpose(document_content),
            'suggested_title': self._suggest_title_from_content(document_content)
        }
        
        return analysis
    
    def _detect_headings(self, content: str) -> Dict[str, Any]:
        """Detect heading structure in the document."""
        heading_pattern = r'^(#{1,6})\s+(.+)$'
        headings = []
        
        for line in content.split('\n'):
            match = re.match(heading_pattern, line.strip())
            if match:
                level = len(match.group(1))
                text = match.group(2).strip()
                headings.append({
                    'level': level,
                    'text': text,
                    'line': line.strip()
                })
        
        return {
            'count': len(headings),
            'max_level': max([h['level'] for h in headings], default=0),
            'headings': headings,
            'main_heading': headings[0]['text'] if headings and headings[0]['level'] == 1 else None
        }
    
    def _extract_heading_structure(self, content: str) -> List[str]:
        """Extract heading structure for title suggestion."""
        heading_info = self._detect_headings(content)
        return [h['text'] for h in heading_info['headings']]
    
    def _detect_content_type_indicators(self, content: str) -> Dict[str, bool]:
        """Detect indicators of different content types."""
        content_lower = content.lower()
        
        indicators = {
            'has_standards_language': any(term in content_lower for term in [
                'standard', 'compliance', 'requirement', 'specification', 'shall', 'must'
            ]),
            'has_policy_language': any(term in content_lower for term in [
                'policy', 'procedure', 'governance', 'mandate', 'directive'
            ]),
            'has_technical_language': any(term in content_lower for term in [
                'implementation', 'architecture', 'system', 'algorithm', 'protocol'
            ]),
            'has_analysis_language': any(term in content_lower for term in [
                'analysis', 'report', 'findings', 'conclusion', 'recommendation'
            ]),
            'has_guide_language': any(term in content_lower for term in [
                'guide', 'tutorial', 'how to', 'step', 'example', 'instructions'
            ]),
            'has_code_examples': '```' in content,
            'has_diagrams': any(term in content_lower for term in [
                'diagram', 'figure', 'chart', 'graph'
            ]),
            'has_references': any(term in content_lower for term in [
                'reference', 'bibliography', 'citation', 'see also'
            ])
        }
        
        return indicators
    
    def _assess_language_complexity(self, content: str) -> Dict[str, Any]:
        """Assess the complexity of language used in the document."""
        words = content.split()
        sentences = re.split(r'[.!?]+', content)
        
        # Calculate metrics
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        avg_sentence_length = sum(len(sentence.split()) for sentence in sentences) / len(sentences) if sentences else 0
        
        # Detect technical terminology density
        technical_indicators = len(re.findall(r'\b[A-Z]{2,}\b', content))  # Acronyms
        code_blocks = len(re.findall(r'```[\s\S]*?```', content))
        
        complexity_score = (avg_word_length * 0.3 + avg_sentence_length * 0.4 + 
                          technical_indicators * 0.2 + code_blocks * 0.1)
        
        return {
            'average_word_length': avg_word_length,
            'average_sentence_length': avg_sentence_length,
            'technical_indicators': technical_indicators,
            'code_blocks': code_blocks,
            'complexity_score': complexity_score,
            'complexity_level': 'high' if complexity_score > 15 else 'medium' if complexity_score > 8 else 'low'
        }
    
    def _extract_technical_terms(self, content: str) -> List[str]:
        """Extract technical terms from the document."""
        # Extract acronyms and technical terms
        acronyms = re.findall(r'\b[A-Z]{2,}\b', content)
        
        # Extract terms in code blocks or backticks
        code_terms = re.findall(r'`([^`]+)`', content)
        
        # Extract capitalized terms (potential proper nouns/technical terms)
        capitalized_terms = re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b', content)
        
        all_terms = list(set(acronyms + code_terms + capitalized_terms))
        return all_terms[:10]  # Limit to most significant terms
    
    def _infer_document_purpose(self, content: str) -> str:
        """Infer the primary purpose of the document."""
        content_lower = content.lower()
        
        purpose_indicators = {
            'specification': ['specification', 'spec', 'requirement', 'standard definition'],
            'guidance': ['guide', 'tutorial', 'how to', 'instruction', 'example'],
            'analysis': ['analysis', 'report', 'study', 'evaluation', 'assessment'],
            'policy': ['policy', 'procedure', 'governance', 'rule', 'regulation'],
            'documentation': ['documentation', 'manual', 'reference', 'api'],
            'reference': ['reference', 'glossary', 'index', 'catalog', 'directory']
        }
        
        purpose_scores = {}
        for purpose, indicators in purpose_indicators.items():
            score = sum(content_lower.count(indicator) for indicator in indicators)
            purpose_scores[purpose] = score
        
        if purpose_scores:
            primary_purpose = max(purpose_scores, key=purpose_scores.get)
            if purpose_scores[primary_purpose] > 0:
                return primary_purpose
        
        return 'general'
    
    def _suggest_title_from_content(self, content: str) -> str:
        """Suggest a title based on document content."""
        heading_info = self._detect_headings(content)
        
        # Use main heading if available
        if heading_info['main_heading']:
            return heading_info['main_heading']
        
        # Use first heading if available
        if heading_info['headings']:
            return heading_info['headings'][0]['text']
        
        # Extract first meaningful sentence
        sentences = re.split(r'[.!?]+', content)
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10 and len(sentence) < 100:
                return sentence
        
        return "Auto-Generated Document Title"
    
    def _build_constraint_instructions(self, mandatory_fields: List[str], 
                                     forbidden_fields: List[str], 
                                     constraints: Dict[str, Any]) -> Dict[str, Any]:
        """Sub-step 2.4: Build comprehensive constraint instructions."""
        instructions = {
            'mandatory_section': self._format_mandatory_fields(mandatory_fields, constraints),
            'forbidden_section': self._format_forbidden_fields(forbidden_fields),
            'pattern_section': self._format_pattern_constraints(constraints.get('pattern_constraints', {})),
            'value_section': self._format_value_constraints(constraints.get('value_constraints', {})),
            'datatype_section': self._format_datatype_constraints(constraints.get('datatype_constraints', {})),
            'validation_section': self._format_validation_rules(constraints),
            'examples_section': self._generate_constraint_examples(constraints)
        }
        
        return instructions
    
    def _format_mandatory_fields(self, mandatory_fields: List[str], 
                                constraints: Dict[str, Any]) -> str:
        """Format mandatory fields with detailed instructions."""
        if not mandatory_fields:
            return "No mandatory fields specified."
        
        field_instructions = []
        field_instructions.append("MANDATORY FIELDS (must be included):")
        
        for field in mandatory_fields:
            field_info = self._get_field_generation_info(field, constraints)
            field_instructions.append(f"- {field}: {field_info}")
        
        return "\n".join(field_instructions)
    
    def _get_field_generation_info(self, field: str, constraints: Dict[str, Any]) -> str:
        """Get detailed generation information for a specific field."""
        # Check for value constraints
        value_constraints = constraints.get('value_constraints', {})
        if field in value_constraints:
            return f"MUST be exactly '{value_constraints[field]}'"
        
        # Check for pattern constraints
        pattern_constraints = constraints.get('pattern_constraints', {})
        if field in pattern_constraints:
            pattern = pattern_constraints[field]
            return f"Must match pattern '{pattern}' - {self._explain_pattern(field, pattern)}"
        
        # Check for datatype constraints
        datatype_constraints = constraints.get('datatype_constraints', {})
        if field in datatype_constraints:
            datatype = datatype_constraints[field]
            return f"Must be of type {datatype} - {self._explain_datatype(field, datatype)}"
        
        # Use field-specific guidance
        return self._get_field_specific_guidance(field)
    
    def _explain_pattern(self, field: str, pattern: str) -> str:
        """Explain what a pattern constraint means."""
        pattern_explanations = {
            r'^[A-Z]{2}-[A-Z]{2,6}-[A-Z0-9\-]+$': 'Format: XX-YYYYY-ZZZZZ (e.g., ST-POLICY-EXAMPLE-001)',
            r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$': 'ISO 8601 date format (e.g., 2023-12-01T10:30:00Z)',
            r'^P[0-4]-[A-Za-z\-]+$': 'Priority format P0-P4 followed by description (e.g., P1-Important)',
            r'^[A-Za-z\-]+$': 'Alphabetic text with hyphens allowed'
        }
        
        for regex, explanation in pattern_explanations.items():
            if pattern == regex:
                return explanation
        
        return f"Custom pattern: {pattern}"
    
    def _explain_datatype(self, field: str, datatype: str) -> str:
        """Explain what a datatype constraint means."""
        datatype_explanations = {
            'xsd:string': 'Text string',
            'xsd:dateTime': 'ISO 8601 date-time format',
            'xsd:date': 'ISO 8601 date format',
            'xsd:integer': 'Whole number',
            'xsd:boolean': 'true or false',
            'xsd:decimal': 'Decimal number'
        }
        
        return datatype_explanations.get(datatype, f'Type: {datatype}')
    
    def _get_field_specific_guidance(self, field: str) -> str:
        """Get field-specific generation guidance."""
        field_guidance = {
            'title': 'Descriptive title based on document content',
            'version': 'Semantic version (e.g., 1.0.0)',
            'date-created': 'Current timestamp in ISO 8601 format',
            'date-modified': 'Current timestamp in ISO 8601 format',
            'kb-id': 'Unique knowledge base identifier',
            'info-type': 'Document type classification',
            'standard_id': 'Standard identifier following repository pattern',
            'criticality': 'Priority level (P0-Critical, P1-Important, P2-Standard, P3-Low)',
            'lifecycle_gatekeeper': 'Review authority (Technical-Review, Architect-Review, etc.)',
            'tags': 'List of relevant classification tags',
            'scope_application': 'Scope of application for this document',
            'primary_topic': 'Primary topic or keyword for this document'
        }
        
        return field_guidance.get(field, 'Appropriate value for this field')
    
    def _format_forbidden_fields(self, forbidden_fields: List[str]) -> str:
        """Format forbidden fields instructions."""
        if not forbidden_fields:
            return "No forbidden fields specified."
        
        instructions = ["FORBIDDEN FIELDS (must NOT be included):"]
        for field in forbidden_fields:
            instructions.append(f"- {field}")
        
        return "\n".join(instructions)
    
    def _format_pattern_constraints(self, pattern_constraints: Dict[str, str]) -> str:
        """Format pattern constraint instructions."""
        if not pattern_constraints:
            return ""
        
        instructions = ["PATTERN CONSTRAINTS:"]
        for field, pattern in pattern_constraints.items():
            explanation = self._explain_pattern(field, pattern)
            instructions.append(f"- {field}: {explanation}")
        
        return "\n".join(instructions)
    
    def _format_value_constraints(self, value_constraints: Dict[str, str]) -> str:
        """Format value constraint instructions."""
        if not value_constraints:
            return ""
        
        instructions = ["VALUE CONSTRAINTS:"]
        for field, value in value_constraints.items():
            instructions.append(f"- {field}: MUST be exactly '{value}'")
        
        return "\n".join(instructions)
    
    def _format_datatype_constraints(self, datatype_constraints: Dict[str, str]) -> str:
        """Format datatype constraint instructions."""
        if not datatype_constraints:
            return ""
        
        instructions = ["DATATYPE CONSTRAINTS:"]
        for field, datatype in datatype_constraints.items():
            explanation = self._explain_datatype(field, datatype)
            instructions.append(f"- {field}: {explanation}")
        
        return "\n".join(instructions)
    
    def _format_validation_rules(self, constraints: Dict[str, Any]) -> str:
        """Format general validation rules."""
        rules = [
            "VALIDATION REQUIREMENTS:",
            "- Generate ONLY valid YAML frontmatter",
            "- Use proper YAML syntax with correct indentation",
            "- Use double quotes for string values when they contain special characters",
            "- Use ISO 8601 format for all date and datetime values",
            "- Ensure all mandatory fields are present with appropriate values",
            "- Do not include any forbidden fields",
            "- Follow all pattern and value constraints exactly"
        ]
        
        return "\n".join(rules)
    
    def _generate_constraint_examples(self, constraints: Dict[str, Any]) -> str:
        """Generate examples based on constraints."""
        examples = ["EXAMPLES:"]
        
        # Generate example for mandatory fields
        mandatory_fields = constraints.get('mandatory_fields', [])
        if mandatory_fields:
            example_frontmatter = {}
            
            for field in mandatory_fields:
                example_value = self._generate_example_value(field, constraints)
                example_frontmatter[field] = example_value
            
            examples.append("Example frontmatter structure:")
            examples.append("```yaml")
            examples.append(yaml.dump(example_frontmatter, default_flow_style=False))
            examples.append("```")
        
        return "\n".join(examples)
    
    def _generate_example_value(self, field: str, constraints: Dict[str, Any]) -> str:
        """Generate an example value for a field."""
        # Check value constraints first
        value_constraints = constraints.get('value_constraints', {})
        if field in value_constraints:
            return value_constraints[field]
        
        # Generate field-specific examples
        field_examples = {
            'title': 'Example Document Title',
            'version': '1.0.0',
            'date-created': '2023-12-01T10:30:00Z',
            'date-modified': '2023-12-01T10:30:00Z',
            'kb-id': 'DOC-EXAMPLE-20231201-1030',
            'info-type': 'general-document',
            'standard_id': 'ST-EXAMPLE-001',
            'criticality': 'P2-Standard',
            'lifecycle_gatekeeper': 'Technical-Review',
            'tags': ['example', 'documentation'],
            'scope_application': 'repository',
            'primary_topic': 'example-content'
        }
        
        return field_examples.get(field, 'example-value')
    
    def _create_context_aware_prompt(self, content_analysis: Dict[str, Any], 
                                   info_type: str, 
                                   constraint_instructions: Dict[str, Any]) -> str:
        """Sub-step 2.5: Create comprehensive context-aware prompt."""
        prompt_sections = []
        
        # Header section
        prompt_sections.append("CRITICAL: Generate YAML frontmatter that MUST pass SHACL validation")
        prompt_sections.append(f"TARGET INFO-TYPE: {info_type}")
        prompt_sections.append("")
        
        # Document context section
        prompt_sections.append("DOCUMENT CONTENT ANALYSIS:")
        prompt_sections.append(f"- Length: {content_analysis['length']} characters")
        prompt_sections.append(f"- Word count: {content_analysis['word_count']}")
        prompt_sections.append(f"- Complexity: {content_analysis['language_complexity']['complexity_level']}")
        prompt_sections.append(f"- Purpose: {content_analysis['document_purpose']}")
        prompt_sections.append(f"- Suggested title: {content_analysis['suggested_title']}")
        
        if content_analysis['technical_terms']:
            prompt_sections.append(f"- Technical terms: {', '.join(content_analysis['technical_terms'][:5])}")
        
        prompt_sections.append("")
        
        # Constraint sections
        for section_name, section_content in constraint_instructions.items():
            if section_content and section_content.strip():
                prompt_sections.append(section_content)
                prompt_sections.append("")
        
        # Output requirements
        prompt_sections.append("OUTPUT REQUIREMENTS:")
        prompt_sections.append("- Generate ONLY the YAML frontmatter block")
        prompt_sections.append("- Start with --- and end with ---")
        prompt_sections.append("- Use proper YAML syntax")
        prompt_sections.append("- Include ALL mandatory fields")
        prompt_sections.append("- Exclude ALL forbidden fields")
        prompt_sections.append("- Follow ALL pattern and value constraints")
        prompt_sections.append("")
        prompt_sections.append("Generate the frontmatter now:")
        
        return "\n".join(prompt_sections)
    
    def _initialize_constraint_templates(self) -> Dict[str, str]:
        """Initialize constraint templates for different scenarios."""
        return {
            'mandatory_field': "- {field}: {guidance}",
            'forbidden_field': "- {field} (MUST NOT be present)",
            'pattern_constraint': "- {field}: Must match pattern '{pattern}' - {explanation}",
            'value_constraint': "- {field}: MUST be exactly '{value}'",
            'datatype_constraint': "- {field}: Must be {datatype} - {explanation}"
        }
    
    def _initialize_field_type_mappings(self) -> Dict[str, str]:
        """Initialize field type mappings for better generation."""
        return {
            'date-created': 'datetime',
            'date-modified': 'datetime',
            'version': 'version',
            'kb-id': 'identifier',
            'standard_id': 'identifier',
            'title': 'title',
            'tags': 'list',
            'criticality': 'enum',
            'lifecycle_gatekeeper': 'enum'
        }
    
    def _initialize_validation_patterns(self) -> Dict[str, str]:
        """Initialize common validation patterns."""
        return {
            'iso_datetime': r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$',
            'semantic_version': r'^\d+\.\d+\.\d+$',
            'standard_id': r'^[A-Z]{2}-[A-Z]{2,6}-[A-Z0-9\-]+$',
            'kb_id': r'^[A-Z0-9\-]+$',
            'criticality': r'^P[0-4]-[A-Za-z\-]+$'
        }
    
    def enhance_prompt_with_feedback(self, original_prompt: str, 
                                   validation_errors: List[Dict[str, Any]]) -> str:
        """Enhance prompt with validation feedback for retry attempts."""
        feedback_sections = [
            original_prompt,
            "",
            "VALIDATION ERRORS DETECTED - Please correct:",
        ]
        
        for error in validation_errors:
            error_type = error.get('type', 'unknown')
            field = error.get('field', 'unknown')
            message = error.get('message', 'Unknown error')
            
            if error_type == 'missing_required_field':
                feedback_sections.append(f"❌ MISSING: {field} - {message}")
            elif error_type == 'forbidden_field_present':
                feedback_sections.append(f"❌ FORBIDDEN: {field} - {message}")
            elif error_type == 'incorrect_value':
                expected = error.get('expected', 'N/A')
                actual = error.get('actual', 'N/A')
                feedback_sections.append(f"❌ WRONG VALUE: {field} - Expected '{expected}', got '{actual}'")
            else:
                feedback_sections.append(f"❌ ERROR: {field} - {message}")
        
        feedback_sections.extend([
            "",
            "Please generate corrected YAML frontmatter that addresses ALL the above errors:",
        ])
        
        return "\n".join(feedback_sections)
    
    def get_prompt_statistics(self, prompt: str) -> Dict[str, Any]:
        """Get statistics about the generated prompt."""
        return {
            'total_length': len(prompt),
            'word_count': len(prompt.split()),
            'line_count': len(prompt.split('\n')),
            'section_count': prompt.count(':'),
            'constraint_count': prompt.count('MUST'),
            'example_count': prompt.count('```'),
            'estimated_tokens': len(prompt.split()) * 1.3  # Rough token estimation
        }


if __name__ == "__main__":
    # Example usage for testing
    engine = SchemaConstraintPromptEngine()
    
    # Test document content
    test_content = """# Example Standard Document
    
    This document defines the standard for example processes.
    
    ## Requirements
    
    The following requirements must be met:
    - Compliance with regulations
    - Implementation of best practices
    """
    
    # Test constraints
    test_constraints = {
        'mandatory_fields': ['title', 'standard_id', 'version', 'criticality'],
        'forbidden_fields': ['draft_status'],
        'pattern_constraints': {
            'standard_id': '^ST-[A-Z]+-[0-9]+$'
        },
        'value_constraints': {
            'info-type': 'standard-definition'
        }
    }
    
    # Generate prompt
    prompt = engine.build_schema_constrained_prompt(
        test_content, 'standard-definition', test_constraints
    )
    
    print("Generated Prompt:")
    print("=" * 60)
    print(prompt)
    
    # Get statistics
    stats = engine.get_prompt_statistics(prompt)
    print(f"\nPrompt Statistics: {stats}")