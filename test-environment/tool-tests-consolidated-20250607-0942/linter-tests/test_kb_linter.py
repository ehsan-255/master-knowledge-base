import unittest
import os
import sys
import tempfile
import shutil

# Add the parent directory (tools/linter) to sys.path to find kb_linter
current_dir = os.path.dirname(os.path.abspath(__file__))
linter_dir = os.path.dirname(current_dir)
sys.path.insert(0, linter_dir)

# Now import from kb_linter
from kb_linter import lint_file, LinterConfig, STANDARD_ID_REGEX, ISO_DATE_REGEX, KEBAB_CASE_TAG_REGEX

class TestKBLinter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a temporary directory structure for testing
        cls.test_root = tempfile.mkdtemp()
        cls.mock_repo_base = os.path.join(cls.test_root, "mock_repo")
        cls.mock_kb_base = os.path.join(cls.mock_repo_base, "master-knowledge-base")
        cls.mock_standards_dist = os.path.join(cls.mock_kb_base, "dist")
        cls.mock_standards_registry = os.path.join(cls.mock_kb_base, "standards", "registry")
        cls.mock_standards_src = os.path.join(cls.mock_kb_base, "standards", "src")

        os.makedirs(cls.mock_repo_base, exist_ok=True)
        os.makedirs(cls.mock_kb_base, exist_ok=True)
        os.makedirs(cls.mock_standards_dist, exist_ok=True)
        os.makedirs(cls.mock_standards_registry, exist_ok=True)
        os.makedirs(cls.mock_standards_src, exist_ok=True)

        # Create a minimal, valid standards_index.json
        index_content = {
            "schemaVersion": "1.0.0",
            "generatedDate": "2023-01-01T00:00:00Z",
            "standards": [
                {"standard_id": "AS-TEST-VALID", "title": "Valid Standard", "filepath": "standards/src/AS-TEST-VALID.md"}
            ]
        }
        with open(os.path.join(cls.mock_standards_dist, "standards_index.json"), "w") as f:
            import json
            json.dump(index_content, f)

        # Create consolidated registry files
        # Create mt-schema-frontmatter.yaml with controlled vocabularies
        frontmatter_schema = """metadata:
  source_document: "MT-SCHEMA-FRONTMATTER.md"
  standard_id: "MT-SCHEMA-FRONTMATTER"
  version: "0.1.0"
  description: "Test frontmatter schema"

controlled_vocabularies:
  info_type:
    - standard-definition
    - policy-document
    - changelog
  
  criticality:
    - level: "P0-Critical"
      description: "Test P0"
    - level: "P1-High"
      description: "Test P1"
  
  primary_domain:
    - id: "AS"
      preferred_label: "Architecture & Structure"
      description: "Test AS domain"
    - id: "CS"
      preferred_label: "Content & Semantics"
      description: "Test CS domain"
  
  lifecycle_gatekeeper:
    - gatekeeper: "Architect-Review"
      name: "Architect Review"
      description: "Test architect review"
    - gatekeeper: "No-Gatekeeper"
      name: "No Formal Gatekeeper"
      description: "Test no gatekeeper"
  
  sub_domain:
    AS:
      - code: "TEST"
        name: "Test Subdomain"
        description: "Test subdomain for AS"
    CS:
      - code: "GENERAL"
        name: "General"
        description: "Test subdomain for CS"
"""
        with open(os.path.join(cls.mock_standards_registry, "mt-schema-frontmatter.yaml"), "w") as f:
            f.write(frontmatter_schema)
        
        # Create mt-registry-tag-glossary.yaml
        tag_glossary = """metadata:
  source_document: "MT-REGISTRY-TAG-GLOSSARY.md"
  standard_id: "MT-REGISTRY-TAG-GLOSSARY"
  version: "0.1.0"
  description: "Test tag glossary"

tag_categories:
  status:
    prefix: "status/"
    description: "Status tags"
    tags:
      - id: "draft"
        full_tag: "status/draft"
        description: "Test draft status"
  topic:
    prefix: "topic/"
    description: "Topic tags"
    tags:
      - id: "test"
        full_tag: "topic/test"
        description: "Test topic"
  kb_id:
    prefix: "kb-id/"
    description: "KB ID tags"
    tags:
      - id: "test-kb"
        full_tag: "kb-id/test-kb"
        description: "Test KB"
  criticality:
    prefix: "criticality/"
    description: "Criticality tags"
    tags:
      - id: "P0-Critical"
        full_tag: "criticality/P0-Critical"
        description: "Test P0 criticality"
      - id: "P1-High"
        full_tag: "criticality/P1-High"
        description: "Test P1 criticality"
"""
        with open(os.path.join(cls.mock_standards_registry, "mt-registry-tag-glossary.yaml"), "w") as f:
            f.write(tag_glossary)
        
        # Keep some .txt files for backward compatibility if needed
        with open(os.path.join(cls.mock_standards_registry, "info_types.txt"), "w") as f:
            f.write("standard-definition\npolicy-document\nchangelog\n")
        with open(os.path.join(cls.mock_standards_registry, "criticality_levels.txt"), "w") as f:
            f.write("p0-critical\np1-high\n")
        with open(os.path.join(cls.mock_standards_registry, "lifecycle_gatekeepers.txt"), "w") as f:
            f.write("Architect-Review\nNo-Gatekeeper\n")
        with open(os.path.join(cls.mock_standards_registry, "tag_categories.txt"), "w") as f:
            f.write("status/\ntopic/\nkb-id/\ncriticality/\n")

        cls.config = LinterConfig(repo_base_path=cls.mock_repo_base)


    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_root)
        # Remove the linter directory from sys.path if it was added
        if linter_dir in sys.path:
            sys.path.remove(linter_dir)

    def create_temp_file(self, filename, content, base_dir=None):
        if base_dir is None:
            base_dir = self.mock_standards_src

        filepath = os.path.join(base_dir, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return filepath

    def assert_has_error(self, results, message_substring, key=None):
        for error in results.get("errors", []):
            if message_substring in error["message"]:
                if key is None or (f"'{key}'" in error["message"] or f"'{key}' " in error["message"]): # check if key is mentioned
                    return
        self.fail(f"Expected error containing '{message_substring}' (and key '{key}' if specified) not found in {results.get('errors')}")

    def assert_has_warning(self, results, message_substring, key=None):
        for warning in results.get("warnings", []):
            if message_substring in warning["message"]:
                if key is None or (f"'{key}'" in warning["message"] or f"'{key}' " in warning["message"]):
                    return
        self.fail(f"Expected warning containing '{message_substring}' (and key '{key}' if specified) not found in {results.get('warnings')}")

    def test_valid_standard_id_format(self):
        content = """---
title: Valid ID
standard_id: AS-TEST-OKAY
info-type: standard-definition
version: 1.0.0
date-created: "2023-01-01T00:00:00Z"
date-modified: "2023-01-01T00:00:00Z"
primary_domain: AS
sub_domain: TEST
tags: [status/draft]
kb-id: test-kb
primary-topic: Test
scope_application: Test
criticality: P1-High
lifecycle_gatekeeper: No-Gatekeeper
impact_areas: ["test"]
change_log_url: ./AS-TEST-OKAY-CHANGELOG.md
---
Content
"""
        filepath = self.create_temp_file("AS-TEST-OKAY.md", content)
        # Create the referenced changelog file
        changelog_filepath = self.create_temp_file("AS-TEST-OKAY-CHANGELOG.md", "# Changelog")

        results = lint_file(filepath, self.config, file_content_raw=content)
        self.assertEqual(len(results["errors"]), 0, f"Should be no errors for valid ID, got: {results['errors']}")
        # Clean up the created files
        os.remove(filepath)
        os.remove(changelog_filepath)

    def test_invalid_standard_id_format_lowercase(self):
        content = """---
title: Invalid ID lowercase
standard_id: as-test-bad
info-type: standard-definition
version: 1.0.0
date-created: "2023-01-01T00:00:00Z"
date-modified: "2023-01-01T00:00:00Z"
primary_domain: AS
sub_domain: TEST
criticality: p1-high
tags: [status/draft]
kb-id: test-kb
primary-topic: Test
scope_application: Test
lifecycle_gatekeeper: No-Gatekeeper
impact_areas: ["test"]
change_log_url: ./as-test-bad-CHANGELOG.md
---
Content
"""
        filepath = self.create_temp_file("as-test-bad.md", content)
        results = lint_file(filepath, self.config, file_content_raw=content)
        self.assert_has_error(results, "fails regex", key="standard_id")
        os.remove(filepath)

    def test_invalid_standard_id_format_nondomain(self):
        content = """---
title: Invalid ID no domain
standard_id: TEST-BAD-ID
info-type: standard-definition
version: 1.0.0
date-created: "2023-01-01T00:00:00Z"
date-modified: "2023-01-01T00:00:00Z"
primary_domain: AS
sub_domain: TEST
criticality: p1-high
tags: [status/draft]
kb-id: test-kb
primary-topic: Test
scope_application: Test
lifecycle_gatekeeper: No-Gatekeeper
impact_areas: ["test"]
change_log_url: ./TEST-BAD-ID-CHANGELOG.md
---
Content
"""
        filepath = self.create_temp_file("TEST-BAD-ID.md", content)
        results = lint_file(filepath, self.config, file_content_raw=content)
        self.assert_has_error(results, "fails regex", key="standard_id")
        os.remove(filepath)

    def test_invalid_date_format(self):
        content = """---
title: Invalid Date
standard_id: AS-TEST-DATEBAD
info-type: standard-definition
version: 1.0.0
date-created: "2023/01/01T00:00:00Z" # Invalid format
date-modified: "2023-01-01T00:00:00Z"
primary_domain: AS
sub_domain: TEST
criticality: p1-high
tags: [status/draft]
kb-id: test-kb
primary-topic: Test
scope_application: Test
lifecycle_gatekeeper: No-Gatekeeper
impact_areas: ["test"]
change_log_url: ./AS-TEST-DATEBAD-CHANGELOG.md
---
Content
"""
        filepath = self.create_temp_file("AS-TEST-DATEBAD.md", content)
        changelog_filepath = self.create_temp_file("AS-TEST-DATEBAD-CHANGELOG.md", "# Changelog")
        results = lint_file(filepath, self.config, file_content_raw=content)
        self.assert_has_error(results, "invalid ISO-8601", key="date-created")
        os.remove(filepath)
        os.remove(changelog_filepath)

    def test_invalid_date_values(self):
        content = """---
title: Invalid Date Values
standard_id: AS-TEST-DATEVALS
info-type: standard-definition
version: 1.0.0
date-created: "2023-99-99T00:00:00Z" # Invalid month/day
date-modified: "2023-01-01T00:00:00Z"
primary_domain: AS
sub_domain: TEST
criticality: p1-high
tags: [status/draft]
kb-id: test-kb
primary-topic: Test
scope_application: Test
lifecycle_gatekeeper: No-Gatekeeper
impact_areas: ["test"]
change_log_url: ./AS-TEST-DATEVALS-CHANGELOG.md
---
Content
"""
        filepath = self.create_temp_file("AS-TEST-DATEVALS.md", content)
        changelog_filepath = self.create_temp_file("AS-TEST-DATEVALS-CHANGELOG.md", "# Changelog")
        results = lint_file(filepath, self.config, file_content_raw=content)
        self.assert_has_error(results, "invalid date/time values", key="date-created")
        os.remove(filepath)
        os.remove(changelog_filepath)

    def test_invalid_info_type(self):
        content = """---
title: Invalid Info Type
standard_id: AS-TEST-INFOBAD
info-type: non-existent-type
version: 1.0.0
date-created: "2023-01-01T00:00:00Z"
date-modified: "2023-01-01T00:00:00Z"
primary_domain: AS
sub_domain: TEST
criticality: p1-high
tags: [status/draft]
kb-id: test-kb
primary-topic: Test
scope_application: Test
lifecycle_gatekeeper: No-Gatekeeper
impact_areas: ["test"]
change_log_url: ./AS-TEST-INFOBAD-CHANGELOG.md
---
Content
"""
        filepath = self.create_temp_file("AS-TEST-INFOBAD.md", content)
        changelog_filepath = self.create_temp_file("AS-TEST-INFOBAD-CHANGELOG.md", "# Changelog")
        results = lint_file(filepath, self.config, file_content_raw=content)
        self.assert_has_error(results, "not in defined list", key="info-type")
        os.remove(filepath)
        os.remove(changelog_filepath)

    def test_invalid_primary_domain(self):
        content = """---
title: Invalid Primary Domain
standard_id: XX-TEST-DOMAINBAD
info-type: standard-definition
version: 1.0.0
date-created: "2023-01-01T00:00:00Z"
date-modified: "2023-01-01T00:00:00Z"
primary_domain: XX
sub_domain: TEST
criticality: p1-high
tags: [status/draft]
kb-id: test-kb
primary-topic: Test
scope_application: Test
lifecycle_gatekeeper: No-Gatekeeper
impact_areas: ["test"]
change_log_url: ./XX-TEST-DOMAINBAD-CHANGELOG.md
---
Content
"""
        filepath = self.create_temp_file("XX-TEST-DOMAINBAD.md", content)
        changelog_filepath = self.create_temp_file("XX-TEST-DOMAINBAD-CHANGELOG.md", "# Changelog")
        results = lint_file(filepath, self.config, file_content_raw=content)
        self.assert_has_error(results, "not in defined domain_codes", key="primary_domain")
        os.remove(filepath)
        os.remove(changelog_filepath)

    def test_invalid_sub_domain_for_primary_domain(self):
        content = """---
title: Invalid Subdomain for Domain
standard_id: AS-TEST-SUBDOMAINBAD
info-type: standard-definition
version: 1.0.0
date-created: "2023-01-01T00:00:00Z"
date-modified: "2023-01-01T00:00:00Z"
primary_domain: AS
sub_domain: NONEXISTENTFORAS
criticality: p1-high
tags: [status/draft]
kb-id: test-kb
primary-topic: Test
scope_application: Test
lifecycle_gatekeeper: No-Gatekeeper
impact_areas: ["test"]
change_log_url: ./AS-TEST-SUBDOMAINBAD-CHANGELOG.md
---
Content
"""
        filepath = self.create_temp_file("AS-TEST-SUBDOMAINBAD.md", content)
        changelog_filepath = self.create_temp_file("AS-TEST-SUBDOMAINBAD-CHANGELOG.md", "# Changelog")
        results = lint_file(filepath, self.config, file_content_raw=content)
        self.assert_has_error(results, "not valid for domain", key="sub_domain")
        os.remove(filepath)
        os.remove(changelog_filepath)

    def test_valid_sub_domain_for_another_primary_domain(self):
        # "GENERAL" is valid for "CS" but not "AS" in our test setup
        content = """---
title: Valid Subdomain for CS, not AS
standard_id: AS-TEST-SUBDOMAINCS
info-type: standard-definition
version: 1.0.0
date-created: "2023-01-01T00:00:00Z"
date-modified: "2023-01-01T00:00:00Z"
primary_domain: AS
sub_domain: GENERAL
criticality: p1-high
tags: [status/draft]
kb-id: test-kb
primary-topic: Test
scope_application: Test
lifecycle_gatekeeper: No-Gatekeeper
impact_areas: ["test"]
change_log_url: ./AS-TEST-SUBDOMAINCS-CHANGELOG.md
---
Content
"""
        filepath = self.create_temp_file("AS-TEST-SUBDOMAINCS.md", content)
        changelog_filepath = self.create_temp_file("AS-TEST-SUBDOMAINCS-CHANGELOG.md", "# Changelog")
        results = lint_file(filepath, self.config, file_content_raw=content)
        self.assert_has_error(results, "not valid for domain 'AS'", key="sub_domain")
        os.remove(filepath)
        os.remove(changelog_filepath)

    def test_key_order_valid(self):
        # Uses DEFINED_KEY_ORDER implicitly
        content = """---
title: Correct Key Order
standard_id: AS-TEST-KEYORDEROK
# aliases: [] # Optional
tags: [status/draft]
kb-id: test-kb
info-type: standard-definition
primary-topic: Test
# related-standards: [] # Optional
version: 1.0.0
date-created: "2023-01-01T00:00:00Z"
date-modified: "2023-01-01T00:00:00Z"
primary_domain: AS
sub_domain: TEST
# scope_application must come before criticality as per DEFINED_KEY_ORDER
scope_application: Test
criticality: P1-High
lifecycle_gatekeeper: No-Gatekeeper
impact_areas: ["test"]
change_log_url: ./AS-TEST-KEYORDEROK-CHANGELOG.md
---
Content
"""
        filepath = self.create_temp_file("AS-TEST-KEYORDEROK.md", content)
        changelog_filepath = self.create_temp_file("AS-TEST-KEYORDEROK-CHANGELOG.md", "# Changelog")
        results = lint_file(filepath, self.config, file_content_raw=content)
        self.assertEqual(len(results["warnings"]), 0, f"Should be no key order warnings, got: {results['warnings']}")
        os.remove(filepath)
        os.remove(changelog_filepath)

    def test_key_order_invalid(self):
        content = """---
standard_id: AS-TEST-KEYORDERBAD # standard_id before title
title: Incorrect Key Order
info-type: standard-definition
version: 1.0.0
date-created: "2023-01-01T00:00:00Z"
date-modified: "2023-01-01T00:00:00Z"
primary_domain: AS
sub_domain: TEST
criticality: p1-high
tags: [status/draft]
kb-id: test-kb
primary-topic: Test
scope_application: Test
lifecycle_gatekeeper: No-Gatekeeper
impact_areas: ["test"]
change_log_url: ./AS-TEST-KEYORDERBAD-CHANGELOG.md
---
Content
"""
        filepath = self.create_temp_file("AS-TEST-KEYORDERBAD.md", content)
        changelog_filepath = self.create_temp_file("AS-TEST-KEYORDERBAD-CHANGELOG.md", "# Changelog")
        results = lint_file(filepath, self.config, file_content_raw=content)
        self.assert_has_warning(results, "Key order issue", key="standard_id")
        os.remove(filepath)
        os.remove(changelog_filepath)

    def test_valid_internal_link(self):
        content = """---
title: Valid Internal Link
standard_id: AS-TEST-LINKOK
# aliases: [] # Optional
tags: [status/draft]
kb-id: test-kb
info-type: standard-definition
primary-topic: Test
# related-standards: [] # Optional
version: 1.0.0
date-created: "2023-01-01T00:00:00Z"
date-modified: "2023-01-01T00:00:00Z"
primary_domain: AS
sub_domain: TEST
scope_application: Test
criticality: P1-High # Corrected case
lifecycle_gatekeeper: No-Gatekeeper
impact_areas: ["test"]
change_log_url: ./AS-TEST-LINKOK-CHANGELOG.md
---
Content with a [[AS-TEST-VALID]] link.
"""
        filepath = self.create_temp_file("AS-TEST-LINKOK.md", content)
        changelog_filepath = self.create_temp_file("AS-TEST-LINKOK-CHANGELOG.md", "# Changelog")
        results = lint_file(filepath, self.config, file_content_raw=content)
        self.assertEqual(len(results["warnings"]), 0, f"Should be no link warnings, got: {results['warnings']}")
        self.assertEqual(len(results["errors"]), 0, f"Should be no link errors, got: {results['errors']}")
        os.remove(filepath)
        os.remove(changelog_filepath)

    def test_invalid_path_based_link(self):
        content = """---
title: Invalid Path Link
standard_id: AS-TEST-LINKBADPATH
info-type: standard-definition
version: 1.0.0
date-created: "2023-01-01T00:00:00Z"
date-modified: "2023-01-01T00:00:00Z"
primary_domain: AS
sub_domain: TEST
criticality: p1-high
tags: [status/draft]
kb-id: test-kb
primary-topic: Test
scope_application: Test
lifecycle_gatekeeper: No-Gatekeeper
impact_areas: ["test"]
change_log_url: ./AS-TEST-LINKBADPATH-CHANGELOG.md
---
Content with a [[./some/path/to/file.md]] link.
"""
        filepath = self.create_temp_file("AS-TEST-LINKBADPATH.md", content)
        changelog_filepath = self.create_temp_file("AS-TEST-LINKBADPATH-CHANGELOG.md", "# Changelog")
        results = lint_file(filepath, self.config, file_content_raw=content)
        self.assert_has_error(results, "Path-based link")
        os.remove(filepath)
        os.remove(changelog_filepath)

    def test_broken_internal_link(self):
        # This standard ID does not exist in our minimal test index
        content = """---
title: Broken Internal Link
standard_id: AS-TEST-LINKBROKEN
info-type: standard-definition
version: 1.0.0
date-created: "2023-01-01T00:00:00Z"
date-modified: "2023-01-01T00:00:00Z"
primary_domain: AS
sub_domain: TEST
criticality: p1-high
tags: [status/draft]
kb-id: test-kb
primary-topic: Test
scope_application: Test
lifecycle_gatekeeper: No-Gatekeeper
impact_areas: ["test"]
change_log_url: ./AS-TEST-LINKBROKEN-CHANGELOG.md
---
Content with a [[XX-NONEXISTENT-STANDARD]] link.
"""
        filepath = self.create_temp_file("AS-TEST-LINKBROKEN.md", content)
        changelog_filepath = self.create_temp_file("AS-TEST-LINKBROKEN-CHANGELOG.md", "# Changelog")
        results = lint_file(filepath, self.config, file_content_raw=content)
        self.assert_has_warning(results, "Potentially broken link")
        os.remove(filepath)
        os.remove(changelog_filepath)

    def test_criticality_field_valid_mixed_case(self):
        content = """---
title: Valid Criticality Field
standard_id: AS-TEST-CRITFOK
info-type: standard-definition
version: 1.0.0
date-created: "2023-01-01T00:00:00Z"
date-modified: "2023-01-01T00:00:00Z"
primary_domain: AS
sub_domain: TEST
tags: [status/draft, criticality/p1-high] # Valid lowercase tag
kb-id: test-kb
primary-topic: Test
scope_application: Test
criticality: P1-High # Valid Mixed Case Field
lifecycle_gatekeeper: No-Gatekeeper
impact_areas: ["test"]
change_log_url: ./AS-TEST-CRITFOK-CHANGELOG.md
---
Content
"""
        filepath = self.create_temp_file("AS-TEST-CRITFOK.md", content)
        changelog_filepath = self.create_temp_file("AS-TEST-CRITFOK-CHANGELOG.md", "# Changelog")
        results = lint_file(filepath, self.config, file_content_raw=content)
        self.assertEqual(len(results["errors"]), 0, f"Should be no criticality field errors, got: {results['errors']}")
        os.remove(filepath)
        os.remove(changelog_filepath)

    def test_criticality_field_invalid_lowercase(self):
        content = """---
title: Invalid Criticality Field (lowercase)
standard_id: AS-TEST-CRITFBADLOW
info-type: standard-definition
version: 1.0.0
date-created: "2023-01-01T00:00:00Z"
date-modified: "2023-01-01T00:00:00Z"
primary_domain: AS
sub_domain: TEST
tags: [status/draft]
kb-id: test-kb
primary-topic: Test
scope_application: Test
criticality: p1-high # Invalid Lowercase Field (should be P1-High)
lifecycle_gatekeeper: No-Gatekeeper
impact_areas: ["test"]
change_log_url: ./AS-TEST-CRITFBADLOW-CHANGELOG.md
---
Content
"""
        filepath = self.create_temp_file("AS-TEST-CRITFBADLOW.md", content)
        changelog_filepath = self.create_temp_file("AS-TEST-CRITFBADLOW-CHANGELOG.md", "# Changelog")
        results = lint_file(filepath, self.config, file_content_raw=content)
        self.assert_has_error(results, "not in defined list. Valid (mixed-case from YAML)", key="criticality")
        os.remove(filepath)
        os.remove(changelog_filepath)

    def test_criticality_tag_valid_lowercase(self):
        content = """---
title: Valid Criticality Tag
standard_id: AS-TEST-CRITTOK
info-type: standard-definition
version: 1.0.0
date-created: "2023-01-01T00:00:00Z"
date-modified: "2023-01-01T00:00:00Z"
primary_domain: AS
sub_domain: TEST
tags: [status/draft, criticality/p0-critical] # Valid lowercase tag
kb-id: test-kb
primary-topic: Test
scope_application: Test
criticality: P0-Critical
lifecycle_gatekeeper: No-Gatekeeper
impact_areas: ["test"]
change_log_url: ./AS-TEST-CRITTOK-CHANGELOG.md
---
Content
"""
        filepath = self.create_temp_file("AS-TEST-CRITTOK.md", content)
        changelog_filepath = self.create_temp_file("AS-TEST-CRITTOK-CHANGELOG.md", "# Changelog")
        results = lint_file(filepath, self.config, file_content_raw=content)
        self.assertEqual(len(results["errors"]), 0, f"Should be no criticality tag errors, got: {results['errors']}")
        os.remove(filepath)
        os.remove(changelog_filepath)

    def test_criticality_tag_invalid_mixedcase(self):
        content = """---
title: Invalid Criticality Tag (mixed case)
standard_id: AS-TEST-CRITTBADMIX
info-type: standard-definition
version: 1.0.0
date-created: "2023-01-01T00:00:00Z"
date-modified: "2023-01-01T00:00:00Z"
primary_domain: AS
sub_domain: TEST
tags: [status/draft, criticality/P0-Critical] # Invalid mixed-case tag
kb-id: test-kb
primary-topic: Test
scope_application: Test
criticality: P0-Critical
lifecycle_gatekeeper: No-Gatekeeper
impact_areas: ["test"]
change_log_url: ./AS-TEST-CRITTBADMIX-CHANGELOG.md
---
Content
"""
        filepath = self.create_temp_file("AS-TEST-CRITTBADMIX.md", content)
        changelog_filepath = self.create_temp_file("AS-TEST-CRITTBADMIX-CHANGELOG.md", "# Changelog")
        results = lint_file(filepath, self.config, file_content_raw=content)
        self.assert_has_error(results, "not in defined list. Valid (lowercase from .txt)")
        os.remove(filepath)
        os.remove(changelog_filepath)

    def test_changelog_self_referential_url_valid(self):
        filename = "MY-CHANGELOG-DOC-CHANGELOG.md"
        content = f"""---
title: My Changelog
standard_id: MY-CHANGELOG-DOC-CHANGELOG
info-type: changelog
version: 1.0.0
date-created: "2023-01-01T00:00:00Z"
date-modified: "2023-01-01T00:00:00Z"
primary_domain: AS
sub_domain: TEST
criticality: P1-High
tags: [status/draft]
kb-id: test-kb
primary-topic: Test
scope_application: Test
lifecycle_gatekeeper: No-Gatekeeper
impact_areas: ["test"]
change_log_url: ./{filename}
---
Content
"""
        filepath = self.create_temp_file(filename, content)
        results = lint_file(filepath, self.config, file_content_raw=content)
        self.assertEqual(len(results["errors"]), 0, f"Should be no changelog URL errors, got: {results['errors']}")
        os.remove(filepath)

    def test_changelog_self_referential_url_invalid(self):
        filename = "MY-CHANGELOG-DOC-INVALID-CHANGELOG.md"
        content = f"""---
title: My Invalid Changelog URL
standard_id: MY-CHANGELOG-DOC-INVALID-CHANGELOG
info-type: changelog
version: 1.0.0
date-created: "2023-01-01T00:00:00Z"
date-modified: "2023-01-01T00:00:00Z"
primary_domain: AS
sub_domain: TEST
criticality: P1-High
tags: [status/draft]
kb-id: test-kb
primary-topic: Test
scope_application: Test
lifecycle_gatekeeper: No-Gatekeeper
impact_areas: ["test"]
change_log_url: ./DIFFERENT-FILENAME.md
---
Content
"""
        filepath = self.create_temp_file(filename, content)
        results = lint_file(filepath, self.config, file_content_raw=content)
        self.assert_has_error(results, "must be self-referential", key="change_log_url")
        os.remove(filepath)

    def test_invalid_lifecycle_gatekeeper(self):
        content = """---
title: Invalid Gatekeeper
standard_id: AS-TEST-LGIBAD
info-type: standard-definition
version: 1.0.0
date-created: "2023-01-01T00:00:00Z"
date-modified: "2023-01-01T00:00:00Z"
primary_domain: AS
sub_domain: TEST
criticality: P1-High
tags: [status/draft]
kb-id: test-kb
primary-topic: Test
scope_application: Test
lifecycle_gatekeeper: Invalid-Gatekeeper-Value
impact_areas: ["test"]
change_log_url: ./AS-TEST-LGIBAD-CHANGELOG.md
---
Content
"""
        filepath = self.create_temp_file("AS-TEST-LGIBAD.md", content)
        changelog_filepath = self.create_temp_file("AS-TEST-LGIBAD-CHANGELOG.md", "# Changelog")
        results = lint_file(filepath, self.config, file_content_raw=content)
        self.assert_has_warning(results, "not in defined list", key="lifecycle_gatekeeper") # It's a warning
        os.remove(filepath)
        os.remove(changelog_filepath)

    def test_invalid_tag_category_prefix(self):
        content = """---
title: Invalid Tag Prefix
standard_id: AS-TEST-TAGPREBAD
info-type: standard-definition
version: 1.0.0
date-created: "2023-01-01T00:00:00Z"
date-modified: "2023-01-01T00:00:00Z"
primary_domain: AS
sub_domain: TEST
criticality: P1-High
tags: [status/draft, invalidprefix/test]
kb-id: test-kb
primary-topic: Test
scope_application: Test
lifecycle_gatekeeper: No-Gatekeeper
impact_areas: ["test"]
change_log_url: ./AS-TEST-TAGPREBAD-CHANGELOG.md
---
Content
"""
        filepath = self.create_temp_file("AS-TEST-TAGPREBAD.md", content)
        changelog_filepath = self.create_temp_file("AS-TEST-TAGPREBAD-CHANGELOG.md", "# Changelog")
        results = lint_file(filepath, self.config, file_content_raw=content)
        self.assert_has_warning(results, "has unrecognized category prefix")
        os.remove(filepath)
        os.remove(changelog_filepath)

    def test_multiple_key_order_invalid(self):
        content = """---
standard_id: AS-TEST-KEYORDERMULTI # standard_id before title (error 1)
title: Incorrect Key Order Multiple
version: 1.0.0 # version before info-type (error 2)
info-type: standard-definition
date-created: "2023-01-01T00:00:00Z"
date-modified: "2023-01-01T00:00:00Z"
primary_domain: AS
sub_domain: TEST
criticality: P1-High # criticality before tags (error 3 if not caught by earlier errors)
tags: [status/draft]
kb-id: test-kb
primary-topic: Test
scope_application: Test
lifecycle_gatekeeper: No-Gatekeeper
impact_areas: ["test"]
change_log_url: ./AS-TEST-KEYORDERMULTI-CHANGELOG.md
---
Content
"""
        filepath = self.create_temp_file("AS-TEST-KEYORDERMULTI.md", content)
        changelog_filepath = self.create_temp_file("AS-TEST-KEYORDERMULTI-CHANGELOG.md", "# Changelog")
        results = lint_file(filepath, self.config, file_content_raw=content)

        warnings = results.get("warnings", [])
        self.assertEqual(len(warnings), 3, f"Expected 3 key order warnings, got {len(warnings)}: {warnings}")

        # Check for specific warnings (order might vary depending on dict iteration)
        messages = [w['message'] for w in warnings]
        self.assertTrue(any("Key 'title'" in m and "before key 'standard_id'" in m for m in messages), "Expected 'title' before 'standard_id' warning")
        self.assertTrue(any("Key 'info-type'" in m and "before key 'version'" in m for m in messages), "Expected 'info-type' before 'version' warning")
        self.assertTrue(any("Key 'tags'" in m and "before key 'criticality'" in m for m in messages), "Expected 'tags' before 'criticality' warning")


        os.remove(filepath)
        os.remove(changelog_filepath)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
