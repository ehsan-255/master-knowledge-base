# tools/scribe/actions/base_action.py
import logging
from pathlib import Path

class BaseAction:
    def __init__(self, action_config: dict, global_config: dict, logger=None):
        self.action_config = action_config
        self.global_config = global_config
        self.logger = logger or logging.getLogger(self.__class__.__name__)
        # Ensure repo_root is a Path object and defaults sensibly
        repo_root_path = self.global_config.get("repo_root", ".")
        if not isinstance(repo_root_path, Path):
            repo_root_path = Path(repo_root_path)
        self.repo_root = repo_root_path.resolve()
        self.logger.info(f"BaseAction initialized with repo_root: {self.repo_root}")


    def setup(self):
        self.logger.info(f"Setting up {self.__class__.__name__}")
        # Basic validation of repo_root
        if not self.repo_root.exists() or not self.repo_root.is_dir():
            self.logger.error(f"Repository root not found or not a directory: {self.repo_root}")
            return False
        return True

    def execute(self, execution_context: dict) -> dict:
        raise NotImplementedError

    def cleanup(self):
        self.logger.info(f"Cleaning up {self.__class__.__name__}")
