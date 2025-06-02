---
title: Knowledge Base Linter (`kb_linter.py`)
standard_id: OM-DOC-TOOLS-LINTER-README # Changed standard_id
aliases:
  - Linter README
tags:
  - status/active
  - content-type/documentation
  - topic/readme
  - kb-id/tools
kb-id: "kb-id/tools" # Standardized kb-id format
info-type: "guide-document" # Ensured info-type
primary-topic: Overview and guidance for the linter directory and its contents.
related-standards: []
version: 1.0.0
date-created: '2025-06-01T11:33:47Z'
date-modified: '2025-06-02T00:00:00Z'
primary_domain: "OM" # Changed primary_domain
sub_domain: "DOCUMENTATION" # Changed sub_domain
scope_application: Provides an overview for the /app/master-knowledge-base/tools/linter directory and its script.
criticality: "P3-Low" # Changed criticality
lifecycle_gatekeeper: No-Gatekeeper
impact_areas:
  - documentation
  - usability
change_log_url: ./changelog.md # Changed change_log_url
---

# Knowledge Base Linter (`kb_linter.py`)

## Purpose

The `kb_linter.py` script validates Knowledge Base (KB) Markdown documents against defined standards. It aims to ensure consistency, adherence to metadata schemas (frontmatter), correct formatting, valid internal links, and overall content quality.

## Current Features & Implemented Checks

The linter currently performs the following checks:

1.  **Frontmatter Validation:**
    *   Presence of YAML frontmatter block.
    *   Valid YAML syntax.
    *   **Mandatory Keys:** Checks for presence of all mandatory keys based on `info-type` (distinguishing between `standard-definition`/`policy-document` and other types).
    *   **Key Order:** Validates the order of keys against a defined sequence (`DEFINED_KEY_ORDER`). Reports all deviations in a file.
    *   **Data Types:** Verifies that values for known keys match their expected data types (e.g., string, list). For lists, checks if items are strings.
    *   **`standard_id`:**
        *   Validates format against regex: `^[A-Z]{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*$`.
        *   Checks for uniqueness across all processed files in a directory run.
        *   Warns if the document's filename (sans `.md`) does not match the `standard_id`.
    *   **Date Formats:** Validates `date-created` and `date-modified` against ISO-8601 format (`YYYY-MM-DDTHH:MM:SSZ`) and ensures they are valid dates/times.
    *   **Controlled Vocabularies:** (Loads from `/master-knowledge-base/standards/registry/`)
        *   `primary_domain`: Validates against `domain_codes.yaml`.
        *   `sub_domain`: Validates against `subdomain_registry.yaml` (scoped to `primary_domain`).
        *   `info-type`: Validates against `info_types.txt`.
        *   `criticality` (field): Validates against mixed-case values in `criticality_levels.yaml` (e.g., `P1-High`).
        *   `lifecycle_gatekeeper`: Validates against `lifecycle_gatekeepers.txt`.
        *   `tags`:
            *   Validates individual tag syntax (kebab-case).
            *   Checks if tag prefixes match categories defined in `tag_categories.txt`.
            *   For `criticality/*` tags, validates the value part against lowercase entries in `criticality_levels.txt` (e.g., `criticality/p1-high`).
    *   **`change_log_url`:**
        *   If `info-type: changelog`, ensures the URL is self-referential (e.g., `./MY-CHANGELOG.md`).
        *   If relative (starts with `./`), checks for the existence of the linked file (for non-changelog documents).
        *   If absolute, warns if it doesn't start with `http://` or `https://`.
        *   Warns if an absolute URL contains spaces.

2.  **File Hygiene:**
    *   **Encoding:** Warns if a UTF-8 BOM is present (expects UTF-8 without BOM).
    *   **Line Endings:** Warns if CRLF or CR line endings are used (expects LF).

3.  **Internal Links (Body Content):**
  *   **Path-Based Links:** Reports an **error** for path-based links (e.g., `[[./some/path.md]]`). Links MUST use the `[[STANDARD_ID]]` format.
    *   **Broken Links:** Warns if a `[[STANDARD_ID]]` does not exist in the `standards_index.json` (requires the index to be available and loaded).

## Configuration & Dependencies

*   **Linter Configuration (`LinterConfig` class):**
    *   Automatically loads controlled vocabularies from files within `/master-knowledge-base/standards/registry/` relative to the specified repository base path. For Phase B, vocabulary loading from Markdown content (e.g., `[[MT-REGISTRY-TAG-GLOSSARY]]`) has been deferred in favor of registry files.
    *   Loads the `standards_index.json` (expected at `[REPO_BASE]/master-knowledge-base/dist/standards_index.json`). A small delay (`time.sleep(0.1)`) was added before index loading to mitigate potential filesystem synchronization issues in some environments, ensuring the index is reliably found after generation.
*   **Python Dependencies:** `PyYAML`.

## Severity Levels

*   **Error:** Violations that MUST be fixed.
*   **Warning:** Issues that SHOULD be fixed.
*   **Info:** Informational messages (currently minimal).

## Unit Tests

A suite of unit tests using the `unittest` framework is implemented in `master-knowledge-base/tools/linter/tests/test_kb_linter.py`. These tests cover various aspects of the linter's functionality, including index loading, vocabulary validation, date checks, link parsing, and key order. Currently, there are 23 tests.

## Usage

The script is run from the command line.

**Basic Usage:**

To lint all `.md` files in a specific directory (recursively):
```bash
python master-knowledge-base/tools/linter/kb_linter.py --repo-base . --directory master-knowledge-base/standards/src/
```

To lint files in the registry:
```bash
python master-knowledge-base/tools/linter/kb_linter.py --repo-base . --directory master-knowledge-base/standards/registry/
```

**Command-Line Arguments:**

*   `--directory DIRECTORY`: Directory to lint (relative to repository root). Defaults to `master-knowledge-base/standards/src`.
*   `--output OUTPUT_FILE`: (Optional) File path to write the linter report to in Markdown format. If not specified, output is to console only (aside from normal logging).
*   `--fail-on-errors`: (Optional) If set, the script will exit with a non-zero status code if any errors are found.
*   `--repo-base REPO_BASE_PATH`: (Optional) Path to the repository root. Defaults to the current directory (`.`). This is crucial for correctly locating the `standards_index.json` and vocabulary registry files.

**Example Output (Console):**

The linter prints results to the console, grouped by file, indicating errors and warnings with their respective line numbers and messages.

```
--- Results for master-knowledge-base/standards/src/XX-LINT-TESTDUMMY2.md ---
Warnings:
  - [L2] Key order issue: Key 'standard_id' (defined order index 1) is before key 'title' (defined order index 0), violating defined relative order.
Errors:
  - [L2] Duplicate 'standard_id' 'XX-LINT-TESTDUMMY1' also found in: master-knowledge-base/standards/src/XX-LINT-TESTDUMMY1.md
```

## Development Status

*   Core validation logic for many checks is implemented and enhanced.
*   Vocabulary loading from registry files is confirmed and used.
*   Index file loading is now more robust.
*   Unit test suite established and covers key functionalities.
*   Specific checks for `criticality` (field vs. tag) and `change_log_url` (for changelogs) are implemented.
*   Key order violation reporting now lists all issues in a file.

(This README reflects the state after completing Sub-Instruction 2.A tasks for Phase B.)
