#!/usr/bin/env python3
"""
Scribe Frontmatter Parser Utility

Consolidated YAML frontmatter parsing functionality for use across
action plugins. Provides standardized parsing with error handling
and preprocessing for special keys.
"""

import yaml
import re
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def parse_frontmatter(content: str) -> Optional[Dict[str, Any]]:
    """
    Parse YAML frontmatter from document content.
    
    Handles both standard YAML frontmatter and special preprocessing
    for keys starting with @ symbols.
    
    Args:
        content: Document content that may contain frontmatter
        
    Returns:
        Dictionary of frontmatter data or None if not found/invalid
    """
    frontmatter_str = _extract_frontmatter_block(content)
    if not frontmatter_str:
        return None
    
    try:
        # Preprocess for keys starting with @ (common in JSON-LD contexts)
        processed_frontmatter_str = _preprocess_special_keys(frontmatter_str)
        
        # Parse YAML
        frontmatter_data = yaml.safe_load(processed_frontmatter_str)
        
        # Ensure we return a dict (not None, string, etc.)
        return frontmatter_data if isinstance(frontmatter_data, dict) else None
        
    except yaml.YAMLError as e:
        logger.warning(f"Could not parse frontmatter as YAML: {e}")
        return None
    except Exception as e:
        logger.warning(f"Unexpected error parsing frontmatter: {e}")
        return None


def _extract_frontmatter_block(content: str) -> Optional[str]:
    """
    Extract the raw frontmatter block from document content.
    
    Looks for YAML frontmatter delimited by --- markers.
    
    Args:
        content: Document content
        
    Returns:
        Raw frontmatter string or None if not found
    """
    if not content.strip().startswith('---'):
        return None
    
    # Find the end marker
    end_marker = content.find('---', 4)  # Start search after first ---
    if end_marker == -1:
        return None
    
    # Extract frontmatter content between markers
    frontmatter_str = content[4:end_marker].strip()
    return frontmatter_str if frontmatter_str else None


def _preprocess_special_keys(frontmatter_str: str) -> str:
    """
    Preprocess frontmatter to handle special key formats.
    
    Specifically handles keys starting with @ by quoting them
    for proper YAML parsing (common in JSON-LD contexts).
    
    Args:
        frontmatter_str: Raw frontmatter string
        
    Returns:
        Preprocessed frontmatter string
    """
    processed_lines = []
    
    for line in frontmatter_str.splitlines():
        # Check if line starts with @ and contains a colon
        if line.strip().startswith('@') and ':' in line:
            # Split on first colon
            key_part, value_part = line.split(':', 1)
            key = key_part.strip()
            value = value_part.strip()
            
            # Quote the key to make it valid YAML
            processed_lines.append(f'"{key}": {value}')
        else:
            processed_lines.append(line)
    
    return "\n".join(processed_lines)


def has_frontmatter(content: str) -> bool:
    """
    Check if content contains YAML frontmatter.
    
    Args:
        content: Document content to check
        
    Returns:
        True if frontmatter is present, False otherwise
    """
    return _extract_frontmatter_block(content) is not None


def remove_frontmatter(content: str) -> str:
    """
    Remove frontmatter from document content.
    
    Args:
        content: Document content that may contain frontmatter
        
    Returns:
        Content with frontmatter removed
    """
    if not content.strip().startswith('---'):
        return content
    
    # Find the end marker
    end_marker = content.find('---', 4)
    if end_marker == -1:
        return content
    
    # Return content after the closing ---
    remaining_content = content[end_marker + 3:]
    return remaining_content.lstrip('\n')


def apply_frontmatter(content: str, frontmatter: Dict[str, Any]) -> str:
    """
    Apply frontmatter to document content.
    
    Replaces existing frontmatter if present, or adds new frontmatter
    to the beginning of the document.
    
    Args:
        content: Document content
        frontmatter: Dictionary of frontmatter data
        
    Returns:
        Content with frontmatter applied
    """
    # Convert frontmatter to YAML
    frontmatter_yaml = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
    
    # Remove existing frontmatter if present
    content_without_frontmatter = remove_frontmatter(content)
    
    # Add new frontmatter
    return f"---\n{frontmatter_yaml}---\n\n{content_without_frontmatter.lstrip()}"