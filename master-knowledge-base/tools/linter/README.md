# Knowledge Base Linter (`kb_linter.py`)

## Purpose

The `kb_linter.py` script validates Knowledge Base (KB) Markdown documents against defined standards. It aims to ensure consistency, adherence to metadata schemas (frontmatter), correct formatting, valid internal links, and overall content quality.

## Current Features & Implemented Checks

The linter currently performs the following checks:

1.  **Frontmatter Validation:**
    *   Presence of YAML frontmatter block.
    *   Valid YAML syntax.
    *   **Mandatory Keys:** Checks for presence of all mandatory keys based on `info-type` (distinguishing between `standard-definition`/`policy-document` and other types). Refer to `[[MT-SCHEMA-FRONTMATTER]]`.
    *   **Key Order:** Validates the order of keys against `[[MT-SCHEMA-FRONTMATTER]]`.
    *   **Data Types:** Verifies that values for known keys match their expected data types (e.g., string, list). For lists, checks if items are strings.
    *   **`standard_id`:**
        *   Validates format against regex: `^[A-Z]{2}-[A-Z]{2,6}-[A-Z0-9\-]+$`.
        *   Checks for uniqueness across all processed files in a directory run.
        *   Warns if the document's filename (sans `.md`) does not match the `standard_id`.
    *   **Date Formats:** Validates `date-created` and `date-modified` against ISO-8601 format (`YYYY-MM-DDTHH:MM:SSZ`).
    *   **Controlled Vocabularies:** (Loads from `/master-knowledge-base/standards/registry/`)
        *   `primary_domain`: Validates against `domain_codes.yaml`.
        *   `sub_domain`: Validates against `subdomain_registry.yaml` (scoped to `primary_domain`).
        *   `info-type`: Validates against `info_types.txt`.
        *   `criticality`: Validates against `criticality_levels.txt`.
        *   `lifecycle_gatekeeper`: Validates against `lifecycle_gatekeepers.txt`.
        *   `tags`: Validates individual tag syntax (kebab-case) and checks if tag prefixes match categories defined in `tag_categories.txt`.
    *   **`change_log_url`:**
        *   If relative (starts with `./`), checks for the existence of the linked file.
        *   If absolute, warns if it doesn't start with `http://` or `https://`.
        *   Warns if an absolute URL contains spaces.

2.  **File Hygiene:**
    *   **Encoding:** Warns if a UTF-8 BOM is present (expects UTF-8 without BOM).
    *   **Line Endings:** Warns if CRLF or CR line endings are used (expects LF).

3.  **Internal Links (Body Content):**
    *   **Path-Based Links:** Reports an **error** for path-based `[[link/path.md]]` style links. Links MUST use `[[STANDARD_ID]]`.
    *   **Broken Links:** Warns if a `[[STANDARD_ID]]` does not exist in the `standards_index.json` (requires the index to be available and loaded).

## Configuration & Dependencies

*   **Linter Configuration (`LinterConfig` class):**
    *   Automatically loads controlled vocabularies from files within `/master-knowledge-base/standards/registry/` relative to the specified repository base path.
    *   Loads the `standards_index.json` (expected at `/master-knowledge-base/dist/standards_index.json` relative to repo base) for link checking and `standard_id` uniqueness.
*   **Standards Documents as Source of Truth:**
    *   Key order, mandatory keys, and `standard_id` regex are defined in alignment with `[[MT-SCHEMA-FRONTMATTER]]`.
    *   Controlled vocabularies are sourced from `.yaml` and `.txt` files in `/master-knowledge-base/standards/registry/`.

## Severity Levels

*   **Error:** Violations that MUST be fixed (e.g., missing mandatory key, invalid `standard_id` format, path-based internal links).
*   **Warning:** Issues that SHOULD be fixed (e.g., filename/`standard_id` mismatch, potentially broken `[[STANDARD_ID]]` link).
*   **Info:** Informational messages (not currently heavily used).

## Usage

The script is run from the command line.

**Basic Usage:**

To lint a single file:
```bash
python master-knowledge-base/tools/linter/kb_linter.py --repo-base . master-knowledge-base/standards/src/some-standard.md
```

To lint all `.md` files in a directory (recursively):
```bash
python master-knowledge-base/tools/linter/kb_linter.py --repo-base . --directory master-knowledge-base/standards/src/
```

**Command-Line Arguments:**

*   `filepaths_or_dirs` (Positional): One or more file paths or directory paths to lint. If a directory is provided, it will be scanned recursively for `.md` files.
*   `--directory DIRECTORY`: (Optional, if not providing positional arguments for directories) Directory to lint (relative to repository root). Defaults to `master-knowledge-base/standards/src`. *Note: The script's argument parsing currently expects file/dir paths as positional arguments after options, or uses the default directory if no positional args are given. The `main` function behavior may need adjustment if mixing `--directory` with positional file paths.*
*   `--output OUTPUT_FILE`: (Optional) File path to write the linter report to in Markdown format.
*   `--fail-on-errors`: (Optional) If set, the script will exit with a non-zero status code if any errors are found.
*   `--repo-base REPO_BASE_PATH`: (Optional) Path to the repository root. Defaults to the current directory (`.`). This is used to correctly locate registry and distribution (for index) directories.

**Example Output (Console):**

The linter prints results to the console, grouped by file, indicating errors and warnings with their respective line numbers and messages.

```
--- Results for master-knowledge-base/standards/src/XX-LINT-TESTDUMMY2.md ---
Warnings:
  - [L2] Key order issue: Key 'standard_id' (defined order index 1) is before key 'title' (defined order index 0), violating defined relative order.
Errors:
  - [L2] Duplicate 'standard_id' 'XX-LINT-TESTDUMMY1' also found in: master-knowledge-base/standards/src/XX-LINT-TESTDUMMY1.md
```

## Development Status & Next Steps

*   Core validation logic for many checks is implemented.
*   Vocabulary loading from registry files is functional.
*   Path-based internal links are now treated as errors.

**Key areas for ongoing "Productionizing" (Phase B):**
*   **Unit Tests:** Writing comprehensive unit tests for all key linting functions and validation rules.
*   **Robustness:** Continued refinement of error handling for edge cases and file/system interactions.
*   **Dynamic Vocabulary Loading:** Ensure all required vocabularies are loaded dynamically and parsing is robust for all registry file formats.
*   **Reporting:** Enhance clarity and precision of error messages and line number reporting where possible.

(This README reflects the state after initial Phase B updates to the linter script.)
