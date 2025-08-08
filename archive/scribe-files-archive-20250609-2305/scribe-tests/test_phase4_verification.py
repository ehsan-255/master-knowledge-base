#!/usr/bin/env python3
"""
Phase 4 Verification Test: Circuit Breaker Action Chain Failure Handling

This test verifies that the circuit breaker correctly opens when a rule
has actions that consistently fail, triggering ActionChainFailedError.
"""

import tempfile
import threading
import time
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the scribe directory to path for imports
import sys
import os
scribe_path = Path(__file__).parent.parent.parent / "tools" / "scribe"
sys.path.insert(0, str(scribe_path))

from core.action_dispatcher import ActionDispatcher, ActionChainFailedError
from core.plugin_loader import PluginLoader
from core.rule_processor import RuleProcessor, RuleMatch
from core.config_manager import ConfigManager
from core.circuit_breaker import CircuitBreakerManager, CircuitState
from actions.base import BaseAction, ActionExecutionError


class AlwaysFailAction(BaseAction):
    """Test action that always fails to trigger circuit breaker."""
    
    def get_required_params(self):
        return ["failure_message"]
    
    def validate_params(self, params):
        return "failure_message" in params
    
    def execute(self, file_content, match, file_path, params, event_id=None):
        # Always fail with the specified message
        raise ActionExecutionError("always_fail", params.get("failure_message", "Intentional test failure"))


def test_circuit_breaker_action_chain_failure():
    """Test that circuit breaker opens on persistent action chain failures."""
    
    print("=== Phase 4 Verification Test: Circuit Breaker Action Chain Failure ===")
    
    # Create temporary directory and test file
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = Path(temp_dir) / "test.md"
        test_file.write_text("# Test Document\nContent here")
        
        # Create test configuration with a rule that has a failing action
        config_data = {
            "config_version": "1.0",
            "engine_settings": {
                "log_level": "INFO",
                "quarantine_path": "archive/scribe/quarantine/",
                "pause_file": ".engine-pause"
            },
            "security": {
                "allowed_commands": [],
                "restricted_paths": []
            },
            "rules": [
                {
                    "id": "RULE-001",
                    "name": "Test Failing Rule",
                    "enabled": True,
                    "file_glob": "*.md",
                    "trigger_pattern": r"# Test Document",
                    "actions": [
                        {
                            "type": "always_fail",
                            "params": {
                                "failure_message": "This action always fails for testing"
                            }
                        }
                    ],
                    "error_handling": {
                        "circuit_breaker": {
                            "failure_threshold": 3,
                            "recovery_timeout_seconds": 30
                        }
                    }
                }
            ]
        }
        
        config_file = Path(temp_dir) / "config.json"
        config_file.write_text(json.dumps(config_data, indent=2))
        
        # Initialize components
        config_manager = ConfigManager(config_path=str(config_file))
        plugin_loader = PluginLoader()
        
        # Manually register the failing action
        plugin_loader._action_plugins = {
            "always_fail": type("AlwaysFailPlugin", (), {
                "name": "always_fail",
                "description": "Test action that always fails",
                "create_action": lambda: AlwaysFailAction()
            })()
        }
        
        action_dispatcher = ActionDispatcher(plugin_loader)
        rule_processor = RuleProcessor(config_manager)
        
        # Get the compiled rules from rule processor
        compiled_rules = rule_processor.get_all_rules()
        test_rule = compiled_rules[0]
        
        # Create circuit breaker manager and get the breaker for this rule
        circuit_breaker_manager = action_dispatcher.circuit_breaker_manager
        rule_breaker = circuit_breaker_manager.get_breaker(test_rule.id)
        
        print(f"Initial circuit breaker state: {rule_breaker.state}")
        print(f"Circuit breaker failure threshold: {rule_breaker.failure_threshold}")
        
        # Trigger the rule multiple times to exceed failure threshold
        failure_count = 0
        max_attempts = rule_breaker.failure_threshold + 2  # Ensure we exceed threshold
        
        for attempt in range(max_attempts):
            print(f"\n--- Attempt {attempt + 1}/{max_attempts} ---")
            
            try:
                # Process the file which should trigger our failing rule
                rule_matches = rule_processor.process_file(str(test_file), test_file.read_text())
                
                print(f"Found {len(rule_matches)} rule matches")
                
                if rule_matches:
                    # Dispatch actions for the first match
                    rule_match = rule_matches[0]
                    dispatch_result = action_dispatcher.dispatch_actions(rule_match)
                    
                    print(f"Dispatch result success: {dispatch_result.success}")
                    print(f"Failed actions: {dispatch_result.failed_actions}")
                    
                    if not dispatch_result.success:
                        failure_count += 1
                        print(f"Action chain failure #{failure_count}")
                
            except Exception as e:
                print(f"Exception during processing: {e}")
                failure_count += 1
            
            # Check circuit breaker state
            current_state = rule_breaker.state
            current_failures = rule_breaker.failure_count
            
            print(f"Circuit breaker state: {current_state}")
            print(f"Circuit breaker failure count: {current_failures}")
            
            # If circuit breaker is open, we've achieved our goal
            if current_state == CircuitState.OPEN:
                print(f"\n🎉 SUCCESS: Circuit breaker opened after {failure_count} failures!")
                print(f"Final state: {current_state}")
                print(f"Final failure count: {current_failures}")
                return True
            
            time.sleep(0.1)  # Small delay between attempts
        
        # If we get here, the circuit breaker didn't open as expected
        print(f"\n❌ FAILURE: Circuit breaker did not open after {max_attempts} attempts")
        print(f"Final state: {rule_breaker.state}")
        print(f"Final failure count: {rule_breaker.failure_count}")
        print(f"Threshold: {rule_breaker.failure_threshold}")
        
        return False


def test_action_chain_failed_error_creation():
    """Test that ActionChainFailedError is properly instantiated."""
    
    print("\n=== Testing ActionChainFailedError Exception ===")
    
    try:
        # Create the exception with all parameters
        error = ActionChainFailedError(
            "Test action chain failure",
            rule_id="TEST_RULE_123",
            failed_actions=3,
            total_actions=5
        )
        
        print(f"Exception message: {error}")
        print(f"Rule ID: {error.rule_id}")
        print(f"Failed actions: {error.failed_actions}")
        print(f"Total actions: {error.total_actions}")
        
        # Verify it's properly raised and caught
        try:
            raise error
        except ActionChainFailedError as caught_error:
            print(f"Successfully caught ActionChainFailedError: {caught_error}")
            return True
            
    except Exception as e:
        print(f"❌ Error testing ActionChainFailedError: {e}")
        return False


if __name__ == "__main__":
    print("Phase 4 Circuit Breaker Verification Test")
    print("=" * 50)
    
    # Test 1: ActionChainFailedError creation
    test1_success = test_action_chain_failed_error_creation()
    
    # Test 2: Circuit breaker integration
    test2_success = test_circuit_breaker_action_chain_failure()
    
    # Summary
    print("\n" + "=" * 50)
    print("PHASE 4 VERIFICATION RESULTS:")
    print(f"✅ ActionChainFailedError Test: {'PASSED' if test1_success else 'FAILED'}")
    print(f"✅ Circuit Breaker Integration: {'PASSED' if test2_success else 'FAILED'}")
    
    if test1_success and test2_success:
        print("\n🎉 PHASE 4 VERIFICATION: ALL TESTS PASSED")
        print("Circuit breaker correctly opens on persistent action failures!")
    else:
        print("\n❌ PHASE 4 VERIFICATION: SOME TESTS FAILED")
        sys.exit(1) 