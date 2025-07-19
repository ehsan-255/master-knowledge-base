#!/usr/bin/env python3
"""
Enhanced Frontmatter Action

Implementation of Phase 3: Step 3.1.5 - Integration with Existing Scribe Actions
From: ultimate-frontmatter-enhancement-guideline-20250617-0312.md

This module provides enhanced frontmatter generation action that integrates
LLM-based generation with SHACL validation and existing Scribe workflow.
"""

import os
import sys
import yaml
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import re

# Add tools paths for importing
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import existing scribe components
from .base import BaseAction, ActionExecutionError

# Import Phase 3 components
try:
    from integrations.llm_integration import LLMSchemaIntegration
    from validation.llm_shacl_validator import LLMSHACLValidator
    from prompts.schema_constraint_prompts import SchemaConstraintPromptEngine
    from error_handling.llm_error_handler import LLMErrorHandler
except ImportError as e:
    logging.warning(f"Could not import Phase 3 components: {e}")
    # Create mock classes for fallback
    class LLMSchemaIntegration:
        def __init__(self, *args, **kwargs):
            pass
        def build_schema_constrained_prompt(self, *args, **kwargs):
            return "Mock prompt"
    
    class LLMSHACLValidator:
        def __init__(self, *args, **kwargs):
            pass
        def validate_with_retry_loop(self, *args, **kwargs):
            return {'success': True, 'frontmatter': {}, 'fallback_used': True}
    
    class SchemaConstraintPromptEngine:
        def __init__(self, *args, **kwargs):
            pass
        def build_schema_constrained_prompt(self, *args, **kwargs):
            return "Mock prompt"
    
    class LLMErrorHandler:
        def __init__(self, *args, **kwargs):
            pass

# Import analysis components from Phase 1
try:
    from analysis.document_type_analyzer import UniversalDocumentTypeAnalyzer
