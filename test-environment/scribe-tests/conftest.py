"""
Pytest configuration and fixtures for Scribe v2.2 testing.

Provides shared fixtures for HMA v2.2 compliance testing including:
- Mock port registry
- Test data fixtures
- Scribe engine instances
- SHACL validation test data
"""

import pytest
import sys
import os
from pathlib import Path
from typing import Dict, Any
from unittest.mock import Mock, MagicMock

# Configure pytest-asyncio
pytest_plugins = ("pytest_asyncio",)

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import Scribe components
from tools.scribe.core.hma_ports import PortRegistry
from tools.scribe.core.port_adapters import (
    ScribePluginExecutionAdapter,
    ScribeConfigurationAdapter,
    ScribeHealthCheckAdapter,
    ScribeLoggingAdapter
)
from tools.scribe.core.hma_telemetry import HMATelemetry
from tools.scribe.core.config_manager import ConfigManager


@pytest.fixture
def mock_port_registry():
    """Mock port registry for testing plugin interactions."""
    registry = PortRegistry()
    
    # Mock essential ports
    mock_config_port = Mock()
    mock_logging_port = Mock()
    mock_event_bus_port = Mock()
    mock_file_system_port = Mock()
    mock_command_port = Mock()
    mock_observability_port = Mock()
    
    registry.register_port("configuration", mock_config_port)
    registry.register_port("logging", mock_logging_port)
    registry.register_port("event_bus", mock_event_bus_port)
    registry.register_port("file_system", mock_file_system_port)
    registry.register_port("command_execution", mock_command_port)
    registry.register_port("observability", mock_observability_port)
    
    return registry


@pytest.fixture
def mock_telemetry():
    """Mock HMA telemetry for testing boundary operations."""
    return Mock(spec=HMATelemetry)


@pytest.fixture
def mock_config_manager():
    """Mock configuration manager for testing."""
    config_manager = Mock(spec=ConfigManager)
    config_manager.get.return_value = {}
    config_manager.get_engine_settings.return_value = {}
    config_manager.validate_config_dict.return_value = True
    return config_manager


@pytest.fixture
def mock_security_manager():
    """Mock security manager for testing."""
    security_manager = Mock()
    security_manager.validate_plugin_access.return_value = True
    security_manager.execute_command_safely.return_value = (True, "success", "")
    security_manager.validate_file_access.return_value = True
    return security_manager


@pytest.fixture
def sample_plugin_manifest():
    """Sample plugin manifest for testing."""
    return {
        "manifest_version": "2.2",
        "hma_version": "2.2",
        "plugin": {
            "id": "test_plugin",
            "name": "Test Plugin",
            "version": "1.0.0",
            "type": "L3-Capability"
        },
        "interfaces": {
            "implemented_ports": [],
            "consumed_ports": []
        },
        "compliance": {
            "hma_version": "2.2",
            "mandatory_standards": {
                "boundary_validation": "json_schema",
                "boundary_observability": "opentelemetry",
                "boundary_security": "mtls_tls"
            }
        }
    }


@pytest.fixture
def sample_shacl_shapes():
    """Sample SHACL shapes for testing validation."""
    return """
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.org/> .

ex:DocumentShape
    a sh:NodeShape ;
    sh:targetClass ex:Document ;
    sh:property [
        sh:path ex:title ;
        sh:datatype xsd:string ;
        sh:minLength 1 ;
        sh:maxLength 200 ;
    ] ;
    sh:property [
        sh:path ex:info-type ;
        sh:datatype xsd:string ;
        sh:in ("general-document" "standard-definition" "policy-document") ;
    ] .
"""


@pytest.fixture
def sample_rdf_data():
    """Sample RDF data for testing SHACL validation."""
    return """
@prefix ex: <http://example.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:TestDocument
    a ex:Document ;
    ex:title "Test Document Title"^^xsd:string ;
    ex:info-type "general-document"^^xsd:string .
"""


@pytest.fixture
def test_file_content():
    """Sample file content for testing actions."""
    return """---
title: "Test Document"
info-type: "general-document"
kb-id: "TEST-DOC-001"
---

# Test Document

This is a test document for validating Scribe functionality.
"""


@pytest.fixture(scope="session")
def test_data_dir():
    """Path to test data directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def mock_plugin_loader():
    """Mock plugin loader for testing."""
    loader = Mock()
    
    # Mock plugin info
    mock_plugin_info = Mock()
    mock_plugin_info.manifest = {
        "manifest_version": "2.2",
        "plugin": {"id": "test_plugin", "type": "L3-Capability"}
    }
    mock_plugin_info.create_instance.return_value = Mock()
    
    loader.get_plugin.return_value = mock_plugin_info
    loader.get_all_plugins.return_value = {"test_plugin": mock_plugin_info}
    
    return loader


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "hma_compliance: mark test as HMA v2.2 compliance test"
    )
    config.addinivalue_line(
        "markers", "plugin_test: mark test as plugin-specific test"
    )
    config.addinivalue_line(
        "markers", "boundary_test: mark test as boundary validation test"
    )
    config.addinivalue_line(
        "markers", "shacl_test: mark test as SHACL validation test"
    )


def pytest_collection_modifyitems(config, items):
    """Add markers to tests based on their location."""
    for item in items:
        # Add markers based on test file location
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        
        # Add HMA compliance marker to relevant tests
        if "hma" in str(item.fspath).lower() or "compliance" in str(item.fspath).lower():
            item.add_marker(pytest.mark.hma_compliance)