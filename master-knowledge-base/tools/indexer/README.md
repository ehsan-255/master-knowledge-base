# Standards Index Generator (`generate_index.py`)

## Purpose

The `generate_index.py` script scans a specified directory for Markdown standard documents (`.md` files), parses their YAML frontmatter, and generates a consolidated JSON file (`standards_index.json`). This index serves as a machine-readable catalog of all atomic standards and their key metadata, validated against a JSON schema.

## Features & Functionality

1.  **Input & Configuration:**
    *   Accepts command-line arguments for specifying repository base path, source directory for standards, output directory for the index, path to the JSON schema, and the output filename.
    *   Recursively walks the source directory.

2.  **Parsing & Data Extraction:**
    *   For each `.md` file, it reads the content and parses the YAML frontmatter.
    *   Extracts core metadata: `standard_id`, `title`, `primary_domain`, `sub_domain`, `info-type`, `version`, `status` (derived from `tags`), `filepath` (relative to repo root), and `date-modified`.
    *   Skips files if essential fields required by `INDEX_REQUIRED_FIELDS` (matching the schema) are missing or empty, or if YAML is invalid.

3.  **Output (`standards_index.json`):**
    *   Generated JSON file includes:
        *   `schemaVersion`: Semantic version of the index schema.
        *   `generatedDate`: ISO-8601 date-time of generation.
        *   `standards`: An array of objects, each representing an atomic standard with its extracted metadata.

4.  **Schema Validation:**
    *   The generated `standards_index.json` data is validated against a specified JSON schema file (e.g., `standards_index.schema.json`) before writing.
    *   The index is only written if it successfully validates against the schema.

5.  **Reporting:**
    *   Prints a summary to the console detailing total files found, successfully indexed files, and skipped files (with reasons).
    *   Reports schema validation success or failure, including error details if validation fails.

## Usage

```bash
python master-knowledge-base/tools/indexer/generate_index.py [OPTIONS]
```

**Command-Line Arguments:**

*   `--repo-base REPO_BASE`
    *   Path to the repository root. Default: `.` (current directory).
*   `--src-dir SRC_DIR`
    *   Source directory for standards files, relative to `repo-base`. 
    *   Default: `master-knowledge-base/standards/src`.
*   `--output-dir OUTPUT_DIR`
    *   Output directory for the index file, relative to `repo-base`. 
    *   Default: `master-knowledge-base/dist`.
*   `--schema-file SCHEMA_FILE`
    *   Path to the JSON schema for the index, relative to `repo-base`. 
    *   Default: `master-knowledge-base/tools/indexer/standards_index.schema.json`.
*   `--output-filename OUTPUT_FILENAME`
    *   Filename for the generated index. Default: `standards_index.json`.

**Example:**

To run with default settings from the repository root:
```bash
python master-knowledge-base/tools/indexer/generate_index.py
```

To specify a different source directory:
```bash
python master-knowledge-base/tools/indexer/generate_index.py --src-dir my_custom_standards/
```

## Development Status & Next Steps

*   Core functionality for parsing, metadata extraction, status derivation, directory traversal, schema validation, and conditional file writing is implemented.
*   Command-line arguments have been added for configurability.
*   Schema for `standard_id` and `sub_domain` patterns in `standards_index.schema.json` aligned with `[[MT-SCHEMA-FRONTMATTER]]`.

**Key areas for ongoing "Productionizing" (Phase B):**
*   **Unit Tests:** Writing comprehensive unit tests for all key indexing functions (metadata extraction, status derivation, schema validation logic).
*   **Robustness:** Continued refinement of error handling for edge cases in file content or system interactions.
