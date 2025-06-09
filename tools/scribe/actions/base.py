#!/usr/bin/env python3
"""
Scribe BaseAction - Abstract Base Class for Action Plugins

This module defines the Port contract that all Scribe action plugins must implement.
It follows the Hexagonal Architecture pattern where this abstract class serves as
the Port interface for L3 Capability Plugins.
"""

import re
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import structlog

# Import logging from the core module
from core.logging_config import get_scribe_logger

logger = get_scribe_logger(__name__)


class BaseAction(ABC):
    """
    Abstract base class for all Scribe action plugins.
    
    This class defines the Port contract in the Hexagonal Architecture.
    All action plugins must inherit from this class and implement the execute() method.
    
    The execute() method receives:
    - file_content: The full content of the file being processed
    - match: The regex match object that triggered the rule
    - file_path: The path to the file being processed
    - params: A dictionary of parameters from the rule's action config
    
    And must return:
    - The modified file content (or original content if no changes)
    """
    
    def __init__(self, action_type: str):
        """
        Initialize the base action.
        
        Args:
            action_type: The type identifier for this action
        """
        self.action_type = action_type
        self.logger = get_scribe_logger(f"{__name__}.{self.__class__.__name__}")
        
        self.logger.debug("Action plugin initialized", action_type=action_type)
    
    @abstractmethod
    def execute(self, 
                file_content: str, 
                match: re.Match, 
                file_path: str, 
                params: Dict[str, Any]) -> str:
        """
        Execute the action on the matched content.
        
        This is the core method that all action plugins must implement.
        It defines the contract for how actions process file content.
        
        Args:
            file_content: The full content of the file being processed
            match: The regex match object that triggered the rule
            file_path: The path to the file being processed
            params: A dictionary of parameters from the rule's action config
            
        Returns:
            The modified file content. If no changes are made, return the original content.
            
        Raises:
            ActionExecutionError: If the action fails to execute
            ValidationError: If the parameters are invalid
        """
        pass
    
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """
        Validate the parameters for this action.
        
        This method can be overridden by subclasses to provide parameter validation.
        The default implementation returns True (no validation).
        
        Args:
            params: The parameters to validate
            
        Returns:
            True if parameters are valid, False otherwise
        """
        return True
    
    def get_required_params(self) -> list[str]:
        """
        Get the list of required parameter names for this action.
        
        This method can be overridden by subclasses to specify required parameters.
        The default implementation returns an empty list.
        
        Returns:
            List of required parameter names
        """
        return []
    
    def get_optional_params(self) -> Dict[str, Any]:
        """
        Get the optional parameters and their default values for this action.
        
        This method can be overridden by subclasses to specify optional parameters.
        The default implementation returns an empty dictionary.
        
        Returns:
            Dictionary of optional parameter names and their default values
        """
        return {}
    
    def get_description(self) -> str:
        """
        Get a human-readable description of what this action does.
        
        This method can be overridden by subclasses to provide documentation.
        The default implementation returns a generic description.
        
        Returns:
            Description of the action
        """
        return f"Action plugin of type '{self.action_type}'"
    
    def pre_execute(self, 
                   file_content: str, 
                   match: re.Match, 
                   file_path: str, 
                   params: Dict[str, Any]) -> None:
        """
        Hook called before execute() is run.
        
        This method can be overridden by subclasses to perform setup operations.
        The default implementation does nothing.
        
        Args:
            file_content: The full content of the file being processed
            match: The regex match object that triggered the rule
            file_path: The path to the file being processed
            params: A dictionary of parameters from the rule's action config
        """
        pass
    
    def post_execute(self, 
                    file_content: str, 
                    modified_content: str,
                    match: re.Match, 
                    file_path: str, 
                    params: Dict[str, Any]) -> None:
        """
        Hook called after execute() is run.
        
        This method can be overridden by subclasses to perform cleanup operations.
        The default implementation does nothing.
        
        Args:
            file_content: The original content of the file
            modified_content: The content returned by execute()
            match: The regex match object that triggered the rule
            file_path: The path to the file being processed
            params: A dictionary of parameters from the rule's action config
        """
        pass
    
    def __str__(self) -> str:
        """String representation of the action."""
        return f"{self.__class__.__name__}(type='{self.action_type}')"
    
    def __repr__(self) -> str:
        """Detailed string representation of the action."""
        return f"{self.__class__.__name__}(action_type='{self.action_type}')"


class ActionExecutionError(Exception):
    """Exception raised when an action fails to execute."""
    
    def __init__(self, action_type: str, message: str, original_error: Optional[Exception] = None):
        """
        Initialize the exception.
        
        Args:
            action_type: The type of action that failed
            message: Error message
            original_error: The original exception that caused this error
        """
        self.action_type = action_type
        self.original_error = original_error
        
        if original_error:
            super().__init__(f"Action '{action_type}' failed: {message} (caused by: {original_error})")
        else:
            super().__init__(f"Action '{action_type}' failed: {message}")


class ValidationError(Exception):
    """Exception raised when action parameters are invalid."""
    
    def __init__(self, action_type: str, param_name: str, message: str):
        """
        Initialize the exception.
        
        Args:
            action_type: The type of action with invalid parameters
            param_name: The name of the invalid parameter
            message: Error message
        """
        self.action_type = action_type
        self.param_name = param_name
        super().__init__(f"Invalid parameter '{param_name}' for action '{action_type}': {message}")


# Utility functions for action plugins

def get_match_context(content: str, match: re.Match, context_lines: int = 2) -> Dict[str, Any]:
    """
    Get context around a regex match for debugging/logging.
    
    Args:
        content: The full file content
        match: The regex match object
        context_lines: Number of lines before/after to include
        
    Returns:
        Dictionary with match context information
    """
    lines = content.split('\n')
    match_text = match.group(0)
    
    # Find which line the match is on
    match_line_num = content[:match.start()].count('\n')
    
    # Get context lines
    start_line = max(0, match_line_num - context_lines)
    end_line = min(len(lines), match_line_num + context_lines + 1)
    
    return {
        'match_text': match_text,
        'match_line': match_line_num + 1,  # 1-based line numbers
        'match_start': match.start(),
        'match_end': match.end(),
        'context_lines': lines[start_line:end_line],
        'groups': match.groups() if match.groups() else None,
        'groupdict': match.groupdict() if match.groupdict() else None
    }


def validate_required_params(params: Dict[str, Any], required: list[str], action_type: str) -> None:
    """
    Validate that all required parameters are present.
    
    Args:
        params: The parameters to validate
        required: List of required parameter names
        action_type: The action type for error messages
        
    Raises:
        ValidationError: If any required parameter is missing
    """
    for param_name in required:
        if param_name not in params:
            raise ValidationError(action_type, param_name, "Required parameter is missing")
        
        if params[param_name] is None:
            raise ValidationError(action_type, param_name, "Required parameter cannot be None")


def apply_default_params(params: Dict[str, Any], defaults: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply default values to parameters.
    
    Args:
        params: The original parameters
        defaults: Dictionary of default values
        
    Returns:
        New dictionary with defaults applied
    """
    result = defaults.copy()
    result.update(params)
    return result 