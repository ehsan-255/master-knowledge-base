---
title: Standards Index Generator (`generate_index.py`)
standard_id: DOC-TOOLS-INDEXER-README
aliases:
  - Indexer README
tags:
  - status/active
  - content-type/documentation
  - topic/readme
  - kb-id/tools
kb-id: tools
info-type: guide-document
primary-topic: Overview and guidance for the indexer directory and its contents.
related-standards: []
version: 1.0.0
date-created: '2025-06-01T11:33:47Z'
date-modified: '2025-06-01T11:33:47Z'
primary_domain: GM
sub_domain: GUIDE
scope_application: Provides an overview for the /app/master-knowledge-base/tools/indexer/README.md.
criticality: P4-Informational
lifecycle_gatekeeper: No-Gatekeeper
impact_areas:
  - documentation
  - usability
change_log_url: ./README-CHANGELOG.MD
---

# Standards Index Generator (`generate_index.py`)

## Purpose

The `generate_index.py` script scans specified source directories for Markdown standard documents (`.md` files), parses their YAML frontmatter, and generates a consolidated JSON file (`standards_index.json`). This index serves as a machine-readable catalog of all atomic standards and their key metadata, validated against a JSON schema.

## Features & Functionality

1.  **Input & Configuration:**
    *   Accepts command-line arguments for specifying repository base path, source directories for standards (multiple allowed), output directory for the index, path to the JSON schema, output filename, and logging level.
    *   Recursively walks the source directories.

2.  **Parsing & Data Extraction:**
    *   For each `.md` file, it reads the content and parses the YAML frontmatter.
    *   Extracts core metadata required by the schema: `standard_id`, `title`, `primary_domain`, `sub_domain`, `info-type`, `version`, `status` (derived from `tags`), `filepath` (relative to repo root), `date-created`, `date-modified`, `criticality`, and `lifecycle_gatekeeper`.
    *   Skips files if essential fields required by `INDEX_REQUIRED_FIELDS` (matching the schema) are missing or empty, or if YAML is invalid.
    *   **Duplicate Handling:**
        *   Keeps track of `standard_id`s already processed. If a file is encountered that claims an already seen `standard_id`, it logs a critical error and skips adding the duplicate to the index (keeps the first one encountered by `os.walk`).
        *   Keeps track of file paths already processed. If the same file path is encountered multiple times (e.g., due to overlapping source directories), it ensures it's processed only once.

3.  **Output (`standards_index.json`):**
    *   Generated JSON file includes:
        *   `schemaVersion`: Semantic version of the index schema.
        *   `generatedDate`: ISO-8601 date-time of generation.
        *   `standards`: An array of objects, each representing an atomic standard with its extracted metadata.

4.  **Schema Validation:**
    *   The generated `standards_index.json` data is validated against a specified JSON schema file (e.g., `standards_index.schema.json`) before writing.
    *   The index is only written if it successfully validates against the schema.

5.  **Reporting & Logging:**
    *   Uses the Python `logging` module (configurable via `--log-level`).
    *   Default log level is `INFO`. Debug messages are available via `--log-level DEBUG`.
    *   Logs a summary detailing total files found, successfully indexed files, and skipped files (with reasons).
    *   Reports schema validation success or failure, including error details if validation fails.

## Unit Tests

A suite of unit tests using the `unittest` framework is implemented in `master-knowledge-base/tools/indexer/tests/test_generate_index.py`. These tests cover:
*   Frontmatter extraction.
*   Metadata processing, including status derivation from tags.
*   Handling of duplicate `standard_id`s.
The test suite currently includes 3 tests.

## Usage

```bash
python master-knowledge-base/tools/indexer/generate_index.py [OPTIONS]
```

**Command-Line Arguments:**

*   `--repo-base REPO_BASE`
    *   Path to the repository root. Default: `.` (current directory).
*   `--src-dirs SRC_DIRS [SRC_DIRS ...]`
    *   One or more source directories for standards files, relative to `repo-base`.
    *   Default: `master-knowledge-base/standards/src`.
*   `--output-dir OUTPUT_DIR`
    *   Output directory for the index file, relative to `repo-base`. 
    *   Default: `master-knowledge-base/dist`.
*   `--schema-file SCHEMA_FILE`
    *   Path to the JSON schema for the index, relative to `repo-base`. 
    *   Default: `master-knowledge-base/tools/indexer/standards_index.schema.json`.
*   `--output-filename OUTPUT_FILENAME`
    *   Filename for the generated index. Default: `standards_index.json`.
*   `--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}`
    *   Set the logging level. Default: `INFO`.

**Example:**

To run with default settings from the repository root:
```bash
python master-knowledge-base/tools/indexer/generate_index.py
```

To specify multiple source directories and enable debug logging:
```bash
python master-knowledge-base/tools/indexer/generate_index.py \
    --src-dirs master-knowledge-base/standards/src master-knowledge-base/standards/registry \
    --log-level DEBUG
```

## Development Status

*   Core functionality for parsing, metadata extraction, status derivation, directory traversal, schema validation, and conditional file writing is implemented.
*   Command-line arguments provide configurability for paths and logging.
*   Duplicate `standard_id` and file path handling are implemented.
*   Unit tests cover core extraction and duplicate handling logic.
*   Logging has replaced most direct `print` statements for console output management.

(This README reflects the state after completing Sub-Instruction 2.B tasks for Phase B.)
