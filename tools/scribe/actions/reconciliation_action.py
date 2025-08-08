# tools/scribe/actions/reconciliation_action.py
import json
import os
import datetime
import yaml # Requires PyYAML
import hashlib
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Set, Tuple

from .base import BaseAction, ActionExecutionError
from tools.scribe.utils.frontmatter_parser import parse_frontmatter

# Helper functions (adapted from tools/indexer/generate_index.py)
# These can be static methods, part of a helper class, or module-level functions

def _calculate_content_hash(file_content: str) -> str:
    return hashlib.sha256(file_content.encode('utf-8')).hexdigest()

def _create_node_from_file(filepath_rel_to_repo: str, file_content: str, file_stats: os.stat_result) -> Dict[str, Any]:
    frontmatter = parse_frontmatter(file_content)
    content_hash = _calculate_content_hash(file_content)

    node = {
        "@type": "kb:Document",
        "@id": f"kb:doc-{filepath_rel_to_repo.replace('/', '-').replace('.md', '')}",
        "kb:filepath": filepath_rel_to_repo,
        "kb:contentHash": content_hash,
        "kb:fileSize": len(file_content),
        "kb:lastModified": datetime.datetime.fromtimestamp(file_stats.st_mtime, datetime.timezone.utc).isoformat(),
        "kb:indexed": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

    if frontmatter:
        for key, value in frontmatter.items():
            processed_key = key
            if key == '@id':
                node['@id'] = str(value)
                continue
            elif key == '@type':
                node['@type'] = str(value)
                continue
            elif ':' not in key:
                processed_key = f"kb:{key.replace('-', '_')}"
            elif key.startswith('kb:') and '-' in key:
                prefix, local_name = key.split(':', 1)
                processed_key = f"{prefix}:{local_name.replace('-', '_')}"

            if isinstance(value, datetime.datetime):
                node[processed_key] = value.isoformat()
            elif isinstance(value, datetime.date):
                node[processed_key] = value.isoformat() + "T00:00:00Z"
            else:
                node[processed_key] = value
    return node

class ReconciliationAction(BaseAction):
    def __init__(self, action_type: str, params: Dict[str, Any], plugin_context: 'PluginContextPort'):
        super().__init__(action_type, params, plugin_context)
        
        # HMA v2.2 compliant port-based access
        config_port = self.context.get_port("configuration")
        self.log_port = self.context.get_port("logging")
        
        self.master_index_path_str = self.params.get("master_index_path", "standards/registry/master-index.jsonld")
        self.kb_root_dirs_str = self.params.get("kb_root_dirs", ["."]) # Scan whole repo by default relative to repo_root
        self.exclude_dirs_set = set(self.params.get("exclude_dirs",
            ['.git', 'node_modules', '__pycache__', '.vscode', 'archive', 'tools', 'temp-naming-enforcer-test']))
        
        # Get repo root through configuration port
        try:
            self.repo_root = Path(config_port.get_config_value("repo_root", self.context.get_plugin_id(), "."))
        except Exception as e:
            self.log_port.log_warning("Could not get repo_root from config, using current directory", error=str(e))
            self.repo_root = Path(".")


    def setup(self):

        self.master_index_file = self.repo_root / self.master_index_path_str
        self.kb_root_paths = [self.repo_root / Path(p) for p in self.kb_root_dirs_str]

        for p_path in self.kb_root_paths:
             if not p_path.exists() or not p_path.is_dir():
                self.logger.error(f"Knowledge base scan directory not found or not a directory: {p_path}")
                return False
        self.logger.info(f"ReconciliationAction setup complete. Master index: {self.master_index_file}")
        return True

    def _load_existing_index(self) -> Dict[str, Any]:
        if self.master_index_file.exists():
            try:
                with open(self.master_index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                self.logger.warning(f"Could not load existing index: {e}. Creating new index.")

        return {
            "@context": ["contexts/base.jsonld", "contexts/fields.jsonld"], # Relative to registry
            "@type": "kb:MasterIndex", "@id": "kb:master-index",
            "kb:schemaVersion": "1.0.0", "kb:title": "Knowledge Base Master Index",
            "kb:created": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "kb:modified": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "kb:version": "1.0.0", "kb:documents": []
        }

    def _scan_knowledge_base(self) -> Dict[str, Dict[str, Any]]:
        found_files = {}
        for root_dir_path in self.kb_root_paths:
            self.logger.info(f"Scanning for .md files in: {root_dir_path}")
            for md_file in root_dir_path.rglob('*.md'):
                # Check if any part of the path is in exclude_dirs_set
                if any(excluded_part in md_file.relative_to(self.repo_root).parts for excluded_part in self.exclude_dirs_set):
                    continue

                rel_path_posix = md_file.relative_to(self.repo_root).as_posix()
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    found_files[rel_path_posix] = {'content': content, 'stats': md_file.stat()}
                except (IOError, UnicodeDecodeError) as e:
                    self.logger.warning(f"Could not read file {rel_path_posix}: {e}")
        self.logger.info(f"Scan found {len(found_files)} markdown files.")
        return found_files

    def _reconcile_index_logic(self, existing_index: Dict[str, Any], current_files: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, int]]:
        stats = {'added': 0, 'updated': 0, 'removed': 0, 'unchanged': 0}
        existing_docs_map = {doc['kb:filepath']: doc for doc in existing_index.get('kb:documents', [])}
        new_documents_list = []

        for filepath, file_info in current_files.items():
            content_hash = _calculate_content_hash(file_info['content'])
            if filepath in existing_docs_map:
                existing_doc = existing_docs_map[filepath]
                if existing_doc.get('kb:contentHash') != content_hash:
                    new_documents_list.append(_create_node_from_file(filepath, file_info['content'], file_info['stats']))
                    stats['updated'] += 1
                else:
                    new_documents_list.append(existing_doc)
                    stats['unchanged'] += 1
            else:
                new_documents_list.append(_create_node_from_file(filepath, file_info['content'], file_info['stats']))
                stats['added'] += 1

        current_filepaths_set = set(current_files.keys())
        for filepath in existing_docs_map.keys():
            if filepath not in current_filepaths_set:
                stats['removed'] += 1

        existing_index['kb:documents'] = new_documents_list
        existing_index['kb:modified'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        existing_index['kb:documentCount'] = len(new_documents_list)
        return existing_index, stats

    def _save_index(self, index_data: Dict[str, Any]) -> bool:
        try:
            self.master_index_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.master_index_file, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            self.logger.error(f"Error writing index file {self.master_index_file}: {e}")
            return False

    def execute(self, file_content: str, match, file_path: str, params: Dict[str, Any]) -> str:
        self.logger.info(f"Executing ReconciliationAction. Context: {params}")
        if not self.setup(): # Call setup if not already called or if it can be re-entrant
             raise ActionExecutionError(self.action_type, "Setup failed.")

        existing_index = self._load_existing_index()
        current_files = self._scan_knowledge_base()

        updated_index, stats = self._reconcile_index_logic(existing_index, current_files)

        if self._save_index(updated_index):
            msg = f"Reconciliation complete. Stats: Added {stats['added']}, Updated {stats['updated']}, Removed {stats['removed']}, Unchanged {stats['unchanged']}."
            self.logger.info(msg)
            return file_content
        else:
            msg = "Reconciliation failed: Could not save master index."
            self.logger.error(msg)
            raise ActionExecutionError(self.action_type, msg)

# Example usage (for testing, not part of the class itself)
if __name__ == '__main__':
    # This part is for direct testing of the action if needed
    # It won't run when Scribe imports the action
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("ReconciliationActionTest")

    # Mock global_config and action_config for testing
    mock_global_config = {
        "repo_root": str(Path(__file__).resolve().parent.parent.parent) # Assumes tools/scribe/actions structure
    }
    mock_action_config = {
        "master_index_path": "standards/registry/master-index.jsonld",
        "kb_root_dirs": ["kb", "standards/src"], # Example scan areas
        "exclude_dirs": ['.git', 'node_modules', 'archive', 'tools', 'temp-naming-enforcer-test']
    }

    action = ReconciliationAction(action_type="reconciliation", params=mock_action_config, config_manager=None, security_manager=None) # Mock ConfigManager and SecurityManager

    if action.setup():
        test_context = {} # Provide any necessary execution context
        result = action.execute(test_context)
        logger.info(f"Test execution result: {result}")
    else:
        logger.error("Test setup failed.")
