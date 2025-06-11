# tools/scribe/actions/view_generation_action.py
import logging
from pathlib import Path
import json
import yaml # Requires PyYAML
from datetime import datetime
import sys

from .base_action import BaseAction

# Core logic adapted from tools/view_generator.py
# These can be static methods or part of the class.

def _load_json_file(file_path: Path, logger: logging.Logger) -> Optional[dict]:
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {file_path}: {e}")
        return None
    except IOError as e:
        logger.error(f"IOError reading {file_path}: {e}")
        return None

def _generate_markdown_view_standard(standard_data: dict, schema_registry: dict, logger: logging.Logger) -> str:
    if not standard_data:
        return "Error: Standard data is empty."

    md_lines = []
    title = standard_data.get("kb:title", "Unknown Standard")
    standard_id_val = standard_data.get("kb:standard_id", standard_data.get("@id", "Unknown ID"))

    md_lines.append(f"# View: {title} ({standard_id_val})")
    md_lines.append(f"Generated: {datetime.now().isoformat()}")
    md_lines.append("\n---")

    md_lines.append("## Fields")
    md_lines.append("| Field Name | Value | Description (from Schema) |")
    md_lines.append("|------------|-------|---------------------------|")

    schema_field_map = {
        defn.get('kb:fieldName'): defn
        for defn in schema_registry.get("kb:fieldDefinitions", [])
    }

    for key, value in standard_data.items():
        if key in ["@id", "@type", "kb:contentHash", "kb:fileSize", "kb:lastModified", "kb:indexed"]: # Skip some internal fields for this view
            continue

        field_desc = "N/A"
        simple_key = key.split("kb:")[-1].replace("_", "-") if key.startswith("kb:") else key
        field_def = schema_field_map.get(simple_key)
        if field_def:
            field_desc = field_def.get("kb:description", "No description in schema.")

        val_str = str(value)
        if isinstance(value, list):
            val_str = "\n".join([f"- {v}" for v in value])
        elif isinstance(value, dict):
            try:
                val_str = f"```yaml\n{yaml.dump(value, indent=2, sort_keys=False, allow_unicode=True)}```"
            except yaml.YAMLError:
                val_str = json.dumps(value, indent=2, ensure_ascii=False)

        # Escape pipes in value string for Markdown table
        if isinstance(val_str, str):
            val_str = val_str.replace("|", "\\|")


        md_lines.append(f"| `{key}` | {val_str} | {field_desc} |")

    # Optionally add raw data if desired, or keep view cleaner
    # md_lines.append("\n## Raw JSON-LD Data")
    # md_lines.append("```json")
    # md_lines.append(json.dumps(standard_data, indent=2, ensure_ascii=False))
    # md_lines.append("```")

    return "\n".join(md_lines)

def _generate_yaml_view_standard(standard_data: dict, logger: logging.Logger) -> str:
    if not standard_data:
        return "# Error: Standard data is empty."
    try:
        # Return a subset of fields for a cleaner "change request" base
        view_data = {k: v for k, v in standard_data.items() if not k.startswith("kb:contentHash") and not k.startswith("kb:fileSize") and not k.startswith("kb:lastModified") and not k.startswith("kb:indexed")}
        return yaml.dump(view_data, sort_keys=False, indent=2, allow_unicode=True)
    except yaml.YAMLError as e:
        logger.error(f"Error encoding YAML: {e}")
        return f"# Error encoding YAML: {e}"


