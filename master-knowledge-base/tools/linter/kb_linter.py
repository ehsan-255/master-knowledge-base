# kb_linter.py
# Knowledge Base Linter with enhanced validation, vocab loading, and error reporting.

import os
import re
import yaml
from datetime import datetime, timezone # Import timezone
import json
from collections import defaultdict
import argparse # For CI-friendliness
import sys # For CI-friendliness

# --- Configuration (Constants) ---
STANDARD_ID_REGEX = r"^[A-Z]{2}-[A-Z]{2,15}-[A-Z0-9\-]+$" # Updated to allow longer sub-domains
ISO_DATE_REGEX = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
KEBAB_CASE_TAG_REGEX = r"^[a-z0-9]+(-[a-z0-9]+)*(/[a-z0-9]+(-[a-z0-9]+)*)*$"
INTERNAL_LINK_REGEX = r"\[\[([^\]#\|]+)(?:#([^\]\|]+))?(?:\|([^\]]+))?\]\]" 

DEFINED_KEY_ORDER = [
    "title", "standard_id", "aliases", "tags", "kb-id", "info-type",
    "primary-topic", "related-standards", "version", "date-created",
    "date-modified", "primary_domain", "sub_domain", "scope_application",
    "criticality", "lifecycle_gatekeeper", "impact_areas", "change_log_url"
]

MANDATORY_KEYS_BASE = [
    "title", "info-type", "version", "date-created", "date-modified", 
    "primary-topic", "kb-id", "tags", "scope_application", 
    "criticality", "lifecycle_gatekeeper", "impact_areas"
]
MANDATORY_KEYS_FOR_STANDARD_DEFINITION = MANDATORY_KEYS_BASE + [
    "standard_id", "primary_domain", "sub_domain", "change_log_url"
]

EXPECTED_TYPES = {
    "title": str, "standard_id": str, "aliases": list, "tags": list,
    "kb-id": str, "info-type": str, "primary-topic": str, "related-standards": list,
    "version": str, "date-created": str, "date-modified": str,
    "primary_domain": str, "sub_domain": str, "scope_application": str,
    "criticality": str, "lifecycle_gatekeeper": str, "impact_areas": list,
    "change_log_url": str
}

