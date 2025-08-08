#!/usr/bin/env python3
"""
Run Command Action Plugin (HMA v2.2 Compliant)

Executes system commands safely using port-based access.
This action demonstrates the HMA v2.2 ports-and-adapters-only pattern.
"""

import re
from typing import Dict, Any, List
from pathlib import Path

from .base import BaseAction, ActionExecutionError, validate_required_params


class RunCommandAction(BaseAction):
    """
    Action plugin that executes system commands safely using HMA v2.2 ports.
    
    This action uses the CommandExecutionPort to execute commands with proper
    security restrictions and uses list-based command format to prevent
    shell injection attacks.
    
    HMA v2.2 Compliance: All functionality accessed through registered ports.
    """
        
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
    
    async def execute(self, 
                      file_content: str, 
                      match: re.Match, 
                      file_path: str, 
                      params: Dict[str, Any]) -> str:
        """
        Execute a system command safely using HMA v2.2 ports.
        
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
            allowed_env_vars = params.get("allowed_env_vars")
            
            # Log command execution using logging port
            self.log_port.log_info("Executing command via port",
                                  command=command_list,
                                  file_path=file_path,
                                  cwd=cwd,
                                  timeout=timeout,
                                  plugin_id=self.context.get_plugin_id())
            
            # Execute command safely through command execution port
            success, stdout, stderr = await self.execute_command_safely(
                command_list=command_list,
                cwd=cwd,
                timeout=timeout,
                allowed_env_vars=allowed_env_vars
            )
            
            if success:
                self.log_port.log_info("Command executed successfully via port",
                                      command=command_list,
                                      stdout_length=len(stdout),
                                      stderr_length=len(stderr))
                
                # Publish success event
                await self.publish_event(
                    "command_executed",
                    {
                        "command": command_list,
                        "success": True,
                        "file_path": file_path,
                        "plugin_id": self.context.get_plugin_id()
                    }
                )
            else:
                self.log_port.log_warning("Command execution failed via port",
                                         command=command_list,
                                         stdout=stdout,
                                         stderr=stderr)
                
                # Publish failure event
                await self.publish_event(
                    "command_failed",
                    {
                        "command": command_list,
                        "success": False,
                        "error": stderr,
                        "file_path": file_path,
                        "plugin_id": self.context.get_plugin_id()
                    }
                )
                
                # Optionally raise an error on command failure
                raise ActionExecutionError(
                    self.action_type,
                    f"Command failed with stderr: {stderr}"
                )
            
            # Return original content (this action doesn't modify files)
            return file_content
            
        except ActionExecutionError:
            raise
            
        except Exception as e:
            self.log_port.log_error("Unexpected error during command execution",
                                   command=params.get("command"),
                                   error=str(e),
                                   plugin_id=self.context.get_plugin_id())
            
            # Publish error event
            await self.publish_event(
                "command_error",
                {
                    "command": params.get("command"),
                    "error": str(e),
                    "file_path": file_path,
                    "plugin_id": self.context.get_plugin_id()
                }
            )
            
            raise ActionExecutionError(
                self.action_type,
                f"Unexpected error: {e}"
            )
    
    def get_description(self) -> str:
        """Get description of this action."""
        return "Executes system commands safely using list-based command format" 