class ViewGenerationAction(BaseAction):
    def __init__(self, action_config: dict, global_config: dict, logger=None):
        super().__init__(action_config, global_config, logger)
        self.schema_registry_path_str = self.action_config.get("schema_registry_path", "standards/registry/schema-registry.jsonld")
        self.master_index_path_str = self.action_config.get("master_index_path", "standards/registry/master-index.jsonld")
        self.schema_registry = None
        self.master_index = None

    def setup(self):
        if not super().setup():
            return False

        schema_file = self.repo_root / self.schema_registry_path_str
        master_index_file = self.repo_root / self.master_index_path_str

        self.schema_registry = _load_json_file(schema_file, self.logger)
        if not self.schema_registry:
            self.logger.error(f"Failed to load schema registry: {schema_file}")
            return False

        self.master_index = _load_json_file(master_index_file, self.logger)
        if not self.master_index:
            self.logger.error(f"Failed to load master index: {master_index_file}")
            return False

        self.logger.info("ViewGenerationAction setup complete.")
        return True

    def execute(self, execution_context: dict) -> dict:
        self.logger.info(f"Executing ViewGenerationAction. Context: {execution_context}")

        entity_id = execution_context.get("entity_id")
        view_type = execution_context.get("view_type")
        output_path_str = execution_context.get("output_path") # Relative to repo_root or absolute

        if not entity_id or not view_type:
            return {'status': 'failure', 'message': "Missing 'entity_id' or 'view_type' in execution_context."}
        if view_type not in ['md', 'yaml']:
            return {'status': 'failure', 'message': f"Invalid 'view_type': {view_type}. Must be 'md' or 'yaml'."}

        target_standard_data = None
        if self.master_index.get("kb:documents"):
            for doc in self.master_index["kb:documents"]:
                if doc.get("kb:standard_id") == entity_id or doc.get("@id") == entity_id:
                    target_standard_data = doc
                    break
                generated_id_suffix = entity_id.replace('/', '-').replace('.md', '') # Handle if filepath-like ID is passed
                if doc.get("@id") == f"kb:doc-{generated_id_suffix}":
                    target_standard_data = doc
                    break

        if not target_standard_data:
            msg = f"Entity with ID '{entity_id}' not found in master index."
            self.logger.error(msg)
            return {'status': 'failure', 'message': msg}

        self.logger.info(f"Found entity: {target_standard_data.get('kb:title', entity_id)}")

        output_content = ""
        if view_type == 'md':
            self.logger.info("Generating Markdown view...")
            output_content = _generate_markdown_view_standard(target_standard_data, self.schema_registry, self.logger)
        elif view_type == 'yaml':
            self.logger.info("Generating YAML view...")
            output_content = _generate_yaml_view_standard(target_standard_data, self.logger)

        if output_path_str:
            try:
                # output_path should be relative to repo_root if not absolute
                actual_output_path = self.repo_root / output_path_str
                actual_output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(actual_output_path, 'w', encoding='utf-8') as f:
                    f.write(output_content)
                self.logger.info(f"View successfully written to: {actual_output_path}")
                return {
                    'status': 'success',
                    'message': f"View generated for {entity_id}.",
                    'output_path': str(Path(output_path_str)) # Return relative path as passed in context
                }
            except IOError as e:
                self.logger.exception(f"Error writing to output file {actual_output_path}: {e}")
                return {
                    'status': 'failure',
                    'message': f"Error writing file: {e}",
                    'output_content': output_content # Return content if write failed
                }
        else: # Output to context/stdout
            return {
                'status': 'success',
                'message': f"View generated for {entity_id}.",
                'output_content': output_content
            }

# Example usage (for testing)
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("ViewGenerationActionTest")

    mock_global_config = {
        "repo_root": str(Path(__file__).resolve().parent.parent.parent)
    }
    mock_action_config = {} # No action-specific config for now beyond defaults

    # For this test to run, master-index.jsonld and schema-registry.jsonld must exist
    # at their default locations relative to the mock_repo_root.
    # And master-index.jsonld should contain a document with standard_id 'TEST-SHACL-001'.

    # Ensure dummy files exist for testing
    registry_dir = Path(mock_global_config["repo_root"]) / "standards" / "registry"
    registry_dir.mkdir(parents=True, exist_ok=True)

    if not (registry_dir / "schema-registry.jsonld").exists():
        with open(registry_dir / "schema-registry.jsonld", "w") as f:
            json.dump({"kb:fieldDefinitions": [{"kb:fieldName": "title", "kb:description": "Test Title Desc"}]}, f)
        logger.info("Created dummy schema-registry.jsonld for test.")

    if not (registry_dir / "master-index.jsonld").exists():
        test_doc = {"@id": "kb:doc-test-shacl-001", "kb:standard_id": "TEST-SHACL-001", "kb:title": "Test Document"}
        with open(registry_dir / "master-index.jsonld", "w") as f:
            json.dump({"kb:documents": [test_doc]}, f)
        logger.info("Created dummy master-index.jsonld for test.")


    action = ViewGenerationAction(action_config=mock_action_config, global_config=mock_global_config, logger=logger)

    if action.setup():
        logger.info("--- MD View to STDOUT Test ---")
        md_context = {"entity_id": "TEST-SHACL-001", "view_type": "md"}
        md_result = action.execute(md_context)
        logger.info(f"MD Result: {md_result.get('status')}")
        if md_result.get('status') == 'success':
             print("MD Output:\n", md_result.get('output_content'))

        logger.info("--- YAML View to File Test ---")
        yaml_context = {"entity_id": "TEST-SHACL-001", "view_type": "yaml", "output_path": "temp_view_output.yaml"}
        yaml_result = action.execute(yaml_context)
        logger.info(f"YAML Result: {yaml_result.get('status')}, Path: {yaml_result.get('output_path')}")

        # Cleanup
        output_file = Path(mock_global_config["repo_root"]) / "temp_view_output.yaml"
        if output_file.exists():
            output_file.unlink()
            logger.info(f"Cleaned up: {output_file}")
    else:
        logger.error("Test setup failed.")
