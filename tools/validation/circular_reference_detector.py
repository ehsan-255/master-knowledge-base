#!/usr/bin/env python3
"""
Circular Reference Detector

Identifies self-referencing and navigation loops in Standards Knowledge Base documents.
Ensures architectural integrity and prevents infinite reference loops.

Author: AI Development Team
Date: 2025-06-18
Purpose: Tactical redundancy elimination and prevention
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any
from datetime import datetime
from collections import defaultdict, deque

class CircularReferenceDetector:
    """Detects circular references and self-referencing in standards documents."""
    
    def __init__(self, standards_dir: str = "standards/src"):
        self.standards_dir = Path(standards_dir)
        self.root_dir = Path.cwd()
        self.errors = []
        self.warnings = []
        self.reference_graph = defaultdict(set)
        
    def validate_all(self) -> Dict[str, Any]:
        """Run comprehensive circular reference detection."""
        print("🔍 Starting Circular Reference Detection...")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "validation_type": "circular_reference_detection",
            "errors": [],
            "warnings": [],
            "summary": {}
        }
        
        # Build reference graph
        self._build_reference_graph()
        
        # Detect circular references
        self._detect_circular_references()
        
        # Check for self-references
        self._detect_self_references()
        
        # Validate architectural layer separation
        self._validate_architectural_layers()
        
        # Compile results
        results["errors"] = self.errors
        results["warnings"] = self.warnings
        results["summary"] = {
            "total_errors": len(self.errors),
            "total_warnings": len(self.warnings),
            "status": "PASS" if len(self.errors) == 0 else "FAIL",
            "reference_count": sum(len(refs) for refs in self.reference_graph.values()),
            "documents_analyzed": len(self.reference_graph)
        }
        
        return results
    
    def _build_reference_graph(self) -> None:
        """Build a graph of all cross-references between documents."""
        print("📊 Building reference graph...")
        
        for file_path in self.standards_dir.glob("*.md"):
            document_id = file_path.stem
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract references using various patterns
                references = self._extract_references(content)
                self.reference_graph[document_id] = references
                
                print(f"   📄 {document_id}: {len(references)} references found")
                
            except Exception as e:
                self.warnings.append(f"Failed to read {file_path}: {str(e)}")
    
    def _extract_references(self, content: str) -> Set[str]:
        """Extract all standard references from document content."""
        references = set()
        
        # Pattern 1: [[STANDARD_ID]] or [[STANDARD_ID|Description]]
        pattern1 = r'\[\[([A-Z]{2}-[A-Z-]+)(?:\|[^\]]+)?\]\]'
        matches1 = re.findall(pattern1, content)
        references.update(matches1)
        
        # Pattern 2: related-standards in frontmatter
        yaml_pattern = r'related-standards:\s*\n((?:\s*-\s*[A-Z]{2}-[A-Z-]+\s*\n)*)'
        yaml_matches = re.findall(yaml_pattern, content, re.MULTILINE)
        for match in yaml_matches:
            standard_refs = re.findall(r'-\s*([A-Z]{2}-[A-Z-]+)', match)
            references.update(standard_refs)
        
        # Pattern 3: Direct mentions in text
        pattern3 = r'`([A-Z]{2}-[A-Z-]+)`'
        matches3 = re.findall(pattern3, content)
        references.update(matches3)
        
        return references
    
    def _detect_circular_references(self) -> None:
        """Detect circular reference chains using DFS."""
        print("🔄 Detecting circular references...")
        
        visited = set()
        rec_stack = set()
        
        def dfs(node: str, path: List[str]) -> None:
            if node in rec_stack:
                # Found a cycle
                cycle_start = path.index(node)
                cycle = path[cycle_start:] + [node]
                self.errors.append(f"Circular reference detected: {' -> '.join(cycle)}")
                return
            
            if node in visited:
                return
            
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in self.reference_graph.get(node, []):
                if neighbor in self.reference_graph:  # Only follow if target exists
                    dfs(neighbor, path.copy())
            
            rec_stack.remove(node)
        
        for document in self.reference_graph:
            if document not in visited:
                dfs(document, [])
    
    def _detect_self_references(self) -> None:
        """Detect documents that reference themselves."""
        print("🪞 Detecting self-references...")
        
        for document_id, references in self.reference_graph.items():
            if document_id in references:
                self.errors.append(f"Self-reference detected: {document_id} references itself")
    
    def _validate_architectural_layers(self) -> None:
        """Validate three-layer architectural separation."""
        print("🏗️ Validating architectural layer separation...")
        
        # Define architectural layers
        layers = {
            "physical": ["AS-KB-DIRECTORY-STRUCTURE"],
            "logical": ["AS-MAP-STANDARDS-KB"],
            "presentation": ["AS-ROOT-STANDARDS-KB"]
        }
        
        # Check for inappropriate cross-layer references
        for layer_name, layer_docs in layers.items():
            for doc in layer_docs:
                if doc in self.reference_graph:
                    references = self.reference_graph[doc]
                    
                    # Check for self-references within the same layer function
                    for other_layer_name, other_layer_docs in layers.items():
                        if layer_name != other_layer_name:
                            inappropriate_refs = references.intersection(set(other_layer_docs))
                            if inappropriate_refs:
                                for ref in inappropriate_refs:
                                    self.warnings.append(
                                        f"Cross-layer reference: {doc} ({layer_name}) -> {ref} ({other_layer_name})"
                                    )
        
        # Specific check for AS-ROOT-STANDARDS-KB referencing AS-STRUCTURE-KB-ROOT
        if "AS-ROOT-STANDARDS-KB" in self.reference_graph:
            if "AS-STRUCTURE-KB-ROOT" in self.reference_graph["AS-ROOT-STANDARDS-KB"]:
                self.errors.append(
                    "Architectural violation: AS-ROOT-STANDARDS-KB should not reference AS-STRUCTURE-KB-ROOT"
                )
    
    def _find_reference_chains(self, max_depth: int = 5) -> List[List[str]]:
        """Find reference chains that might indicate problematic dependencies."""
        chains = []
        
        def find_chains_from_node(node: str, current_chain: List[str], depth: int):
            if depth > max_depth:
                return
            
            if node in current_chain:
                # Found a cycle
                return
            
            current_chain.append(node)
            
            for reference in self.reference_graph.get(node, []):
                if reference in self.reference_graph:
                    find_chains_from_node(reference, current_chain.copy(), depth + 1)
            
            if len(current_chain) > 2:  # Only report non-trivial chains
                chains.append(current_chain.copy())
        
        for document in self.reference_graph:
            find_chains_from_node(document, [], 0)
        
        return chains
    
    def generate_report(self, results: Dict[str, Any], output_file: str = None) -> str:
        """Generate a formatted validation report."""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M")
            output_file = f"tools/reports/circular-reference-detection-{timestamp}.md"
        
        report_content = f"""---
