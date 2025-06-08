#!/usr/bin/env python3
"""
Scribe Circuit Breaker

Implements circuit breaker pattern for rule execution to prevent cascading failures.
Tracks failures, manages state transitions, and provides recovery mechanisms.
"""

import time
import threading
from enum import Enum
from typing import Dict, Any, Optional, Callable
import structlog

from .logging_config import get_scribe_logger

logger = get_scribe_logger(__name__)


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, blocking requests
    HALF_OPEN = "half_open"  # Testing recovery


class CircuitBreakerError(Exception):
    """Exception raised when circuit breaker is open."""
    
    def __init__(self, rule_id: str, failure_count: int, last_failure_time: float):
        """
        Initialize the exception.
        
        Args:
            rule_id: ID of the rule with open circuit
            failure_count: Number of failures that triggered the circuit
            last_failure_time: Timestamp of the last failure
        """
        self.rule_id = rule_id
        self.failure_count = failure_count
        self.last_failure_time = last_failure_time
        
        super().__init__(f"Circuit breaker is OPEN for rule '{rule_id}' (failures: {failure_count})")


class CircuitBreaker:
    """
    Circuit breaker implementation for rule execution.
    
    Tracks failures for individual rules and prevents execution when
    failure threshold is exceeded. Provides automatic recovery after timeout.
    """
    
    def __init__(self, 
                 rule_id: str,
                 failure_threshold: int = 5,
                 recovery_timeout_seconds: int = 60,
                 success_threshold: int = 3):
        """
        Initialize circuit breaker for a specific rule.
        
        Args:
            rule_id: ID of the rule this circuit breaker protects
            failure_threshold: Number of failures before opening circuit
            recovery_timeout_seconds: Seconds to wait before attempting recovery
            success_threshold: Number of successes needed to close circuit from half-open
        """
        self.rule_id = rule_id
        self.failure_threshold = failure_threshold
        self.recovery_timeout_seconds = recovery_timeout_seconds
        self.success_threshold = success_threshold
        
        # State management
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._last_failure_time = 0.0
        self._last_success_time = 0.0
        self._state_change_time = time.time()
        
        # Thread safety
        self._lock = threading.RLock()
        
        # Statistics
        self._total_calls = 0
        self._total_failures = 0
        self._total_successes = 0
        self._state_changes = 0
        
        logger.info("CircuitBreaker initialized",
                   rule_id=rule_id,
                   failure_threshold=failure_threshold,
                   recovery_timeout_seconds=recovery_timeout_seconds,
                   success_threshold=success_threshold)
    
    @property
    def state(self) -> CircuitState:
        """Get current circuit state."""
        with self._lock:
            return self._state
    
    @property
    def failure_count(self) -> int:
        """Get current failure count."""
        with self._lock:
            return self._failure_count
    
    @property
    def is_open(self) -> bool:
        """Check if circuit is open (blocking requests)."""
        return self.state == CircuitState.OPEN
    
    @property
    def is_closed(self) -> bool:
        """Check if circuit is closed (normal operation)."""
        return self.state == CircuitState.CLOSED
    
    @property
    def is_half_open(self) -> bool:
        """Check if circuit is half-open (testing recovery)."""
        return self.state == CircuitState.HALF_OPEN
    
    def _change_state(self, new_state: CircuitState, reason: str = "") -> None:
        """
        Change circuit state with logging.
        
        Args:
            new_state: New state to transition to
            reason: Reason for state change
        """
        old_state = self._state
        self._state = new_state
        self._state_change_time = time.time()
        self._state_changes += 1
        
        logger.info("Circuit breaker state changed",
                   rule_id=self.rule_id,
                   old_state=old_state.value,
                   new_state=new_state.value,
                   reason=reason,
                   failure_count=self._failure_count,
                   success_count=self._success_count)
    
    def _should_attempt_reset(self) -> bool:
        """
        Check if enough time has passed to attempt recovery.
        
        Returns:
            True if recovery should be attempted
        """
        if self._state != CircuitState.OPEN:
            return False
        
        time_since_failure = time.time() - self._last_failure_time
        return time_since_failure >= self.recovery_timeout_seconds
    
    def can_execute(self) -> bool:
        """
        Check if execution is allowed based on circuit state.
        
        Returns:
            True if execution is allowed
        """
        with self._lock:
            if self._state == CircuitState.CLOSED:
                return True
            
            elif self._state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    self._change_state(CircuitState.HALF_OPEN, "Recovery timeout elapsed")
                    return True
                return False
            
            elif self._state == CircuitState.HALF_OPEN:
                return True
            
            return False
    
    def record_success(self) -> None:
        """Record a successful execution."""
        with self._lock:
            self._total_calls += 1
            self._total_successes += 1
            self._last_success_time = time.time()
            
            if self._state == CircuitState.CLOSED:
                # Reset failure count on success in closed state
                if self._failure_count > 0:
                    logger.debug("Resetting failure count after success",
                               rule_id=self.rule_id,
                               previous_failures=self._failure_count)
                    self._failure_count = 0
            
            elif self._state == CircuitState.HALF_OPEN:
                self._success_count += 1
                logger.debug("Success in half-open state",
                           rule_id=self.rule_id,
                           success_count=self._success_count,
                           success_threshold=self.success_threshold)
                
                if self._success_count >= self.success_threshold:
                    self._failure_count = 0
                    self._success_count = 0
                    self._change_state(CircuitState.CLOSED, "Success threshold reached")
            
            logger.debug("Success recorded",
                        rule_id=self.rule_id,
                        state=self._state.value,
                        total_successes=self._total_successes)
    
    def record_failure(self, error: Optional[Exception] = None) -> None:
        """
        Record a failed execution.
        
        Args:
            error: The exception that caused the failure
        """
        with self._lock:
            self._total_calls += 1
            self._total_failures += 1
            self._failure_count += 1
            self._last_failure_time = time.time()
            
            error_type = type(error).__name__ if error else "Unknown"
            error_message = str(error) if error else "No error details"
            
            logger.warning("Failure recorded",
                          rule_id=self.rule_id,
                          state=self._state.value,
                          failure_count=self._failure_count,
                          failure_threshold=self.failure_threshold,
                          error_type=error_type,
                          error_message=error_message)
            
            if self._state == CircuitState.CLOSED:
                if self._failure_count >= self.failure_threshold:
                    self._change_state(CircuitState.OPEN, f"Failure threshold exceeded ({self._failure_count}/{self.failure_threshold})")
            
            elif self._state == CircuitState.HALF_OPEN:
                # Any failure in half-open state goes back to open
                self._success_count = 0
                self._change_state(CircuitState.OPEN, "Failure during recovery test")
    
    def execute(self, func: Callable[[], Any]) -> Any:
        """
        Execute a function with circuit breaker protection.
        
        Args:
            func: Function to execute
            
        Returns:
            Result of function execution
            
        Raises:
            CircuitBreakerError: If circuit is open
            Exception: Any exception raised by the function
        """
        if not self.can_execute():
            raise CircuitBreakerError(self.rule_id, self._failure_count, self._last_failure_time)
        
        try:
            result = func()
            self.record_success()
            return result
        except Exception as e:
            self.record_failure(e)
            raise
    
    def force_open(self, reason: str = "Manually opened") -> None:
        """
        Force circuit to open state.
        
        Args:
            reason: Reason for forcing open
        """
        with self._lock:
            self._change_state(CircuitState.OPEN, reason)
    
    def force_close(self, reason: str = "Manually closed") -> None:
        """
        Force circuit to closed state and reset counters.
        
        Args:
            reason: Reason for forcing closed
        """
        with self._lock:
            self._failure_count = 0
            self._success_count = 0
            self._change_state(CircuitState.CLOSED, reason)
    
    def reset(self) -> None:
        """Reset circuit breaker to initial state."""
        with self._lock:
            self._failure_count = 0
            self._success_count = 0
            self._last_failure_time = 0.0
            self._last_success_time = 0.0
            self._change_state(CircuitState.CLOSED, "Circuit breaker reset")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get circuit breaker statistics.
        
        Returns:
            Dictionary with statistics
        """
        with self._lock:
            current_time = time.time()
            
            return {
                'rule_id': self.rule_id,
                'state': self._state.value,
                'failure_count': self._failure_count,
                'success_count': self._success_count,
                'failure_threshold': self.failure_threshold,
                'success_threshold': self.success_threshold,
                'recovery_timeout_seconds': self.recovery_timeout_seconds,
                'total_calls': self._total_calls,
                'total_failures': self._total_failures,
                'total_successes': self._total_successes,
                'state_changes': self._state_changes,
                'last_failure_time': self._last_failure_time,
                'last_success_time': self._last_success_time,
                'state_change_time': self._state_change_time,
                'time_since_last_failure': current_time - self._last_failure_time if self._last_failure_time > 0 else 0,
                'time_since_state_change': current_time - self._state_change_time,
                'can_execute': self.can_execute()
            }
    
    def __str__(self) -> str:
        """String representation of circuit breaker."""
        return f"CircuitBreaker(rule_id='{self.rule_id}', state={self._state.value}, failures={self._failure_count})"
    
    def __repr__(self) -> str:
        """Detailed string representation of circuit breaker."""
        return f"CircuitBreaker(rule_id='{self.rule_id}', state={self._state.value}, failure_count={self._failure_count}, failure_threshold={self.failure_threshold})"


class CircuitBreakerManager:
    """
    Manages circuit breakers for multiple rules.
    
    Provides centralized management of circuit breakers with automatic
    creation and configuration based on rule settings.
    """
    
    def __init__(self):
        """Initialize circuit breaker manager."""
        self._breakers: Dict[str, CircuitBreaker] = {}
        self._lock = threading.RLock()
        
        logger.info("CircuitBreakerManager initialized")
    
    def get_breaker(self, 
                   rule_id: str,
                   failure_threshold: int = 5,
                   recovery_timeout_seconds: int = 60,
                   success_threshold: int = 3) -> CircuitBreaker:
        """
        Get or create a circuit breaker for a rule.
        
        Args:
            rule_id: ID of the rule
            failure_threshold: Number of failures before opening circuit
            recovery_timeout_seconds: Seconds to wait before attempting recovery
            success_threshold: Number of successes needed to close circuit
            
        Returns:
            CircuitBreaker instance for the rule
        """
        with self._lock:
            if rule_id not in self._breakers:
                self._breakers[rule_id] = CircuitBreaker(
                    rule_id=rule_id,
                    failure_threshold=failure_threshold,
                    recovery_timeout_seconds=recovery_timeout_seconds,
                    success_threshold=success_threshold
                )
                logger.debug("Created new circuit breaker",
                           rule_id=rule_id,
                           failure_threshold=failure_threshold,
                           recovery_timeout_seconds=recovery_timeout_seconds)
            
            return self._breakers[rule_id]
    
    def remove_breaker(self, rule_id: str) -> bool:
        """
        Remove a circuit breaker for a rule.
        
        Args:
            rule_id: ID of the rule
            
        Returns:
            True if breaker was removed, False if not found
        """
        with self._lock:
            if rule_id in self._breakers:
                del self._breakers[rule_id]
                logger.debug("Removed circuit breaker", rule_id=rule_id)
                return True
            return False
    
    def get_all_breakers(self) -> Dict[str, CircuitBreaker]:
        """
        Get all circuit breakers.
        
        Returns:
            Dictionary mapping rule IDs to circuit breakers
        """
        with self._lock:
            return self._breakers.copy()
    
    def get_open_breakers(self) -> Dict[str, CircuitBreaker]:
        """
        Get all open circuit breakers.
        
        Returns:
            Dictionary mapping rule IDs to open circuit breakers
        """
        with self._lock:
            return {rule_id: breaker for rule_id, breaker in self._breakers.items() 
                   if breaker.is_open}
    
    def reset_all_breakers(self) -> None:
        """Reset all circuit breakers to closed state."""
        with self._lock:
            for breaker in self._breakers.values():
                breaker.reset()
            logger.info("All circuit breakers reset")
    
    def get_manager_stats(self) -> Dict[str, Any]:
        """
        Get manager statistics.
        
        Returns:
            Dictionary with manager statistics
        """
        with self._lock:
            breaker_stats = {}
            open_count = 0
            half_open_count = 0
            closed_count = 0
            
            for rule_id, breaker in self._breakers.items():
                stats = breaker.get_stats()
                breaker_stats[rule_id] = stats
                
                if breaker.is_open:
                    open_count += 1
                elif breaker.is_half_open:
                    half_open_count += 1
                else:
                    closed_count += 1
            
            return {
                'total_breakers': len(self._breakers),
                'open_breakers': open_count,
                'half_open_breakers': half_open_count,
                'closed_breakers': closed_count,
                'breaker_stats': breaker_stats
            } 