#!/usr/bin/env python3
"""
Run Command Action Plugin

Executes system commands safely using the SecurityManager.
This action demonstrates the list-based command execution pattern.
"""

import re
from typing import Dict, Any, List
from pathlib import Path

from .base import BaseAction, ActionExecutionError, validate_required_params
from core.security_manager import SecurityManager, SecurityViolation
from core.logging_config import get_scribe_logger

logger = get_scribe_logger(__name__)


class RunCommandAction(BaseAction):
    """
    Action plugin that executes system commands safely.
    
    This action uses the SecurityManager to execute commands with proper
    security restrictions and uses list-based command format to prevent
    shell injection attacks.
    """
    
    def __init__(self, security_manager: SecurityManager):
        """
        Initialize the run command action.
        
        Args:
            security_manager: SecurityManager instance for safe command execution
        """
        super().__init__("run_command")
        self.security_manager = security_manager
        
    def get_required_params(self) -> List[str]:
        """Get required parameters for this action."""
        return ["command"]
    
    def get_optional_params(self) -> Dict[str, Any]:
        """Get optional parameters and their defaults."""
        return {
            "cwd": None,
            "timeout": 30,
            "allowed_env_vars": []
        }
    
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """
        Validate parameters for the run command action.
        
        Args:
            params: Parameters to validate
            
        Returns:
            True if parameters are valid
            
        Raises:
            ActionExecutionError: If parameters are invalid
        """
        try:
            # Validate required parameters
            validate_required_params(params, self.get_required_params(), self.action_type)
            
            # Validate command is a list
            command = params.get("command")
            if not isinstance(command, list):
                raise ActionExecutionError(
                    self.action_type, 
                    f"Command must be a list of strings, got {type(command).__name__}"
                )
            
            if len(command) == 0:
                raise ActionExecutionError(
                    self.action_type, 
                    "Command list cannot be empty"
                )
            
            # Validate all command elements are strings
            for i, cmd_part in enumerate(command):
                if not isinstance(cmd_part, str):
                    raise ActionExecutionError(
                        self.action_type,
                        f"Command element {i} must be a string, got {type(cmd_part).__name__}"
                    )
            
            # Validate timeout
            timeout = params.get("timeout", 30)
            if not isinstance(timeout, int) or timeout <= 0:
                raise ActionExecutionError(
                    self.action_type,
                    f"Timeout must be a positive integer, got {timeout}"
                )
            
            # Validate working directory if provided
            cwd = params.get("cwd")
            if cwd is not None:
                if not isinstance(cwd, str):
                    raise ActionExecutionError(
                        self.action_type,
                        f"Working directory must be a string, got {type(cwd).__name__}"
                    )
                
                cwd_path = Path(cwd)
                if not cwd_path.exists():
                    raise ActionExecutionError(
                        self.action_type,
                        f"Working directory does not exist: {cwd}"
                    )
                
                if not cwd_path.is_dir():
                    raise ActionExecutionError(
                        self.action_type,
                        f"Working directory is not a directory: {cwd}"
                    )
            
            return True
            
        except ActionExecutionError:
            raise
        except Exception as e:
            raise ActionExecutionError(
                self.action_type,
                f"Parameter validation failed: {e}"
            )
    
    def execute(self, 
                file_content: str, 
                match: re.Match, 
                file_path: str, 
                params: Dict[str, Any]) -> str:
        """
        Execute a system command safely.
        
        Args:
            file_content: The full content of the file being processed
            match: The regex match object that triggered the rule
            file_path: The path to the file being processed
            params: Action parameters including command list
            
        Returns:
            The original file content (this action doesn't modify files)
            
        Raises:
            ActionExecutionError: If command execution fails
        """
        try:
            # Validate parameters
            self.validate_params(params)
            
            # Extract parameters
            command_list = params["command"]
            cwd = params.get("cwd")
            timeout = params.get("timeout", 30)
            
            self.logger.info("Executing command",
                           command=command_list,
                           file_path=file_path,
                           cwd=cwd,
                           timeout=timeout)
            
            # Execute command safely
            success, stdout, stderr = self.security_manager.execute_command_safely(
                command_list=command_list,
                cwd=cwd,
                timeout=timeout
            )
            
            if success:
                self.logger.info("Command executed successfully",
                               command=command_list,
                               stdout_length=len(stdout),
                               stderr_length=len(stderr))
            else:
                self.logger.warning("Command execution failed",
                                  command=command_list,
                                  stdout=stdout,
                                  stderr=stderr)
                
                # Optionally raise an error on command failure
                # This can be controlled by a parameter in the future
                raise ActionExecutionError(
                    self.action_type,
                    f"Command failed with stderr: {stderr}"
                )
            
            # Return original content (this action doesn't modify files)
            return file_content
            
        except SecurityViolation as e:
            self.logger.error("Security violation during command execution",
                            command=params.get("command"),
                            violation_type=e.violation_type,
                            error=str(e))
            raise ActionExecutionError(
                self.action_type,
                f"Security violation: {e}"
            )
        
        except ActionExecutionError:
            raise
            
        except Exception as e:
            self.logger.error("Unexpected error during command execution",
                            command=params.get("command"),
                            error=str(e),
                            exc_info=True)
            raise ActionExecutionError(
                self.action_type,
                f"Unexpected error: {e}"
            )
    
    def get_description(self) -> str:
        """Get description of this action."""
        return "Executes system commands safely using list-based command format" 