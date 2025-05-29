# kb_linter.py
# Knowledge Base Linter with enhanced validation

import os
import re
import yaml 
from datetime import datetime
import json

# --- Configuration (Embedded & Loaded) ---

# (MT-SCHEMA-FRONTMATTER) Mandatory Keys - simplified
MANDATORY_KEYS_CORE = [
    "title", "info-type", "version", 
    "date-created", "date-modified" 
]
MANDATORY_KEYS_STANDARD_DEF = MANDATORY_KEYS_CORE + [
    "standard_id", "primary_domain", "sub_domain", "change_log_url",
    "primary-topic", "kb-id", "tags", "scope_application", 
    "criticality", "lifecycle_gatekeeper", "impact_areas"
]


# (MT-SCHEMA-FRONTMATTER) Correct Key Order
DEFINED_KEY_ORDER = [
    "title", "standard_id", "aliases", "tags", "kb-id", "info-type",
    "primary-topic", "related-standards", "version", "date-created",
    "date-modified", "primary_domain", "sub_domain", "scope_application",
    "criticality", "lifecycle_gatekeeper", "impact_areas", "change_log_url"
]

STANDARD_ID_REGEX = r"^[A-Z]{2}-[A-Z]{2,6}-[A-Z0-9\-]+$"
INTERNAL_LINK_REGEX = r"\[\[([A-Za-z0-9\-\./_#]+)(\|[^\]]+)?\]\]" # Basic, captures ID/path

# --- Vocabulary Loading Functions ---
# These will be loaded once when the linter initializes in a more complete version.
# For now, they might be loaded per call or cached globally in a simple way.

_vocab_cache = {}

