#!/usr/bin/env python3
"""
Scribe Rule Processor

Handles rule matching logic and file content processing.
Implements efficient regex matching with pre-compiled patterns.
"""

import re
import fnmatch
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Iterator
import structlog

from .logging_config import get_scribe_logger
from .config_manager import ConfigManager

logger = get_scribe_logger(__name__)


class CompiledRule:
    """A rule with pre-compiled regex pattern for efficient matching."""
    
    def __init__(self, rule_dict: Dict[str, Any]):
        """
        Initialize a compiled rule.
        
        Args:
            rule_dict: Rule configuration dictionary
        """
        self.id = rule_dict['id']
        self.name = rule_dict['name']
        self.enabled = rule_dict['enabled']
        self.file_glob = rule_dict['file_glob']
        self.trigger_pattern = rule_dict['trigger_pattern']
        self.actions = rule_dict['actions']
        self.error_handling = rule_dict.get('error_handling', {})
        
        # Pre-compile the regex pattern
        try:
            self.compiled_pattern = re.compile(self.trigger_pattern, re.MULTILINE)
            logger.debug("Rule pattern compiled successfully",
                        rule_id=self.id,
                        pattern=self.trigger_pattern)
        except re.error as e:
            logger.error("Failed to compile rule pattern",
                        rule_id=self.id,
                        pattern=self.trigger_pattern,
                        error=str(e))
            raise ValueError(f"Invalid regex pattern in rule {self.id}: {e}")
    
    def matches_file_path(self, file_path: str) -> bool:
        """
        Check if the file path matches this rule's file glob pattern.
        
        Args:
            file_path: Path to the file to check
            
        Returns:
            True if the file path matches the glob pattern
        """
        try:
            # Convert to Path object for consistent handling
            path_obj = Path(file_path)
            
            # Use fnmatch for glob pattern matching
            # Check both the full path and just the filename
            full_path_str = str(path_obj).replace('\\', '/')  # Normalize path separators
            filename = path_obj.name
            
            # Try matching against full path first, then filename
            matches_full = fnmatch.fnmatch(full_path_str, self.file_glob)
            matches_name = fnmatch.fnmatch(filename, self.file_glob)
            
            result = matches_full or matches_name
            
            if result:
                logger.debug("File path matches rule glob",
                           rule_id=self.id,
                           file_path=file_path,
                           glob_pattern=self.file_glob)
            
            return result
            
        except Exception as e:
            logger.error("Error matching file path against glob pattern",
                        rule_id=self.id,
                        file_path=file_path,
                        glob_pattern=self.file_glob,
                        error=str(e))
            return False
    
    def find_matches(self, content: str) -> Iterator[re.Match]:
        """
        Find all matches of this rule's pattern in the given content.
        
        Args:
            content: File content to search
            
        Yields:
            Match objects for each occurrence of the pattern
        """
        try:
            for match in self.compiled_pattern.finditer(content):
                logger.debug("Pattern match found",
                           rule_id=self.id,
                           match_start=match.start(),
                           match_end=match.end(),
                           matched_text=match.group(0)[:100])  # Limit log output
                yield match
                
        except Exception as e:
            logger.error("Error finding pattern matches",
                        rule_id=self.id,
                        error=str(e),
                        exc_info=True)
    
    def __repr__(self) -> str:
        return f"CompiledRule(id='{self.id}', enabled={self.enabled})"


class RuleMatch:
    """Represents a successful rule match with context."""
    
    def __init__(self, rule: CompiledRule, match: re.Match, file_path: str, file_content: str):
        """
        Initialize a rule match.
        
        Args:
            rule: The rule that matched
            match: The regex match object
            file_path: Path to the file that matched
            file_content: Full content of the file
        """
        self.rule = rule
        self.match = match
        self.file_path = file_path
        self.file_content = file_content
        self.timestamp = None  # Will be set by processor
    
    def get_match_context(self, context_lines: int = 2) -> Dict[str, Any]:
        """
        Get context around the match for debugging/logging.
        
        Args:
            context_lines: Number of lines before/after to include
            
        Returns:
            Dictionary with match context information
        """
        lines = self.file_content.split('\n')
        match_text = self.match.group(0)
        
        # Find which line the match is on
        match_line_num = self.file_content[:self.match.start()].count('\n')
        
        # Get context lines
        start_line = max(0, match_line_num - context_lines)
        end_line = min(len(lines), match_line_num + context_lines + 1)
        
        context = {
            'rule_id': self.rule.id,
            'file_path': self.file_path,
            'match_text': match_text,
            'match_line': match_line_num + 1,  # 1-based line numbers
            'match_start': self.match.start(),
            'match_end': self.match.end(),
            'context_lines': lines[start_line:end_line],
            'groups': self.match.groups() if self.match.groups() else None
        }
        
        return context
    
    def __repr__(self) -> str:
        return f"RuleMatch(rule_id='{self.rule.id}', file='{self.file_path}')"


