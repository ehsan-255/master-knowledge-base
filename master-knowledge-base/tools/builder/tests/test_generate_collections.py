import unittest
import sys
import os

# Adjust the path to import from the parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from generate_collections import generate_gfm_anchor, get_body_content_from_markdown, filter_standards

class TestGenerateCollections(unittest.TestCase):

    def test_generate_gfm_anchor(self):
        used_anchors = set()
        self.assertEqual(generate_gfm_anchor("Test Heading", used_anchors), "test-heading")
        self.assertEqual(generate_gfm_anchor("Test Heading", used_anchors), "test-heading-1") # Duplicate
        self.assertEqual(generate_gfm_anchor("Another Heading", used_anchors), "another-heading")
        used_anchors.clear() # Reset for next assertion group

        self.assertEqual(generate_gfm_anchor("Heading with Spaces", used_anchors), "heading-with-spaces")
        self.assertEqual(generate_gfm_anchor(" كثير من الكلام ", used_anchors), "كثير-من-الكلام") # Arabic text
        self.assertEqual(generate_gfm_anchor("Title with !@#$%^&*()_+", used_anchors), "title-with-_")
        self.assertEqual(generate_gfm_anchor("  leading/trailing hyphens--", used_anchors), "leadingtrailing-hyphens")
        self.assertEqual(generate_gfm_anchor("", used_anchors), "untitled-section")
        self.assertEqual(generate_gfm_anchor("!@#$", used_anchors), "section") # Only special chars
        self.assertEqual(generate_gfm_anchor("Duplicate", used_anchors), "duplicate")
        self.assertEqual(generate_gfm_anchor("Duplicate", used_anchors), "duplicate-1")
        self.assertEqual(generate_gfm_anchor("Duplicate", used_anchors), "duplicate-2")

    def test_get_body_content_from_markdown(self):
        content_with_fm = """---
title: Test
---
This is the body.
Another line."""
        self.assertEqual(get_body_content_from_markdown(content_with_fm), "This is the body.\nAnother line.")

        content_without_fm = "This is the body directly.\nNo frontmatter."
        self.assertEqual(get_body_content_from_markdown(content_without_fm), content_without_fm)

        empty_content = ""
        self.assertEqual(get_body_content_from_markdown(empty_content), "")

        only_fm = """---
title: Only Frontmatter
---"""
        self.assertEqual(get_body_content_from_markdown(only_fm), "")

        malformed_fm_start = """--
title: Malformed
---
Body here."""
        self.assertEqual(get_body_content_from_markdown(malformed_fm_start), malformed_fm_start)

        no_fm_end = """---
title: No End
Actually part of body.
"""
        # This behavior might be debatable, but current function extracts from first ---
        # if no second --- is found, it returns everything after the first ---
        # For this test, let's assume the original function's behavior is to return content after the first '---'
        # if a closing '---' is not found on a new line.
        # Based on re-reading `get_body_content_from_markdown` it would return "" if no closing ---
        # The original test for this case was likely flawed.
        # It should return "" if the frontmatter doesn't properly close.
        # Let's re-evaluate the function's logic:
        # if not lines or not lines[0].startswith("---"): return file_content
        # fm_end_index = -1
        # for i, line in enumerate(lines[1:], start=1):
        #     if line.startswith("---"): fm_end_index = i; break
        # if fm_end_index == -1: return file_content -> THIS IS THE CASE FOR "no_fm_end"
        # So, it should return the original content if no *second* "---" is found.
        self.assertEqual(get_body_content_from_markdown(no_fm_end), no_fm_end)


    def test_filter_standards(self):
        all_standards_map = {
            "STD-001": {"standard_id": "STD-001", "title": "Alpha Standard", "domain": "AS", "status": "live", "tags": ["core", "important"]},
            "STD-002": {"standard_id": "STD-002", "title": "Bravo Standard", "domain": "AS", "status": "draft", "tags": ["core"]},
            "STD-003": {"standard_id": "STD-003", "title": "Charlie Standard", "domain": "CS", "status": "live", "tags": ["important"]},
            "STD-004": {"standard_id": "STD-004", "title": "Delta Standard", "domain": "MT", "status": "deprecated", "tags": []},
            "STD-005": {"standard_id": "STD-005", "title": "Echo Standard", "domain": "AS", "status": "live", "custom_field": "value1"},
        }

        # Test equals
        criteria_equals = [{"field": "domain", "operator": "equals", "value": "AS"}]
        filtered = filter_standards(all_standards_map, criteria_equals)
        self.assertEqual(len(filtered), 3)
        self.assertIn(all_standards_map["STD-001"], filtered)
        self.assertIn(all_standards_map["STD-002"], filtered)
        self.assertIn(all_standards_map["STD-005"], filtered)

        # Test in
        criteria_in = [{"field": "status", "operator": "in", "value": ["live", "draft"]}]
        filtered = filter_standards(all_standards_map, criteria_in)
        self.assertEqual(len(filtered), 4) # STD-001, STD-002, STD-003, STD-005
        self.assertNotIn(all_standards_map["STD-004"], filtered)


        # Test not_equals
        criteria_not_equals = [{"field": "status", "operator": "not_equals", "value": "live"}]
        filtered = filter_standards(all_standards_map, criteria_not_equals)
        self.assertEqual(len(filtered), 2) # STD-002 (draft), STD-004 (deprecated)
        self.assertIn(all_standards_map["STD-002"], filtered)
        self.assertIn(all_standards_map["STD-004"], filtered)

        # Test multiple criteria (AND logic)
        criteria_multiple = [
            {"field": "domain", "operator": "equals", "value": "AS"},
            {"field": "status", "operator": "equals", "value": "live"}
        ]
        filtered = filter_standards(all_standards_map, criteria_multiple)
        self.assertEqual(len(filtered), 2) # STD-001, STD-005
        self.assertIn(all_standards_map["STD-001"], filtered)
        self.assertIn(all_standards_map["STD-005"], filtered)


        # Test criteria resulting in no matches
        criteria_no_match = [{"field": "domain", "operator": "equals", "value": "XYZ"}]
        filtered = filter_standards(all_standards_map, criteria_no_match)
        self.assertEqual(len(filtered), 0)

        # Test empty criteria list (should return all)
        filtered_empty_criteria = filter_standards(all_standards_map, [])
        self.assertEqual(len(filtered_empty_criteria), len(all_standards_map))

        # Test field not present in a standard
        criteria_missing_field = [{"field": "custom_field", "operator": "equals", "value": "value1"}]
        filtered = filter_standards(all_standards_map, criteria_missing_field)
        self.assertEqual(len(filtered), 1)
        self.assertIn(all_standards_map["STD-005"], filtered)

        criteria_missing_field_no_match = [{"field": "non_existent_field", "operator": "equals", "value": "any"}]
        filtered = filter_standards(all_standards_map, criteria_missing_field_no_match)
        self.assertEqual(len(filtered), 0)


if __name__ == '__main__':
    unittest.main()
