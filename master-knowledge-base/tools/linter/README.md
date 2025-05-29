# Knowledge Base Linter (`kb_linter.py`)

## Purpose

The `kb_linter.py` script is designed to validate Knowledge Base (KB) documents, primarily Markdown files, against a defined set of standards and policies. Its main goal is to ensure consistency, adherence to metadata schemas, correct formatting, and overall quality of the content within the KB ecosystem.

## Planned Features & Specifications

1.  **Entry Point:**
    *   Command-line interface (CLI).
    *   Accepts one or more file paths or directory paths as input for linting.
    *   Will support recursive directory scanning.

2.  **Configuration:**
    *   Rules will be loaded from the master standard documents themselves, such as:
        *   `[[MT-SCHEMA-FRONTMATTER]]` (for frontmatter key names, order, data types, controlled vocabularies)
        *   `[[SF-SYNTAX-YAML-FRONTMATTER]]` (for basic YAML syntax in frontmatter)
        *   `[[SF-FORMATTING-FILE-HYGIENE]]` (for file encoding, line endings)
        *   `[[SF-CONVENTIONS-NAMING]]` (for filename conventions)
        *   `[[SF-LINKS-INTERNAL-SYNTAX]]` (for internal link styles)
        *   Various registry files in `/master-knowledge-base/standards/registry/` (for controlled vocabularies).
    *   A helper module or parsing functions will be needed to extract machine-readable rules from these Markdown-based standards.

3.  **Severity Levels:**
    *   **Error:** Violations that MUST be fixed (e.g., missing mandatory frontmatter key, incorrect `standard_id` format).
    *   **Warning:** Issues that SHOULD be fixed but might not break processing (e.g., path-based internal links instead of `[[STANDARD_ID]]` links, filename not matching `standard_id`).
    *   **Info:** Informational messages (e.g., file skipped because it's not Markdown).

4.  **Key Checks to Implement:**
    *   **Frontmatter:**
        *   Presence of frontmatter block and valid YAML syntax.
        *   Presence of all mandatory keys as per `[[MT-SCHEMA-FRONTMATTER]]`.
        *   Correct order of keys.
        *   `standard_id` format (regex validation) and uniqueness within `/master-knowledge-base/standards/src/`.
        *   `date-created` and `date-modified` format (ISO-8601 `YYYY-MM-DDTHH:MM:SSZ`).
        *   Validation of values against controlled vocabularies for fields like `info-type`, `primary_domain`, `sub_domain`, `criticality`, and tag categories by loading registry files.
        *   `change_log_url`: Check for existence if relative path, basic syntax if absolute URL.
    *   **File:**
        *   Encoding (UTF-8 without BOM).
        *   Line endings (LF).
        *   Filename (sans `.md`) SHOULD match `standard_id` if `standard_id` is present.
    *   **Links:**
        *   Issue warnings for path-based internal links (e.g., `[[../file.md]]` or `[text](./file.md)`) and prefer `[[STANDARD_ID]]` or `[[STANDARD_ID#Heading]]` for links between standard documents.

5.  **Reporting:**
    *   Initial version: Output findings to the console, clearly indicating the file path, line number (where applicable), severity level, and a descriptive message for each issue found.
    *   Future enhancement (Roadmap Task 0.5.4): Option to generate a Markdown summary report of all issues found across multiple files.

## Usage (Conceptual)

```bash
python kb_linter.py /path/to/master-knowledge-base/standards/src/some-standard.md
python kb_linter.py /path/to/master-knowledge-base/standards/src/
```

## Development Status

This script is currently a skeleton with defined specifications. Implementation of parsing and individual checks is pending.