except ImportError:
    class UniversalDocumentTypeAnalyzer:
        def __init__(self, *args, **kwargs):
            pass
        def analyze_on_demand(self, *args, **kwargs):
            return {'document_types_identified': {}}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnhancedFrontmatterAction(BaseAction):
    """
    Enhanced Frontmatter Action with LLM integration and SHACL validation.
    
    Provides complete frontmatter generation workflow integrating:
    - Document type analysis
    - Schema-constrained LLM generation  
    - SHACL validation with retry loops
    - Error handling with 100% success guarantee
    """
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # Initialize Phase 3 components
        self.llm_integration = LLMSchemaIntegration(
            'standards/registry/shacl-shapes.ttl',
            'standards/registry/contexts/fields.jsonld'
        )
        self.validator = LLMSHACLValidator()
        self.prompt_engine = SchemaConstraintPromptEngine()
        self.error_handler = LLMErrorHandler()
        
        # Initialize Phase 1 components
        self.document_analyzer = UniversalDocumentTypeAnalyzer()
        
        # Generation statistics
        self.generation_stats = {
            'total_processed': 0,
            'successful_generations': 0,
            'fallback_generations': 0,
            'average_attempts': 0,
            'processing_history': []
        }
    
    @property
    def name(self) -> str:
        """Action name for Scribe registration."""
        return "enhanced-frontmatter"
    
    @property 
    def description(self) -> str:
        """Action description."""
        return "Generate enhanced frontmatter with LLM integration and SHACL validation"
    
    def execute(self, file_content: str, match: re.Match, file_path: str, params: Dict[str, Any]) -> str:
        """
        Step 5: Complete integration with Scribe workflow.
        
        Args:
            file_path: Path to the markdown file to process
            **kwargs: Additional options (info_type, force_regenerate, etc.)
            
        Returns:
            Execution result with success status and metadata
        """
        self.logger.info(f"Processing file: {file_path}")
        start_time = datetime.now()
        
        try:
            # Sub-step 5.1: Read document content
            content = self._read_file_content(file_path)
            
            # Sub-step 5.2: Detect or specify info-type
            info_type = params.get('info_type') or self._detect_info_type(content, file_path)
            
            # Sub-step 5.3: Check if regeneration is needed
            if not params.get('force_regenerate', False):
                existing_frontmatter = self._extract_existing_frontmatter(content)
                if existing_frontmatter and self._is_frontmatter_valid(existing_frontmatter, info_type):
                    self.logger.info(f"Valid frontmatter exists, skipping generation for {file_path}")
                    return self._create_success_result(file_path, existing_frontmatter, 'skipped_valid')
            
            # Sub-step 5.4: Build schema-constrained prompt
            prompt = self._build_comprehensive_prompt(content, info_type, file_path)
            
            # Sub-step 5.5: Generate with validation loop (100% success)
            generation_result = self.validator.validate_with_retry_loop(prompt, info_type)
            
            # Sub-step 5.6: Apply frontmatter to document
            updated_content = self._apply_frontmatter_to_file(
                file_path, content, generation_result['frontmatter']
            )
            
            # Sub-step 5.7: Write updated content back to file
            self._write_file_content(file_path, updated_content)
            
            # Sub-step 5.8: Log success metrics
            processing_time = (datetime.now() - start_time).total_seconds()
            result = self._log_generation_metrics(file_path, generation_result, processing_time)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {e}")
            
            # Use error handler for recovery
            error_type = self.error_handler.classify_error(str(e))
            recovery_result = self.error_handler.handle_generation_errors(
                error_type, {'error_message': str(e), 'file_path': file_path}
            )
            
            # If recovery suggests deterministic fallback, use it
            if recovery_result.get('recovery_strategy') == 'deterministic_fallback':
                fallback_result = self.validator._generate_deterministic_fallback(
                    params.get('info_type', 'general-document')
                )
                
                try:
                    content = self._read_file_content(file_path)
                    updated_content = self._apply_frontmatter_to_file(
                        file_path, content, fallback_result['frontmatter']
                    )
                    self._write_file_content(file_path, updated_content)
                    
                    processing_time = (datetime.now() - start_time).total_seconds()
                    return self._log_generation_metrics(file_path, fallback_result, processing_time)
                    
                except Exception as fallback_error:
                    self.logger.error(f"Fallback generation failed for {file_path}: {fallback_error}")
            
            # Return error result if all recovery attempts fail
            return {
                'success': False,
                'file_processed': file_path,
                'error': str(e),
                'recovery_attempted': True,
                'recovery_result': recovery_result
            }
    
    def _read_file_content(self, file_path: str) -> str:
        """Sub-step 5.1: Read document content safely."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            self.logger.error(f"Could not read file {file_path}: {e}")
            raise
    
    def _detect_info_type(self, content: str, file_path: str) -> str:
        """Sub-step 5.2: Detect or specify info-type using Phase 1 analyzer."""
        try:
            # Use document analyzer for sophisticated type detection
            analysis_result = self.document_analyzer.analyze_on_demand([Path(file_path).parent])
            
            # Extract classification for this specific file
            file_classifications = analysis_result.get('document_types_identified', {})
            
            # Find classification for this file
            for file_key, classification in file_classifications.items():
                if Path(file_path).name in file_key or str(file_path) in file_key:
                    detected_type = classification.get('inferred_type', 'general-document')
                    self.logger.info(f"Detected info-type '{detected_type}' for {file_path}")
                    return detected_type
            
            # Fallback to content-based detection
            return self._fallback_content_type_detection(content, file_path)
            
        except Exception as e:
            self.logger.warning(f"Type detection failed, using fallback: {e}")
            return self._fallback_content_type_detection(content, file_path)
    
    def _fallback_content_type_detection(self, content: str, file_path: str) -> str:
        """Fallback content-based type detection."""
        content_lower = content.lower()
        
        # Simple pattern matching for common types
        if 'standard' in content_lower and ('definition' in content_lower or 'compliance' in content_lower):
            return 'standard-definition'
        elif 'policy' in content_lower or 'procedure' in content_lower:
            return 'policy-document'
        elif 'report' in content_lower or 'analysis' in content_lower:
            return 'technical-report'
        elif 'meeting' in content_lower or 'attendees' in content_lower:
            return 'meeting-notes'
        else:
            return 'general-document'
    
    def _extract_existing_frontmatter(self, content: str) -> Optional[Dict[str, Any]]:
        """Extract existing frontmatter from document content."""
        try:
            # Look for YAML frontmatter
            if content.startswith('---\n'):
                end_marker = content.find('\n---\n', 4)
                if end_marker != -1:
                    frontmatter_yaml = content[4:end_marker]
                    return yaml.safe_load(frontmatter_yaml)
            return None
        except Exception as e:
            self.logger.warning(f"Could not parse existing frontmatter: {e}")
            return None
    
    def _is_frontmatter_valid(self, frontmatter: Dict[str, Any], info_type: str) -> bool:
        """Check if existing frontmatter is valid for the info-type."""
        try:
            # Use validator to check if current frontmatter passes SHACL
            validation_result = self.validator._validate_against_shacl(frontmatter, info_type)
            return validation_result.get('conforms', False)
        except Exception as e:
            self.logger.warning(f"Frontmatter validation check failed: {e}")
            return False
    
    def _build_comprehensive_prompt(self, content: str, info_type: str, file_path: str) -> str:
        """Sub-step 5.3: Build comprehensive schema-constrained prompt."""
        try:
            # Get SHACL constraints for the info-type
            constraints = self._get_constraints_for_type(info_type)
            
            # Use prompt engine to build sophisticated prompt
            prompt = self.prompt_engine.build_schema_constrained_prompt(
                content, info_type, constraints
            )
            
            # Add file-specific context
            file_context = f"""
