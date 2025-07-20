#!/usr/bin/env python3
"""
Test suite for HMA v2.2 Plugin Manifest System

Tests the implementation of plugin manifest loading, validation,
and HMA v2.2 compliance checking.
"""

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

# Add tools to path for imports
sys.path.append(str(Path(__file__).resolve().parent.parent.parent / "tools"))

from tools.scribe.core.plugin_loader import PluginLoader, PluginInfo
from tools.scribe.actions.base import BaseAction


class TestPluginManifestSystem:
    """Test the plugin manifest system for HMA v2.2 compliance."""
    
    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.plugin_dir = self.temp_dir / "test_action"
        self.plugin_dir.mkdir(parents=True)
        
        # Create test plugin file
        self.plugin_file = self.temp_dir / "test_action.py"
        self.plugin_file.write_text('''
from tools.scribe.actions.base import BaseAction

class TestAction(BaseAction):
    def __init__(self, action_type, params, config_manager, security_manager):
        super().__init__(action_type, params, config_manager, security_manager)
    
    def execute(self):
        return {"status": "success"}
''')
        
        # Create valid manifest
        self.valid_manifest = {
            "manifest_version": "2.0",
            "plugin_metadata": {
                "name": "test_action",
                "version": "2.0.0",
                "description": "Test action for manifest system validation",
                "author": "Test Author"
            },
            "hma_compliance": {
                "hma_version": "2.2",
                "tier_classification": {
                    "mandatory": ["json_schema", "event_bus"],
                    "recommended": ["structured_logging"],
                    "alternative": []
                },
                "boundary_interfaces": [
                    {
                        "type": "inbound",
                        "protocol": "event_bus",
                        "endpoint": "file_system_events",
                        "telemetry_enabled": True
                    }
                ]
            },
            "runtime_requirements": {
                "python_version": ">=3.8",
                "dependencies": {
                    "required": [],
                    "optional": []
                },
                "platform_support": ["windows", "linux", "macos"]
            },
            "interface_contracts": {
                "action_interface": {
                    "entry_point": "test_action.TestAction",
                    "configuration_schema": {
                        "type": "object",
                        "properties": {}
                    }
                }
            }
        }
        
        self.manifest_file = self.plugin_dir / "manifest.json"
        
    def teardown_method(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_load_valid_manifest(self):
        """Test loading a valid plugin manifest."""
        # Write valid manifest
        with open(self.manifest_file, 'w') as f:
            json.dump(self.valid_manifest, f, indent=2)
        
        loader = PluginLoader()
        manifest = loader.load_plugin_manifest(self.plugin_dir)
        
        assert manifest is not None
        assert manifest["manifest_version"] == "2.0"
        assert manifest["hma_compliance"]["hma_version"] == "2.2"
        assert "test_action" == manifest["plugin_metadata"]["name"]
    
    def test_load_missing_manifest(self):
        """Test behavior when manifest file is missing."""
        loader = PluginLoader()
        manifest = loader.load_plugin_manifest(self.plugin_dir)
        
        assert manifest is None
    
    def test_load_invalid_json_manifest(self):
        """Test loading manifest with invalid JSON."""
        # Write invalid JSON
        self.manifest_file.write_text("{ invalid json }")
        
        loader = PluginLoader()
        manifest = loader.load_plugin_manifest(self.plugin_dir)
        
        assert manifest is None
    
    def test_load_invalid_manifest_schema(self):
        """Test loading manifest that fails schema validation."""
        # Create invalid manifest (missing required fields)
        invalid_manifest = {
            "manifest_version": "2.0",
            "plugin_metadata": {
                "name": "test_action"
                # Missing required fields: version, description, author
            }
        }
        
        with open(self.manifest_file, 'w') as f:
            json.dump(invalid_manifest, f, indent=2)
        
        loader = PluginLoader()
        manifest = loader.load_plugin_manifest(self.plugin_dir)
        
        # Should return None due to validation failure
        assert manifest is None
    
    def test_plugin_info_with_manifest(self):
        """Test PluginInfo creation with manifest data."""
        mock_action_class = MagicMock(spec=BaseAction)
        mock_action_class.__name__ = "TestAction"
        mock_action_class.__module__ = "test_module"
        
        plugin_info = PluginInfo(
            action_class=mock_action_class,
            module_path=str(self.plugin_file),
            action_type="test_action",
            manifest=self.valid_manifest
        )
        
        assert plugin_info.manifest == self.valid_manifest
        assert plugin_info.action_type == "test_action"
        assert plugin_info.manifest["hma_compliance"]["hma_version"] == "2.2"
    
    def test_plugin_info_without_manifest(self):
        """Test PluginInfo creation without manifest (legacy mode)."""
        mock_action_class = MagicMock(spec=BaseAction)
        mock_action_class.__name__ = "TestAction"
        mock_action_class.__module__ = "test_module"
        
        plugin_info = PluginInfo(
            action_class=mock_action_class,
            module_path=str(self.plugin_file),
            action_type="test_action"
        )
        
        assert plugin_info.manifest == {}
        assert plugin_info.action_type == "test_action"
    
    def test_hma_compliance_detection(self):
        """Test detection of HMA v2.2 compliance through manifest."""
        # Write valid manifest
        with open(self.manifest_file, 'w') as f:
            json.dump(self.valid_manifest, f, indent=2)
        
        loader = PluginLoader()
        manifest = loader.load_plugin_manifest(self.plugin_dir)
        
        # Verify HMA compliance indicators
        assert manifest["hma_compliance"]["hma_version"] == "2.2"
        assert "json_schema" in manifest["hma_compliance"]["tier_classification"]["mandatory"]
        assert "event_bus" in manifest["hma_compliance"]["tier_classification"]["mandatory"]
        assert len(manifest["hma_compliance"]["boundary_interfaces"]) > 0
    
    def test_manifest_security_permissions(self):
        """Test manifest security permission declarations."""
        # Add security section to manifest
        self.valid_manifest["security"] = {
            "permissions": ["file_read", "file_write"],
            "sandbox_compatible": True,
            "mtls_required": False
        }
        
        with open(self.manifest_file, 'w') as f:
            json.dump(self.valid_manifest, f, indent=2)
        
        loader = PluginLoader()
        manifest = loader.load_plugin_manifest(self.plugin_dir)
        
        assert "security" in manifest
        assert "file_read" in manifest["security"]["permissions"]
        assert manifest["security"]["sandbox_compatible"] is True
    
    def test_manifest_tier_classification(self):
        """Test HMA tier classification in manifest."""
        loader = PluginLoader()
        with open(self.manifest_file, 'w') as f:
            json.dump(self.valid_manifest, f, indent=2)
        
        manifest = loader.load_plugin_manifest(self.plugin_dir)
        tier_classification = manifest["hma_compliance"]["tier_classification"]
        
        # Verify tier structure
        assert "mandatory" in tier_classification
        assert "recommended" in tier_classification
        assert "alternative" in tier_classification
        
        # Verify mandatory technologies
        assert "json_schema" in tier_classification["mandatory"]
        assert "event_bus" in tier_classification["mandatory"]
        
        # Verify recommended technologies  
        assert "structured_logging" in tier_classification["recommended"]
    
    def test_manifest_boundary_interfaces(self):
        """Test boundary interface declarations in manifest."""
        loader = PluginLoader()
        with open(self.manifest_file, 'w') as f:
            json.dump(self.valid_manifest, f, indent=2)
        
        manifest = loader.load_plugin_manifest(self.plugin_dir)
        interfaces = manifest["hma_compliance"]["boundary_interfaces"]
        
        assert len(interfaces) > 0
        interface = interfaces[0]
        
        # Verify interface structure
        assert "type" in interface
        assert "protocol" in interface
        assert "telemetry_enabled" in interface
        
        # Verify values
        assert interface["type"] == "inbound"
        assert interface["protocol"] == "event_bus"
        assert interface["telemetry_enabled"] is True
    
    def test_manifest_schema_validation_missing_schema(self):
        """Test behavior when manifest schema file is missing."""
        with open(self.manifest_file, 'w') as f:
            json.dump(self.valid_manifest, f, indent=2)
        
        # Temporarily move the schema file if it exists to simulate missing schema
        loader = PluginLoader()
        schema_path = Path(__file__).parent.parent.parent / "tools" / "scribe" / "schemas" / "plugin_manifest.schema.json"
        schema_backup = None
        
        try:
            if schema_path.exists():
                schema_backup = schema_path.read_text()
                schema_path.unlink()  # Remove the schema file
            
            manifest = loader.load_plugin_manifest(self.plugin_dir)
            
            # Should still load manifest but skip validation
            assert manifest is not None
            assert manifest["manifest_version"] == "2.0"
            
        finally:
            # Restore the schema file if it was backed up
            if schema_backup is not None:
                schema_path.write_text(schema_backup)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])