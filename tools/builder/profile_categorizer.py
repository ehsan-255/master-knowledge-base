#!/usr/bin/env python3
"""
Profile Identification and Categorization

Implementation of Phase 2: Step 2.1.2 - Profile Identification and Categorization
From: ultimate-frontmatter-enhancement-guideline-20250617-0312.md

This module categorizes SHACL profiles by document type and complexity,
generating structured hierarchies for documentation generation.
"""

from typing import Dict, List, Any, Set, Tuple
from collections import defaultdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProfileCategorizer:
    """
    Profile Categorizer for SHACL profiles.
    
    Categorizes SHACL profiles by document type and complexity to generate
    structured hierarchies suitable for automated documentation generation.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def categorize_profiles(self, rule_matrix: Dict[str, Any]) -> Dict[str, Any]:
        """
        Categorize SHACL profiles by document type and complexity.
        
        Args:
            rule_matrix: Rule matrix from SHACL parser
            
        Returns:
            Structured profile hierarchy with categorization
        """
        self.logger.info(f"Starting profile categorization for {len(rule_matrix)} profiles")
        
        # Step 1: Group rules by target info-type
        self.logger.info("Step 1: Grouping rules by target info-type...")
        type_groups = self._group_by_info_type(rule_matrix)
        
        # Step 2: Identify mandatory vs optional fields per type
        self.logger.info("Step 2: Categorizing fields by requirement level...")
        field_categories = self._categorize_fields_by_requirement(type_groups)
        
        # Step 3: Detect inheritance patterns
        self.logger.info("Step 3: Detecting inheritance patterns...")
        inheritance_patterns = self._detect_inheritance_patterns(type_groups)
        
        # Step 4: Generate profile hierarchy
        self.logger.info("Step 4: Building profile hierarchy...")
        profile_hierarchy = self._build_profile_hierarchy(
            field_categories, inheritance_patterns
        )
        
        self.logger.info(f"Profile categorization complete. Generated {len(profile_hierarchy)} profile categories.")
        return profile_hierarchy
    
    def _group_by_info_type(self, rule_matrix: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Step 1: Group rules by target info-type."""
        type_groups = defaultdict(list)
        
        for shape_name, rule_set in rule_matrix.items():
            # Determine target info-type from shape targets or name
            info_type = self._extract_info_type_from_rule(rule_set)
            
            # Add shape to appropriate group
            type_groups[info_type].append({
                'shape_name': shape_name,
                'rule_set': rule_set,
                'profile_type': rule_set.get('profile_type', 'general-validation'),
                'documentation_priority': rule_set.get('documentation_priority', 0)
            })
        
        # Sort each group by documentation priority
        for info_type in type_groups:
            type_groups[info_type].sort(
                key=lambda x: x['documentation_priority'], 
                reverse=True
            )
        
        self.logger.info(f"Grouped profiles into {len(type_groups)} info-type categories")
        return dict(type_groups)
    
    def _extract_info_type_from_rule(self, rule_set: Dict[str, Any]) -> str:
        """Extract info-type from rule set targets or infer from shape name."""
        targets = rule_set.get('targets', {})
        shape_name = rule_set.get('shape_name', '')
        
        # First, check target_node expressions for explicit info-type
        target_nodes = targets.get('target_node', [])
        for target_expr in target_nodes:
            if 'kb:info_type' in target_expr:
                # Extract value from expressions like: sh:property [ sh:path kb:info_type ; sh:hasValue "standard-definition" ]
                info_type_match = self._extract_has_value_from_target(target_expr)
                if info_type_match:
                    return info_type_match
        
        # Fallback: infer from shape name
        return self._infer_info_type_from_shape_name(shape_name)
    
    def _extract_has_value_from_target(self, target_expr: str) -> str:
        """Extract hasValue from target expression."""
        # Look for patterns like: sh:hasValue "standard-definition"
        import re
        has_value_pattern = r'sh:hasValue\s+"([^"]+)"'
        match = re.search(has_value_pattern, target_expr)
        if match:
            return match.group(1)
        
        # Look for patterns without quotes
        has_value_pattern = r'sh:hasValue\s+(\w+[-\w]*)'
        match = re.search(has_value_pattern, target_expr)
        if match:
            return match.group(1)
        
        return 'general-document'
    
    def _infer_info_type_from_shape_name(self, shape_name: str) -> str:
        """Infer info-type from shape name patterns."""
        shape_lower = shape_name.lower()
        
        if 'standard' in shape_lower:
            return 'standard-definition'
        elif 'critical' in shape_lower or 'p0' in shape_lower:
            return 'technical-report'
        elif 'mandatory' in shape_lower:
            return 'policy-document'
        elif 'related' in shape_lower:
            return 'general-document'
        else:
            return 'general-document'
    
    def _categorize_fields_by_requirement(self, type_groups: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Step 2: Identify mandatory vs optional fields per type."""
        field_categories = {}
        
        for info_type, profiles in type_groups.items():
            # Aggregate field requirements across all profiles for this info-type
            aggregated_fields = {
                'mandatory_fields': set(),
                'forbidden_fields': set(),
                'optional_fields': set(),
                'pattern_constraints': {},
                'datatype_constraints': {},
                'value_constraints': {}
            }
            
            for profile in profiles:
                rule_set = profile['rule_set']
                cardinality = rule_set.get('cardinality', {})
                patterns = rule_set.get('patterns', {})
                datatypes = rule_set.get('datatypes', {})
                
                # Collect mandatory fields
                for field_info in cardinality.get('mandatory_fields', []):
                    field_name = field_info.get('field') if isinstance(field_info, dict) else field_info
                    aggregated_fields['mandatory_fields'].add(field_name)
                
                # Collect forbidden fields
                for field_info in cardinality.get('forbidden_fields', []):
                    field_name = field_info.get('field') if isinstance(field_info, dict) else field_info
                    aggregated_fields['forbidden_fields'].add(field_name)
                
                # Collect optional fields
                for field_info in cardinality.get('optional_fields', []):
                    field_name = field_info.get('field') if isinstance(field_info, dict) else field_info
                    aggregated_fields['optional_fields'].add(field_name)
                
                # Collect pattern constraints
                for field_name, pattern_info in patterns.items():
                    aggregated_fields['pattern_constraints'][field_name] = pattern_info
                
                # Collect datatype constraints
                for field_name, datatype_info in datatypes.items():
                    aggregated_fields['datatype_constraints'][field_name] = datatype_info
            
            # Convert sets to sorted lists for consistent output
            aggregated_fields['mandatory_fields'] = sorted(list(aggregated_fields['mandatory_fields']))
            aggregated_fields['forbidden_fields'] = sorted(list(aggregated_fields['forbidden_fields']))
            aggregated_fields['optional_fields'] = sorted(list(aggregated_fields['optional_fields']))
            
            # Calculate field requirement metrics
            field_metrics = {
                'total_constraints': len(aggregated_fields['mandatory_fields']) + 
                                   len(aggregated_fields['forbidden_fields']) + 
                                   len(aggregated_fields['pattern_constraints']),
                'mandatory_count': len(aggregated_fields['mandatory_fields']),
                'forbidden_count': len(aggregated_fields['forbidden_fields']),
                'pattern_count': len(aggregated_fields['pattern_constraints']),
                'complexity_score': self._calculate_complexity_score(aggregated_fields)
            }
            
            field_categories[info_type] = {
                'fields': aggregated_fields,
                'metrics': field_metrics,
                'profiles': profiles
            }
        
        return field_categories
    
    def _calculate_complexity_score(self, aggregated_fields: Dict[str, Any]) -> int:
        """Calculate complexity score for field requirements."""
        score = 0
        score += len(aggregated_fields['mandatory_fields']) * 2  # Mandatory fields are high impact
        score += len(aggregated_fields['forbidden_fields']) * 3  # Forbidden fields are highest impact
        score += len(aggregated_fields['pattern_constraints']) * 2  # Pattern constraints are high impact
        score += len(aggregated_fields['datatype_constraints']) * 1  # Datatype constraints are medium impact
        return score
    
    def _detect_inheritance_patterns(self, type_groups: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Step 3: Detect inheritance patterns between profile types."""
        inheritance_patterns = {
            'base_profiles': [],
            'derived_profiles': {},
            'shared_constraints': {},
            'type_hierarchy': {}
        }
        
        # Find shared mandatory fields across all types (universal requirements)
        all_mandatory_fields = []
        for info_type, profiles in type_groups.items():
            for profile in profiles:
                cardinality = profile['rule_set'].get('cardinality', {})
                mandatory_fields = cardinality.get('mandatory_fields', [])
                for field_info in mandatory_fields:
                    field_name = field_info.get('field') if isinstance(field_info, dict) else field_info
                    all_mandatory_fields.append(field_name)
        
        # Calculate field frequency
        field_frequency = defaultdict(int)
        for field in all_mandatory_fields:
            field_frequency[field] += 1
        
        # Fields that appear in multiple types are candidates for base profile
        universal_fields = [
            field for field, count in field_frequency.items() 
            if count >= len(type_groups) * 0.5  # Appears in at least 50% of types
        ]
        
        inheritance_patterns['shared_constraints']['universal_mandatory'] = universal_fields
        
        # Identify base profile (most commonly used constraints)
        if universal_fields:
            inheritance_patterns['base_profiles'].append({
                'name': 'UniversalDocumentProfile',
                'mandatory_fields': universal_fields,
                'description': 'Base profile with universal mandatory fields'
            })
        
        # Build type hierarchy based on field relationships
        for info_type, profiles in type_groups.items():
            # Calculate field overlap with universal fields
            type_mandatory = set()
            for profile in profiles:
                cardinality = profile['rule_set'].get('cardinality', {})
                for field_info in cardinality.get('mandatory_fields', []):
                    field_name = field_info.get('field') if isinstance(field_info, dict) else field_info
                    type_mandatory.add(field_name)
            
            overlap_with_universal = len(set(universal_fields) & type_mandatory)
            total_type_fields = len(type_mandatory)
            
            inheritance_patterns['type_hierarchy'][info_type] = {
                'extends_universal': overlap_with_universal > 0,
                'field_overlap_ratio': overlap_with_universal / max(total_type_fields, 1),
                'specialization_fields': sorted(list(type_mandatory - set(universal_fields))),
                'total_field_count': total_type_fields
            }
        
        return inheritance_patterns
    
    def _build_profile_hierarchy(self, field_categories: Dict[str, Any], 
                                inheritance_patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Step 4: Generate profile hierarchy with inheritance and categorization."""
        profile_hierarchy = {
            'base_profiles': inheritance_patterns.get('base_profiles', []),
            'document_type_profiles': {},
            'specialization_profiles': {},
            'metadata': {
                'total_types': len(field_categories),
                'hierarchy_depth': 2,  # Base + Document Type levels
                'complexity_distribution': {}
            }
        }
        
        # Build document type profiles
        for info_type, category_data in field_categories.items():
            fields = category_data['fields']
            metrics = category_data['metrics']
            profiles = category_data['profiles']
            
            # Determine inheritance relationship
            type_hierarchy = inheritance_patterns.get('type_hierarchy', {}).get(info_type, {})
            
            document_profile = {
                'info_type': info_type,
                'extends': 'UniversalDocumentProfile' if type_hierarchy.get('extends_universal', False) else None,
                'mandatory_fields': fields['mandatory_fields'],
                'forbidden_fields': fields['forbidden_fields'],
                'optional_fields': fields['optional_fields'],
                'pattern_constraints': fields['pattern_constraints'],
                'datatype_constraints': fields['datatype_constraints'],
                'specialization_fields': type_hierarchy.get('specialization_fields', []),
                'complexity_metrics': metrics,
                'source_shapes': [p['shape_name'] for p in profiles],
                'documentation_sections': self._generate_documentation_sections(fields, metrics)
            }
            
            profile_hierarchy['document_type_profiles'][info_type] = document_profile
            
            # Build specialization profiles if there are multiple shapes for this type
            if len(profiles) > 1:
                specializations = []
                for profile in profiles:
                    if profile['profile_type'] != 'general-validation':
                        specialization = {
                            'name': profile['shape_name'],
                            'profile_type': profile['profile_type'],
                            'extends': info_type,
                            'additional_constraints': self._extract_additional_constraints(profile['rule_set']),
                            'priority': profile['documentation_priority']
                        }
                        specializations.append(specialization)
                
                if specializations:
                    profile_hierarchy['specialization_profiles'][info_type] = specializations
        
        # Calculate complexity distribution
        complexity_scores = [
            data.get('metrics', {}).get('complexity_score', 0)
            for data in field_categories.values()
        ]
        
        if complexity_scores:
            profile_hierarchy['metadata']['complexity_distribution'] = {
                'min_complexity': min(complexity_scores),
                'max_complexity': max(complexity_scores),
                'avg_complexity': sum(complexity_scores) / len(complexity_scores),
                'total_constraints': sum(data.get('metrics', {}).get('total_constraints', 0) for data in field_categories.values())
            }
        
        return profile_hierarchy
    
    def _generate_documentation_sections(self, fields: Dict[str, Any], metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate documentation sections based on field requirements."""
        sections = {
            'required_fields': {
                'title': 'Required Fields',
                'fields': fields['mandatory_fields'],
                'description': f"These {len(fields['mandatory_fields'])} fields are mandatory for this document type."
            },
            'forbidden_fields': {
                'title': 'Forbidden Fields', 
                'fields': fields['forbidden_fields'],
                'description': f"These {len(fields['forbidden_fields'])} fields must not be present in this document type."
            },
            'validation_rules': {
                'title': 'Validation Rules',
                'pattern_count': len(fields['pattern_constraints']),
                'datatype_count': len(fields['datatype_constraints']),
                'description': f"Contains {len(fields['pattern_constraints'])} pattern constraints and {len(fields['datatype_constraints'])} datatype constraints."
            }
        }
        
        # Add complexity indicator
        complexity_level = 'Low'
        if metrics['complexity_score'] > 10:
            complexity_level = 'High'
        elif metrics['complexity_score'] > 5:
            complexity_level = 'Medium'
        
        sections['complexity'] = {
            'level': complexity_level,
            'score': metrics['complexity_score'],
            'description': f"This profile has {complexity_level.lower()} complexity with a score of {metrics['complexity_score']}."
        }
        
        return sections
    
    def _extract_additional_constraints(self, rule_set: Dict[str, Any]) -> Dict[str, Any]:
        """Extract additional constraints for specialization profiles."""
        additional = {
            'specific_patterns': {},
            'specific_values': {},
            'cardinality_overrides': {}
        }
        
        patterns = rule_set.get('patterns', {})
        for field, pattern_info in patterns.items():
            if isinstance(pattern_info, dict) and pattern_info.get('pattern'):
                additional['specific_patterns'][field] = pattern_info['pattern']
            elif isinstance(pattern_info, dict) and pattern_info.get('hasValue'):
                additional['specific_values'][field] = pattern_info['hasValue']
        
        return additional
    
    def get_categorization_summary(self, profile_hierarchy: Dict[str, Any]) -> Dict[str, Any]:
        """Get a summary of the profile categorization."""
        summary = {
            'hierarchy_overview': {
                'base_profiles': len(profile_hierarchy.get('base_profiles', [])),
                'document_type_profiles': len(profile_hierarchy.get('document_type_profiles', {})),
                'specialization_profiles': sum(
                    len(specs) for specs in profile_hierarchy.get('specialization_profiles', {}).values()
                ),
            },
            'field_analysis': {},
            'complexity_analysis': profile_hierarchy.get('metadata', {}).get('complexity_distribution', {}),
            'inheritance_coverage': {}
        }
        
        # Analyze field distribution across document types
        all_mandatory = set()
        all_forbidden = set()
        
        for info_type, profile in profile_hierarchy.get('document_type_profiles', {}).items():
            all_mandatory.update(profile.get('mandatory_fields', []))
            all_forbidden.update(profile.get('forbidden_fields', []))
        
        summary['field_analysis'] = {
            'unique_mandatory_fields': len(all_mandatory),
            'unique_forbidden_fields': len(all_forbidden),
            'total_unique_fields': len(all_mandatory | all_forbidden)
        }
        
        # Analyze inheritance coverage
        extending_count = sum(
            1 for profile in profile_hierarchy.get('document_type_profiles', {}).values()
            if profile.get('extends')
        )
        
        summary['inheritance_coverage'] = {
            'profiles_extending_base': extending_count,
            'inheritance_ratio': extending_count / max(len(profile_hierarchy.get('document_type_profiles', {})), 1)
        }
        
        return summary


if __name__ == "__main__":
    # Example usage for testing
    from shacl_parser import SHACLParser
    
    parser = SHACLParser('standards/registry/shacl-shapes.ttl')
    rules = parser.extract_validation_rules()
    
    categorizer = ProfileCategorizer()
    hierarchy = categorizer.categorize_profiles(rules)
    
    print(f"Generated profile hierarchy with {len(hierarchy['document_type_profiles'])} document types")
    
    summary = categorizer.get_categorization_summary(hierarchy)
    print(f"Summary: {summary}")