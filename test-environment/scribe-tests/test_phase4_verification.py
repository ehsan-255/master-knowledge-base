#!/usr/bin/env python3
"""
PHASE 4 Exit Condition Verification

Simple test to verify that the circuit breaker correctly trips on persistent action failures.
"""

import unittest
from unittest.mock import Mock

# Import scribe modules
from core.action_dispatcher import ActionDispatcher
from core.plugin_loader import PluginLoader
from core.rule_processor import CompiledRule, RuleMatch
from core.circuit_breaker import CircuitBreakerError
from actions.base import BaseAction, ActionExecutionError


class AlwaysFailingAction(BaseAction):
    """Test action that always fails."""
    
    def __init__(self):
        super().__init__("always_failing_action")
    
    def execute(self, file_content: str, match, file_path: str, params: dict) -> str:
        """Always fail with an exception."""
        raise ActionExecutionError(self.action_type, "This action always fails")
    
    def validate_params(self, params: dict) -> bool:
        return True
    
    def get_required_params(self) -> list:
        return []


class TestPhase4ExitCondition(unittest.TestCase):
    """Test PHASE 4 exit condition: Circuit breaker trips on persistent action failures."""
    
    def test_phase_4_exit_condition_satisfied(self):
        """
        PHASE 4 EXIT CONDITION TEST:
        Circuit breaker correctly trips on persistent action failures.
        """
        print("\n🎯 TESTING PHASE 4 EXIT CONDITION")
        print("=" * 50)
        
        # Create mock plugin loader and action dispatcher
        mock_plugin_loader = Mock()
        action_dispatcher = ActionDispatcher(mock_plugin_loader)
        
        # Configure mock to return always-failing actions
        failing_action = AlwaysFailingAction()
        mock_plugin_loader.create_action_instance.return_value = failing_action
        
        # Create rule match with failing actions (100% failure rate)
        rule_dict = {
            'id': 'PHASE4-EXIT-TEST',
            'name': 'Phase 4 Exit Condition Test',
            'enabled': True,
            'file_glob': '*.md',
            'trigger_pattern': r'# (.+)',
            'actions': [
                {'type': 'always_failing_action', 'params': {}},
                {'type': 'always_failing_action', 'params': {}},
            ]
        }
        
        compiled_rule = CompiledRule(rule_dict)
        test_content = "# Test Header\nContent for PHASE 4 testing"
        
        import re
        match = re.search(r'# (.+)', test_content)
        
        rule_match = RuleMatch(
            rule=compiled_rule,
            match=match,
            file_path="phase4_exit_test.md",
            file_content=test_content,
            event_id="phase4-exit-test-event"
        )
        
        # Mock validation methods to pass
        action_dispatcher.validate_action_params = Mock(return_value=(True, None))
        action_dispatcher.apply_security_restrictions = Mock(return_value=(True, None))
        
        # Execute multiple times to trigger circuit breaker
        circuit_breaker_opened = False
        action_chain_failures = 0
        
        print("📋 Executing failing action chains to trigger circuit breaker...")
        
        for attempt in range(1, 8):  # Try up to 7 attempts
            try:
                print(f"  Attempt {attempt}: ", end="")
                result = action_dispatcher.dispatch_actions(rule_match)
                
                # Check if this was an action chain failure (should trigger circuit breaker)
                if result.failed_actions == result.total_actions and result.total_actions > 0:
                    action_chain_failures += 1
                    print(f"Action chain failed ({result.failed_actions}/{result.total_actions} actions failed)")
                else:
                    print(f"Partial failure ({result.failed_actions}/{result.total_actions} actions failed)")
                
                # Check if circuit breaker has opened
                cb_stats = action_dispatcher.get_circuit_breaker_stats()
                if cb_stats and cb_stats.get('open_breakers', 0) > 0:
                    print(f"Circuit breaker OPENED! (after {action_chain_failures} action chain failures)")
                    circuit_breaker_opened = True
                    break
                
            except CircuitBreakerError as e:
                print(f"Circuit breaker OPENED via exception! (after {action_chain_failures} action chain failures)")
                circuit_breaker_opened = True
                break
            except Exception as e:
                print(f"Unexpected error: {e}")
                break
        
        # Verify circuit breaker behavior
        print(f"\n📊 RESULTS:")
        print(f"  Action chain failures before circuit opened: {action_chain_failures}")
        print(f"  Circuit breaker opened: {circuit_breaker_opened}")
        
        # Check circuit breaker stats
        cb_stats = action_dispatcher.get_circuit_breaker_stats()
        print(f"  Circuit breaker stats: {cb_stats}")
        
        # PHASE 4 EXIT CONDITION: Circuit breaker should trip on persistent action failures
        if circuit_breaker_opened:
            print(f"\n✅ PHASE 4 EXIT CONDITION SATISFIED!")
            print(f"✅ Circuit breaker correctly tripped on persistent action failures")
            print(f"✅ Action chain failures triggered circuit breaker protection")
        else:
            print(f"\n❌ PHASE 4 EXIT CONDITION NOT SATISFIED")
            print(f"❌ Circuit breaker did not trip on persistent action failures")
        
        # Assert the exit condition
        self.assertTrue(circuit_breaker_opened, 
                       "PHASE 4 EXIT CONDITION: Circuit breaker must trip on persistent action failures")
        
        # Verify that action chain failures were detected
        self.assertGreater(action_chain_failures, 0, 
                          "Action chain failures should have been detected")
        
        print(f"\n🎯 PHASE 4 IMPLEMENTATION VERIFIED SUCCESSFULLY!")


if __name__ == '__main__':
    unittest.main(verbosity=2) 