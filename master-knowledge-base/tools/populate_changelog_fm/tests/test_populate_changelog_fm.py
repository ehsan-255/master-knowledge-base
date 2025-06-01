import unittest
import os
import sys
import tempfile
import shutil
from ruamel.yaml import YAML

# Simplified sys.path manipulation: add script's directory directly
current_dir = os.path.dirname(os.path.abspath(__file__)) # .../tests
script_dir = os.path.dirname(current_dir) # .../populate_changelog_fm (directory containing the .py file)

if script_dir not in sys.path:
    sys.path.insert(0, script_dir)
elif sys.path[0] != script_dir: # If already present but not first, move to front
    sys.path.remove(script_dir)
    sys.path.insert(0, script_dir)

import importlib.util
module_path = os.path.join(script_dir, "populate_changelog_fm.py")
spec = importlib.util.spec_from_file_location("populate_changelog_fm_module", module_path)
populate_changelog_fm_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(populate_changelog_fm_module)

process_changelog_file = populate_changelog_fm_module.process_changelog_file
CHANGELOG_KEY_ORDER = populate_changelog_fm_module.CHANGELOG_KEY_ORDER
DEFAULT_CHANGELOG_CRITICALITY_MIXED_CASE = populate_changelog_fm_module.DEFAULT_CHANGELOG_CRITICALITY_MIXED_CASE


class TestPopulateChangelogFM(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def create_temp_file(self, filename, content):
        filepath = os.path.join(self.test_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return filepath

    def read_frontmatter_from_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if not lines or not lines[0].strip() == "---":
            return None
        fm_end_line_idx = -1
        for i, line in enumerate(lines[1:]):
            if line.strip() == "---":
                fm_end_line_idx = i + 1
                break
        if fm_end_line_idx == -1:
            return None

        frontmatter_str = "".join(lines[1:fm_end_line_idx])
        yaml = YAML(typ='safe')
        return yaml.load(frontmatter_str)

    def test_populate_new_changelog_fm(self):
        parent_id = "AS-TESTPARENT-001"
        parent_filename = f"{parent_id}.MD"
        changelog_filename = f"{parent_id}-CHANGELOG.MD"

        parent_content = f"""---
title: Test Parent Standard
standard_id: {parent_id}
kb-id: "test-kb"
primary_domain: AS
sub_domain: TESTSUB
version: "1.2.3"
date-created: "2022-01-01T00:00:00Z"
criticality: P1-High
lifecycle_gatekeeper: "Architect-Review"
impact_areas: ["testing", "docs"]
---
Parent content.
"""
        self.create_temp_file(parent_filename, parent_content)

        changelog_initial_content = """# Initial Changelog Content
Some text.
"""
        changelog_filepath = self.create_temp_file(changelog_filename, changelog_initial_content)

        # Ensure logging is suppressed or captured if it prints to stdout by default in script
        # For now, assume it's handled or test with --log-level ERROR if script has it

        success = process_changelog_file(changelog_filepath, dry_run=False, force_overwrite_fm=True)
        self.assertTrue(success, "Processing changelog file should succeed.")

        fm = self.read_frontmatter_from_file(changelog_filepath)
        self.assertIsNotNone(fm, "Frontmatter should exist after processing.")

        self.assertEqual(fm.get("standard_id"), f"{parent_id}-CHANGELOG")
        self.assertEqual(fm.get("title"), f"Changelog: Test Parent Standard")
        self.assertEqual(fm.get("info-type"), "changelog")
        self.assertEqual(fm.get("related-standards"), [parent_id])
        self.assertEqual(fm.get("primary_domain"), "AS")
        self.assertEqual(fm.get("sub_domain"), "TESTSUB")
        self.assertEqual(fm.get("version"), "1.2.3") # Takes parent version
        self.assertEqual(fm.get("criticality"), "P1-High") # Takes parent criticality
        self.assertEqual(fm.get("change_log_url"), f"./{changelog_filename}")
        self.assertIn("status/active", fm.get("tags", []))

        # Check key order
        fm_keys = list(fm.keys())
        expected_keys_present = [k for k in CHANGELOG_KEY_ORDER if k in fm_keys]
        self.assertEqual(fm_keys, expected_keys_present, "Frontmatter key order is not as expected.")

    def test_populate_changelog_default_criticality(self):
        parent_id = "CS-TESTPARENT-002"
        parent_filename = f"{parent_id}.MD"
        changelog_filename = f"{parent_id}-CHANGELOG.MD"

        parent_content = f"""---
title: Parent Standard No Criticality
standard_id: {parent_id}
kb-id: "test-kb"
primary_domain: CS
sub_domain: GENERAL
version: "0.5.0"
date-created: "2022-03-01T00:00:00Z"
# criticality field missing
lifecycle_gatekeeper: "No-Gatekeeper"
---
Parent content.
"""
        self.create_temp_file(parent_filename, parent_content)
        changelog_filepath = self.create_temp_file(changelog_filename, "# Changelog")

        success = process_changelog_file(changelog_filepath, dry_run=False, force_overwrite_fm=True)
        self.assertTrue(success)
        fm = self.read_frontmatter_from_file(changelog_filepath)
        self.assertIsNotNone(fm)
        self.assertEqual(fm.get("criticality"), DEFAULT_CHANGELOG_CRITICALITY_MIXED_CASE)


if __name__ == '__main__':
    # Adjust sys.path for direct script execution if necessary, similar to other test files
    # This setup assumes 'python -m unittest discover' from 'tools' or 'tools/populate_changelog_fm'
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
