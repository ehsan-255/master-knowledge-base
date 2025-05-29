# kb_linter.py
# Knowledge Base Linter with enhanced validation, vocab loading, and error reporting.

import os
import re
import yaml 
from datetime import datetime
import json
from collections import defaultdict

# --- Configuration (Constants) ---
STANDARD_ID_REGEX = r"^[A-Z]{2}-[A-Z]{2,6}-[A-Z0-9\-]+$"
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
        self.domain_codes = [item['code'] for item in domain_codes_data.get('codes', []) if isinstance(item, dict) and 'code' in item]
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

    if file_content_raw is None:
        try:
            with open(filepath_abs, 'r', encoding='utf-8', newline='') as f: file_content_raw = f.read()
        except FileNotFoundError:
            errors.append({"message": "File not found.", "line": None}); return {"filepath": filepath_abs, "errors": errors, "warnings": warnings, "infos": infos, "standard_id": None}
        except UnicodeDecodeError:
            try:
                with open(filepath_abs, 'r', encoding='utf-8-sig') as f_sig: file_content_raw = f_sig.read()
                warnings.append({"message": "File is UTF-8 with BOM. Should be UTF-8 without BOM.", "line": 1})
            except: errors.append({"message": "File not UTF-8 or undecodable.", "line": None}); return {"filepath": filepath_abs, "errors": errors, "warnings": warnings, "infos": infos, "standard_id": None}
        except Exception as e: errors.append({"message": f"Error reading file: {e}", "line": None}); return {"filepath": filepath_abs, "errors": errors, "warnings": warnings, "infos": infos, "standard_id": None}

    if "\r\n" in file_content_raw: warnings.append({"message": "File contains CRLF line endings. Should use LF.", "line": None})
    elif "\r" in file_content_raw: warnings.append({"message": "File contains CR line endings. Should use LF.", "line": None})

    frontmatter_str, markdown_content, fm_content_start_line, fm_content_end_line = get_frontmatter_and_content(file_content_raw)

    if frontmatter_str is None:
        errors.append({"message": "No YAML frontmatter block found.", "line": 1})
        return {"filepath": filepath_abs, "errors": errors, "warnings": warnings, "infos": infos, "standard_id": None}

    frontmatter_data = None
    try:
        frontmatter_data = yaml.safe_load(frontmatter_str)
        if not isinstance(frontmatter_data, dict):
             errors.append({"message": "Frontmatter is not a valid YAML mapping.", "line": fm_content_start_line}); frontmatter_data = {} 
    except yaml.YAMLError as e:
        err_line = (e.problem_mark.line + 1 if hasattr(e, 'problem_mark') and e.problem_mark else 0) + fm_content_start_line -1
        errors.append({"message": f"Invalid YAML syntax: {e.problem}", "line": err_line})
        return {"filepath": filepath_abs, "errors": errors, "warnings": warnings, "infos": infos, "standard_id": None}

    current_info_type = frontmatter_data.get("info-type")
    mandatory_keys = MANDATORY_KEYS_FOR_STANDARD_DEFINITION if current_info_type == "standard-definition" else MANDATORY_KEYS_BASE
    for key in mandatory_keys:
        if key not in frontmatter_data:
            errors.append({"message": f"Mandatory key '{key}' missing.", "line": fm_content_start_line -1 })
    
    actual_keys = list(frontmatter_data.keys())
    present_defined_keys = [k for k in DEFINED_KEY_ORDER if k in actual_keys]
    
    current_order_of_present_defined_keys = [k for k in actual_keys if k in expected_order_indices]

    if current_order_of_present_defined_keys != present_defined_keys:
        for i in range(len(current_order_of_present_defined_keys)):
            actual_key = current_order_of_present_defined_keys[i]
            expected_key_at_this_pos = present_defined_keys[i]
            if actual_key != expected_key_at_this_pos:
                key_line = get_line_number_of_key(frontmatter_str, actual_key, fm_content_start_line)
                warnings.append({
                    "message": f"Key order issue: Key '{actual_key}' found. Expected '{expected_key_at_this_pos}' at this position relative to other defined keys. Current order of defined keys found: {current_order_of_present_defined_keys}",
                    "line": key_line
                })
                break # Report first discrepancy in ordered subset

    for key, expected_type in EXPECTED_TYPES.items():
        if key in frontmatter_data:
            value = frontmatter_data[key]
            key_line = get_line_number_of_key(frontmatter_str, key, fm_content_start_line)
            if not isinstance(value, expected_type):
                actual_type = type(value).__name__
                errors.append({"message": f"Key '{key}' has value '{value}' of type '{actual_type}'. Expected type '{expected_type.__name__}'.", "line": key_line})
            elif expected_type == list: # Check item types for lists
                 for item_idx, item in enumerate(value):
                     if not isinstance(item, str):
                        errors.append({"message": f"Item '{item}' at index {item_idx} in list key '{key}' is type '{type(item).__name__}'. Expected 'str'.", "line": key_line})


    if "standard_id" in frontmatter_data:
        std_id = frontmatter_data.get("standard_id") # Use get to avoid error if key was removed due to type error
        key_line = get_line_number_of_key(frontmatter_str, "standard_id", fm_content_start_line)
        if isinstance(std_id, str): 
            extracted_standard_id = std_id 
            if not re.match(STANDARD_ID_REGEX, std_id):
                errors.append({"message": f"'standard_id' ('{std_id}') fails regex: '{STANDARD_ID_REGEX}'.", "line": key_line})
            filename_base = os.path.splitext(os.path.basename(filepath_abs))[0]
            if filename_base != std_id:
                warnings.append({"message": f"Filename '{filename_base}.md' should match 'standard_id' '{std_id}'.", "line": key_line })
    
    for dk in ["date-created", "date-modified"]:
        key_line = get_line_number_of_key(frontmatter_str, dk, fm_content_start_line)
        if dk in frontmatter_data and isinstance(frontmatter_data[dk], str):
            if not re.match(ISO_DATE_REGEX, frontmatter_data[dk]):
                 errors.append({"message": f"'{dk}' ('{frontmatter_data[dk]}') invalid ISO-8601 (YYYY-MM-DDTHH:MM:SSZ).", "line": key_line })
            else: 
                try: datetime.strptime(frontmatter_data[dk][:-1], "%Y-%m-%dT%H:%M:%S")
                except ValueError: errors.append({"message": f"'{dk}' ('{frontmatter_data[dk]}') invalid date/time values for ISO-8601.", "line": key_line })

    # Vocabulary checks using LinterConfig
    pd_value = frontmatter_data.get("primary_domain")
    pd_line = get_line_number_of_key(frontmatter_str, "primary_domain", fm_content_start_line)
    if pd_value and pd_value not in config.domain_codes:
        errors.append({"message": f"'primary_domain' ('{pd_value}') not in defined domain_codes.", "line": pd_line })
    
    sd_value = frontmatter_data.get("sub_domain")
    sd_line = get_line_number_of_key(frontmatter_str, "sub_domain", fm_content_start_line)
    if pd_value and sd_value and config.subdomain_registry: # Ensure subdomain_registry loaded
        if pd_value in config.subdomain_registry:
            if sd_value not in config.subdomain_registry[pd_value]:
                errors.append({"message": f"'sub_domain' ('{sd_value}') not valid for domain '{pd_value}'.", "line": sd_line })
        # else: # primary_domain itself is invalid, already caught

    it_value = frontmatter_data.get("info-type")
    it_line = get_line_number_of_key(frontmatter_str, "info-type", fm_content_start_line)
    if it_value and it_value not in config.info_types:
        errors.append({"message": f"'info-type' ('{it_value}') not in defined list.", "line": it_line })

    crit_value = frontmatter_data.get("criticality")
    crit_line = get_line_number_of_key(frontmatter_str, "criticality", fm_content_start_line)
    if crit_value and crit_value not in config.criticality_levels:
        errors.append({"message": f"'criticality' ('{crit_value}') not in defined list.", "line": crit_line })

    lg_value = frontmatter_data.get("lifecycle_gatekeeper")
    lg_line = get_line_number_of_key(frontmatter_str, "lifecycle_gatekeeper", fm_content_start_line)
    if lg_value and lg_value not in config.lifecycle_gatekeepers:
         warnings.append({"message": f"'lifecycle_gatekeeper' ('{lg_value}') not in defined list.", "line": lg_line })

    tags_value = frontmatter_data.get("tags")
    tags_line = get_line_number_of_key(frontmatter_str, "tags", fm_content_start_line)
    if tags_value and isinstance(tags_value, list): # Type check for tags itself done earlier
        for tag_idx, tag in enumerate(tags_value):
            if isinstance(tag, str): # Type check for items in list
                if not re.match(KEBAB_CASE_TAG_REGEX, tag):
                    warnings.append({"message": f"Tag '{tag}' (at index {tag_idx}) invalid kebab-case/structure.", "line": tags_line })
                if not any(tag.startswith(cat) for cat in config.tag_categories):
                     warnings.append({"message": f"Tag '{tag}' (at index {tag_idx}) has unrecognized category prefix.", "line": tags_line })
            # else: item type error already caught by general type checking for lists
    
    cl_url = frontmatter_data.get("change_log_url")
    cl_line = get_line_number_of_key(frontmatter_str, "change_log_url", fm_content_start_line)
    if isinstance(cl_url, str):
        if cl_url.startswith("./"):
            doc_dir = os.path.dirname(filepath_abs)
            abs_path = os.path.normpath(os.path.join(doc_dir, cl_url))
            if not os.path.exists(abs_path):
                errors.append({"message": f"Relative 'change_log_url' non-existent: {cl_url} (abs: {abs_path})", "line": cl_line })
        elif cl_url.startswith("http://") or cl_url.startswith("https://"):
            if "://" not in cl_url or " " in cl_url: warnings.append({"message": f"Absolute 'change_log_url' syntax questionable: {cl_url}", "line": cl_line })
        
    content_lines = markdown_content.splitlines(True)
    for i, line_text in enumerate(content_lines):
        for match in re.finditer(INTERNAL_LINK_REGEX, line_text):
            target, anchor, _, _, alias = match.groups() 
            link_line_num = fm_content_end_line + i + 1 # Add 1 because fm_content_end_line is the '---' line
            if "/" in target or target.endswith(".md"):
                warnings.append({"message": f"Path-based link '[[{match.group(0)}]]'. Use '[[STANDARD_ID]]'.", "line": link_line_num })
            elif re.match(STANDARD_ID_REGEX, target) and target not in config.standards_index: # Check if it's an ID and if it's broken
                warnings.append({"message": f"Broken link? '[[{target}]]' not in standards_index.", "line": link_line_num })
                
    return {"filepath": filepath_abs, "errors": errors, "warnings": warnings, "infos": infos, "standard_id": extracted_standard_id}


