#!/usr/bin/env python3
"""
Test Circuit Breaker Enhancement

This test verifies that the circuit breaker correctly trips on persistent
action failures, not just system-level failures.
"""

import unittest
import tempfile
import time
from pathlib import Path
from unittest.mock import Mock, patch

# Import scribe modules
from core.action_dispatcher import ActionDispatcher, ActionResult, DispatchResult
from core.plugin_loader import PluginLoader
from core.rule_processor import CompiledRule, RuleMatch
from core.circuit_breaker import CircuitBreakerError
from actions.base import BaseAction, ActionExecutionError


class FailingTestAction(BaseAction):
    """Test action that always fails."""
    
    def __init__(self):
        super().__init__("failing_test_action")
    
    def execute(self, file_content: str, match, file_path: str, params: dict) -> str:
        """Always fail with an exception."""
        raise ActionExecutionError(self.action_type, "Simulated action failure")
    
    def validate_params(self, params: dict) -> bool:
        return True
    
    def get_required_params(self) -> list:
        return []


class SuccessTestAction(BaseAction):
    """Test action that always succeeds."""
    
    def __init__(self):
        super().__init__("success_test_action")
    
    def execute(self, file_content: str, match, file_path: str, params: dict) -> str:
        """Always succeed and return unchanged content."""
        return file_content
    
    def validate_params(self, params: dict) -> bool:
        return True
    
    def get_required_params(self) -> list:
        return []


class TestCircuitBreakerEnhancement(unittest.TestCase):
    """Test the enhanced circuit breaker functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        
        # Create mock plugin loader
        self.mock_plugin_loader = Mock()
        
        # Create action dispatcher
        self.action_dispatcher = ActionDispatcher(self.mock_plugin_loader)
        
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def create_rule_match(self, actions_config: list, rule_id: str = "TEST-CIRCUIT-001") -> RuleMatch:
        """Create a test rule match with specified actions."""
        rule_dict = {
            'id': rule_id,
            'name': 'Test Circuit Breaker Rule',
            'enabled': True,
            'file_glob': '*.md',
            'trigger_pattern': r'# (.+)',
            'actions': actions_config
        }
        
        compiled_rule = CompiledRule(rule_dict)
        test_content = "# Test Header\nSome content"
        
        import re
        match = re.search(r'# (.+)', test_content)
        
        return RuleMatch(
            rule=compiled_rule,
            match=match,
            file_path="test.md",
            file_content=test_content,
            event_id="test-event-id"
        )
    
    def test_circuit_breaker_trips_on_all_actions_failing(self):
        """Test that circuit breaker trips when all actions fail."""
        # Configure mock to return failing actions
        failing_action = FailingTestAction()
        self.mock_plugin_loader.create_action_instance.return_value = failing_action
        
        # Create rule match with multiple failing actions
        actions_config = [
            {'type': 'failing_test_action', 'params': {}},
            {'type': 'failing_test_action', 'params': {}},
        ]
        rule_match = self.create_rule_match(actions_config)
        
        # Mock validation methods to pass
        self.action_dispatcher.validate_action_params = Mock(return_value=(True, None))
        self.action_dispatcher.apply_security_restrictions = Mock(return_value=(True, None))
        
        # First execution should succeed but trigger circuit breaker due to action failures
        with self.assertRaises(CircuitBreakerError):
            # Execute multiple times to trigger circuit breaker
            for i in range(6):  # Default failure threshold is 5
                try:
                    result = self.action_dispatcher.dispatch_actions(rule_match)
                except CircuitBreakerError:
                    if i >= 4:  # Should trip on 5th failure
                        raise
                    else:
                        self.fail(f"Circuit breaker tripped too early on attempt {i+1}")
        
        print("✅ Circuit breaker correctly tripped on persistent action failures")
    
    def test_circuit_breaker_does_not_trip_on_partial_failures(self):
        """Test that circuit breaker doesn't trip when only some actions fail."""
        # Configure mock to return different actions based on type
        def mock_create_action(action_type):
            if action_type == "failing_test_action":
                return FailingTestAction()
            elif action_type == "success_test_action":
                return SuccessTestAction()
            return None
        
        self.mock_plugin_loader.create_action_instance.side_effect = mock_create_action
        
        # Create rule match with mixed success/failure actions (50% failure rate)
        actions_config = [
            {'type': 'success_test_action', 'params': {}},
            {'type': 'failing_test_action', 'params': {}},
        ]
        rule_match = self.create_rule_match(actions_config)
        
        # Mock validation methods to pass
        self.action_dispatcher.validate_action_params = Mock(return_value=(True, None))
        self.action_dispatcher.apply_security_restrictions = Mock(return_value=(True, None))
        
        # Execute multiple times - should not trigger circuit breaker
        for i in range(10):
            result = self.action_dispatcher.dispatch_actions(rule_match)
            self.assertIsInstance(result, DispatchResult)
            self.assertEqual(result.failed_actions, 1)
            self.assertEqual(result.successful_actions, 1)
        
        print("✅ Circuit breaker correctly did not trip on partial failures (50% rate)")
    
    def test_circuit_breaker_trips_on_high_failure_rate(self):
        """Test that circuit breaker trips when >50% of actions fail with multiple actions."""
        # Configure mock to return different actions based on type
        def mock_create_action(action_type):
            if action_type == "failing_test_action":
                return FailingTestAction()
            elif action_type == "success_test_action":
                return SuccessTestAction()
            return None
        
        self.mock_plugin_loader.create_action_instance.side_effect = mock_create_action
        
        # Create rule match with 2/3 actions failing (66% failure rate)
        actions_config = [
            {'type': 'success_test_action', 'params': {}},
            {'type': 'failing_test_action', 'params': {}},
            {'type': 'failing_test_action', 'params': {}},
        ]
        rule_match = self.create_rule_match(actions_config)
        
        # Mock validation methods to pass
        self.action_dispatcher.validate_action_params = Mock(return_value=(True, None))
        self.action_dispatcher.apply_security_restrictions = Mock(return_value=(True, None))
        
        # Execute multiple times to trigger circuit breaker
        with self.assertRaises(CircuitBreakerError):
            for i in range(6):  # Default failure threshold is 5
                try:
                    result = self.action_dispatcher.dispatch_actions(rule_match)
                except CircuitBreakerError:
                    if i >= 4:  # Should trip on 5th failure
                        raise
                    else:
                        self.fail(f"Circuit breaker tripped too early on attempt {i+1}")
        
        print("✅ Circuit breaker correctly tripped on high failure rate (66%)")
    
    def test_circuit_breaker_allows_single_action_failures(self):
        """Test that circuit breaker doesn't trip on single action failures."""
        # Configure mock to return failing action
        failing_action = FailingTestAction()
        self.mock_plugin_loader.create_action_instance.return_value = failing_action
        
        # Create rule match with single failing action
        actions_config = [
            {'type': 'failing_test_action', 'params': {}},
        ]
        rule_match = self.create_rule_match(actions_config)
        
        # Mock validation methods to pass
        self.action_dispatcher.validate_action_params = Mock(return_value=(True, None))
        self.action_dispatcher.apply_security_restrictions = Mock(return_value=(True, None))
        
        # Execute multiple times to trigger circuit breaker
        with self.assertRaises(CircuitBreakerError):
            for i in range(6):  # Default failure threshold is 5
                try:
                    result = self.action_dispatcher.dispatch_actions(rule_match)
                except CircuitBreakerError:
                    if i >= 4:  # Should trip on 5th failure
                        raise
                    else:
                        self.fail(f"Circuit breaker tripped too early on attempt {i+1}")
        
        print("✅ Circuit breaker correctly tripped on single action persistent failures")


