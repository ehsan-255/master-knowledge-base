#!/usr/bin/env python3
"""
Scribe Actions Package

This package contains all action plugins for the Scribe automation engine.
Action plugins implement the L3 Capability Plugin layer in the HMA architecture.
"""

from .base import BaseAction, ActionExecutionError, ValidationError
from .base import get_match_context, validate_required_params, apply_default_params
from .run_command_action import RunCommandAction
from .enhanced_frontmatter_action import EnhancedFrontmatterAction
from .graph_validation_action import GraphValidationAction
from .naming_enforcement_action import NamingEnforcementAction
from .reconciliation_action import ReconciliationAction
from .roadmap_populator_action import RoadmapPopulatorAction
from .view_generation_action import ViewGenerationAction


__all__ = [
    'BaseAction',
    'ActionExecutionError', 
    'ValidationError',
    'get_match_context',
    'validate_required_params',
    'apply_default_params',
    'RunCommandAction',
    'EnhancedFrontmatterAction',
    'GraphValidationAction',
    'NamingEnforcementAction',
    'ReconciliationAction',
    'RoadmapPopulatorAction',
    'ViewGenerationAction',
]

__version__ = "1.0.0" 