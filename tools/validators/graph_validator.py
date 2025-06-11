#!/usr/bin/env python3
"""
Knowledge Base Graph Validator
Refactored from kb_linter.py to validate against JSON-LD schema registry

This script:
1. Loads schema-registry.jsonld and checks kb:schemaVersion for compatibility
2. Loads master-index.jsonld
3. Validates every node in the master index against the rules defined in the schema registry
"""

import json
import os
import argparse
import logging
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Supported schema versions
SUPPORTED_SCHEMA_VERSIONS = ["1.0.0"]

class GraphValidator:
    def __init__(self, repo_base_path="."):
        self.repo_base = Path(repo_base_path).resolve()
        self.registry_path = self.repo_base / "standards" / "registry"
        
        # Load schema registry
        self.schema_registry = self._load_schema_registry()
        self.master_index = None
        
        # Extract validation data from schema registry
        self._extract_validation_rules()
        
        # Link validation data
        self.document_lookup = {}  # Maps standard_id to document info
        self.broken_links = []
        
        # Relationship graph data
        self.relationships = []  # List of relationship objects
        self.relationship_graph = {}  # Graph structure for analysis
        
    def _load_schema_registry(self):
        """Load and validate the schema registry."""
        schema_path = self.registry_path / "schema-registry.jsonld"
        
        if not schema_path.exists():
            raise FileNotFoundError(f"Schema registry not found: {schema_path}")
        
        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_data = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            raise ValueError(f"Could not load schema registry: {e}")
        
        # Check schema version compatibility
        schema_version = schema_data.get('kb:schemaVersion')
        if schema_version not in SUPPORTED_SCHEMA_VERSIONS:
            raise ValueError(f"Unsupported schema version: {schema_version}. Supported: {SUPPORTED_SCHEMA_VERSIONS}")
        
        logging.info(f"Loaded schema registry version {schema_version}")
        return schema_data
    
    def _load_master_index(self):
        """Load the master index."""
        index_path = self.registry_path / "master-index.jsonld"
        
        if not index_path.exists():
            raise FileNotFoundError(f"Master index not found: {index_path}")
        
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                self.master_index = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            raise ValueError(f"Could not load master index: {e}")
        
        logging.info(f"Loaded master index with {len(self.master_index.get('kb:documents', []))} documents")
        
        # Build document lookup for link validation
        self._build_document_lookup()
    
    def _extract_validation_rules(self):
        """Extract validation rules from the schema registry."""
        self.field_definitions = {}
        self.controlled_vocabularies = {}
        self.tag_categories = {}
        
        # Extract field definitions
        for field_def in self.schema_registry.get('kb:fieldDefinitions', []):
            field_name = field_def.get('kb:fieldName')
            if field_name:
                self.field_definitions[field_name] = field_def
        
        # Extract controlled vocabularies
        for vocab in self.schema_registry.get('kb:controlledVocabularies', []):
            vocab_name = vocab.get('kb:vocabularyName')
            if vocab_name:
                values = vocab.get('kb:values', [])
                # Extract just the IDs/levels from the vocabulary objects
                if vocab_name in ['primary_domain', 'criticality', 'lifecycle_gatekeeper']:
                    # These have objects with 'id', 'level', or 'gatekeeper' keys
                    if vocab_name == 'primary_domain':
                        self.controlled_vocabularies[vocab_name] = [v.get('id') for v in values if isinstance(v, dict) and 'id' in v]
                    elif vocab_name == 'criticality':
                        self.controlled_vocabularies[vocab_name] = [v.get('level') for v in values if isinstance(v, dict) and 'level' in v]
                    elif vocab_name == 'lifecycle_gatekeeper':
                        self.controlled_vocabularies[vocab_name] = [v.get('gatekeeper') for v in values if isinstance(v, dict) and 'gatekeeper' in v]
                else:
                    # These are simple string lists
                    self.controlled_vocabularies[vocab_name] = values
        
        # Extract tag categories
        for tag_category in self.schema_registry.get('kb:tagCategories', []):
            category_name = tag_category.get('kb:categoryName')
            if category_name:
                self.tag_categories[category_name] = tag_category
        
        logging.debug(f"Extracted {len(self.field_definitions)} field definitions")
        logging.debug(f"Extracted {len(self.controlled_vocabularies)} controlled vocabularies")
        logging.debug(f"Extracted {len(self.tag_categories)} tag categories")
    
    def _build_document_lookup(self):
        """Build a lookup table for document validation."""
        self.document_lookup = {}
        
        for doc in self.master_index.get('kb:documents', []):
            # Index by standard_id if it exists
            standard_id = doc.get('kb:standard_id')
            if standard_id:
                self.document_lookup[standard_id] = {
                    'filepath': doc.get('kb:filepath'),
                    'node_id': doc.get('@id'),
                    'title': doc.get('kb:title', 'Unknown')
                }
            
            # Also index by filepath for reference
            filepath = doc.get('kb:filepath')
            if filepath:
                # Create a pseudo-ID from filepath for documents without standard_id
                if not standard_id:
                    pseudo_id = filepath.replace('/', '-').replace('.md', '').upper()
                    self.document_lookup[pseudo_id] = {
                        'filepath': filepath,
                        'node_id': doc.get('@id'),
                        'title': doc.get('kb:title', 'Unknown')
                    }
        
        logging.debug(f"Built document lookup with {len(self.document_lookup)} entries")
    
    def _extract_internal_links(self, content):
        """Extract internal links in the format [[STANDARD_ID]] from content."""
        if not isinstance(content, str):
            return []
        
        # Pattern for internal links: [[STANDARD_ID]]
        pattern = r'\[\[([A-Z]{2}-[A-Z0-9-]+)\]\]'
        matches = re.findall(pattern, content)
        return matches
    
    def _validate_internal_links(self, doc_node, content):
        """Validate internal links in document content."""
        errors = []
        node_id = doc_node.get('@id', 'unknown')
        filepath = doc_node.get('kb:filepath', 'unknown')
        
        # Extract internal links from content
        internal_links = self._extract_internal_links(content)
        
        for link_target in internal_links:
            if link_target not in self.document_lookup:
                error_msg = f"Broken internal link [[{link_target}]] in document {node_id} ({filepath})"
                errors.append(error_msg)
                self.broken_links.append({
                    'source_document': node_id,
                    'source_filepath': filepath,
                    'target_standard_id': link_target,
                    'link_type': 'internal_content_link'
                })
        
        return errors
    
    def _validate_related_standards(self, doc_node):
        """Validate related-standards field references."""
        errors = []
        node_id = doc_node.get('@id', 'unknown')
        filepath = doc_node.get('kb:filepath', 'unknown')
        
        related_standards = doc_node.get('kb:related_standards')
        if not related_standards:
            return errors
        
        if not isinstance(related_standards, list):
            errors.append(f"Document {node_id}: related-standards must be a list")
            return errors
        
        for standard_ref in related_standards:
            if not isinstance(standard_ref, str):
                errors.append(f"Document {node_id}: related-standards items must be strings, got {type(standard_ref).__name__}")
                continue
            
            # Handle both direct standard IDs and internal link format
            if standard_ref.startswith('[[') and standard_ref.endswith(']]'):
                # Internal link format [[STANDARD_ID]]
                target_id = standard_ref[2:-2]  # Remove [[ and ]]
            else:
                # Direct standard ID
                target_id = standard_ref
            
            # Check if the referenced standard exists
            if target_id not in self.document_lookup:
                error_msg = f"Document {node_id}: related-standards references non-existent standard '{target_id}'"
                errors.append(error_msg)
                self.broken_links.append({
                    'source_document': node_id,
                    'source_filepath': filepath,
                    'target_standard_id': target_id,
                    'link_type': 'related_standards'
                })
        
        return errors
    
    def _validate_field_value(self, field_name, value, field_def):
        """Validate a field value against its definition."""
        errors = []
        
        # Check data type
        expected_type = field_def.get('kb:dataType', 'string')
        if expected_type == 'string' and not isinstance(value, str):
            errors.append(f"Field '{field_name}' should be string, got {type(value).__name__}")
        elif expected_type == 'list_of_strings' and not isinstance(value, list):
            errors.append(f"Field '{field_name}' should be list, got {type(value).__name__}")
        elif expected_type == 'list_of_strings' and isinstance(value, list):
            for item in value:
                if not isinstance(item, str):
                    errors.append(f"Field '{field_name}' list should contain only strings, found {type(item).__name__}")
        
        # Check validation rules
        validation_rules = field_def.get('kb:validationRules', [])
        for rule in validation_rules:
            if isinstance(rule, str):
                if "Must not be empty" in rule and (not value or (isinstance(value, str) and not value.strip())):
                    errors.append(f"Field '{field_name}' must not be empty")
                elif "MUST follow regex pattern:" in rule:
                    # Extract regex pattern from rule
                    pattern_match = re.search(r'MUST follow regex pattern: (.+)$', rule)
                    if pattern_match and isinstance(value, str):
                        pattern = pattern_match.group(1)
                        if not re.match(pattern, value):
                            errors.append(f"Field '{field_name}' does not match required pattern: {pattern}")
                elif "MUST be in ISO-8601 date-time format" in rule and isinstance(value, str):
                    # Basic ISO-8601 validation
                    iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'
                    if not re.match(iso_pattern, value):
                        errors.append(f"Field '{field_name}' must be in ISO-8601 format (YYYY-MM-DDTHH:MM:SSZ)")
        
        # Check controlled vocabulary
        if field_def.get('kb:hasControlledVocabulary') and isinstance(value, str):
            # Find the appropriate controlled vocabulary
            vocab_name = None
            if field_name == 'info-type':
                vocab_name = 'info_type'
            elif field_name == 'criticality':
                vocab_name = 'criticality'
            elif field_name == 'primary_domain':
                vocab_name = 'primary_domain'
            elif field_name == 'sub_domain':
                vocab_name = 'sub_domain'
            elif field_name == 'lifecycle_gatekeeper':
                vocab_name = 'lifecycle_gatekeeper'
            
            if vocab_name and vocab_name in self.controlled_vocabularies:
                valid_values = self.controlled_vocabularies[vocab_name]
                if value not in valid_values:
                    errors.append(f"Field '{field_name}' value '{value}' not in controlled vocabulary: {valid_values}")
        
        return errors
    
    def _validate_tags(self, tags):
        """Validate tags against tag categories."""
        errors = []
        
        if not isinstance(tags, list):
            return ["Tags field must be a list"]
        
        # Check for required tag categories
        required_categories = ['status', 'content-type', 'topic']
        found_categories = set()
        
        for tag in tags:
            if not isinstance(tag, str):
                errors.append(f"Tag must be string, got {type(tag).__name__}: {tag}")
                continue
            
            # Check kebab-case format
            if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*(/[a-z0-9]+(-[a-z0-9]+)*)*$', tag):
                errors.append(f"Tag '{tag}' must be in kebab-case format")
            
            # Check if tag belongs to a known category
            if '/' in tag:
                category = tag.split('/')[0]
                found_categories.add(category)
                
                # Validate against tag categories
                if category in self.tag_categories:
                    tag_category = self.tag_categories[category]
                    valid_tags = [t.get('kb:fullTag', '') for t in tag_category.get('kb:tags', []) if isinstance(t, dict)]
                    if tag not in valid_tags:
                        errors.append(f"Tag '{tag}' not found in category '{category}' vocabulary")
        
        # Check for missing required categories
        for required_cat in required_categories:
            if required_cat not in found_categories:
                errors.append(f"Missing required tag category: {required_cat}/*")
        
        return errors
    
    def _validate_document_node(self, doc_node):
        """Validate a single document node."""
        errors = []
        node_id = doc_node.get('@id', 'unknown')
        filepath = doc_node.get('kb:filepath', 'unknown')
        
        # Validate required JSON-LD structure
        if '@type' not in doc_node:
            errors.append(f"Document {node_id} missing @type")
        elif doc_node['@type'] != 'kb:Document':
            errors.append(f"Document {node_id} has invalid @type: {doc_node['@type']}")
        
        if '@id' not in doc_node:
            errors.append(f"Document {filepath} missing @id")
        
        # Validate against field definitions
        for field_name, field_def in self.field_definitions.items():
            kb_field_name = f"kb:{field_name.replace('-', '_')}"
            
            # Check if field is mandatory
            is_mandatory = field_def.get('kb:mandatory')
            has_field = kb_field_name in doc_node
            
            if is_mandatory is True and not has_field:
                errors.append(f"Document {node_id} missing mandatory field: {field_name}")
            elif is_mandatory == "conditional":
                # Handle conditional mandatory fields
                mandatory_conditions = field_def.get('kb:mandatoryConditions', [])
                for condition in mandatory_conditions:
                    if isinstance(condition, str) and "info-type:" in condition:
                        # Extract required info-types from condition
                        if "standard-definition" in condition or "policy-document" in condition:
                            doc_info_type = doc_node.get('kb:info_type')
                            if doc_info_type in ['standard-definition', 'policy-document'] and not has_field:
                                errors.append(f"Document {node_id} missing conditionally mandatory field: {field_name}")
            
            # Validate field value if present
            if has_field:
                field_value = doc_node[kb_field_name]
                field_errors = self._validate_field_value(field_name, field_value, field_def)
                errors.extend([f"Document {node_id}: {error}" for error in field_errors])
        
        # Special validation for tags
        if 'kb:tags' in doc_node:
            tag_errors = self._validate_tags(doc_node['kb:tags'])
            errors.extend([f"Document {node_id}: {error}" for error in tag_errors])
        
        # Validate related-standards references
        related_standards_errors = self._validate_related_standards(doc_node)
        errors.extend(related_standards_errors)
        
        # Load and validate internal links in document content, and generate relationships
        if filepath != 'unknown':
            try:
                full_filepath = self.repo_base / filepath
                if full_filepath.exists():
                    with open(full_filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    link_errors = self._validate_internal_links(doc_node, content)
                    errors.extend(link_errors)
                    
                    # Generate relationships from validated links
                    self._generate_relationships(doc_node, content)
            except (IOError, UnicodeDecodeError) as e:
                errors.append(f"Document {node_id}: Could not read file for link validation: {e}")
        
        return errors
    
    def _generate_relationships(self, doc_node, content):
        """Generate relationship objects from validated links."""
        node_id = doc_node.get('@id', 'unknown')
        filepath = doc_node.get('kb:filepath', 'unknown')
        source_standard_id = doc_node.get('kb:standard_id')
        
        # Generate relationships from related-standards field
        related_standards = doc_node.get('kb:related_standards')
        if related_standards and isinstance(related_standards, list):
            for standard_ref in related_standards:
                if isinstance(standard_ref, str):
                    # Handle both direct standard IDs and internal link format
                    if standard_ref.startswith('[[') and standard_ref.endswith(']]'):
                        target_id = standard_ref[2:-2]  # Remove [[ and ]]
                    else:
                        target_id = standard_ref
                    
                    # Only create relationship if target exists (avoid broken links)
                    if target_id in self.document_lookup:
                        relationship = {
                            '@type': 'kb:DocumentRelationship',
                            'kb:source': node_id,
                            'kb:target': f"kb:doc-{target_id.replace('-', '-').lower()}",
                            'kb:relationship_type': 'related_standards',
                            'kb:source_standard_id': source_standard_id,
                            'kb:target_standard_id': target_id,
                            'kb:source_filepath': filepath,
                            'kb:target_filepath': self.document_lookup[target_id]['filepath']
                        }
                        self.relationships.append(relationship)
        
        # Generate relationships from internal content links
        internal_links = self._extract_internal_links(content)
        for link_target in internal_links:
            # Only create relationship if target exists (avoid broken links)
            if link_target in self.document_lookup:
                relationship = {
                    '@type': 'kb:DocumentRelationship',
                    'kb:source': node_id,
                    'kb:target': f"kb:doc-{link_target.replace('-', '-').lower()}",
                    'kb:relationship_type': 'internal_content_link',
                    'kb:source_standard_id': source_standard_id,
                    'kb:target_standard_id': link_target,
                    'kb:source_filepath': filepath,
                    'kb:target_filepath': self.document_lookup[link_target]['filepath']
                }
                self.relationships.append(relationship)
    
    def _build_relationship_graph(self):
        """Build a graph structure from relationships for analysis."""
        self.relationship_graph = defaultdict(lambda: {'outgoing': [], 'incoming': []})
        
        for rel in self.relationships:
            source = rel['kb:source']
            target = rel['kb:target']
            rel_type = rel['kb:relationship_type']
            
            # Add to outgoing relationships for source
            self.relationship_graph[source]['outgoing'].append({
                'target': target,
                'type': rel_type,
                'target_standard_id': rel.get('kb:target_standard_id'),
                'target_filepath': rel.get('kb:target_filepath')
            })
            
            # Add to incoming relationships for target
            self.relationship_graph[target]['incoming'].append({
                'source': source,
                'type': rel_type,
                'source_standard_id': rel.get('kb:source_standard_id'),
                'source_filepath': rel.get('kb:source_filepath')
            })
    
    def _analyze_relationship_graph(self):
        """Analyze the relationship graph for insights."""
        analysis = {
            'total_relationships': len(self.relationships),
            'total_nodes_with_relationships': len(self.relationship_graph),
            'relationship_types': dict(defaultdict(int)),
            'most_referenced_documents': [],
            'most_referencing_documents': [],
            'isolated_documents': []
        }
        
        # Count relationship types
        type_counts = defaultdict(int)
        for rel in self.relationships:
            type_counts[rel['kb:relationship_type']] += 1
        analysis['relationship_types'] = dict(type_counts)
        
        # Find most referenced documents (highest incoming)
        incoming_counts = []
        for node_id, data in self.relationship_graph.items():
            incoming_count = len(data['incoming'])
            if incoming_count > 0:
                incoming_counts.append((node_id, incoming_count))
        
        incoming_counts.sort(key=lambda x: x[1], reverse=True)
        analysis['most_referenced_documents'] = incoming_counts[:10]
        
        # Find most referencing documents (highest outgoing)
        outgoing_counts = []
        for node_id, data in self.relationship_graph.items():
            outgoing_count = len(data['outgoing'])
            if outgoing_count > 0:
                outgoing_counts.append((node_id, outgoing_count))
        
        outgoing_counts.sort(key=lambda x: x[1], reverse=True)
        analysis['most_referencing_documents'] = outgoing_counts[:10]
        
        # Find isolated documents (no relationships)
        all_documents = set(doc.get('@id') for doc in self.master_index.get('kb:documents', []))
        connected_documents = set(self.relationship_graph.keys())
        analysis['isolated_documents'] = list(all_documents - connected_documents)
        
        return analysis
    
    def validate_all_documents(self):
        """Validate all documents in the master index."""
        if self.master_index is None:
            self._load_master_index()
        
        all_errors = []
        documents = self.master_index.get('kb:documents', [])
        
        logging.info(f"Validating {len(documents)} documents...")
        
        for i, doc_node in enumerate(documents):
            doc_errors = self._validate_document_node(doc_node)
            all_errors.extend(doc_errors)
            
            if (i + 1) % 10 == 0:
                logging.debug(f"Validated {i + 1}/{len(documents)} documents")
        
        # Build and analyze relationship graph after all documents are processed
        logging.info("Building relationship graph...")
        self._build_relationship_graph()
        
        logging.info("Analyzing relationship graph...")
        self.graph_analysis = self._analyze_relationship_graph()
        
        logging.info(f"Generated {len(self.relationships)} relationships between {len(self.relationship_graph)} documents")
        
        return all_errors
    
    def generate_validation_report(self, errors):
        """Generate a validation report."""
        report = {
            "validation_timestamp": datetime.now().isoformat(),
            "schema_version": self.schema_registry.get('kb:schemaVersion'),
            "total_documents": len(self.master_index.get('kb:documents', [])),
            "total_errors": len(errors),
            "total_broken_links": len(self.broken_links),
            "errors": errors,
            "broken_links": self.broken_links,
            "link_validation_summary": {
                "internal_content_links": len([link for link in self.broken_links if link['link_type'] == 'internal_content_link']),
                "related_standards_links": len([link for link in self.broken_links if link['link_type'] == 'related_standards'])
            },
            "relationship_graph": {
                "relationships": self.relationships,
                "analysis": getattr(self, 'graph_analysis', {})
            }
        }
        
        return report

def main():
    parser = argparse.ArgumentParser(description="Knowledge Base Graph Validator")
    parser.add_argument("--repo-base", default=".", 
                        help="Path to the repository root. Default is current directory.")
    parser.add_argument("--log-level", default="INFO", 
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="Set the logging level (default: INFO).")
    parser.add_argument("--output-report", 
                        help="Path to save validation report JSON file.")

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=getattr(logging, args.log_level.upper()),
                        format='%(levelname)s: %(message)s')

    try:
        # Initialize validator
        logging.info("Initializing Graph Validator...")
        validator = GraphValidator(args.repo_base)
        
        # Validate all documents
        logging.info("Starting validation...")
        errors = validator.validate_all_documents()
        
        # Generate report
        report = validator.generate_validation_report(errors)
        
        # Output results
        if errors:
            logging.error(f"Validation completed with {len(errors)} errors:")
            for error in errors[:10]:  # Show first 10 errors
                logging.error(f"  - {error}")
            if len(errors) > 10:
                logging.error(f"  ... and {len(errors) - 10} more errors")
        else:
            logging.info("Validation completed successfully with no errors!")
        
        # Report broken links separately
        if validator.broken_links:
            logging.warning(f"Found {len(validator.broken_links)} broken links:")
            for link in validator.broken_links[:5]:  # Show first 5 broken links
                logging.warning(f"  - {link['link_type']}: [[{link['target_standard_id']}]] in {link['source_filepath']}")
            if len(validator.broken_links) > 5:
                logging.warning(f"  ... and {len(validator.broken_links) - 5} more broken links")
        else:
            logging.info("No broken links found!")
        
        # Report relationship graph information
        if hasattr(validator, 'graph_analysis'):
            analysis = validator.graph_analysis
            logging.info(f"Relationship Graph Analysis:")
            logging.info(f"  - Total relationships: {analysis.get('total_relationships', 0)}")
            logging.info(f"  - Connected documents: {analysis.get('total_nodes_with_relationships', 0)}")
            logging.info(f"  - Isolated documents: {len(analysis.get('isolated_documents', []))}")
            
            rel_types = analysis.get('relationship_types', {})
            if rel_types:
                logging.info(f"  - Relationship types: {dict(rel_types)}")
            
            most_referenced = analysis.get('most_referenced_documents', [])
            if most_referenced:
                top_ref = most_referenced[0]
                logging.info(f"  - Most referenced document: {top_ref[0]} ({top_ref[1]} incoming links)")
        else:
            logging.warning("Relationship graph analysis not available")
        
        # Save report if requested
        if args.output_report:
            with open(args.output_report, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            logging.info(f"Validation report saved to: {args.output_report}")
        
        # Return appropriate exit code
        return 1 if errors else 0
        
    except Exception as e:
        logging.error(f"Validation failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 