def load_yaml_vocab(filepath, cache_key):
    if cache_key in _vocab_cache:
        return _vocab_cache[cache_key]
    try:
        abs_path = os.path.abspath(filepath)
        if not os.path.exists(abs_path):
            print(f"Warning: Vocab file not found: {abs_path}")
            _vocab_cache[cache_key] = None # Cache missing status
            return None
        with open(abs_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            _vocab_cache[cache_key] = data
            return data
    except Exception as e:
        print(f"Warning: Failed to load/parse YAML vocab {filepath}: {e}")
        _vocab_cache[cache_key] = None
        return None

def load_standards_index(index_path):
    cache_key = "standards_index"
    if cache_key in _vocab_cache:
        return _vocab_cache[cache_key]
    try:
        abs_path = os.path.abspath(index_path)
        if not os.path.exists(abs_path):
            print(f"Warning: Standards index not found: {abs_path}")
            _vocab_cache[cache_key] = {}
            return {}
        with open(abs_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            index = {std["standard_id"]: std for std in data.get("standards", [])}
            _vocab_cache[cache_key] = index
            return index
    except Exception as e:
        print(f"Warning: Failed to load/parse standards index {index_path}: {e}")
        _vocab_cache[cache_key] = {}
        return {}

# Hardcoded vocabularies (as per self-correction for this iteration)
# TODO: Implement dynamic parsing of Markdown-based vocabularies in a future enhancement.
HARDCODED_INFO_TYPES = [
    "standard-definition", "policy-document", "guide-document", "glossary-document", 
    "template-document", "registry-document", "schema-document", "navigation-document",
    "chapter-document", "key-definition-set", "kb-definition-map", "how-to-guide",
    "tutorial-document", "troubleshooting-guide", "reference-document", 
    "architecture-overview", "design-specification", "meeting-notes", "report-document",
    "process-definition", "role-definition", "service-definition", "api-specification",
    "data-model-definition", "security-standard", "compliance-guideline"
]
HARDCODED_CRITICALITY_VALUES = ["P0-Critical", "P1-High", "P2-Medium", "P3-Low", "P4-Informational"]
HARDCODED_TAG_CATEGORIES = ["status/", "kb-id/", "content-type/", "topic/", "criticality/", "lifecycle_gatekeeper/"]


# --- Helper Functions ---
def get_frontmatter_and_content(file_content):
    lines = file_content.splitlines(True) 
    if not lines or not lines[0].startswith("---"):
        return None, file_content, 0, 0
    fm_end_index = -1
    for i, line in enumerate(lines[1:], start=1):
        if line.startswith("---"):
            fm_end_index = i
            break
    if fm_end_index == -1:
        return None, file_content, 0, 0
    frontmatter_str = "".join(lines[1:fm_end_index])
    content_str = "".join(lines[fm_end_index+1:])
    return frontmatter_str, content_str, 1, fm_end_index + 1

# --- Linter Core Function ---
def lint_file(filepath, domain_codes, subdomain_registry, standards_index):
    errors = []
    warnings = []
    infos = []
    
    try:
        with open(filepath, 'r', encoding='utf-8', newline='') as f:
            file_content = f.read()
    except FileNotFoundError:
        errors.append({"message": "File not found.", "line": None})
        return {"filepath": filepath, "errors": errors, "warnings": warnings, "infos": infos}
    except UnicodeDecodeError:
        # This check is basic. A dedicated library might be better for BOM detection.
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as f_sig: # Try reading with BOM
                file_content = f_sig.read()
            warnings.append({"message": "File is UTF-8 with BOM. Should be UTF-8 without BOM.", "line": 1})
        except Exception: # If fails again, it's likely not a simple BOM issue or not UTF-8
            errors.append({"message": "File is not UTF-8 encoded or contains undecodable characters.", "line": None})
            return {"filepath": filepath, "errors": errors, "warnings": warnings, "infos": infos}
    except Exception as e:
        errors.append({"message": f"Error reading file: {e}", "line": None})
        return {"filepath": filepath, "errors": errors, "warnings": warnings, "infos": infos}

    # (SF-FORMATTING-FILE-HYGIENE) Line Endings Check
    if "\r\n" in file_content:
        warnings.append({"message": "File contains CRLF line endings. Should use LF.", "line": None})
    elif "\r" in file_content: # Check for isolated CR after CRLF check
        warnings.append({"message": "File contains CR line endings. Should use LF.", "line": None})

    frontmatter_str, markdown_content, fm_start_line, fm_end_line = get_frontmatter_and_content(file_content)

    if frontmatter_str is None:
        errors.append({"message": "No YAML frontmatter block found.", "line": 1})
        return {"filepath": filepath, "errors": errors, "warnings": warnings, "infos": infos}

    frontmatter_data = None
    try:
        frontmatter_data = yaml.safe_load(frontmatter_str)
        if not isinstance(frontmatter_data, dict):
             errors.append({"message": "Frontmatter is not a valid YAML mapping (dictionary).", "line": fm_start_line})
             frontmatter_data = {} 
    except yaml.YAMLError as e:
        error_line_in_fm = e.problem_mark.line + 1 if hasattr(e, 'problem_mark') and e.problem_mark else 0
        actual_line = fm_start_line + error_line_in_fm
        errors.append({"message": f"Invalid YAML syntax in frontmatter: {e.problem}", "line": actual_line})
        return {"filepath": filepath, "errors": errors, "warnings": warnings, "infos": infos}

    # Determine mandatory keys based on info-type
    current_info_type = frontmatter_data.get("info-type")
    mandatory_keys_to_check = MANDATORY_KEYS_STANDARD_DEF if current_info_type == "standard-definition" else MANDATORY_KEYS_CORE
    
    for key in mandatory_keys_to_check:
        if key not in frontmatter_data:
            errors.append({"message": f"Mandatory key '{key}' is missing.", "line": fm_start_line})

    actual_keys = list(frontmatter_data.keys())
    last_known_def_order_idx = -1
    for key_idx, key in enumerate(actual_keys):
        if key in DEFINED_KEY_ORDER:
            current_def_order_idx = DEFINED_KEY_ORDER.index(key)
            if current_def_order_idx < last_known_def_order_idx:
                warnings.append({
                    "message": f"Key '{key}' is out of defined order. It appears after '{actual_keys[key_idx-1]}' which has a later position in the defined order.",
                    "line": fm_start_line 
                })
            last_known_def_order_idx = current_def_order_idx
        # else:
            # warnings.append({"message": f"Key '{key}' is present but not in the DEFINED_KEY_ORDER list.", "line": fm_start_line})


    if "standard_id" in frontmatter_data:
        standard_id_value = frontmatter_data["standard_id"]
        if not isinstance(standard_id_value, str) or not re.match(STANDARD_ID_REGEX, standard_id_value):
            errors.append({"message": f"'standard_id' ('{standard_id_value}') fails regex: '{STANDARD_ID_REGEX}'.", "line": fm_start_line})
        
        # (MT-SCHEMA-FRONTMATTER) Filename Matches standard_id
        filename_base = os.path.splitext(os.path.basename(filepath))[0]
        if standard_id_value and filename_base != standard_id_value:
            warnings.append({"message": f"Filename '{filename_base}.md' does not match 'standard_id' value '{standard_id_value}'.", "line": fm_start_line})


    for date_key in ["date-created", "date-modified"]:
        if date_key in frontmatter_data:
            date_value = frontmatter_data.get(date_key)
            if not isinstance(date_value, str):
                 errors.append({"message": f"'{date_key}' ('{date_value}') is not a string.", "line": fm_start_line})
            else:
                try:
                    if not (len(date_value) == 20 and date_value.endswith('Z') and date_value[10] == 'T' and date_value[4] == '-' and date_value[7] == '-' and date_value[13] == ':' and date_value[16] == ':'):
                        raise ValueError("Structure mismatch YYYY-MM-DDTHH:MM:SSZ")
                    datetime.strptime(date_value[:-1], "%Y-%m-%dT%H:%M:%S")
                except ValueError:
                    errors.append({"message": f"'{date_key}' ('{date_value}') invalid ISO-8601 (YYYY-MM-DDTHH:MM:SSZ).", "line": fm_start_line})

    # (MT-SCHEMA-FRONTMATTER) Controlled Vocabularies
    if "primary_domain" in frontmatter_data:
        pd_value = frontmatter_data["primary_domain"]
        if domain_codes and pd_value not in domain_codes:
            errors.append({"message": f"'primary_domain' value '{pd_value}' not in defined domain_codes.yaml.", "line": fm_start_line})
        
        if "sub_domain" in frontmatter_data:
            sd_value = frontmatter_data["sub_domain"]
            if subdomain_registry and pd_value in subdomain_registry and sd_value not in subdomain_registry[pd_value]:
                errors.append({"message": f"'sub_domain' value '{sd_value}' not valid for primary_domain '{pd_value}'.", "line": fm_start_line})
            elif subdomain_registry and pd_value not in subdomain_registry:
                 warnings.append({"message": f"'primary_domain' value '{pd_value}' not found in subdomain_registry for sub_domain check.", "line": fm_start_line})


    if "info-type" in frontmatter_data and frontmatter_data["info-type"] not in HARDCODED_INFO_TYPES:
        errors.append({"message": f"'info-type' value '{frontmatter_data['info-type']}' not in hardcoded list.", "line": fm_start_line})

    if "criticality" in frontmatter_data and frontmatter_data["criticality"] not in HARDCODED_CRITICALITY_VALUES:
        errors.append({"message": f"'criticality' value '{frontmatter_data['criticality']}' not in hardcoded list.", "line": fm_start_line})

    if "tags" in frontmatter_data and isinstance(frontmatter_data["tags"], list):
        for tag in frontmatter_data["tags"]:
            if not isinstance(tag, str) or not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*(/[a-z0-9]+(-[a-z0-9]+)*)*$", tag):
                warnings.append({"message": f"Tag '{tag}' is not valid kebab-case or has invalid characters/structure.", "line": fm_start_line})
            
            is_known_category = False
            for category in HARDCODED_TAG_CATEGORIES:
                if tag.startswith(category):
                    is_known_category = True
                    break
            if not is_known_category:
                 warnings.append({"message": f"Tag '{tag}' does not start with a recognized category prefix.", "line": fm_start_line})
    
    # (MT-SCHEMA-FRONTMATTER) change_log_url Validity
    if "change_log_url" in frontmatter_data:
        url = frontmatter_data["change_log_url"]
        if isinstance(url, str):
            if url.startswith("./"):
                # Check relative file existence
                doc_dir = os.path.dirname(filepath)
                abs_changelog_path = os.path.abspath(os.path.join(doc_dir, url))
                if not os.path.exists(abs_changelog_path):
                    errors.append({"message": f"Relative 'change_log_url' points to non-existent file: {url} (resolved to {abs_changelog_path})", "line": fm_start_line})
            elif url.startswith("http://") or url.startswith("https://"):
                if "://" not in url or " " in url: # Basic sanity check
                     warnings.append({"message": f"Absolute 'change_log_url' ('{url}') has questionable syntax.", "line": fm_start_line})
            # else: # Could be other forms of relative or absolute paths not starting with ./
            #    warnings.append({"message": f"'change_log_url' ('{url}') is not a recognized relative path or absolute HTTP(S) URL.", "line": fm_start_line})

    # Internal Link Style and Existence
    # Using content_lines for line number reference
    content_lines = markdown_content.splitlines(True)
    for i, line_text in enumerate(content_lines):
        for match in re.finditer(INTERNAL_LINK_REGEX, line_text):
            link_target = match.group(1)
            # Check for path-based links
            if "/" in link_target or link_target.endswith(".md"):
                warnings.append({
                    "message": f"Path-based internal link '[[{link_target}]]' found. Recommend using '[[STANDARD_ID]]' style.",
                    "line": fm_end_line + i + 1 
                })
            # Check for STANDARD_ID existence (if it looks like one)
            elif re.match(STANDARD_ID_REGEX, link_target) and standards_index and link_target not in standards_index:
                warnings.append({
                    "message": f"Potentially broken link: '[[{link_target}]]' does not match any known standard_id in the index.",
                    "line": fm_end_line + i + 1
                })


    return {"filepath": filepath, "errors": errors, "warnings": warnings, "infos": infos}

def main():
    repo_base = "." 
    
    domain_codes_path = os.path.join(repo_base, "master-knowledge-base", "standards", "registry", "domain_codes.yaml")
    subdomain_registry_path = os.path.join(repo_base, "master-knowledge-base", "standards", "registry", "subdomain_registry.yaml")
    standards_index_path = os.path.join(repo_base, "master-knowledge-base", "dist", "standards_index.json") # Assuming index is built

    domain_codes_data = load_yaml_vocab(domain_codes_path, "domain_codes")
    domain_codes_list = [item['code'] for item in domain_codes_data['codes']] if domain_codes_data and 'codes' in domain_codes_data else []
    
    subdomain_registry_data = load_yaml_vocab(subdomain_registry_path, "subdomain_registry")
    
    standards_index_data = load_standards_index(standards_index_path)


    test_files_rel_paths = [
        os.path.join("master-knowledge-base", "standards", "src", "MT-SCHEMA-FRONTMATTER.md"),
        os.path.join("master-knowledge-base", "standards", "src", "AS-SCHEMA-CONCEPT-DEFINITION.md"),
    ]
    
    dummy_file_path_rel = os.path.join("master-knowledge-base", "dummy_lint_test.md")
    with open(os.path.abspath(os.path.join(repo_base, dummy_file_path_rel)), "w", encoding="utf-8", newline="\n") as f:
        f.write("---\r\n") 
        f.write("title: Dummy Test for Linter\r\n") # CRLF
        f.write("standard_id: XX-DOM-INVALIDID\r\n") # Valid ID for filename check
        f.write("info-type: invalid-info-type\r\n")
        f.write("version: 1.0\r\n") 
        f.write("date-created: 2023-01-01T00:00:00Z\r\n") # Correct
        f.write("date-modified: 2023-10-INVALID\r\n") 
        f.write("primary_domain: ZZ\r\n") # Invalid domain
        f.write("sub_domain: TEST\r\n")   # Invalid for ZZ or if ZZ not in registry
        f.write("criticality: P9-Unknown\r\n")
        f.write("tags:\r\n  - status/ok\r\n  - unknown-category/test\r\n  - topic/good\r\n  - badTagFormat\r\n")
        f.write("change_log_url: ./non_existent_changelog.md\r\n")
        f.write("primary-topic: Test\r\n")
        f.write("kb-id: kb-id/test\r\n")
        f.write("scope_application: Test scope\r\n")
        f.write("lifecycle_gatekeeper: TestGate\r\n")
        f.write("impact_areas: ['test']\r\n")
        f.write("---\r\n")
        f.write("Content with a [[../path/based/link.md]] and a broken [[XX-BROKEN-ID-001]].\n")
        f.write("Another line with [[AS-SCHEMA-CONCEPT-DEFINITION]].\n") # Valid link
    test_files_rel_paths.append(dummy_file_path_rel)

    print("Starting Knowledge Base Linter (Enhanced)...")
    for test_file_rel in test_files_rel_paths:
        test_file_abs = os.path.abspath(os.path.join(repo_base, test_file_rel))
        
        if not os.path.exists(test_file_abs):
             print(f"\n--- Test file not found by main(): {test_file_abs} (Skipping) ---")
             continue

        results = lint_file(test_file_abs, domain_codes_list, subdomain_registry_data, standards_index_data)
        print(f"\n--- Results for {results['filepath']} ---")
        if results["infos"]:
            print("Infos:")
            for item in results["infos"]: print(f"  - [L{item.get('line', 'N/A')}] {item['message']}")
        if results["warnings"]:
            print("Warnings:")
            for item in results["warnings"]: print(f"  - [L{item.get('line', 'N/A')}] {item['message']}")
        if results["errors"]:
            print("Errors:")
            for item in results["errors"]: print(f"  - [L{item.get('line', 'N/A')}] {item['message']}")
        if not results["errors"] and not results["warnings"] and not results["infos"]:
            print("No issues found.")
            
    if os.path.exists(os.path.abspath(os.path.join(repo_base, dummy_file_path_rel))):
        os.remove(os.path.abspath(os.path.join(repo_base, dummy_file_path_rel)))
        print(f"\nCleaned up dummy file: {dummy_file_path_rel}")

if __name__ == "__main__":
    main()