# --- LinterConfig Class ---
class LinterConfig:
    def __init__(self, repo_base_path="."):
        self.repo_base = os.path.abspath(repo_base_path)
        self.registry_path = os.path.join(self.repo_base, "master-knowledge-base", "standards", "registry")
        self.dist_path = os.path.join(self.repo_base, "master-knowledge-base", "dist")

        # Load YAML Vocabularies
        domain_codes_data = self._load_yaml_vocab(os.path.join(self.registry_path, "domain_codes.yaml"))
        # Corrected parsing based on actual domain_codes.yaml structure
        self.domain_codes = [item['id'] for item in domain_codes_data.get('entries', []) if isinstance(item, dict) and 'id' in item]
        self.subdomain_registry = self._load_yaml_vocab(os.path.join(self.registry_path, "subdomain_registry.yaml"))
        if not isinstance(self.subdomain_registry, dict): self.subdomain_registry = {}


        # Load Standards Index
        self.standards_index = self._load_standards_index(os.path.join(self.dist_path, "standards_index.json"))
        
        # Load TXT Vocabularies
        self.info_types = self._load_txt_vocab(os.path.join(self.registry_path, "info_types.txt"))
        self.criticality_levels = self._load_txt_vocab(os.path.join(self.registry_path, "criticality_levels.txt"))
        self.lifecycle_gatekeepers = self._load_txt_vocab(os.path.join(self.registry_path, "lifecycle_gatekeepers.txt"))
        self.tag_categories = self._load_txt_vocab(os.path.join(self.registry_path, "tag_categories.txt"))

        # TODO: Dynamic Vocabulary Loading Strategy from Markdown (as comments)
        # (Retain comments from previous version about dynamic parsing strategy)
        # For MT-SCHEMA-FRONTMATTER.md (info-type list):
        #   1. Read 'MT-SCHEMA-FRONTMATTER.md'.
        #   2. Locate the specific H3 section, e.g., "### `info-type`".
        #   3. Parse the subsequent bulleted list. Extract terms.
        # For MT-REGISTRY-TAG-GLOSSARY.md (tag categories, criticality, lifecycle_gatekeeper):
        #   1. Read 'MT-REGISTRY-TAG-GLOSSARY.md'.
        #   2. For tag categories: Find H3 headings like "### Status Tags (`status/*`)"
        #      Use regex to extract the "status/" part.
        #   3. For criticality/lifecycle: Find H3 headings like "### Criticality Tags (`criticality/*`)"
        #      Parse subsequent list items (e.g., "- `criticality/P0-Critical`: Description") to get the full tag.

    def _load_yaml_vocab(self, filepath, list_key=None, extract_key=None):
        try:
            abs_filepath = os.path.join(self.repo_base, filepath) if not os.path.isabs(filepath) else filepath
            if not os.path.exists(abs_filepath):
                print(f"Warning: Vocab file not found: {abs_filepath}")
                return {} if list_key is None and not extract_key else []
            with open(abs_filepath, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if list_key: 
                    data = data.get(list_key, [])
                    if extract_key: 
                        return [item[extract_key] for item in data if isinstance(item, dict) and extract_key in item]
                return data if data is not None else ({} if list_key is None and not extract_key else [])
        except Exception as e:
            print(f"Warning: Failed to load/parse YAML vocab {filepath}: {e}")
            return {} if list_key is None and not extract_key else []

    def _load_txt_vocab(self, filepath):
        try:
            abs_filepath = os.path.join(self.repo_base, filepath) if not os.path.isabs(filepath) else filepath
            if not os.path.exists(abs_filepath):
                print(f"Warning: Vocab file not found: {abs_filepath}")
                return []
            with open(abs_filepath, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip() and not line.startswith("#")]
        except Exception as e:
            print(f"Warning: Failed to load .txt vocab {filepath}: {e}")
            return []

    def _load_standards_index(self, index_path):
        try:
            abs_filepath = os.path.join(self.repo_base, index_path) if not os.path.isabs(index_path) else index_path
            if not os.path.exists(abs_filepath):
                print(f"Warning: Standards index not found: {abs_filepath}. Link checking will be limited.")
                return {}
            with open(abs_filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {std["standard_id"]: std for std in data.get("standards", []) if "standard_id" in std}
        except Exception as e:
            print(f"Warning: Failed to load/parse standards index {index_path}: {e}")
            return {}

# --- Helper Functions ---
def get_frontmatter_and_content(file_content):
    lines = file_content.splitlines(True) 
    if not lines or not lines[0].startswith("---"):
        return None, file_content, 0, 0 
    fm_end_index = -1
    fm_start_line_num = 1 
    for i, line in enumerate(lines[1:], start=1): 
        if line.startswith("---"):
            fm_end_index = i
            break
    if fm_end_index == -1: return None, file_content, 0, 0
    
    frontmatter_str = "".join(lines[1:fm_end_index])
    content_str = "".join(lines[fm_end_index+1:])
    return frontmatter_str, content_str, fm_start_line_num + 1, fm_start_line_num + fm_end_index

def get_line_number_of_key(frontmatter_str, key, fm_content_start_line):
    """Approximates line number of a key in the original document."""
    for i, line in enumerate(frontmatter_str.splitlines()):
        if line.strip().startswith(key + ":"):
            return fm_content_start_line + i
    return fm_content_start_line # Default to start of FM content if key not found (e.g. for missing key)


# --- Linter Core Function ---
def lint_file(filepath_abs, config: LinterConfig, file_content_raw=None):
    errors, warnings, infos = [], [], []
    extracted_standard_id = None
    # Cache for duplicate ID line number reporting
    fm_str_cache = None
    fm_content_start_line_cache = 0

    if file_content_raw is None:
        try:
            with open(filepath_abs, 'r', encoding='utf-8', newline='') as f: file_content_raw = f.read()
        except FileNotFoundError:
            errors.append({"message": "File not found.", "line": None}); return {"filepath": filepath_abs, "errors": errors, "warnings": warnings, "infos": infos, "standard_id": None, "_fm_str_cache": None, "_fm_content_start_line_cache": 0}
        except UnicodeDecodeError:
            try:
                with open(filepath_abs, 'r', encoding='utf-8-sig') as f_sig: file_content_raw = f_sig.read()
                warnings.append({"message": "File is UTF-8 with BOM. Should be UTF-8 without BOM.", "line": 1})
            except: errors.append({"message": "File not UTF-8 or undecodable.", "line": None}); return {"filepath": filepath_abs, "errors": errors, "warnings": warnings, "infos": infos, "standard_id": None, "_fm_str_cache": None, "_fm_content_start_line_cache": 0}
        except Exception as e: errors.append({"message": f"Error reading file: {e}", "line": None}); return {"filepath": filepath_abs, "errors": errors, "warnings": warnings, "infos": infos, "standard_id": None, "_fm_str_cache": None, "_fm_content_start_line_cache": 0}

    if "\r\n" in file_content_raw: warnings.append({"message": "File contains CRLF line endings. Should use LF.", "line": None})
    elif "\r" in file_content_raw: warnings.append({"message": "File contains CR line endings. Should use LF.", "line": None})

    frontmatter_str, markdown_content, fm_content_start_line, fm_content_end_line = get_frontmatter_and_content(file_content_raw)
    fm_str_cache = frontmatter_str # Cache for later use
    fm_content_start_line_cache = fm_content_start_line

    if frontmatter_str is None:
        errors.append({"message": "No YAML frontmatter block found.", "line": 1})
        return {"filepath": filepath_abs, "errors": errors, "warnings": warnings, "infos": infos, "standard_id": None, "_fm_str_cache": fm_str_cache, "_fm_content_start_line_cache": fm_content_start_line_cache}

    frontmatter_data = None
    try:
        frontmatter_data = yaml.safe_load(frontmatter_str)
        if not isinstance(frontmatter_data, dict):
             errors.append({"message": "Frontmatter is not a valid YAML mapping.", "line": fm_content_start_line}); frontmatter_data = {}
    except yaml.YAMLError as e:
        err_line = (e.problem_mark.line + 1 if hasattr(e, 'problem_mark') and e.problem_mark else 0) + fm_content_start_line -1
        errors.append({"message": f"Invalid YAML syntax: {e.problem}", "line": err_line})
        return {"filepath": filepath_abs, "errors": errors, "warnings": warnings, "infos": infos, "standard_id": None, "_fm_str_cache": fm_str_cache, "_fm_content_start_line_cache": fm_content_start_line_cache}

    current_info_type = frontmatter_data.get("info-type")
    mandatory_keys = MANDATORY_KEYS_FOR_STANDARD_DEFINITION if current_info_type == "standard-definition" else MANDATORY_KEYS_BASE
    for key in mandatory_keys:
        if key not in frontmatter_data:
            errors.append({"message": f"Mandatory key '{key}' missing.", "line": fm_content_start_line -1 })

    # Key order validation (refined)
    actual_keys_in_doc = list(frontmatter_data.keys())
    # Filter to keys that are in DEFINED_KEY_ORDER, maintaining the order they appear in the document
    keys_in_doc_for_order_check = [k for k in actual_keys_in_doc if k in DEFINED_KEY_ORDER]

    last_defined_idx = -1
    first_violation_reported = False
    for key_in_doc in keys_in_doc_for_order_check:
        try:
            current_defined_idx = DEFINED_KEY_ORDER.index(key_in_doc)
            if current_defined_idx < last_defined_idx:
                # Find the key from DEFINED_KEY_ORDER that was violated
                # This means `key_in_doc` appeared too early relative to `DEFINED_KEY_ORDER[last_defined_idx]`
                # or `DEFINED_KEY_ORDER[last_defined_idx]` appeared too late relative to `key_in_doc`
                problem_key = key_in_doc
                expected_after_key = DEFINED_KEY_ORDER[last_defined_idx] # The key that current key should be after

                # Attempt to find what key should have been at this position based on DEFINED_KEY_ORDER
                # Find index of `expected_after_key` in `keys_in_doc_for_order_check`
                idx_of_expected_after_key_in_doc = -1
                try:
                    idx_of_expected_after_key_in_doc = keys_in_doc_for_order_check.index(expected_after_key)
                except ValueError:
                    pass # Should not happen

                expected_key_at_problem_pos_in_doc = ""
                # Find what key *should* have been at the position of problem_key
                # This involves mapping DEFINED_KEY_ORDER to the subset present in the document
                
                # Simplified message:
                key_line = get_line_number_of_key(frontmatter_str, problem_key, fm_content_start_line)
                warnings.append({
                    "message": f"Key order issue: Key '{problem_key}' (defined order index {current_defined_idx}) is before key '{expected_after_key}' (defined order index {last_defined_idx}), violating defined relative order.",
                    "line": key_line
                })
                first_violation_reported = True
                break 
            last_defined_idx = current_defined_idx
        except ValueError:
            # This key from the document isn't in DEFINED_KEY_ORDER, so it's not part of this specific check.
            # Extraneous keys might be caught by other checks if desired.
            pass
    
    for key, expected_type in EXPECTED_TYPES.items():
        if key in frontmatter_data:
            value = frontmatter_data[key]
            key_line = get_line_number_of_key(frontmatter_str, key, fm_content_start_line)
            if not isinstance(value, expected_type):
                actual_type = type(value).__name__
                errors.append({"message": f"Key '{key}' has value '{value}' of type '{actual_type}'. Expected type '{expected_type.__name__}'.", "line": key_line})
            elif expected_type == list: # Check item types for lists
                 for item_idx, item in enumerate(value):
                     if not isinstance(item, str): # Assuming all list items for defined keys are strings
                        errors.append({"message": f"Item '{item}' at index {item_idx} in list key '{key}' is type '{type(item).__name__}'. Expected 'str'.", "line": key_line})


    if "standard_id" in frontmatter_data:
        std_id_val = frontmatter_data.get("standard_id") # Use get to avoid error if key was removed due to type error
        key_line = get_line_number_of_key(frontmatter_str, "standard_id", fm_content_start_line)
        if isinstance(std_id_val, str): 
            extracted_standard_id = std_id_val 
            if not re.match(STANDARD_ID_REGEX, std_id_val):
                errors.append({"message": f"'standard_id' ('{std_id_val}') fails regex: '{STANDARD_ID_REGEX}'.", "line": key_line})
            filename_base = os.path.splitext(os.path.basename(filepath_abs))[0]
            if filename_base != std_id_val:
                warnings.append({"message": f"Filename '{filename_base}.md' should match 'standard_id' '{std_id_val}'.", "line": key_line })
    
    for dk in ["date-created", "date-modified"]:
        key_line = get_line_number_of_key(frontmatter_str, dk, fm_content_start_line)
        date_val = frontmatter_data.get(dk)
        if date_val is not None: # Check if key exists
            if isinstance(date_val, str):
                if not re.match(ISO_DATE_REGEX, date_val):
                    errors.append({"message": f"'{dk}' ('{date_val}') invalid ISO-8601 (YYYY-MM-DDTHH:MM:SSZ).", "line": key_line })
                else: 
                    try: datetime.strptime(date_val[:-1], "%Y-%m-%dT%H:%M:%S") # Check if date part is valid
                    except ValueError: errors.append({"message": f"'{dk}' ('{date_val}') invalid date/time values for ISO-8601.", "line": key_line })
            # else: Type error already caught

    # Vocabulary checks using LinterConfig (ensure key exists before getting value)
    if "primary_domain" in frontmatter_data:
        pd_value = frontmatter_data["primary_domain"]
        pd_line = get_line_number_of_key(frontmatter_str, "primary_domain", fm_content_start_line)
        if pd_value not in config.domain_codes: # Assuming domain_codes is a list/set
            errors.append({"message": f"'primary_domain' ('{pd_value}') not in defined domain_codes. Valid: {config.domain_codes}", "line": pd_line })
        
        if "sub_domain" in frontmatter_data:
            sd_value = frontmatter_data["sub_domain"]
            sd_line = get_line_number_of_key(frontmatter_str, "sub_domain", fm_content_start_line)
            # Check if pd_value is a key in the subdomain_registry dictionary
            if pd_value in config.subdomain_registry:
                # Then check if sd_value is in the list associated with that key
                # Assuming subdomain_registry structure is { "DOMAIN_CODE": ["SUB_CODE1", "SUB_CODE2"], ... }
                # This needs to be adjusted if subdomain_registry structure is different, e.g. list of dicts
                valid_subdomains_for_domain = []
                for item in config.subdomain_registry.get(pd_value, []): # Iterate through list of dicts for the domain
                    if isinstance(item, dict) and 'code' in item:
                        valid_subdomains_for_domain.append(item['code'])

                if sd_value not in valid_subdomains_for_domain:
                    errors.append({"message": f"'sub_domain' ('{sd_value}') not valid for domain '{pd_value}'. Valid: {valid_subdomains_for_domain}", "line": sd_line })
            elif pd_value: # If primary_domain was valid but not found in subdomain_registry (problem with registry load or content)
                 warnings.append({"message": f"Primary domain '{pd_value}' not found in subdomain registry structure for sub_domain check.", "line": sd_line})


    if "info-type" in frontmatter_data:
        it_value = frontmatter_data["info-type"]
        it_line = get_line_number_of_key(frontmatter_str, "info-type", fm_content_start_line)
        if it_value not in config.info_types:
            errors.append({"message": f"'info-type' ('{it_value}') not in defined list. Valid: {config.info_types}", "line": it_line })

    if "criticality" in frontmatter_data:
        crit_value = frontmatter_data["criticality"]
        crit_line = get_line_number_of_key(frontmatter_str, "criticality", fm_content_start_line)
        if crit_value not in config.criticality_levels:
            errors.append({"message": f"'criticality' ('{crit_value}') not in defined list. Valid: {config.criticality_levels}", "line": crit_line })

    if "lifecycle_gatekeeper" in frontmatter_data:
        lg_value = frontmatter_data["lifecycle_gatekeeper"]
        lg_line = get_line_number_of_key(frontmatter_str, "lifecycle_gatekeeper", fm_content_start_line)
        if lg_value not in config.lifecycle_gatekeepers:
            warnings.append({"message": f"'lifecycle_gatekeeper' ('{lg_value}') not in defined list. Valid: {config.lifecycle_gatekeepers}", "line": lg_line })

    if "tags" in frontmatter_data:
        tags_value = frontmatter_data["tags"]
        tags_line = get_line_number_of_key(frontmatter_str, "tags", fm_content_start_line)
        if isinstance(tags_value, list): # Type check for tags itself done earlier
            for tag_idx, tag in enumerate(tags_value):
                if isinstance(tag, str): # Type check for items in list
                    if not re.match(KEBAB_CASE_TAG_REGEX, tag):
                        warnings.append({"message": f"Tag '{tag}' (at index {tag_idx}) invalid kebab-case/structure.", "line": tags_line })
                    # Check against loaded tag categories (prefixes)
                    if not any(tag.startswith(cat_prefix) for cat_prefix in config.tag_categories):
                        warnings.append({"message": f"Tag '{tag}' (at index {tag_idx}) has unrecognized category prefix. Valid prefixes: {config.tag_categories}", "line": tags_line })
                # else: item type error already caught by general type checking for lists
    
    if "change_log_url" in frontmatter_data:
        cl_url = frontmatter_data["change_log_url"]
        cl_line = get_line_number_of_key(frontmatter_str, "change_log_url", fm_content_start_line)
        if isinstance(cl_url, str):
            if cl_url.startswith("./"):
                doc_dir = os.path.dirname(filepath_abs)
                abs_path = os.path.normpath(os.path.join(doc_dir, cl_url))
                if not os.path.exists(abs_path):
                    errors.append({"message": f"Relative 'change_log_url' non-existent: {cl_url} (resolved: {abs_path})", "line": cl_line })
            elif not (cl_url.startswith("http://") or cl_url.startswith("https://")):
                 warnings.append({"message": f"Non-relative 'change_log_url' should be an absolute HTTP(S) URL: {cl_url}", "line": cl_line })
            elif " " in cl_url : warnings.append({"message": f"Absolute 'change_log_url' syntax questionable (contains space): {cl_url}", "line": cl_line })
        
    content_lines = markdown_content.splitlines(True)
    for i, line_text in enumerate(content_lines):
        for match in re.finditer(INTERNAL_LINK_REGEX, line_text):
            target_link, anchor, display_text = match.groups() # Adjusted group unpacking
            link_line_num = fm_content_end_line + i + 1 
            if "/" in target_link or target_link.endswith(".md"):
                warnings.append({"message": f"Path-based link '[[{match.group(0)}]]'. Use '[[STANDARD_ID]]' or '[[STANDARD_ID#Anchor|Display Text]]'.", "line": link_line_num })
            elif re.match(STANDARD_ID_REGEX, target_link):
                 if target_link not in config.standards_index:
                    warnings.append({"message": f"Potentially broken link: Standard ID '[[{target_link}]]' not found in standards_index.json.", "line": link_line_num })
            # Else: could be a plain text [[bracketed phrase]], not necessarily an ID. Or an anchor to current doc.
                
    return {"filepath": filepath_abs, "errors": errors, "warnings": warnings, "infos": infos, "standard_id": extracted_standard_id, "_fm_str_cache": fm_str_cache, "_fm_content_start_line_cache": fm_content_start_line_cache}


def lint_directory(dir_path, config: LinterConfig):
    # Ensure config.repo_base is used for consistent relative paths
    all_results = []
    seen_standard_ids = defaultdict(list)

    # Use absolute path for initial directory walk
    abs_dir_path = os.path.join(config.repo_base, dir_path) if not os.path.isabs(dir_path) else dir_path
    
    if not os.path.isdir(abs_dir_path):
        # This case should ideally be handled by the caller or main function
        # For robustness, let's add a print statement and return empty
        print(f"Error: Directory not found: {abs_dir_path}")
        return []

    for root, _, files in os.walk(abs_dir_path):
        for file in files:
            if file.endswith(".md"):
                filepath_abs = os.path.join(root, file)
                # Report with path relative to repo_base for consistency
                rel_filepath_from_repo_root = os.path.relpath(filepath_abs, config.repo_base).replace(os.sep, '/')
                
                result = lint_file(filepath_abs, config)
                result["filepath"] = rel_filepath_from_repo_root 
                
                if result.get("standard_id"):
                    seen_standard_ids[result["standard_id"]].append(result) # Store full result for caching
                all_results.append(result)
    
    # Standard ID Uniqueness Check
    for std_id, results_with_id in seen_standard_ids.items():
        if len(results_with_id) > 1:
            filepaths_with_duplicate = [res["filepath"] for res in results_with_id]
            for res_item in results_with_id: # Iterate through the result objects that have this duplicate ID
                other_fps = [f for f in filepaths_with_duplicate if f != res_item["filepath"]]
                # Use cached frontmatter string and start line from the result object
                fm_str = res_item.get("_fm_str_cache", "") # Default to empty string if not found
                fm_start_line = res_item.get("_fm_content_start_line_cache", 1) # Default to 1
                
                res_item["errors"].append({
                    "message": f"Duplicate 'standard_id' '{std_id}' also found in: {', '.join(other_fps)}",
                    "line": get_line_number_of_key(fm_str, "standard_id", fm_start_line) 
                })
    return all_results


def main():
    parser = argparse.ArgumentParser(description="Knowledge Base Linter")
    parser.add_argument("--directory", default="master-knowledge-base/standards/src",
                        help="Directory to lint (relative to repository root). Default: master-knowledge-base/standards/src")
    parser.add_argument("--output", help="File to write the linter report to (Markdown format).")
    parser.add_argument("--fail-on-errors", action="store_true", help="Exit with a non-zero status code if errors are found.")
    parser.add_argument("--repo-base", default=".", help="Path to the repository root. Default is current directory.")

    args = parser.parse_args()

    repo_base_abs_path = os.path.abspath(args.repo_base)
    config = LinterConfig(repo_base_path=repo_base_abs_path)
    
    lint_target_dir_rel = args.directory
    lint_target_dir_abs = os.path.join(repo_base_abs_path, lint_target_dir_rel)

    # Check if target directory exists before proceeding
    if not os.path.isdir(lint_target_dir_abs):
        print(f"Error: Target directory for linting not found: {lint_target_dir_abs}")
        sys.exit(1) # Exit if directory doesn't exist

    # Remove dummy file creation unless specifically testing the main() without args
    # For CI, dummy files are not needed as it will lint actual files.
    create_dummies_for_testing = not (sys.argv[1:] and args.directory != "master-knowledge-base/standards/src") # Basic check if run with default dir and no other args

    dummy_files_created_paths = []
    if create_dummies_for_testing:
        print("Running in local test mode with dummy files as no specific directory was provided beyond default.")
        dummy_index_path = os.path.join(config.dist_path, "standards_index.json")
        if not os.path.exists(dummy_index_path): # Only create if indexer hasn't run
            os.makedirs(config.dist_path, exist_ok=True)
            with open(dummy_index_path, "w") as f:
                # Corrected datetime.now(datetime.timezone.utc) to datetime.now(timezone.utc)
                json.dump({"schemaVersion": "1.0.0", "generatedDate": datetime.now(timezone.utc).isoformat(), "standards": [
                    {"standard_id": "AS-SCHEMA-CONCEPT-DEFINITION", "title": "Concept Definition Schema", "filepath": "master-knowledge-base/standards/src/AS-SCHEMA-CONCEPT-DEFINITION.md"},
                    {"standard_id": "AS-SCHEMA-TASK", "title": "Task Schema", "filepath": "master-knowledge-base/standards/src/AS-SCHEMA-TASK.md"}
                ]}, f)
            print(f"Created dummy {dummy_index_path} for linter testing.")
        else:
            print(f"Using existing standards_index.json found at {dummy_index_path}")

        dummy_files_to_create = {
            "XX-LINT-TESTDUMMY1.md": """---
title: Dummy Test One (Correct ID)
standard_id: XX-LINT-TESTDUMMY1
info-type: standard-definition
version: '1.0'
date-created: 2023-01-01T00:00:00Z
date-modified: 2023-01-01T00:00:00Z
primary_domain: AS 
sub_domain: SCHEMA # Make sure this is valid for AS in your test registry
criticality: P1-High
tags: [status/draft, topic/testing, kb-id/test]
change_log_url: ./XX-LINT-TESTDUMMY1-changelog.md 
primary-topic: Test
kb-id: kb-id/test
scope_application: Test scope
lifecycle_gatekeeper: Architect-Review
impact_areas: ['test']
aliases: ["one", "two"]
related-standards: ["AS-SCHEMA-TASK"]
---
Content of dummy 1. [[AS-SCHEMA-CONCEPT-DEFINITION]]
""",
            "XX-LINT-TESTDUMMY2.md": """---
title: Dummy Test Two (Duplicate ID) # Key order error - title is not first
standard_id: XX-LINT-TESTDUMMY1 
info-type: policy-document
version: '0.1.0'
date-created: 2023-02-02T00:00:00Z
date-modified: 2023-02-02T00:00:00Z
tags: [status/approved, kb-id/test]
primary-topic: Test 2
kb-id: kb-id/test
scope_application: Test scope 2
criticality: P2-Medium
lifecycle_gatekeeper: SME-Consensus
impact_areas: ['test2']
---
Content of dummy 2. [[XX-LINT-TESTDUMMY1#some-anchor]]
""",
            "bad_filename_id_mismatch.md": """---
title: Filename Mismatch Test
standard_id: XX-CORRECT-ID-001
info-type: standard-definition
version: '1.0'
date-created: 2023-03-03T00:00:00Z
date-modified: 2023-03-03T00:00:00Z
primary_domain: CS # Make sure this is valid
sub_domain: POLICY # Make sure this is valid for CS
criticality: P3-Low
tags: [status/draft, kb-id/test]
change_log_url: ./changelog.md
primary-topic: Test 3
kb-id: kb-id/test
scope_application: Test scope 3
lifecycle_gatekeeper: No-Gatekeeper # Check if this is in your vocab
impact_areas: ['test3']
---
Content.
"""
        }
        
        target_dummy_dir = os.path.join(repo_base_abs_path, lint_target_dir_rel)
        os.makedirs(target_dummy_dir, exist_ok=True) # Ensure dummy dir exists

        for fname, content in dummy_files_to_create.items():
            fpath = os.path.join(target_dummy_dir, fname)
            dummy_files_created_paths.append(fpath)
            with open(fpath, "w", encoding="utf-8", newline="\n") as f: f.write(content)
            if fname == "XX-LINT-TESTDUMMY1.md" and "change_log_url: ./XX-LINT-TESTDUMMY1-changelog.md" in content:
                cl_path = os.path.join(target_dummy_dir, "XX-LINT-TESTDUMMY1-changelog.md")
                dummy_files_created_paths.append(cl_path)
                with open(cl_path, "w") as cf: cf.write("# Changelog")
        print(f"Created dummy files in {target_dummy_dir}")


    print(f"Starting Knowledge Base Linter on {lint_target_dir_abs}...")
    
    results_list = lint_directory(lint_target_dir_rel, config) # Pass relative path to lint_directory
    total_errors = 0
    total_warnings = 0
    report_content = "# Linter Report\n\n"

    for results in results_list:
        filepath_to_display = results['filepath']
        # Only print details if there are issues, or for specific test files
        # if results["errors"] or results["warnings"] or (create_dummies_for_testing and ("TESTDUMMY" in filepath_to_display.upper() or "BAD_FILENAME" in filepath_to_display.upper())):
        if results["errors"] or results["warnings"]: # Simpler: always add to report if issues
            report_content += f"\n## File: `{filepath_to_display}`\n"
            print(f"\n--- Results for {filepath_to_display} ---")
            if results["infos"]:
                report_content += "### Infos:\n"
                print("Infos:")
                for item in results["infos"]: 
                    msg_line = f"  - [L{item.get('line', 'N/A')}] {item['message']}\n"
                    print(msg_line.strip())
                    report_content += msg_line
            if results["warnings"]:
                report_content += "### Warnings:\n"
                print("Warnings:")
                for item in results["warnings"]: 
                    msg_line = f"  - [L{item.get('line', 'N/A')}] {item['message']}\n"
                    print(msg_line.strip())
                    report_content += msg_line
                total_warnings += len(results["warnings"])
            if results["errors"]:
                report_content += "### Errors:\n"
                print("Errors:")
                for item in results["errors"]:
                    msg_line = f"  - [L{item.get('line', 'N/A')}] {item['message']}\n"
                    print(msg_line.strip())
                    report_content += msg_line
                total_errors += len(results["errors"])
            if not results["errors"] and not results["warnings"] and not results["infos"] and (create_dummies_for_testing and ("TESTDUMMY" in filepath_to_display.upper() or "BAD_FILENAME" in filepath_to_display.upper())):
                print("No issues found.")
                report_content += "- No issues found.\n"
    
    summary_section = f"\n---\n## Linting Summary\n"
    summary_section += f"- Total files processed: {len(results_list)}\n"
    summary_section += f"- Total errors found: {total_errors}\n"
    summary_section += f"- Total warnings found: {total_warnings}\n"
    
    print(summary_section)
    report_content += summary_section

    if args.output:
        output_path_abs = os.path.join(repo_base_abs_path, args.output)
        with open(output_path_abs, "w", encoding="utf-8") as f_report:
            f_report.write(report_content)
        print(f"\nLinter report written to: {output_path_abs}")

    if create_dummies_for_testing:
        for path_to_remove in dummy_files_created_paths:
            if os.path.exists(path_to_remove):
                os.remove(path_to_remove)
        print(f"Cleaned up dummy files.")
        # Also remove dummy index if it was created by this test run
        if not os.path.exists(os.path.join(config.dist_path, "standards_index.json.original")): # cheap check
             if os.path.exists(dummy_index_path): os.remove(dummy_index_path)


    if args.fail_on_errors and total_errors > 0:
        print("\nExiting with non-zero status due to errors.")
        sys.exit(1)

if __name__ == "__main__":
    main()
