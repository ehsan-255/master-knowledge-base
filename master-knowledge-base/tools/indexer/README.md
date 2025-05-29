# Standards Index Generator (`generate_index.py`)

## Purpose

The `generate_index.py` script is responsible for scanning the `/master-knowledge-base/standards/src/` directory, parsing the YAML frontmatter from all Markdown standard documents (`.md` files), and generating a consolidated JSON file (`standards_index.json`). This index file serves as a machine-readable catalog of all atomic standards and their key metadata.

## Planned Features & Specifications

1.  **Input:**
    *   The script will take the path to the `/master-knowledge-base/standards/src/` directory as a primary input.

2.  **Parsing:**
    *   It will recursively walk through the input directory.
    *   For each `.md` file found, it will read the content and parse the YAML frontmatter block.

3.  **Data Extraction:**
    *   From each document's frontmatter, the script will extract the following core metadata fields:
        *   `standard_id`
        *   `title`
        *   `primary_domain`
        *   `sub_domain`
        *   `info-type`
        *   `version`
        *   `status` (This will be derived from the `tags` list, e.g., by finding a tag like `status/draft` and extracting "draft".)
        *   `filepath` (The path to the standard document, relative to the repository root, e.g., `master-knowledge-base/standards/src/XX-YYYY-ZZZZ.md`).
        *   `date-modified`

4.  **Output:**
    *   The script will generate a JSON file named `standards_index.json`.
    *   This output file will be placed in the same directory as the script (`/master-knowledge-base/tools/indexer/`) by default, but an option for a different output directory (e.g., a `/dist/` folder) might be added later.
    *   The JSON file will have a root-level structure including:
        *   `schemaVersion`: A semantic version string (e.g., "1.0.0") indicating the version of the `standards_index.json` schema itself (defined in `standards_index.schema.json`).
        *   `generatedDate`: An ISO-8601 compliant date-time string indicating when the index was generated.
        *   `standards`: An array of objects, where each object represents an atomic standard and contains the extracted metadata fields listed above.

5.  **Schema Conformance:**
    *   The generated `standards_index.json` file MUST conform to the structure and constraints defined in the `standards_index.schema.json` file located in the same directory.

## Usage (Conceptual)

```bash
python generate_index.py
# (Optionally, in the future: python generate_index.py --src /path/to/standards/src --out /path/to/output/dir)
```

## Development Status

This script is currently a skeleton with defined specifications. Implementation of robust file parsing, frontmatter extraction, status derivation, and file walking is pending.
The current skeleton includes a simulation of adding one standard's metadata to the index for illustrative purposes.
The output path for `standards_index.json` is currently set to the script's own directory.
Paths for input and output are relative to the assumed repository root or need to be adjusted based on the actual execution context of the script.