title: 'Circular Reference Detection Report'
date-created: '{results["timestamp"]}'
validation-type: '{results["validation_type"]}'
status: '{results["summary"]["status"]}'
---

# Circular Reference Detection Report

## Executive Summary

**Validation Status:** {results["summary"]["status"]}
**Total Errors:** {results["summary"]["total_errors"]}
**Total Warnings:** {results["summary"]["total_warnings"]}
**Documents Analyzed:** {results["summary"]["documents_analyzed"]}
**Total References:** {results["summary"]["reference_count"]}
**Validation Date:** {results["timestamp"]}

## Errors Found

"""
        
        if results["errors"]:
            for i, error in enumerate(results["errors"], 1):
                report_content += f"{i}. ❌ **ERROR:** {error}\n"
        else:
            report_content += "✅ **No circular references found!**\n"
        
        report_content += "\n## Warnings Found\n\n"
        
        if results["warnings"]:
            for i, warning in enumerate(results["warnings"], 1):
                report_content += f"{i}. ⚠️ **WARNING:** {warning}\n"
        else:
            report_content += "✅ **No architectural warnings found!**\n"
        
        # Add reference graph summary
        report_content += f"""

## Reference Graph Analysis

### Most Referenced Documents
"""
        
        # Calculate most referenced documents
        reference_counts = defaultdict(int)
        for doc, refs in self.reference_graph.items():
            for ref in refs:
                reference_counts[ref] += 1
        
        sorted_refs = sorted(reference_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        for doc, count in sorted_refs:
            report_content += f"- **{doc}:** {count} references\n"
        
        report_content += f"""

### Documents with Most Outgoing References
"""
        
        sorted_outgoing = sorted(
            [(doc, len(refs)) for doc, refs in self.reference_graph.items()], 
            key=lambda x: x[1], reverse=True
        )[:10]
        
        for doc, count in sorted_outgoing:
            report_content += f"- **{doc}:** {count} outgoing references\n"
        
        report_content += f"""

## Validation Details

- **Reference Patterns Detected:**
  - `[[STANDARD_ID]]` and `[[STANDARD_ID|Description]]`
  - `related-standards` in YAML frontmatter
  - Direct mentions in backticks
- **Architectural Layers Validated:**
  - Physical Layer: AS-KB-DIRECTORY-STRUCTURE
  - Logical Layer: AS-MAP-STANDARDS-KB  
  - Presentation Layer: AS-ROOT-STANDARDS-KB
- **Detection Methods:**
  - Depth-First Search for cycles
  - Self-reference detection
  - Cross-layer reference validation

## Recommendations

"""
        
        if results["summary"]["status"] == "FAIL":
            report_content += "🚨 **IMMEDIATE ACTION REQUIRED:** Circular references detected that could cause infinite loops.\n\n"
        else:
            report_content += "✅ **Reference architecture validated successfully.**\n\n"
        
        report_content += """
## Next Steps

1. **Fix circular references immediately** to prevent infinite loops
2. **Review architectural layer violations** for proper separation
3. **Monitor reference patterns** for complexity management
4. **Implement automated checks** in development workflow

---
*Generated by Circular Reference Detector*
"""
        
        # Write report file
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return output_file

def main():
    """Main execution function."""
    detector = CircularReferenceDetector()
    results = detector.validate_all()
    
    # Generate report
    report_file = detector.generate_report(results)
    
    # Print summary
    print("\n" + "="*60)
    print("🔄 CIRCULAR REFERENCE DETECTION COMPLETE")
    print("="*60)
    print(f"Status: {results['summary']['status']}")
    print(f"Errors: {results['summary']['total_errors']}")
    print(f"Warnings: {results['summary']['total_warnings']}")
    print(f"Documents: {results['summary']['documents_analyzed']}")
    print(f"References: {results['summary']['reference_count']}")
    print(f"Report: {report_file}")
    
    if results['summary']['status'] == "FAIL":
        print("\n🚨 ACTION REQUIRED: Circular references detected!")
        for error in results['errors']:
            print(f"   ❌ {error}")
    else:
        print("\n✅ No circular references found!")
    
    return results['summary']['total_errors']

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code) 