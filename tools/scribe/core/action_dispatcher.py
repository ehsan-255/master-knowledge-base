#!/usr/bin/env python3
"""
Scribe Action Dispatcher

Orchestrates the execution of actions when rules match.
Handles action loading, parameter validation, execution, and error recovery.
"""

import re
import time
import shutil
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import structlog

from .logging_config import get_scribe_logger
from .plugin_loader import PluginLoader, PluginInfo
from .rule_processor import RuleMatch
from .circuit_breaker import CircuitBreakerManager, CircuitBreakerError

# Import action base classes
from actions.base import BaseAction, ActionExecutionError, ValidationError

logger = get_scribe_logger(__name__)


class ActionChainFailedError(Exception):
    """Exception raised when one or more actions fail in a chain."""
    
    def __init__(self, message: str, rule_id: str = None, failed_actions: int = 0, total_actions: int = 0):
        """
        Initialize the exception.
        
        Args:
            message: Error message
            rule_id: ID of the rule that failed
            failed_actions: Number of failed actions
            total_actions: Total number of actions in the chain
        """
        self.rule_id = rule_id
        self.failed_actions = failed_actions
        self.total_actions = total_actions
        super().__init__(message)


class ActionResult:
    """Result of executing an action."""
    
    def __init__(self, 
                 action_type: str,
                 success: bool,
                 modified_content: Optional[str] = None,
                 error: Optional[Exception] = None,
                 execution_time: float = 0.0,
                 metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize action result.
        
        Args:
            action_type: Type of action that was executed
            success: Whether the action succeeded
            modified_content: The modified file content (if successful)
            error: Exception if the action failed
            execution_time: Time taken to execute the action in seconds
            metadata: Additional metadata about the execution
        """
        self.action_type = action_type
        self.success = success
        self.modified_content = modified_content
        self.error = error
        self.execution_time = execution_time
        self.metadata = metadata or {}
        self.timestamp = time.time()
    
    def __str__(self) -> str:
        status = "SUCCESS" if self.success else "FAILED"
        return f"ActionResult({self.action_type}: {status})"
    
    def __repr__(self) -> str:
        return f"ActionResult(action_type='{self.action_type}', success={self.success}, execution_time={self.execution_time:.3f}s)"


class DispatchResult:
    """Result of dispatching all actions for a rule match."""
    
    def __init__(self, 
                 rule_id: str,
                 file_path: str,
                 final_content: str,
                 action_results: List[ActionResult]):
        """
        Initialize dispatch result.
        
        Args:
            rule_id: ID of the rule that was processed
            file_path: Path to the file that was processed
            final_content: Final content after all actions
            action_results: Results of individual actions
        """
        self.rule_id = rule_id
        self.file_path = file_path
        self.final_content = final_content
        self.action_results = action_results
        self.timestamp = time.time()
        
        # Calculate summary statistics
        self.total_actions = len(action_results)
        self.successful_actions = sum(1 for r in action_results if r.success)
        self.failed_actions = self.total_actions - self.successful_actions
        self.total_execution_time = sum(r.execution_time for r in action_results)
        self.success = self.failed_actions == 0
    
    def get_failed_actions(self) -> List[ActionResult]:
        """Get list of failed action results."""
        return [r for r in self.action_results if not r.success]
    
    def get_successful_actions(self) -> List[ActionResult]:
        """Get list of successful action results."""
        return [r for r in self.action_results if r.success]
    
    def __str__(self) -> str:
        status = "SUCCESS" if self.success else "PARTIAL/FAILED"
        return f"DispatchResult({self.rule_id}: {status}, {self.successful_actions}/{self.total_actions} actions)"
    
    def __repr__(self) -> str:
        return f"DispatchResult(rule_id='{self.rule_id}', success={self.success}, actions={self.successful_actions}/{self.total_actions})"


class ActionDispatcher:
    """
    Dispatches and executes actions for rule matches.
    
    Handles action loading, parameter validation, execution orchestration,
    and error recovery with comprehensive logging.
    """
    
    def __init__(self, plugin_loader: PluginLoader, security_config: Optional[Dict[str, Any]] = None, quarantine_path: Optional[str] = None):
        """
        Initialize the action dispatcher.
        
        Args:
            plugin_loader: Plugin loader for action plugins
            security_config: Security configuration for action execution
            quarantine_path: Path to quarantine directory for failed files
        """
        self.plugin_loader = plugin_loader
        self.security_config = security_config or {}
        self.quarantine_path = quarantine_path or "archive/scribe/quarantine/"
        
        # Circuit breaker manager for rule failure isolation
        self.circuit_breaker_manager = CircuitBreakerManager()
        
        # Action instance cache for performance
        self._action_cache: Dict[str, BaseAction] = {}
        
        # Execution statistics
        self._execution_stats = {
            'total_dispatches': 0,
            'successful_dispatches': 0,
            'failed_dispatches': 0,
            'total_actions_executed': 0,
            'total_execution_time': 0.0,
            'circuit_breaker_blocks': 0,
            'files_quarantined': 0
        }
        
        logger.info("ActionDispatcher initialized",
                   security_enabled=bool(security_config),
                   circuit_breaker_enabled=True,
                   quarantine_path=self.quarantine_path)
    
    def get_action_instance(self, action_type: str) -> Optional[BaseAction]:
        """
        Get an action instance, using cache for performance.
        
        Args:
            action_type: Type of action to get
            
        Returns:
            Action instance if available, None otherwise
        """
        # Check cache first
        if action_type in self._action_cache:
            return self._action_cache[action_type]
        
        # Create new instance
        action_instance = self.plugin_loader.create_action_instance(action_type)
        if action_instance:
            self._action_cache[action_type] = action_instance
            logger.debug("Action instance cached",
                        action_type=action_type,
                        class_name=action_instance.__class__.__name__)
        
        return action_instance
    
    def validate_action_params(self, action: BaseAction, params: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate action parameters.
        
        Args:
            action: The action instance
            params: Parameters to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Check required parameters
            required_params = action.get_required_params()
            for param_name in required_params:
                if param_name not in params:
                    return False, f"Required parameter '{param_name}' is missing"
                if params[param_name] is None:
                    return False, f"Required parameter '{param_name}' cannot be None"
            
            # Use action's validation method
            if not action.validate_params(params):
                return False, "Action parameter validation failed"
            
            return True, None
            
        except Exception as e:
            return False, f"Parameter validation error: {e}"
    
    def apply_security_restrictions(self, action_type: str, params: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Apply security restrictions to action execution.
        
        Args:
            action_type: Type of action being executed
            params: Action parameters
            
        Returns:
            Tuple of (is_allowed, denial_reason)
        """
        # Check if action type is allowed
        allowed_actions = self.security_config.get('allowed_actions', [])
        if allowed_actions and action_type not in allowed_actions:
            return False, f"Action type '{action_type}' is not in allowed actions list"
        
        # Check for restricted parameters
        restricted_params = self.security_config.get('restricted_params', [])
        for param_name in params:
            if param_name in restricted_params:
                return False, f"Parameter '{param_name}' is restricted by security policy"
        
        # Check for dangerous parameter values
        dangerous_patterns = self.security_config.get('dangerous_patterns', [])
        for param_name, param_value in params.items():
            if isinstance(param_value, str):
                for pattern in dangerous_patterns:
                    if re.search(pattern, param_value):
                        return False, f"Parameter '{param_name}' contains dangerous pattern"
        
        return True, None
    
    def execute_action(self, 
                      action: BaseAction,
                      file_content: str,
                      match: re.Match,
                      file_path: str,
                      params: Dict[str, Any],
                      event_id: Optional[str] = None) -> ActionResult:
        """
        Execute a single action with error handling and timing.
        
        Args:
            action: The action instance to execute
            file_content: Current file content
            match: Regex match that triggered the action
            file_path: Path to the file being processed
            params: Action parameters
            event_id: Unique identifier for the event that triggered this action
            
        Returns:
            ActionResult with execution details
        """
        start_time = time.time()
        action_type = action.action_type
        
        try:
            logger.debug("Executing action",
                        event_id=event_id,
                        action_type=action_type,
                        file_path=file_path,
                        params=params)
            
            # Pre-execution hook
            action.pre_execute(file_content, match, file_path, params)
            
            # Execute the action
            modified_content = action.execute(file_content, match, file_path, params)
            
            # Post-execution hook
            action.post_execute(file_content, modified_content, match, file_path, params)
            
            execution_time = time.time() - start_time
            
            # Validate that we got a string back
            if not isinstance(modified_content, str):
                raise ActionExecutionError(action_type, f"Action returned {type(modified_content)}, expected str")
            
            logger.info("Action executed successfully",
                       event_id=event_id,
                       action_type=action_type,
                       file_path=file_path,
                       execution_time=execution_time,
                       content_changed=modified_content != file_content)
            
            return ActionResult(
                action_type=action_type,
                success=True,
                modified_content=modified_content,
                execution_time=execution_time,
                metadata={
                    'content_changed': modified_content != file_content,
                    'content_length_before': len(file_content),
                    'content_length_after': len(modified_content)
                }
            )
            
        except (ActionExecutionError, ValidationError) as e:
            execution_time = time.time() - start_time
            logger.error("Action execution failed",
                        event_id=event_id,
                        action_type=action_type,
                        file_path=file_path,
                        error=str(e),
                        execution_time=execution_time)
            
            return ActionResult(
                action_type=action_type,
                success=False,
                error=e,
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error("Unexpected error during action execution",
                        event_id=event_id,
                        action_type=action_type,
                        file_path=file_path,
                        error=str(e),
                        execution_time=execution_time,
                        exc_info=True)
            
            wrapped_error = ActionExecutionError(action_type, "Unexpected error", e)
            return ActionResult(
                action_type=action_type,
                success=False,
                error=wrapped_error,
                execution_time=execution_time
            )
    
    def dispatch_actions(self, rule_match: RuleMatch) -> DispatchResult:
        """
        Dispatch all actions for a rule match with circuit breaker protection.
        
        Args:
            rule_match: The rule match to process
            
        Returns:
            DispatchResult with execution details
        """
        start_time = time.time()
        rule_id = rule_match.rule.id
        file_path = rule_match.file_path
        current_content = rule_match.file_content
        event_id = rule_match.event_id
        
        logger.info("Dispatching actions for rule match",
                   event_id=event_id,
                   rule_id=rule_id,
                   file_path=file_path,
                   actions_count=len(rule_match.rule.actions))
        
        # Update statistics
        self._execution_stats['total_dispatches'] += 1
        
        # Get circuit breaker configuration from rule
        circuit_breaker_config = self._get_circuit_breaker_config(rule_match.rule)
        circuit_breaker = self.circuit_breaker_manager.get_breaker(
            rule_id=rule_id,
            **circuit_breaker_config
        )
        
        # Check if circuit breaker allows execution
        try:
            # Wrap the action execution logic with circuit breaker
            def execute_actions():
                return self._execute_actions_internal(rule_match, current_content)
            
            dispatch_result = circuit_breaker.execute(execute_actions)
            
            # Update statistics for successful dispatch
            self._execution_stats['successful_dispatches'] += 1
            total_time = time.time() - start_time
            self._execution_stats['total_execution_time'] += total_time
            
            logger.info("Action dispatch complete (circuit breaker: CLOSED)",
                       event_id=event_id,
                       rule_id=rule_id,
                       file_path=file_path,
                       total_actions=dispatch_result.total_actions,
                       successful_actions=dispatch_result.successful_actions,
                       failed_actions=dispatch_result.failed_actions,
                       total_time=total_time,
                       content_changed=dispatch_result.final_content != rule_match.file_content)
            
            return dispatch_result
            
        except CircuitBreakerError as e:
            # Circuit breaker is open - block execution and quarantine file
            self._execution_stats['circuit_breaker_blocks'] += 1
            self._execution_stats['failed_dispatches'] += 1
            
            logger.warning("Action dispatch blocked by circuit breaker",
                          event_id=event_id,
                          rule_id=rule_id,
                          file_path=file_path,
                          failure_count=e.failure_count,
                          last_failure_time=e.last_failure_time,
                          circuit_state="OPEN")
            
            # Quarantine the problematic file
            quarantine_result = self.quarantine_file(file_path, rule_id, "circuit_breaker_open")
            
            # Return result with a synthetic failure to indicate circuit breaker block
            circuit_breaker_error = ActionResult(
                action_type="circuit_breaker",
                success=False,
                error=e,
                execution_time=0.0,
                metadata={
                    "blocked_by_circuit_breaker": True,
                    "quarantined": quarantine_result["success"],
                    "quarantine_path": quarantine_result.get("quarantine_path"),
                    "quarantine_reason": "circuit_breaker_open"
                }
            )
            
            return DispatchResult(
                rule_id=rule_id,
                file_path=file_path,
                final_content=current_content,
                action_results=[circuit_breaker_error]
            )
            
        except Exception as e:
            # Unexpected error during circuit breaker execution
            self._execution_stats['failed_dispatches'] += 1
            
            logger.error("Unexpected error during circuit breaker execution",
                        event_id=event_id,
                        rule_id=rule_id,
                        file_path=file_path,
                        error=str(e),
                        exc_info=True)
            
            # Return result with a synthetic failure to indicate system error
            system_error = ActionResult(
                action_type="system_error",
                success=False,
                error=e,
                execution_time=0.0,
                metadata={"system_level_failure": True}
            )
            
            return DispatchResult(
                rule_id=rule_id,
                file_path=file_path,
                final_content=current_content,
                action_results=[system_error]
            )
    
    def _get_circuit_breaker_config(self, rule) -> Dict[str, int]:
        """
        Extract circuit breaker configuration from rule.
        
        Args:
            rule: Rule object with potential circuit breaker config
            
        Returns:
            Dictionary with circuit breaker parameters
        """
        # Default circuit breaker configuration
        default_config = {
            'failure_threshold': 5,
            'recovery_timeout_seconds': 60,
            'success_threshold': 3
        }
        
        # Check if rule has error handling configuration
        if hasattr(rule, 'error_handling') and rule.error_handling:
            circuit_breaker_config = rule.error_handling.get('circuit_breaker', {})
            
            # Override defaults with rule-specific config
            for key in default_config:
                if key in circuit_breaker_config:
                    default_config[key] = circuit_breaker_config[key]
        
        return default_config
    
    def _execute_actions_internal(self, rule_match: RuleMatch, current_content: str) -> DispatchResult:
        """
        Internal method to execute actions for a rule match.
        
        This method contains the actual action execution logic and is wrapped
        by the circuit breaker in dispatch_actions().
        
        Args:
            rule_match: The rule match to process
            current_content: Current file content
            
        Returns:
            DispatchResult with execution details
            
        Raises:
            Exception: Any exception during action execution (will be caught by circuit breaker)
        """
        rule_id = rule_match.rule.id
        file_path = rule_match.file_path
        event_id = rule_match.event_id
        action_results = []
        
        # Process each action in sequence
        for action_config in rule_match.rule.actions:
            action_type = action_config['type']
            params = action_config.get('params', {})
            
            # Get action instance
            action = self.get_action_instance(action_type)
            if action is None:
                error = ActionExecutionError(action_type, "Action plugin not found")
                action_results.append(ActionResult(
                    action_type=action_type,
                    success=False,
                    error=error
                ))
                logger.error("Action plugin not found", action_type=action_type)
                continue
            
            # Validate parameters
            params_valid, validation_error = self.validate_action_params(action, params)
            if not params_valid:
                error = ValidationError(action_type, "params", validation_error)
                action_results.append(ActionResult(
                    action_type=action_type,
                    success=False,
                    error=error
                ))
                logger.error("Action parameter validation failed",
                           action_type=action_type,
                           error=validation_error)
                continue
            
            # Apply security restrictions
            security_allowed, security_reason = self.apply_security_restrictions(action_type, params)
            if not security_allowed:
                error = ActionExecutionError(action_type, f"Security restriction: {security_reason}")
                action_results.append(ActionResult(
                    action_type=action_type,
                    success=False,
                    error=error
                ))
                logger.error("Action blocked by security policy",
                           action_type=action_type,
                           reason=security_reason)
                continue
            
            # Execute the action
            result = self.execute_action(action, current_content, rule_match.match, file_path, params, event_id)
            action_results.append(result)
            
            # Update statistics
            self._execution_stats['total_actions_executed'] += 1
            
            # If action succeeded, use its output as input for next action
            if result.success and result.modified_content is not None:
                current_content = result.modified_content
            else:
                # If action failed, log but continue with other actions
                logger.warning("Action failed, continuing with remaining actions",
                             action_type=action_type,
                             rule_id=rule_id)
        
        # Create dispatch result
        dispatch_result = DispatchResult(
            rule_id=rule_id,
            file_path=file_path,
            final_content=current_content,
            action_results=action_results
        )
        
        # Check if action chain should trigger circuit breaker
        # Circuit breaker should trip on persistent action failures, not just system failures
        failed_actions = dispatch_result.get_failed_actions()
        total_actions = len(action_results)
        
        if total_actions > 0:
            failure_rate = len(failed_actions) / total_actions
            
            # Trip circuit breaker if:
            # 1. All actions failed, OR
            # 2. More than 50% of actions failed AND there are multiple actions
            should_trip_breaker = (
                failure_rate >= 1.0 or  # All actions failed
                (failure_rate > 0.5 and total_actions > 1)  # >50% failed with multiple actions
            )
            
            if should_trip_breaker:
                # Create a summary of failures for the exception
                failure_summary = []
                for failed_action in failed_actions:
                    failure_summary.append(f"{failed_action.action_type}: {failed_action.error}")
                
                error_message = (
                    f"Action chain failure in rule '{rule_id}': "
                    f"{len(failed_actions)}/{total_actions} actions failed. "
                    f"Failures: {'; '.join(failure_summary)}"
                )
                
                logger.error("Action chain failure triggering circuit breaker",
                           event_id=event_id,
                           rule_id=rule_id,
                           file_path=file_path,
                           failed_actions=len(failed_actions),
                           total_actions=total_actions,
                           failure_rate=failure_rate)
                
                # Raise exception to trigger circuit breaker
                raise ActionChainFailedError(
                    error_message,
                    rule_id=rule_id,
                    failed_actions=len(failed_actions),
                    total_actions=total_actions
                )
        
        return dispatch_result
    
    def quarantine_file(self, file_path: str, rule_id: str, reason: str) -> Dict[str, Any]:
        """
        Quarantine a problematic file by moving it to the quarantine directory.
        
        Args:
            file_path: Path to the file to quarantine
            rule_id: ID of the rule that caused the quarantine
            reason: Reason for quarantine (e.g., "circuit_breaker_open")
            
        Returns:
            Dictionary with quarantine operation result
        """
        try:
            # Convert to Path objects for easier manipulation
            source_path = Path(file_path)
            
            # Check if source file exists
            if not source_path.exists():
                logger.warning("Cannot quarantine file - file does not exist",
                             file_path=file_path,
                             rule_id=rule_id,
                             reason=reason)
                return {
                    "success": False,
                    "error": "File does not exist",
                    "file_path": file_path
                }
            
            # Create quarantine directory structure
            quarantine_base = Path(self.quarantine_path)
            
            # Preserve relative path structure in quarantine
            if source_path.is_absolute():
                # For absolute paths, use relative path from current working directory
                try:
                    relative_path = source_path.relative_to(Path.cwd())
                except ValueError:
                    # If can't make relative, preserve the full path structure
                    # Remove drive letter and leading slash for Windows compatibility
                    path_parts = source_path.parts
                    if len(path_parts) > 1 and ':' in path_parts[0]:
                        # Windows path with drive letter
                        relative_path = Path(*path_parts[1:])
                    else:
                        # Unix-style absolute path
                        relative_path = Path(*path_parts[1:]) if path_parts[0] == '/' else source_path
            else:
                relative_path = source_path
            
            # Ensure relative_path is a Path object
            if isinstance(relative_path, str):
                relative_path = Path(relative_path)
            
            # Create timestamped filename to avoid conflicts
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            stem = relative_path.stem
            suffix = relative_path.suffix
            quarantine_filename = f"{stem}_{timestamp}{suffix}"
            
            # Build full quarantine path
            quarantine_dir = quarantine_base / relative_path.parent
            quarantine_path = quarantine_dir / quarantine_filename
            
            # Create quarantine directory if it doesn't exist
            quarantine_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy file to quarantine (preserving original)
            shutil.copy2(source_path, quarantine_path)
            
            # Create metadata file alongside quarantined file
            metadata_path = quarantine_path.with_suffix(quarantine_path.suffix + ".quarantine_info")
            metadata = {
                "original_path": str(source_path),
                "quarantine_time": datetime.now().isoformat(),
                "rule_id": rule_id,
                "reason": reason,
                "quarantine_path": str(quarantine_path)
            }
            
            with open(metadata_path, 'w') as f:
                import json
                json.dump(metadata, f, indent=2)
            
            # Remove original file after successful quarantine
            source_path.unlink()
            
            # Update statistics
            self._execution_stats['files_quarantined'] += 1
            
            logger.info("File quarantined successfully",
                       original_path=str(source_path),
                       quarantine_path=str(quarantine_path),
                       rule_id=rule_id,
                       reason=reason)
            
            return {
                "success": True,
                "original_path": str(source_path),
                "quarantine_path": str(quarantine_path),
                "metadata_path": str(metadata_path),
                "rule_id": rule_id,
                "reason": reason
            }
            
        except Exception as e:
            logger.error("Failed to quarantine file",
                        file_path=file_path,
                        rule_id=rule_id,
                        reason=reason,
                        error=str(e),
                        exc_info=True)
            
            return {
                "success": False,
                "error": str(e),
                "file_path": file_path,
                "rule_id": rule_id,
                "reason": reason
            }
    
    def clear_action_cache(self) -> None:
        """Clear the action instance cache."""
        self._action_cache.clear()
        logger.debug("Action cache cleared")
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """
        Get execution statistics.
        
        Returns:
            Dictionary with execution statistics
        """
        stats = self._execution_stats.copy()
        
        # Calculate derived statistics
        if stats['total_dispatches'] > 0:
            stats['success_rate'] = stats['successful_dispatches'] / stats['total_dispatches']
            stats['average_execution_time'] = stats['total_execution_time'] / stats['total_dispatches']
        else:
            stats['success_rate'] = 0.0
            stats['average_execution_time'] = 0.0
        
        stats['cached_actions'] = len(self._action_cache)
        stats['available_action_types'] = list(self.plugin_loader.get_all_plugins().keys())
        
        # Add circuit breaker statistics
        stats['circuit_breaker_stats'] = self.get_circuit_breaker_stats()
        
        # Add quarantine statistics
        stats['quarantine_stats'] = {
            'files_quarantined': stats['files_quarantined'],
            'quarantine_path': self.quarantine_path
        }
        
        return stats
    
    def get_circuit_breaker_stats(self) -> Dict[str, Any]:
        """
        Get circuit breaker statistics.
        
        Returns:
            Dictionary with circuit breaker statistics
        """
        return self.circuit_breaker_manager.get_manager_stats()
    
    def reset_stats(self) -> None:
        """Reset execution statistics."""
        self._execution_stats = {
            'total_dispatches': 0,
            'successful_dispatches': 0,
            'failed_dispatches': 0,
            'total_actions_executed': 0,
            'total_execution_time': 0.0,
            'circuit_breaker_blocks': 0,
            'files_quarantined': 0
        }
        logger.debug("Execution statistics reset") 