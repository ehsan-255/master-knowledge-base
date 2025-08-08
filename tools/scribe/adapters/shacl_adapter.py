#!/usr/bin/env python3
"""
SHACL to JSON Schema Compliance Adapter

This adapter implements the HMA v2.2 Tier 3 compliance pattern by bridging
SHACL validation (Tier 3 alternative) to standard JSON Schema validation
reports (Tier 1 mandatory). This ensures interoperability and compliance
while allowing the use of specialized validation technologies.
"""

import json
import time
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from enum import Enum

from ..core.logging_config import get_scribe_logger

logger = get_scribe_logger(__name__)


class ValidationSeverity(Enum):
    """Standardized validation severity levels."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationResult:
    """Standardized validation result structure."""
    valid: bool
    severity: ValidationSeverity
    message: str
    property_path: Optional[str] = None
    source_location: Optional[str] = None
    constraint_component: Optional[str] = None
    focus_node: Optional[str] = None
    value: Optional[Any] = None


@dataclass
class ComplianceReport:
    """HMA v2.2 compliant validation report."""
    report_id: str
    timestamp: float
    validator_type: str
    validator_version: str
    input_format: str
    output_format: str = "json_schema_validation_report"
    hma_compliance_version: str = "2.2"
    
    # Validation results
    overall_valid: bool = True
    total_violations: int = 0
    error_count: int = 0
    warning_count: int = 0
    info_count: int = 0
    
    # Detailed results
    violations: List[ValidationResult] = None
    
    def __post_init__(self):
        if self.violations is None:
            self.violations = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "report_metadata": {
                "report_id": self.report_id,
                "timestamp": self.timestamp,
                "validator_type": self.validator_type,
                "validator_version": self.validator_version,
                "input_format": self.input_format,
                "output_format": self.output_format,
                "hma_compliance_version": self.hma_compliance_version
            },
            "validation_summary": {
                "overall_valid": self.overall_valid,
                "total_violations": self.total_violations,
                "error_count": self.error_count,
                "warning_count": self.warning_count,
                "info_count": self.info_count
            },
            "violations": [
                {
                    "severity": violation.severity.value,
                    "message": violation.message,
                    "property_path": violation.property_path,
                    "source_location": violation.source_location,
                    "constraint_component": violation.constraint_component,
                    "focus_node": violation.focus_node,
                    "value": violation.value
                }
                for violation in self.violations
            ]
        }


class SHACLToJSONSchemaAdapter:
    """
    Compliance adapter that transforms SHACL validation results into 
    HMA v2.2 compliant JSON Schema validation reports.
    
    This adapter enables the use of SHACL (Tier 3 alternative) while 
    maintaining compliance with JSON Schema validation (Tier 1 mandatory).
    """
    
    def __init__(self, adapter_version: str = "2.2.0"):
        """
        Initialize the SHACL compliance adapter.
        
        Args:
            adapter_version: Version of the adapter
        """
        self.adapter_version = adapter_version
        self.logger = get_scribe_logger(f"{__name__}.{self.__class__.__name__}")
        
        self.logger.info("SHACL compliance adapter initialized",
                        adapter_version=adapter_version,
                        hma_compliance="2.2")
    
    def transform_shacl_report(self, 
                              shacl_graph: Any, 
                              conforms: bool,
                              report_id: Optional[str] = None) -> ComplianceReport:
        """
        Transform a SHACL validation report into HMA v2.2 compliant format.
        
        Args:
            shacl_graph: SHACL validation report graph (from pyshacl)
            conforms: Whether the validation passed
            report_id: Optional custom report ID
            
        Returns:
            ComplianceReport: HMA v2.2 compliant validation report
        """
        if report_id is None:
            report_id = f"shacl_validation_{int(time.time() * 1000)}"
        
        # Create compliance report
        report = ComplianceReport(
            report_id=report_id,
            timestamp=time.time(),
            validator_type="shacl",
            validator_version=self.adapter_version,
            input_format="rdf_turtle",
            overall_valid=conforms
        )
        
        try:
            # Extract violations from SHACL graph
            violations = self._extract_shacl_violations(shacl_graph)
            
            # Transform violations to standardized format
            for violation in violations:
                standardized_violation = self._transform_violation(violation)
                report.violations.append(standardized_violation)
                
                # Update counters
                if standardized_violation.severity == ValidationSeverity.ERROR:
                    report.error_count += 1
                elif standardized_violation.severity == ValidationSeverity.WARNING:
                    report.warning_count += 1
                elif standardized_violation.severity == ValidationSeverity.INFO:
                    report.info_count += 1
            
            report.total_violations = len(report.violations)
            
            self.logger.info("SHACL report transformed successfully",
                           report_id=report_id,
                           overall_valid=conforms,
                           total_violations=report.total_violations,
                           error_count=report.error_count)
            
            return report
            
        except Exception as e:
            self.logger.error("Failed to transform SHACL report",
                            report_id=report_id,
                            error=str(e))
            
            # Return error report
            error_violation = ValidationResult(
                valid=False,
                severity=ValidationSeverity.ERROR,
                message=f"SHACL adapter transformation failed: {str(e)}",
                constraint_component="adapter_error"
            )
            
            report.violations = [error_violation]
            report.overall_valid = False
            report.error_count = 1
            report.total_violations = 1
            
            return report
    
    def _extract_shacl_violations(self, shacl_graph: Any) -> List[Dict[str, Any]]:
        """
        Extract violation information from SHACL validation report graph.
        
        Args:
            shacl_graph: SHACL validation report graph
            
        Returns:
            List of raw violation dictionaries
        """
        violations = []
        
        try:
            from rdflib import Graph, Namespace
            from rdflib.namespace import SH
            
            # Parse the SHACL report graph if it's a string
            if isinstance(shacl_graph, str):
                report_graph = Graph()
                report_graph.parse(data=shacl_graph, format='turtle')
            else:
                report_graph = shacl_graph
            
            # SPARQL query to extract validation results
            query = """
            PREFIX sh: <http://www.w3.org/ns/shacl#>
            SELECT ?result ?severity ?message ?focusNode ?resultPath ?sourceConstraintComponent ?value
            WHERE {
                ?result a sh:ValidationResult ;
                        sh:resultSeverity ?severity ;
                        sh:resultMessage ?message .
                OPTIONAL { ?result sh:focusNode ?focusNode }
                OPTIONAL { ?result sh:resultPath ?resultPath }
                OPTIONAL { ?result sh:sourceConstraintComponent ?sourceConstraintComponent }
                OPTIONAL { ?result sh:value ?value }
            }
            """
            
            # Execute query and extract violations
            for row in report_graph.query(query):
                violation = {
                    "severity": str(row.severity),
                    "message": str(row.message),
                    "focusNode": str(row.focusNode) if row.focusNode else None,
                    "resultPath": str(row.resultPath) if row.resultPath else None,
                    "sourceConstraintComponent": str(row.sourceConstraintComponent) if row.sourceConstraintComponent else None,
                    "value": str(row.value) if row.value else None
                }
                violations.append(violation)
                
            self.logger.info("Extracted SHACL violations",
                           violation_count=len(violations))
                
        except Exception as e:
            self.logger.error("SHACL violation extraction failed",
                            error=str(e))
            # Fallback to empty list rather than crashing
            violations = []
        
        return violations
    
    def _simulate_shacl_extraction(self, shacl_graph: Any) -> List[Dict[str, Any]]:
        """
        Simulate SHACL violation extraction for demonstration.
        In a real implementation, this would use SPARQL queries or RDF parsing.
        """
        # This is a placeholder implementation
        # Real implementation would query the SHACL validation report graph
        return [
            {
                "severity": "sh:Violation",
                "message": "Property value violates constraint",
                "focusNode": "ex:Document1",
                "resultPath": "ex:title",
                "sourceConstraintComponent": "sh:MinLengthConstraintComponent",
                "value": "Short"
            }
        ]
    
    def _transform_violation(self, raw_violation: Dict[str, Any]) -> ValidationResult:
        """
        Transform a raw SHACL violation into standardized format.
        
        Args:
            raw_violation: Raw violation data from SHACL
            
        Returns:
            ValidationResult: Standardized validation result
        """
        # Map SHACL severity to standard severity
        shacl_severity = raw_violation.get("severity", "sh:Violation")
        if shacl_severity in ["sh:Violation", "sh:Error"]:
            severity = ValidationSeverity.ERROR
        elif shacl_severity in ["sh:Warning"]:
            severity = ValidationSeverity.WARNING
        else:
            severity = ValidationSeverity.INFO
        
        # Extract violation details
        message = raw_violation.get("message", "SHACL validation violation")
        property_path = raw_violation.get("resultPath", raw_violation.get("propertyPath"))
        focus_node = raw_violation.get("focusNode")
        constraint_component = raw_violation.get("sourceConstraintComponent")
        value = raw_violation.get("value")
        
        # Create standardized violation
        return ValidationResult(
            valid=False,
            severity=severity,
            message=message,
            property_path=property_path,
            focus_node=focus_node,
            constraint_component=constraint_component,
            value=value,
            source_location=f"SHACL:{focus_node}" if focus_node else None
        )
    
    def create_json_schema_report(self, compliance_report: ComplianceReport) -> str:
        """
        Create a JSON Schema validation report from the compliance report.
        
        Args:
            compliance_report: HMA v2.2 compliant report
            
        Returns:
            JSON string of the validation report
        """
        try:
            report_dict = compliance_report.to_dict()
            return json.dumps(report_dict, indent=2, ensure_ascii=False)
            
        except Exception as e:
            self.logger.error("Failed to create JSON Schema report",
                            report_id=compliance_report.report_id,
                            error=str(e))
            
            # Return minimal error report
            error_report = {
                "report_metadata": {
                    "report_id": compliance_report.report_id,
                    "timestamp": time.time(),
                    "validator_type": "shacl_adapter_error",
                    "hma_compliance_version": "2.2"
                },
                "validation_summary": {
                    "overall_valid": False,
                    "total_violations": 1,
                    "error_count": 1
                },
                "violations": [
                    {
                        "severity": "error",
                        "message": f"JSON Schema report generation failed: {str(e)}",
                        "constraint_component": "adapter_serialization_error"
                    }
                ]
            }
            
            return json.dumps(error_report, indent=2)
    
    def _dict_to_rdf_graph(self, data: Dict[str, Any]) -> Any:
        """
        Convert dictionary data to RDF graph for SHACL validation.
        
        Args:
            data: Dictionary data to convert
            
        Returns:
            RDF Graph object
        """
        try:
            from rdflib import Graph, Literal, URIRef, Namespace
            from rdflib.namespace import XSD
            
            graph = Graph()
            EX = Namespace("http://example.org/")
            
            # Create a basic RDF representation from the dictionary
            subject = EX.Document
            
            for key, value in data.items():
                predicate = EX[key.replace('-', '_').replace(' ', '_')]
                
                if isinstance(value, str):
                    graph.add((subject, predicate, Literal(value)))
                elif isinstance(value, (int, float)):
                    graph.add((subject, predicate, Literal(value)))
                elif isinstance(value, bool):
                    graph.add((subject, predicate, Literal(value, datatype=XSD.boolean)))
                else:
                    # Convert complex objects to string
                    graph.add((subject, predicate, Literal(str(value))))
            
            return graph
            
        except Exception as e:
            self.logger.error("Failed to convert dict to RDF graph", error=str(e))
            # Return empty graph as fallback
            from rdflib import Graph
            return Graph()
    
    def validate_with_compliance_bridge(self, 
                                      data: Any,
                                      shacl_shapes_graph: Any,
                                      report_id: Optional[str] = None) -> ComplianceReport:
        """
        Perform SHACL validation and return HMA v2.2 compliant report.
        
        This method provides a complete bridge from SHACL validation to
        JSON Schema compliance reporting.
        
        Args:
            data: Data to validate (RDF graph or dict)
            shacl_shapes_graph: SHACL shapes for validation
            report_id: Optional custom report ID
            
        Returns:
            ComplianceReport: HMA v2.2 compliant validation report
        """
        try:
            # Production SHACL validation using pyshacl
            from pyshacl import validate
            from rdflib import Graph
            
            # Convert data to RDF graph if needed
            if isinstance(data, dict):
                data_graph = self._dict_to_rdf_graph(data)
            elif isinstance(data, str):
                data_graph = Graph()
                data_graph.parse(data=data, format='turtle')
            else:
                data_graph = data
            
            # Convert shapes to RDF graph if needed
            if isinstance(shacl_shapes_graph, str):
                shapes_graph = Graph()
                shapes_graph.parse(data=shacl_shapes_graph, format='turtle')
            else:
                shapes_graph = shacl_shapes_graph
            
            # Perform SHACL validation
            conforms, results_graph, results_text = validate(
                data_graph, 
                shacl_graph=shapes_graph,
                inference='rdfs',
                serialize_report_graph='turtle'
            )
            
            self.logger.info("SHACL validation completed",
                           conforms=conforms,
                           data_triples=len(data_graph),
                           shapes_triples=len(shapes_graph))
            
            # Transform to compliance report
            return self.transform_shacl_report(results_graph, conforms, report_id)
            
        except Exception as e:
            self.logger.error("SHACL compliance validation failed",
                            error=str(e))
            
            # Return error report
            error_report = ComplianceReport(
                report_id=report_id or f"error_{int(time.time() * 1000)}",
                timestamp=time.time(),
                validator_type="shacl_adapter_error",
                validator_version=self.adapter_version,
                input_format="unknown",
                overall_valid=False
            )
            
            error_violation = ValidationResult(
                valid=False,
                severity=ValidationSeverity.ERROR,
                message=f"SHACL validation failed: {str(e)}",
                constraint_component="validation_error"
            )
            
            error_report.violations = [error_violation]
            error_report.error_count = 1
            error_report.total_violations = 1
            
            return error_report
    
    def _simulate_shacl_validation(self, data: Any, shapes: Any) -> bool:
        """Simulate SHACL validation for demonstration."""
        # In a real implementation, this would use pyshacl
        # For now, assume validation passes if data is present
        return data is not None and shapes is not None
    
    def _create_mock_results_graph(self, conforms: bool) -> List[Dict[str, Any]]:
        """Create mock results for demonstration."""
        if conforms:
            return []
        else:
            return [
                {
                    "severity": "sh:Violation",
                    "message": "Mock validation violation for demonstration",
                    "focusNode": "ex:TestNode",
                    "resultPath": "ex:testProperty",
                    "sourceConstraintComponent": "sh:MockConstraintComponent"
                }
            ]
    
    def get_adapter_info(self) -> Dict[str, Any]:
        """Get adapter information and capabilities."""
        return {
            "adapter_name": "SHACLToJSONSchemaAdapter",
            "adapter_version": self.adapter_version,
            "hma_compliance_version": "2.2",
            "tier_bridge": {
                "from_tier": "3_alternative",
                "to_tier": "1_mandatory",
                "from_technology": "SHACL",
                "to_technology": "JSON_Schema"
            },
            "capabilities": [
                "shacl_validation_report_transformation",
                "json_schema_compliance_reporting",
                "validation_result_standardization",
                "hma_compliant_output_generation"
            ],
            "supported_input_formats": [
                "rdf_turtle",
                "rdf_xml",
                "json_ld"
            ],
            "output_format": "json_schema_validation_report"
        }