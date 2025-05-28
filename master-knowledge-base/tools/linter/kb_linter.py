# kb_linter.py
#
# This script will lint Markdown files in the knowledge base, primarily focusing on
# frontmatter validation against the rules defined in U-METADATA-FRONTMATTER-RULES-001.md
# and other related standards.

import os
import re
import yaml # PyYAML library
import argparse
from datetime importdatetime # For ISO-8601 validation

# --- Configuration & Constants ---

# Regex for standard_id (from U-METADATA-FRONTMATTER-RULES-001.md)
STANDARD_ID_REGEX = r"^[A-Z]{2}-[A-Z]{2,6}-[A-Z0-9\-]+$"

# ISO-8601 Date-Time format (YYYY-MM-DDTHH:MM:SSZ)
ISO_8601_REGEX = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"

# Expected frontmatter keys (referencing U-METADATA-FRONTMATTER-RULES-001.md)
# This list should be dynamically loaded or kept in sync with the standard.
# For now, a placeholder for the core mandatory keys.
MANDATORY_KEYS = [
    "title", "standard_id", "tags", "info-type", "primary-topic",
    "version", "date-created", "date-modified", "primary_domain",
    "sub_domain", "scope_application", "criticality", "lifecycle_gatekeeper",
    "impact_areas" # change_log_url is conditionally mandatory
]

# Paths (these could be made configurable via CLI args or a config file)
REGISTRY_PATH = "master-knowledge-base/standards/registry/"
SRC_PATH = "master-knowledge-base/standards/src/"

# Severity levels
SEVERITY_INFO = "INFO"
SEVERITY_WARNING = "WARNING"
SEVERITY_ERROR = "ERROR"

# --- Helper Functions ---

def log_issue(filepath, line_number, severity, code, message):
    """
    Logs an issue found during linting.
    Args:
        filepath (str): Path to the file with the issue.
        line_number (int or None): Line number of the issue, if applicable.
        severity (str): Severity level (INFO, WARNING, ERROR).
        code (str): A short code for the type of issue (e.g., 'FM001', 'DATE002').
        message (str): Detailed message describing the issue.
    """
    loc = f":{line_number}" if line_number else ""
    print(f"[{severity}] {filepath}{loc} [{code}]: {message}")

