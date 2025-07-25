# tools/scribe/actions/naming_enforcement_action.py
import logging
from pathlib import Path
import sys
from typing import Dict, Any

from .base import BaseAction, ActionExecutionError

try:
    from tools.naming_enforcer.naming_enforcer import NamingEnforcerV2, SafetyLogger
except ImportError:
    # Fallback for path issues
    try:
        sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
        from tools.naming_enforcer.naming_enforcer import NamingEnforcerV2, SafetyLogger
    except ImportError:
        # Create mock classes for testing/development
        class NamingEnforcerV2:
            def __init__(self, *args, **kwargs):
                pass
            def enforce_naming(self, *args, **kwargs):
                return {"status": "skipped", "reason": "NamingEnforcer not available"}
        
        class SafetyLogger:
            def __init__(self, *args, **kwargs):
                pass
            def info(self, *args, **kwargs):
                pass
            def error(self, *args, **kwargs):
                pass

class NamingEnforcementAction(BaseAction):
    def __init__(self, action_type: str, params: Dict[str, Any], plugin_context):
        super().__init__(action_type, params, plugin_context)
        self.scan_paths_str = self.params.get("scan_paths", ["."]) # List of paths relative to repo_root
        self.schema_registry_path_str = self.params.get("schema_registry_path", "standards/registry/schema-registry.jsonld")
        self.fix_mode = self.params.get("fix_mode", False)
        # Naming Enforcer V2 auto-detects .namingignore, so explicit path might not be needed unless overridden
        self.namingignore_path_str = self.params.get("namingignore_path", None)
        self.enforcer_instance = None
        self.safety_logger_instance = None
        self.repo_root = Path(self.context.get_port("configuration").get_repo_root())

    def setup(self):
        if not super().setup():
            return False

        self.scan_paths = [self.repo_root / Path(p) for p in self.scan_paths_str]
        self.schema_registry_file = self.repo_root / self.schema_registry_path_str

        for sp in self.scan_paths:
            if not sp.exists():
                self.logger.error(f"Scan path not found: {sp}")
                return False

        if not self.schema_registry_file.exists():
            self.logger.error(f"Schema registry for naming enforcer not found: {self.schema_registry_file}")
            return False

        try:
            # NamingEnforcerV2's standard_path expects the path to the schema registry directly now
            self.enforcer_instance = NamingEnforcerV2(standard_path=str(self.schema_registry_file))

            # Configure include/exclude managers if paths are provided via action_config
            # NamingEnforcerV2's _load_automatic_files loads .namingignore from repo root or tool dir.
            # If specific ignore/include files are needed for this action, load them here.
            # For now, rely on its automatic detection or future config enhancements.
            if self.namingignore_path_str:
                 ignore_file = self.repo_root / self.namingignore_path_str
                 if ignore_file.exists():
                     self.enforcer_instance.exclude_manager.load_exclude_file(ignore_file)
                     self.logger.info(f"Loaded custom .namingignore from: {ignore_file}")
                 else:
                    self.logger.warning(f"Custom .namingignore file not found: {ignore_file}")

            # Setup SafetyLogger for fix mode
            if self.fix_mode:
                operation_name = f"scribe_naming_fix_{self.global_config.get('run_id', 'default')}"
                # SafetyLogger's __init__ sets up logging handlers.
                # Ensure this doesn't conflict with Scribe's main logger if Scribe has one.
                # It might be better if SafetyLogger could accept an existing logger.
                # For now, let it create its own as per its design.
                self.safety_logger_instance = SafetyLogger(operation_name=operation_name)
                self.logger.info(f"SafetyLogger initialized for fix mode: {operation_name}")

        except Exception as e:
            self.logger.exception(f"Failed to initialize NamingEnforcerV2: {e}")
            return False

        self.logger.info("NamingEnforcementAction setup complete.")
        return True

    def execute(self, file_content: str, match, file_path: str, params: Dict[str, Any]) -> str:
        self.logger.info(f"Executing NamingEnforcementAction. Context: {params}. Fix mode: {self.fix_mode}")
        if not self.enforcer_instance:
            self.logger.error("NamingEnforcerV2 instance not available. Setup might have failed.")
            raise ActionExecutionError(self.action_type, "Setup failed: NamingEnforcerV2 not initialized.")

        all_violations = []
        total_violations_count = 0
        scan_paths_to_process = self.scan_paths

        # Optionally refine scan_paths based on execution_context (e.g., changed_files)
        if "changed_files" in params and params["changed_files"]:
            # A more sophisticated approach might be needed here.
            # For now, if changed_files is present, we'll scan the unique parent directories.
            # Or, if NamingEnforcerV2 can take a list of files, that would be better.
            # Current NamingEnforcerV2.scan_directory takes a root_path.
            # We'll stick to the configured scan_paths but log the context.
            self.logger.info(f"Received changed_files in context: {params['changed_files']}. Scanning configured root paths.")


        for scan_path_root in scan_paths_to_process:
            self.logger.info(f"Scanning path: {scan_path_root}")
            # NamingEnforcerV2.scan_directory populates self.enforcer_instance.violations
            self.enforcer_instance.scan_directory(scan_path_root)
            all_violations.extend(self.enforcer_instance.violations) # Accumulate violations
            # Clear violations for next scan path if NamingEnforcerV2 accumulates them internally on instance
            self.enforcer_instance.violations = []

        total_violations_count = len(all_violations)
        # The NamingEnforcerV2.print_report() prints to stdout. We might want to capture this.
        # For Scribe, returning structured data is better.

        fixes_applied_count = 0
        if total_violations_count > 0:
            if self.fix_mode:
                if not self.safety_logger_instance:
                    self.logger.error("SafetyLogger not initialized for fix mode. Aborting fixes.")
                    return {'status': 'failure', 'message': "Fix mode error: SafetyLogger not initialized."}

                try:
                    self.logger.info(f"Attempting to fix {total_violations_count} violations.")
                    # Populate violations for the enforcer instance again, as they were cleared per scan_path_root loop
                    self.enforcer_instance.violations = all_violations
                    self.enforcer_instance.build_rename_operations() # Uses self.enforcer_instance.violations

                    # Backup files before modification (SafetyLogger handles this if files_to_backup is passed)
                    # This logic needs to be robust in NamingEnforcerV2 or adapted here.
                    # For now, assuming NamingEnforcerV2's existing backup logic within apply_... methods is sufficient.
                    # The SafetyLogger is passed to apply methods in NamingEnforcerV2.
                    # Here, we'd call the top-level fix application method of NamingEnforcerV2.

                    # The NamingEnforcerV2's main() has the fix logic. We need to replicate parts of it.
                    # NamingEnforcerV2.apply_frontmatter_fixes, .apply_content_updates, .apply_file_renames

                    fm_fixes = self.enforcer_instance.apply_frontmatter_fixes(self.safety_logger_instance, dry_run=False)
                    content_updates = self.enforcer_instance.apply_content_updates(self.safety_logger_instance, dry_run=False)
                    file_renames = self.enforcer_instance.apply_file_renames(self.safety_logger_instance, dry_run=False)
                    fixes_applied_count = fm_fixes + content_updates + file_renames # This is an approximation of "fixes"

                    self.safety_logger_instance.finalize_operation()
                    self.logger.info(f"Fix mode complete. Approximate fixes made: {fixes_applied_count}")
                    # Re-scan to confirm fixes (optional, or trust the fix counts)
                    # self.enforcer_instance.violations = []
                    # for scan_path_root in scan_paths_to_process:
                    #    self.enforcer_instance.scan_directory(scan_path_root)
                    # total_violations_count = len(self.enforcer_instance.violations)

                except Exception as e:
                    self.logger.exception(f"Error during fix application: {e}")
                    if self.safety_logger_instance: self.safety_logger_instance.finalize_operation()
                    raise ActionExecutionError(self.action_type, f"Error applying fixes: {e}", original_error=e)

            status = 'failure_violations_found' if total_violations_count > 0 and not self.fix_mode else 'success'
            if self.fix_mode and total_violations_count > 0 and fixes_applied_count < total_violations_count : # If fixes were attempted but some violations remain
                status = 'failure_violations_found' # Or a specific status like 'success_with_remaining_violations'
                raise ActionExecutionError(self.action_type, f"Naming enforcement scan complete. Violations found: {total_violations_count}. Fixes applied: {fixes_applied_count if self.fix_mode else 0}.")


            return file_content
        else:
            return file_content

