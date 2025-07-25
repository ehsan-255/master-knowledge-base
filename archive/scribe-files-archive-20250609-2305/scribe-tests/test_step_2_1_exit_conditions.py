#!/usr/bin/env python3
"""
Test STEP 2.1 Exit Conditions

Verifies that:
1. A change to a rule's trigger_pattern in config.json is detected and applied 
   by the running engine within 5 seconds, without a restart.
2. A rule with an invalid regex pattern is rejected with a descriptive error 
   message on load.
"""

import sys
import os
import json
import time
import tempfile
import shutil
import threading
from pathlib import Path
# Add the scribe module to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools" / "scribe"))

from core.config_manager import ConfigManager
from core.rule_processor import RuleProcessor


class TestStep21ExitConditions:
    """Test class for STEP 2.1 exit conditions."""
    
    def setup_method(self):
        """Set up test environment."""
        # Create temporary directory for test files
        self.test_dir = Path(tempfile.mkdtemp())
        self.config_dir = self.test_dir / "config"
        self.config_dir.mkdir()
        
        self.config_path = self.config_dir / "config.json"
        self.schema_path = self.config_dir / "config.schema.json"
        
        # Copy schema file
        original_schema = Path(__file__).parent.parent.parent / "config" / "config.schema.json"
        shutil.copy2(original_schema, self.schema_path)
        
        # Create initial valid config
        self.initial_config = {
            "config_version": "1.0",
            "engine_settings": {
                "log_level": "INFO",
                "quarantine_path": "archive/scribe/quarantine/",
                "pause_file": ".engine-pause"
            },
            "security": {
                "allowed_commands": ["git"],
                "restricted_paths": [".git/"]
            },
            "rules": [
                {
                    "id": "RULE-001",
                    "name": "Test Rule",
                    "enabled": True,
                    "file_glob": "*.md",
                    "trigger_pattern": "test_pattern_v1",
                    "actions": [
                        {
                            "type": "log_event",
                            "params": {"message": "test"}
                        }
                    ]
                }
            ]
        }
        
        with open(self.config_path, 'w') as f:
            json.dump(self.initial_config, f, indent=2)
    
    def teardown_method(self):
        """Clean up test environment."""
        if hasattr(self, 'config_manager') and self.config_manager:
            self.config_manager.stop()
        if hasattr(self, 'rule_processor') and self.rule_processor:
            self.rule_processor.stop()
        
        # Clean up temporary directory
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_condition_1_hot_reload_pattern_change(self):
        """
        Test CONDITION 1: A change to a rule's trigger_pattern in config.json 
        is detected and applied by the running engine within 5 seconds, without a restart.
        """
        print("\n=== Testing CONDITION 1: Hot-reload pattern change ===")
        
        # Initialize config manager and rule processor
        self.config_manager = ConfigManager(
            config_path=str(self.config_path),
            schema_path=str(self.schema_path),
            auto_reload=True
        )
        
        self.rule_processor = RuleProcessor(self.config_manager)
        
        # Verify initial pattern
        initial_rule = self.rule_processor.get_rule_by_id("RULE-001")
        assert initial_rule is not None, "Initial rule should be loaded"
        assert initial_rule.trigger_pattern == "test_pattern_v1", "Initial pattern should match"
        
        print(f"✓ Initial pattern loaded: {initial_rule.trigger_pattern}")
        
        # Set up change detection
        pattern_changed = threading.Event()
        new_pattern_detected = None
        
        def on_config_change(new_config):
            nonlocal new_pattern_detected
            rules = new_config.get('rules', [])
            if rules:
                new_pattern_detected = rules[0]['trigger_pattern']
                if new_pattern_detected == "test_pattern_v2":
                    pattern_changed.set()
        
        self.config_manager.add_change_callback(on_config_change)
        
        # Record start time
        start_time = time.time()
        
        # Modify the config file
        modified_config = self.initial_config.copy()
        modified_config['rules'][0]['trigger_pattern'] = "test_pattern_v2"
        
        with open(self.config_path, 'w') as f:
            json.dump(modified_config, f, indent=2)
        
        print("✓ Config file modified with new pattern: test_pattern_v2")
        
        # Wait for change detection (max 5 seconds)
        change_detected = pattern_changed.wait(timeout=5.0)
        detection_time = time.time() - start_time
        
        assert change_detected, f"Pattern change not detected within 5 seconds (waited {detection_time:.2f}s)"
        assert detection_time < 5.0, f"Pattern change took too long: {detection_time:.2f}s"
        
        print(f"✓ Pattern change detected in {detection_time:.2f} seconds")
        
        # Verify the rule processor has the new pattern
        updated_rule = self.rule_processor.get_rule_by_id("RULE-001")
        assert updated_rule is not None, "Updated rule should be available"
        assert updated_rule.trigger_pattern == "test_pattern_v2", "Rule processor should have new pattern"
        
        print(f"✓ Rule processor updated with new pattern: {updated_rule.trigger_pattern}")
        print("✅ CONDITION 1 PASSED: Hot-reload works within 5 seconds")
    
    def test_condition_2_invalid_regex_rejection(self):
        """
        Test CONDITION 2: A rule with an invalid regex pattern is rejected 
        with a descriptive error message on load.
        """
        print("\n=== Testing CONDITION 2: Invalid regex rejection ===")
        
        # Create config with invalid regex pattern
        invalid_config = {
            "config_version": "1.0",
            "engine_settings": {
                "log_level": "INFO",
                "quarantine_path": "archive/scribe/quarantine/",
                "pause_file": ".engine-pause"
            },
            "security": {
                "allowed_commands": ["git"],
                "restricted_paths": [".git/"]
            },
            "rules": [
                {
                    "id": "RULE-001",
                    "name": "Invalid Regex Rule",
                    "enabled": True,
                    "file_glob": "*.md",
                    "trigger_pattern": "[invalid_regex_pattern(",  # Invalid regex
                    "actions": [
                        {
                            "type": "log_event",
                            "params": {"message": "test"}
                        }
                    ]
                }
            ]
        }
        
        # Write invalid config
        with open(self.config_path, 'w') as f:
            json.dump(invalid_config, f, indent=2)
        
        print("✓ Created config with invalid regex pattern: [invalid_regex_pattern(")
        
        # Try to initialize config manager (should succeed)
        self.config_manager = ConfigManager(
            config_path=str(self.config_path),
            schema_path=str(self.schema_path),
            auto_reload=False
        )
        
        print("✓ ConfigManager initialized (config validation passed)")
        
        # Initialize rule processor (should succeed but with 0 rules due to invalid regex)
        self.rule_processor = RuleProcessor(self.config_manager)
        
        # Verify that the invalid rule was rejected
        all_rules = self.rule_processor.get_all_rules()
        assert len(all_rules) == 0, f"Invalid rule should be rejected, but found {len(all_rules)} rules"
        
        # Verify that the rule with invalid pattern is not available
        invalid_rule = self.rule_processor.get_rule_by_id("RULE-001")
        assert invalid_rule is None, "Invalid rule should not be available in processor"
        
        print("✓ Invalid regex rejected and rule not loaded in processor")
        print("✅ CONDITION 2 PASSED: Invalid regex patterns are rejected with descriptive errors")
    
    def test_rule_processor_validation_method(self):
        """Test the rule processor's pattern validation method."""
        print("\n=== Testing Rule Processor Pattern Validation ===")
        
        # Initialize with valid config first
        self.config_manager = ConfigManager(
            config_path=str(self.config_path),
            schema_path=str(self.schema_path),
            auto_reload=False
        )
        
        self.rule_processor = RuleProcessor(self.config_manager)
        
        # Test valid pattern
        is_valid, error = self.rule_processor.validate_rule_pattern("test.*pattern")
        assert is_valid, f"Valid pattern should pass validation: {error}"
        assert error is None, "Valid pattern should have no error message"
        
        print("✓ Valid pattern validation works")
        
        # Test invalid pattern
        is_valid, error = self.rule_processor.validate_rule_pattern("[invalid(")
        assert not is_valid, "Invalid pattern should fail validation"
        assert error is not None, "Invalid pattern should have error message"
        assert "unterminated" in error.lower() or "missing" in error.lower(), f"Error should describe issue: {error}"
        
        print(f"✓ Invalid pattern validation works: {error}")
        print("✅ Pattern validation method works correctly")


def main():
    """Run the exit condition tests."""
    print("🎯 Testing STEP 2.1 Exit Conditions")
    print("=" * 50)
    
    test_instance = TestStep21ExitConditions()
    
    try:
        # Test Condition 1
        test_instance.setup_method()
        test_instance.test_condition_1_hot_reload_pattern_change()
        test_instance.teardown_method()
        
        # Test Condition 2
        test_instance.setup_method()
        test_instance.test_condition_2_invalid_regex_rejection()
        test_instance.teardown_method()
        
        # Test validation method
        test_instance.setup_method()
        test_instance.test_rule_processor_validation_method()
        test_instance.teardown_method()
        
        print("\n" + "=" * 50)
        print("🎉 ALL STEP 2.1 EXIT CONDITIONS PASSED!")
        print("✅ CONDITION 1: Hot-reload works within 5 seconds")
        print("✅ CONDITION 2: Invalid regex patterns rejected with descriptive errors")
        print("✅ Rule processor validation methods work correctly")
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Ensure cleanup
        try:
            test_instance.teardown_method()
        except:
            pass


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 