def load_yaml_file(filepath):
    """
    Loads a YAML file and returns its content.
    Args:
        filepath (str): Path to the YAML file.
    Returns:
        dict or list: Parsed YAML content, or None if an error occurs.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # Basic check for LF line endings (more robust checks might be needed)
            # content = f.read()
            # if '\r\n' in content:
            #     log_issue(filepath, None, SEVERITY_WARNING, "ENC002", "File appears to use CRLF line endings instead of LF.")
            # f.seek(0) # Reset file pointer
            return yaml.safe_load(f)
    except FileNotFoundError:
        log_issue(filepath, None, SEVERITY_ERROR, "LDR001", f"File not found: {filepath}")
        return None
    except yaml.YAMLError as e:
        log_issue(filepath, None, SEVERITY_ERROR, "LDR002", f"Error parsing YAML file {filepath}: {e}")
        return None
    except Exception as e:
        log_issue(filepath, None, SEVERITY_ERROR, "LDR003", f"Unexpected error loading {filepath}: {e}")
        return None

def load_controlled_vocabularies():
    """
    Loads all controlled vocabularies from the registry.
    Returns:
        dict: A dictionary where keys are vocabulary names (e.g., 'domain_codes')
              and values are their parsed content.
    """
    vocabularies = {}
    registry_files = {
        "domain_codes": "domain_codes.yaml",
        "subdomain_registry": "subdomain_registry.yaml",
        "criticality_levels": "criticality_levels.yaml",
        "lifecycle_gatekeepers": "lifecycle_gatekeepers.yaml",
        # Add other registry files here, e.g., tag_glossary_definition.md (needs Markdown parsing for tags)
        # For info-type, the U-METADATA-FRONTMATTER-RULES-001.md itself is the source.
    }
    for vocab_name, filename in registry_files.items():
        filepath = os.path.join(REGISTRY_PATH, filename)
        vocabularies[vocab_name] = load_yaml_file(filepath)

    # TODO: Load info-type controlled vocabulary from U-METADATA-FRONTMATTER-RULES-001.md (requires Markdown parsing)
    # For now, placeholder:
    vocabularies["info_types_from_standard"] = [
        "standard-definition", "policy-document", "guide-document", "glossary-document",
        "tag-glossary-document", "key-definition-set", "kb-definition-map",
        "registry-document", "template-document", "schema-definition", "report-document"
    ]
    return vocabularies

# --- Frontmatter Validation Functions ---

def validate_frontmatter_completeness(filepath, frontmatter):
    """
    Checks if all mandatory frontmatter keys are present.
    Args:
        filepath (str): Path to the file being validated.
        frontmatter (dict): Parsed frontmatter content.
    """
    for key in MANDATORY_KEYS:
        if key not in frontmatter:
            log_issue(filepath, None, SEVERITY_ERROR, "FM001", f"Mandatory key '{key}' is missing from frontmatter.")
    # Check for conditional 'change_log_url'
    if frontmatter.get("version"): # Assuming versioned docs need changelog
        if "change_log_url" not in frontmatter:
             log_issue(filepath, None, SEVERITY_WARNING, "FM002", f"Conditionally mandatory key 'change_log_url' is missing for versioned document.")


def validate_standard_id(filepath, standard_id_value, all_standard_ids):
    """
    Validates the standard_id format and uniqueness.
    Args:
        filepath (str): Path to the file being validated.
        standard_id_value (str): The value of the standard_id key.
        all_standard_ids (set): A set of all standard_ids found so far for uniqueness check.
    """
    if not isinstance(standard_id_value, str):
        log_issue(filepath, None, SEVERITY_ERROR, "FM003", f"'standard_id' must be a string. Found: {type(standard_id_value)}")
        return
    if not re.match(STANDARD_ID_REGEX, standard_id_value):
        log_issue(filepath, None, SEVERITY_ERROR, "FM004", f"'standard_id' value '{standard_id_value}' does not match regex: {STANDARD_ID_REGEX}")
    # Check for uniqueness (case-sensitive)
    # This basic check assumes all_standard_ids is populated during the walk
    # A more robust approach might involve a pre-scan or a central registry if performance is an issue.
    # if standard_id_value in all_standard_ids:
    #     log_issue(filepath, None, SEVERITY_ERROR, "FM005", f"Duplicate 'standard_id' found: {standard_id_value}")
    # else:
    #     all_standard_ids.add(standard_id_value) # This logic needs to be handled in the main walk

def validate_date_format(filepath, key_name, date_value):
    """
    Validates date strings against ISO-8601 format (YYYY-MM-DDTHH:MM:SSZ).
    Args:
        filepath (str): Path to the file being validated.
        key_name (str): Name of the date key (e.g., 'date-created').
        date_value (str): The date string to validate.
    """
    if not isinstance(date_value, str):
        log_issue(filepath, None, SEVERITY_ERROR, "DATE001", f"Date key '{key_name}' must be a string. Found: {type(date_value)}")
        return
    if not re.match(ISO_8601_REGEX, date_value):
        log_issue(filepath, None, SEVERITY_ERROR, "DATE002", f"Date key '{key_name}' value '{date_value}' does not match ISO-8601 format (YYYY-MM-DDTHH:MM:SSZ).")
    else:
        try:
            # Further check if it's a valid date (e.g., not 2023-13-01T...)
            datetime.strptime(date_value, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            log_issue(filepath, None, SEVERITY_ERROR, "DATE003", f"Date key '{key_name}' value '{date_value}' is not a valid date (e.g., month or day out of range).")


def validate_against_controlled_vocabulary(filepath, key_name, value, vocab_name, vocabularies):
    """
    Validates a frontmatter value against a loaded controlled vocabulary.
    Args:
        filepath (str): Path to the file being validated.
        key_name (str): Name of the key being validated.
        value (str or list): The value(s) to validate.
        vocab_name (str): The key for the specific vocabulary in the `vocabularies` dict.
        vocabularies (dict): The dictionary of all loaded vocabularies.
    """
    # Placeholder for actual validation logic
    # Example for 'info-type':
    # if key_name == "info-type":
    #     allowed_values = vocabularies.get("info_types_from_standard", [])
    #     if value not in allowed_values:
    #         log_issue(filepath, None, SEVERITY_ERROR, "CV001", f"Value '{value}' for key '{key_name}' is not in the controlled vocabulary. Allowed: {allowed_values}")
    #
    # Example for 'primary_domain':
    # if key_name == "primary_domain":
    #     domain_codes_vocab = vocabularies.get("domain_codes")
    #     if domain_codes_vocab:
    #         allowed_domains = [item['code'] for item in domain_codes_vocab] # Assuming list of dicts with 'code'
    #         if value not in allowed_domains:
    #             log_issue(filepath, None, SEVERITY_ERROR, "CV002", f"Value '{value}' for key '{key_name}' is not a valid domain code. Allowed: {allowed_domains}")
    #
    # Example for 'criticality' tag (from 'tags' list):
    # if key_name == "tags" and isinstance(value, list):
    #     criticality_tags = [tag for tag in value if tag.startswith("criticality/")]
    #     criticality_levels_vocab = vocabularies.get("criticality_levels")
    #     if criticality_levels_vocab:
    #         allowed_criticality_tags = [item['tag'] for item in criticality_levels_vocab]
    #         for ctag in criticality_tags:
    #             if ctag not in allowed_criticality_tags:
    #                 log_issue(filepath, None, SEVERITY_ERROR, "CV003", f"Tag '{ctag}' is not a valid criticality tag. Allowed: {allowed_criticality_tags}")
    pass # Implement actual logic based on vocabulary structure

def validate_change_log_url(filepath, url_value):
    """
    Validates the change_log_url.
    Args:
        filepath (str): Path to the file being validated.
        url_value (str): The URL string from frontmatter.
    """
    if not isinstance(url_value, str):
        log_issue(filepath, None, SEVERITY_ERROR, "URL001", f"'change_log_url' must be a string. Found: {type(url_value)}")
        return

    if url_value.startswith("./") or url_value.startswith("../"):
        # Relative path: check existence
        # Construct absolute path relative to the file being linted
        abs_path = os.path.normpath(os.path.join(os.path.dirname(filepath), url_value))
        if not os.path.exists(abs_path):
            log_issue(filepath, None, SEVERITY_WARNING, "URL002", f"'change_log_url' relative path '{url_value}' (resolved to '{abs_path}') does not exist.")
    elif url_value.startswith("http://") or url_value.startswith("https://"):
        # Absolute URL: basic syntax check (very basic)
        if " " in url_value or not ("://" in url_value): # Extremely naive check
            log_issue(filepath, None, SEVERITY_WARNING, "URL003", f"'change_log_url' absolute URL '{url_value}' has invalid syntax.")
    else:
        log_issue(filepath, None, SEVERITY_WARNING, "URL004", f"'change_log_url' value '{url_value}' is neither a recognized relative path nor an absolute URL.")

# --- File Processing ---

def parse_markdown_file(filepath):
    """
    Parses a Markdown file to extract frontmatter and content.
    Args:
        filepath (str): Path to the Markdown file.
    Returns:
        tuple: (frontmatter_dict, content_string, frontmatter_raw_lines) or (None, None, None) if error.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content_lines = f.readlines()

        # Basic check for UTF-8 BOM (though 'utf-8-sig' encoding is better for reading)
        # if content_lines and content_lines[0].startswith('\ufeff'):
        #    log_issue(filepath, 1, SEVERITY_WARNING, "ENC001", "File starts with UTF-8 BOM.")

        if not content_lines or not content_lines[0].strip() == "---":
            log_issue(filepath, 1, SEVERITY_INFO, "FM000", "File does not start with YAML frontmatter delimiter '---'.")
            return None, "".join(content_lines), []

        fm_end_index = -1
        for i, line in enumerate(content_lines[1:], start=1):
            if line.strip() == "---":
                fm_end_index = i
                break

        if fm_end_index == -1:
            log_issue(filepath, None, SEVERITY_ERROR, "FM00X", "YAML frontmatter closing delimiter '---' not found.")
            return None, "".join(content_lines), []

        frontmatter_raw_lines = content_lines[1:fm_end_index]
        frontmatter_str = "".join(frontmatter_raw_lines)
        content_str = "".join(content_lines[fm_end_index + 1:])

        try:
            frontmatter = yaml.safe_load(frontmatter_str)
            if not isinstance(frontmatter, dict):
                log_issue(filepath, None, SEVERITY_ERROR, "FM00Y", "Frontmatter did not parse as a dictionary.")
                return None, content_str, frontmatter_raw_lines
            return frontmatter, content_str, frontmatter_raw_lines
        except yaml.YAMLError as e:
            # Try to find line number of error if possible (tricky with safe_load on string)
            err_line = e.problem_mark.line + 1 if hasattr(e, 'problem_mark') and e.problem_mark else None
            log_issue(filepath, err_line, SEVERITY_ERROR, "FM00Z", f"Error parsing YAML frontmatter: {e}")
            return None, content_str, frontmatter_raw_lines

    except FileNotFoundError:
        log_issue(filepath, None, SEVERITY_ERROR, "LDR001", f"File not found: {filepath}")
        return None, None, None
    except Exception as e:
        log_issue(filepath, None, SEVERITY_ERROR, "PROC001", f"Error processing file {filepath}: {e}")
        return None, None, None

