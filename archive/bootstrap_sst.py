#!/usr/bin/env python3
"""
Bootstrap Script for JSON-LD SST Migration
Converts legacy YAML SSTs to JSON-LD format

This script reads:
- standards/registry/mt-schema-frontmatter.yaml
- standards/registry/mt-registry-tag-glossary.yaml

And generates:
- standards/registry/schema-registry.jsonld
- standards/registry/contexts/fields.jsonld
"""

import yaml
import json
import os
from datetime import datetime
from pathlib import Path

def load_yaml_file(filepath):
    """Load and parse a YAML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

def create_fields_context(frontmatter_schema):
    """Create the fields.jsonld context from frontmatter schema"""
    context = {
        "@context": {
            "kb": "https://knowledge-base.local/vocab#",
            "schema": "https://schema.org/",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
        }
    }
    
    # Add field definitions from the schema
    fields = frontmatter_schema.get('fields', {})
    for field_name, field_def in fields.items():
        # Convert field names to kb: namespace
        kb_field = f"kb:{field_name.replace('-', '_')}"
        
        # Determine data type mapping
        data_type = field_def.get('data_type', 'string')
        if data_type == 'string':
            context["@context"][kb_field] = {"@type": "xsd:string"}
        elif data_type == 'list_of_strings':
            context["@context"][kb_field] = {"@type": "@id", "@container": "@list"}
        else:
            context["@context"][kb_field] = {"@type": "xsd:string"}
    
    return context

def create_schema_registry(frontmatter_schema, tag_glossary):
    """Create the main schema-registry.jsonld file"""
    registry = {
        "@context": [
            "contexts/base.jsonld",
            "contexts/fields.jsonld"
        ],
        "@type": "kb:SchemaRegistry",
        "@id": "kb:schema-registry",
        "kb:schemaVersion": "1.0.0",
        "kb:title": "Knowledge Base Schema Registry",
        "kb:description": "Unified JSON-LD schema registry for the knowledge base system",
        "kb:created": datetime.now().isoformat() + "Z",
        "kb:modified": datetime.now().isoformat() + "Z",
        "kb:version": "1.0.0",
        "kb:status": "active"
    }
    
    # Add field definitions
    registry["kb:fieldDefinitions"] = []
    fields = frontmatter_schema.get('fields', {})
    for field_name, field_def in fields.items():
        field_entry = {
            "@type": "kb:FieldDefinition",
            "@id": f"kb:field-{field_name.replace('-', '_')}",
            "kb:fieldName": field_name,
            "kb:description": field_def.get('description', ''),
            "kb:mandatory": field_def.get('mandatory', False),
            "kb:dataType": field_def.get('data_type', 'string'),
            "kb:validationRules": field_def.get('validation_rules', [])
        }
        
        # Add controlled vocabulary if present
        if field_def.get('controlled_vocabulary'):
            field_entry["kb:hasControlledVocabulary"] = True
            
        # Add mandatory conditions if present
        if field_def.get('mandatory_conditions'):
            field_entry["kb:mandatoryConditions"] = field_def.get('mandatory_conditions', [])
            
        registry["kb:fieldDefinitions"].append(field_entry)
    
    # Add controlled vocabularies
    registry["kb:controlledVocabularies"] = []
    controlled_vocabs = frontmatter_schema.get('controlled_vocabularies', {})
    for vocab_name, vocab_values in controlled_vocabs.items():
        vocab_entry = {
            "@type": "kb:ControlledVocabulary",
            "@id": f"kb:vocab-{vocab_name.replace('_', '-')}",
            "kb:vocabularyName": vocab_name,
            "kb:values": vocab_values if isinstance(vocab_values, list) else []
        }
        registry["kb:controlledVocabularies"].append(vocab_entry)
    
    # Add tag categories from tag glossary
    registry["kb:tagCategories"] = []
    tag_categories = tag_glossary.get('tag_categories', {})
    for category_name, category_def in tag_categories.items():
        category_entry = {
            "@type": "kb:TagCategory",
            "@id": f"kb:tag-category-{category_name}",
            "kb:categoryName": category_name,
            "kb:prefix": category_def.get('prefix', ''),
            "kb:description": category_def.get('description', ''),
            "kb:tags": []
        }
        
        # Add individual tags
        tags = category_def.get('tags', [])
        for tag in tags:
            tag_entry = {
                "@type": "kb:Tag",
                "@id": f"kb:tag-{tag.get('id', '')}",
                "kb:tagId": tag.get('id', ''),
                "kb:fullTag": tag.get('full_tag', ''),
                "kb:description": tag.get('description', '')
            }
            if 'field_value' in tag:
                tag_entry["kb:fieldValue"] = tag['field_value']
            category_entry["kb:tags"].append(tag_entry)
            
        registry["kb:tagCategories"].append(category_entry)
    
    # Add field order
    field_order = frontmatter_schema.get('field_order', [])
    if field_order:
        registry["kb:fieldOrder"] = field_order
    
    return registry

def main():
    """Main execution function"""
    print("Starting JSON-LD SST Bootstrap Migration...")
    
    # Define file paths
    base_dir = Path(__file__).parent.parent.parent
    frontmatter_yaml = base_dir / "standards" / "registry" / "mt-schema-frontmatter.yaml"
    tag_glossary_yaml = base_dir / "standards" / "registry" / "mt-registry-tag-glossary.yaml"
    
    schema_registry_output = base_dir / "standards" / "registry" / "schema-registry.jsonld"
    fields_context_output = base_dir / "standards" / "registry" / "contexts" / "fields.jsonld"
    
    # Load YAML files
    print(f"Loading {frontmatter_yaml}...")
    frontmatter_schema = load_yaml_file(frontmatter_yaml)
    if not frontmatter_schema:
        print("Failed to load frontmatter schema. Exiting.")
        return False
    
    print(f"Loading {tag_glossary_yaml}...")
    tag_glossary = load_yaml_file(tag_glossary_yaml)
    if not tag_glossary:
        print("Failed to load tag glossary. Exiting.")
        return False
    
    # Create JSON-LD structures
    print("Creating fields context...")
    fields_context = create_fields_context(frontmatter_schema)
    
    print("Creating schema registry...")
    schema_registry = create_schema_registry(frontmatter_schema, tag_glossary)
    
    # Write output files
    print(f"Writing {fields_context_output}...")
    os.makedirs(fields_context_output.parent, exist_ok=True)
    with open(fields_context_output, 'w', encoding='utf-8') as f:
        json.dump(fields_context, f, indent=2, ensure_ascii=False)
    
    print(f"Writing {schema_registry_output}...")
    with open(schema_registry_output, 'w', encoding='utf-8') as f:
        json.dump(schema_registry, f, indent=2, ensure_ascii=False)
    
    print("Bootstrap migration completed successfully!")
    print(f"Generated files:")
    print(f"  - {fields_context_output}")
    print(f"  - {schema_registry_output}")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 