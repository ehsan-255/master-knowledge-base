#!/usr/bin/env python3
"""Validate one or more registry YAML files against the registry schema."""
import sys
import pathlib
import json
import yaml
import jsonschema # type: ignore
from jsonschema import validate # type: ignore

def main():
    """Main validation logic."""
    if len(sys.argv) < 3:
        print("Usage: python validate_registry.py <schema_path> <registry_path1> [registry_path2 ...]")
        sys.exit(2)

    schema_path = pathlib.Path(sys.argv[1])
    registry_paths = [pathlib.Path(p) for p in sys.argv[2:]]

    print(f"Loading schema from: {schema_path}")
    try:
        schema = json.loads(schema_path.read_text(encoding='utf-8'))
    except Exception as e:
        print(f"✖ Error loading schema {schema_path}: {e}")
        sys.exit(1)

    all_valid = True
    for path in registry_paths:
        print(f"Validating: {path}")
        if not path.exists():
            print(f"✖ File not found: {path}")
            all_valid = False
            continue
        try:
            data = yaml.safe_load(path.read_text(encoding='utf-8'))
            validate(instance=data, schema=schema)
            print(f"✔ {path} is valid")
        except jsonschema.exceptions.ValidationError as err:
            print(f"✖ {path} is invalid: {err.message}")
            all_valid = False
        except yaml.YAMLError as err:
            print(f"✖ {path} has YAML parsing error: {err}")
            all_valid = False
        except Exception as e:
            print(f"✖ An unexpected error occurred with {path}: {e}")
            all_valid = False

    if not all_valid:
        print("Validation failed for one or more files.")
        sys.exit(1)
    else:
        print("All registry files are valid.")

if __name__ == "__main__":
    main() 