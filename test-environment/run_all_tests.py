#!/usr/bin/env python3
"""
Comprehensive Test Runner for Master Knowledge Base
Executes all tests and saves outputs to test-environment/
"""

import os
import sys
import subprocess
import datetime
import json
from pathlib import Path

# Add the master-knowledge-base tools to Python path
repo_root = Path(__file__).parent.parent
tools_path = repo_root / "master-knowledge-base" / "tools"
sys.path.insert(0, str(tools_path))

class TestRunner:
    def __init__(self):
        self.test_environment = Path(__file__).parent
        self.repo_root = self.test_environment.parent
        self.results = {
            "timestamp": datetime.datetime.now().isoformat(),
            "test_suites": {},
            "summary": {
                "total_suites": 0,
                "passed_suites": 0,
                "failed_suites": 0,
                "total_tests": 0,
                "passed_tests": 0,
                "failed_tests": 0
            }
        }
        
    def run_test_suite(self, test_file, suite_name):
        """Run a specific test suite and capture results"""
        print(f"\n{'='*60}")
        print(f"Running {suite_name}")
        print(f"{'='*60}")
        
        try:
            # Change to the directory containing the test file
            test_dir = Path(test_file).parent
            original_cwd = os.getcwd()
            os.chdir(test_dir)
            
            # Run the test
            result = subprocess.run(
                [sys.executable, "-m", "unittest", Path(test_file).name, "-v"],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            # Restore original directory
            os.chdir(original_cwd)
            
            # Parse results
            suite_result = {
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "passed": result.returncode == 0
            }
            
            # Count individual tests
            test_count = result.stdout.count("test_")
            if suite_result["passed"]:
                passed_count = test_count
                failed_count = 0
            else:
                # Try to parse failure count from output
                failed_count = result.stdout.count("FAIL")
                passed_count = test_count - failed_count
            
            suite_result["test_count"] = test_count
            suite_result["passed_count"] = passed_count
            suite_result["failed_count"] = failed_count
            
            self.results["test_suites"][suite_name] = suite_result
            
            # Update summary
            self.results["summary"]["total_suites"] += 1
            self.results["summary"]["total_tests"] += test_count
            self.results["summary"]["passed_tests"] += passed_count
            self.results["summary"]["failed_tests"] += failed_count
            
            if suite_result["passed"]:
                self.results["summary"]["passed_suites"] += 1
                print(f"✅ {suite_name} PASSED ({test_count} tests)")
            else:
                self.results["summary"]["failed_suites"] += 1
                print(f"❌ {suite_name} FAILED ({failed_count}/{test_count} tests failed)")
                print(f"Error output: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"⏰ {suite_name} TIMEOUT")
            self.results["test_suites"][suite_name] = {
                "exit_code": -1,
                "stdout": "",
                "stderr": "Test timed out after 5 minutes",
                "passed": False,
                "test_count": 0,
                "passed_count": 0,
                "failed_count": 1
            }
            self.results["summary"]["total_suites"] += 1
            self.results["summary"]["failed_suites"] += 1
            self.results["summary"]["failed_tests"] += 1
            
        except Exception as e:
            print(f"💥 {suite_name} ERROR: {e}")
            self.results["test_suites"][suite_name] = {
                "exit_code": -2,
                "stdout": "",
                "stderr": str(e),
                "passed": False,
                "test_count": 0,
                "passed_count": 0,
                "failed_count": 1
            }
            self.results["summary"]["total_suites"] += 1
            self.results["summary"]["failed_suites"] += 1
            self.results["summary"]["failed_tests"] += 1
    
    def run_all_tests(self):
        """Run all test suites in the repository"""
        print("🚀 Starting Comprehensive Test Suite")
        print(f"Test Environment: {self.test_environment}")
        print(f"Repository Root: {self.repo_root}")
        
        # Define test suites to run
        test_suites = [
            {
                "file": self.repo_root / "master-knowledge-base" / "tools" / "linter" / "tests" / "test_kb_linter.py",
                "name": "KB Linter Tests"
            },
            {
                "file": self.repo_root / "master-knowledge-base" / "tools" / "indexer" / "tests" / "test_generate_index.py",
                "name": "Index Generator Tests"
            },
            {
                "file": self.repo_root / "master-knowledge-base" / "tools" / "builder" / "tests" / "test_generate_collections.py",
                "name": "Collection Builder Tests"
            },
            {
                "file": self.repo_root / "master-knowledge-base" / "tools" / "naming-enforcer" / "test_include_functionality.py",
                "name": "Naming Enforcer Tests"
            }
        ]
        
        # Run each test suite
        for suite in test_suites:
            if suite["file"].exists():
                self.run_test_suite(suite["file"], suite["name"])
            else:
                print(f"⚠️  Test file not found: {suite['file']}")
                self.results["test_suites"][suite["name"]] = {
                    "exit_code": -3,
                    "stdout": "",
                    "stderr": f"Test file not found: {suite['file']}",
                    "passed": False,
                    "test_count": 0,
                    "passed_count": 0,
                    "failed_count": 1
                }
                self.results["summary"]["total_suites"] += 1
                self.results["summary"]["failed_suites"] += 1
                self.results["summary"]["failed_tests"] += 1
    
    def save_results(self):
        """Save test results to test-environment"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        
        # Save detailed JSON results
        json_file = self.test_environment / f"test-results-{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        # Save human-readable summary
        summary_file = self.test_environment / f"test-summary-{timestamp}.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"# Test Execution Summary\n\n")
            f.write(f"**Timestamp**: {self.results['timestamp']}\n")
            f.write(f"**Test Environment**: {self.test_environment}\n\n")
            
            f.write(f"## Overall Results\n\n")
            summary = self.results["summary"]
            f.write(f"- **Total Test Suites**: {summary['total_suites']}\n")
            f.write(f"- **Passed Suites**: {summary['passed_suites']}\n")
            f.write(f"- **Failed Suites**: {summary['failed_suites']}\n")
            f.write(f"- **Total Individual Tests**: {summary['total_tests']}\n")
            f.write(f"- **Passed Tests**: {summary['passed_tests']}\n")
            f.write(f"- **Failed Tests**: {summary['failed_tests']}\n\n")
            
            success_rate = (summary['passed_tests'] / summary['total_tests'] * 100) if summary['total_tests'] > 0 else 0
            f.write(f"**Success Rate**: {success_rate:.1f}%\n\n")
            
            f.write(f"## Test Suite Details\n\n")
            for suite_name, suite_result in self.results["test_suites"].items():
                status = "✅ PASSED" if suite_result["passed"] else "❌ FAILED"
                f.write(f"### {suite_name} - {status}\n\n")
                f.write(f"- **Exit Code**: {suite_result['exit_code']}\n")
                f.write(f"- **Test Count**: {suite_result['test_count']}\n")
                f.write(f"- **Passed**: {suite_result['passed_count']}\n")
                f.write(f"- **Failed**: {suite_result['failed_count']}\n\n")
                
                if suite_result["stderr"]:
                    f.write(f"**Error Output**:\n```\n{suite_result['stderr']}\n```\n\n")
        
        print(f"\n📊 Results saved to:")
        print(f"   - {json_file}")
        print(f"   - {summary_file}")
        
        return json_file, summary_file
    
    def print_final_summary(self):
        """Print final test summary"""
        print(f"\n{'='*60}")
        print("FINAL TEST SUMMARY")
        print(f"{'='*60}")
        
        summary = self.results["summary"]
        print(f"Total Test Suites: {summary['total_suites']}")
        print(f"Passed Suites: {summary['passed_suites']}")
        print(f"Failed Suites: {summary['failed_suites']}")
        print(f"Total Individual Tests: {summary['total_tests']}")
        print(f"Passed Tests: {summary['passed_tests']}")
        print(f"Failed Tests: {summary['failed_tests']}")
        
        if summary['total_tests'] > 0:
            success_rate = summary['passed_tests'] / summary['total_tests'] * 100
            print(f"Success Rate: {success_rate:.1f}%")
        
        if summary['failed_suites'] == 0:
            print("\n🎉 ALL TESTS PASSED!")
        else:
            print(f"\n⚠️  {summary['failed_suites']} test suite(s) failed")

def main():
    """Main test runner entry point"""
    runner = TestRunner()
    
    try:
        runner.run_all_tests()
        runner.save_results()
        runner.print_final_summary()
        
        # Exit with appropriate code
        if runner.results["summary"]["failed_suites"] > 0:
            sys.exit(1)
        else:
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Test execution interrupted by user")
        runner.save_results()
        sys.exit(130)
    except Exception as e:
        print(f"\n\n💥 Test runner error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 