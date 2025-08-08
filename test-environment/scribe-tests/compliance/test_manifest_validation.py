#!/usr/bin/env python3
"""
HMA v2.2 Plugin Manifest Validation Test

Repository-wide validation of ALL plugin manifests against HMA v2.2 schema.
Priority 0.2 Acceptance Test - ALL MUST PASS for HMA v2.2 compliance.

This test iterates through ALL plugin manifest.json files and validates them
against the HMA v2.2 schema with sophisticated PluginLoader validation.
"""

import pytest
import json
import re
from pathlib import Path
from typing import List, Dict, Any
import jsonschema

from tools.scribe.core.plugin_loader import PluginLoader


class TestPluginManifestSchemaCompliance:
    """Test all plugin manifests comply with HMA v2.2 schema."""
    
    @pytest.fixture
    def manifest_schema(self) -> Dict[str, Any]:
        """Load the HMA v2.2 plugin manifest schema."""
        schema_path = Path("../tools/scribe/schemas/plugin_manifest.schema.json")
        assert schema_path.exists(), "Plugin manifest schema is required for HMA v2.2"
        
        with open(schema_path) as f:
            return json.load(f)
    
    @pytest.fixture  
    def all_plugin_manifests(self) -> List[Path]:
        """Discover all plugin manifest.json files in the repository."""
        manifests = []
        
        # Search for manifest.json files in actions directories
        actions_dir = Path("../tools/scribe/actions")
        if actions_dir.exists():
            for manifest_file in actions_dir.rglob("manifest.json"):
                manifests.append(manifest_file)
        
        return manifests
    
    def test_manifest_schema_is_valid(self, manifest_schema):
        """The manifest schema itself must be valid JSON Schema."""
        # Validate the schema is well-formed
        assert "$schema" in manifest_schema
        assert "type" in manifest_schema
        assert "properties" in manifest_schema
        assert "required" in manifest_schema
        
        # Verify HMA v2.2 specific requirements
        assert "manifest_version" in manifest_schema["properties"]
        assert "hma_compliance" in manifest_schema["properties"]
        
        # Verify the manifest_version pattern matches our requirements
        version_pattern = manifest_schema["properties"]["manifest_version"]["pattern"]
        assert version_pattern == "^2\\.2(\\.\\d+)?$"
        
        # Verify product constraint exists
        product_field = manifest_schema["properties"]["plugin_metadata"]["properties"]["product"]
        assert product_field["const"] == "scribe"
    
    def test_all_plugin_manifests_exist(self, all_plugin_manifests):
        """All plugins must have manifest.json files."""
        assert len(all_plugin_manifests) > 0, "No plugin manifests found - this indicates a configuration issue"
        
        for manifest_path in all_plugin_manifests:
            assert manifest_path.exists(), f"Manifest file missing: {manifest_path}"
    
    def test_all_manifests_valid_json(self, all_plugin_manifests):
        """All manifest.json files must contain valid JSON."""
        for manifest_path in all_plugin_manifests:
            try:
                with open(manifest_path) as f:
                    manifest_data = json.load(f)
                assert isinstance(manifest_data, dict), f"Manifest must be JSON object: {manifest_path}"
            except json.JSONDecodeError as e:
                pytest.fail(f"Invalid JSON in manifest {manifest_path}: {e}")
    
    def test_all_manifests_schema_compliant(self, all_plugin_manifests, manifest_schema):
        """ALL plugin manifests must comply with HMA v2.2 schema."""
        failures = []
        
        for manifest_path in all_plugin_manifests:
            try:
                with open(manifest_path) as f:
                    manifest_data = json.load(f)
                
                # Validate against schema
                jsonschema.validate(manifest_data, manifest_schema)
                
            except jsonschema.ValidationError as e:
                failures.append(f"{manifest_path}: {e.message}")
            except Exception as e:
                failures.append(f"{manifest_path}: Unexpected error - {e}")
        
        if failures:
            failure_msg = "The following plugin manifests failed HMA v2.2 schema validation:\n\n"
            failure_msg += "\n".join(f"  • {failure}" for failure in failures)
            failure_msg += "\n\nALL manifests must be HMA v2.2 compliant!"
            pytest.fail(failure_msg)
    
    def test_all_manifests_hma_version_compliance(self, all_plugin_manifests):
        """ALL manifests must have proper HMA v2.2 version compliance."""
        failures = []
        version_pattern = re.compile(r"^2\.2(\.\d+)?$")
        
        for manifest_path in all_plugin_manifests:
            try:
                with open(manifest_path) as f:
                    manifest_data = json.load(f)
                
                # Check manifest_version
                manifest_version = manifest_data.get("manifest_version")
                if not manifest_version or not version_pattern.match(manifest_version):
                    failures.append(f"{manifest_path}: Invalid manifest_version '{manifest_version}' (must be 2.2 or 2.2.x)")
                
                # Check hma_compliance.hma_version
                hma_version = manifest_data.get("hma_compliance", {}).get("hma_version")
                if hma_version != "2.2":
                    failures.append(f"{manifest_path}: Invalid hma_compliance.hma_version '{hma_version}' (must be '2.2')")
                
                # Check product field
                product = manifest_data.get("plugin_metadata", {}).get("product")
                if product != "scribe":
                    failures.append(f"{manifest_path}: Invalid product '{product}' (must be 'scribe')")
                    
            except Exception as e:
                failures.append(f"{manifest_path}: Error reading manifest - {e}")
        
        if failures:
            failure_msg = "The following plugin manifests failed HMA v2.2 version compliance:\n\n"
            failure_msg += "\n".join(f"  • {failure}" for failure in failures)
            failure_msg += "\n\nALL manifests must have proper HMA v2.2 version compliance!"
            pytest.fail(failure_msg)


