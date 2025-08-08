# tools/scribe/actions/graph_validation_action.py
import logging
from pathlib import Path
import json # For loading context if master_index_data is passed as string

from .base_action import BaseAction
# Assuming GraphValidator is in tools/validators/graph_validator.py
# Adjust import path if necessary, e.g. if tools is a top-level package
# For now, let's assume we might need to add tools to sys.path or structure differently
# For simplicity in this subtask, we'll try a direct relative import path if possible,
# or rely on Python's path if 'tools' is in PYTHONPATH.
# A more robust way would be to ensure 'tools' is an importable package.
# Let's assume for now that the Scribe engine or environment setup handles Python path.
try:
    from tools.validators.graph_validator import GraphValidator
except ImportError:
    # Fallback if 'tools' is not directly in path, try relative if scribe is run from repo root
    # This is a common challenge with scripts vs packages.
    # For a real Scribe engine, it would manage its environment.
    import sys
    # Assuming script is run from repo root, and 'tools' is a dir in repo root
    sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
    from tools.validators.graph_validator import GraphValidator


class GraphValidationAction(BaseAction):
    def __init__(self, action_config: dict, global_config: dict, logger=None):
        super().__init__(action_config, global_config, logger)
        self.schema_registry_path_str = self.action_config.get("schema_registry_path", "standards/registry/schema-registry.jsonld")
        self.master_index_path_str = self.action_config.get("master_index_path", "standards/registry/master-index.jsonld")
        self.shacl_shapes_path_str = self.action_config.get("shacl_shapes_path", "standards/registry/shacl-shapes.ttl")
        self.report_output_path_str = self.action_config.get("report_output_path", "scribe_validation_report.json")
        self.validator_instance = None

    def setup(self):
        if not super().setup():
            return False

        self.schema_registry_file = self.repo_root / self.schema_registry_path_str
        self.master_index_file = self.repo_root / self.master_index_path_str
        self.shacl_shapes_file = self.repo_root / self.shacl_shapes_path_str
        self.report_output_file = self.repo_root / self.report_output_path_str # Ensure report path is absolute or relative to repo_root

        # Validate paths
        if not self.schema_registry_file.exists():
            self.logger.error(f"Schema registry not found: {self.schema_registry_file}")
            return False
        if not self.master_index_file.exists(): # Master index might be created by a previous step, but path should be valid
            self.logger.warning(f"Master index path specified, but file may not exist yet: {self.master_index_file}")
        if not self.shacl_shapes_file.exists():
            self.logger.error(f"SHACL shapes file not found: {self.shacl_shapes_file}")
            return False

        # Ensure report output directory exists
        self.report_output_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Pass repo_root to GraphValidator, as it constructs absolute paths from it.
            self.validator_instance = GraphValidator(repo_base_path=str(self.repo_root))
            # Configure validator paths directly (GraphValidator's __init__ loads schema, but master_index is loaded later)
            # GraphValidator's internal paths are relative to its repo_base_path.
            # We need to ensure it uses the paths provided in this action's config if they differ from its defaults.
            # However, GraphValidator's current __init__ directly loads schema based on its internal logic.
            # And master_index is loaded via _load_master_index().
            # This action will primarily call validator.validate_all_documents() and validator.generate_validation_report()
            # The paths used by GraphValidator for schema, master_index, shacl are derived inside it using its self.registry_path.
            # To override, we'd need to modify GraphValidator or pass paths more directly.
            # For now, assume GraphValidator's default path construction (relative to its repo_root) is acceptable
            # as long as self.repo_root is correctly set for it.
            self.logger.info(f"GraphValidator instance created with repo_base_path: {self.repo_root}")
            self.logger.info(f"GraphValidator will use schema: {self.validator_instance.registry_path / 'schema-registry.jsonld'}")
            self.logger.info(f"GraphValidator will use master index: {self.validator_instance.registry_path / 'master-index.jsonld'}")
            self.logger.info(f"GraphValidator will use SHACL shapes from its internal shacl_shapes_path attribute if set, or its default logic.")

        except Exception as e:
            self.logger.error(f"Failed to initialize GraphValidator: {e}")
            return False

        self.logger.info("GraphValidationAction setup complete.")
        return True

    def execute(self, execution_context: dict) -> dict:
        self.logger.info(f"Executing GraphValidationAction. Context: {execution_context}")
        if not self.validator_instance:
            self.logger.error("GraphValidator instance not available. Setup might have failed.")
            return {'status': 'failure', 'message': "Setup failed: GraphValidator not initialized."}

        # Handle potential master_index_data from context (e.g., if index was just generated)
        # GraphValidator's _load_master_index currently reads from a file.
        # If master_index_data is in context, we'd ideally pass it to the validator.
        # This might require a small modification to GraphValidator or a temporary file write.
        # For now, assume GraphValidator reads from MASTER_INDEX_PATH as defined.
        if 'master_index_data' in execution_context and execution_context['master_index_data']:
            self.logger.info("Master index data found in execution_context. Current GraphValidator loads from file; this data is not directly used yet.")


        try:
            # The GraphValidator needs its internal master_index path to point to the correct file.
            # This is handled if self.repo_root passed to its constructor is correct.
            # GraphValidator also has its own _load_shacl_shapes which uses self.shacl_shapes_path.
            # We need to ensure GraphValidator uses the SHACL path from this action's config.
            # This might involve setting it on the instance if GraphValidator allows it.
            if hasattr(self.validator_instance, 'shacl_shapes_path'):
                 self.validator_instance.shacl_shapes_path = self.shacl_shapes_file # Override if possible
                 self.logger.info(f"Set GraphValidator.shacl_shapes_path to {self.shacl_shapes_file}")


            validation_errors = self.validator_instance.validate_all_documents() # This also generates relationships and SHACL errors
            report = self.validator_instance.generate_validation_report(validation_errors)

            # Save the report
            with open(self.report_output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Validation report saved to: {self.report_output_file}")

            error_count = report.get("total_errors", 0)
            # Assuming shacl_validation_errors is a list of strings within report['errors'] or a specific key
            # The current GraphValidator appends SHACL errors to the main 'errors' list.
            # And has a shacl_validation_errors list in its instance.
            shacl_error_count = 0
            if hasattr(self.validator_instance, 'shacl_validation_errors'):
                shacl_error_count = len(self.validator_instance.shacl_validation_errors)


            status = 'success'
            if error_count > 0:
                # Distinguish critical? For now, any error is non_critical failure for Scribe.
                # Critical failure might be if the validator itself crashes.
                status = 'failure_non_critical'

            return {
                'status': status,
                'message': f"Graph validation complete. Total errors: {error_count}. SHACL errors: {shacl_error_count}.",
                'report_path': str(self.report_output_file.relative_to(self.repo_root)),
                'error_count': error_count,
                'shacl_error_count': shacl_error_count,
                'raw_report': report # Optional: include full report data in context for other actions
            }

        except Exception as e:
            self.logger.exception(f"Error during graph validation: {e}")
            return {'status': 'failure_critical', 'message': f"Graph validation failed with exception: {e}"}

# Example usage (for testing)
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("GraphValidationActionTest")

    mock_global_config = {
        "repo_root": str(Path(__file__).resolve().parent.parent.parent)
    }
    mock_action_config = {
        "report_output_path": "temp_scribe_validation_report.json"
        # Paths for schema, master_index, shacl_shapes will use defaults relative to repo_root
    }

    # Ensure necessary files (schema, master_index, shacl) exist for testing
    # For this test, we assume they are in their default locations within the mock_repo_root
    # e.g., mock_repo_root/standards/registry/schema-registry.jsonld etc.
    # Actual testing would require these files to be present.

    action = GraphValidationAction(action_config=mock_action_config, global_config=mock_global_config, logger=logger)

    if action.setup():
        # Create dummy master-index if it doesn't exist for the test, to avoid setup failure for path check
        # This is a simplified test setup.
        mj_path = action.repo_root / action.action_config.get("master_index_path", "standards/registry/master-index.jsonld")
        mj_path.parent.mkdir(parents=True, exist_ok=True)
        if not mj_path.exists():
            with open(mj_path, 'w') as f:
                json.dump({"kb:documents":[]}, f) # Minimal master index
            logger.info(f"Created dummy master index for test: {mj_path}")


        test_context = {}
        result = action.execute(test_context)
        logger.info(f"Test execution result: {result}")

        # Clean up report
        if Path(result.get('report_path', '')).exists():
             Path(result['report_path']).unlink()
             logger.info(f"Cleaned up report: {result['report_path']}")
        elif (action.repo_root / mock_action_config['report_output_path']).exists():
             (action.repo_root / mock_action_config['report_output_path']).unlink()
             logger.info(f"Cleaned up report: {mock_action_config['report_output_path']}")


    else:
        logger.error("Test setup failed.")
