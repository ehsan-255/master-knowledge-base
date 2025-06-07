# kb_linter.py
# Knowledge Base Linter with enhanced validation, vocab loading, and error reporting.

import os
import re
import yaml
from datetime import datetime, timezone # Import timezone
import json
from collections import defaultdict
import argparse # For CI-friendliness
from pathlib import Path # Added for robust path handling
import sys # For CI-friendliness
import time # For adding a small delay

# --- Configuration (Constants) ---
STANDARD_ID_REGEX = r"^[A-Z]{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*$" # Agreed: All UPPERCASE, Domain-RestOfID structure
ISO_DATE_REGEX = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
KEBAB_CASE_TAG_REGEX = r"^[a-z0-9]+(-[a-z0-9]+)*(/[a-z0-9]+(-[a-z0-9]+)*)*$"
INTERNAL_LINK_REGEX = r"\[\[([^\]#\|]+)(?:#([^\]\|]+))?(?:\|([^\]]+))?\]\]" 

DEFINED_KEY_ORDER = [
    "title", "standard_id", "aliases", "tags", "kb-id", "info-type",
    "primary-topic", "related-standards", "version", "date-created",
    "date-modified", "primary_domain", "sub_domain", "scope_application",
    "criticality", "lifecycle_gatekeeper", "impact_areas"
]

MANDATORY_KEYS_BASE = [
    "title", "info-type", "version", "date-created", "date-modified", 
    "primary-topic", "kb-id", "tags", "scope_application", 
    "criticality", "lifecycle_gatekeeper", "impact_areas"
]
MANDATORY_KEYS_FOR_STANDARD_DEFINITION_POLICY = MANDATORY_KEYS_BASE + [
    "standard_id", "primary_domain", "sub_domain"
]

EXPECTED_TYPES = {
    "title": str, "standard_id": str, "aliases": list, "tags": list,
    "kb-id": str, "info-type": str, "primary-topic": str, "related-standards": list,
    "version": str, "date-created": str, "date-modified": str,
    "primary_domain": str, "sub_domain": str, "scope_application": str,
    "criticality": str, "lifecycle_gatekeeper": str, "impact_areas": list,
    # Collection document specific fields
    "description": str, "date_generated": str, "source_collection_definition_id": str,
    "number_of_standards": int
}

