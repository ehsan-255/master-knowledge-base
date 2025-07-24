#!/usr/bin/env python3
"""
Run Command Action Plugin (Legacy Version)

This is the original version before HMA v2.2 ports-and-adapters conversion.
Kept for reference and backward compatibility testing.
"""

import re
from typing import Dict, Any, List
from pathlib import Path

from .base import BaseAction, ActionExecutionError, validate_required_params
from tools.scribe.core.security_manager import SecurityManager, SecurityViolation
from tools.scribe.core.logging_config import get_scribe_logger

logger = get_scribe_logger(__name__)


class RunCommandActionLegacy(BaseAction):
    """Legacy version of Run Command Action using direct dependencies."""
    
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
        """Validate parameters for the run command action."""
        # Legacy validation logic here...
        return True
    
    def execute(self, 
                file_content: str, 
                match: re.Match, 
                file_path: str, 
                params: Dict[str, Any]) -> str:
        """Execute a system command safely (legacy version)."""
        # Legacy execution logic here...
        return file_content