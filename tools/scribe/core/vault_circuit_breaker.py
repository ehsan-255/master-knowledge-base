#!/usr/bin/env python3
"""
Scribe Vault Circuit Breaker

Implements enterprise-grade circuit breaker pattern for Vault operations
to prevent cascading failures and ensure system resilience under fault conditions.
"""

import time
import threading
from enum import Enum
from typing import Callable, Any, Optional, Dict
from dataclasses import dataclass
import structlog

from .logging_config import get_scribe_logger

logger = get_scribe_logger(__name__)


class CircuitState(Enum):
    """Circuit breaker states following Martin Fowler's pattern."""
    CLOSED = "closed"        # Normal operation, requests pass through
    OPEN = "open"           # Circuit is open, requests fail fast
    HALF_OPEN = "half_open" # Testing if service has recovered


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker behavior."""
    failure_threshold: int = 5          # Failures before opening circuit
    recovery_timeout: float = 60.0      # Seconds before trying half-open
    success_threshold: int = 3          # Successes needed to close circuit
    timeout: float = 30.0               # Request timeout in seconds
    expected_exception_types: tuple = (Exception,)  # Exceptions that count as failures


class CircuitBreakerError(Exception):
    """Exception raised when circuit breaker is open."""
    
    def __init__(self, message: str, state: CircuitState, failure_count: int):
        self.state = state
        self.failure_count = failure_count
        super().__init__(message)


class VaultCircuitBreaker:
    """
    Circuit breaker implementation for Vault operations.
    
    Protects against cascading failures by failing fast when Vault
    is experiencing issues, allowing it time to recover.
    """
    
    def __init__(self, config: CircuitBreakerConfig, name: str = "vault_circuit_breaker"):
        """
        Initialize circuit breaker.
        
        Args:
            config: Circuit breaker configuration
            name: Name for logging and identification
        """
        self.config = config
        self.name = name
        
        # Circuit state management
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._last_failure_time = 0.0
        self._next_attempt_time = 0.0
        
        # Thread safety
        self._lock = threading.RLock()
        
        # Metrics for monitoring
        self._total_calls = 0
        self._failed_calls = 0
        self._rejected_calls = 0
        self._state_transitions = {
            CircuitState.CLOSED: 0,
            CircuitState.OPEN: 0,
            CircuitState.HALF_OPEN: 0
        }
        
        logger.info("Circuit breaker initialized",
                   name=self.name,
                   failure_threshold=config.failure_threshold,
                   recovery_timeout=config.recovery_timeout,
                   success_threshold=config.success_threshold)
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function through circuit breaker protection.
        
        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result
            
        Raises:
            CircuitBreakerError: If circuit is open
            Original exception: If function fails
        """
        with self._lock:
            self._total_calls += 1
            
            # Check if we should allow the call
            if not self._should_allow_request():
                self._rejected_calls += 1
                raise CircuitBreakerError(
                    f"Circuit breaker '{self.name}' is {self._state.value}",
                    self._state,
                    self._failure_count
                )
            
            # Execute the function
            try:
                start_time = time.time()
                
                logger.debug("Executing function through circuit breaker",
                           function=func.__name__,
                           state=self._state.value,
                           failure_count=self._failure_count)
                
                result = func(*args, **kwargs)
                
                execution_time = time.time() - start_time
                
                # Record success
                self._on_success(execution_time)
                
                logger.debug("Function executed successfully",
                           function=func.__name__,
                           execution_time=execution_time,
                           state=self._state.value)
                
                return result
                
            except self.config.expected_exception_types as e:
                execution_time = time.time() - start_time
                
                # Record failure
                self._on_failure(e, execution_time)
                
                logger.warning("Function execution failed through circuit breaker",
                             function=func.__name__,
                             error=str(e),
                             execution_time=execution_time,
                             state=self._state.value,
                             failure_count=self._failure_count)
                
                raise  # Re-raise the original exception
    
    def _should_allow_request(self) -> bool:
        """Determine if request should be allowed based on circuit state."""
        current_time = time.time()
        
        if self._state == CircuitState.CLOSED:
            return True
        
        elif self._state == CircuitState.OPEN:
            # Check if enough time has passed to try half-open
            if current_time >= self._next_attempt_time:
                logger.info("Circuit breaker transitioning to half-open",
                           name=self.name,
                           failure_count=self._failure_count)
                self._transition_to_half_open()
                return True
            return False
        
        elif self._state == CircuitState.HALF_OPEN:
            # Allow limited requests in half-open state
            return True
        
        return False
    
    def _on_success(self, execution_time: float):
        """Handle successful function execution."""
        if self._state == CircuitState.HALF_OPEN:
            self._success_count += 1
            
            logger.debug("Success in half-open state",
                        name=self.name,
                        success_count=self._success_count,
                        required=self.config.success_threshold)
            
            if self._success_count >= self.config.success_threshold:
                logger.info("Circuit breaker closing after successful recovery",
                           name=self.name,
                           success_count=self._success_count)
                self._transition_to_closed()
        
        elif self._state == CircuitState.CLOSED:
            # Reset failure count on success in closed state
            if self._failure_count > 0:
                logger.debug("Resetting failure count after success",
                           name=self.name,
                           previous_failures=self._failure_count)
                self._failure_count = 0
    
    def _on_failure(self, exception: Exception, execution_time: float):
        """Handle failed function execution."""
        self._failed_calls += 1
        self._failure_count += 1
        self._last_failure_time = time.time()
        
        if self._state == CircuitState.CLOSED:
            if self._failure_count >= self.config.failure_threshold:
                logger.warning("Circuit breaker opening due to failure threshold",
                             name=self.name,
                             failure_count=self._failure_count,
                             threshold=self.config.failure_threshold,
                             error=str(exception))
                self._transition_to_open()
        
        elif self._state == CircuitState.HALF_OPEN:
            logger.warning("Circuit breaker opening again after half-open failure",
                         name=self.name,
                         error=str(exception))
            self._transition_to_open()
    
    def _transition_to_closed(self):
        """Transition circuit breaker to closed state."""
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._state_transitions[CircuitState.CLOSED] += 1
        
        logger.info("Circuit breaker state: CLOSED",
                   name=self.name,
                   total_calls=self._total_calls,
                   failed_calls=self._failed_calls)
    
    def _transition_to_open(self):
        """Transition circuit breaker to open state."""
        self._state = CircuitState.OPEN
        self._success_count = 0
        self._next_attempt_time = time.time() + self.config.recovery_timeout
        self._state_transitions[CircuitState.OPEN] += 1
        
        logger.error("Circuit breaker state: OPEN",
                    name=self.name,
                    failure_count=self._failure_count,
                    recovery_timeout=self.config.recovery_timeout,
                    next_attempt_time=self._next_attempt_time)
    
    def _transition_to_half_open(self):
        """Transition circuit breaker to half-open state."""
        self._state = CircuitState.HALF_OPEN
        self._success_count = 0
        self._state_transitions[CircuitState.HALF_OPEN] += 1
        
        logger.info("Circuit breaker state: HALF_OPEN",
                   name=self.name,
                   failure_count=self._failure_count)
    
    def get_state(self) -> CircuitState:
        """Get current circuit breaker state."""
        with self._lock:
            return self._state
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get circuit breaker metrics for monitoring."""
        with self._lock:
            return {
                'name': self.name,
                'state': self._state.value,
                'failure_count': self._failure_count,
                'success_count': self._success_count,
                'total_calls': self._total_calls,
                'failed_calls': self._failed_calls,
                'rejected_calls': self._rejected_calls,
                'failure_rate': self._failed_calls / max(self._total_calls, 1),
                'rejection_rate': self._rejected_calls / max(self._total_calls, 1),
                'last_failure_time': self._last_failure_time,
                'next_attempt_time': self._next_attempt_time,
                'state_transitions': dict(self._state_transitions)
            }
    
    def force_open(self):
        """Manually force circuit breaker to open state (for testing/maintenance)."""
        with self._lock:
            logger.warning("Circuit breaker manually forced to OPEN state",
                         name=self.name)
            self._transition_to_open()
    
    def force_closed(self):
        """Manually force circuit breaker to closed state (for testing/maintenance)."""
        with self._lock:
            logger.warning("Circuit breaker manually forced to CLOSED state",
                         name=self.name)
            self._transition_to_closed()
    
    def reset(self):
        """Reset circuit breaker to initial state."""
        with self._lock:
            logger.info("Circuit breaker reset",
                       name=self.name,
                       previous_state=self._state.value,
                       failure_count=self._failure_count)
            
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._success_count = 0
            self._last_failure_time = 0.0
            self._next_attempt_time = 0.0


class VaultCircuitBreakerManager:
    """
    Manages multiple circuit breakers for different Vault operations.
    
    Provides centralized control and monitoring of circuit breakers
    for various Vault API endpoints and operations.
    """
    
    def __init__(self):
        """Initialize circuit breaker manager."""
        self._breakers: Dict[str, VaultCircuitBreaker] = {}
        self._lock = threading.RLock()
        self._max_breakers = 10  # CRITICAL: Limit to prevent unbounded growth
        
        # Default configurations for different operation types
        self._default_configs = {
            'secret_read': CircuitBreakerConfig(
                failure_threshold=3,
                recovery_timeout=30.0,
                success_threshold=2,
                timeout=10.0
            ),
            'secret_write': CircuitBreakerConfig(
                failure_threshold=5,
                recovery_timeout=60.0,
                success_threshold=3,
                timeout=30.0
            ),
            'pki_generate': CircuitBreakerConfig(
                failure_threshold=3,
                recovery_timeout=45.0,
                success_threshold=2,
                timeout=20.0
            ),
            'auth': CircuitBreakerConfig(
                failure_threshold=2,
                recovery_timeout=30.0,
                success_threshold=1,
                timeout=15.0
            ),
            'health': CircuitBreakerConfig(
                failure_threshold=5,
                recovery_timeout=15.0,
                success_threshold=2,
                timeout=5.0
            )
        }
        
        logger.info("Circuit breaker manager initialized",
                   available_configs=list(self._default_configs.keys()))
    
    def get_breaker(self, operation_type: str, custom_config: Optional[CircuitBreakerConfig] = None) -> VaultCircuitBreaker:
        """
        Get or create circuit breaker for operation type.
        
        Args:
            operation_type: Type of operation (e.g., 'secret_read', 'pki_generate')
            custom_config: Optional custom configuration
            
        Returns:
            Circuit breaker instance
        """
        with self._lock:
            if operation_type not in self._breakers:
                # CRITICAL: Prevent unbounded growth that causes crashes
                if len(self._breakers) >= self._max_breakers:
                    logger.warning("Too many circuit breakers, clearing oldest",
                                 current_count=len(self._breakers),
                                 max_allowed=self._max_breakers)
                    # Clear all breakers to prevent memory exhaustion
                    self._breakers.clear()
                
                # Use custom config or default for operation type
                config = custom_config or self._default_configs.get(
                    operation_type, 
                    CircuitBreakerConfig()  # Fallback to default
                )
                
                breaker_name = f"vault_{operation_type}"
                self._breakers[operation_type] = VaultCircuitBreaker(config, breaker_name)
                
                logger.info("Created new circuit breaker",
                           operation_type=operation_type,
                           name=breaker_name)
            
            return self._breakers[operation_type]
    
    def get_all_metrics(self) -> Dict[str, Dict[str, Any]]:
        """Get metrics for all circuit breakers."""
        with self._lock:
            return {
                operation_type: breaker.get_metrics()
                for operation_type, breaker in self._breakers.items()
            }
    
    def reset_all(self):
        """Reset all circuit breakers."""
        with self._lock:
            for breaker in self._breakers.values():
                breaker.reset()
            
            logger.info("All circuit breakers reset",
                       count=len(self._breakers))
    
    def get_overall_health(self) -> Dict[str, Any]:
        """Get overall health status of all circuit breakers."""
        with self._lock:
            total_breakers = len(self._breakers)
            open_breakers = sum(1 for b in self._breakers.values() if b.get_state() == CircuitState.OPEN)
            half_open_breakers = sum(1 for b in self._breakers.values() if b.get_state() == CircuitState.HALF_OPEN)
            
            health_status = "healthy"
            if open_breakers > 0:
                health_status = "degraded" if open_breakers < total_breakers else "critical"
            elif half_open_breakers > 0:
                health_status = "recovering"
            
            return {
                'status': health_status,
                'total_breakers': total_breakers,
                'closed_breakers': total_breakers - open_breakers - half_open_breakers,
                'open_breakers': open_breakers,
                'half_open_breakers': half_open_breakers,
                'timestamp': time.time()
            }


# Global circuit breaker manager instance
_circuit_breaker_manager: Optional[VaultCircuitBreakerManager] = None
_manager_lock = threading.RLock()


def get_vault_circuit_breaker_manager() -> VaultCircuitBreakerManager:
    """Get or create global circuit breaker manager."""
    global _circuit_breaker_manager
    
    with _manager_lock:
        if _circuit_breaker_manager is None:
            _circuit_breaker_manager = VaultCircuitBreakerManager()
        
        return _circuit_breaker_manager


def circuit_breaker_protected(operation_type: str, custom_config: Optional[CircuitBreakerConfig] = None):
    """
    Decorator to protect functions with circuit breaker.
    
    Args:
        operation_type: Type of operation for circuit breaker selection
        custom_config: Optional custom circuit breaker configuration
    """
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            manager = get_vault_circuit_breaker_manager()
            breaker = manager.get_breaker(operation_type, custom_config)
            return breaker.call(func, *args, **kwargs)
        
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper
    
    return decorator