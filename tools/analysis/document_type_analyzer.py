#!/usr/bin/env python3
"""
Universal Document Type Analyzer

Implementation of Phase 1: Robust Document Type Analysis Methodology
From: ultimate-frontmatter-enhancement-guideline-20250617-0312.md

This module provides scalable, on-demand methodology for current repository
and future KB imports with comprehensive document type analysis.
"""

import re
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UniversalDocumentTypeAnalyzer:
    """
    Universal Document Type Analyzer for scalable document classification.
    
    Designed to work with current limited documents AND future KB imports.
    Provides robust methodology for analyzing document types and generating
    actionable SHACL profile suggestions.
    """
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.analysis_results = {}
        self.type_patterns = {}
        self.field_usage_matrix = {}
        
        # Initialize logger for this analyzer instance
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def analyze_on_demand(self, target_paths: Optional[List[Path]] = None, 
                         kb_import_mode: bool = False) -> Dict[str, Any]:
        """
        Robust methodology for analyzing document types.
        Works with current limited documents AND future KB imports.
        
        Args:
            target_paths: List of paths to analyze. If None, analyzes entire repository.
            kb_import_mode: Whether this is analyzing an imported KB (changes behavior)
            
        Returns:
            Comprehensive analysis results with actionable recommendations
        """
        if target_paths is None:
            target_paths = [self.repo_path]
        
        self.logger.info(f"Starting document type analysis for {len(target_paths)} target paths")
        self.logger.info(f"KB import mode: {kb_import_mode}")
        
        # Phase 1: Content-based classification
        self.logger.info("Phase 1: Analyzing content patterns...")
        content_analysis = self._analyze_content_patterns(target_paths)
        
        # Phase 2: Structural pattern recognition
        self.logger.info("Phase 2: Analyzing structural patterns...")
        structural_analysis = self._analyze_structural_patterns(target_paths)
        
        # Phase 3: Metadata pattern extraction
        self.logger.info("Phase 3: Analyzing metadata patterns...")
        metadata_analysis = self._analyze_metadata_patterns(target_paths)
        
        # Phase 4: Path-based classification
        self.logger.info("Phase 4: Analyzing path patterns...")
        path_analysis = self._analyze_path_patterns(target_paths)
        
        # Phase 5: Composite classification
        self.logger.info("Phase 5: Generating composite profiles...")
        composite_profiles = self._generate_composite_profiles(
            content_analysis, structural_analysis, 
            metadata_analysis, path_analysis
        )
        
        # Phase 6: Generate actionable SHACL profiles
        self.logger.info("Phase 6: Generating SHACL profile suggestions...")
        shacl_profiles = self._generate_shacl_profile_suggestions(composite_profiles)
        
        results = {
            'document_types_identified': composite_profiles,
            'shacl_profile_suggestions': shacl_profiles,
            'field_usage_matrix': self.field_usage_matrix,
            'recommended_actions': self._generate_action_recommendations(),
            'analysis_metadata': {
                'target_paths': [str(p) for p in target_paths],
                'kb_import_mode': kb_import_mode,
                'total_documents_analyzed': sum(len(data.get('files', [])) for data in composite_profiles.values()),
                'document_types_found': list(composite_profiles.keys())
            }
        }
        
        self.logger.info(f"Analysis complete. Found {len(composite_profiles)} document types.")
        return results
    
    def _analyze_content_patterns(self, target_paths: List[Path]) -> Dict[str, Any]:
        """Analyze document content to infer types based on content patterns."""
        patterns = {
            'standard-definition': [
                r'## STANDARD DEFINITION',
                r'standard_id:',
                r'## COMPLIANCE REQUIREMENTS',
                r'## STANDARD SCOPE',
                r'## VALIDATION CRITERIA'
            ],
            'technical-report': [
                r'## EXECUTIVE SUMMARY',
                r'## ANALYSIS',
                r'Report Date:',
                r'## FINDINGS',
                r'## RECOMMENDATIONS'
            ],
            'policy-document': [
                r'## POLICY STATEMENT',
                r'## MANDATORY REQUIREMENTS',
                r'lifecycle_gatekeeper:',
                r'## ENFORCEMENT',
                r'## COMPLIANCE'
            ],
            'meeting-notes': [
                r'## ATTENDEES',
                r'## ACTION ITEMS',
                r'Meeting Date:',
                r'## DECISIONS',
                r'## NEXT STEPS'
            ],
            'process-document': [
                r'## PROCESS OVERVIEW',
                r'## STEPS',
                r'## WORKFLOW',
                r'## METHODOLOGY'
            ],
            'guide-document': [
                r'## INTRODUCTION',
                r'## GETTING STARTED',
                r'## TUTORIAL',
                r'## EXAMPLES'
            ],
            'general-document': [
                # Fallback patterns
                r'# .+',  # Any heading
                r'## .+'  # Any sub-heading
            ]
        }
        
        classification_results = {}
        
        for path in target_paths:
            for md_file in path.rglob("*.md"):
                try:
                    content = md_file.read_text(encoding='utf-8', errors='ignore')
                    scores = {}
                    
                    for doc_type, pattern_list in patterns.items():
                        score = sum(1 for pattern in pattern_list 
                                  if re.search(pattern, content, re.IGNORECASE))
                        scores[doc_type] = score
                    
                    # Assign type based on highest score
                    best_type = max(scores, key=scores.get) if scores and max(scores.values()) > 0 else 'general-document'
                    classification_results[str(md_file)] = {
                        'inferred_type': best_type,
                        'confidence_scores': scores,
                        'current_frontmatter': self._extract_frontmatter(content),
                        'content_length': len(content),
                        'heading_count': len(re.findall(r'^#+\s', content, re.MULTILINE))
                    }
                    
                except Exception as e:
                    self.logger.warning(f"Error analyzing {md_file}: {e}")
        
        return classification_results
    
    def _analyze_structural_patterns(self, target_paths: List[Path]) -> Dict[str, Any]:
        """Analyze document structure patterns."""
        structural_analysis = {}
        
        for path in target_paths:
            for md_file in path.rglob("*.md"):
                try:
                    content = md_file.read_text(encoding='utf-8', errors='ignore')
                    
                    # Analyze document structure
                    structure = {
                        'has_frontmatter': content.startswith('---'),
                        'heading_levels': self._extract_heading_levels(content),
                        'has_code_blocks': bool(re.search(r'```', content)),
                        'has_tables': bool(re.search(r'\|.*\|', content)),
                        'has_lists': bool(re.search(r'^\s*[-\*\+]\s', content, re.MULTILINE)),
                        'has_numbered_lists': bool(re.search(r'^\s*\d+\.\s', content, re.MULTILINE)),
                        'has_links': bool(re.search(r'\[.*\]\(.*\)', content)),
                        'paragraph_count': len(re.findall(r'\n\s*\n', content))
                    }
                    
                    structural_analysis[str(md_file)] = structure
                    
                except Exception as e:
                    self.logger.warning(f"Error analyzing structure of {md_file}: {e}")
        
        return structural_analysis
    
    def _analyze_metadata_patterns(self, target_paths: List[Path]) -> Dict[str, Any]:
        """Analyze existing metadata patterns in frontmatter."""
        metadata_analysis = {}
        field_usage = defaultdict(int)
        field_patterns = defaultdict(set)
        
        for path in target_paths:
            for md_file in path.rglob("*.md"):
                try:
                    content = md_file.read_text(encoding='utf-8', errors='ignore')
                    frontmatter = self._extract_frontmatter(content)
                    
                    if frontmatter:
                        # Track field usage
                        for field, value in frontmatter.items():
                            field_usage[field] += 1
                            if isinstance(value, str):
                                field_patterns[field].add(value)
                            elif isinstance(value, list):
                                for item in value:
                                    if isinstance(item, str):
                                        field_patterns[field].add(item)
                        
                        metadata_analysis[str(md_file)] = {
                            'fields_present': list(frontmatter.keys()),
                            'field_count': len(frontmatter),
                            'info_type': frontmatter.get('info_type'),
                            'has_standard_id': 'standard_id' in frontmatter,
                            'has_kb_id': 'kb_id' in frontmatter,
                            'criticality': frontmatter.get('criticality'),
                            'frontmatter_data': frontmatter
                        }
                    else:
                        metadata_analysis[str(md_file)] = {
                            'fields_present': [],
                            'field_count': 0,
                            'info_type': None,
                            'has_standard_id': False,
                            'has_kb_id': False,
                            'criticality': None,
                            'frontmatter_data': {}
                        }
                        
                except Exception as e:
                    self.logger.warning(f"Error analyzing metadata of {md_file}: {e}")
        
        # Store field usage matrix for later use
        self.field_usage_matrix = {
            'usage_counts': dict(field_usage),
            'value_patterns': {k: list(v) for k, v in field_patterns.items()}
        }
        
        return metadata_analysis
    
    def _analyze_path_patterns(self, target_paths: List[Path]) -> Dict[str, Any]:
        """Analyze file path patterns for type inference."""
        path_patterns = {
            'standard-definition': [r'standards/src/', r'/standards/', r'.*-STANDARD.*', r'.*POLICY.*'],
            'technical-report': [r'tools/reports/', r'/reports/', r'.*-report.*', r'.*-analysis.*'],
            'policy-document': [r'standards/src/.*POLICY.*', r'/policies/', r'.*-policy.*'],
            'meeting-notes': [r'meetings/', r'/notes/', r'.*-notes.*', r'.*-meeting.*'],
            'guide-document': [r'guides/', r'/guide/', r'.*-guide.*', r'.*tutorial.*'],
            'general-document': []  # Fallback
        }
        
        path_analysis = {}
        
        for path in target_paths:
            for md_file in path.rglob("*.md"):
                file_path_str = str(md_file)
                scores = {}
                
                for doc_type, pattern_list in path_patterns.items():
                    score = sum(1 for pattern in pattern_list 
                              if re.search(pattern, file_path_str, re.IGNORECASE))
                    scores[doc_type] = score
                
                # Determine best match
                best_type = max(scores, key=scores.get) if scores and max(scores.values()) > 0 else 'general-document'
                
                path_analysis[file_path_str] = {
                    'inferred_type': best_type,
                    'path_scores': scores,
                    'file_name': md_file.name,
                    'directory': str(md_file.parent),
                    'depth': len(md_file.parts)
                }
        
        return path_analysis
    
    def _generate_composite_profiles(self, content_analysis: Dict, structural_analysis: Dict,
                                   metadata_analysis: Dict, path_analysis: Dict) -> Dict[str, Any]:
        """Generate composite classification profiles combining all analysis types."""
        composite_profiles = defaultdict(lambda: {
            'files': [],
            'characteristics': {
                'content_patterns': set(),
                'structural_features': set(),
                'common_fields': set(),
                'path_indicators': set()
            },
            'confidence_data': [],
            'field_requirements': {
                'mandatory_fields': set(),
                'optional_fields': set(),
                'forbidden_fields': set()
            }
        })
        
        # Get all files that were analyzed
        all_files = set(content_analysis.keys()) | set(structural_analysis.keys()) | set(metadata_analysis.keys()) | set(path_analysis.keys())
        
        for file_path in all_files:
            # Collect analysis results for this file
            content_data = content_analysis.get(file_path, {})
            structural_data = structural_analysis.get(file_path, {})
            metadata_data = metadata_analysis.get(file_path, {})
            path_data = path_analysis.get(file_path, {})
            
            # Determine final document type using weighted scoring
            type_scores = defaultdict(float)
            
            # Content analysis (weight: 0.4)
            if content_data.get('inferred_type'):
                content_type = content_data['inferred_type']
                confidence_scores = content_data.get('confidence_scores', {})
                content_confidence = max(confidence_scores.values()) if confidence_scores else 0
                type_scores[content_type] += 0.4 * content_confidence
            
            # Path analysis (weight: 0.3)
            if path_data.get('inferred_type'):
                path_type = path_data['inferred_type']
                path_scores = path_data.get('path_scores', {})
                path_confidence = max(path_scores.values()) if path_scores else 0
                type_scores[path_type] += 0.3 * path_confidence
            
            # Metadata analysis (weight: 0.3)
            if metadata_data.get('info_type'):
                metadata_type = metadata_data['info_type']
                type_scores[metadata_type] += 0.3 * 2  # High confidence for explicit info_type
            
            # Determine final type
            if type_scores:
                final_type = max(type_scores, key=type_scores.get)
            else:
                final_type = 'general-document'
            
            # Add to composite profile
            profile = composite_profiles[final_type]
            profile['files'].append(file_path)
            profile['confidence_data'].append({
                'file': file_path,
                'type_scores': dict(type_scores),
                'final_confidence': type_scores[final_type]
            })
            
            # Collect characteristics
            if metadata_data.get('fields_present'):
                profile['characteristics']['common_fields'].update(metadata_data['fields_present'])
            
            # Determine field requirements based on analysis
            self._update_field_requirements(profile, metadata_data, final_type)
        
        # Convert sets to lists for JSON serialization
        for profile_name, profile_data in composite_profiles.items():
            for char_name, char_set in profile_data['characteristics'].items():
                profile_data['characteristics'][char_name] = list(char_set)
            for req_name, req_set in profile_data['field_requirements'].items():
                profile_data['field_requirements'][req_name] = list(req_set)
        
        return dict(composite_profiles)
    
    def _generate_shacl_profile_suggestions(self, composite_profiles: Dict[str, Any]) -> List[str]:
        """Generate actionable SHACL profiles based on analysis results."""
        profiles = []
        
        for doc_type, characteristics in composite_profiles.items():
            # Clean up document type name for SHACL
            clean_type = doc_type.title().replace('-', '').replace('_', '')
            
            profile = f"""
# SHACL Profile for {doc_type} documents
kb:{clean_type}Profile a sh:NodeShape ;
    sh:targetNode [ sh:property [ sh:path kb:info_type ; sh:hasValue "{doc_type}" ] ] ;"""
            
            # Add mandatory fields based on analysis
            mandatory_fields = characteristics['field_requirements']['mandatory_fields']
            for field in mandatory_fields:
                profile += f"""
    sh:property [
        sh:path kb:{field} ; 
        sh:minCount 1 ;
        sh:message "{doc_type} documents must have {field} field." ;
    ] ;"""
            
            # Add forbidden fields based on analysis
            forbidden_fields = characteristics['field_requirements']['forbidden_fields']
            for field in forbidden_fields:
                profile += f"""
    sh:property [
        sh:path kb:{field} ; 
        sh:maxCount 0 ;
        sh:message "{doc_type} documents must not have {field} field." ;
    ] ;"""
            
            # Remove trailing semicolon and add period
            profile = profile.rstrip(' ;') + ' .'
            profiles.append(profile)
        
        return profiles
    
    def _update_field_requirements(self, profile: Dict, metadata_data: Dict, doc_type: str):
        """Update field requirements based on document type and analysis."""
        fields_present = set(metadata_data.get('fields_present', []))
        
        # Universal mandatory fields for all documents
        universal_mandatory = {'title', 'version', 'date_created', 'date_modified', 'info_type'}
        profile['field_requirements']['mandatory_fields'].update(universal_mandatory)
        
        # Type-specific requirements
        if doc_type in ['standard-definition', 'policy-document']:
            profile['field_requirements']['mandatory_fields'].update({'standard_id', 'criticality', 'lifecycle_gatekeeper'})
        else:
            profile['field_requirements']['forbidden_fields'].add('standard_id')
        
        # Add kb_id as universal requirement
        profile['field_requirements']['mandatory_fields'].add('kb_id')
        
        # Optional fields based on common usage
        common_optional = {'tags', 'primary_topic', 'scope_application', 'impact_areas'}
        profile['field_requirements']['optional_fields'].update(common_optional & fields_present)
    
    def _generate_action_recommendations(self) -> List[Dict[str, Any]]:
        """Generate actionable recommendations based on analysis."""
        recommendations = []
        
        recommendations.append({
            'action': 'update_shacl_shapes',
            'description': 'Update SHACL shapes with generated profiles',
            'priority': 'high',
            'implementation': 'Add generated SHACL profiles to standards/registry/shacl-shapes.ttl'
        })
        
        recommendations.append({
            'action': 'implement_universal_kb_id',
            'description': 'Ensure all documents have kb_id field',
            'priority': 'high',
            'implementation': 'Run universal kb_id migration script'
        })
        
        recommendations.append({
            'action': 'field_scope_correction',
            'description': 'Remove standard_id from non-standard documents',
            'priority': 'medium',
            'implementation': 'Run field scope correction script'
        })
        
        return recommendations
    
    def generate_kb_import_profile(self, kb_source_path: str) -> Dict[str, Any]:
        """
        Special methodology for analyzing imported KBs.
        Generates import-specific profiles and mapping recommendations.
        """
        import_analysis = self.analyze_on_demand([Path(kb_source_path)], kb_import_mode=True)
        
        mapping_recommendations = {
            'field_mappings': self._suggest_field_mappings(import_analysis),
            'type_conversions': self._suggest_type_conversions(import_analysis),
            'bulk_migration_script': self._generate_import_migration_script(import_analysis)
        }
        
        return mapping_recommendations
    
    def _suggest_field_mappings(self, import_analysis: Dict[str, Any]) -> Dict[str, str]:
        """Suggest field mappings for KB import."""
        # Implementation for field mapping suggestions
        return {
            'document_type': 'info_type',
            'id': 'kb_id',
            'standard_identifier': 'standard_id'
        }
    
    def _suggest_type_conversions(self, import_analysis: Dict[str, Any]) -> Dict[str, str]:
        """Suggest document type conversions for KB import."""
        # Implementation for type conversion suggestions
        return {
            'documentation': 'general-document',
            'standard': 'standard-definition',
            'policy': 'policy-document'
        }
    
    def _generate_import_migration_script(self, import_analysis: Dict[str, Any]) -> str:
        """Generate migration script for KB import."""
        # Implementation for migration script generation
        return """
# Generated KB Import Migration Script
# This script should be customized based on specific import requirements
"""
    
    def _extract_frontmatter(self, content: str) -> Dict[str, Any]:
        """Extract and parse YAML frontmatter from document content."""
        if not content.startswith('---'):
            return {}
        
        try:
            # Find the end of frontmatter
            end_match = re.search(r'\n---\s*\n', content)
            if not end_match:
                return {}
            
            frontmatter_text = content[3:end_match.start()]
            return yaml.safe_load(frontmatter_text) or {}
        except yaml.YAMLError:
            return {}
    
    def _extract_heading_levels(self, content: str) -> List[int]:
        """Extract heading levels from document content."""
        headings = re.findall(r'^(#+)\s', content, re.MULTILINE)
        return [len(heading) for heading in headings]


if __name__ == "__main__":
    # Example usage for testing
    analyzer = UniversalDocumentTypeAnalyzer()
    results = analyzer.analyze_on_demand()
    
    # Save results to reports directory
    timestamp = "20250617-1126"  # Use actual system timestamp
    output_file = f"tools/reports/document-type-analysis-{timestamp}.json"
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Analysis complete. Results saved to {output_file}")
    print(f"Document types found: {list(results['document_types_identified'].keys())}")