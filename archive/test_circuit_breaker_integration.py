#!/usr/bin/env python3
"""
Test Circuit Breaker Integration in ActionDispatcher

Verifies that the circuit breaker is properly integrated and functioning
within the ActionDispatcher.
"""

import sys
import time
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch

# Add the scribe directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools" / "scribe"))

from core.action_dispatcher import ActionDispatcher, DispatchResult
from core.plugin_loader import PluginLoader
from core.rule_processor import RuleMatch, CompiledRule
from core.circuit_breaker import CircuitBreakerError
from actions.base import BaseAction, ActionExecutionError
import re


class FailingTestAction(BaseAction):
    """Test action that always fails."""
    
    def __init__(self):
        super().__init__("failing_test_action")
    
    def execute(self, file_content: str, match: re.Match, file_path: str, params: dict) -> str:
        raise ActionExecutionError("failing_test_action", "This action always fails")


class SuccessTestAction(BaseAction):
    """Test action that always succeeds."""
    
    def __init__(self):
        super().__init__("success_test_action")
    
    def execute(self, file_content: str, match: re.Match, file_path: str, params: dict) -> str:
        return file_content + "\n# Modified by test action"


def test_circuit_breaker_integration():
    """Test that circuit breaker properly integrates with ActionDispatcher."""
    print("🧪 Testing Circuit Breaker Integration...")
    
    # Create mock plugin loader that will cause system-level failures
    plugin_loader = Mock(spec=PluginLoader)
    
    # Create test actions
    success_action = SuccessTestAction()
    
    # Mock plugin loader methods to simulate system failures
    def failing_plugin_loader(action_type):
        if action_type == 'system_failing_action':
            raise Exception("System-level plugin loading failure")
        elif action_type == 'success_test_action':
            return success_action
        return None
    
    plugin_loader.create_action_instance.side_effect = failing_plugin_loader
    plugin_loader.get_all_plugins.return_value = {
        'system_failing_action': Mock(),
        'success_test_action': Mock()
    }
    
    # Create ActionDispatcher
    dispatcher = ActionDispatcher(plugin_loader)
    
    # Create a mock rule that will cause system failures
    mock_rule = Mock()
    mock_rule.id = "TEST-RULE-001"
    mock_rule.actions = [
        {'type': 'system_failing_action', 'params': {}}
    ]
    mock_rule.error_handling = {
        'circuit_breaker': {
            'failure_threshold': 2,  # Low threshold for testing
            'recovery_timeout_seconds': 1,
            'success_threshold': 1
        }
    }
    
    # Create rule match
    rule_match = Mock(spec=RuleMatch)
    rule_match.rule = mock_rule
    rule_match.file_path = "/test/file.txt"
    rule_match.file_content = "test content"
    rule_match.match = re.match(r"test", "test content")
    
    print("  ✓ Test setup complete")
    
    # Test 1: First system failure should be caught by circuit breaker
    print("  🔬 Test 1: First system failure (circuit should remain closed)")
    result1 = dispatcher.dispatch_actions(rule_match)
    # System failure results in dispatch result with synthetic failure
    assert not result1.success, "First dispatch should fail due to system failure"
    assert len(result1.action_results) == 1, "Should have 1 synthetic failure result"
    assert result1.action_results[0].action_type == "system_error", "Should be a system error"
    assert not result1.action_results[0].success, "System error should be marked as failure"
    
    # Get circuit breaker stats
    cb_stats = dispatcher.get_circuit_breaker_stats()
    assert "TEST-RULE-001" in cb_stats['breaker_stats'], "Circuit breaker should exist for rule"
    breaker_stats = cb_stats['breaker_stats']['TEST-RULE-001']
    assert breaker_stats['state'] == 'closed', "Circuit should still be closed after first failure"
    assert breaker_stats['failure_count'] == 1, "Should have 1 failure recorded"
    print("    ✓ Circuit breaker recorded first system failure, state: CLOSED")
    
    # Test 2: Second system failure should open the circuit
    print("  🔬 Test 2: Second system failure (circuit should open)")
    result2 = dispatcher.dispatch_actions(rule_match)
    assert not result2.success, "Second dispatch should fail due to system failure"
    
    # Check circuit breaker state
    cb_stats = dispatcher.get_circuit_breaker_stats()
    breaker_stats = cb_stats['breaker_stats']['TEST-RULE-001']
    assert breaker_stats['state'] == 'open', "Circuit should be open after threshold failures"
    assert breaker_stats['failure_count'] == 2, "Should have 2 failures recorded"
    print("    ✓ Circuit breaker opened after threshold system failures")
    
    # Test 3: Third attempt should be blocked by circuit breaker
    print("  🔬 Test 3: Third attempt (should be blocked by circuit breaker)")
    result3 = dispatcher.dispatch_actions(rule_match)
    assert not result3.success, "Third dispatch should fail due to circuit breaker"
    assert len(result3.action_results) == 1, "Should have 1 circuit breaker failure result"
    assert result3.action_results[0].action_type == "circuit_breaker", "Should be a circuit breaker error"
    assert not result3.action_results[0].success, "Circuit breaker error should be marked as failure"
    
    # Check statistics
    stats = dispatcher.get_execution_stats()
    assert stats['circuit_breaker_blocks'] >= 1, "Should have at least 1 circuit breaker block"
    print("    ✓ Circuit breaker blocked execution, no actions executed")
    
    # Test 4: Wait for recovery timeout and test with success action
    print("  🔬 Test 4: Recovery after timeout with success action")
    time.sleep(1.1)  # Wait for recovery timeout
    
    # Change rule to use success action
    mock_rule.actions = [
        {'type': 'success_test_action', 'params': {}}
    ]
    
    result4 = dispatcher.dispatch_actions(rule_match)
    assert result4.success, "Dispatch should succeed with success action after recovery"
    
    # Check circuit breaker state
    cb_stats = dispatcher.get_circuit_breaker_stats()
    breaker_stats = cb_stats['breaker_stats']['TEST-RULE-001']
    assert breaker_stats['state'] == 'closed', "Circuit should be closed after successful recovery"
    print("    ✓ Circuit breaker recovered and closed after successful execution")
    
    print("  ✅ All circuit breaker integration tests passed!")
    return True


