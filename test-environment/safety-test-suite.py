#!/usr/bin/env python3
"""
Safety Test Suite for Knowledge Base Tools

Comprehensive testing of date-time-manager.py and todo-tracker.py
to ensure they are safe for production use.
"""

import os
import sys
import shutil
import tempfile
import subprocess
import json
from pathlib import Path
from datetime import datetime

class SafetyTestSuite:
    def __init__(self):
        self.test_dir = Path("test-environment")
        self.tools_dir = Path("tools")
        self.results = {
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "errors": [],
            "warnings": []
        }
    
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
        
        if level == "ERROR":
            self.results["errors"].append(message)
        elif level == "WARNING":
            self.results["warnings"].append(message)
    
    def run_test(self, test_name, test_func):
        """Run a single test with error handling"""
        self.results["tests_run"] += 1
        self.log(f"Running test: {test_name}")
        
        try:
            result = test_func()
            if result:
                self.results["tests_passed"] += 1
                self.log(f"✅ PASSED: {test_name}")
                return True
            else:
                self.results["tests_failed"] += 1
                self.log(f"❌ FAILED: {test_name}", "ERROR")
                return False
        except Exception as e:
            self.results["tests_failed"] += 1
            self.log(f"❌ ERROR in {test_name}: {str(e)}", "ERROR")
            return False
    
    def backup_test_files(self):
        """Create backup of test files"""
        backup_dir = self.test_dir / "backup"
        if backup_dir.exists():
            shutil.rmtree(backup_dir)
        shutil.copytree(self.test_dir / "test-documents", backup_dir)
        self.log("Created backup of test files")
    
    def restore_test_files(self):
        """Restore test files from backup"""
        backup_dir = self.test_dir / "backup"
        test_docs = self.test_dir / "test-documents"
        
        if test_docs.exists():
            shutil.rmtree(test_docs)
        shutil.copytree(backup_dir, test_docs)
        self.log("Restored test files from backup")
    
    def test_todo_tracker_safety(self):
        """Test TODO tracker for safety issues"""
        script_path = self.tools_dir / "todo-tracker.py"
        test_docs = self.test_dir / "test-documents"
        
        # Test 1: Basic scan without errors
        try:
            result = subprocess.run([
                sys.executable, str(script_path), 
                "scan", "--directory", str(test_docs),
                "--output", str(self.test_dir / "test-todos.json")
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                self.log(f"TODO tracker failed: {result.stderr}", "ERROR")
                return False
            
            # Check if output file was created
            output_file = self.test_dir / "test-todos.json"
            if not output_file.exists():
                self.log("TODO tracker didn't create output file", "ERROR")
                return False
            
            # Validate JSON output
            with open(output_file, 'r') as f:
                data = json.load(f)
                if "todos" not in data:
                    self.log("Invalid JSON structure from TODO tracker", "ERROR")
                    return False
            
            self.log(f"TODO tracker found {len(data['todos'])} TODOs")
            return True
            
        except subprocess.TimeoutExpired:
            self.log("TODO tracker timed out", "ERROR")
            return False
        except Exception as e:
            self.log(f"TODO tracker exception: {str(e)}", "ERROR")
            return False
    
    def test_date_time_manager_safety(self):
        """Test date-time manager with safety checks"""
        script_path = self.tools_dir / "frontmatter-management" / "date-time-manager.py"
        test_docs = self.test_dir / "test-documents"
        
        # Test on a single file first (least risk)
        test_file = test_docs / "sample1.md"
        
        try:
            # Read original content
            with open(test_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Test dry run (update command without force)
            result = subprocess.run([
                sys.executable, str(script_path),
                "update", str(test_file),
                "--date", "2025-01-11"
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                self.log(f"Date-time manager failed: {result.stderr}", "ERROR")
                return False
            
            # Read updated content
            with open(test_file, 'r', encoding='utf-8') as f:
                updated_content = f.read()
            
            # Verify file wasn't corrupted
            if "---" not in updated_content or "title:" not in updated_content:
                self.log("Date-time manager corrupted frontmatter", "ERROR")
                return False
            
            # Verify date was updated
            if "2025-01-11" not in updated_content:
                self.log("Date-time manager didn't update date", "ERROR")
                return False
            
            self.log("Date-time manager updated file successfully")
            return True
            
        except subprocess.TimeoutExpired:
            self.log("Date-time manager timed out", "ERROR")
            return False
        except Exception as e:
            self.log(f"Date-time manager exception: {str(e)}", "ERROR")
            return False
    
    def test_date_time_manager_lock_safety(self):
        """Test date locking mechanism"""
        script_path = self.tools_dir / "frontmatter-management" / "date-time-manager.py"
        test_file = self.test_dir / "test-documents" / "sample2.md"  # Has date-locked marker
        
        try:
            # Try to update locked file (should be skipped)
            result = subprocess.run([
                sys.executable, str(script_path),
                "update", str(test_file),
                "--date", "2025-01-11"
            ], capture_output=True, text=True, timeout=30)
            
            if "dates are locked" not in result.stdout:
                self.log("Date locking mechanism not working", "ERROR")
                return False
            
            self.log("Date locking mechanism working correctly")
            return True
            
        except Exception as e:
            self.log(f"Lock test exception: {str(e)}", "ERROR")
            return False
    
    def test_file_integrity(self):
        """Test that files maintain their integrity"""
        test_docs = self.test_dir / "test-documents"
        
        # Check all test files are readable and have expected content
        for md_file in test_docs.glob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if len(content) < 10:  # Suspiciously small
                    self.log(f"File {md_file} appears corrupted (too small)", "ERROR")
                    return False
                
                # Check for basic markdown structure
                if md_file.name != "no-frontmatter.md" and "---" not in content:
                    self.log(f"File {md_file} missing frontmatter markers", "ERROR")
                    return False
                    
            except UnicodeDecodeError:
                self.log(f"File {md_file} has encoding issues", "ERROR")
                return False
            except Exception as e:
                self.log(f"Error reading {md_file}: {str(e)}", "ERROR")
                return False
        
        self.log("All test files maintain integrity")
        return True
    
    def test_error_handling(self):
        """Test error handling with invalid inputs"""
        script_path = self.tools_dir / "frontmatter-management" / "date-time-manager.py"
        
        # Test with non-existent file
        result = subprocess.run([
            sys.executable, str(script_path),
            "update", "non-existent-file.md",
            "--date", "2025-01-11"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            self.log("Script didn't handle non-existent file properly", "WARNING")
        
        # Test with invalid date format
        test_file = self.test_dir / "test-documents" / "sample1.md"
        result = subprocess.run([
            sys.executable, str(script_path),
            "update", str(test_file),
            "--date", "invalid-date"
        ], capture_output=True, text=True)
        
        if "Invalid date format" not in result.stderr and result.returncode == 0:
            self.log("Script didn't handle invalid date format", "WARNING")
        
        self.log("Error handling tests completed")
        return True
    
    def run_all_tests(self):
        """Run comprehensive safety test suite"""
        self.log("🧪 Starting Safety Test Suite")
        self.log("=" * 50)
        
        # Backup test files
        self.backup_test_files()
        
        # Run tests
        tests = [
            ("File Integrity Check", self.test_file_integrity),
            ("TODO Tracker Safety", self.test_todo_tracker_safety),
            ("Date-Time Manager Basic Safety", self.test_date_time_manager_safety),
            ("Date Locking Mechanism", self.test_date_time_manager_lock_safety),
            ("Error Handling", self.test_error_handling),
        ]
        
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
            # Restore files after each test
            if test_name != "File Integrity Check":
                self.restore_test_files()
        
        # Final results
        self.log("=" * 50)
        self.log("🏁 Test Suite Complete")
        self.log(f"Tests Run: {self.results['tests_run']}")
        self.log(f"Tests Passed: {self.results['tests_passed']}")
        self.log(f"Tests Failed: {self.results['tests_failed']}")
        
        if self.results['errors']:
            self.log("❌ ERRORS FOUND:")
            for error in self.results['errors']:
                self.log(f"  - {error}")
        
        if self.results['warnings']:
            self.log("⚠️  WARNINGS:")
            for warning in self.results['warnings']:
                self.log(f"  - {warning}")
        
        # Safety assessment
        if self.results['tests_failed'] == 0 and len(self.results['errors']) == 0:
            self.log("✅ SAFETY ASSESSMENT: SCRIPTS ARE SAFE FOR PRODUCTION")
            return True
        else:
            self.log("🚨 SAFETY ASSESSMENT: SCRIPTS NEED FIXES BEFORE PRODUCTION")
            return False

if __name__ == "__main__":
    test_suite = SafetyTestSuite()
    safe = test_suite.run_all_tests() 