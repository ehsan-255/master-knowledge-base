#!/usr/bin/env python3
"""
Script to update all plugin manifests to HMA v2.1 compliance
"""

import json
import os
from pathlib import Path

def update_manifest(manifest_path: Path):
    """Update a single manifest to HMA v2.1 compliance"""
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    # Update version information
    manifest["manifest_version"] = "2.1"
    
    # Update plugin metadata
    if "plugin_metadata" in manifest:
        # Update version
        if "version" in manifest["plugin_metadata"]:
            version_parts = manifest["plugin_metadata"]["version"].split(".")
            manifest["plugin_metadata"]["version"] = f"{version_parts[0]}.1.0"
        
        # Add type if missing
        if "type" not in manifest["plugin_metadata"]:
            manifest["plugin_metadata"]["type"] = "L3-Capability"
    
    # Update HMA compliance
    if "hma_compliance" in manifest:
        manifest["hma_compliance"]["hma_version"] = "2.1"
        
        # Update tier classification
        if "tier_classification" in manifest["hma_compliance"]:
            manifest["hma_compliance"]["tier_classification"] = {
                "mandatory": ["json_schema", "otel_boundary", "mtls"],
                "recommended": ["structured_logging", "health_checks", "kubernetes"],
                "alternative": []
            }
        
        # Update boundary interfaces
        if "boundary_interfaces" in manifest["hma_compliance"]:
            manifest["hma_compliance"]["boundary_interfaces"] = [
                {
                    "port_type": "PluginExecutionPort",
                    "direction": "inbound", 
                    "validation": "json_schema",
                    "telemetry": "otel_spans"
                },
                {
                    "port_type": "EventBusPort",
                    "direction": "outbound",
                    "validation": "event_schema", 
                    "telemetry": "otel_spans"
                }
            ]
    
    # Update security requirements
    if "security" in manifest:
        manifest["security"]["mtls_required"] = True
        
        # Add sandbox compatibility for non-system plugins
        plugin_name = manifest.get("plugin_metadata", {}).get("name", "")
        if "command" not in plugin_name and "run" not in plugin_name:
            manifest["security"]["sandbox_compatible"] = True
    
    # Save updated manifest
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"Updated: {manifest_path}")

def main():
    """Update all plugin manifests"""
    script_dir = Path(__file__).parent
    actions_dir = script_dir.parent / "scribe" / "actions"
    
    for manifest_path in actions_dir.glob("*/manifest.json"):
        try:
            update_manifest(manifest_path)
        except Exception as e:
            print(f"Error updating {manifest_path}: {e}")

if __name__ == "__main__":
    main()