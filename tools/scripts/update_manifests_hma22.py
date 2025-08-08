#!/usr/bin/env python3
"""
Update all plugin manifests for HMA v2.2 compliance.
Adds the required "product": "scribe" field to plugin_metadata.
"""

import json
from pathlib import Path

def update_manifests():
    """Update all plugin manifests with HMA v2.2 compliance."""
    manifest_files = list(Path('tools/scribe/actions').rglob('manifest.json'))
    print(f'Found {len(manifest_files)} plugin manifest files')
    
    updated_count = 0
    for manifest_path in manifest_files:
        try:
            # Read current manifest
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest_data = json.load(f)
            
            # Add product field if missing
            needs_update = False
            if 'plugin_metadata' in manifest_data:
                if 'product' not in manifest_data['plugin_metadata']:
                    manifest_data['plugin_metadata']['product'] = 'scribe'
                    needs_update = True
                    print(f'Adding product field to {manifest_path}')
                else:
                    print(f'Already has product field: {manifest_path}')
            
            if needs_update:
                # Write updated manifest
                with open(manifest_path, 'w', encoding='utf-8') as f:
                    json.dump(manifest_data, f, indent=2, ensure_ascii=False)
                updated_count += 1
                
        except Exception as e:
            print(f'Error updating {manifest_path}: {e}')
    
    print(f'Updated {updated_count} manifest files')
    return updated_count

if __name__ == "__main__":
    update_manifests()