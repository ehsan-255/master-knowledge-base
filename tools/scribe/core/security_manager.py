#!/usr/bin/env python3
"""
Scribe Security Manager

Implements security sandboxing for action execution including:
- Command whitelisting
- Path restrictions
- Environment variable scrubbing
- Parameter validation
"""

import os
import re
import shlex
import subprocess
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Set
import structlog

from .logging_config import get_scribe_logger
from .config_manager import ConfigManager

logger = get_scribe_logger(__name__)


class SecurityViolation(Exception):
    """Exception raised when a security policy is violated."""
    
    def __init__(self, violation_type: str, message: str, details: Optional[Dict[str, Any]] = None):
        """
        Initialize the exception.
        
        Args:
            violation_type: Type of security violation
            message: Error message
            details: Additional details about the violation
        """
        self.violation_type = violation_type
        self.details = details or {}
        super().__init__(f"Security violation ({violation_type}): {message}")


class SecurityManager:
    """
    Manages security policies and enforcement for action execution.
    
    Provides command whitelisting, path restrictions, environment scrubbing,
    and other security measures to ensure safe action execution.
    """
    
    def __init__(self, config_manager: ConfigManager):
        """
        Initialize the security manager.
        
        Args:
            config_manager: Configuration manager for security settings
        """
        self.config_manager = config_manager
        
        # Cache security settings for performance
        self._security_config: Dict[str, Any] = {}
        self._allowed_commands: Set[str] = set()
        self._restricted_paths: List[str] = []
        self._dangerous_patterns: List[re.Pattern] = []
        
        # Register for configuration changes
        self.config_manager.add_change_callback(self._on_config_change)
        
        # Load initial security configuration
        self._load_security_config()
        
        logger.info("SecurityManager initialized",
                   allowed_commands=len(self._allowed_commands),
                   restricted_paths=len(self._restricted_paths),
                   dangerous_patterns=len(self._dangerous_patterns))
    
    def _load_security_config(self) -> None:
        """Load security configuration from config manager and external security policy."""
        try:
            self._security_config = self.config_manager.get_security_settings()
            
            # Load allowed commands
            allowed_commands = self._security_config.get('allowed_commands', [])
            self._allowed_commands = set(allowed_commands)
            
            # Load restricted paths
            self._restricted_paths = self._security_config.get('restricted_paths', [])
            
            # Load dangerous patterns from external security policy file
            security_policy = self._load_security_policy_file()
            dangerous_patterns = security_policy.get('dangerous_patterns', [])
            
            self._dangerous_patterns = []
            for pattern in dangerous_patterns:
                try:
                    compiled_pattern = re.compile(pattern, re.IGNORECASE)
                    self._dangerous_patterns.append(compiled_pattern)
                except re.error as e:
                    logger.error("Failed to compile dangerous pattern",
                               pattern=pattern,
                               error=str(e))
            
            # Load dangerous environment keys from external policy
            self._dangerous_env_keys = security_policy.get('dangerous_env_keys_to_always_scrub', [])
            
            logger.debug("Security configuration loaded",
                        allowed_commands=len(self._allowed_commands),
                        restricted_paths=len(self._restricted_paths),
                        dangerous_patterns=len(self._dangerous_patterns),
                        dangerous_env_keys=len(self._dangerous_env_keys))
            
        except Exception as e:
            logger.error("Failed to load security configuration",
                        error=str(e),
                        exc_info=True)
            # Use safe defaults
            self._security_config = {}
            self._allowed_commands = set()
            self._restricted_paths = []
            self._dangerous_patterns = []
            self._dangerous_env_keys = []
    
    def _load_security_policy_file(self) -> Dict[str, Any]:
        """Load security policy from external YAML file."""
        try:
            # Try to get policy file path from config, fallback to default
            policy_file_path = self.config_manager.get('security_policy_file', 
                                                      'config/security_policy.yaml')
            
            # Make path relative to the script directory if not absolute
            if not Path(policy_file_path).is_absolute():
                script_dir = Path(__file__).parent.parent
                policy_file_path = script_dir / policy_file_path
            
            with open(policy_file_path, 'r', encoding='utf-8') as f:
                policy = yaml.safe_load(f)
                
            logger.debug("Security policy loaded from file", 
                        policy_file=str(policy_file_path),
                        policy_version=policy.get('policy_metadata', {}).get('version'))
            
            return policy or {}
            
        except FileNotFoundError:
            logger.warning("Security policy file not found, using empty policy", 
                          policy_file=str(policy_file_path))
            return {}
        except yaml.YAMLError as e:
            logger.error("Failed to parse security policy YAML file",
                        policy_file=str(policy_file_path),
                        error=str(e))
            return {}
        except Exception as e:
            logger.error("Failed to load security policy file",
                        policy_file=str(policy_file_path),
                        error=str(e))
            return {}
    
    def _on_config_change(self, new_config: Dict[str, Any]) -> None:
        """Handle configuration changes by reloading security settings."""
        logger.info("Security configuration changed, reloading")
        self._load_security_config()
    
    def validate_command(self, command: str) -> Tuple[bool, Optional[str]]:
        """
        Validate a command against the whitelist.
        
        Args:
            command: Command to validate
            
        Returns:
            Tuple of (is_allowed, denial_reason)
        """
        if not command or not command.strip():
            return False, "Empty command not allowed"
        
        try:
            # Parse the command to extract the base command
            parsed_command = shlex.split(command.strip())
            if not parsed_command:
                return False, "Invalid command format"
            
            base_command = parsed_command[0]
            
            # Extract just the command name (remove path)
            command_name = Path(base_command).name
            
            # Check against whitelist
            if self._allowed_commands and command_name not in self._allowed_commands:
                return False, f"Command '{command_name}' is not in the allowed commands list"
            
            # Check for dangerous patterns
            for pattern in self._dangerous_patterns:
                if pattern.search(command):
                    return False, f"Command contains dangerous pattern: {pattern.pattern}"
            
            logger.debug("Command validation passed",
                        command=command,
                        base_command=command_name)
            
            return True, None
            
        except Exception as e:
            logger.error("Error validating command",
                        command=command,
                        error=str(e))
            return False, f"Command validation error: {e}"
    
    def validate_path(self, path: str, operation: str = "access") -> Tuple[bool, Optional[str]]:
        """
        Validate a file path against restrictions.
        
        Args:
            path: Path to validate
            operation: Type of operation (access, read, write, execute)
            
        Returns:
            Tuple of (is_allowed, denial_reason)
        """
        if not path:
            return False, "Empty path not allowed"
        
        try:
            # Normalize the path
            normalized_path = str(Path(path).resolve())
            
            # Check against restricted paths
            for restricted_path in self._restricted_paths:
                # Handle glob patterns
                if '*' in restricted_path or '?' in restricted_path:
                    import fnmatch
                    if fnmatch.fnmatch(normalized_path, restricted_path):
                        return False, f"Path matches restricted pattern: {restricted_path}"
                else:
                    # Handle directory restrictions
                    restricted_normalized = str(Path(restricted_path).resolve())
                    if normalized_path.startswith(restricted_normalized):
                        return False, f"Path is within restricted directory: {restricted_path}"
            
            # Additional security checks
            if '..' in path:
                return False, "Path traversal attempts not allowed"
            
            if path.startswith('/'):
                return False, "Absolute paths not allowed"
            
            logger.debug("Path validation passed",
                        path=path,
                        normalized_path=normalized_path,
                        operation=operation)
            
            return True, None
            
        except Exception as e:
            logger.error("Error validating path",
                        path=path,
                        error=str(e))
            return False, f"Path validation error: {e}"
    
    
    def validate_action_params(self, action_type: str, params: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate action parameters for security issues.
        
        Args:
            action_type: Type of action being executed
            params: Parameters to validate
            
        Returns:
            Tuple of (is_allowed, denial_reason)
        """
        try:
            # Check for dangerous parameter values
            for param_name, param_value in params.items():
                if isinstance(param_value, str):
                    # Check for dangerous patterns
                    for pattern in self._dangerous_patterns:
                        if pattern.search(param_value):
                            return False, f"Parameter '{param_name}' contains dangerous pattern"
                    
                    # Check for command injection attempts
                    if any(char in param_value for char in ['|', '&', ';', '`', '$(']):
                        return False, f"Parameter '{param_name}' contains command injection characters"
                    
                    # Check for path traversal
                    if '..' in param_value or param_value.startswith('/'):
                        return False, f"Parameter '{param_name}' contains unsafe path"
            
            # Action-specific validation
            if action_type == 'execute_command':
                command = params.get('command', '')
                is_valid, reason = self.validate_command(command)
                if not is_valid:
                    return False, f"Command validation failed: {reason}"
            
            elif action_type in ['read_file', 'write_file', 'append_file']:
                file_path = params.get('file_path', '')
                is_valid, reason = self.validate_path(file_path, 'write' if 'write' in action_type else 'read')
                if not is_valid:
                    return False, f"Path validation failed: {reason}"
            
            logger.debug("Action parameter validation passed",
                        action_type=action_type,
                        param_count=len(params))
            
            return True, None
            
        except Exception as e:
            logger.error("Error validating action parameters",
                        action_type=action_type,
                        error=str(e))
            return False, f"Parameter validation error: {e}"
    
    def execute_command_safely(self, 
                              command_list: List[str], 
                              cwd: Optional[str] = None,
                              timeout: int = 30,
                              allowed_env_vars: Optional[List[str]] = None) -> Tuple[bool, str, str]:
        """
        Execute a command safely with security restrictions.
        
        Args:
            command_list: Command as list of strings to execute
            cwd: Working directory (must be validated)
            timeout: Timeout in seconds
            
        Returns:
            Tuple of (success, stdout, stderr)
        """
        # Validate command (only validate the first element - the executable)
        if not command_list or len(command_list) == 0:
            raise SecurityViolation("command_validation", "Empty command list not allowed", {'command_list': command_list})
        
        is_valid, reason = self.validate_command(command_list[0])
        if not is_valid:
            raise SecurityViolation("command_validation", reason, {'command': command_list[0]})
        
        # Validate working directory if provided
        if cwd:
            is_valid, reason = self.validate_path(cwd, 'access')
            if not is_valid:
                raise SecurityViolation("path_validation", reason, {'path': cwd})
        
        try:
            # Scrub environment
            safe_env = self.scrub_environment(allowed_env_vars=allowed_env_vars)
            
            # Execute with restrictions
            result = subprocess.run(
                command_list,
                shell=False,  # Safe execution without shell
                cwd=cwd,
                env=safe_env,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False  # Don't raise on non-zero exit
            )
            
            logger.info("Command executed safely",
                       command=command_list,
                       exit_code=result.returncode,
                       cwd=cwd,
                       timeout=timeout)
            
            return result.returncode == 0, result.stdout, result.stderr
            
        except subprocess.TimeoutExpired:
            logger.error("Command execution timed out",
                        command=command_list,
                        timeout=timeout)
            raise SecurityViolation("execution_timeout", f"Command timed out after {timeout} seconds")
        
        except Exception as e:
            logger.error("Command execution failed",
                        command=command_list,
                        error=str(e),
                        exc_info=True)
            raise SecurityViolation("execution_error", f"Command execution failed: {e}")
    
    def get_security_stats(self) -> Dict[str, Any]:
        """
        Get security manager statistics.
        
        Returns:
            Dictionary with security statistics
        """
        return {
            'allowed_commands': list(self._allowed_commands),
            'allowed_commands_count': len(self._allowed_commands),
            'restricted_paths': self._restricted_paths,
            'restricted_paths_count': len(self._restricted_paths),
            'dangerous_patterns_count': len(self._dangerous_patterns),
            'security_config': self._security_config
        }
    
    def stop(self) -> None:
        """Stop the security manager and cleanup resources."""
        # Remove configuration change callback
        self.config_manager.remove_change_callback(self._on_config_change)
        
        logger.info("SecurityManager stopped")
    
    def scrub_environment(self, env_vars: Dict[str, str] = None, allowed_env_vars: Optional[List[str]] = None) -> Dict[str, str]:
        """
        Scrub sensitive information from environment variables.
        
        This method is overloaded to handle two different use cases:
        1. When called with env_vars dict: scrubs sensitive values from provided env vars
        2. When called with allowed_env_vars list: creates safe environment from os.environ
        
        Args:
            env_vars: Dictionary of environment variables to scrub (optional)
            allowed_env_vars: List of allowed environment variable names from os.environ (optional)
            
        Returns:
            Scrubbed environment variables with sensitive data removed/masked
        """
        # If env_vars dict is provided, scrub it (test compatibility mode)
        if env_vars is not None:
            return self._scrub_env_dict(env_vars)
        
        # Otherwise use the original implementation
        return self._scrub_from_os_environ(allowed_env_vars)
    
    def _scrub_env_dict(self, env_vars: Dict[str, str]) -> Dict[str, str]:
        """
        Scrub dangerous system environment variables from provided dict
        
        Args:
            env_vars: Dictionary of environment variables
            
        Returns:
            Scrubbed environment variables with dangerous keys removed and safe defaults
        """
        scrubbed = {}
        
        # Get dangerous keys from externalized policy (fallback to empty list if not loaded)
        dangerous_keys = getattr(self, '_dangerous_env_keys', [])
        
        # Copy all non-dangerous environment variables
        for key, value in env_vars.items():
            if key not in dangerous_keys:
                scrubbed[key] = value
        
        # Set safe defaults for critical environment variables
        scrubbed['PATH'] = '/usr/bin:/bin'
        scrubbed['LC_ALL'] = 'C' 
        scrubbed['LANG'] = 'C'
        
        return scrubbed
    
    def _scrub_from_os_environ(self, allowed_env_vars: Optional[List[str]] = None) -> Dict[str, str]:
        """
        Original scrub_environment implementation for creating safe environment from os.environ
        """
        safe_env: Dict[str, str] = {}

        # Start with an empty environment or a very minimal one
        safe_env: Dict[str, str] = {}

        # Populate with allowed variables from os.environ
        if allowed_env_vars:
            logger.debug(f"Processing allowed_env_vars: {allowed_env_vars}")
            for var_name in allowed_env_vars:
                if var_name in os.environ:
                    safe_env[var_name] = os.environ[var_name]
                    logger.debug(f"Allowed and copied from os.environ: {var_name}={safe_env[var_name]}")
                else:
                    logger.warning(f"Allowed environment variable '{var_name}' not found in system environment.")
        else:
            logger.debug("No specific environment variables allowed by (caller-provided) allowed_env_vars list.")

        # Ensure essential variables have safe defaults if not explicitly allowed and set from os.environ
        if 'PATH' not in safe_env:
            safe_env['PATH'] = '/usr/bin:/bin'
            logger.debug("Default PATH set for safe execution.")
        
        if 'HOME' not in safe_env:
            safe_env['HOME'] = os.path.expanduser('~')
            logger.debug(f"Default HOME set: {safe_env['HOME']}")

        logger.info(f"Environment scrubbed successfully. Final environment contains {len(safe_env)} variables.")
        return safe_env 