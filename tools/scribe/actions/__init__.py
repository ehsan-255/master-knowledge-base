#!/usr/bin/env python3
"""
Scribe Actions Package

This package contains all action plugins for the Scribe automation engine.
Action plugins implement the L3 Capability Plugin layer in the HMA architecture.
"""

from .base import BaseAction, ActionExecutionError, ValidationError
from .base import get_match_context, validate_required_params, apply_default_params

__all__ = [
    'BaseAction',
    'ActionExecutionError', 
    'ValidationError',
    'get_match_context',
    'validate_required_params',
    'apply_default_params'
]

__version__ = "1.0.0" 