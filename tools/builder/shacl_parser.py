#!/usr/bin/env python3
"""
SHACL Parser and Rule Extractor

Implementation of Phase 2: Step 2.1.1 - SHACL Parser and Rule Extractor
From: ultimate-frontmatter-enhancement-guideline-20250617-0312.md

This module provides comprehensive parsing and rule extraction from SHACL shapes
for generating automated documentation and validation rules.
"""

import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
import logging

try:
    from rdflib import Graph, Namespace, URIRef, Literal
    from rdflib.namespace import SH, RDF, RDFS
except ImportError:
    # Fallback implementation without rdflib
    Graph = None
    print("Warning: rdflib not available. Using text-based parsing fallback.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SHACLParser:
    """
    SHACL Parser for comprehensive rule extraction from SHACL shapes.
    
    Provides step-by-step rule extraction from SHACL shapes to generate
    actionable validation rules and documentation templates.
    """
    
    def __init__(self, shacl_file_path: str):
        self.shacl_file_path = Path(shacl_file_path)
        self.shacl_graph = None
        self.profiles = {}
        self.constraints = {}
        self.raw_content = ""
        
        # Initialize logger
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # Load SHACL content
        self._load_shacl_content()
    
    def _load_shacl_content(self):
        """Load SHACL content using available parsing method."""
        try:
            with open(self.shacl_file_path, 'r', encoding='utf-8') as f:
                self.raw_content = f.read()
            
            if Graph is not None:
                self._load_with_rdflib()
            else:
                self._load_with_text_parsing()
                
        except Exception as e:
            self.logger.error(f"Failed to load SHACL file {self.shacl_file_path}: {e}")
            raise
    
    def _load_with_rdflib(self):
        """Load SHACL content using rdflib."""
        if Graph is None:
            self.logger.warning("rdflib not available, using text parsing")
            self._load_with_text_parsing()
            return
            
        try:
            self.shacl_graph = Graph()
            self.shacl_graph.parse(self.shacl_file_path, format='turtle')
            self.logger.info(f"Loaded SHACL graph with {len(self.shacl_graph)} triples")
        except Exception as e:
            self.logger.warning(f"rdflib parsing failed, falling back to text parsing: {e}")
            self.shacl_graph = None
            self._load_with_text_parsing()
    
    def _load_with_text_parsing(self):
        """Fallback text-based parsing when rdflib is not available."""
        self.logger.info("Using text-based SHACL parsing")
        # Text-based parsing implementation will be in the text parsing methods
    
    def extract_validation_rules(self) -> Dict[str, Any]:
        """
        Step-by-step rule extraction from SHACL shapes.
        
        Returns comprehensive rule matrix for documentation generation.
        """
        self.logger.info("Starting step-by-step SHACL rule extraction")
        
        # Step 1: Identify all NodeShapes
        self.logger.info("Step 1: Identifying all NodeShapes...")
        node_shapes = self._find_all_node_shapes()
        
        # Step 2: Extract targeting information
        self.logger.info("Step 2: Extracting targeting information...")
        shape_targets = self._extract_shape_targets(node_shapes)
        
        # Step 3: Parse property constraints
        self.logger.info("Step 3: Parsing property constraints...")
        property_constraints = self._parse_property_constraints(node_shapes)
        
        # Step 4: Extract cardinality constraints
        self.logger.info("Step 4: Extracting cardinality constraints...")
        cardinality_rules = self._extract_cardinality_rules(property_constraints)
        
        # Step 5: Extract datatype constraints
        self.logger.info("Step 5: Extracting datatype constraints...")
        datatype_rules = self._extract_datatype_constraints(property_constraints)
        
        # Step 6: Extract pattern constraints
        self.logger.info("Step 6: Extracting pattern constraints...")
        pattern_rules = self._extract_pattern_constraints(property_constraints)
        
        # Step 7: Build comprehensive rule matrix
        self.logger.info("Step 7: Building comprehensive rule matrix...")
        rule_matrix = self._build_rule_matrix(
            shape_targets, cardinality_rules, 
            datatype_rules, pattern_rules
        )
        
        self.logger.info(f"Rule extraction complete. Found {len(rule_matrix)} rule sets.")
        return rule_matrix
    
    def _find_all_node_shapes(self) -> List[Dict[str, Any]]:
        """Step 1: Identify all NodeShapes in the SHACL content."""
        node_shapes = []
        
        if self.shacl_graph is not None:
            # RDFLib-based extraction
            node_shapes = self._extract_node_shapes_rdf()
        else:
            # Text-based extraction
            node_shapes = self._extract_node_shapes_text()
        
        self.logger.info(f"Found {len(node_shapes)} NodeShapes")
        return node_shapes
    
    def _extract_node_shapes_rdf(self) -> List[Dict[str, Any]]:
        """Extract NodeShapes using RDFLib."""
        if self.shacl_graph is None:
            return []
            
        node_shapes = []
        
        # Define namespaces
        try:
            from rdflib import Namespace
            from rdflib.namespace import SH, RDF
            KB = Namespace("https://knowledge-base.local/vocab#")
            
            # Find all NodeShapes
            for shape in self.shacl_graph.subjects(RDF.type, SH.NodeShape):
                shape_data = {
                    'uri': str(shape),
                    'name': str(shape).split('#')[-1] if '#' in str(shape) else str(shape).split('/')[-1],
                    'raw_shape': shape
                }
                node_shapes.append(shape_data)
        except ImportError:
            self.logger.warning("rdflib not available for namespace imports")
            return []
        
        return node_shapes
    
    def _extract_node_shapes_text(self) -> List[Dict[str, Any]]:
        """Extract NodeShapes using text parsing."""
        node_shapes = []
        
        # Pattern to match NodeShape definitions
        shape_pattern = r'kb:(\w+)\s+a\s+sh:NodeShape\s*;'
        
        matches = re.finditer(shape_pattern, self.raw_content)
        for match in matches:
            shape_name = match.group(1)
            shape_data = {
                'uri': f"kb:{shape_name}",
                'name': shape_name,
                'raw_content': self._extract_shape_block(match.start())
            }
            node_shapes.append(shape_data)
        
        return node_shapes
    
    def _extract_shape_block(self, start_pos: int) -> str:
        """Extract the complete shape block from text starting at position."""
        content = self.raw_content[start_pos:]
        
        # Find the end of this shape (next shape or end of file)
        end_patterns = [
            r'\nkb:\w+\s+a\s+sh:NodeShape',  # Next shape
            r'\n\n#',  # Comment section
            r'\n@prefix',  # Prefix definition
        ]
        
        end_pos = len(content)
        for pattern in end_patterns:
            match = re.search(pattern, content)
            if match:
                end_pos = min(end_pos, match.start())
        
        return content[:end_pos]
    
    def _extract_shape_targets(self, node_shapes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Step 2: Extract targeting information from NodeShapes."""
        shape_targets = {}
        
        for shape in node_shapes:
            shape_name = shape['name']
            targets = {
                'target_class': [],
                'target_node': [],
                'target_subjects_of': [],
                'target_objects_of': []
            }
            
            if self.shacl_graph is not None:
                targets = self._extract_targets_rdf(shape['raw_shape'])
            else:
                targets = self._extract_targets_text(shape['raw_content'])
            
            shape_targets[shape_name] = targets
        
        return shape_targets
    
    def _extract_targets_rdf(self, shape_uri) -> Dict[str, List[str]]:
        """Extract targets using RDFLib."""
        targets = {
            'target_class': [],
            'target_node': [],
            'target_subjects_of': [],
            'target_objects_of': []
        }
        
        # Extract different target types
        for target_class in self.shacl_graph.objects(shape_uri, SH.targetClass):
            targets['target_class'].append(str(target_class))
        
        for target_node in self.shacl_graph.objects(shape_uri, SH.targetNode):
            targets['target_node'].append(str(target_node))
        
        return targets
    
    def _extract_targets_text(self, shape_content: str) -> Dict[str, List[str]]:
        """Extract targets using text parsing."""
        targets = {
            'target_class': [],
            'target_node': [],
            'target_subjects_of': [],
            'target_objects_of': []
        }
        
        # Extract sh:targetClass
        target_class_pattern = r'sh:targetClass\s+([\w:]+)'
        for match in re.finditer(target_class_pattern, shape_content):
            targets['target_class'].append(match.group(1))
        
        # Extract sh:targetNode with complex expressions
        target_node_pattern = r'sh:targetNode\s+\[(.*?)\]'
        for match in re.finditer(target_node_pattern, shape_content, re.DOTALL):
            target_expression = match.group(1).strip()
            targets['target_node'].append(target_expression)
        
        return targets
    
    def _parse_property_constraints(self, node_shapes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Step 3: Parse property constraints from NodeShapes."""
        property_constraints = {}
        
        for shape in node_shapes:
            shape_name = shape['name']
            constraints = []
            
            if self.shacl_graph is not None:
                constraints = self._parse_properties_rdf(shape['raw_shape'])
            else:
                constraints = self._parse_properties_text(shape['raw_content'])
            
            property_constraints[shape_name] = constraints
        
        return property_constraints
    
    def _parse_properties_rdf(self, shape_uri) -> List[Dict[str, Any]]:
        """Parse property constraints using RDFLib."""
        properties = []
        
        for prop in self.shacl_graph.objects(shape_uri, SH.property):
            prop_data = {
                'path': None,
                'constraints': {}
            }
            
            # Extract property path
            for path in self.shacl_graph.objects(prop, SH.path):
                prop_data['path'] = str(path)
            
            # Extract constraints
            for min_count in self.shacl_graph.objects(prop, SH.minCount):
                prop_data['constraints']['minCount'] = int(min_count)
            
            for max_count in self.shacl_graph.objects(prop, SH.maxCount):
                prop_data['constraints']['maxCount'] = int(max_count)
            
            for pattern in self.shacl_graph.objects(prop, SH.pattern):
                prop_data['constraints']['pattern'] = str(pattern)
            
            for datatype in self.shacl_graph.objects(prop, SH.datatype):
                prop_data['constraints']['datatype'] = str(datatype)
            
            for has_value in self.shacl_graph.objects(prop, SH.hasValue):
                prop_data['constraints']['hasValue'] = str(has_value)
            
            for message in self.shacl_graph.objects(prop, SH.message):
                prop_data['constraints']['message'] = str(message)
            
            properties.append(prop_data)
        
        return properties
    
    def _parse_properties_text(self, shape_content: str) -> List[Dict[str, Any]]:
        """Parse property constraints using text parsing."""
        properties = []
        
        # Find all sh:property blocks
        property_pattern = r'sh:property\s+\[(.*?)\]'
        
        for match in re.finditer(property_pattern, shape_content, re.DOTALL):
            prop_content = match.group(1)
            prop_data = {
                'path': None,
                'constraints': {}
            }
            
            # Extract path
            path_match = re.search(r'sh:path\s+([\w:]+)', prop_content)
            if path_match:
                prop_data['path'] = path_match.group(1)
            
            # Extract constraints
            constraint_patterns = {
                'minCount': r'sh:minCount\s+(\d+)',
                'maxCount': r'sh:maxCount\s+(\d+)',
                'pattern': r'sh:pattern\s+"([^"]+)"',
                'datatype': r'sh:datatype\s+([\w:]+)',
                'hasValue': r'sh:hasValue\s+"([^"]+)"',
                'message': r'sh:message\s+"([^"]+)"'
            }
            
            for constraint_name, pattern in constraint_patterns.items():
                match = re.search(pattern, prop_content)
                if match:
                    value = match.group(1)
                    if constraint_name in ['minCount', 'maxCount']:
                        value = int(value)
                    prop_data['constraints'][constraint_name] = value
            
            # Handle sh:in (value lists)
            in_pattern = r'sh:in\s+\(\s*([^)]+)\s*\)'
            in_match = re.search(in_pattern, prop_content)
            if in_match:
                values = [v.strip().strip('"') for v in in_match.group(1).split()]
                prop_data['constraints']['in'] = values
            
            properties.append(prop_data)
        
        return properties
    
    def _extract_cardinality_rules(self, property_constraints: Dict[str, Any]) -> Dict[str, Any]:
        """Step 4: Extract cardinality constraints from properties."""
        cardinality_rules = {}
        
        for shape_name, properties in property_constraints.items():
            rules = {
                'mandatory_fields': [],
                'forbidden_fields': [],
                'optional_fields': []
            }
            
            for prop in properties:
                path = prop.get('path')
                constraints = prop.get('constraints', {})
                
                if not path:
                    continue
                
                # Clean path (remove kb: prefix)
                clean_path = path.replace('kb:', '')
                
                # Determine cardinality category
                min_count = constraints.get('minCount', 0)
                max_count = constraints.get('maxCount')
                
                if min_count > 0:
                    rules['mandatory_fields'].append({
                        'field': clean_path,
                        'min_count': min_count,
                        'message': constraints.get('message', f'{clean_path} is required')
                    })
                elif max_count == 0:
                    rules['forbidden_fields'].append({
                        'field': clean_path,
                        'message': constraints.get('message', f'{clean_path} is not allowed')
                    })
                else:
                    rules['optional_fields'].append({
                        'field': clean_path,
                        'max_count': max_count
                    })
            
            cardinality_rules[shape_name] = rules
        
        return cardinality_rules
    
    def _extract_datatype_constraints(self, property_constraints: Dict[str, Any]) -> Dict[str, Any]:
        """Step 5: Extract datatype constraints from properties."""
        datatype_rules = {}
        
        for shape_name, properties in property_constraints.items():
            rules = {}
            
            for prop in properties:
                path = prop.get('path')
                constraints = prop.get('constraints', {})
                
                if not path:
                    continue
                
                clean_path = path.replace('kb:', '')
                datatype = constraints.get('datatype')
                
                if datatype:
                    rules[clean_path] = {
                        'datatype': datatype,
                        'message': constraints.get('message', f'{clean_path} must be of type {datatype}')
                    }
            
            datatype_rules[shape_name] = rules
        
        return datatype_rules
    
    def _extract_pattern_constraints(self, property_constraints: Dict[str, Any]) -> Dict[str, Any]:
        """Step 6: Extract pattern constraints from properties."""
        pattern_rules = {}
        
        for shape_name, properties in property_constraints.items():
            rules = {}
            
            for prop in properties:
                path = prop.get('path')
                constraints = prop.get('constraints', {})
                
                if not path:
                    continue
                
                clean_path = path.replace('kb:', '')
                
                # Pattern constraints
                pattern = constraints.get('pattern')
                if pattern:
                    rules[clean_path] = {
                        'pattern': pattern,
                        'message': constraints.get('message', f'{clean_path} must match pattern {pattern}')
                    }
                
                # Value constraints (hasValue, in)
                has_value = constraints.get('hasValue')
                if has_value:
                    rules[clean_path] = {
                        'hasValue': has_value,
                        'message': constraints.get('message', f'{clean_path} must have value {has_value}')
                    }
                
                in_values = constraints.get('in')
                if in_values:
                    rules[clean_path] = {
                        'in': in_values,
                        'message': constraints.get('message', f'{clean_path} must be one of: {", ".join(in_values)}')
                    }
            
            pattern_rules[shape_name] = rules
        
        return pattern_rules
    
    def _build_rule_matrix(self, shape_targets: Dict, cardinality_rules: Dict,
                          datatype_rules: Dict, pattern_rules: Dict) -> Dict[str, Any]:
        """Step 7: Build comprehensive rule matrix combining all constraint types."""
        rule_matrix = {}
        
        # Get all shape names
        all_shapes = set(shape_targets.keys()) | set(cardinality_rules.keys()) | \
                    set(datatype_rules.keys()) | set(pattern_rules.keys())
        
        for shape_name in all_shapes:
            rule_set = {
                'shape_name': shape_name,
                'targets': shape_targets.get(shape_name, {}),
                'cardinality': cardinality_rules.get(shape_name, {}),
                'datatypes': datatype_rules.get(shape_name, {}),
                'patterns': pattern_rules.get(shape_name, {}),
                'profile_type': self._determine_profile_type(shape_name),
                'documentation_priority': self._calculate_documentation_priority(
                    cardinality_rules.get(shape_name, {}),
                    pattern_rules.get(shape_name, {})
                )
            }
            
            rule_matrix[shape_name] = rule_set
        
        return rule_matrix
    
    def _determine_profile_type(self, shape_name: str) -> str:
        """Determine the profile type based on shape name."""
        shape_lower = shape_name.lower()
        
        if 'critical' in shape_lower or 'p0' in shape_lower:
            return 'critical-document'
        elif 'standard' in shape_lower:
            return 'standard-definition'
        elif 'mandatory' in shape_lower:
            return 'mandatory-validation'
        else:
            return 'general-validation'
    
    def _calculate_documentation_priority(self, cardinality_rules: Dict, pattern_rules: Dict) -> int:
        """Calculate documentation priority based on rule complexity."""
        priority = 0
        
        # Higher priority for shapes with many mandatory fields
        priority += len(cardinality_rules.get('mandatory_fields', []))
        
        # Higher priority for shapes with pattern constraints
        priority += len(pattern_rules) * 2
        
        # Higher priority for shapes with forbidden fields
        priority += len(cardinality_rules.get('forbidden_fields', [])) * 3
        
        return priority
    
    def get_profile_summary(self) -> Dict[str, Any]:
        """Get a summary of all profiles found in the SHACL shapes."""
        rules = self.extract_validation_rules()
        
        summary = {
            'total_profiles': len(rules),
            'profile_types': {},
            'field_coverage': {},
            'constraint_complexity': {}
        }
        
        for shape_name, rule_set in rules.items():
            profile_type = rule_set['profile_type']
            summary['profile_types'][profile_type] = summary['profile_types'].get(profile_type, 0) + 1
            
            # Count field coverage
            mandatory_count = len(rule_set['cardinality'].get('mandatory_fields', []))
            forbidden_count = len(rule_set['cardinality'].get('forbidden_fields', []))
            pattern_count = len(rule_set['patterns'])
            
            summary['constraint_complexity'][shape_name] = {
                'mandatory_fields': mandatory_count,
                'forbidden_fields': forbidden_count,
                'pattern_constraints': pattern_count,
                'total_complexity': mandatory_count + forbidden_count + pattern_count
            }
        
        return summary


if __name__ == "__main__":
    # Example usage for testing
    parser = SHACLParser('standards/registry/shacl-shapes.ttl')
    rules = parser.extract_validation_rules()
    
    print(f"Extracted rules for {len(rules)} shapes:")
    for shape_name, rule_set in rules.items():
        print(f"  - {shape_name}: {rule_set['profile_type']}")
    
    summary = parser.get_profile_summary()
    print(f"\nProfile Summary: {summary['total_profiles']} total profiles")
    for profile_type, count in summary['profile_types'].items():
        print(f"  - {profile_type}: {count}")