# Example usage (for testing)
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("NamingEnforcementActionTest")

    mock_global_config = {
        "repo_root": str(Path(__file__).resolve().parent.parent.parent)
    }
    # Create a dummy test file with a violation for testing fix_mode
    test_dir = Path(mock_global_config["repo_root"]) / "temp_ne_test"
    test_dir.mkdir(exist_ok=True)
    violating_file = test_dir / "BadName.txt"
    with open(violating_file, "w") as f:
        f.write("test")

    mock_action_config_scan = {
        "scan_paths": ["temp_ne_test"], # Scan the temp directory
        "fix_mode": False
    }
    mock_action_config_fix = {
        "scan_paths": ["temp_ne_test"],
        "fix_mode": True
    }

    action_scan = NamingEnforcementAction(action_config=mock_action_config_scan, global_config=mock_global_config, logger=logger)
    if action_scan.setup():
        logger.info("--- SCAN MODE TEST ---")
        result_scan = action_scan.execute({})
        logger.info(f"Scan Test Result: {result_scan}")

    action_fix = NamingEnforcementAction(action_config=mock_action_config_fix, global_config=mock_global_config, logger=logger)
    if action_fix.setup():
        logger.info("--- FIX MODE TEST ---")
        result_fix = action_fix.execute({})
        logger.info(f"Fix Test Result: {result_fix}")

    # Cleanup
    import shutil
    shutil.rmtree(test_dir, ignore_errors=True)
    # SafetyLogger creates logs in master-knowledge-base/tools/reports, clean them up too if needed
    # For this test, we'll leave them.
    logger.info(f"Cleaned up test directory: {test_dir}")
