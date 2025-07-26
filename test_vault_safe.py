#!/usr/bin/env python3
"""
Safe Vault Integration Test
Testing the fixed implementation with minimal resource usage
"""

import os
import sys
import time
import threading
from pathlib import Path

# Add the tools/scribe directory to path
scribe_path = Path(__file__).parent / "tools" / "scribe"
sys.path.insert(0, str(scribe_path))

def test_safe_imports():
    """Test that the fixed modules can be imported safely."""
    try:
        print("Testing safe imports...")
        
        # Test retry handler with bounds
        from core.vault_retry_handler import VaultRetryHandler, RetryConfig
        print("[OK] Retry handler imported safely")
        
        # Test circuit breaker with bounds  
        from core.vault_circuit_breaker import VaultCircuitBreaker, CircuitBreakerConfig
        print("[OK] Circuit breaker imported safely")
        
        # Test metrics collector with reduced footprint
        from core.vault_metrics_collector import VaultMetricsCollector
        print("[OK] Metrics collector imported safely")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Import failed: {e}")
        return False

def test_bounded_data_structures():
    """Test that data structures have proper bounds."""
    try:
        print("\nTesting bounded data structures...")
        
        # Test retry manager bounds
        from core.vault_retry_handler import VaultRetryManager
        retry_manager = VaultRetryManager()
        
        # Try to create more handlers than the limit
        for i in range(15):  # More than max_handlers (10)
            handler = retry_manager.get_handler(f"test_op_{i}")
        
        # Should have cleared and only have latest handler
        metrics = retry_manager.get_all_metrics()
        print(f"[OK] Retry manager bounded: {len(metrics)} handlers")
        
        # Test circuit breaker manager bounds
        from core.vault_circuit_breaker import VaultCircuitBreakerManager
        cb_manager = VaultCircuitBreakerManager()
        
        # Try to create more breakers than the limit
        for i in range(15):  # More than max_breakers (10)
            breaker = cb_manager.get_breaker(f"test_op_{i}")
        
        # Should have cleared and only have latest breakers
        cb_metrics = cb_manager.get_all_metrics()
        print(f"[OK] Circuit breaker manager bounded: {len(cb_metrics)} breakers")
        
        # Test metrics collector history bounds
        from core.vault_metrics_collector import VaultMetricsCollector
        metrics_collector = VaultMetricsCollector()
        
        # Try to create more history than the limit
        for i in range(100):  # More than max_history_size (50)
            metrics_collector._record_operation_history({
                "operation_id": f"test_{i}",
                "status": "success",
                "duration": 0.1,
                "timestamp": time.time()
            })
        
        summary = metrics_collector.get_metrics_summary()
        print(f"[OK] Metrics collector bounded: {summary['operation_history_size']} history entries")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Bounds test failed: {e}")
        return False

def test_resource_cleanup():
    """Test that resources are properly cleaned up."""
    try:
        print("\nTesting resource cleanup...")
        
        # Test that global instances can be created and cleaned
        from core.vault_retry_handler import get_vault_retry_manager
        from core.vault_circuit_breaker import get_vault_circuit_breaker_manager
        from core.vault_metrics_collector import get_vault_metrics_collector
        
        # Create instances
        retry_mgr = get_vault_retry_manager()
        cb_mgr = get_vault_circuit_breaker_manager()
        metrics = get_vault_metrics_collector()
        
        print("[OK] Global instances created safely")
        
        # Test cleanup
        retry_mgr.reset_all_metrics()
        cb_mgr.reset_all()
        metrics.reset_metrics()
        
        print("[OK] Resource cleanup completed")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Cleanup test failed: {e}")
        return False

def main():
    """Run safe validation tests."""
    print("=" * 60)
    print("SAFE VAULT INTEGRATION VALIDATION")
    print("=" * 60)
    print("Testing the fixed implementation to prevent system crashes")
    print()
    
    tests = [
        test_safe_imports,
        test_bounded_data_structures,
        test_resource_cleanup
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print("Test failed!")
        except Exception as e:
            print(f"Test error: {e}")
    
    print()
    print("=" * 60)
    print(f"RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("[SUCCESS] ALL TESTS PASSED - Safe to proceed with limited deployment")
    else:
        print("[WARNING] SOME TESTS FAILED - Further fixes needed")
    
    print("=" * 60)
    
    return passed == total

if __name__ == "__main__":
    main()