# --- LinterConfig Class ---
class LinterConfig:
    def __init__(self, repo_base_path="."):
        print(f"DEBUG LinterConfig: Initial repo_base_path: {repo_base_path}")
        # Correct repo_base detection
        raw_repo_base = Path(repo_base_path).resolve()
        if not (raw_repo_base / "master-knowledge-base" / "standards").exists() and (raw_repo_base / "standards").exists():
             # Likely running from inside master-knowledge-base
             self.repo_base = raw_repo_base
        elif (raw_repo_base / "master-knowledge-base").is_dir():
            # Likely running from one level above master-knowledge-base
            self.repo_base = raw_repo_base / "master-knowledge-base"
        else:
            # Fallback or if structure is unexpected
            self.repo_base = raw_repo_base
            # Check if we need to append master-knowledge-base
            if not (self.repo_base / "standards" / "registry").exists() and (Path(repo_base_path) / "master-knowledge-base" / "standards" / "registry").exists():
                 self.repo_base = Path(repo_base_path).resolve() / "master-knowledge-base"


        print(f"DEBUG LinterConfig: self.repo_base (resolved): {self.repo_base}")

        self.registry_path = self.repo_base / "standards" / "registry"
        self.schema_yaml_path = self.registry_path / "mt-schema-frontmatter.yaml"
        self.tag_glossary_yaml_path = self.registry_path / "mt-registry-tag-glossary.yaml"

        # Load consolidated YAMLs first
        self.frontmatter_schema_data = self._load_yaml_vocab(str(self.schema_yaml_path)) # Use str() for os.path.exists in _load_yaml_vocab
        self.tag_glossary_data = self._load_yaml_vocab(str(self.tag_glossary_yaml_path)) # Use str() for os.path.exists

        # Extract vocabularies from consolidated files
        cv_data = self.frontmatter_schema_data.get('controlled_vocabularies', {})

        self.domain_codes = [item['id'] for item in cv_data.get('primary_domain', []) if isinstance(item, dict) and 'id' in item]
        self.subdomain_registry = cv_data.get('sub_domain', {}) # This is already a dict keyed by primary_domain
        if not isinstance(self.subdomain_registry, dict): self.subdomain_registry = {}

        self.info_types = cv_data.get('info_type', [])

        # For 'criticality' field validation (e.g., "P0-Critical")
        self.criticality_levels_yaml = [item['level'] for item in cv_data.get('criticality', []) if isinstance(item, dict) and 'level' in item]

        # For 'lifecycle_gatekeeper' field validation
        self.lifecycle_gatekeepers = [item['gatekeeper'] for item in cv_data.get('lifecycle_gatekeeper', []) if isinstance(item, dict) and 'gatekeeper' in item]

        # For tag category prefix validation (e.g., "status/", "topic/")
        self.tag_categories_prefixes = []
        if self.tag_glossary_data and 'tag_categories' in self.tag_glossary_data:
            for cat_info in self.tag_glossary_data['tag_categories'].values():
                if isinstance(cat_info, dict) and cat_info.get('prefix'):
                    self.tag_categories_prefixes.append(cat_info['prefix'])

        # For criticality/* tag value validation (e.g., "p0-critical")
        self.criticality_tag_values = []
        if self.tag_glossary_data and 'tag_categories' in self.tag_glossary_data:
            crit_tags = self.tag_glossary_data['tag_categories'].get('criticality', {}).get('tags', [])
            for tag_item in crit_tags:
                if isinstance(tag_item, dict) and 'full_tag' in tag_item:
                    # Extract value like "p0-critical" from "criticality/P0-Critical"
                    # The tag value in frontmatter is expected to be P0-Critical, so we take field_value and lowercase.
                    # Or, if we use full_tag, "criticality/P0-Critical" -> "p0-critical"
                    tag_value = tag_item.get('field_value', tag_item['full_tag'].split('/')[-1])
                    self.criticality_tag_values.append(tag_value.lower())

        # Audience types and Maturity levels (loaded but not yet used in existing lint checks)
        self.audience_types = [item['id'] for item in cv_data.get('audience_type', []) if isinstance(item, dict) and 'id' in item]
        self.maturity_levels = [item['id'] for item in cv_data.get('maturity_level', []) if isinstance(item, dict) and 'id' in item]

        # Load Standards Index (existing logic)
        dist_path_local = os.path.join(self.repo_base, "dist")
        print(f"DEBUG LinterConfig: local dist_path_local for index: {dist_path_local}")
        time.sleep(0.1) # Small delay to help with potential filesystem sync issues
        os.makedirs(dist_path_local, exist_ok=True) # Ensure dist directory is accessible
        full_index_path = os.path.join(dist_path_local, "standards_index.json")
        print(f"DEBUG LinterConfig: Attempting to load index directly from: {full_index_path}")
        self.standards_index = self._load_standards_index(full_index_path)

        # Decision for Phase B: Rely on .txt/.yaml registry files for vocabularies.
        # Defer complex Markdown-based vocabulary loading.
        # THIS COMMENT IS NOW OUTDATED AS WE LOAD FROM CONSOLIDATED YAMLS.
        # TODO: (Post-Phase B) Re-evaluate dynamic vocabulary loading from Markdown if needed for flexibility.
        # Original TODO comments related to parsing MD files are now less relevant.

    def _load_yaml_vocab(self, filepath, list_key=None, extract_key=None): # Modified to be more generic
        try:
            abs_filepath = os.path.join(self.repo_base, filepath) if not os.path.isabs(filepath) else filepath
            if not os.path.exists(abs_filepath):
                print(f"Warning: Vocab file not found: {abs_filepath}")
                return {} # Return a dict for schema/glossary, or an empty dict if expecting a dict
            with open(abs_filepath, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                # The following logic for list_key/extract_key might be too specific for the main YAMLs
                # and can be handled by the caller if needed, or removed if not used by main YAML loading.
                # For now, let's assume the main YAMLs are loaded as whole dicts.
                # if list_key:
                #     data = data.get(list_key, [])
                #     if extract_key:
                #         return [item[extract_key] for item in data if isinstance(item, dict) and extract_key in item]
                return data if data is not None else {}
        except Exception as e:
            print(f"Warning: Failed to load/parse YAML vocab {filepath}: {e}")
            return {} # Return empty dict on error

    def _load_standards_index(self, index_file_abs_path): # Now expects an absolute path
        try:
            if not os.path.exists(index_file_abs_path):
                print(f"DEBUG _load_standards_index: os.path.exists returned False for: {index_file_abs_path}") # Added debug
                print(f"Warning: Standards index not found: {index_file_abs_path}. Link checking will be limited.")
                return {}
            with open(index_file_abs_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {std["standard_id"]: std for std in data.get("standards", []) if "standard_id" in std}
        except Exception as e:
            print(f"Warning: Failed to load/parse standards index {index_file_abs_path}: {e}") # Use abs_filepath in error
            return {}

# --- Helper Functions ---

def is_placeholder_value(value_str):
    if not isinstance(value_str, str):
        return False
    value_str = value_str.strip()
    if value_str.startswith("[") and value_str.endswith("]"):
        return True
    if value_str == "YYYY-MM-DDTHH:MM:SSZ" or value_str == "YYYY-MM-DD":
        return True
    if value_str.upper().startswith("XX-") or "PLACEHOLDER" in value_str.upper() or "TBD" in value_str.upper():
        return True
    return False

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


def lint_file(filepath_abs, config: LinterConfig, file_content_raw=None):
    errors, warnings, infos = [], [], []
    extracted_standard_id = None
    fm_str_cache = None
    fm_content_start_line_cache = 0

    normalized_filepath_for_template_check = filepath_abs.replace(os.sep, '/')
    is_template_file = "master-knowledge-base/standards/templates/" in normalized_filepath_for_template_check or                        os.path.basename(normalized_filepath_for_template_check).startswith("tpl-")

    if is_template_file:
        # infos.append({"message": "Applying template-specific linting rules.", "line": 1}) # Optional: too verbose for now
        pass

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

    # Fix line endings automatically
    if "\r\n" in file_content_raw or "\r" in file_content_raw:
        # Convert CRLF or CR to LF
        fixed_content = file_content_raw.replace("\r\n", "\n").replace("\r", "\n")
        try:
            with open(filepath_abs, 'w', encoding='utf-8', newline='\n') as f:
                f.write(fixed_content)
            infos.append({"message": "Fixed line endings: converted CRLF/CR to LF.", "line": None})
            file_content_raw = fixed_content  # Use fixed content for further processing
        except Exception as e:
            warnings.append({"message": f"Failed to fix line endings: {e}", "line": None})

    frontmatter_str, markdown_content, fm_content_start_line, fm_content_end_line = get_frontmatter_and_content(file_content_raw)
    fm_str_cache = frontmatter_str
    fm_content_start_line_cache = fm_content_start_line

    if frontmatter_str is None:
        is_readme = os.path.basename(normalized_filepath_for_template_check).upper() == "README.MD"
        is_tool_subfile = "master-knowledge-base/tools/" in normalized_filepath_for_template_check
        is_report_file = "master-knowledge-base/tools/reports/" in normalized_filepath_for_template_check
        is_standards_templates_readme = "master-knowledge-base/standards/templates/README.md" == normalized_filepath_for_template_check
        is_standards_readme = "master-knowledge-base/standards/README.md" == normalized_filepath_for_template_check

        # Exempt READMEs in tools, reports, and standards/templates from requiring frontmatter
        # Also exempt the main standards README.
        if not (is_readme and (is_tool_subfile or is_report_file or is_standards_templates_readme or is_standards_readme)):
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
    if current_info_type in ["standard-definition", "policy-document"]:
        mandatory_keys = MANDATORY_KEYS_FOR_STANDARD_DEFINITION_POLICY
    elif current_info_type == "collection-document":
        # Collection documents have different mandatory fields - they are auto-generated derived views
        mandatory_keys = ["title", "info-type", "tags", "description", "date_generated"]
    else:
        mandatory_keys = MANDATORY_KEYS_BASE
    
    for key in mandatory_keys:
        if key not in frontmatter_data:
            if not (is_template_file and key not in ["title", "standard_id", "info-type"]): # Allow most mandatory keys to be missing in templates
                errors.append({"message": f"Mandatory key '{key}' missing.", "line": fm_content_start_line -1 })

    actual_keys_in_doc = list(frontmatter_data.keys())
    keys_in_doc_for_order_check = [k for k in actual_keys_in_doc if k in DEFINED_KEY_ORDER]
    last_defined_idx = -1
    for key_in_doc in keys_in_doc_for_order_check:
        try:
            current_defined_idx = DEFINED_KEY_ORDER.index(key_in_doc)
            if current_defined_idx < last_defined_idx:
                problem_key = key_in_doc
                expected_after_key = DEFINED_KEY_ORDER[last_defined_idx]
                key_line = get_line_number_of_key(frontmatter_str, problem_key, fm_content_start_line)
                warnings.append({
                    "message": f"Key order issue: Key '{problem_key}' (defined order index {current_defined_idx}) is before key '{expected_after_key}' (defined order index {last_defined_idx}), violating defined relative order.",
                    "line": key_line
                })
            last_defined_idx = current_defined_idx
        except ValueError:
            pass
    
    for key, expected_type in EXPECTED_TYPES.items():
        if key in frontmatter_data:
            value = frontmatter_data[key]
            key_line = get_line_number_of_key(frontmatter_str, key, fm_content_start_line)
            if is_template_file and is_placeholder_value(str(value)):
                continue
            if not isinstance(value, expected_type):
                actual_type = type(value).__name__
                errors.append({"message": f"Key '{key}' has value '{value}' of type '{actual_type}'. Expected type '{expected_type.__name__}'.", "line": key_line})
            elif expected_type == list:
                 for item_idx, item in enumerate(value):
                     if not isinstance(item, str):
                         if not (is_template_file and is_placeholder_value(str(item))):
                            errors.append({"message": f"Item '{item}' at index {item_idx} in list key '{key}' is type '{type(item).__name__}'. Expected 'str'.", "line": key_line})

    if "standard_id" in frontmatter_data:
        std_id_val = frontmatter_data.get("standard_id")
        key_line = get_line_number_of_key(frontmatter_str, "standard_id", fm_content_start_line)
        if isinstance(std_id_val, str): 
            extracted_standard_id = std_id_val 
            if not (is_template_file and is_placeholder_value(std_id_val)):
                if not re.match(STANDARD_ID_REGEX, std_id_val):
                    errors.append({"message": f"'standard_id' ('{std_id_val}') fails regex: '{STANDARD_ID_REGEX}'.", "line": key_line})

            filename_base = os.path.splitext(os.path.basename(filepath_abs))[0]
            if not (is_template_file and is_placeholder_value(std_id_val)):
                if filename_base != std_id_val:
                    warnings.append({"message": f"Filename '{filename_base}.md' should match 'standard_id' '{std_id_val}'.", "line": key_line })
    
    for dk in ["date-created", "date-modified"]:
        key_line = get_line_number_of_key(frontmatter_str, dk, fm_content_start_line)
        date_val = frontmatter_data.get(dk)
        if date_val is not None:
            if isinstance(date_val, str):
                if not (is_template_file and is_placeholder_value(date_val)):
                    if not re.match(ISO_DATE_REGEX, date_val):
                        errors.append({"message": f"'{dk}' ('{date_val}') invalid ISO-8601 (YYYY-MM-DDTHH:MM:SSZ).", "line": key_line })
                    else:
                        try: datetime.strptime(date_val[:-1], "%Y-%m-%dT%H:%M:%S")
                        except ValueError: errors.append({"message": f"'{dk}' ('{date_val}') invalid date/time values for ISO-8601.", "line": key_line })

    if "primary_domain" in frontmatter_data:
        pd_value = frontmatter_data.get("primary_domain")
        pd_line = get_line_number_of_key(frontmatter_str, "primary_domain", fm_content_start_line)
        if not (is_template_file and is_placeholder_value(pd_value)):
            if pd_value not in config.domain_codes: # Uses new self.domain_codes
                errors.append({"message": f"'primary_domain' ('{pd_value}') not in defined domain_codes. Valid: {config.domain_codes}", "line": pd_line })
        
        if "sub_domain" in frontmatter_data:
            sd_value = frontmatter_data.get("sub_domain")
            sd_line = get_line_number_of_key(frontmatter_str, "sub_domain", fm_content_start_line)
            if not (is_template_file and is_placeholder_value(sd_value)):
                if pd_value in config.subdomain_registry: # Uses new self.subdomain_registry
                    # Ensure that the items in the subdomain registry for the given pd_value are dictionaries with a 'code' key
                    valid_subdomains_for_domain = [
                        item['code'] for item in config.subdomain_registry.get(pd_value, [])
                        if isinstance(item, dict) and 'code' in item
                    ]
                    if sd_value not in valid_subdomains_for_domain:
                        errors.append({"message": f"'sub_domain' ('{sd_value}') not valid for domain '{pd_value}'. Valid: {valid_subdomains_for_domain}", "line": sd_line })
                elif pd_value and not (is_template_file and is_placeholder_value(pd_value)): # pd_value exists and is not a placeholder
                     warnings.append({"message": f"Primary domain '{pd_value}' not found in subdomain registry structure for sub_domain check.", "line": sd_line})

    if "info-type" in frontmatter_data:
        it_value = frontmatter_data.get("info-type")
        it_line = get_line_number_of_key(frontmatter_str, "info-type", fm_content_start_line)
        if not (is_template_file and is_placeholder_value(it_value)):
            if it_value not in config.info_types: # Uses new self.info_types
                errors.append({"message": f"'info-type' ('{it_value}') not in defined list. Valid: {config.info_types}", "line": it_line })

    if "criticality" in frontmatter_data:
        crit_value = frontmatter_data.get("criticality")
        crit_line = get_line_number_of_key(frontmatter_str, "criticality", fm_content_start_line)
        if not (is_template_file and is_placeholder_value(crit_value)):
            if crit_value not in config.criticality_levels_yaml: # Uses new self.criticality_levels_yaml
                errors.append({"message": f"'criticality' ('{crit_value}') not in defined list. Valid (mixed-case from YAML): {config.criticality_levels_yaml}", "line": crit_line })

    if "lifecycle_gatekeeper" in frontmatter_data:
        lg_value = frontmatter_data.get("lifecycle_gatekeeper")
        lg_line = get_line_number_of_key(frontmatter_str, "lifecycle_gatekeeper", fm_content_start_line)
        if not (is_template_file and is_placeholder_value(lg_value)):
            if lg_value not in config.lifecycle_gatekeepers: # Uses new self.lifecycle_gatekeepers
                warnings.append({"message": f"'lifecycle_gatekeeper' ('{lg_value}') not in defined list. Valid: {config.lifecycle_gatekeepers}", "line": lg_line })

    if "tags" in frontmatter_data:
        tags_value = frontmatter_data.get("tags")
        tags_line = get_line_number_of_key(frontmatter_str, "tags", fm_content_start_line)
        if isinstance(tags_value, list):
            for tag_idx, tag in enumerate(tags_value):
                if isinstance(tag, str):
                    if is_template_file and is_placeholder_value(tag):
                        continue
                    if not re.match(KEBAB_CASE_TAG_REGEX, tag):
                        warnings.append({"message": f"Tag '{tag}' (at index {tag_idx}) invalid kebab-case/structure.", "line": tags_line })

                    valid_prefix = False
                    # Use new self.tag_categories_prefixes for validation
                    for cat_prefix in config.tag_categories_prefixes:
                        if tag.startswith(cat_prefix):
                            valid_prefix = True
                            if cat_prefix == "criticality/":
                                tag_value_part = tag[len(cat_prefix):]
                                if not (is_template_file and is_placeholder_value(tag_value_part)):
                                    # Use new self.criticality_tag_values for validation
                                    if tag_value_part.lower() not in config.criticality_tag_values:
                                        errors.append({"message": f"Tag value for 'criticality/' ('{tag_value_part}') not in defined list. Valid (lowercase values): {config.criticality_tag_values}", "line": tags_line})
                            break
                    if not valid_prefix and not (is_template_file and is_placeholder_value(tag)):
                        # Check if it's a non-prefixed tag defined in structural or utility_process etc.
                        is_known_non_prefixed_tag = False
                        if config.tag_glossary_data and 'tag_categories' in config.tag_glossary_data:
                            for cat_key, cat_def in config.tag_glossary_data['tag_categories'].items():
                                if not cat_def.get('prefix'): # Categories with no prefix
                                    for defined_tag_item in cat_def.get('tags', []):
                                        if isinstance(defined_tag_item, dict) and defined_tag_item.get('full_tag') == tag:
                                            is_known_non_prefixed_tag = True
                                            break
                                if is_known_non_prefixed_tag:
                                    break
                        if not is_known_non_prefixed_tag:
                             warnings.append({"message": f"Tag '{tag}' (at index {tag_idx}) has unrecognized category prefix or is not a known non-prefixed tag. Valid prefixes: {config.tag_categories_prefixes}", "line": tags_line })
    
    # change_log_url validation removed - using unified changelog policy
    content_lines = markdown_content.splitlines(True)
    for i, line_text in enumerate(content_lines):
        for match in re.finditer(INTERNAL_LINK_REGEX, line_text):
            target_id_from_link, anchor, display_text_from_link = match.groups()
            link_line_num = fm_content_end_line + i + 1 
            if "/" in target_id_from_link or target_id_from_link.endswith(".md"):
                errors.append({"message": f"Path-based link '[[{match.group(0)}]]'. Must use '[[STANDARD_ID]]' or '[[STANDARD_ID#Anchor|Display Text]]'.", "line": link_line_num })
            elif re.match(STANDARD_ID_REGEX, target_id_from_link):
                 if not (is_template_file and is_placeholder_value(target_id_from_link)):
                    if target_id_from_link not in config.standards_index:
                        warnings.append({"message": f"Potentially broken link: Standard ID '[[{target_id_from_link}]]' not found in standards_index.json.", "line": link_line_num })
                
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

    # Track files that need extension case fixes
    files_to_rename = []

    for root, _, files in os.walk(abs_dir_path):
        # Skip /tools/reports/ directory entirely
        if "tools/reports" in root.replace(os.sep, '/'):
            continue
            
        for file in files:
            if file.endswith(".md") or file.endswith(".MD"):
                filepath_abs = os.path.join(root, file)
                
                # Check for uppercase extension and mark for renaming
                if file.endswith(".MD"):
                    new_filename = file[:-3] + ".md"  # Replace .MD with .md
                    new_filepath_abs = os.path.join(root, new_filename)
                    files_to_rename.append((filepath_abs, new_filepath_abs))
                    print(f"INFO: Found uppercase extension: {file} -> will rename to {new_filename}")
                
                # Process the file (using original name for now)
                # Report with path relative to repo_base for consistency
                rel_filepath_from_repo_root = os.path.relpath(filepath_abs, config.repo_base).replace(os.sep, '/')
                
                result = lint_file(filepath_abs, config)
                result["filepath"] = rel_filepath_from_repo_root 
                
                # Add extension case warning if uppercase extension found
                if file.endswith(".MD"):
                    result["warnings"].append({
                        "message": f"File extension should be lowercase '.md', not '.MD'. File will be renamed automatically.",
                        "line": 1
                    })
                
                if result.get("standard_id"):
                    seen_standard_ids[result["standard_id"]].append(result) # Store full result for caching
                all_results.append(result)
    
    # Perform file renames after processing
    for old_path, new_path in files_to_rename:
        try:
            # If target exists, compare content and remove duplicate if identical
            if os.path.exists(new_path):
                try:
                    # Use separate context managers to ensure proper file handle cleanup
                    with open(old_path, 'r', encoding='utf-8') as f1:
                        old_content = f1.read()
                    
                    with open(new_path, 'r', encoding='utf-8') as f2:
                        new_content = f2.read()
                    
                    if old_content == new_content:
                        os.remove(old_path)
                        print(f"SUCCESS: Removed duplicate .MD file: {os.path.basename(old_path)} (identical to .md version)")
                    else:
                        print(f"WARNING: .MD and .md versions differ - manual resolution needed: {old_path}")
                except Exception as e:
                    print(f"WARNING: Could not compare files {old_path} and {new_path}: {e}")
            else:  # ← FIXED: Now correctly aligned with if statement
                # Simple rename if target doesn't exist
                os.rename(old_path, new_path)
                print(f"SUCCESS: Renamed {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
        except Exception as e:
            print(f"ERROR: Failed to process {old_path} -> {new_path}: {e}")
    
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
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="Set the logging level (default: INFO).")

    args = parser.parse_args()

    # Configure logging (basic setup, can be more sophisticated if needed)
    # For now, messages will go to stderr by default.
    # The LinterConfig class and other functions use print() for debug/warnings,
    # which should be converted to use logging for consistency if further developed.
    # This basicConfig will only apply to new logging calls, not existing prints.
    # For this exercise, we'll assume print statements are acceptable for now,
    # and this log-level primarily controls verbosity of future logging.
    # However, to make it effective for current prints, they'd need to be changed.
    # For now, this arg is more of a placeholder for future logging integration.
    # The `print` statements in LinterConfig will still show.

    repo_base_abs_path = os.path.abspath(args.repo_base)
    config = LinterConfig(repo_base_path=repo_base_abs_path)
    
    lint_target_dir_rel = args.directory
    # Adjust lint_target_dir_rel if config.repo_base already incorporates 'master-knowledge-base'
    # and args.directory also starts with it.
    if str(config.repo_base).endswith("master-knowledge-base") and lint_target_dir_rel.startswith("master-knowledge-base/"):
        lint_target_dir_rel = lint_target_dir_rel[len("master-knowledge-base/"):]

    # The path passed to lint_directory should be relative to config.repo_base
    # config.repo_base is already the correct absolute path to master-knowledge-base
    lint_target_dir_for_function_call = lint_target_dir_rel

    # For os.path.isdir check, we need the full absolute path based on the original repo_base_abs_path
    # This check is to ensure the user-provided path (or default) is valid from where script is called.
    initial_check_abs_path = os.path.join(repo_base_abs_path, args.directory) # Use original args.directory for this check

    # Check if target directory exists before proceeding
    if not os.path.isdir(initial_check_abs_path):
        # Try with resolved config.repo_base and adjusted relative path
        # This covers cases where repo-base might be '.' from within MKB
        check_path_alt = os.path.join(str(config.repo_base), lint_target_dir_rel)
        if not os.path.isdir(check_path_alt):
            print(f"Error: Target directory for linting not found using path: {initial_check_abs_path} or {check_path_alt}")
            sys.exit(1) # Exit if directory doesn't exist
        lint_target_display_abs = check_path_alt # For print message
    else:
        lint_target_display_abs = initial_check_abs_path


    # Remove dummy file creation unless specifically testing the main() without args
    # For CI, dummy files are not needed as it will lint actual files.
    create_dummies_for_testing = not (sys.argv[1:] and args.directory != "master-knowledge-base/standards/src") # Basic check if run with default dir and no other args
    #create_dummies_for_testing = False # Disabled for this debugging

    if create_dummies_for_testing:
        dummy_files_created_paths = [] # Keep this for cleaning up dummy .md files
        print("Running in local test mode with dummy .md files (dummy index creation is disabled).")
        # The following logic for dummy index creation is now disabled.
        # We rely on the LinterConfig to load the real index or fail clearly.
        # dist_path_local = os.path.join(repo_base_abs_path, "master-knowledge-base", "dist")
        # dummy_index_path_local = os.path.join(dist_path_local, "standards_index.json")
        # if not os.path.exists(dummy_index_path_local):
        #    print(f"DEBUG: Dummy block check: index does not exist at {dummy_index_path_local}")
        #    # os.makedirs(dist_path_local, exist_ok=True) # This would be redundant with LinterConfig's one
        #    # with open(dummy_index_path_local, "w") as f:
        #    #     json.dump(...)
        #    # print(f"Created dummy {dummy_index_path_local} for linter testing.")
        # else:
        #    print(f"DEBUG: Dummy block check: index *does* exist at {dummy_index_path_local}")

        # Make target_dummy_dir calculation robust
        if args.directory.startswith("master-knowledge-base/"):
            target_dummy_dir_rel_part = args.directory[len("master-knowledge-base/"):]
        else:
            target_dummy_dir_rel_part = args.directory
        target_dummy_dir = os.path.join(str(config.repo_base), target_dummy_dir_rel_part)

        dummy_files_to_create = { # These are dummy .md files for testing various linting rules
            "XX-LINT-TESTDUMMY1.MD": """---
title: Dummy Test One (Correct ID)
standard_id: XX-LINT-TESTDUMMY1
info-type: standard-definition
version: '1.0'
date-created: "2023-01-01T00:00:00Z"
date-modified: "2023-01-01T00:00:00Z"
primary_domain: AS 
sub_domain: SCHEMA # Make sure this is valid for AS in your test registry
criticality: p1-high # Corrected casing
tags: [status/draft, topic/testing, kb-id/test]
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
            "XX-LINT-TESTDUMMY2.MD": """---
title: Dummy Test Two (Duplicate ID) # Key order error - title is not first
standard_id: XX-LINT-TESTDUMMY1 
info-type: policy-document
version: '0.1.0'
date-created: "2023-02-02T00:00:00Z"
date-modified: "2023-02-02T00:00:00Z"
tags: [status/approved, kb-id/test]
primary-topic: Test 2
kb-id: kb-id/test
scope_application: Test scope 2
criticality: p2-medium # Corrected casing
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
date-created: "2023-03-03T00:00:00Z"
date-modified: "2023-03-03T00:00:00Z"
primary_domain: CS # Make sure this is valid
sub_domain: POLICY # Make sure this is valid for CS
criticality: p3-low # Corrected casing
tags: [status/draft, kb-id/test]
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
            # Dummy changelog creation removed - using unified changelog policy
        print(f"Created dummy files in {target_dummy_dir}")


    print(f"Starting Knowledge Base Linter on {lint_target_display_abs}...")
    
    results_list = lint_directory(lint_target_dir_for_function_call, config)
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
            if results["infos"]: # Should be "if results.get('infos'):" for safety
                report_content += "### Infos:\n"
                print("Infos:")
                for item in results["infos"]: 
                    msg_line = f"  - [L{item.get('line', 'N/A')}] {item['message']}\n"
                    print(msg_line.strip())
                    report_content += msg_line
            if results["warnings"]: # Should be "if results.get('warnings'):"
                report_content += "### Warnings:\n"
                print("Warnings:")
                for item in results["warnings"]: 
                    msg_line = f"  - [L{item.get('line', 'N/A')}] {item['message']}\n"
                    print(msg_line.strip())
                    report_content += msg_line
                total_warnings += len(results["warnings"])
            if results["errors"]: # Should be "if results.get('errors'):"
                report_content += "### Errors:\n"
                print("Errors:")
                for item in results["errors"]:
                    msg_line = f"  - [L{item.get('line', 'N/A')}] {item['message']}\n"
                    print(msg_line.strip())
                    report_content += msg_line
                total_errors += len(results["errors"])
            # This condition will now be false due to create_dummies_for_testing being false
            # if not results["errors"] and not results["warnings"] and not results["infos"] and (create_dummies_for_testing and ("TESTDUMMY" in filepath_to_display.upper() or "BAD_FILENAME" in filepath_to_display.upper())):
            #    print("No issues found.")
            #    report_content += "- No issues found.\n"
    
    summary_section = f"\n---\n## Linting Summary\n"
    summary_section += f"- Total files processed: {len(results_list)}\n"
    summary_section += f"- Total errors found: {total_errors}\n"
    summary_section += f"- Total warnings found: {total_warnings}\n"
    
    print(summary_section)
    report_content += summary_section

    if args.output:
        # Default to reports directory if just filename provided
        if os.path.dirname(args.output) == "":
            output_path_abs = os.path.join(repo_base_abs_path, "master-knowledge-base", "tools", "reports", args.output)
        else:
            output_path_abs = os.path.join(repo_base_abs_path, args.output)
        
        # Ensure reports directory exists
        os.makedirs(os.path.dirname(output_path_abs), exist_ok=True)
        
        with open(output_path_abs, "w", encoding="utf-8") as f_report:
            f_report.write(report_content)
        print(f"\nLinter report written to: {output_path_abs}")

    if create_dummies_for_testing: # This block will now be skipped
        for path_to_remove in dummy_files_created_paths:
            if os.path.exists(path_to_remove):
                os.remove(path_to_remove)
        print(f"Cleaned up dummy files.")
        # Also remove dummy index if it was created by this test run
        # The dummy index creation is now disabled, so no need to remove it here.
        # if not os.path.exists(os.path.join(dist_path_local, "standards_index.json.original")):
        #      if os.path.exists(dummy_index_path_local): os.remove(dummy_index_path_local)

    if args.fail_on_errors and total_errors > 0:
        print("\nExiting with non-zero status due to errors.")
        sys.exit(1)

if __name__ == "__main__":
    main()
