#!/usr/bin/env python3
"""
Unit tests for the Scribe SecurityManager.

These tests verify the security manager functionality, particularly
the critical shell=False requirement for TASK 1.2.1.
"""

import unittest
import tempfile
import os
import sys
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Import scribe modules using the installed package

from core.security_manager import SecurityManager, SecurityViolation
from core.config_manager import ConfigManager


class TestSecurityManager(unittest.TestCase):
    """Test the SecurityManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directory for test config
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        
        # Create mock config manager
        self.mock_config_manager = Mock(spec=ConfigManager)
        self.mock_config_manager.get_security_settings.return_value = {
            'allowed_commands': ['git', 'echo', 'ls'],
            'restricted_paths': ['.git/', 'node_modules/'],
            'dangerous_patterns': []
        }
        
        # Create security manager instance
        self.security_manager = SecurityManager(self.mock_config_manager)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
        if hasattr(self, 'security_manager'):
            self.security_manager.stop()
    
    def test_security_manager_initialization(self):
        """Test that security manager initializes correctly."""
        self.assertIsNotNone(self.security_manager)
        self.assertEqual(self.security_manager._allowed_commands, {'git', 'echo', 'ls'})
        self.assertEqual(self.security_manager._restricted_paths, ['.git/', 'node_modules/'])
    
    def test_validate_command_allowed(self):
        """Test command validation for allowed commands."""
        # Test allowed command
        is_valid, reason = self.security_manager.validate_command('git')
        self.assertTrue(is_valid)
        self.assertIsNone(reason)
        
        # Test allowed command with path
        is_valid, reason = self.security_manager.validate_command('/usr/bin/git')
        self.assertTrue(is_valid)
        self.assertIsNone(reason)
    
    def test_validate_command_not_allowed(self):
        """Test command validation for disallowed commands."""
        is_valid, reason = self.security_manager.validate_command('rm')
        self.assertFalse(is_valid)
        self.assertIn("not in the allowed commands list", reason)
    
    def test_validate_command_empty(self):
        """Test command validation for empty commands."""
        is_valid, reason = self.security_manager.validate_command('')
        self.assertFalse(is_valid)
        self.assertEqual(reason, "Empty command not allowed")
        
        is_valid, reason = self.security_manager.validate_command(None)
        self.assertFalse(is_valid)
        self.assertEqual(reason, "Empty command not allowed")
    
    @patch('core.security_manager.subprocess.run')
    def test_execute_command_safely_uses_shell_false(self, mock_subprocess_run):
        """
        CRITICAL TEST for TASK 1.2.1: Verify that execute_command_safely 
        uses shell=False and accepts list-based commands.
        """
        # Setup mock subprocess result
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "test output"
        mock_result.stderr = ""
        mock_subprocess_run.return_value = mock_result
        
        # Test command as list
        command_list = ["git", "status"]
        
        # Execute command
        success, stdout, stderr = self.security_manager.execute_command_safely(command_list)
        
        # CRITICAL ASSERTION: Verify subprocess.run was called with shell=False
        mock_subprocess_run.assert_called_once()
        call_args = mock_subprocess_run.call_args
        
        # Verify command_list was passed directly (not as string)
        self.assertEqual(call_args[0][0], command_list)
        
        # CRITICAL: Verify shell=False was used
        self.assertIn('shell', call_args[1])
        self.assertFalse(call_args[1]['shell'], "SecurityManager MUST use shell=False")
        
        # Verify other security parameters
        self.assertIn('env', call_args[1])  # Environment should be scrubbed
        self.assertIn('capture_output', call_args[1])
        self.assertTrue(call_args[1]['capture_output'])
        self.assertIn('text', call_args[1])
        self.assertTrue(call_args[1]['text'])
        
        # Verify return values
        self.assertTrue(success)
        self.assertEqual(stdout, "test output")
        self.assertEqual(stderr, "")
    
    def test_execute_command_safely_empty_list(self):
        """Test that empty command list raises SecurityViolation."""
        with self.assertRaises(SecurityViolation) as context:
            self.security_manager.execute_command_safely([])
        
        self.assertEqual(context.exception.violation_type, "command_validation")
        self.assertIn("Empty command list not allowed", str(context.exception))
    
    def test_execute_command_safely_invalid_command(self):
        """Test that invalid command raises SecurityViolation."""
        with self.assertRaises(SecurityViolation) as context:
            self.security_manager.execute_command_safely(["rm", "-rf", "/"])
        
        self.assertEqual(context.exception.violation_type, "command_validation")
        self.assertIn("not in the allowed commands list", str(context.exception))
    
    @patch('core.security_manager.subprocess.run')
    def test_execute_command_safely_with_cwd(self, mock_subprocess_run):
        """Test command execution with working directory."""
        # Setup mock subprocess result
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "test output"
        mock_result.stderr = ""
        mock_subprocess_run.return_value = mock_result
        
        # Create test directory
        test_cwd = self.temp_path / "test_cwd"
        test_cwd.mkdir()
        
        # Execute command with cwd
        command_list = ["git", "status"]
        success, stdout, stderr = self.security_manager.execute_command_safely(
            command_list, 
            cwd=str(test_cwd)
        )
        
        # Verify subprocess.run was called with correct cwd
        mock_subprocess_run.assert_called_once()
        call_args = mock_subprocess_run.call_args
        self.assertEqual(call_args[1]['cwd'], str(test_cwd))
        
        # Still verify shell=False
        self.assertFalse(call_args[1]['shell'])
    
    @patch('core.security_manager.subprocess.run')
    def test_execute_command_safely_timeout(self, mock_subprocess_run):
        """Test command execution with custom timeout."""
        # Setup mock subprocess result
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "test output"
        mock_result.stderr = ""
        mock_subprocess_run.return_value = mock_result
        
        # Execute command with custom timeout
        command_list = ["git", "status"]
        success, stdout, stderr = self.security_manager.execute_command_safely(
            command_list, 
            timeout=60
        )
        
        # Verify subprocess.run was called with correct timeout
        mock_subprocess_run.assert_called_once()
        call_args = mock_subprocess_run.call_args
        self.assertEqual(call_args[1]['timeout'], 60)
        
        # Still verify shell=False
        self.assertFalse(call_args[1]['shell'])
    
    @patch('core.security_manager.subprocess.run')
    def test_execute_command_safely_command_failure(self, mock_subprocess_run):
        """Test handling of command execution failure."""
        # Setup mock subprocess result for failed command
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "error message"
        mock_subprocess_run.return_value = mock_result
        
        # Execute command that fails
        command_list = ["git", "status"]
        success, stdout, stderr = self.security_manager.execute_command_safely(command_list)
        
        # Verify failure is handled correctly
        self.assertFalse(success)
        self.assertEqual(stdout, "")
        self.assertEqual(stderr, "error message")
        
        # Still verify shell=False was used
        mock_subprocess_run.assert_called_once()
        call_args = mock_subprocess_run.call_args
        self.assertFalse(call_args[1]['shell'])
    
    def test_validate_path_allowed(self):
        """Test path validation for allowed paths."""
        # Create test file
        test_file = self.temp_path / "test.txt"
        test_file.write_text("test content")
        
        is_valid, reason = self.security_manager.validate_path(str(test_file))
        self.assertTrue(is_valid)
        self.assertIsNone(reason)
    
    def test_validate_path_restricted(self):
        """Test path validation for restricted paths."""
        # Test restricted path
        is_valid, reason = self.security_manager.validate_path(".git/config")
        self.assertFalse(is_valid)
        self.assertIn("restricted", reason.lower())
    
    def test_scrub_environment(self):
        """Test environment variable scrubbing."""
        # Test with dangerous environment variables
        test_env = {
            'PATH': '/dangerous/path',
            'LD_PRELOAD': '/malicious/lib.so',
            'SAFE_VAR': 'safe_value',
            'PYTHONPATH': '/dangerous/python/path'
        }
        
        scrubbed_env = self.security_manager.scrub_environment(test_env)
        
        # Verify dangerous variables are removed
        self.assertNotIn('LD_PRELOAD', scrubbed_env)
        self.assertNotIn('PYTHONPATH', scrubbed_env)
        
        # Verify safe PATH is set
        self.assertEqual(scrubbed_env['PATH'], '/usr/bin:/bin')
        
        # Verify safe locale is set
        self.assertEqual(scrubbed_env['LC_ALL'], 'C')
        self.assertEqual(scrubbed_env['LANG'], 'C')
    
    def test_get_security_stats(self):
        """Test security statistics retrieval."""
        stats = self.security_manager.get_security_stats()
        
        self.assertIn('allowed_commands', stats)
        self.assertIn('allowed_commands_count', stats)
        self.assertIn('restricted_paths', stats)
        self.assertIn('restricted_paths_count', stats)
        self.assertIn('dangerous_patterns_count', stats)
        
        self.assertEqual(stats['allowed_commands_count'], 3)  # git, echo, ls
        self.assertEqual(stats['restricted_paths_count'], 2)  # .git/, node_modules/


class TestSecurityManagerExitConditions(unittest.TestCase):
    """Test specific exit conditions for TASK 1.2.1."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create mock config manager
        self.mock_config_manager = Mock(spec=ConfigManager)
        self.mock_config_manager.get_security_settings.return_value = {
            'allowed_commands': ['git', 'echo'],
            'restricted_paths': [],
            'dangerous_patterns': []
        }
        
        # Create security manager instance
        self.security_manager = SecurityManager(self.mock_config_manager)
    
    def tearDown(self):
        """Clean up test fixtures."""
        if hasattr(self, 'security_manager'):
            self.security_manager.stop()
    
    @patch('core.security_manager.subprocess.run')
    def test_task_1_2_1_exit_condition_shell_false(self, mock_subprocess_run):
        """
        TASK 1.2.1 EXIT CONDITION: The execute_command_safely method in 
        security_manager.py exclusively uses subprocess.run with shell=False.
        """
        # Setup mock subprocess result
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "success"
        mock_result.stderr = ""
        mock_subprocess_run.return_value = mock_result
        
        # Test multiple command executions
        test_commands = [
            ["git", "status"],
            ["echo", "hello"],
            ["git", "log", "--oneline"]
        ]
        
        for command_list in test_commands:
            # Reset mock for each test
            mock_subprocess_run.reset_mock()
            
            # Execute command
            self.security_manager.execute_command_safely(command_list)
            
            # CRITICAL ASSERTION: Verify shell=False is ALWAYS used
            mock_subprocess_run.assert_called_once()
            call_args = mock_subprocess_run.call_args
            
            self.assertIn('shell', call_args[1], 
                         f"shell parameter missing for command {command_list}")
            self.assertFalse(call_args[1]['shell'], 
                           f"shell=True detected for command {command_list} - SECURITY VIOLATION!")
            
            # Verify command_list is passed directly (not as string)
            self.assertIsInstance(call_args[0][0], list,
                                f"Command should be passed as list, got {type(call_args[0][0])}")
            self.assertEqual(call_args[0][0], command_list,
                           f"Command list not passed correctly: expected {command_list}, got {call_args[0][0]}")


if __name__ == '__main__':
    unittest.main() 