class TestPluginLoaderManifestValidation:
    """Test that sophisticated PluginLoader properly validates manifests."""
    
    def test_plugin_loader_rejects_invalid_version(self, tmp_path):
        """PluginLoader must reject manifests with invalid versions."""
        loader = PluginLoader()
        
        # Create invalid manifest with wrong version
        invalid_manifest = {
            "manifest_version": "2.1",  # Invalid - must be 2.2+
            "plugin_metadata": {"product": "scribe"},
            "hma_compliance": {"hma_version": "2.2"}
        }
        
        manifest_dir = tmp_path / "invalid_plugin"
        manifest_dir.mkdir()
        manifest_file = manifest_dir / "manifest.json"
        
        with open(manifest_file, 'w') as f:
            json.dump(invalid_manifest, f)
        
        # Should raise validation error
        result = loader.load_plugin_manifest(manifest_dir)
        assert result is None  # Should return None on validation failure
    
    def test_plugin_loader_accepts_valid_version(self, tmp_path):
        """PluginLoader must accept manifests with valid HMA v2.2 versions."""
        loader = PluginLoader()
        
        # Create valid manifest
        valid_manifest = {
            "manifest_version": "2.2.1",  # Valid - matches pattern
            "plugin_metadata": {
                "name": "test_plugin",
                "version": "1.0.0", 
                "description": "Test plugin for validation",
                "author": "Test Author",
                "product": "scribe"
            },
            "hma_compliance": {
                "hma_version": "2.2",
                "tier_classification": {
                    "mandatory": ["json_schema"],
                    "recommended": ["structured_logging"],
                    "alternative": []
                },
                "boundary_interfaces": []
            },
            "runtime_requirements": {
                "python_version": ">=3.8",
                "dependencies": {}
            },
            "interface_contracts": {
                "action_interface": {
                    "entry_point": "test.TestAction",
                    "configuration_schema": {}
                }
            }
        }
        
        manifest_dir = tmp_path / "valid_plugin"
        manifest_dir.mkdir()
        manifest_file = manifest_dir / "manifest.json"
        
        with open(manifest_file, 'w') as f:
            json.dump(valid_manifest, f)
        
        # Should load successfully
        result = loader.load_plugin_manifest(manifest_dir)
        assert result is not None
        assert result["manifest_version"] == "2.2.1"


class TestManifestPatternValidation:
    """Test manifest version pattern validation."""
    
    def test_valid_version_patterns(self):
        """Test that all valid version patterns are accepted."""
        pattern = re.compile(r"^2\.2(\.\d+)?$")
        
        valid_versions = ["2.2", "2.2.0", "2.2.1", "2.2.10", "2.2.999"]
        for version in valid_versions:
            assert pattern.match(version), f"Valid version '{version}' should match pattern"
    
    def test_invalid_version_patterns(self):
        """Test that invalid version patterns are rejected."""
        pattern = re.compile(r"^2\.2(\.\d+)?$")
        
        invalid_versions = ["2.1", "2.3", "3.2", "2.2.x", "2.2.0.1", "v2.2", "2.2-beta"]
        for version in invalid_versions:
            assert not pattern.match(version), f"Invalid version '{version}' should not match pattern"


if __name__ == "__main__":
    # Run as: python -m pytest test-environment/scribe-tests/compliance/test_manifest_validation.py -v
    pytest.main([__file__, "-v"])