def lint_markdown_file(filepath, vocabularies, all_standard_ids):
    """
    Lints a single Markdown file.
    Args:
        filepath (str): Path to the Markdown file.
        vocabularies (dict): Loaded controlled vocabularies.
        all_standard_ids (set): Set to track standard_ids for uniqueness.
    """
    print(f"Linting: {filepath}")
    frontmatter, content, _ = parse_markdown_file(filepath)

    if frontmatter is None:
        # Error already logged by parse_markdown_file
        return

    # --- Perform Validations ---
    validate_frontmatter_completeness(filepath, frontmatter)

    # standard_id validation
    standard_id_val = frontmatter.get("standard_id")
    if standard_id_val:
        validate_standard_id(filepath, standard_id_val, all_standard_ids)
        # This part of uniqueness check needs to be outside if we want to collect all first
        # For now, assume it's handled by the caller accumulating all_standard_ids
    else:
        if "standard_id" in MANDATORY_KEYS: # Check if it was expected
             log_issue(filepath, None, SEVERITY_ERROR, "FM003B", "'standard_id' key is present but has no value or is null.")


    # Date validation
    if "date-created" in frontmatter:
        validate_date_format(filepath, "date-created", frontmatter["date-created"])
    if "date-modified" in frontmatter:
        validate_date_format(filepath, "date-modified", frontmatter["date-modified"])

    # Controlled vocabulary checks (examples)
    if "info-type" in frontmatter:
        validate_against_controlled_vocabulary(filepath, "info-type", frontmatter["info-type"], "info_types_from_standard", vocabularies)
    if "primary_domain" in frontmatter:
        validate_against_controlled_vocabulary(filepath, "primary_domain", frontmatter["primary_domain"], "domain_codes", vocabularies)
    # ... add more calls for other keys like sub_domain, criticality (key vs tag), lifecycle_gatekeeper

    # Check 'criticality' key against 'criticality_levels' vocab
    if "criticality" in frontmatter:
        validate_against_controlled_vocabulary(filepath, "criticality", frontmatter["criticality"], "criticality_levels", vocabularies) # Needs adjustment in vocab loader and validator

    # Check 'criticality/' tags in 'tags' field
    if "tags" in frontmatter and isinstance(frontmatter.get("tags"), list):
        # This logic should be refined in validate_against_controlled_vocabulary
        pass


    # change_log_url validation
    if "change_log_url" in frontmatter:
        validate_change_log_url(filepath, frontmatter["change_log_url"])

    # YAML encoding (UTF-8 no BOM) and line endings (LF)
    # These are harder to check reliably for existing files without reading them in binary mode
    # or relying on external tools. Basic checks can be done in load_yaml_file or parse_markdown_file.
    # For now, we assume 'utf-8' in open() handles encoding. BOM/LF checks are complex.
    # log_issue(filepath, None, SEVERITY_INFO, "ENC000", "UTF-8 (no BOM) and LF line ending checks are placeholders.")

    # Path-based internal link check (basic example)
    if content:
        # Regex for [[./...]] or [[../...]] style links
        path_wikilinks = re.findall(r"\[\[([./].*?)\]\]", content)
        for link in path_wikilinks:
            log_issue(filepath, None, SEVERITY_WARNING, "LINK001", f"Path-based internal wikilink found: [[{link}]]")

        # Regex for [text](./...) or [text](../...) style links that might point to other standards
        # This is more complex as it needs to differentiate from external links or links to assets.
        # md_links = re.findall(r"\[.*?\]\(([./].*?\.md)\)", content)
        # for link_target in md_links:
        #    if "/standards/src/" in link_target or "/master-knowledge-base/standards/src/" in link_target: # Heuristic
        #        log_issue(filepath, None, SEVERITY_WARNING, "LINK002", f"Potential path-based Markdown link to standard: {link_target}")
        pass