def test_action_failure_vs_system_failure():
    """Test that action failures don't trigger circuit breaker, but system failures do."""
    print("🧪 Testing Action Failure vs System Failure...")
    
    # Create mock plugin loader
    plugin_loader = Mock(spec=PluginLoader)
    
    # Create test actions
    failing_action = FailingTestAction()
    
    plugin_loader.create_action_instance.side_effect = lambda action_type: {
        'failing_test_action': failing_action
    }.get(action_type)
    
    plugin_loader.get_all_plugins.return_value = {
        'failing_test_action': Mock()
    }
    
    # Create ActionDispatcher
    dispatcher = ActionDispatcher(plugin_loader)
    
    # Create a mock rule with failing action
    mock_rule = Mock()
    mock_rule.id = "TEST-RULE-002"
    mock_rule.actions = [
        {'type': 'failing_test_action', 'params': {}}
    ]
    mock_rule.error_handling = {
        'circuit_breaker': {
            'failure_threshold': 2,
            'recovery_timeout_seconds': 1,
            'success_threshold': 1
        }
    }
    
    # Create rule match
    rule_match = Mock(spec=RuleMatch)
    rule_match.rule = mock_rule
    rule_match.file_path = "/test/file.txt"
    rule_match.file_content = "test content"
    rule_match.match = re.match(r"test", "test content")
    
    print("  ✓ Test setup complete")
    
    # Test: Multiple action failures should NOT trigger circuit breaker
    print("  🔬 Test: Action failures should not trigger circuit breaker")
    
    for i in range(5):  # Try multiple times
        result = dispatcher.dispatch_actions(rule_match)
        assert not result.success, f"Dispatch {i+1} should fail due to action failure"
        assert result.failed_actions == 1, f"Dispatch {i+1} should have 1 failed action"
        
        # Circuit breaker should remain closed and have 0 failures
        cb_stats = dispatcher.get_circuit_breaker_stats()
        breaker_stats = cb_stats['breaker_stats']['TEST-RULE-002']
        assert breaker_stats['state'] == 'closed', f"Circuit should remain closed after action failure {i+1}"
        assert breaker_stats['failure_count'] == 0, f"Circuit breaker should have 0 failures after action failure {i+1}"
    
    print("    ✓ Action failures correctly ignored by circuit breaker")
    print("  ✅ Action failure vs system failure test passed!")
    return True


def test_circuit_breaker_config_extraction():
    """Test that circuit breaker configuration is properly extracted from rules."""
    print("🧪 Testing Circuit Breaker Configuration Extraction...")
    
    # Create mock plugin loader
    plugin_loader = Mock(spec=PluginLoader)
    dispatcher = ActionDispatcher(plugin_loader)
    
    # Test 1: Rule with custom circuit breaker config
    mock_rule_custom = Mock()
    mock_rule_custom.error_handling = {
        'circuit_breaker': {
            'failure_threshold': 10,
            'recovery_timeout_seconds': 120,
            'success_threshold': 5
        }
    }
    
    config = dispatcher._get_circuit_breaker_config(mock_rule_custom)
    assert config['failure_threshold'] == 10, "Should use custom failure threshold"
    assert config['recovery_timeout_seconds'] == 120, "Should use custom recovery timeout"
    assert config['success_threshold'] == 5, "Should use custom success threshold"
    print("  ✓ Custom circuit breaker configuration extracted correctly")
    
    # Test 2: Rule with no circuit breaker config (should use defaults)
    mock_rule_default = Mock()
    mock_rule_default.error_handling = None
    
    config = dispatcher._get_circuit_breaker_config(mock_rule_default)
    assert config['failure_threshold'] == 5, "Should use default failure threshold"
    assert config['recovery_timeout_seconds'] == 60, "Should use default recovery timeout"
    assert config['success_threshold'] == 3, "Should use default success threshold"
    print("  ✓ Default circuit breaker configuration used when none specified")
    
    # Test 3: Rule with partial circuit breaker config
    mock_rule_partial = Mock()
    mock_rule_partial.error_handling = {
        'circuit_breaker': {
            'failure_threshold': 7  # Only specify one parameter
        }
    }
    
    config = dispatcher._get_circuit_breaker_config(mock_rule_partial)
    assert config['failure_threshold'] == 7, "Should use custom failure threshold"
    assert config['recovery_timeout_seconds'] == 60, "Should use default recovery timeout"
    assert config['success_threshold'] == 3, "Should use default success threshold"
    print("  ✓ Partial circuit breaker configuration merged with defaults correctly")
    
    print("  ✅ All configuration extraction tests passed!")
    return True


def main():
    """Run all circuit breaker integration tests."""
    print("🎯 Starting Circuit Breaker Integration Tests")
    print("=" * 60)
    
    try:
        # Run tests
        test_circuit_breaker_config_extraction()
        print()
        test_action_failure_vs_system_failure()
        print()
        test_circuit_breaker_integration()
        
        print()
        print("🎉 ALL CIRCUIT BREAKER INTEGRATION TESTS PASSED!")
        print("✅ ACTION 2.2.3.2 - Circuit breaker successfully integrated into ActionDispatcher")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 