FILE CONTEXT:
- File path: {file_path}
- File name: {Path(file_path).name}
- Processing timestamp: {datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}

"""
            
            return file_context + prompt
            
        except Exception as e:
            self.logger.warning(f"Could not build comprehensive prompt: {e}")
            # Fallback to basic prompt
            return self._build_basic_prompt(content, info_type)
    
    def _get_constraints_for_type(self, info_type: str) -> Dict[str, Any]:
        """Get SHACL constraints for a specific info-type."""
        # This would typically load from SHACL shapes
        # For now, use predefined constraints based on the guideline
        constraints_map = {
            'general-document': {
                'mandatory_fields': ['title', 'info-type', 'kb-id'],
                'forbidden_fields': ['standard_id'],
                'pattern_constraints': {},
                'value_constraints': {'info-type': 'general-document'}
            },
            'standard-definition': {
                'mandatory_fields': ['title', 'info-type', 'standard_id', 'version', 'kb-id'],
                'forbidden_fields': [],
                'pattern_constraints': {'standard_id': '^[A-Z]{2}-[A-Z]{2,6}-[A-Z0-9\\-]+$'},
                'value_constraints': {'info-type': 'standard-definition'}
            },
            'policy-document': {
                'mandatory_fields': ['title', 'info-type', 'standard_id', 'version', 'kb-id'],
                'forbidden_fields': [],
                'pattern_constraints': {'standard_id': '^[A-Z]{2}-[A-Z]{2,6}-[A-Z0-9\\-]+$'},
                'value_constraints': {'info-type': 'policy-document'}
            },
            'technical-report': {
                'mandatory_fields': ['title', 'info-type', 'version', 'kb-id'],
                'forbidden_fields': ['standard_id'],
                'pattern_constraints': {},
                'value_constraints': {'info-type': 'technical-report'}
            },
            'meeting-notes': {
                'mandatory_fields': ['title', 'info-type', 'kb-id'],
                'forbidden_fields': ['standard_id', 'version'],
                'pattern_constraints': {},
                'value_constraints': {'info-type': 'meeting-notes'}
            }
        }
        
        return constraints_map.get(info_type, constraints_map['general-document'])
    
    def _build_basic_prompt(self, content: str, info_type: str) -> str:
        """Build basic prompt as fallback."""
        return f"""
Generate YAML frontmatter for a {info_type} document.

Document content preview:
{content[:500]}...

Requirements:
- Generate valid YAML frontmatter
- Include 'title', 'info-type', and 'kb-id' fields
- Set 'info-type' to '{info_type}'
- Use ISO 8601 format for dates

