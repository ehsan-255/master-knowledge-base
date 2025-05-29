# kb_linter.py
# Placeholder for Knowledge Base Linter

# Specifications:
# 1. Entry Point: Command-line script. Accepts file paths or directories.
# 2. Configuration: Load rules from MT-SCHEMA-FRONTMATTER.md, SF-SYNTAX-YAML-FRONTMATTER.md, SF-FORMATTING-FILE-HYGIENE.md, etc.
#    - Consider a helper script/module to parse these Markdown standards into machine-readable rules if not already planned.
# 3. Severity Levels: Implement info, warning, error.
# 4. Checks to Implement (as per Roadmap Task 0.5.1 and MT-SCHEMA-FRONTMATTER.md):
#    - Frontmatter presence and basic YAML syntax (SF-SYNTAX-YAML-FRONTMATTER).
#    - File encoding (UTF-8 no BOM) and line endings (LF) (SF-FORMATTING-FILE-HYGIENE).
#    - Presence of all mandatory keys defined in MT-SCHEMA-FRONTMATTER.md.
#    - Correct order of keys in frontmatter (MT-SCHEMA-FRONTMATTER.md).
#    - Validation of `standard_id` regex and uniqueness across files in /standards/src/.
#    - Validation of `date-created` and `date-modified` against ISO-8601 format (YYYY-MM-DDTHH:MM:SSZ).
#    - Validation of values against controlled vocabularies (e.g., for `info-type`, `primary_domain`, `sub_domain`, `criticality`, `tags` categories) by loading registry files from /standards/registry/.
#    - `change_log_url`: check existence if relative, basic syntax if absolute.
#    - Filename (sans .md) SHOULD equal `standard_id` if `standard_id` is present.
#    - Internal link style: Issue warning for path-based links (e.g., `[[../file.md]]`) vs `[[STANDARD_ID]]`. (Roadmap Task 0.3.3 and 3.2.2)
# 5. Reporting: Output findings to console, indicating file, line number (if applicable), severity, and message.
#    - Future: Generate Markdown summary report (Roadmap Task 0.5.4).

def lint_file(filepath):
    errors = []
    warnings = []
    info = []
    # TODO: Implement file reading and parsing (e.g., frontmatter extraction)
    # TODO: Implement checks based on specifications
    print(f"Linting {filepath}...")
    # Example check:
    # if not filepath.endswith(".md"):
    #     info.append({"message": "File is not Markdown, skipping some checks.", "line": None})
    return {"errors": errors, "warnings": warnings, "info": info}

def main():
    # TODO: Implement argument parsing for file/directory paths
    # For now, simulate with a test file
    # Note: Path should be relative to repo root for consistency if run from repo root.
    # For testing within a tool, absolute paths or paths relative to a known base might be used.
    test_file = "master-knowledge-base/standards/src/MT-SCHEMA-FRONTMATTER.md" # Example
    print(f"Attempting to lint: {test_file}")
    # This is a placeholder. Actual file access would need to be from the perspective
    # of where the script is run, or use absolute paths if the script context allows.
    # For now, this will just print.
    # results = lint_file(test_file)
    # print(f"Results for {test_file}: {results}")
    print("Linter main function called (simulation).")

if __name__ == "__main__":
    main()
