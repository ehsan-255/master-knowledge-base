import unittest
import os
import sys
import tempfile
import shutil
import json

# Add the parent directory (tools/indexer) to sys.path to find generate_index
current_dir = os.path.dirname(os.path.abspath(__file__))
indexer_dir = os.path.dirname(current_dir)
sys.path.insert(0, indexer_dir)

# Now import from generate_index
from generate_index import get_frontmatter_from_content, extract_metadata, main as generate_index_main, get_status_from_tags # Removed validate_index_against_schema

class TestGenerateIndex(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_root = tempfile.mkdtemp()
        cls.mock_repo_base = os.path.join(cls.test_root, "mock_repo")

        # Structure expected by the indexer and linter (for schema/registry files)
        cls.mock_kb_base = os.path.join(cls.mock_repo_base, "master-knowledge-base")
        cls.mock_standards_dist = os.path.join(cls.mock_kb_base, "dist")
        cls.mock_standards_registry = os.path.join(cls.mock_kb_base, "standards", "registry")
        cls.mock_indexer_tools = os.path.join(cls.mock_kb_base, "tools", "indexer") # For schema
        cls.mock_src_dir = os.path.join(cls.mock_kb_base, "standards", "src", "test_docs")


        os.makedirs(cls.mock_repo_base, exist_ok=True)
        os.makedirs(cls.mock_kb_base, exist_ok=True)
        os.makedirs(cls.mock_standards_dist, exist_ok=True)
        os.makedirs(cls.mock_standards_registry, exist_ok=True)
        os.makedirs(cls.mock_indexer_tools, exist_ok=True)
        os.makedirs(cls.mock_src_dir, exist_ok=True)

        # Create a minimal, valid standards_index.schema.json
        # This is used by the indexer to validate its own output.
        schema_content = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "Standards Index Schema",
            "description": "Schema for the standards_index.json file.",
            "type": "object",
            "properties": {
                "schemaVersion": {"type": "string"},
                "generatedDate": {"type": "string", "format": "date-time"},
                "standards": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "standard_id": {"type": "string", "pattern": "^[A-Z]{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*$"},
                            "title": {"type": "string"},
                            "filepath": {"type": "string"},
                            "primary_domain": {"type": "string"},
                            "sub_domain": {"type": "string"},
                            "status": {"type": "string"},
                            "version": {"type": "string"},
                            "date-created": {"type": "string", "format": "date-time"},
                            "date-modified": {"type": "string", "format": "date-time"},
                            "criticality": {"type": "string"},
                            "lifecycle_gatekeeper": {"type": "string"}
                        },
                        "required": [
                            "standard_id", "title", "filepath", "primary_domain", "sub_domain",
                            "status", "version", "date-created", "date-modified",
                            "criticality", "lifecycle_gatekeeper"
                        ]
                    }
                }
            },
            "required": ["schemaVersion", "generatedDate", "standards"]
        }
        with open(os.path.join(cls.mock_indexer_tools, "standards_index.schema.json"), "w") as f:
            json.dump(schema_content, f)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_root)
        if indexer_dir in sys.path:
            sys.path.remove(indexer_dir)

    def create_temp_md_file(self, filename, content, base_dir=None):
        if base_dir is None:
            base_dir = self.mock_src_dir

        filepath = os.path.join(base_dir, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return filepath

    def test_extract_frontmatter_valid(self):
        content = """---
title: Test Standard
standard_id: AS-TEST-001
version: 1.0.0
primary_domain: AS
sub_domain: SCHEMA
status: draft # This will be derived by process_markdown_file
tags: [status/draft]
date-created: 2023-01-01T10:00:00Z
date-modified: 2023-01-02T10:00:00Z
criticality: P2-Medium
lifecycle_gatekeeper: Architect-Review
---
Document content.
"""
        filepath = self.create_temp_md_file("AS-TEST-001.md", content)
        # Read the raw content for get_frontmatter_from_content
        with open(filepath, 'r') as f:
            raw_content = f.read()
        fm_str = get_frontmatter_from_content(raw_content)
        self.assertIsNotNone(fm_str)
        import yaml # Need yaml for this test part
        fm_data_loaded = yaml.safe_load(fm_str)
        self.assertEqual(fm_data_loaded.get("title"), "Test Standard")
        self.assertEqual(fm_data_loaded.get("standard_id"), "AS-TEST-001")
        os.remove(filepath)

    def test_extract_metadata_and_status_derivation(self):
        # This test now uses extract_metadata which gets raw file content
        raw_file_content = """---
title: Test Standard Process
standard_id: CS-PROCESS-001
version: 0.1.0
primary_domain: CS
sub_domain: POLICY
tags: [status/approved, topic/testing]
date-created: "2023-02-01T11:00:00Z" # Required by schema if not derived
date-modified: "2023-02-02T11:00:00Z" # Required by schema
criticality: P1-High # Required by schema
lifecycle_gatekeeper: SME-Consensus # Required by schema
# Minimal required fields for INDEX_REQUIRED_FIELDS for this test
info-type: standard-definition # Required by schema
status: approved # This will be overridden by get_status_from_tags
filepath: master-knowledge-base/standards/src/test_docs/CS-PROCESS-001.md # Required by schema
---
Document content.
"""
        # filepath_rel needs to be relative to the mock_repo_base for extract_metadata
        filepath_rel = os.path.join("master-knowledge-base", "standards", "src", "test_docs", "CS-PROCESS-001.md")

        # Create the dummy file so extract_metadata can (in theory) read it, though we pass content
        # However, extract_metadata itself doesn't read, it expects file_content.
        # The main loop in generate_index reads, then calls extract_metadata.
        # So, for this unit test, we directly pass the content.

        entry, error_reason = extract_metadata(filepath_rel, raw_file_content)

        self.assertIsNone(error_reason, f"extract_metadata failed: {error_reason}")
        self.assertIsNotNone(entry, "Entry should not be None")

        self.assertEqual(entry["standard_id"], "CS-PROCESS-001")
        self.assertEqual(entry["title"], "Test Standard Process")
        self.assertEqual(entry["filepath"], filepath_rel) # Should be unchanged
        self.assertEqual(entry["primary_domain"], "CS")
        self.assertEqual(entry["sub_domain"], "POLICY")
        self.assertEqual(entry["status"], "approved") # Derived from tags
        self.assertEqual(entry["version"], "0.1.0")
        # Note: extract_metadata doesn't populate all schema fields by itself,
        # It relies on what's in frontmatter and what it's programmed to derive (like status).
        # The INDEX_REQUIRED_FIELDS check within extract_metadata is key.
        self.assertEqual(entry["date-modified"], "2023-02-02T11:00:00Z")
        # Fields like "criticality", "lifecycle_gatekeeper" are not directly processed by extract_metadata
        # beyond being fetched if present, so we don't check them here unless they are part of INDEX_REQUIRED_FIELDS.
        # The schema used in setUpClass defines criticality & lifecycle_gatekeeper as required.
        # The test data for raw_file_content ensures these are present.
        # Let's add them to the check to be sure they are picked up.
        # The current extract_metadata only explicitly copies a few fields. This needs to be more generic.

        # Ah, extract_metadata only directly copies some fields. Let's adjust.
        # It copies: "standard_id", "title", "primary_domain", "sub_domain", "info-type", "version", "date-modified"
        # and derives "status" and adds "filepath".
        # So, the test should only check these.
        # The other fields like criticality, lifecycle_gatekeeper are NOT part of `extract_metadata`'s direct output construction
        # other than being part of the frontmatter that might be checked for INDEX_REQUIRED_FIELDS.
        # This test is for what extract_metadata *itself* produces.

        # Re-evaluating what extract_metadata does:
        # It gets all fields listed in `direct_fields` from frontmatter.
        # `direct_fields = ["standard_id", "title", "primary_domain", "sub_domain", "info-type", "version", "date-modified"]`
        # It derives `status`. It sets `filepath`.
        # Then it checks `INDEX_REQUIRED_FIELDS`.
        # `INDEX_REQUIRED_FIELDS = ["standard_id", "title", "primary_domain", "sub_domain", "info-type", "version", "status", "filepath", "date-modified"]`
        # It does NOT explicitly copy criticality or lifecycle_gatekeeper into its returned dict.
        # This is a bug in extract_metadata or my understanding of its role.
        # For now, the test will reflect what it *currently* does.
        # The schema requires them, so if they are not returned by extract_metadata, validation will fail later.
        # This means the test data for raw_file_content needs to be perfect according to schema for `extract_metadata` to pass its internal check.

        # For the test to pass with current extract_metadata, criticality & lifecycle_gatekeeper should NOT be checked in the entry dict.
        # They are checked for presence by extract_metadata for its internal validation against INDEX_REQUIRED_FIELDS, but not returned.
        # UPDATE: Now extract_metadata should return all INDEX_REQUIRED_FIELDS if present in frontmatter.
        self.assertEqual(entry["criticality"], "P1-High")
        self.assertEqual(entry["lifecycle_gatekeeper"], "SME-Consensus")
        self.assertEqual(entry["date-created"], "2023-02-01T11:00:00Z")


    def test_duplicate_standard_id_skipped(self):
        content1 = """---
title: First Standard
standard_id: AS-DUPE-001
version: 1.0.0
primary_domain: AS
sub_domain: TEST
info-type: standard-definition
status: active
tags: [status/active]
date-created: "2023-01-01T00:00:00Z"
date-modified: "2023-01-01T00:00:00Z"
criticality: P1-High
lifecycle_gatekeeper: No-Gatekeeper
filepath: master-knowledge-base/standards/src/test_docs/AS-DUPE-001.md
---
Content1
"""
        content2 = """---
title: Second Standard With Same ID
standard_id: AS-DUPE-001
version: 1.0.1
primary_domain: CS
sub_domain: GENERAL
info-type: policy-document
status: draft
tags: [status/draft]
date-created: "2023-02-01T00:00:00Z"
date-modified: "2023-02-01T00:00:00Z"
criticality: P2-Medium
lifecycle_gatekeeper: Architect-Review
filepath: master-knowledge-base/standards/src/test_docs/CS-DUPE-SAMEID-002.md
---
Content2
"""
        file1_path_abs = self.create_temp_md_file("AS-DUPE-001.md", content1)
        file2_path_abs = self.create_temp_md_file("CS-DUPE-SAMEID-002.md", content2)

        # Use a temporary output directory for this test run
        temp_output_dir = tempfile.mkdtemp(dir=self.test_root)

        # Run the main indexer script
        # Note: generate_index_main uses sys.argv, so we need to mock that or use a wrapper
        # For simplicity, we'll reconstruct the argument string for direct call
        # The generate_index.py script's main() function directly uses argparse with sys.argv.
        # To test it, we'd typically need to mock sys.argv or use subprocess.
        # However, since generate_index_main is imported, we can call it with mocked args.

        mock_args = [
            "--repo-base", self.mock_repo_base,
            "--src-dirs", os.path.relpath(self.mock_src_dir, self.mock_repo_base), # relative path
            "--output-dir", os.path.relpath(temp_output_dir, self.mock_repo_base), # relative path
            "--schema-file", os.path.relpath(os.path.join(self.mock_indexer_tools, "standards_index.schema.json"), self.mock_repo_base)
        ]

        import argparse
        original_argv = sys.argv
        sys.argv = ["generate_index.py"] + mock_args

        generate_index_main() # Call the main function from the script

        sys.argv = original_argv # Restore original argv

        # Check the generated index
        output_index_file = os.path.join(temp_output_dir, "standards_index.json")
        self.assertTrue(os.path.exists(output_index_file))

        with open(output_index_file, "r") as f:
            index_data = json.load(f)

        self.assertEqual(len(index_data["standards"]), 1, "Expected only one entry due to duplicate ID")
        kept_entry = index_data["standards"][0]
        self.assertEqual(kept_entry["standard_id"], "AS-DUPE-001")
        self.assertIn(kept_entry["title"], ["First Standard", "Second Standard With Same ID"], "Kept entry title is not one of the expected titles.")

        os.remove(file1_path_abs)
        os.remove(file2_path_abs)
        shutil.rmtree(temp_output_dir)


if __name__ == '__main__':
    # Need to ensure CWD is tools/indexer for schema path resolution in generate_index.py if run directly
    # For `python -m unittest discover`, this is handled by test runner's start dir.
    # If running this file directly:
    # original_cwd = os.getcwd()
    # if os.path.basename(original_cwd) == "tests":
    #    os.chdir(indexer_dir) # Change to 'tools/indexer'
    #    print(f"Changed CWD for direct script run: {os.getcwd()}")

    unittest.main(argv=['first-arg-is-ignored'], exit=False)

    # if os.path.basename(original_cwd) == "tests":
    #    os.chdir(original_cwd) # Change back
