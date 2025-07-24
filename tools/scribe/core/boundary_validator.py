#!/usr/bin/env python3
"""
HMA v2.1 Boundary Validation System

Validates data at all HMA boundary interfaces to ensure compliance
with JSON Schema requirements and event schema validation.
"""

import jsonschema
import json
import time
import uuid
from typing import Dict, Any, Optional, List
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

from .logging_config import get_scribe_logger
from .hma_ports import ObservabilityPort

logger = get_scribe_logger(__name__)

class BoundaryType(Enum):
    """Types of HMA boundaries"""
    L1_INTERFACE = "l1_interface"
    L2_CORE = "l2_core"
    L3_PLUGIN = "l3_plugin"
    L4_INFRASTRUCTURE = "l4_infrastructure"

@dataclass
class ValidationResult:
    """Result of boundary validation"""
    valid: bool
    errors: List[str]
    boundary_type: BoundaryType
    component_id: str
    timestamp: float

class BoundaryValidator:
    """Validates data at HMA boundary interfaces"""
    
    def __init__(self, schema_registry: Dict[str, Dict], observability_port: Optional[ObservabilityPort] = None):
        self.schemas = schema_registry
        self.observability = observability_port
        self._load_schemas()
    
    def _load_schemas(self) -> None:
        """Load boundary validation schemas"""
        # Default schemas for HMA v2.1 boundaries
        self.default_schemas = {
            "l1_file_system_input": {
                "type": "object",
                "required": ["event_id", "type", "file_path", "timestamp"],
                "properties": {
                    "event_id": {"type": "string", "format": "uuid"},
                    "type": {"type": "string", "enum": ["created", "modified", "deleted", "moved"]},
                    "file_path": {"type": "string", "minLength": 1},
                    "old_path": {"type": "string"},
                    "timestamp": {"type": "number", "minimum": 0}
                }
            },
            "l2_plugin_execution_input": {
                "type": "object", 
                "required": ["plugin_id", "input_data", "request_id"],
                "properties": {
                    "plugin_id": {"type": "string", "minLength": 1},
                    "input_data": {"type": "object"},
                    "request_id": {"type": "string", "format": "uuid"},
                    "correlation_id": {"type": "string"}
                }
            },
            "event_schema": {
                "type": "object",
                "required": ["event_id", "event_type", "timestamp", "source", "data"],
                "properties": {
                    "event_id": {"type": "string", "format": "uuid"},
                    "event_type": {"type": "string", "minLength": 1},
                    "timestamp": {"type": "string", "format": "date-time"},
                    "source": {"type": "string", "minLength": 1},
                    "data": {"type": "object"},
                    "correlation_id": {"type": "string"},
                    "target": {"type": "string"}
                }
            }
        }
        
        # Merge with provided schemas
        self.schemas.update(self.default_schemas)
    
    def validate_l1_input(self, data: Dict[str, Any], interface: str) -> ValidationResult:
        """Validate L1 adapter input against schema"""
        schema_key = f"l1_{interface}_input"
        return self._validate_data(data, schema_key, BoundaryType.L1_INTERFACE, interface)
    
    def validate_l2_plugin_call(self, data: Dict[str, Any], component_id: str) -> ValidationResult:
        """Validate L2 plugin execution call"""
        return self._validate_data(data, "l2_plugin_execution_input", BoundaryType.L2_CORE, component_id)
    
    def validate_event_schema(self, event: Dict[str, Any], source_component: str) -> ValidationResult:
        """Validate event against HMA event schema"""
        return self._validate_data(event, "event_schema", BoundaryType.L3_PLUGIN, source_component)
    
    def validate_custom_boundary(self, data: Dict[str, Any], 
                                schema_key: str, 
                                boundary_type: BoundaryType,
                                component_id: str) -> ValidationResult:
        """Validate against custom boundary schema"""
        return self._validate_data(data, schema_key, boundary_type, component_id)
    
    def _validate_data(self, data: Dict[str, Any], 
                      schema_key: str, 
                      boundary_type: BoundaryType,
                      component_id: str) -> ValidationResult:
        """Internal validation logic"""
        timestamp = time.time()
        
        # Get schema
        schema = self.schemas.get(schema_key)
        if not schema:
            error_msg = f"No schema found for {schema_key}"
            logger.error("Schema not found", schema_key=schema_key, component=component_id)
            
            if self.observability:
                self.observability.emit_metric(
                    "hma_boundary_validation_errors_total", 
                    1.0,
                    {"boundary_type": boundary_type.value, "error_type": "schema_missing"}
                )
            
            return ValidationResult(False, [error_msg], boundary_type, component_id, timestamp)
        
        # Perform validation
        try:
            jsonschema.validate(data, schema)
            
            logger.debug("Boundary validation passed", 
                        boundary_type=boundary_type.value,
                        component=component_id,
                        schema_key=schema_key)
            
            if self.observability:
                self.observability.emit_metric(
                    "hma_boundary_validations_total",
                    1.0, 
                    {"boundary_type": boundary_type.value, "status": "success"}
                )
                
                self.observability.record_boundary_crossing(
                    "validator", component_id, "validate", 
                    (time.time() - timestamp) * 1000
                )
            
            return ValidationResult(True, [], boundary_type, component_id, timestamp)
            
        except jsonschema.ValidationError as e:
            error_msg = f"Validation failed: {e.message}"
            logger.error("Boundary validation failed",
                        boundary_type=boundary_type.value,
                        component=component_id,
                        error=error_msg,
                        error_path=list(e.absolute_path) if e.absolute_path else None)
            
            if self.observability:
                self.observability.emit_metric(
                    "hma_boundary_validation_errors_total",
                    1.0,
                    {"boundary_type": boundary_type.value, "error_type": "schema_violation"}
                )
            
            return ValidationResult(False, [error_msg], boundary_type, component_id, timestamp)
            
        except jsonschema.SchemaError as e:
            error_msg = f"Schema error: {e.message}"
            logger.error("Schema validation error",
                        boundary_type=boundary_type.value,
                        component=component_id,
                        schema_error=error_msg)
            
            return ValidationResult(False, [error_msg], boundary_type, component_id, timestamp)

class EventValidator:
    """Specialized validator for HMA events"""
    
    def __init__(self, boundary_validator: BoundaryValidator):
        self.boundary_validator = boundary_validator
    
    def create_hma_event(self, event_type: str, data: Dict[str, Any], 
                        source: str, target: Optional[str] = None) -> Dict[str, Any]:
        """Create HMA-compliant event"""
        event = {
            "event_id": str(uuid.uuid4()),
            "event_type": event_type,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "source": source,
            "data": data
        }
        
        if target:
            event["target"] = target
            
        return event
    
    def validate_and_publish_event(self, event: Dict[str, Any], source_component: str) -> bool:
        """Validate event and return whether it's safe to publish"""
        result = self.boundary_validator.validate_event_schema(event, source_component)
        return result.valid

def create_boundary_validator(schema_dir: Optional[Path] = None, 
                            observability_port: Optional[ObservabilityPort] = None) -> BoundaryValidator:
    """Factory function to create configured boundary validator"""
    
    # Load schemas from directory if provided
    schemas = {}
    if schema_dir and schema_dir.exists():
        for schema_file in schema_dir.glob("*.json"):
            try:
                with open(schema_file) as f:
                    schema_data = json.load(f)
                    schemas[schema_file.stem] = schema_data
            except Exception as e:
                logger.warning(f"Failed to load schema {schema_file}: {e}")
    
    return BoundaryValidator(schemas, observability_port)