def lint_directory(dir_path, config: LinterConfig):
    # ... (same as previous version, ensure it uses config.repo_base for relpath)
    all_results = []
    seen_standard_ids = defaultdict(list)

    abs_dir_path = os.path.abspath(dir_path)
    if not os.path.isdir(abs_dir_path):
        print(f"Error: Directory not found: {abs_dir_path}")
        return []

    for root, _, files in os.walk(abs_dir_path):
        for file in files:
            if file.endswith(".md"):
                filepath_abs = os.path.join(root, file)
                # Report with path relative to repo_base for consistency
                rel_filepath_from_repo_root = os.path.relpath(filepath_abs, config.repo_base).replace(os.sep, '/')
                
                result = lint_file(filepath_abs, config) # Pass absolute path for file operations
                result["filepath"] = rel_filepath_from_repo_root 
                
                if result.get("standard_id"): # standard_id might be None if not found or invalid
                    seen_standard_ids[result["standard_id"]].append(rel_filepath_from_repo_root)
                all_results.append(result)
    
    # Standard ID Uniqueness Check
    for std_id, filepaths in seen_standard_ids.items():
        if len(filepaths) > 1:
            # This error needs to be added to each file's result object
            for fp_with_duplicate in filepaths:
                for res_idx, res_item in enumerate(all_results):
                    if res_item["filepath"] == fp_with_duplicate:
                        other_fps = [f for f in filepaths if f != fp_with_duplicate]
                        all_results[res_idx]["errors"].append({
                            "message": f"Duplicate 'standard_id' '{std_id}' also found in: {', '.join(other_fps)}",
                            "line": get_line_number_of_key(res_item.get("_fm_str_cache",""), "standard_id", res_item.get("_fm_start_line_cache",1)) # Requires caching fm_str
                        })
                        break
    return all_results