# --- Main Execution ---

def main():
    """
    Main function to drive the linter.
    """
    parser = argparse.ArgumentParser(description="Linter for Knowledge Base Markdown files.")
    parser.add_argument(
        "--dir",
        default=SRC_PATH,
        help=f"Directory to scan for Markdown files (default: {SRC_PATH})"
    )
    parser.add_argument(
        "--registry",
        default=REGISTRY_PATH,
        help=f"Directory containing controlled vocabulary registries (default: {REGISTRY_PATH})"
    )
    # Add more arguments (config file, specific checks to run/skip, output format, etc.)
    args = parser.parse_args()

    print("Starting Knowledge Base Linter...")
    print(f"Source directory: {args.dir}")
    print(f"Registry directory: {args.registry}")

    vocabularies = load_controlled_vocabularies()
    # print(f"Loaded vocabularies: {list(vocabularies.keys())}") # For debugging

    all_found_standard_ids = set() # Used for uniqueness checks

    # Walk through Markdown files
    for root, _, files in os.walk(args.dir):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                lint_markdown_file(filepath, vocabularies, all_found_standard_ids)
                # Collect standard_id for global uniqueness check after all files parsed
                # temp_fm, _, _ = parse_markdown_file(filepath) # Avoid double parsing if possible
                # if temp_fm and temp_fm.get("standard_id"):
                #    all_found_standard_ids.add(temp_fm["standard_id"])


    # Post-walk checks (e.g., standard_id uniqueness across all files)
    # This requires a more sophisticated approach, perhaps storing all frontmatters first
    # or using the all_found_standard_ids set built during the walk if lint_markdown_file populates it.
    print("Linting process complete.")
    # Summarize errors/warnings if desired

if __name__ == "__main__":
    main()
```
