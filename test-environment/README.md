# Test Environment

**Purpose**: Centralized location for ALL test setup, execution, and output in the Master Knowledge Base repository.

## Directory Structure

```
test-environment/
├── README.md                           # This file
├── run_all_tests.py                   # Comprehensive test runner
├── safety-test-suite.py               # Safety validation test suite
├── test-documents/                    # Test documents for validation
├── backup/                            # Test backups
├── tool-tests-consolidated-20250607-0942/  # Consolidated tool tests from tools directories
│   ├── linter-tests/                  # Tests for kb_linter.py
│   ├── builder-tests/                 # Tests for collection builder
│   └── indexer-tests/                 # Tests for index generator
├── test-results-YYYYMMDD-HHMM.json   # Detailed test results (JSON)
├── test-summary-YYYYMMDD-HHMM.md     # Human-readable test summaries
├── naming-enforcer-test-files.md     # Test files for naming enforcer
├── test-todos.json                   # Test TODO tracking
└── [other test files and outputs]
```

## Key Principles

### ✅ ALWAYS SETUP AND EXECUTE TESTS HERE
- **ALL test execution** must happen in this directory
- **ALL test outputs** (results, logs, reports) must be saved here
- **DIFFERENT FROM TOOLS!** - Tools contain production code, testing happens here
- **CONSOLIDATED STRUCTURE** - All tool tests moved from scattered locations to centralized structure

### ❌ NEVER TEST IN TOOLS DIRECTORIES
- Tool test directories have been consolidated into `test-environment/tool-tests-consolidated-*/`
- This ensures clean separation between production tools and testing infrastructure
- Maintains repository organization standards per repo-tree.md guidelines

## Recent Consolidation (2025-06-07)

### What Was Moved
- `tools/linter/tests/` → `test-environment/tool-tests-consolidated-20250607-0942/linter-tests/`
- `tools/builder/tests/` → `test-environment/tool-tests-consolidated-20250607-0942/builder-tests/`
- `tools/indexer/tests/` → `test-environment/tool-tests-consolidated-20250607-0942/indexer-tests/`

### Benefits
- **Clean Repository Structure**: Tools directories now contain only production code
- **Centralized Testing**: All test execution and outputs in one location
- **Better Organization**: Clear separation between code and testing infrastructure
- **Compliance**: Follows repository standards for test environment usage

## Usage

### Running All Tests
```bash
cd test-environment
python run_all_tests.py
```

### Running Specific Tool Tests
```bash
cd test-environment/tool-tests-consolidated-20250607-0942
# Run specific test suites as needed
```

### Test Runner Features
- **Comprehensive Coverage**: Runs all test suites across the repository
- **Centralized Output**: All results saved to test-environment/
- **Detailed Reporting**: Both JSON and Markdown output formats
- **Error Handling**: Graceful handling of timeouts and failures
- **Summary Statistics**: Overall success rates and detailed breakdowns

### Test Suites Included
1. **KB Linter Tests** - Validates knowledge base content and metadata
2. **Index Generator Tests** - Tests standards index generation
3. **Collection Builder Tests** - Tests collection document generation
4. **Naming Enforcer Tests** - Tests file naming convention enforcement
5. **Safety Test Suite** - Repository safety and integrity validation
6. **Consolidated Tool Tests** - All tool-specific tests in organized structure

## Output Files

### Test Results (JSON)
- **File Pattern**: `test-results-YYYYMMDD-HHMM.json`
- **Content**: Detailed test execution data, stdout/stderr, exit codes
- **Usage**: Machine-readable results for automation and analysis

### Test Summary (Markdown)
- **File Pattern**: `test-summary-YYYYMMDD-HHMM.md`
- **Content**: Human-readable test summary with success rates
- **Usage**: Quick review of test status and failures

## Integration with Repository Standards

### Compliance with Repository Rules
- **Archive Policy**: Test outputs remain in test-environment/ (not archived)
- **Tracking**: Test execution tracked in progress documents when part of roadmaps
- **Quality Gates**: Test results used for validation in project completion criteria
- **Organization**: Follows repo-tree.md guidelines for test environment usage

### Relationship to Tools
- **Tools Directory**: Contains production code and utilities only
- **Test Environment**: Executes tests and stores all outputs
- **Clear Separation**: Maintains clean separation between production code and testing infrastructure
- **Consolidated Structure**: All tool tests organized in timestamped consolidated directories

## Maintenance

### Regular Tasks
1. **Periodic Cleanup**: Remove old test results (keep recent 10-20 runs)
2. **Test Updates**: Update test runner when new test suites are added
3. **Documentation**: Keep this README updated with new test suites
4. **Consolidation**: When adding new tool tests, add to consolidated structure

### Adding New Test Suites
1. Add test files to appropriate consolidated directory or create new one
2. Update `run_all_tests.py` test_suites list if needed
3. Ensure tests follow unittest framework conventions
4. Test the addition with a dry run
5. Update this README with new test suite description

### Archive Management
- **Tool Tests**: Consolidated directories are timestamped for historical tracking
- **Results**: Test results remain in test-environment for analysis
- **Cleanup**: Periodic cleanup of old consolidated test directories as needed

---

**Last Updated**: 2025-06-07 09:45:00 (Consolidated tool tests and updated structure)
**Maintained By**: Repository automation and project teams 