def main():
    # Assume script is run from the repository root for correct relative pathing.
    repo_base_abs_path = os.path.abspath(".") 
    config = LinterConfig(repo_base_path=repo_base_abs_path)
    
    # Ensure dependent files for testing are present or handled if missing by loaders
    # Example: Create a dummy standards_index.json if it's missing and critical for a test run
    dummy_index_path = os.path.join(config.dist_path, "standards_index.json")
    if not os.path.exists(dummy_index_path):
        os.makedirs(config.dist_path, exist_ok=True)
        with open(dummy_index_path, "w") as f:
            json.dump({"schemaVersion": "1.0.0", "generatedDate": datetime.now(datetime.timezone.utc).isoformat(), "standards": [
                {"standard_id": "AS-SCHEMA-CONCEPT-DEFINITION", "title": "Concept Definition Schema", "filepath": "master-knowledge-base/standards/src/AS-SCHEMA-CONCEPT-DEFINITION.md"}
            ]}, f)
        print(f"Created dummy {dummy_index_path} for linter testing.")


    standards_src_dir = os.path.join("master-knowledge-base", "standards", "src") 
    
    dummy_files_to_create = {
        "XX-LINT-TESTDUMMY1.md": """---
title: Dummy Test One (Correct ID)
standard_id: XX-LINT-TESTDUMMY1
info-type: standard-definition
version: '1.0'
date-created: 2023-01-01T00:00:00Z
date-modified: 2023-01-01T00:00:00Z
primary_domain: AS 
sub_domain: SCHEMA
criticality: P1-High
tags: [status/draft, topic/testing]
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
title: Dummy Test Two (Duplicate ID)
standard_id: XX-LINT-TESTDUMMY1 
info-type: policy-document # Not a standard-def, so fewer mandatory fields initially
version: '0.1.0'
date-created: 2023-02-02T00:00:00Z
date-modified: 2023-02-02T00:00:00Z
tags: [status/approved]
primary-topic: Test 2
kb-id: kb-id/test
scope_application: Test scope 2
criticality: P2-Medium
lifecycle_gatekeeper: SME-Consensus
impact_areas: ['test2']
title: This is out of order # Key order error, also duplicate title key (YAML parser might handle it)
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
primary_domain: CS
sub_domain: POLICY
criticality: P3-Low
tags: [status/draft]
change_log_url: ./changelog.md
primary-topic: Test 3
kb-id: kb-id/test
scope_application: Test scope 3
lifecycle_gatekeeper: No-Gatekeeper
impact_areas: ['test3']
---
Content.
"""
    }
    
    # Create dummy files
    for fname, content in dummy_files_to_create.items():
        fpath = os.path.join(repo_base_abs_path, standards_src_dir, fname)
        with open(fpath, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        # Create dummy changelog for the first dummy file if referenced
        if fname == "XX-LINT-TESTDUMMY1.md" and "change_log_url: ./XX-LINT-TESTDUMMY1-changelog.md" in content:
            with open(os.path.join(repo_base_abs_path, standards_src_dir, "XX-LINT-TESTDUMMY1-changelog.md"), "w") as cf:
                cf.write("# Changelog")


    print(f"Starting Knowledge Base Linter (Fully Enhanced) on {os.path.abspath(standards_src_dir)}...")
    
    results_list = lint_directory(standards_src_dir, config)
    total_errors = 0
    total_warnings = 0

    for results in results_list:
        filepath_to_display = results['filepath']
        # Only print details if there are issues, or for specific test files
        if results["errors"] or results["warnings"] or "TESTDUMMY" in filepath_to_display.upper() or "BAD_FILENAME" in filepath_to_display.upper() :
            print(f"\n--- Results for {filepath_to_display} ---")
            if results["infos"]:
                print("Infos:")
                for item in results["infos"]: print(f"  - [L{item.get('line', 'N/A')}] {item['message']}")
            if results["warnings"]:
                print("Warnings:")
                for item in results["warnings"]: print(f"  - [L{item.get('line', 'N/A')}] {item['message']}")
                total_warnings += len(results["warnings"])
            if results["errors"]:
                print("Errors:")
                for item in results["errors"]: print(f"  - [L{item.get('line', 'N/A')}] {item['message']}")
                total_errors += len(results["errors"])
            if not results["errors"] and not results["warnings"] and not results["infos"]:
                print("No issues found.")
    
    print(f"\n--- Linting Summary ---")
    print(f"Total files processed: {len(results_list)}")
    print(f"Total errors found: {total_errors}")
    print(f"Total warnings found: {total_warnings}")

    # Clean up dummy files
    for fname in dummy_files_to_create.keys():
        fpath = os.path.join(repo_base_abs_path, standards_src_dir, fname)
        if os.path.exists(fpath): os.remove(fpath)
    changelog_dummy = os.path.join(repo_base_abs_path, standards_src_dir, "XX-LINT-TESTDUMMY1-changelog.md")
    if os.path.exists(changelog_dummy): os.remove(changelog_dummy)
    print(f"\nCleaned up dummy files.")

if __name__ == "__main__":
    main()