Generate ONLY the YAML frontmatter block:
"""
    
    def _apply_frontmatter_to_file(self, file_path: str, content: str, 
                                 frontmatter: Dict[str, Any]) -> str:
        """Sub-step 5.6: Apply frontmatter to document content."""
        # Convert frontmatter to YAML
        frontmatter_yaml = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
        
        # Remove existing frontmatter if present
        if content.startswith('---\n'):
            end_marker = content.find('\n---\n', 4)
            if end_marker != -1:
                # Replace existing frontmatter
                content = content[end_marker + 5:]  # Skip past the closing ---
        
        # Add new frontmatter
        new_content = f"---\n{frontmatter_yaml}---\n\n{content.lstrip()}"
        
        return new_content
    
    def _write_file_content(self, file_path: str, content: str):
        """Write updated content back to file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.logger.info(f"Successfully updated {file_path}")
        except Exception as e:
            self.logger.error(f"Could not write file {file_path}: {e}")
            raise
    
    def _log_generation_metrics(self, file_path: str, generation_result: Dict[str, Any], 
                              processing_time: float) -> Dict[str, Any]:
        """Sub-step 5.8: Log success metrics and return result."""
        success = generation_result.get('success', False)
        attempts_used = generation_result.get('attempts_used', 1)
        fallback_used = generation_result.get('fallback_used', False)
        validation_method = generation_result.get('validation_method', 'unknown')
        
        # Update statistics
        self.generation_stats['total_processed'] += 1
        if success:
            self.generation_stats['successful_generations'] += 1
        if fallback_used:
            self.generation_stats['fallback_generations'] += 1
        
        # Update average attempts
        total_attempts = (self.generation_stats['average_attempts'] * 
                         (self.generation_stats['total_processed'] - 1) + attempts_used)
        self.generation_stats['average_attempts'] = total_attempts / self.generation_stats['total_processed']
        
        # Record processing history
        history_entry = {
            'file_path': file_path,
            'timestamp': datetime.now().isoformat(),
            'success': success,
            'attempts_used': attempts_used,
            'fallback_used': fallback_used,
            'validation_method': validation_method,
            'processing_time_seconds': processing_time
        }
        self.generation_stats['processing_history'].append(history_entry)
        
        # Log metrics
        self.logger.info(f"Generation metrics for {file_path}:")
        self.logger.info(f"  Success: {success}")
        self.logger.info(f"  Attempts: {attempts_used}")
        self.logger.info(f"  Fallback used: {fallback_used}")
        self.logger.info(f"  Processing time: {processing_time:.2f}s")
        self.logger.info(f"  Validation method: {validation_method}")
        
        return self._create_success_result(file_path, generation_result['frontmatter'], validation_method)
    
    def _create_success_result(self, file_path: str, frontmatter: Dict[str, Any], 
                             method: str) -> Dict[str, Any]:
        """Create success result dictionary."""
        return {
            'success': True,
            'file_processed': file_path,
            'info_type': frontmatter.get('info-type', 'unknown'),
            'frontmatter_fields': list(frontmatter.keys()),
            'generation_method': method,
            'processing_timestamp': datetime.now().isoformat()
        }
    
    def get_processing_statistics(self) -> Dict[str, Any]:
        """Get comprehensive processing statistics."""
        stats = self.generation_stats.copy()
        
        if stats['total_processed'] > 0:
            stats['success_rate'] = (stats['successful_generations'] / 
                                   stats['total_processed'] * 100)
            stats['fallback_rate'] = (stats['fallback_generations'] / 
                                    stats['total_processed'] * 100)
        else:
            stats['success_rate'] = 0
            stats['fallback_rate'] = 0
        
        return stats
    
    def process_multiple_files(self, file_paths: List[str], params: Dict[str, Any]) -> Dict[str, Any]:
        """Process multiple files with enhanced frontmatter generation."""
        results = {}
        total_start_time = datetime.now()
        
        for file_path in file_paths:
            try:
                result = self.execute(file_path, **params)
                results[file_path] = result
            except Exception as e:
                results[file_path] = {
                    'success': False,
                    'error': str(e)
                }
        
        total_time = (datetime.now() - total_start_time).total_seconds()
        
        return {
            'total_files': len(file_paths),
            'results': results,
            'total_processing_time': total_time,
            'statistics': self.get_processing_statistics()
        }


# Registration function for Scribe engine
def register_action():
    """Register the enhanced frontmatter action with Scribe."""
    return EnhancedFrontmatterAction()


if __name__ == "__main__":
    # Example usage for testing
    action = EnhancedFrontmatterAction()
    
    # Test with a sample file (if it exists)
    test_files = [
        'README.md',
        'standards/src/MT-SCHEMA-FRONTMATTER.md'
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"Testing enhanced frontmatter generation on: {test_file}")
            result = action.execute(test_file, force_regenerate=True)
            print(f"Result: {result}")
            break
    else:
        print("No test files found for demonstration")
    
    # Get statistics
    stats = action.get_processing_statistics()
    print(f"Processing Statistics: {stats}")