class RuleProcessor:
    """
    Processes files against configured rules to find matches.
    
    Handles rule compilation, file path matching, and content pattern matching
    with efficient pre-compiled regex patterns.
    """
    
    def __init__(self, config_manager: ConfigManager):
        """
        Initialize the rule processor.
        
        Args:
            config_manager: Configuration manager instance
        """
        self.config_manager = config_manager
        self._compiled_rules: List[CompiledRule] = []
        
        # Register for configuration changes
        self.config_manager.add_change_callback(self._on_config_change)
        
        # Initial rule compilation
        self._compile_rules()
        
        logger.info("RuleProcessor initialized",
                   rules_count=len(self._compiled_rules))
    
    def _compile_rules(self) -> None:
        """Compile all rules from the current configuration."""
        try:
            rules = self.config_manager.get_rules()
            compiled_rules = []
            
            for rule_dict in rules:
                try:
                    compiled_rule = CompiledRule(rule_dict)
                    compiled_rules.append(compiled_rule)
                except Exception as e:
                    logger.error("Failed to compile rule",
                                rule_id=rule_dict.get('id', 'unknown'),
                                error=str(e))
                    # Continue with other rules
            
            self._compiled_rules = compiled_rules
            
            enabled_count = sum(1 for rule in self._compiled_rules if rule.enabled)
            logger.info("Rules compiled successfully",
                       total_rules=len(self._compiled_rules),
                       enabled_rules=enabled_count)
            
        except Exception as e:
            logger.error("Failed to compile rules", error=str(e), exc_info=True)
            self._compiled_rules = []
    
    def _on_config_change(self, new_config: Dict[str, Any]) -> None:
        """Handle configuration changes by recompiling rules."""
        logger.info("Configuration changed, recompiling rules")
        self._compile_rules()
    
    def get_matching_rules(self, file_path: str) -> List[CompiledRule]:
        """
        Get all enabled rules that match the given file path.
        
        Args:
            file_path: Path to the file to check
            
        Returns:
            List of rules that match the file path
        """
        matching_rules = []
        
        for rule in self._compiled_rules:
            if not rule.enabled:
                continue
                
            if rule.matches_file_path(file_path):
                matching_rules.append(rule)
        
        if matching_rules:
            logger.debug("Found matching rules for file",
                        file_path=file_path,
                        matching_rule_ids=[rule.id for rule in matching_rules])
        
        return matching_rules
    
    def process_file(self, file_path: str, file_content: str) -> List[RuleMatch]:
        """
        Process a file against all applicable rules.
        
        Args:
            file_path: Path to the file being processed
            file_content: Content of the file
            
        Returns:
            List of rule matches found in the file
        """
        matches = []
        
        try:
            # Get rules that match this file path
            matching_rules = self.get_matching_rules(file_path)
            
            if not matching_rules:
                logger.debug("No rules match file path", file_path=file_path)
                return matches
            
            # Process each matching rule
            for rule in matching_rules:
                try:
                    # Find all pattern matches in the content
                    for regex_match in rule.find_matches(file_content):
                        rule_match = RuleMatch(rule, regex_match, file_path, file_content)
                        matches.append(rule_match)
                        
                        logger.info("Rule match found",
                                   rule_id=rule.id,
                                   file_path=file_path,
                                   match_line=rule_match.get_match_context()['match_line'])
                
                except Exception as e:
                    logger.error("Error processing rule against file",
                                rule_id=rule.id,
                                file_path=file_path,
                                error=str(e),
                                exc_info=True)
            
            if matches:
                logger.info("File processing complete",
                           file_path=file_path,
                           total_matches=len(matches),
                           matched_rule_ids=[match.rule.id for match in matches])
            
        except Exception as e:
            logger.error("Error processing file",
                        file_path=file_path,
                        error=str(e),
                        exc_info=True)
        
        return matches
    
    def get_rule_by_id(self, rule_id: str) -> Optional[CompiledRule]:
        """
        Get a compiled rule by its ID.
        
        Args:
            rule_id: The rule ID to search for
            
        Returns:
            The compiled rule if found, None otherwise
        """
        for rule in self._compiled_rules:
            if rule.id == rule_id:
                return rule
        return None
    
    def get_enabled_rules(self) -> List[CompiledRule]:
        """Get all enabled compiled rules."""
        return [rule for rule in self._compiled_rules if rule.enabled]
    
    def get_all_rules(self) -> List[CompiledRule]:
        """Get all compiled rules (enabled and disabled)."""
        return self._compiled_rules.copy()
    
    def validate_rule_pattern(self, pattern: str) -> Tuple[bool, Optional[str]]:
        """
        Validate a regex pattern without compiling a full rule.
        
        Args:
            pattern: Regex pattern to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            re.compile(pattern, re.MULTILINE)
            return True, None
        except re.error as e:
            return False, str(e)
    
    def stop(self) -> None:
        """Stop the rule processor and cleanup resources."""
        # Remove configuration change callback
        self.config_manager.remove_change_callback(self._on_config_change)
        
        logger.info("RuleProcessor stopped")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop() 