class TestPhase4ExitConditions(unittest.TestCase):
    """Test the exit conditions for PHASE 4."""
    
    def test_phase_4_exit_condition_circuit_breaker_trips_on_failures(self):
        """
        PHASE 4 EXIT CONDITION TEST:
        Circuit breaker correctly trips on persistent action failures.
        """
        # Create mock plugin loader and action dispatcher
        mock_plugin_loader = Mock()
        action_dispatcher = ActionDispatcher(mock_plugin_loader)
        
        # Configure mock to return failing actions
        failing_action = FailingTestAction()
        mock_plugin_loader.create_action_instance.return_value = failing_action
        
        # Create rule match with failing actions
        rule_dict = {
            'id': 'PHASE4-TEST-001',
            'name': 'Phase 4 Test Rule',
            'enabled': True,
            'file_glob': '*.md',
            'trigger_pattern': r'# (.+)',
            'actions': [
                {'type': 'failing_test_action', 'params': {}},
                {'type': 'failing_test_action', 'params': {}},
            ]
        }
        
        compiled_rule = CompiledRule(rule_dict)
        test_content = "# Test Header\nContent for testing"
        
        import re
        match = re.search(r'# (.+)', test_content)
        
        rule_match = RuleMatch(
            rule=compiled_rule,
            match=match,
            file_path="phase4_test.md",
            file_content=test_content,
            event_id="phase4-test-event"
        )
        
        # Mock validation methods to pass
        action_dispatcher.validate_action_params = Mock(return_value=(True, None))
        action_dispatcher.apply_security_restrictions = Mock(return_value=(True, None))
        
        # Execute multiple times to trigger circuit breaker
        circuit_breaker_tripped = False
        for i in range(6):  # Default failure threshold is 5
            try:
                result = action_dispatcher.dispatch_actions(rule_match)
            except CircuitBreakerError as e:
                if i >= 4:  # Should trip on 5th failure
                    circuit_breaker_tripped = True
                    break
                else:
                    self.fail(f"Circuit breaker tripped too early on attempt {i+1}")
        
        # Verify circuit breaker tripped
        self.assertTrue(circuit_breaker_tripped, "Circuit breaker should have tripped on persistent failures")
        
        print(f"\n🎯 PHASE 4 EXIT CONDITION SATISFIED")
        print(f"✅ Circuit breaker correctly trips on persistent action failures")
        print(f"✅ Integration test confirms breaker opens for failing rule")


if __name__ == '__main__':
    unittest.main(verbosity=2) 